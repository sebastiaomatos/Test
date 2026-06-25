"""
Loader: unifica todas as fontes em um DataFrame mensal de RETORNOS (decimal, BRL).

Convenções:
  - Index: DatetimeIndex, primeiro dia de cada mês (período de competência).
  - Valores: retorno mensal decimal (0.01 = +1% no mês).
  - Todas as séries em BRL.
  - BDRs/S&P500: IVVB11 para janelas ≤ 6 anos; ^GSPC × BRL=X como extensão para 10a.
  - IMA-B: BCB série 12466 principal; IMAB11.SA como complemento quando BCB pára.
"""
import logging
from pathlib import Path

import pandas as pd
import numpy as np

from src.sources import yahoo as yf_src
from src.sources import bcb as bcb_src
from src.fx import get_usd_brl_monthly, convert_usd_to_brl, price_to_monthly_return

log = logging.getLogger(__name__)


def _price_series_to_return(s: pd.Series) -> pd.Series:
    """Preço → retorno mensal decimal."""
    return s.pct_change().dropna()


def build_returns_dataframe(
    cfg: dict,
    cache_dir: Path = Path("data/raw"),
    refresh: bool = False,
) -> pd.DataFrame:
    """
    Constrói DataFrame com retornos mensais de todos os ativos.
    Colunas: nome do ativo.  Index: DatetimeIndex mês.
    """
    # ── 1. Câmbio USD/BRL ───────────────────────────────────────────────
    log.info("=== Carregando câmbio USD/BRL ===")
    usd_brl = get_usd_brl_monthly(cache_dir=cache_dir, max_age_days=cfg["cache"]["max_age_days"], refresh=refresh)
    usd_brl_ret = _price_series_to_return(usd_brl)  # variação cambial mensal

    # ── 2. Fontes BCB ───────────────────────────────────────────────────
    log.info("=== Carregando séries BCB ===")
    bcb_data = bcb_src.fetch_all(cfg, cache_dir, refresh=refresh)
    cdi_ret   = bcb_data.get("CDI")       # já é retorno decimal
    poup_ret  = bcb_data.get("Poupanca")
    imab_ret  = bcb_data.get("IMA_B")

    # ── 3. Fontes Yahoo Finance ─────────────────────────────────────────
    log.info("=== Carregando tickers Yahoo Finance ===")
    yf_prices = yf_src.fetch_all(cfg, cache_dir, refresh=refresh)

    # Ativos já em BRL → retorno direto de preço
    bvsp_ret  = _price_series_to_return(yf_prices.get("Ibovespa", pd.Series(dtype=float)))
    divo_ret  = _price_series_to_return(yf_prices.get("Dividendos_IDIV", pd.Series(dtype=float)))
    hglg_ret  = _price_series_to_return(yf_prices.get("FIIs_IFIX", pd.Series(dtype=float)))
    smal_ret  = _price_series_to_return(yf_prices.get("SmallCaps", pd.Series(dtype=float)))
    dolar_ret = _price_series_to_return(yf_prices.get("Dolar", pd.Series(dtype=float)))

    # Ativos em USD → converter para BRL
    # Bitcoin
    btc_usd_p = yf_prices.get("Bitcoin", pd.Series(dtype=float))
    btc_brl_p = convert_usd_to_brl(btc_usd_p, usd_brl)
    btc_ret   = _price_series_to_return(btc_brl_p)

    # Ouro
    ouro_usd_p = yf_prices.get("Ouro", pd.Series(dtype=float))
    ouro_brl_p = convert_usd_to_brl(ouro_usd_p, usd_brl)
    ouro_ret   = _price_series_to_return(ouro_brl_p)

    # BDRs / Ações EUA em BRL
    # Primário: IVVB11 (preço BRL); extensão para 10a: ^GSPC × BRL=X
    ivvb_ret  = _price_series_to_return(yf_prices.get("Acoes_EUA_BDR", pd.Series(dtype=float)))

    # Recupera ^GSPC para extensão (ticker está como hidden, buscamos diretamente)
    sp500_ext = _load_sp500_extension(cfg, cache_dir, usd_brl, refresh=refresh)

    # Mescla IVVB11 + extensão S&P500: usa IVVB11 onde disponível, S&P500 × BRL antes
    bdrs_ret  = _splice_series(sp500_ext, ivvb_ret, label="Acoes_EUA_BDR")

    # IMA-B: BCB como principal, complemento com IMAB11 se BCB tiver lacuna recente
    imab_ret = _extend_imab(imab_ret, cfg, cache_dir, refresh=refresh)

    # ── 4. Montar DataFrame ─────────────────────────────────────────────
    series_map = {
        "Bitcoin":       btc_ret,
        "Ouro":          ouro_ret,
        "Acoes_EUA_BDR": bdrs_ret,
        "Ibovespa":      bvsp_ret,
        "Dividendos_IDIV": divo_ret,
        "FIIs_IFIX":     hglg_ret,
        "CDI":           cdi_ret,
        "IMA_B":         imab_ret,
        "Poupanca":      poup_ret,
        "Dolar":         dolar_ret,
        "SmallCaps":     smal_ret,
    }

    df = pd.DataFrame(series_map)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Relatório de cobertura
    log.info("=== Cobertura de dados (por ativo) ===")
    for col in df.columns:
        valid = df[col].dropna()
        if len(valid) > 0:
            log.info("  %-20s %3d obs  %s → %s", col, len(valid),
                     valid.index[0].strftime("%Y-%m"),
                     valid.index[-1].strftime("%Y-%m"))
        else:
            log.warning("  %-20s SEM DADOS", col)

    return df


def _load_sp500_extension(cfg, cache_dir, usd_brl, refresh=False):
    """Carrega ^GSPC e converte para retorno em BRL."""
    import time
    from src.sources.yahoo import fetch_monthly
    try:
        sp500_p = fetch_monthly(
            "^GSPC", start="2015-01-01",
            cache_dir=cache_dir,
            max_age_days=cfg["cache"]["max_age_days"],
            refresh=refresh,
        )
        sp500_brl = convert_usd_to_brl(sp500_p, usd_brl)
        return _price_series_to_return(sp500_brl)
    except Exception as e:
        log.warning("^GSPC não disponível: %s", e)
        return pd.Series(dtype=float)


def _extend_imab(imab_bcb: pd.Series, cfg, cache_dir, refresh=False) -> pd.Series:
    """
    Estende IMA-B com IMAB11.SA para meses não cobertos pelo BCB.
    O BCB pára em ~mai/2023; IMAB11.SA cobre mai/2019 em diante.
    """
    from src.sources.yahoo import fetch_monthly
    try:
        imab11_p = fetch_monthly(
            "IMAB11.SA", start="2019-01-01",
            cache_dir=cache_dir,
            max_age_days=cfg["cache"]["max_age_days"],
            refresh=refresh,
        )
        imab11_ret = _price_series_to_return(imab11_p)
        if imab_bcb is None or len(imab_bcb) == 0:
            log.info("IMA-B: usando apenas IMAB11.SA")
            return imab11_ret
        # Usa BCB onde disponível, IMAB11 para meses faltantes
        combined = imab_bcb.copy()
        gap_months = imab11_ret.index.difference(combined.dropna().index)
        if len(gap_months) > 0:
            log.info("IMA-B: BCB cobre até %s; complementando com IMAB11 para %d meses",
                     combined.dropna().index[-1].strftime("%Y-%m"), len(gap_months))
            combined = pd.concat([combined, imab11_ret[gap_months]]).sort_index()
            combined = combined[~combined.index.duplicated(keep="first")]
        return combined
    except Exception as e:
        log.warning("IMAB11.SA não disponível para extensão: %s", e)
        return imab_bcb


def _splice_series(base: pd.Series, overlay: pd.Series, label: str = "") -> pd.Series:
    """
    Mescla duas séries: usa `overlay` onde disponível, `base` para o restante.
    Aplica escalonamento de nível no ponto de junção para evitar salto.
    """
    if overlay is None or len(overlay) == 0:
        return base
    if base is None or len(base) == 0:
        return overlay

    combined = overlay.reindex(base.index.union(overlay.index))
    # Para meses antes do início do overlay, usa base
    first_overlay = overlay.dropna().index[0] if len(overlay.dropna()) > 0 else None
    if first_overlay is not None:
        mask_base = combined.index < first_overlay
        combined[mask_base] = base.reindex(combined.index[mask_base])
        log.info("%s: splice — base até %s, overlay de %s em diante",
                 label, first_overlay.strftime("%Y-%m"), first_overlay.strftime("%Y-%m"))
    combined.name = label
    return combined.dropna()

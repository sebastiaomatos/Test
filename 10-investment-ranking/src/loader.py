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
    O BCB pára em mai/2023. IMAB11.SA tem dados estragados (preço congelado=79.50)
    de Abr/2022 a Dez/2025; usamos IMAB11 apenas a partir de Jan/2026.

    NOTA DE QUALIDADE: gap Jun/2023-Dez/2025 (31 meses) sem dados confiáveis.
    Para janelas que caem neste período, IMA-B terá cobertura reduzida (NaN).
    """
    from src.sources.yahoo import fetch_monthly
    import numpy as np

    # Último mês bom do BCB
    bcb_end = imab_bcb.dropna().index[-1] if (imab_bcb is not None and len(imab_bcb) > 0) else None

    try:
        imab11_p = fetch_monthly(
            "IMAB11.SA", start="2019-01-01",
            cache_dir=cache_dir,
            max_age_days=cfg["cache"]["max_age_days"],
            refresh=refresh,
        )

        # Filtra preços estragados: qualquer sequência de preço constante >= 5 meses = estale
        # Método: marcar NaN onde o preço não muda por 3+ meses consecutivos
        price_diff = imab11_p.diff().abs()
        rolling_min = price_diff.rolling(3, min_periods=3).min()
        stale_mask = (rolling_min == 0.0) & (imab11_p == 79.5)
        n_stale = stale_mask.sum()
        if n_stale > 0:
            log.warning("IMA-B: IMAB11.SA tem %d meses com preço estagnado (=79.50) — marcados NaN", n_stale)
            # Marca meses com preço estagnado (e um mês antes do retorno ao preço real) como NaN
            # De forma conservadora: marca NaN do início do stale até o mês antes do primeiro preço "vivo"
            stale_months = imab11_p.index[stale_mask]
            if len(stale_months) > 0:
                stale_start = stale_months[0]
                stale_end = stale_months[-1]
                imab11_p.loc[stale_start:stale_end] = np.nan
                log.warning("IMA-B: preços IMAB11 zerados para %s a %s",
                            stale_start.strftime("%Y-%m"), stale_end.strftime("%Y-%m"))

        imab11_ret = _price_series_to_return(imab11_p)
        # Remove NaN (meses estragados)
        imab11_ret = imab11_ret.dropna()

        if imab_bcb is None or len(imab_bcb) == 0:
            log.info("IMA-B: usando apenas IMAB11.SA (após limpeza)")
            return imab11_ret

        # Combina: BCB como principal, IMAB11 apenas para meses APÓS o final do BCB
        combined = imab_bcb.copy()
        post_bcb = imab11_ret[imab11_ret.index > (bcb_end if bcb_end else pd.Timestamp("2023-05-01"))]
        if len(post_bcb) > 0:
            log.info("IMA-B: BCB cobre até %s; IMAB11 (limpo) complementa %d meses a partir de %s",
                     bcb_end.strftime("%Y-%m") if bcb_end else "N/A",
                     len(post_bcb), post_bcb.index[0].strftime("%Y-%m"))
            combined = pd.concat([combined, post_bcb]).sort_index()
            combined = combined[~combined.index.duplicated(keep="first")]
        else:
            log.warning("IMA-B: IMAB11 não tem dados válidos após BCB — gap Jun/2023-Dez/2025 sem cobertura")

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

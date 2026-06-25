"""
Fonte: Banco Central do Brasil — API SGS (Sistema Gerenciador de Séries Temporais).

Endpoint: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{id}/dados
Séries usadas:
  4391 — CDI acumulado mensal (% ao mês)
   196 — Poupança rendimento mensal (% ao mês)
 12466 — IMA-B preço diário (índice)
   433 — IPCA mensal (% ao mês) — referência
"""
import logging
import time
from pathlib import Path
from datetime import datetime, timedelta, date

import pandas as pd
import requests

log = logging.getLogger(__name__)

BCB_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}/dados"
# Janela máxima para séries diárias é 10 anos; séries mensais não têm limite declarado


def _cache_path(cache_dir: Path, series_id: int) -> Path:
    return cache_dir / f"bcb_{series_id}.parquet"


def _is_fresh(path: Path, max_age_days: int) -> bool:
    if not path.exists():
        return False
    age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
    return age < timedelta(days=max_age_days)


def _fetch_bcb_raw(
    series_id: int,
    start: str,
    end: str,
    max_retries: int = 4,
) -> list[dict]:
    """Baixa dados brutos do SGS em formato JSON."""
    url = BCB_BASE.format(series_id=series_id)
    params = {"dataInicial": start, "dataFinal": end, "formato": "json"}
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and "error" in data:
                raise ValueError(f"BCB API erro: {data}")
            return data
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                log.warning("BCB %d tentativa %d/%d: %s — aguarda %ds",
                            series_id, attempt + 1, max_retries, e, wait)
                time.sleep(wait)
            else:
                raise


def fetch_monthly_series(
    series_id: int,
    start: str = "2015-01-01",
    end: str | None = None,
    cache_dir: Path = Path("data/raw"),
    max_age_days: int = 1,
    refresh: bool = False,
) -> pd.Series:
    """
    Retorna série mensal de retorno (%) — para CDI e Poupança.
    Divide por 100 e converte para decimal: 0.97 → 0.0097.
    Index: DatetimeIndex primeiro dia do mês.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cp = _cache_path(cache_dir, series_id)

    if not refresh and _is_fresh(cp, max_age_days):
        s = pd.read_parquet(cp).squeeze()
        log.info("CACHE BCB %d: %d obs (%s - %s)", series_id, len(s),
                 s.index[0].date(), s.index[-1].date())
        return s

    if end is None:
        end = datetime.today().strftime("%d/%m/%Y")
    start_fmt = datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")

    raw = _fetch_bcb_raw(series_id, start_fmt, end)
    df = pd.DataFrame(raw)
    df["date"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["value"] = pd.to_numeric(df["valor"].str.replace(",", "."), errors="coerce")
    df = df.set_index("date").sort_index()
    # Normaliza para primeiro dia do mês
    df.index = df.index.to_period("M").to_timestamp()
    s = df["value"].groupby(level=0).last()  # pega último se duplicado
    s = s / 100.0  # converte % para decimal
    s.name = f"bcb_{series_id}"

    pd.DataFrame(s).to_parquet(cp)
    log.info("BAIXOU BCB %d: %d obs (%s - %s)", series_id, len(s),
             s.index[0].date(), s.index[-1].date())
    return s


def fetch_imab_daily_to_monthly(
    series_id: int = 12466,
    start: str = "2015-01-01",
    end: str | None = None,
    cache_dir: Path = Path("data/raw"),
    max_age_days: int = 1,
    refresh: bool = False,
) -> pd.Series:
    """
    IMA-B: série de preço diário do BCB → retorno mensal (fim-de-mês vs fim-do-mês-anterior).
    O BCB limita a 10 anos para séries diárias; fazemos duas requisições se necessário.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cp = _cache_path(cache_dir, series_id)

    if not refresh and _is_fresh(cp, max_age_days):
        s = pd.read_parquet(cp).squeeze()
        log.info("CACHE BCB %d (IMA-B mensal): %d obs (%s - %s)", series_id, len(s),
                 s.index[0].date(), s.index[-1].date())
        return s

    if end is None:
        end = datetime.today()
    else:
        end = datetime.strptime(end, "%Y-%m-%d")

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    # Limite BCB: janela de 10 anos para série diária
    limit = timedelta(days=365 * 10 - 1)
    chunks = []
    cur = start_dt
    while cur < end:
        chunk_end = min(cur + limit, end)
        raw = _fetch_bcb_raw(
            series_id,
            cur.strftime("%d/%m/%Y"),
            chunk_end.strftime("%d/%m/%Y"),
        )
        chunks.extend(raw)
        cur = chunk_end + timedelta(days=1)
        if cur < end:
            time.sleep(1)

    df = pd.DataFrame(chunks)
    df["date"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["price"] = pd.to_numeric(df["valor"].str.replace(",", "."), errors="coerce")
    df = df.set_index("date").sort_index()
    df = df[~df.index.duplicated(keep="last")]

    # Fim de cada mês → retorno mensal
    monthly_eom = df["price"].resample("ME").last()
    ret = monthly_eom.pct_change().dropna()
    # Normaliza index para primeiro dia do mês
    ret.index = ret.index.to_period("M").to_timestamp()
    ret.name = f"bcb_{series_id}"

    pd.DataFrame(ret).to_parquet(cp)
    log.info("BAIXOU BCB %d (IMA-B): %d obs mensais (%s - %s)", series_id, len(ret),
             ret.index[0].date(), ret.index[-1].date())
    return ret


def fetch_all(cfg: dict, cache_dir: Path, refresh: bool = False) -> dict[str, pd.Series]:
    """Baixa todas as séries BCB do config e retorna dict nome->série de retorno."""
    results: dict[str, pd.Series] = {}
    for name, info in cfg["bcb_series"].items():
        if info.get("hidden"):
            continue
        sid = info["series_id"]
        start = "2015-01-01"
        log.info("Buscando BCB %s (série %d)...", name, sid)
        try:
            if info["unit"] == "index_price":
                s = fetch_imab_daily_to_monthly(
                    series_id=sid, start=start, cache_dir=cache_dir,
                    max_age_days=cfg["cache"]["max_age_days"], refresh=refresh,
                )
            else:
                s = fetch_monthly_series(
                    series_id=sid, start=start, cache_dir=cache_dir,
                    max_age_days=cfg["cache"]["max_age_days"], refresh=refresh,
                )
            results[name] = s
        except Exception as e:
            log.error("Falha BCB %s: %s", name, e)
    return results

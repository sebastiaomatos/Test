"""
Fonte: Yahoo Finance via yfinance + curl_cffi.

Usa curl_cffi como sessão para contornar TLS do proxy corporativo.
CURL_CA_BUNDLE deve estar setado para /root/.ccr/ca-bundle.crt (ou equivalente).
Cache em parquet por ticker; reusa se < max_age_days.
"""
import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

log = logging.getLogger(__name__)

CA_BUNDLE = os.environ.get("CURL_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")
_SESSION = None


def _get_session():
    global _SESSION
    if _SESSION is None:
        try:
            from curl_cffi import requests as cf
            _SESSION = cf.Session(impersonate="chrome110", verify=CA_BUNDLE)
            log.debug("curl_cffi session criada (CA=%s)", CA_BUNDLE)
        except ImportError:
            log.warning("curl_cffi não encontrado; usando requests padrão")
            import requests
            _SESSION = requests.Session()
    return _SESSION


def _cache_path(cache_dir: Path, ticker: str) -> Path:
    safe = ticker.replace("^", "IDX_").replace("=", "FX_").replace("/", "_")
    return cache_dir / f"{safe}.parquet"


def _is_fresh(path: Path, max_age_days: int) -> bool:
    if not path.exists():
        return False
    age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
    return age < timedelta(days=max_age_days)


def fetch_monthly(
    ticker: str,
    start: str = "2015-01-01",
    end: str | None = None,
    cache_dir: Path = Path("data/raw"),
    max_age_days: int = 1,
    refresh: bool = False,
    retry_delay: float = 2.0,
    max_retries: int = 4,
) -> pd.Series:
    """
    Retorna série mensal de preço de fechamento ajustado (Close).
    Index: DatetimeIndex (último dia útil do mês, UTC normalizado).
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cp = _cache_path(cache_dir, ticker)

    if not refresh and _is_fresh(cp, max_age_days):
        s = pd.read_parquet(cp).squeeze()
        log.info("CACHE %s: %d obs (%s - %s)", ticker, len(s), s.index[0].date(), s.index[-1].date())
        return s

    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    import yfinance as yf
    session = _get_session()

    for attempt in range(max_retries):
        try:
            t = yf.Ticker(ticker, session=session)
            h = t.history(start=start, end=end, interval="1mo", auto_adjust=True)
            if h.empty:
                raise ValueError(f"Sem dados para {ticker}")
            s = h["Close"].rename(ticker)
            s.index = pd.to_datetime(s.index).tz_localize(None)
            # Normaliza para primeiro dia do mês (convenção: identifica o mês)
            s.index = s.index.to_period("M").to_timestamp()
            s = s[~s.index.duplicated(keep="last")]
            s = s.sort_index()
            pd.DataFrame(s).to_parquet(cp)
            log.info("BAIXOU %s: %d obs (%s - %s)", ticker, len(s), s.index[0].date(), s.index[-1].date())
            return s
        except Exception as e:
            if attempt < max_retries - 1:
                wait = retry_delay * (2 ** attempt)
                log.warning("Tentativa %d/%d falhou para %s: %s — aguarda %.0fs",
                            attempt + 1, max_retries, ticker, e, wait)
                time.sleep(wait)
            else:
                log.error("Falha definitiva para %s após %d tentativas: %s", ticker, max_retries, e)
                raise


def fetch_all(cfg: dict, cache_dir: Path, refresh: bool = False) -> dict[str, pd.Series]:
    """Baixa todos os tickers do config.yaml e retorna dict nome->série de preço."""
    results: dict[str, pd.Series] = {}
    for name, info in cfg["yahoo_tickers"].items():
        if info.get("hidden"):
            continue
        ticker = info["ticker"]
        start = info.get("start", "2015-01-01")
        log.info("Buscando %s (%s)...", name, ticker)
        try:
            s = fetch_monthly(ticker, start=start, cache_dir=cache_dir,
                               max_age_days=cfg["cache"]["max_age_days"], refresh=refresh)
            results[name] = s
            time.sleep(0.4)
        except Exception as e:
            log.error("Falha %s: %s", name, e)
    return results

"""
Conversão USD → BRL por fim de mês usando PTAX (BRL=X via Yahoo Finance).

Retorna pd.Series com taxa USD/BRL no último dia útil de cada mês.
"""
import logging
from pathlib import Path

import pandas as pd

from src.sources.yahoo import fetch_monthly

log = logging.getLogger(__name__)


def get_usd_brl_monthly(
    cache_dir: Path = Path("data/raw"),
    max_age_days: int = 1,
    refresh: bool = False,
) -> pd.Series:
    """
    Série mensal de câmbio USD/BRL.
    Returns: pd.Series com valores em BRL por 1 USD; index = primeiro dia do mês.
    """
    s = fetch_monthly(
        "BRL=X",
        start="2015-01-01",
        cache_dir=cache_dir,
        max_age_days=max_age_days,
        refresh=refresh,
    )
    s.name = "USD_BRL"
    return s


def convert_usd_to_brl(
    price_usd: pd.Series,
    usd_brl: pd.Series,
) -> pd.Series:
    """
    Converte preço em USD para BRL multiplicando pelas taxas de câmbio.
    Os índices são alinhados por mês (inner join) antes da multiplicação.
    """
    aligned = price_usd.align(usd_brl, join="inner")
    brl = aligned[0] * aligned[1]
    brl.name = price_usd.name
    return brl


def price_to_monthly_return(price: pd.Series) -> pd.Series:
    """Converte série de preço em retorno mensal percentual."""
    ret = price.pct_change().dropna()
    ret.name = price.name
    return ret

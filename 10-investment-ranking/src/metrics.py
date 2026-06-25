"""
Cálculo das métricas de performance para janelas móveis.

Métricas por ativo × janela:
  - geom_monthly:   (1+R_total)^(1/n) - 1   [média mensal geométrica]
  - total_return:   produto dos (1+r_i) - 1
  - cagr:           (1+total_return)^(12/n) - 1
  - arith_monthly:  média aritmética dos retornos mensais
  - vol_monthly:    desvio-padrão dos retornos mensais (amostral)
  - ret_risk_vs_cdi: (geom_monthly - cdi_geom_monthly) / vol_monthly
"""
import logging
from datetime import date

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def reference_date(cfg: dict) -> date:
    """Retorna a data de referência (último dia do último mês civil fechado)."""
    if cfg.get("ref_date", "auto") == "auto":
        today = date.today()
        # Último mês fechado = mês anterior ao mês atual
        if today.month == 1:
            ref = date(today.year - 1, 12, 31)
        else:
            ref = date(today.year, today.month - 1, 1)
            # último dia do mês anterior
            import calendar
            last_day = calendar.monthrange(ref.year, ref.month)[1]
            ref = date(ref.year, ref.month, last_day)
        return ref
    else:
        return date.fromisoformat(cfg["ref_date"])


def window_slice(returns: pd.Series, ref: date, years: int) -> pd.Series:
    """
    Retorna fatia de `years` anos fechados até `ref`.
    O índice do DataFrame usa primeiro dia do mês; selecionamos até o mês de ref.
    """
    end_period = pd.Period(ref, freq="M")
    start_period = end_period - (years * 12 - 1)
    start_ts = start_period.to_timestamp()
    end_ts = end_period.to_timestamp()
    sliced = returns.loc[start_ts:end_ts]
    return sliced.dropna()


def compute_metrics(returns_slice: pd.Series) -> dict:
    """
    Calcula todas as métricas de performance dado vetor de retornos mensais.
    returns_slice: pd.Series de retornos decimais (ex: 0.01 = +1%).
    """
    n = len(returns_slice)
    if n == 0:
        return _empty_metrics()

    r = returns_slice.values.astype(float)

    # Retorno total acumulado
    total_return = float(np.prod(1.0 + r) - 1.0)

    # Média mensal geométrica
    geom_monthly = float((1.0 + total_return) ** (1.0 / n) - 1.0)

    # CAGR (anualiza a média mensal geométrica)
    cagr = float((1.0 + geom_monthly) ** 12 - 1.0)

    # Média aritmética mensal
    arith_monthly = float(np.mean(r))

    # Volatilidade mensal (desvio-padrão amostral)
    vol_monthly = float(np.std(r, ddof=1)) if n > 1 else float("nan")

    return {
        "n_months": n,
        "total_return": total_return,
        "geom_monthly": geom_monthly,
        "cagr": cagr,
        "arith_monthly": arith_monthly,
        "vol_monthly": vol_monthly,
    }


def _empty_metrics() -> dict:
    return {
        "n_months": 0,
        "total_return": float("nan"),
        "geom_monthly": float("nan"),
        "cagr": float("nan"),
        "arith_monthly": float("nan"),
        "vol_monthly": float("nan"),
    }


def build_metrics_table(
    returns_df: pd.DataFrame,
    cfg: dict,
) -> dict[int, pd.DataFrame]:
    """
    Constrói tabela de métricas por janela.

    Returns: dict {years: DataFrame com colunas de métricas, linhas = ativos}
    """
    ref = reference_date(cfg)
    log.info("Data de referência: %s (mês fechado)", ref)

    windows = cfg["windows"]
    results: dict[int, pd.DataFrame] = {}

    for years in windows:
        rows = []
        cdi_geom = None  # será preenchido com CDI da mesma janela

        # Primeiro passo: calcula CDI para normalização ret/risco
        if "CDI" in returns_df.columns:
            cdi_slice = window_slice(returns_df["CDI"], ref, years)
            cdi_metrics = compute_metrics(cdi_slice)
            cdi_geom = cdi_metrics["geom_monthly"]

        for asset in returns_df.columns:
            sliced = window_slice(returns_df[asset], ref, years)
            m = compute_metrics(sliced)
            m["asset"] = asset

            # Retorno/risco vs CDI: (geom_monthly_ativo - geom_monthly_CDI) / vol_monthly_ativo
            if cdi_geom is not None and not np.isnan(m["vol_monthly"]) and m["vol_monthly"] > 0:
                m["ret_risk_vs_cdi"] = (m["geom_monthly"] - cdi_geom) / m["vol_monthly"]
            else:
                m["ret_risk_vs_cdi"] = float("nan")

            rows.append(m)

        df = pd.DataFrame(rows).set_index("asset")
        df = df.sort_values("geom_monthly", ascending=False)
        results[years] = df
        log.info("Janela %da: ref=%s, %d ativos calculados", years, ref, len(df))

    return results, ref


def top10_table(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """Formata tabela Top 10 para exibição."""
    df = metrics_df.head(10).copy().reset_index()  # reset para índice numérico
    df.insert(0, "Rank", range(1, len(df) + 1))

    display = pd.DataFrame({
        "Rank":                           df["Rank"],
        "Investimento":                   df["asset"],
        "Retorno Acum. (%)":              (df["total_return"] * 100).round(2),
        "Rend. Médio Mensal (%) geom.":   (df["geom_monthly"] * 100).round(3),
        "CAGR (%)":                       (df["cagr"] * 100).round(2),
        "Vol. Mensal (%)":                (df["vol_monthly"] * 100).round(3),
        "Ret/Risco vs CDI":               df["ret_risk_vs_cdi"].round(3),
        "N meses":                        df["n_months"].astype(int),
    }).set_index("Rank")
    return display


def cross_horizon_table(metrics_by_window: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """
    Tabela resumo cross-horizonte.
    Linhas = ativos; colunas = rend. médio mensal geom. por janela (%).
    """
    windows = sorted(metrics_by_window.keys())
    all_assets = set()
    for df in metrics_by_window.values():
        all_assets.update(df.index.tolist())

    rows = {}
    for asset in sorted(all_assets):
        row = {}
        for w in windows:
            df = metrics_by_window[w]
            if asset in df.index:
                row[f"{w}a (%)"] = round(df.loc[asset, "geom_monthly"] * 100, 3)
            else:
                row[f"{w}a (%)"] = float("nan")
        rows[asset] = row

    cross = pd.DataFrame(rows).T
    # Ordena pela janela de 2 anos (ou a menor disponível)
    sort_col = f"{min(windows)}a (%)"
    cross = cross.sort_values(sort_col, ascending=False)
    return cross

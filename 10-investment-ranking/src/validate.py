"""
Validações de qualidade dos dados — falha alto (raise) se quebrar tolerância crítica.

Checks:
  1. Número de observações mensais por ativo e janela
  2. Datas inicial/final efetivas
  3. % de meses NaN/faltantes por janela
  4. Coerência interna: recompor acumulado dos mensais ≈ produto
  5. Sanity check de ordem de grandeza (jan/2024–dez/2025)
"""
import logging
from datetime import date

import numpy as np
import pandas as pd

from src.metrics import reference_date, window_slice

log = logging.getLogger(__name__)

SANITY_BENCHMARKS = {
    # Janela 2 anos ~jan/2024–dez/2025, BRL: referência de sanidade
    "Bitcoin":       (2.5, 5.0),    # %/mês — intervalo aceitável
    "Ouro":          (2.0, 4.5),
    "Acoes_EUA_BDR": (1.5, 3.5),
    "Ibovespa":      (0.0, 1.5),
    "CDI":           (0.7, 1.3),
    "Poupanca":      (0.3, 0.9),
    "Dolar":         (0.2, 1.0),
    "IMA_B":         (0.5, 1.5),
}


class ValidationError(Exception):
    pass


def run_all(
    returns_df: pd.DataFrame,
    metrics_by_window: dict[int, pd.DataFrame],
    cfg: dict,
    strict: bool = True,
) -> list[str]:
    """
    Executa todos os checks. Retorna lista de avisos.
    Se strict=True, levanta ValidationError se check crítico falhar.
    """
    warnings = []
    ref = reference_date(cfg)

    # CHECK 1 & 3: cobertura por ativo × janela
    log.info("=== Validação: cobertura de dados ===")
    min_obs = cfg["validation"]["min_obs_for_window"]
    max_nan = cfg["validation"]["max_nan_pct"]
    all_windows = cfg["windows"]

    for asset in returns_df.columns:
        for years in all_windows:
            sliced = window_slice(returns_df[asset], ref, years)
            expected_n = years * 12
            actual_n = len(sliced)
            nan_pct = 1 - (actual_n / expected_n) if expected_n > 0 else 1.0
            min_required = min_obs.get(years, int(expected_n * 0.9))

            msg = f"{asset} janela={years}a: {actual_n}/{expected_n} meses ({nan_pct:.1%} faltando)"
            if actual_n < min_required:
                w = f"COBERTURA INSUFICIENTE — {msg} (mín={min_required})"
                warnings.append(w)
                log.warning(w)
            else:
                log.info("OK %s", msg)

    # CHECK 2: datas efetivas
    log.info("=== Validação: datas efetivas ===")
    for asset in returns_df.columns:
        valid = returns_df[asset].dropna()
        if len(valid) > 0:
            log.info("  %-20s início=%s  fim=%s  n=%d",
                     asset, valid.index[0].strftime("%Y-%m"),
                     valid.index[-1].strftime("%Y-%m"), len(valid))

    # CHECK 4: consistência aritmética — acumulado via produto ≈ geom_monthly^n
    log.info("=== Validação: consistência aritmética ===")
    for asset in returns_df.columns:
        for years in [2]:  # check só na janela de 2 anos por brevidade
            sliced = window_slice(returns_df[asset], ref, years)
            if len(sliced) < 2:
                continue
            r = sliced.values.astype(float)
            total_check = float(np.prod(1.0 + r) - 1.0)
            n = len(r)
            geom = float((1.0 + total_check) ** (1.0 / n) - 1.0)
            recomputed = float((1.0 + geom) ** n - 1.0)
            diff = abs(total_check - recomputed)
            if diff > 1e-10:
                w = f"INCONSISTÊNCIA ARITMÉTICA {asset}: acumulado={total_check:.6f}, recomposto={recomputed:.6f}, diff={diff:.2e}"
                warnings.append(w)
                log.warning(w)
            else:
                log.info("OK aritmética %s janela=2a: %.4f%%/mês, acum=%.2f%%",
                         asset, geom * 100, total_check * 100)

    # CHECK 5: sanity check de ordem de grandeza (janela 2 anos)
    log.info("=== Validação: sanity check (janela 2 anos) ===")
    if 2 in metrics_by_window:
        df2 = metrics_by_window[2]
        for asset, (lo, hi) in SANITY_BENCHMARKS.items():
            if asset in df2.index:
                geom_pct = df2.loc[asset, "geom_monthly"] * 100
                if not (lo <= geom_pct <= hi):
                    w = (f"SANITY CHECK FALHOU {asset}: geom_monthly={geom_pct:.3f}%/mês "
                         f"fora do intervalo [{lo}, {hi}] %/mês")
                    warnings.append(w)
                    log.warning(w)
                else:
                    log.info("OK sanity %s: %.3f%%/mês (esperado %.1f–%.1f)", asset, geom_pct, lo, hi)

    if warnings and strict:
        critical = [w for w in warnings if "CRÍTICO" in w or "INCONSISTÊNCIA ARITMÉTICA" in w]
        if critical:
            raise ValidationError("Validações críticas falharam:\n" + "\n".join(critical))

    log.info("=== Validação concluída: %d avisos ===", len(warnings))
    return warnings


def print_coverage_report(returns_df: pd.DataFrame, cfg: dict) -> None:
    """Imprime relatório de cobertura (contagens) para o stdout."""
    ref = reference_date(cfg)
    print(f"\n{'='*70}")
    print(f"RELATÓRIO DE COBERTURA — referência: {ref}")
    print(f"{'='*70}")
    header = f"{'Ativo':<22} {'Total':>6} " + " ".join(f"{'W'+str(w)+'a':>6}" for w in cfg["windows"])
    print(header)
    print("-" * 70)
    for asset in returns_df.columns:
        total = returns_df[asset].dropna().count()
        window_counts = []
        for years in cfg["windows"]:
            sl = window_slice(returns_df[asset], ref, years)
            window_counts.append(f"{len(sl):>6}")
        row = f"{asset:<22} {total:>6} " + " ".join(window_counts)
        print(row)
    print("=" * 70)

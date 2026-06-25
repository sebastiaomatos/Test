"""
Testes unitários para src/metrics.py.
Executa: python -m pytest tests/ -v
"""
import numpy as np
import pandas as pd
import pytest
from datetime import date

from src.metrics import compute_metrics, window_slice, cross_horizon_table


class TestComputeMetrics:
    def test_known_total_return(self):
        # 21% total em 24 meses → ~0.792%/mês geom.
        # (1.21)^(1/24) - 1 = 0.007924...
        total_target = 0.21
        n = 24
        monthly = (1 + total_target) ** (1 / n) - 1  # ≈ 0.007924
        returns = pd.Series([monthly] * n)
        m = compute_metrics(returns)
        assert abs(m["total_return"] - total_target) < 1e-10, \
            f"total_return={m['total_return']:.6f} ≠ {total_target}"
        assert abs(m["geom_monthly"] - monthly) < 1e-10, \
            f"geom_monthly={m['geom_monthly']:.6f} ≠ {monthly:.6f}"
        assert abs(m["n_months"] - n) < 1

    def test_recompose_accumulation(self):
        # Os mensais devem recompor o acumulado: (1+geom)^n - 1 ≈ total
        returns = pd.Series([0.01, -0.005, 0.02, 0.008, -0.003, 0.015] * 4)
        m = compute_metrics(returns)
        recomputed = (1 + m["geom_monthly"]) ** m["n_months"] - 1
        assert abs(recomputed - m["total_return"]) < 1e-10, \
            f"Recomposto {recomputed:.8f} ≠ total {m['total_return']:.8f}"

    def test_cagr_from_monthly(self):
        # CAGR = (1+geom_monthly)^12 - 1
        returns = pd.Series([0.01] * 24)
        m = compute_metrics(returns)
        expected_cagr = (1 + m["geom_monthly"]) ** 12 - 1
        assert abs(m["cagr"] - expected_cagr) < 1e-10

    def test_zero_returns(self):
        returns = pd.Series([0.0] * 12)
        m = compute_metrics(returns)
        assert m["total_return"] == pytest.approx(0.0)
        assert m["geom_monthly"] == pytest.approx(0.0)
        assert m["cagr"] == pytest.approx(0.0)
        assert m["vol_monthly"] == pytest.approx(0.0, abs=1e-10)

    def test_empty_series(self):
        m = compute_metrics(pd.Series(dtype=float))
        assert m["n_months"] == 0
        assert np.isnan(m["total_return"])

    def test_high_volatility_asset(self):
        # Bitcoin-like: +50% seguido de -30% × 12 → total negativo
        returns = pd.Series(([0.50, -0.30] * 12))
        m = compute_metrics(returns)
        # (1.5 * 0.7)^12 - 1 = 1.05^12 - 1 ≈ 79.6% no total
        expected_total = (1.5 * 0.7) ** 12 - 1
        assert abs(m["total_return"] - expected_total) < 1e-8

    def test_arithmetic_vs_geometric(self):
        # Média aritmética sempre ≥ média geométrica para séries com variância > 0
        returns = pd.Series([0.05, -0.02, 0.03, 0.08, -0.01, 0.04])
        m = compute_metrics(returns)
        assert m["arith_monthly"] >= m["geom_monthly"] - 1e-12

    def test_vol_computation(self):
        returns = pd.Series([0.01, 0.02, 0.03, 0.01, 0.02])
        m = compute_metrics(returns)
        expected_vol = float(np.std([0.01, 0.02, 0.03, 0.01, 0.02], ddof=1))
        assert abs(m["vol_monthly"] - expected_vol) < 1e-10

    def test_single_month(self):
        returns = pd.Series([0.05])
        m = compute_metrics(returns)
        assert m["total_return"] == pytest.approx(0.05)
        assert m["geom_monthly"] == pytest.approx(0.05)
        assert np.isnan(m["vol_monthly"])  # ddof=1, n=1


class TestWindowSlice:
    def _make_monthly_series(self):
        idx = pd.date_range("2015-01-01", periods=120, freq="MS")
        return pd.Series(np.random.randn(120) * 0.02, index=idx)

    def test_slice_length_2y(self):
        s = self._make_monthly_series()
        ref = date(2024, 12, 31)
        sliced = window_slice(s, ref, 2)
        assert len(sliced) == 24, f"Esperado 24 meses, obtido {len(sliced)}"

    def test_slice_length_5y(self):
        s = self._make_monthly_series()
        ref = date(2024, 12, 31)
        sliced = window_slice(s, ref, 5)
        assert len(sliced) == 60, f"Esperado 60 meses, obtido {len(sliced)}"

    def test_slice_ends_at_ref(self):
        s = self._make_monthly_series()
        ref = date(2024, 6, 30)
        sliced = window_slice(s, ref, 2)
        # Último mês deve ser junho/2024
        last_period = sliced.index[-1].to_period("M")
        assert last_period == pd.Period("2024-06", "M"), \
            f"Último mês: {last_period}"


class TestCrossHorizonTable:
    def test_shape(self):
        # Simula métricas de 3 ativos em 2 janelas
        def make_df(assets, geom_vals):
            rows = {a: {"geom_monthly": g, "total_return": 0, "cagr": 0,
                        "arith_monthly": 0, "vol_monthly": 0, "ret_risk_vs_cdi": 0,
                        "n_months": 24}
                    for a, g in zip(assets, geom_vals)}
            return pd.DataFrame(rows).T

        assets = ["A", "B", "C"]
        m2 = make_df(assets, [0.02, 0.01, 0.005])
        m5 = make_df(assets, [0.015, 0.012, 0.008])
        cross = cross_horizon_table({2: m2, 5: m5})
        assert cross.shape == (3, 2)
        assert "2a (%)" in cross.columns
        assert "5a (%)" in cross.columns

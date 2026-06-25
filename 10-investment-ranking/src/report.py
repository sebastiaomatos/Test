"""
Geração de relatórios: tabelas no console, xlsx e gráfico de barras.
"""
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # sem display
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

from src.metrics import top10_table, cross_horizon_table

log = logging.getLogger(__name__)

ASSET_LABELS = {
    "Bitcoin":        "Bitcoin",
    "Ouro":           "Ouro",
    "Acoes_EUA_BDR":  "Ações EUA (IVVB11)",
    "Ibovespa":       "Ibovespa",
    "Dividendos_IDIV": "Dividendos (DIVO11)",
    "FIIs_IFIX":      "FIIs (HGLG11*)",
    "CDI":            "CDI",
    "IMA_B":          "IMA-B (IPCA+)",
    "Poupanca":       "Poupança",
    "Dolar":          "Dólar",
    "SmallCaps":      "Small Caps",
}

DISCLAIMER = (
    "⚠ Não é recomendação de investimento. Rentabilidade passada não garante retorno futuro.\n"
    "  Análise retrospectiva; sensível à janela temporal. BRL vs USD pode alterar o ranking.\n"
    "  Bitcoin/Ouro: volatilidade muito superior — ver coluna Ret/Risco vs CDI.\n"
    "  (*) FIIs_IFIX proxy: HGLG11 individual ≠ IFIX. BDRs: IVVB11 (preço, sem dividendos reinvestidos)."
)


def print_top10(metrics_by_window: dict, warnings: list[str]) -> None:
    """Imprime tabelas Top 10 no console."""
    for years, df in sorted(metrics_by_window.items()):
        print(f"\n{'='*80}")
        print(f"TOP 10 — Janela {years} anos")
        print("="*80)
        top = top10_table(df)
        # Renomeia ativos para labels amigáveis
        top["Investimento"] = top["Investimento"].map(lambda x: ASSET_LABELS.get(x, x))
        print(top.to_string())

    print(f"\n{'='*80}")
    print("TABELA CROSS-HORIZONTE — Rendimento Médio Mensal (% geom.)")
    print("="*80)
    cross = cross_horizon_table(metrics_by_window)
    cross.index = [ASSET_LABELS.get(x, x) for x in cross.index]
    print(cross.to_string())

    if warnings:
        print(f"\n{'='*80}")
        print(f"AVISOS ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")

    print(f"\n{'-'*80}")
    print(DISCLAIMER)
    print("-"*80)


def save_xlsx(
    returns_df: pd.DataFrame,
    metrics_by_window: dict,
    ref_date,
    output_dir: Path,
    filename: str = "rentabilidade.xlsx",
) -> Path:
    """Salva xlsx com uma aba por janela + aba de séries brutas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        # Aba séries brutas
        raw = (returns_df * 100).round(4)
        raw.index = raw.index.strftime("%Y-%m")
        raw.columns = [ASSET_LABELS.get(c, c) for c in raw.columns]
        raw.to_excel(writer, sheet_name="Series Brutas pct-mes")

        # Abas por janela
        for years, df in sorted(metrics_by_window.items()):
            top = top10_table(df)
            top["Investimento"] = top["Investimento"].map(lambda x: ASSET_LABELS.get(x, x))
            top.to_excel(writer, sheet_name=f"Ranking {years}a")

            # Tabela completa nessa janela
            full = df.copy()
            full.index = [ASSET_LABELS.get(x, x) for x in full.index]
            pct_cols = ["total_return", "geom_monthly", "cagr", "arith_monthly", "vol_monthly"]
            for c in pct_cols:
                if c in full.columns:
                    full[c] = (full[c] * 100).round(4)
            full.to_excel(writer, sheet_name=f"Completo {years}a", startrow=2)

        # Cross-horizonte
        cross = cross_horizon_table(metrics_by_window)
        cross.index = [ASSET_LABELS.get(x, x) for x in cross.index]
        cross.to_excel(writer, sheet_name="Cross-Horizonte")

        # Aba de metadados
        meta_df = pd.DataFrame({
            "Parâmetro": ["Data de referência", "Janelas (anos)", "Disclaimer"],
            "Valor": [str(ref_date), str(sorted(metrics_by_window.keys())), DISCLAIMER],
        })
        meta_df.to_excel(writer, sheet_name="Metadados", index=False)

    log.info("Xlsx salvo: %s", path)
    return path


def save_chart(
    metrics_by_window: dict,
    ref_date,
    output_dir: Path,
    filename: str = "ranking_barras.png",
) -> Path:
    """
    Gráfico de barras agrupadas: rendimento médio mensal (%) × horizonte temporal.
    Verifica visualmente eixos, escala, rótulos.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    windows = sorted(metrics_by_window.keys())

    # Coleta dados: todos os ativos que aparecem em pelo menos uma janela
    all_assets = []
    seen = set()
    for w in windows:
        for a in metrics_by_window[w].index:
            if a not in seen:
                all_assets.append(a)
                seen.add(a)

    # Matriz: assets × windows
    data = np.full((len(all_assets), len(windows)), np.nan)
    for j, w in enumerate(windows):
        df = metrics_by_window[w]
        for i, a in enumerate(all_assets):
            if a in df.index:
                data[i, j] = df.loc[a, "geom_monthly"] * 100

    labels = [ASSET_LABELS.get(a, a) for a in all_assets]

    # Ordena por janela de 2 anos (ou menor disponível)
    sort_col = 0
    order = np.argsort(-np.nan_to_num(data[:, sort_col], nan=-999))
    data = data[order]
    labels = [labels[i] for i in order]

    n_assets = len(labels)
    n_windows = len(windows)

    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(n_assets)
    width = 0.18
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    offsets = np.linspace(-(n_windows - 1) / 2 * width, (n_windows - 1) / 2 * width, n_windows)

    for j, (w, offset) in enumerate(zip(windows, offsets)):
        vals = data[:, j]
        bars = ax.bar(x + offset, vals, width, label=f"{w} anos",
                      color=colors[j % len(colors)], alpha=0.85, edgecolor="white", linewidth=0.5)
        # Rótulos sobre as barras (apenas se valor não é nan)
        for bar, v in zip(bars, vals):
            if not np.isnan(v):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                        f"{v:.2f}%", ha="center", va="bottom", fontsize=6.5, rotation=90)

    ax.set_xlabel("Ativo", fontsize=11)
    ax.set_ylabel("Rendimento Médio Mensal (% geom.)", fontsize=11)
    ax.set_title(
        f"Ranking de Investimentos — Rendimento Médio Mensal\n"
        f"Referência: {ref_date.strftime('%b/%Y')} | Janelas: {', '.join(str(w)+'a' for w in windows)}",
        fontsize=12, fontweight="bold"
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f%%"))
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.legend(title="Janela", fontsize=9, title_fontsize=9)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    # Anotação de disclaimer
    fig.text(0.5, 0.01,
             "Não é recomendação de investimento. (*) FIIs_IFIX proxy: HGLG11. BDRs: IVVB11 (preço).",
             ha="center", fontsize=7, color="gray", style="italic")

    plt.tight_layout(rect=[0, 0.03, 1, 1])

    path = output_dir / filename
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Gráfico salvo: %s", path)
    return path

#!/usr/bin/env python3
"""
Pipeline principal: fetch → load → validate → report.

Uso:
  python run.py                 # execução normal (usa cache)
  python run.py --refresh       # força re-download de todas as fontes
  python run.py --no-strict     # validações não bloqueiam em aviso
  python run.py --skip-chart    # pula geração de gráfico
"""
import argparse
import logging
import os
import sys
from pathlib import Path

# Configura CA bundle ANTES de qualquer import de rede
os.environ.setdefault("CURL_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")

# Adiciona diretório raiz ao path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import yaml
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("run")


def load_config(path: Path = ROOT / "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Pipeline de ranking de investimentos")
    parser.add_argument("--refresh", action="store_true", help="Força re-download")
    parser.add_argument("--no-strict", action="store_true", help="Não bloqueia em aviso de validação")
    parser.add_argument("--skip-chart", action="store_true", help="Não gera gráfico")
    args = parser.parse_args()

    cfg = load_config()
    cache_dir = ROOT / cfg["cache"]["raw_dir"]
    output_dir = ROOT / cfg["output"]["dir"]

    log.info("════════════════════════════════════════════")
    log.info("  RANKING DE INVESTIMENTOS BRASILEIROS")
    log.info("════════════════════════════════════════════")

    # ── STEP 1: Fetch & Load ─────────────────────────────────────────────
    from src.loader import build_returns_dataframe
    log.info("[1/4] Carregando e unificando dados...")
    returns_df = build_returns_dataframe(cfg, cache_dir=cache_dir, refresh=args.refresh)

    # ── STEP 2: Métricas ─────────────────────────────────────────────────
    from src.metrics import build_metrics_table, reference_date
    log.info("[2/4] Calculando métricas por janela...")
    metrics_by_window, ref_date = build_metrics_table(returns_df, cfg)
    log.info("Data de referência: %s", ref_date)

    # ── STEP 3: Validação ────────────────────────────────────────────────
    from src.validate import run_all, print_coverage_report
    log.info("[3/4] Validando dados...")
    print_coverage_report(returns_df, cfg)
    strict = not args.no_strict
    warnings = run_all(returns_df, metrics_by_window, cfg, strict=strict)

    # ── STEP 4: Relatório ─────────────────────────────────────────────────
    from src.report import print_top10, save_xlsx, save_chart
    log.info("[4/4] Gerando relatório...")
    print_top10(metrics_by_window, warnings)

    xlsx_path = save_xlsx(returns_df, metrics_by_window, ref_date, output_dir,
                           filename=cfg["output"]["xlsx_file"])
    log.info("Xlsx: %s", xlsx_path)

    if not args.skip_chart:
        chart_path = save_chart(metrics_by_window, ref_date, output_dir,
                                 filename=cfg["output"]["chart_file"])
        log.info("Gráfico: %s", chart_path)

    log.info("════════════════════════════════════════════")
    log.info("  PIPELINE CONCLUÍDO")
    log.info("  Referência: %s | Janelas: %s anos", ref_date, cfg["windows"])
    log.info("  Saídas em: %s/", output_dir)
    log.info("════════════════════════════════════════════")


if __name__ == "__main__":
    main()

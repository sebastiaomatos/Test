# CLAUDE.md — Investment Ranking Pipeline

## Visão Geral

Pipeline de ranqueamento de investimentos brasileiros por retorno mensal geométrico médio,
em janelas rolantes de 2, 3, 5 e 10 anos, encerrando no último mês civil fechado.

---

## Mapa de Ativos e Fontes

| Ativo             | Ticker / Série    | Fonte      | Moeda | Observações                                |
|-------------------|-------------------|------------|-------|--------------------------------------------|
| Bitcoin           | BTC-USD           | Yahoo      | USD   | Convertido para BRL via PTAX               |
| Ouro              | GC=F              | Yahoo      | USD   | Convertido para BRL via PTAX               |
| Ações EUA (BDR)   | IVVB11.SA         | Yahoo      | BRL   | Disponível desde 2015; extensão com ^GSPC  |
| Ibovespa          | ^BVSP             | Yahoo      | BRL   | Índice, não ETF                            |
| Dividendos (IDIV) | DIVO11.SA         | Yahoo      | BRL   | ETF do índice IDIV                         |
| FIIs (IFIX)       | HGLG11.SA         | Yahoo      | BRL   | Proxy para IFIX — substituir se necessário |
| SmallCaps         | SMAL11.SA         | Yahoo      | BRL   | ETF SMAL11                                 |
| CDI               | BCB série 4391    | BCB SGS    | BRL   | % ao mês → decimal (/100)                 |
| Poupança          | BCB série 196     | BCB SGS    | BRL   | % ao mês → decimal (/100)                 |
| IMA-B             | BCB série 12466   | BCB SGS    | BRL   | Descontinuada em mai/2023; extensão abaixo |
| IMA-B (ext)       | IMAB11.SA         | Yahoo      | BRL   | Preços estagnados (79.50) Apr/22–Dez/25    |
| Dólar             | BRL=X             | Yahoo      | BRL   | Cotação USD/BRL — retorno = variação camb. |
| Câmbio (FX)       | BRL=X             | Yahoo      | —     | Usado internamente para converter USD→BRL  |
| S&P 500 (ext)     | ^GSPC             | Yahoo      | USD   | Hidden; extensão histórica para IVVB11     |

---

## Convenções de Dados

- **Index**: DatetimeIndex com **primeiro dia do mês** (período de competência).
- **Retornos**: decimal mensal (`0.01 = +1%`). Nunca percentual nos cálculos intermediários.
- **Moeda**: tudo em BRL. USD convertido via `BRL=X` (PTAX intraday, fim-de-mês).
- **Preços → retornos**: `pct_change().dropna()`.
- **Yahoo Finance**: sempre buscar intervalo `1d` e resamplar `resample("ME").last()` — intervalo `1mo` tem gaps para ETFs da B3.
- **BCB SGS**: endpoint `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{id}/dados`, datas em `dd/mm/yyyy`, valores com vírgula decimal.
- **BCB últimos**: endpoint `…/ultimos/{n}?formato=json` (count no **path**, não como query param).

---

## Lacunas de Dados Conhecidas

### IMA-B (Jun/2023 – Jan/2026)
- BCB série 12466 foi descontinuada em **22/mai/2023**.
- IMAB11.SA (ETF) tem **preço congelado em 79.50** de Abr/2022 a Dez/2025 no yfinance — dados estragados, descartados.
- IMAB11 válido a partir de **Fev/2026** (5 meses adicionais).
- **Gap de 31 meses** (Jun/2023–Jan/2026) sem dados confiáveis. Janelas 2a e 3a ficam com cobertura insuficiente — esperado, não é bug.
- Para cobrir o gap: considerar ANBIMA API direto (série IMA-B do portal dados.anbima.com.br).

---

## Estrutura do Projeto

```
10-investment-ranking/
├── config.yaml          # Tickers, séries, janelas, tolerâncias — tudo parametrizado
├── requirements.txt     # Dependências Python
├── run.py               # Entrypoint: fetch → load → validate → report
├── Makefile             # make run / make test / make refresh / make clean
├── CLAUDE.md            # Este arquivo
├── data/
│   └── raw/             # Cache parquet (max_age_days=1 por padrão)
├── outputs/             # Resultados: xlsx, png, csv
├── src/
│   ├── sources/
│   │   ├── yahoo.py     # fetch_monthly(ticker, ...) — diário→mensal, curl_cffi
│   │   └── bcb.py       # fetch_monthly_series(), fetch_imab_daily_to_monthly()
│   ├── fx.py            # get_usd_brl_monthly(), convert_usd_to_brl()
│   ├── loader.py        # build_returns_dataframe() — une todas as fontes
│   ├── metrics.py       # compute_metrics(), build_metrics_table(), top10_table()
│   ├── validate.py      # run_all() — checks de cobertura, sanidade, consistência
│   └── report.py        # Gera xlsx, png, csv em outputs/
└── tests/
    └── test_metrics.py  # 13 testes unitários (pytest)
```

---

## Infraestrutura / Proxy

- Todo HTTPS passa pelo proxy em `http://127.0.0.1:40089` com CA bundle em `/root/.ccr/ca-bundle.crt`.
- Variáveis já configuradas no ambiente: `CURL_CA_BUNDLE`, `REQUESTS_CA_BUNDLE`, `SSL_CERT_FILE`.
- **curl_cffi**: yfinance 1.4+ usa internamente; configurar `cf.Session(impersonate="chrome110", verify=CA_BUNDLE)` e passar ao `yf.Ticker(ticker, session=session)`.
- Se `CURL_CA_BUNDLE` não estiver set, `run.py` aplica o default via `os.environ.setdefault`.

---

## Métricas Calculadas

| Métrica              | Fórmula                                              |
|----------------------|------------------------------------------------------|
| `geom_monthly`       | `(1+R_total)^(1/n) − 1`                              |
| `total_return`       | `∏(1+rᵢ) − 1`                                       |
| `cagr`               | `(1+geom_monthly)^12 − 1`                            |
| `arith_monthly`      | `mean(rᵢ)`                                           |
| `vol_monthly`        | `std(rᵢ, ddof=1)`                                    |
| `ret_risk_vs_cdi`    | `(geom_monthly_ativo − geom_monthly_CDI) / vol`      |

---

## Tolerâncias de Validação (config.yaml)

- `max_nan_pct`: 10% de meses faltando por janela (exceção documentada: IMA-B)
- `min_obs_for_window`: 2a→22, 3a→32, 5a→54, 10a→108
- `reconcile_tolerance_pp`: 2.0 pp — consistência aritmética interna

---

## Faixas de Sanidade (janela 2 anos, %/mês)

Baseadas no período Jun/2024–Mai/2026 (BRL apreciou vs USD neste período).

| Ativo          | Mín  | Máx  |
|----------------|------|------|
| Bitcoin        | -2.0 | 5.0  |
| Ouro           | 1.5  | 5.0  |
| Ações EUA BDR  | 0.8  | 3.5  |
| Ibovespa       | 0.0  | 2.5  |
| CDI            | 0.7  | 1.3  |
| Poupança       | 0.3  | 0.9  |
| Dólar          | -1.0 | 1.5  |
| IMA-B          | 0.5  | 2.0  |

---

## Ressalvas Obrigatórias

> **Este relatório não constitui recomendação de investimento.**
> Rentabilidade passada não garante rentabilidade futura.
> Análise retrospectiva e sensível à janela temporal escolhida.
> Retornos em BRL: variação cambial BRL/USD altera significativamente o ranking.
> Ativos do topo (cripto, ouro) têm volatilidade muito superior — ver coluna Ret/Risco vs CDI.

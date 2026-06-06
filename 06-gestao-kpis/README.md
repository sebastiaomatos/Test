# 06 · Planilha de gestão de tráfego e funil

`Planilha-Gestao-Trafego-e-Funil.xlsx` — abra no Excel ou importe no Google Sheets
(as fórmulas e a formatação condicional são recalculadas ao abrir).

## Abas
| Aba | Para que serve |
|---|---|
| **Painel** | Dashboard automático: investimento, leads, CPL, custo por conversa/visita/venda (CAC), taxas do funil, receita e ROAS — com **semáforo** (✅/⚠️/🔴) comparando às metas. |
| **Metas** | Defina aqui os alvos de CPL, custo por conversa, taxas e comissão média. O Painel usa estes valores. |
| **Lançamentos** | Registre **dia a dia** cada campanha (investido, impressões, cliques, leads, conversas, visitas, propostas, vendas). CTR, CPL e custo/conversa são calculados sozinhos, com semáforo de CPL. |
| **Funil de Vendas** | Pipeline dos atendimentos atuais por estágio. Calcula comissão potencial, **dias parado** (fica vermelho > 3 dias) e traz um resumo por estágio. |

## Como usar
1. Ajuste as **Metas** para a sua praça/ticket.
2. Todo dia, lance uma linha por campanha em **Lançamentos** (use os menus suspensos de Plataforma/Etapa).
3. Acompanhe o **Painel**: o que estiver 🔴 é onde cortar verba; o que estiver ✅ é onde escalar (+20% a cada 3 dias).
4. Gerencie os atendimentos no **Funil**: priorize quem está "parado" há mais dias e quem está em Proposta.

> Os dados preenchidos são **exemplos** — substitua pelos números reais. Regenerar: `python3 src/make_planilha.py`.

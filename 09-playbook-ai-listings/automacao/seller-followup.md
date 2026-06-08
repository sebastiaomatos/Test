# Automação — follow-up do lead de avaliação (vendedor)

> Dispare via CRM + SMS/WhatsApp + e-mail. Objetivo: do laudo → reunião de captação.
> Pare a régua quando o lead responder/agendar; classifique HOT/WARM/COLD.

| Toque | Quando | Canal | Mensagem (modelo) |
|---|---|---|---|
| T0 | 0 min | E-mail/WhatsApp | "Olá {{nome}}! Aqui está a avaliação do seu imóvel em {{endereço}}: faixa estimada **{{R$ low–high}}**. Quer que eu te explique em 2 min como cheguei nesse número?" |
| T1 | 5 min | SMS/WhatsApp | "Recebeu a avaliação que te mandei? Qualquer dúvida sobre o valor, me chama por aqui 🙂" |
| T2 | Dia 1 | WhatsApp | "Curiosidade: ajudei a vender {{n}} imóveis aqui no {{bairro}} nos últimos meses. A demanda na sua região está {{alta/aquecida}} agora." |
| T3 | Dia 3 | E-mail | "3 ajustes simples que podem aumentar o valor de venda do seu imóvel — e o que está movendo o mercado em {{bairro}} este mês." |
| T4 | Dia 7 | WhatsApp | "Se fizer sentido, posso te mostrar um **plano de venda** em 15 min (sem compromisso). Prefere {{amanhã à tarde}} ou {{sábado de manhã}}?" |
| T5 | Dia 14 | WhatsApp | "Os valores se movem rápido. Quer que eu **atualize sua avaliação** com os dados mais recentes?" |

## Ramificações
- **Respondeu interesse / agendou** → para a régua + notifica corretor + estágio "Reunião agendada".
- **HOT** (vai vender em ≤3 meses) → atendimento humano imediato.
- **Sem resposta após T5** → estágio "Frio" + entra em retargeting (Meta) e newsletter mensal de mercado.

## Eventos para otimização
`lead_avaliacao` → conversão no Pixel/Google · `reuniao_agendada` e `captacao_assinada` → eventos de valor (base de Lookalike de quem vira captação).

## Stack sugerida
Meta Ads · Landing (form de endereço) · ChatGPT (laudo + textos) · CRM/automação (ex.: GoHighLevel, RD Station, Kommo) · Agendamento (Calendly).

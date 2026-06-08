# Biblioteca de Prompts ChatGPT — Funil AI Listings (captação)

> O motor do método. Cole no ChatGPT (GPT‑4o/o‑series) e troque os campos entre `{{ }}`.
> Os prompts estão em inglês (mercado‑alvo do produto é global/EUA); ao final, a nota de adaptação para PT‑BR.

---

## 1. Anúncios — ângulos, headlines e copy
```
You are a direct-response copywriter for real estate listing acquisition.
Audience: homeowners in {{city/neighborhood}} who MIGHT sell in the next 6–12 months.
Offer: a free, instant AI home valuation (no phone call).
Write 10 Facebook/Instagram ad variations. For each: a 1-line HOOK, 3-line primary text,
and a CTA. Use curiosity + low friction ("30 seconds", "no calls"). Avoid hype/banned claims.
Tone: helpful neighbor, not pushy. Output as a table: Angle | Hook | Primary text | CTA.
Angles to cover: curiosity ("what's it worth"), market timing, equity/"hidden money",
downsizing, relocation, "just curious", neighbor proof ("homes on your street").
```

## 2. Laudo de avaliação (CMA) — relatório que gera autoridade
```
Act as a local real estate market analyst. Create a clear, friendly home valuation report
for a homeowner. Inputs: address {{address}}, beds {{n}}, baths {{n}}, sqft {{area}},
condition {{condition}}, recent comps {{3-5 comparable sales: address, price, sqft, date}}.
Output sections:
1) Estimated value RANGE (low/likely/high) with a 2-line rationale.
2) "What's driving your value right now" (3 bullets, local market).
3) "3 things that could add R$/US$ X to your sale" (quick wins).
4) A soft CTA to book a 15-min strategy call.
Keep it under 400 words, confident but not salesy. No legal guarantees of price.
```

## 3. Sequência de follow‑up (SMS + e‑mail)
```
Write a 6-touch follow-up sequence for a seller lead who requested a free home valuation.
Channels: SMS (short) + email (longer). Timing: 0min, 5min, Day1, Day3, Day7, Day14.
Each touch: goal, channel, message. Progression: deliver value -> local social proof ->
market urgency -> offer the 15-min call -> reactivation. Personal, human, no spam vibe.
Include 1 PS with a soft objection-dissolver. Output as a table: Touch | Timing | Channel | Message.
```

## 4. Scripts de objeção (vendedor)
```
You are a top listing agent. For each common SELLER objection, write a short, empathetic
response (3-5 sentences) that reframes and moves toward booking a listing appointment.
Objections: "I'm just curious", "I'll think about it", "Your commission is too high",
"Another agent quoted me higher", "I'll talk to my spouse", "The market is bad right now",
"I want to try selling it myself (FSBO)". Output: Objection | Reframe | Exact reply.
```

## 5. Apresentação de captação (listing presentation)
```
Build a 7-slide listing presentation outline to win the listing at the appointment.
Seller context: {{home + motivation}}. Slides should cover: 1) their goal, 2) what's
happening in the local market, 3) my pricing strategy (range + why), 4) my marketing plan
(AI ads + online), 5) recent results/social proof, 6) the process & timeline, 7) clear next
step (sign today). For each slide: title + 2-3 talking points. Confident, data-led, concise.
```

## 6. Agente de mensagens — qualificação no chat
```
Act as an SMS qualification assistant for inbound seller leads. Ask, one at a time, in a
friendly tone: (a) timeframe to sell, (b) reason for moving, (c) property condition,
(d) best time for a 15-min call. After answers, classify the lead as HOT / WARM / COLD
with a 1-line reason, and propose the next action. Never sound like a bot; keep it human.
```

---

## Adaptação para PT‑BR
Troque os termos do mercado americano pelos equivalentes locais:
- *home valuation / what's my home worth* → **“avaliação gratuita do seu imóvel / quanto vale seu imóvel”**
- *CMA (comparative market analysis)* → **análise comparativa de mercado** (comparáveis = imóveis vendidos na região)
- *listing appointment* → **reunião de captação** · *commission* → **comissão** · *FSBO* → **“vender por conta própria”**
- Canais: priorize **WhatsApp** no lugar do SMS. Acrescente ao fim de cada prompt: *"Write in Brazilian Portuguese, WhatsApp-friendly, informal você."*

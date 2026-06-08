# Engenharia Reversa — VSL `luccasbraga.com/vsl-aqv01/`

> Análise técnica e estratégica completa da Video Sales Letter "Anúncio que Vende Imóvel" (Luccas Braga).
> Data da análise: 2026-06-06. Assets da página datados de 2026-06-02 (campanha recém-lançada).

---

## 1. Como o vídeo foi acessado (stack técnico)

A página é um *stub* HTML mínimo (2,8 KB). O vídeo **não** está no HTML — é injetado por JavaScript via player **VTurb / ConverteAI (smartplayer v4)**.

### Cadeia de descoberta
1. HTML bruto → tag `<vturb-smartplayer id="vid-69f3ea1bf646b7c8621d3f30">` + injeção do `player.js`.
2. `player.js` (ConverteAI) → referencia o manifesto HLS mestre.
3. Manifesto HLS → 3 qualidades adaptativas (404x720, 270x480, 202x360) — vídeo **vertical** (formato Reels/Stories).

| Item | Valor |
|---|---|
| Plataforma de vídeo | ConverteAI / VTurb SmartPlayer v4 |
| Account ID | `da7a2e9c-6603-42c8-9afe-e432d963fd2e` |
| Player ID | `69f3ea1bf646b7c8621d3f30` |
| Video ID | `69f3e86dc864fc4eeaccebe6` |
| Manifesto HLS | `cdn.converteai.net/.../69f3e86dc864fc4eeaccebe6/main.m3u8` |
| Duração | 27:34 min (~1.655 s, 414 segmentos TS) |

### Como o áudio foi obtido e transcrito
- Download dos 414 segmentos `.ts` (qualidade 360p, ~63 MB) em paralelo.
- `ffmpeg` (concat) → extração de áudio mono 16 kHz WAV.
- Transcrição com **faster-whisper** (modelo `small`, pt) → transcript com timestamps.

### Stack de rastreamento/marketing identificado na página
| Ferramenta | Função | ID |
|---|---|---|
| **UTMify** (`latest.js` + `pixel.js`) | Atribuição de UTMs e rastreio de conversão de afiliado/tráfego | pixelId `69f8ccf12965b0933030307e` |
| **Google Analytics 4** | Analytics | `G-WNVCNYZ165` |
| ConverteAI | Player + heatmap de retenção do vídeo | — |

> **Leitura estratégica do stack:** É um setup clássico de *tráfego pago direto → VSL*. UTMify indica que ele controla origem de tráfego/UTMs com precisão (provavelmente Meta Ads), e o SmartPlayer da ConverteAI dá métricas de retenção segundo-a-segundo para otimizar o roteiro — exatamente o que ele *ensina* no produto.

---

## 2. O produto / oferta

- **Nome:** "Anúncios que Vendem" (AQV — daí o slug `vsl-aqv01`).
- **Promessa central:** vender imóvel pelo Instagram/Meta Ads **sem virar blogueiro, sem seguidores, sem postar todo dia, sem aparecer**.
- **Formato:** programa de implementação, **7 módulos** (não "curso", posicionado como "implementação").
- **Público (ICP do próprio funil):** corretor que já tem CRECI (ou tirando), gastando dinheiro com leads ruins e querendo parar.

### Estrutura de preços (ancoragem em cascata)
| Âncora | Valor citado |
|---|---|
| Contratá-lo como gestor de tráfego | "impossível, não aceito mais cliente" |
| Consultoria individual | R$ 5.000 |
| "Poderia cobrar" | R$ 10.000 |
| Valor cheio declarado do curso | R$ 997 |
| Valor dos bônus isolados | "+ de R$ 2.000" |
| **Preço final (turma fundadora)** | **R$ 197 à vista** ou **12x R$ 20,25** |

### Bônus (empilhamento de valor)
1. Checklist de campanha pré-lançamento.
2. Lista de **30 ganchos** que filtram comprador / repelem curioso.
3. **3 templates** dos anúncios que mais vendem (formatos dos últimos 6 meses).
4. Comunidade no WhatsApp com corretores de vários estados.

### Bônus exclusivos "turma fundadora"
- Aulas ao vivo extras.
- **Acesso vitalício** (upgrade grátis) + atualizações para sempre.

### Garantias (dupla, reversão de risco)
- **7 dias incondicional** (declarada como obrigatória por lei — CDC).
- **30 dias condicional**: aplicou os 3 elementos, subiu campanhas, não gerou nenhum lead → reembolso 100%.

### Escassez/urgência
- **Próximos 15 minutos** → bônus extra: workshop ao vivo "empresarização do corretor" (convite VIP no WhatsApp). Passou os 15 min, ainda entra por R$ 197, mas perde o workshop.
- **Turma fundadora** com vagas/valor "especial" de lançamento.

---

## 3. A estratégia ENSINADA no vídeo (o conteúdo de verdade)

O núcleo intelectual da VSL é uma tese sobre algoritmo. Resumo destilado:

### Tese central: "Marketing de Atenção" vs. "Marketing de Intenção"

**O erro (Marketing de Atenção):**
- Gurus ensinam corretor a *entreter* — postar rotina, dancinha, café da manhã, hook que prende "todo mundo" nos 3 primeiros segundos, viralizar para ganhar seguidores.
- O algoritmo entrega para **quem pediu: gente buscando entretenimento** (no ônibus, antes de dormir) — não compradores.
- Prova social invertida: corretor que viraliza só é seguido por **outros corretores** → por isso acaba **vendendo curso pra corretor** em vez de imóvel. ("a prova de que viralizar não atrai comprador").

**A "bola de neve da otimização" (mecanismo de dor):**
- O algoritmo não sabe se o lead é bom — só registra reação (viu, mandou msg).
- Curioso manda mensagem → algoritmo lê como "sucesso" → busca mais curiosos → leads pioram progressivamente → 30 dias queimando orçamento com "quanto custa?" e gente que some.

**A solução (Marketing de Intenção) — 3 elementos:**
Se o algoritmo entrega para quem você *pede*, peça outra coisa. Hook que **exclui/repele** o curioso em vez de atrair todo mundo. A "bola de neve" passa a otimizar para leads bons.

1. **ICP real** — não é dado demográfico (idade/gênero). É a *motivação de compra* (dor, medo, desejo). Ex.: Minha Casa Minha Vida = sair do aluguel; imóvel de R$2M = upgrade de espaço. → **"trabalhe com a regra, não com a exceção"**.
2. **O imóvel como protagonista** — o astro do vídeo é o imóvel, não o corretor. Quem é fisgado pelo imóvel (não pela simpatia do corretor) vira lead muito mais qualificado.
3. **Elementos qualificativos** — explicitar preço, metragem, condições, localização. Isso *expulsa* quem não se enquadra → o algoritmo afasta perfis parecidos com o curioso e busca parecidos com o interessado real.

### O case (prova) repetido como moldura (bookend)
- **R$ 16** investidos → cliente que nunca o viu → visita no mesmo dia → financiamento aprovado em 5 dias → imóvel de ~R$ 400 mil → **comissão R$ 12 mil**.
- Matemática de escala "pessimista": R$ 30/dia (R$ 900/mês) → 1 venda → R$ 12 mil → reinveste → bola de neve positiva.

---

## 4. Arquitetura de persuasão do roteiro (timeline)

| Tempo | Bloco | Função persuasiva |
|---|---|---|
| 00:00–00:28 | **Hook/case** (R$16 → venda de R$400k) | Resultado extremo + curiosidade; "não é dancinha/viral/seguidores" |
| 00:29–01:31 | **Promessa + tom honesto** | "vou te vender algo no final, sem segredo" → constrói confiança |
| 01:31–03:40 | **História de origem** | Marketing→corretor, "fiz o caminho inverso", venda = 2 anos de salário |
| 03:40–04:02 | **Autoridade / "skin in the game"** | "se eu ensinar errado, EU perco dinheiro antes de você" |
| 04:02–09:05 | **Inimigo comum + mecanismo da dor** | Algoritmo, marketing de atenção, bola de neve ruim |
| 09:05–11:14 | **Virada / esperança** | Marketing de intenção, "treinar o algoritmo" |
| 11:14–11:33 | **Meta-prova** | "o anúncio que te trouxe aqui usou isso — VOCÊ é o lead qualificado" |
| 11:33–15:46 | **Conteúdo de valor (3 elementos)** | Entrega real → reciprocidade |
| 15:46–17:10 | **Prova / case detalhado** | Reforço do case com números (comissão R$12k) |
| 17:10–18:18 | **Escala / projeção** | Matemática de reinvestimento (bola de neve) |
| 18:18–21:00 | **Transição para oferta + bônus** | Empacotamento, 7 módulos, 4 bônus |
| 21:00–23:35 | **Ancoragem de preço + turma fundadora** | R$5k→R$10k→R$997→**R$197** + vitalício |
| 23:35–24:27 | **Urgência (15 min)** | Workshop bônus por tempo limitado |
| 24:27–25:24 | **Reversão de risco (2 garantias)** | "o risco é meu, não seu" |
| 25:24–27:34 | **Visualização futura + recap + escolha binária + CTA** | "dois caminhos": voltar a postar e torcer, ou clicar e ter campanha em 48h |

---

## 5. Gatilhos / frameworks de copy usados

- **Bookend (moldura):** abre e fecha com o mesmo case dos R$16 → R$12k.
- **Inimigo comum:** "gurus que ensinam teoria e não vendem imóvel".
- **Skin in the game / autoridade vivida:** "testo em mim antes de ensinar".
- **Mecanismo único nomeado:** "Marketing de Intenção", "bola de neve da otimização", "elementos qualificativos" — jargão proprietário aumenta percepção de método exclusivo.
- **Meta-prova (loop):** usa a própria VSL como demonstração ("você é a prova viva").
- **Reciprocidade:** entrega os 3 elementos de graça antes de pedir a venda.
- **Ancoragem em cascata** + **empilhamento de valor** (stacking de bônus).
- **Escassez dupla:** turma fundadora (vagas) + 15 min (bônus workshop).
- **Reversão de risco dupla** (7 + 30 dias).
- **Future pacing:** "imagina uma terça-feira... 7 visitas, 3 propostas, 2 vendas".
- **Escolha binária / dilema do CTA:** dois caminhos, um claramente ruim.
- **Negação de objeções:** "sem ser expert em tecnologia, sem equipe, sem experiência".

---

## 6. O funil completo (inferido)

```
Meta Ads (vídeo vertical, "marketing de intenção" aplicado a si mesmo)
   │  ← qualifica/filtra antes do clique (UTMify rastreia origem)
   ▼
VSL 27min (ConverteAI SmartPlayer, mede retenção) — luccasbraga.com/vsl-aqv01
   │  ← botão de checkout revelado abaixo do player
   ▼
Checkout R$197 / 12x R$20,25  (turma fundadora + bônus 15min)
   │
   ▼
[Provável] Order bump / upsell  → "bola de neve / reinvestimento" citado como "outra aula"
   │
   ▼
Workshop ao vivo "empresarização do corretor" (entregue no WhatsApp = captura de contato + LTV)
   │
   ▼
Comunidade WhatsApp (retenção, prova social, futuras ofertas)
```

**Observação:** ele aplica no próprio funil exatamente o que ensina — o anúncio "repele curioso", a VSL é o filtro, e o produto é o método. É um funil coerente e auto-referente ("a meta-prova").

---

## 7. Síntese executiva

| Camada | O que é |
|---|---|
| **Técnica** | Página estática + VTurb/ConverteAI + UTMify + GA4. Vídeo vertical HLS, 27 min. |
| **Oferta** | Curso "Anúncios que Vendem", 7 módulos, R$197 (ancorado em R$5k–10k), dupla garantia, vitalício. |
| **Tese** | Marketing de Intenção (repelir curioso) > Marketing de Atenção (viralizar). 3 elementos: ICP por motivação, imóvel como protagonista, elementos qualificativos. |
| **Persuasão** | VSL clássica: hook-case → origem → inimigo → mecanismo → valor → oferta → ancoragem → escassez → garantia → CTA binário. |
| **Diferencial real** | Coerência: ele *demonstra* a tese usando o próprio funil como prova viva. |

*Arquivos gerados localmente durante a análise: `transcript_timed.txt` (com timestamps) e `transcript.txt` (texto corrido).*

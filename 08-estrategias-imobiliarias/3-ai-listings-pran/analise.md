# Engenharia reversa — "AI Listings™" (Pran) · re-leads.store

> Página: `https://www.re-leads.store/` · sales page longa (advertorial), **sem VSL em vídeo**.
> Análise: 2026. Mecanismo deliberadamente velado na página (curiosity gap) — partes marcadas como **[dedução]**.

## 1. O que é
- **Produto:** **AI Listings™** — curso/sistema digital para **corretores de imóveis** (mercado global: EUA, Canadá, UK, Austrália, Europa, Ásia).
- **Promessa:** *"A brand new way of acquiring listings"* — assinar **30–50 captações/mês** usando **IA + ChatGPT**, **sem cold calling nem prospecção**, "em até 24h".
- **Autor:** "**Pran**" — narrativa de virada (150 ligações frias/dia e 2 captações → "#1 produtor numa rede de 17.000+ corretores").
- **Foco:** **listing acquisition** (captação — proprietários querendo vender), não a venda ao comprador.

## 2. Stack técnico (engenharia reversa da página)
| Item | Achado |
|---|---|
| Plataforma | **Wix** (HTML ~1,2 MB; título interno "RE WW 2" = *Real Estate WorldWide 2*) |
| Mídia | Sem VSL principal — **long-form sales letter** (texto + imagens). "Panda" no código era falso-positivo de fonte |
| Tracking | **Meta Pixel (`fbq`)** + **Google (`gtag`)** |
| Domínio | `.store` — padrão de funil de **baixo ticket por impulso** |
| Checkout/upsell | Externo (Stripe/CartPanda/ThriveCart provável), com order bumps/upsells **[dedução]** |

> Setup clássico: **tráfego pago frio (Meta) → advertorial → checkout de impulso $97**, Pixel otimizando Purchase.

## 3. A oferta
- **Preço:** **US$ 97** (único), ancorado em **$497–$997** + "**90% OFF**".
- **Escala de preço:** sobe **$10 a cada 100 pedidos** (degraus $87/$97/$107 vistos no código) — urgência matemática.
- **Escassez territorial:** "a cada hora que você espera, outro corretor da sua área compra isto" + animação de estoque baixo.
- **Bônus:** "How To Get Luxury Listings", vídeo-tutoriais ($197 alegado), mini-aula de "Pricing & Negotiation".
- **Garantia:** menção a reembolso/30 dias no código, **apagada da copy visível** (reduz fricção sem destacar).
- **Prova social:** Patrick (72h), Mark (3 leads/24h), Bradley (3 dias); name-drop de **Ryan Serhant**.
- **CTA:** repetido — "YES! I Want This!".

## 4. A estratégia ensinada — declarado × **[dedução]**

**Declarado (velado):** "use IA + ChatGPT, copy-paste, 30 min de setup, no automático, fecha até 90% dos prospects gelados, sem ligar."

**[Dedução de especialista]** — é o playbook padrão de captação dos EUA, o **funil de "home valuation"**:
```
1. ANÚNCIO PAGO (Meta) para PROPRIETÁRIOS de uma região
   → isca "Descubra quanto vale sua casa" (home valuation / "what's my home worth")
2. LANDING/FORM de avaliação grátis (CMA) captura endereço + contato
3. IA/ChatGPT faz o trabalho pesado:
   • gera criativos e copy dos anúncios
   • gera o relatório de avaliação personalizado
   • escreve follow-ups (SMS/e-mail) e scripts de objeção
4. QUALIFICAÇÃO + AGENDAMENTO automatizado (chatbot/IA) → reunião de listing
5. Corretor só aparece para ASSINAR a captação
```
Em uma frase: **trocar a prospecção fria por um funil de "avaliação gratuita de imóvel" movido a anúncio + IA**, com ChatGPT produzindo anúncios, relatórios e follow-ups.

## 5. Estrutura de persuasão (playbook low-ticket / advertorial)
Mecanismo único ("AI Listings") vs. inimigo ("cold calling") → história de virada do fundador → resultado extremo + velocidade (24h) → ancoragem $997→$97 → escala de preço por pedidos → escassez territorial → empilhamento de bônus → CTA repetido → **curiosity gap** (esconde o método para forçar a compra).

## 6. Veredito crítico / red flags
- ✅ Tese de fundo legítima: o funil de "home valuation" + automação é como muitos top-producers captam; IA acelera criativos/scripts.
- ⚠️ Embalagem de **impulso**: claims sem prova ("90% dos prospects gelados", "no automático"), garantia escondida, escassez artificial, método ocultado.
- ⚠️ "Sem budget" é enganoso: se o motor são anúncios pagos, **há custo de mídia** minimizado pela copy.
- ⚠️ Produto de aquisição em massa ($97) — provável funil de **upsells** caros depois.

**Resumo:** info-produto global de baixo ticket vendendo, com copy de impulso, um **funil de captação baseado em anúncios de "avaliação gratuita" + IA/ChatGPT** para criativos, relatórios e follow-up — substituindo a prospecção fria, com o mecanismo velado para maximizar a conversão no $97.

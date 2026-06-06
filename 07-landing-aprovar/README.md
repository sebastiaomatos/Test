# 07 · Landing pages prontas — Imobiliária Aprovar (Cuiabá/MT)

Duas landing pages de captação **100% prontas**, com o branding real da
**Aprovar Negócios Imobiliários** (extraído de imobiliariaaprovar.com.br), para **imóveis fictícios mas realistas** em Cuiabá-MT.

**Entregável:** [`Landing-Pages-Aprovar-Cuiaba.pdf`](Landing-Pages-Aprovar-Cuiaba.pdf) — capa, identidade aplicada,
e cada página em **desktop** (rolagem) + **mobile** (responsivo).

## Branding aplicado
| Token | Valor | Uso |
|---|---|---|
| Laranja Aprovar | `#F57F17` | CTAs, destaques, ícones |
| Verde-floresta | `#004310` | topo, rodapé, seções escuras |
| Verde WhatsApp | `#25D366` | botões de conversão |
| Areia/claro | `#F7F5EE` | seções alternadas |

Logo oficial (wordmark branco + selo redondo), slogan "Os melhores imóveis de Cuiabá e região",
WhatsApp/Tel **(65) 99232-6461**, **CRECI 9770J**, endereço no Carumbé.

## Imóveis (fictícios, realistas)
- **Residencial Cuiabá Park** — Apto 3q (1 suíte), 78 m², 2 vagas · Jardim Itália · **R$ 539.000** · `AP-1042`
- **Residencial Bem Viver** — Apto 2q (MCMV), 48 m², 1 vaga · Pedra 90 · **R$ 219.000** · `AP-2087`

## Páginas prontas (deployáveis)
`landing/apartamento-jardim-italia.html` e `landing/apartamento-pedra-90.html` — HTML self-contained
(CSS embutido, ícones SVG, deep links de WhatsApp já com o número da Aprovar). Em `landing/assets/`
ficam o logo oficial e as fotos (troque pelas reais do imóvel). É só hospedar.

## Reprodução (`src/`)
1. `build_landings.py` — gera as duas landings com o branding.
2. `render.py` — screenshots de página inteira (desktop 1280px + mobile 414px).
3. `build_pdf.py` — monta o PDF de apresentação.

> Fotos sob licença Creative Commons (placeholder). Logo e dados de contato são públicos da Aprovar.
> Imóveis e textos são fictícios para demonstração.

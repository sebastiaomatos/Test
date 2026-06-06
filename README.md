# Imóveis AQV — Sistema completo de marketing e vendas

Projeto que parte da **engenharia reversa** de uma VSL do mercado imobiliário e evolui para um
**sistema operacional completo** de aquisição e conversão: método, mídia paga, criativos, landing,
automações e gestão. Tudo deduzido e construído com a inteligência unificada de
*corretor + marketeiro + gestor de tráfego* de elite.

> **Objetivos do sistema:** leads de qualidade baratos e em escala · acelerar o fechamento ·
> aumentar a taxa de conversão dos atendimentos · vender mais.

---

## 📁 Estrutura do repositório

| Pasta | O que é | Entregável principal |
|---|---|---|
| **[00-fonte-vsl/](00-fonte-vsl/)** | Engenharia reversa da VSL original + transcrição completa (27 min) | `engenharia-reversa-vsl-aqv01.md` |
| **[01-apostila-metodo/](01-apostila-metodo/)** | Apostila ilustrada ensinando o método de venda (Marketing de Intenção) | `Apostila-Anuncios-que-Vendem-Imoveis.pdf` (29 p.) |
| **[02-playbook-midia/](02-playbook-midia/)** | Plano de mídia paga full-funnel: organogramas + 10 cards de anúncio | `Playbook-Campanhas-Pagas-Imoveis.pdf` (23 p.) |
| **[03-storyboards/](03-storyboards/)** | Roteiros cena a cena dos 3 formatos de vídeo | `Storyboards-3-Formatos-de-Video.pdf` |
| **[04-copy/](04-copy/)** | Banco de 111 variações de copy por ICP × plataforma | `Banco-de-Copy.pdf` + `banco-de-copy.csv` |
| **[05-landing-automacoes/](05-landing-automacoes/)** | Landing page deployável + réguas de WhatsApp e e-mail | `landing/` · `whatsapp/` · `email/` |
| **[06-gestao-kpis/](06-gestao-kpis/)** | Planilha de gestão de tráfego e funil (dashboard + semáforo) | `Planilha-Gestao-Trafego-e-Funil.xlsx` |

---

## 🧠 A tese (resumo do método)

**Marketing de Intenção, não de Atenção.** Em vez de viralizar e atrair todo mundo (curiosos),
criamos anúncios que **filtram o curioso e atraem o comprador real**, usando três elementos:

1. **ICP real** — mirar na *motivação de compra*, não na demografia.
2. **Imóvel protagonista** — o astro do vídeo é o imóvel, não o corretor.
3. **Elementos qualificativos** — preço, metragem e condição explícitos, que repelem o curioso.

Com os dados de venda voltando via **CAPI/CRM**, o algoritmo aprende a caçar mais compradores
(Lookalike). O lead fica mais barato, o atendimento mais rápido, e a venda vira sistema.

---

## 🚀 Por onde começar
1. Leia a **apostila** (01) para dominar o método.
2. Use o **playbook** (02) para montar as campanhas.
3. Produza criativos com os **storyboards** (03) e o **banco de copy** (04).
4. Publique a **landing** e ligue as **automações** (05).
5. Acompanhe tudo na **planilha** (06) e escale o que estiver ✅.

## 🛠️ Reprodutibilidade
Cada pasta com material gerado traz os scripts em `src/` (Python):
PDFs via **WeasyPrint**, infográficos/criativos via **Matplotlib/Pillow**, planilha via **openpyxl**.
Imagens fotográficas sob licença Creative Commons (Openverse); infográficos e mockups de produção própria.

> Conteúdo educacional/estratégico. Públicos, copy, orçamentos e KPIs são pontos de partida — calibre com os dados da sua praça.

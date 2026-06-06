# 05 · Landing page + Automações (WhatsApp & E-mail)

Pacote pronto para implementar a **captura** (landing) e a **conversão** (réguas automáticas).

```
05-landing-automacoes/
├── landing/                 Landing page estática, responsiva e deployável
│   ├── index.html           Estrutura + seções (hero, qualificativos, galeria, prova, FAQ, CTA)
│   ├── style.css            Identidade visual (dark + dourado), mobile-first
│   ├── script.js            ⚙️ CONFIGURE AQUI: telefone, endpoint do CRM, UTMs
│   └── assets/              Imagens (troque pelas fotos reais do imóvel)
├── whatsapp/
│   ├── fluxo-whatsapp.md     Régua documentada (mensagens, tempos, ramificações)
│   └── fluxo-whatsapp.json   Mesmo fluxo em formato de nós (importável em builders)
└── email/
    ├── email-1..6.html       6 e-mails responsivos (email-safe)
    ├── emails.md             Índice (assunto, disparo, objetivo)
    └── make_emails.py        Gerador dos e-mails
```

## Como publicar a landing
1. Abra `landing/script.js` e ajuste:
   - `CONFIG.phone` → seu número (DDI+DDD+número, só dígitos).
   - `CONFIG.formEndpoint` → URL do webhook/CRM (deixe vazio para usar só WhatsApp).
2. Troque as imagens em `landing/assets/` pelas fotos reais e os textos entre `[colchetes]`.
3. Suba os arquivos em qualquer hospedagem estática (Netlify, Vercel, GitHub Pages, Hostinger).
4. Adicione o **Pixel da Meta** e o **GA4** no `<head>` — o `script.js` já dispara os eventos
   `click_whatsapp`, `lead_submit` e `engaged_15s`.

## Destaques técnicos
- **Captura de UTM/clids** automática e repasse para o WhatsApp e para o CRM (atribuição).
- **Deep link de WhatsApp** com mensagem pré-preenchida por seção.
- Formulário com validação, qualificação (intenção + pagamento) e redirecionamento ao WhatsApp.
- Botão flutuante de WhatsApp com animação.

## Como usar as automações
- **WhatsApp:** importe a lógica de `fluxo-whatsapp.json` no seu builder (ManyChat, 360dialog, Kommo, Z-API)
  ou siga `fluxo-whatsapp.md` manualmente. Dispare `M0` no minuto 0; pare a régua quando o lead responder.
- **E-mail:** suba os 6 HTMLs na sua ferramenta (RD Station, Mailchimp, ActiveCampaign) com os disparos de
  `emails.md`. Configure remetente e ajuste o link do WhatsApp em `make_emails.py` e regenere.

> Objetivo das automações: **responder em < 5 min**, qualificar, agendar visita e **recuperar quem esfria** —
> acelerando o fechamento e elevando a taxa de conversão dos atendimentos atuais.

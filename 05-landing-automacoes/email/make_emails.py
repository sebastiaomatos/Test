#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera 6 e-mails responsivos (email-safe, tabelas + inline) + índice markdown."""
import os
BASE=os.path.dirname(os.path.abspath(__file__))
WA="https://wa.me/5582990000000?text=Oi!%20Vim%20pelo%20e-mail%20e%20quero%20saber%20mais%20sobre%20o%20ap%C3%AA%20no%20%5BBairro%5D."

GOLD="#D8A84B"; DARK="#14110E"; CREAM="#F4EEE2"; INK="#2b2620"; WA_G="#25D366"; LINE="#e7ddc7"

def shell(subject, preheader, blocks, cta_text="Falar no WhatsApp"):
    body="".join(blocks)
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="x-apple-disable-message-reformatting">
<title>{subject}</title></head>
<body style="margin:0;padding:0;background:#efe9dc;font-family:Arial,Helvetica,sans-serif;color:{INK};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#efe9dc;padding:24px 12px;">
<tr><td align="center">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:14px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.08);">
    <!-- header -->
    <tr><td style="background:{DARK};padding:20px 28px;">
      <span style="color:{CREAM};font-size:20px;font-weight:bold;">Imóveis<span style="color:{GOLD};">AQV</span></span>
    </td></tr>
    <!-- body -->
    <tr><td style="padding:30px 28px 8px;">
      {body}
    </td></tr>
    <!-- CTA -->
    <tr><td align="center" style="padding:8px 28px 30px;">
      <a href="{WA}" style="display:inline-block;background:{WA_G};color:#fff;text-decoration:none;font-weight:bold;font-size:16px;padding:15px 34px;border-radius:999px;">{cta_text} →</a>
    </td></tr>
    <!-- footer -->
    <tr><td style="background:#0f0d0a;padding:18px 28px;color:#9a8b6a;font-size:11px;line-height:1.6;">
      Imóveis AQV · CRECI 00000-F · [Cidade]/[UF]<br>
      Você recebe este e-mail porque demonstrou interesse em um de nossos imóveis.
      <a href="#" style="color:#c9b88e;">Descadastrar</a>. Imagens ilustrativas.
    </td></tr>
  </table>
</td></tr></table></body></html>"""

def h(txt): return f'<h1 style="font-size:23px;line-height:1.25;margin:0 0 14px;color:{DARK};">{txt}</h1>'
def p(txt): return f'<p style="font-size:15px;line-height:1.65;margin:0 0 14px;color:#3a342b;">{txt}</p>'
def quote(txt): return f'<table role="presentation" width="100%"><tr><td style="border-left:4px solid {GOLD};background:#faf6ec;padding:14px 18px;font-style:italic;font-size:15px;color:#3a342b;border-radius:0 8px 8px 0;">{txt}</td></tr></table><div style="height:14px;"></div>'
def bullets(items):
    li="".join(f'<tr><td style="vertical-align:top;color:{GOLD};font-weight:bold;padding:2px 8px 2px 0;">✓</td><td style="font-size:15px;color:#3a342b;padding:2px 0;">{i}</td></tr>' for i in items)
    return f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 14px;">{li}</table>'

EMAILS=[
 dict(file="email-1-boasvindas.html", dia="Imediato",
   subject="Recebi seu interesse — próximos passos",
   preheader="Bora agilizar? Te respondo no WhatsApp em minutos.",
   cta="Falar agora no WhatsApp",
   blocks=[h("Oi! Que bom te ver por aqui 👋"),
     p("Recebi seu interesse no apê de 2 quartos no <b>[Bairro]</b>. Pra agilizar (e porque é por ali que tudo acontece mais rápido), me chama no WhatsApp que eu já te mando o vídeo por dentro e simulo a sua parcela."),
     p("No WhatsApp consigo te responder em minutos e até agendar uma visita pra você ver pessoalmente.")]),
 dict(file="email-2-prova.html", dia="Dia 1",
   subject="Vendi um imóvel de R$ 400 mil com R$ 16 de anúncio",
   preheader="A história por trás de uma venda que não dependeu de sorte.",
   cta="Quero ver os imóveis disponíveis",
   blocks=[h("Uma venda que não dependeu de sorte"),
     p("Um cliente viu um anúncio simples, me chamou no WhatsApp e, no mesmo dia, marcou a visita. Cinco dias depois, financiamento aprovado. Imóvel de quase R$ 400 mil."),
     quote("“Comprei sem nunca ter visto o corretor antes. Foi rápido e sem enrolação.”"),
     p("O segredo não foi dancinha nem sorte: foi mostrar o imóvel certo, com a informação certa, pra pessoa certa. É exatamente o que eu quero fazer por você.")]),
 dict(file="email-3-financiamento.html", dia="Dia 2",
   subject="Financiamento pela Caixa: o passo a passo (sem letra miúda)",
   preheader="Entenda como sair do aluguel usando o FGTS na entrada.",
   cta="Quero simular minha parcela",
   blocks=[h("Como funciona, na prática"),
     p("Muita gente acha que não consegue financiar — e poderia. Veja o caminho simplificado:"),
     bullets(["Verificamos se você pode usar o <b>FGTS</b> na entrada (3 anos de carteira somados).",
              "Fazemos a <b>simulação</b> da parcela com base na sua renda.",
              "A Caixa faz a <b>análise de crédito</b> (rápida na maioria dos casos).",
              "Aprovado, você assina e recebe a <b>chave</b>."]),
     p("Quer que eu faça a simulação pra você agora? Em 2 minutos no WhatsApp te mostro os números reais.")]),
 dict(file="email-4-imovel.html", dia="Dia 4",
   subject="Separei este apê pensando em você",
   preheader="2 quartos, pronto pra morar, com condição especial.",
   cta="Quero ver por dentro",
   blocks=[h("Esse aqui tem tudo a ver com o que você procura"),
     p("<b>Apê de 2 quartos no [Bairro]</b> — 68m², 1 vaga, pronto pra morar. A partir de <b>R$ 389.000</b>, financia pela Caixa e usa o FGTS na entrada."),
     bullets(["Sala integrada e cozinha com armários","Suíte + quarto","Varanda com vista livre","Lazer completo: piscina, academia, salão"]),
     p("Posso te mostrar por dentro hoje mesmo. Me chama no WhatsApp que eu te envio o vídeo e marco sua visita.")]),
 dict(file="email-5-escassez.html", dia="Dia 6",
   subject="A condição da entrada termina sexta",
   preheader="Restam poucas unidades nessa faixa.",
   cta="Quero garantir minha unidade",
   blocks=[h("Não quero que você perca isso"),
     p("A condição especial de entrada do apê no <b>[Bairro]</b> vai até <b>sexta-feira</b>, e restam poucas unidades nessa metragem."),
     p("Se sair do aluguel ainda este ano está nos seus planos, esse é o momento de garantir a simulação no seu nome — sem compromisso."),
     quote("“Vi, chamei no WhatsApp e visitei no mesmo dia. Fechei na semana.”")]),
 dict(file="email-6-reativacao.html", dia="Dia 10",
   subject="Ainda procurando? Tenho 3 opções novas",
   preheader="Selecionei imóveis no seu perfil e faixa de preço.",
   cta="Quero ver as 3 opções",
   blocks=[h("Talvez uma destas seja a sua"),
     p("Se o primeiro apê não foi exatamente o que você queria, sem problema — selecionei <b>3 opções novas</b> no mesmo perfil e faixa de preço."),
     p("Me chama no WhatsApp que eu te mando os vídeos das três e a gente vê juntos qual faz mais sentido. Assim você não perde tempo nem viagem.")]),
]

idx=["# Sequência de e-mail — Imóveis AQV\n",
     "Nutrição automática para leads que deixaram e-mail (Lead Ads / landing). Cada e-mail tem **um único CTA**: voltar para a conversa no WhatsApp. Configure o remetente e o link do WhatsApp em `make_emails.py`.\n",
     "| # | Disparo | Assunto | Objetivo |","|---|---|---|---|"]
goals=["Boas-vindas + levar pro WhatsApp","História/prova → autoridade","Conteúdo útil → reciprocidade",
       "Oferta do imóvel do ICP","Escassez + CTA visita","Reativação"]
for e,g in zip(EMAILS,goals):
    open(os.path.join(BASE,e["file"]),"w",encoding="utf-8").write(
        shell(e["subject"],e["preheader"],e["blocks"],e["cta"]))
    idx.append(f'| {e["file"].split("-")[1]} | {e["dia"]} | {e["subject"]} | {g} |')
open(os.path.join(BASE,"emails.md"),"w",encoding="utf-8").write("\n".join(idx)+"\n")
print("Gerados",len(EMAILS),"e-mails + emails.md")

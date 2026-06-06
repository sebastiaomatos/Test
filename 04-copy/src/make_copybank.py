#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Banco de copy por ICP x plataforma -> CSV + HTML (para PDF)."""
import csv, os, html
BASE="/home/user/Test/04-copy"; os.makedirs(BASE,exist_ok=True)

# Cada ICP: headlines Meta, textos primários Meta, headlines Google, descrições Google, ganchos TikTok
ICPS=[
{"id":"aluguel","nome":"Sair do aluguel / Minha Casa Minha Vida","cor":"#4CB286",
 "meta_headlines":[
   "2 quartos no [Bairro]: R$ 389 mil, pronto pra morar",
   "Saia do aluguel ainda este ano",
   "Financia pela Caixa e usa o FGTS na entrada",
   "Seu primeiro apê custa menos do que você imagina",
   "Cansou de pagar aluguel? Esse apê resolve",
   "Apê de 2 quartos com parcela que cabe no bolso",
   "Pare de pagar o financiamento do seu vizinho",
   "R$ 389 mil: o apê que tira você do aluguel",
   "MCMV: entrada facilitada e chave na mão",
   "Use seu FGTS de entrada e saia do aluguel",
   "Apê pronto pra morar perto de tudo no [Bairro]",
   "Parcela parecida com o aluguel — só que é seu"],
 "meta_textos":[
   "Você paga aluguel há anos e o imóvel nunca fica seu. Esse apê de 2 quartos no [Bairro] sai por R$ 389 mil, financia pela Caixa e ainda usa o FGTS na entrada. Me chama no WhatsApp que eu simulo sua parcela hoje.",
   "Imagina parar de pagar aluguel e essa parcela virar SEU apartamento. 2 quartos, 1 vaga, pronto pra morar. Te explico a condição em 2 minutos no WhatsApp.",
   "Sem entrada gigante, sem burocracia. Apê de 2 quartos no [Bairro] com financiamento pela Caixa e FGTS na entrada. Quer simular? Chama aqui.",
   "Aluguel é dinheiro que não volta. Esse apê pronto pra morar muda isso. Me manda mensagem que eu te mostro por dentro e simulo o financiamento.",
   "A parcela desse apê é parecida com o aluguel que você já paga — só que no fim ele é seu. R$ 389 mil, financia + FGTS. Bora conversar no WhatsApp?",
   "Você não precisa de muito pra começar. FGTS de entrada + financiamento Caixa e a chave é sua. Te explico tudo no WhatsApp, sem compromisso."]},
{"id":"upgrade","nome":"Upgrade / Médio padrão (família crescendo)","cor":"#5B8DB8",
 "meta_headlines":[
   "Seu apê ficou pequeno? Veja este de 3 quartos",
   "Mais espaço pros filhos no [Bairro]",
   "Hora de trocar o compacto por um maior",
   "3 quartos, varanda gourmet e melhor bairro",
   "O upgrade que sua família merece",
   "Saia do apê apertado sem sair do orçamento",
   "Mais quarto, mais lazer, mesmo bairro que você ama",
   "A casa que cresce junto com a sua família",
   "Troque de apê usando o seu como entrada",
   "Espaço de verdade pra quem trabalha em casa",
   "3 quartos no [Bairro] com lazer completo",
   "Da sala pequena pra varanda gourmet"],
 "meta_textos":[
   "A família cresceu e o apê continuou do mesmo tamanho? Esse de 3 quartos no [Bairro] tem varanda gourmet, suíte e lazer completo. Aceito seu imóvel atual como entrada. Chama no WhatsApp.",
   "Mais um filho, home office, visitas… e o espaço some. Hora do upgrade: 3 quartos, 2 vagas, varanda gourmet. Te mostro por dentro no WhatsApp.",
   "Você merece mais espaço sem mudar de cidade. 3 quartos no mesmo bairro que você já gosta, com lazer completo. Me chama que eu te explico a condição.",
   "Trocar de apê é mais fácil do que parece: uso o seu atual na negociação. 3 quartos, suíte, varanda gourmet. Conversa comigo no WhatsApp.",
   "Espaço pros filhos brincarem, varanda pra receber, suíte pra você. Esse apê foi feito pra próxima fase da sua família. Bora ver por dentro?",
   "Seu apê pequeno pode ser a entrada do seu apê grande. Te mostro como no WhatsApp — sem compromisso."]},
{"id":"alto","nome":"Alto padrão / Frente-mar","cor":"#D8A84B",
 "meta_headlines":[
   "Cobertura frente-mar, pronta pra morar",
   "Vista permanente: não tem prédio na frente",
   "Alto padrão no [Bairro] mais valorizado",
   "3 suítes, 2 vagas e o mar como vizinho",
   "O endereço que fala por você",
   "Frente-mar de verdade, não 'vista lateral'",
   "Cobertura duplex com piscina privativa",
   "Para quem já tem e quer o melhor",
   "Lazer de resort no seu condomínio",
   "Acordar com o mar todos os dias",
   "Alto padrão pronto pra morar — agende sua visita",
   "Exclusividade frente-mar no [Bairro]"],
 "meta_textos":[
   "Vista permanente para o mar, 3 suítes, 2 vagas e lazer de resort. Uma cobertura frente-mar no [Bairro] que não depende de sorte: não tem prédio na frente. Agende sua visita pelo WhatsApp.",
   "Você trabalhou pra chegar aqui. Que tal acordar com o mar todos os dias? Cobertura frente-mar, acabamento de alto padrão, pronta pra morar. Vamos conversar?",
   "Endereço, vista e acabamento que combinam com o seu momento. Cobertura no [Bairro] com piscina privativa. Atendimento reservado pelo WhatsApp.",
   "Frente-mar de verdade é raro. Essa unidade tem vista permanente e lazer completo. Posso te mostrar pessoalmente — me chama no WhatsApp.",
   "Quem busca alto padrão não quer 'mais um apê'. Quer o melhor endereço, a melhor vista, o melhor acabamento. É exatamente isso. Agende sua visita.",
   "Discrição, exclusividade e o mar na sua janela. Atendimento personalizado pelo WhatsApp para essa cobertura frente-mar."]},
{"id":"investidor","nome":"Investidor / Renda de temporada","cor":"#C58FBF",
 "meta_headlines":[
   "O aluguel paga a parcela: studio frente-mar",
   "Investidor: receba o estudo de rentabilidade",
   "Renda de temporada na praia mais procurada",
   "Studio que se paga com Airbnb",
   "Valorização + renda no [Bairro] turístico",
   "Diversifique seu patrimônio com tijolo",
   "ROI de temporada que o CDB não dá",
   "Comprou na planta, valorizou na entrega",
   "Imóvel pra render, não pra morar",
   "Frente-mar: alta demanda o ano inteiro",
   "Seu dinheiro rendendo com vista pro mar",
   "Studio frente-mar com gestão de locação"],
 "meta_textos":[
   "Esse studio frente-mar foi feito pra render: alta demanda de temporada o ano inteiro e o aluguel cobrindo a parcela. Quer o estudo de rentabilidade da unidade? Me chama no WhatsApp que eu te envio.",
   "Enquanto o CDB rende pouco, um studio bem localizado rende aluguel + valorização. Te mando o estudo completo com projeção de ROI. Chama no WhatsApp.",
   "Investir em imóvel na praia mais procurada não é sorte, é estratégia. Recebe o estudo de rentabilidade e a projeção de ocupação. Me manda mensagem.",
   "Comprar na planta hoje é valorizar na entrega. Studio frente-mar com gestão de locação inclusa. Quer os números? Te envio pelo WhatsApp.",
   "Patrimônio que rende todo mês e ainda valoriza. Studio frente-mar com alta demanda de temporada. Receba o estudo de rentabilidade agora.",
   "Diversificar com tijolo é segurança + renda. Te mostro a projeção de retorno desse studio frente-mar. Chama no WhatsApp."]},
]

GOOGLE_HEADLINES=[
 "Apartamento em [Cidade]","2 Quartos a Partir de R$389mil","Pronto pra Morar","Financia pela Caixa",
 "Use o FGTS na Entrada","Visita no Mesmo Dia","Frente-Mar em [Cidade]","Alto Padrão [Bairro]",
 "Studio para Investir","Fale no WhatsApp Agora","Sem Burocracia","Agende sua Visita",
 "Imóvel na Planta [Cidade]","3 Quartos com Lazer","Condição Especial Hoje"]
GOOGLE_DESC=[
 "Apartamentos prontos pra morar no [Bairro]. Financia pela Caixa e usa FGTS. Fale no WhatsApp.",
 "Visita no mesmo dia, sem burocracia. Agende agora e conheça as unidades disponíveis.",
 "Frente-mar com vista permanente. Atendimento rápido pelo WhatsApp. Agende sua visita.",
 "Studio para renda de temporada. Receba o estudo de rentabilidade. Fale com um especialista.",
 "Saia do aluguel ainda este ano. Simule seu financiamento em 2 minutos. Chama no WhatsApp.",
 "3 quartos, varanda gourmet e lazer completo. Aceito seu imóvel na troca. Agende a visita."]
TIKTOK_HOOKS=[
 "Saiu do aluguel aos 26 👀 olha o apê novo",
 "POV: você descobre que a parcela é igual ao aluguel",
 "Ninguém te conta que dá pra usar o FGTS assim",
 "Esse apê de R$389 mil tem algo que os caros não têm",
 "Comenta 'QUERO' que eu te mando a simulação",
 "3 motivos pra sair do aluguel esse ano (o 2 choca)",
 "Mostrei esse apê e venderam no mesmo dia",
 "Investidor, esse studio se paga sozinho 🏖️"]
CTAS=["Enviar mensagem","Falar no WhatsApp","Saiba mais","Quero simular","Agendar visita",
      "Receber o estudo","Ver condição","Quero saber o preço","Chamar agora","Garantir minha unidade"]

# ---------- CSV ----------
rows=[]
for icp in ICPS:
    for h in icp["meta_headlines"]: rows.append([icp["nome"],"Meta","Título (headline)",h])
    for t in icp["meta_textos"]: rows.append([icp["nome"],"Meta","Texto primário",t])
for h in GOOGLE_HEADLINES: rows.append(["Todos","Google Search","Headline (≤30c)",h])
for dsc in GOOGLE_DESC: rows.append(["Todos","Google Search","Descrição (≤90c)",dsc])
for h in TIKTOK_HOOKS: rows.append(["Todos","TikTok","Gancho/legenda",h])
for c in CTAS: rows.append(["Todos","Todas","CTA",c])
with open(f"{BASE}/banco-de-copy.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["ICP","Plataforma","Tipo","Texto"]); w.writerows(rows)
print("CSV linhas:",len(rows))

# ---------- HTML ----------
def esc(s): return html.escape(s)
H=['<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><style>',
'''@page{size:A4; margin:16mm 15mm 18mm; @bottom-center{content:"BANCO DE COPY · por ICP e plataforma"; font-family:Georgia,serif; font-size:8pt; color:#9a8b6a;} @bottom-right{content:counter(page); font-family:Georgia,serif; font-size:9pt; color:#b08d3a;}}
@page :first{margin:0; @bottom-center{content:""} @bottom-right{content:""}}
*{box-sizing:border-box} html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Helvetica Neue',Arial,sans-serif; color:#2b2620; font-size:9.6pt; line-height:1.5; margin:0;}
.cover{height:297mm; background:linear-gradient(120deg,#14110E,#2a2118); color:#f4eee2; padding:34mm 22mm; page-break-after:always;}
.cover .kick{letter-spacing:4px; color:#E0B84C; text-transform:uppercase; font-size:11pt;}
.cover h1{font-size:40pt; margin:12mm 0 5mm; font-weight:800;} .cover h1 span{color:#E0B84C;}
.cover .sub{font-family:Georgia,serif; font-style:italic; font-size:14pt; color:#e8e1d2; max-width:150mm;}
h2{font-size:15pt; color:#fff; background:#14110E; padding:3mm 4mm; border-radius:6px; margin:0 0 3mm; page-break-before:always;}
h2 .pill{font-size:8.5pt; padding:2px 8px; border-radius:5px; color:#14110E; margin-left:6px; vertical-align:middle;}
h3{font-size:10.5pt; color:#9a6f17; margin:4mm 0 1mm; border-bottom:1px solid #e6d29a; padding-bottom:1mm;}
ol{margin:1mm 0 3mm; padding-left:7mm;} ol li{margin-bottom:1.6mm; break-inside:avoid;}
.txt li{font-family:Georgia,serif;}
.intro{font-family:Georgia,serif; font-style:italic; color:#4a4234; border-left:3px solid #d8b35a; padding-left:5mm; margin:3mm 0;}
.note{background:#faf5e9; border:1px solid #e6d29a; border-left:5px solid #d8b35a; border-radius:6px; padding:3mm 4mm; margin:3mm 0; font-size:9pt;}
.cols{columns:2; column-gap:8mm;} .cols li{break-inside:avoid;}
code{background:#f0ead9; padding:1px 4px; border-radius:3px; font-size:8.6pt;}</style></head><body>''',
'<div class="cover"><div class="kick">Criativos · textos prontos para testar</div>',
'<h1>BANCO DE <span>COPY</span></h1>',
'<div class="sub">Títulos, textos, headlines de Search, ganchos de TikTok e CTAs — organizados por ICP e por plataforma. Copie, adapte os [colchetes] e suba para teste.</div>',
'<div style="position:absolute;bottom:30mm;left:22mm;border-left:3px solid #E0B84C;padding-left:6mm;color:#d8cdb6;font-size:10pt;line-height:1.7;">4 ICPs · Meta · Google · TikTok<br>+ de 90 variações · exporta em CSV pronto pra importar</div></div>',
'<h2 style="page-break-before:auto;">Como usar este banco</h2>',
'<p class="intro">Todo texto aqui respeita o método: o gancho filtra o curioso e os qualificativos aparecem cedo. Troque os <code>[colchetes]</code> pelos dados reais do imóvel/praça. Suba pelo menos 3 variações de título por conjunto e deixe o algoritmo escolher o vencedor. O arquivo <code>banco-de-copy.csv</code> traz tudo em planilha.</p>',
'<div class="note"><strong>Regra de teste:</strong> 1 conjunto de anúncios = 1 ICP. Varie o título (gancho), mantenha a oferta. Pause o que tiver custo por conversa 2× acima do melhor e dobre no vencedor.</div>']

for icp in ICPS:
    H.append(f'<h2>ICP · {esc(icp["nome"])} <span class="pill" style="background:{icp["cor"]}">META + variações</span></h2>')
    H.append('<h3>Títulos / Headlines (Meta)</h3><ol>')
    for h in icp["meta_headlines"]: H.append(f"<li>{esc(h)}</li>")
    H.append('</ol><h3>Textos primários (Meta)</h3><ol class="txt">')
    for t in icp["meta_textos"]: H.append(f"<li>{esc(t)}</li>")
    H.append('</ol>')

H.append('<h2>Google Search — banco compartilhado</h2>')
H.append('<h3>Headlines (até ~30 caracteres)</h3><ol class="cols">')
for h in GOOGLE_HEADLINES: H.append(f"<li>{esc(h)}</li>")
H.append('</ol><h3>Descrições (até ~90 caracteres)</h3><ol>')
for d in GOOGLE_DESC: H.append(f"<li>{esc(d)}</li>")
H.append('</ol><div class="note">Monte 1 RSA com 10–15 headlines + 4 descrições e deixe o Google combinar. Capriche nas <strong>palavras negativas</strong> (aluguel, curso, emprego, planta baixa) pra não pagar por curioso.</div>')

H.append('<h2>TikTok — ganchos e CTAs gerais</h2>')
H.append('<h3>Ganchos / legendas (TikTok)</h3><ol>')
for h in TIKTOK_HOOKS: H.append(f"<li>{esc(h)}</li>")
H.append('</ol><h3>CTAs (todas as plataformas)</h3><ol class="cols">')
for c in CTAS: H.append(f"<li>{esc(c)}</li>")
H.append('</ol>')
H.append('</body></html>')
open(f"{BASE}/src/banco-de-copy.html","w",encoding="utf-8").write("\n".join(H))
print("HTML ok")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagramas + criativos para o playbook AI Listings."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
OUT="/home/user/Test/09-playbook-ai-listings/img"; os.makedirs(OUT,exist_ok=True)
FD="/usr/local/lib/python3.11/dist-packages/matplotlib/mpl-data/fonts/ttf"
def F(sz,b=True): return ImageFont.truetype(os.path.join(FD,"DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"),sz)

# tech palette
BG="#0E1B2A"; PANEL="#16293c"; PANEL2="#1d3447"; CYAN="#38C6E0"; CY2="#6FE0F0"
AMBER="#F2B23E"; CREAM="#EAF2F7"; MUTE="#8aa0b2"; GOOD="#3FB984"; AI="#9B7BE0"
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":CREAM})
def fig(w,h):
    f=plt.figure(figsize=(w,h),dpi=170);ax=f.add_axes([0,0,1,1]);ax.set_xlim(0,100);ax.set_ylim(0,100)
    ax.axis("off");f.patch.set_facecolor(BG);ax.set_facecolor(BG);return f,ax
def box(ax,x,y,w,h,fc=PANEL,ec=CYAN,lw=1.8,rad=2.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.15,rounding_size={rad}",fc=fc,ec=ec,lw=lw))
def t(ax,x,y,s,size=11,color=CREAM,w="normal",ha="center",va="center",style="normal"):
    ax.text(x,y,s,fontsize=size,color=color,weight=w,ha=ha,va=va,style=style,zorder=6)
def arr(ax,x1,y1,x2,y2,color=CYAN,lw=2.2,style="-|>",rad=0.0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=18,lw=lw,color=color,connectionstyle=f"arc3,rad={rad}",zorder=3))
def chip(ax,x,y,w,lab,c):
    box(ax,x,y,w,5.2,fc=c,ec=c,rad=2.6);t(ax,x+w/2,y+2.6,lab,size=8.7,color="#0E1B2A",w="bold")
def save(f,n):f.savefig(f"{OUT}/{n}",facecolor=BG);plt.close(f);print("saved",n)

# A1 — FUNIL
f,ax=fig(12,7)
t(ax,50,95,"O FUNIL AI LISTINGS (CAPTAÇÃO COM IA)",size=20,color=CYAN,w="bold")
t(ax,50,90,"trocar a prospecção fria por anúncio de “avaliação gratuita” + IA fazendo o trabalho pesado",size=10.5,color=MUTE,style="italic")
steps=[("1 · ANÚNCIO","Meta Ads p/ PROPRIETÁRIOS\n“Quanto vale sua casa?”",CYAN,9),
       ("2 · LANDING","Form de avaliação grátis\n(endereço + contato)",CYAN,29.5),
       ("3 · RELATÓRIO IA","ChatGPT gera o laudo\n(CMA) personalizado",AI,50),
       ("4 · QUALIFICA","Bot/IA qualifica e\nagenda a reunião",AMBER,70.5),
       ("5 · CAPTAÇÃO","Corretor só aparece\npara ASSINAR",GOOD,91)]
# horizontally arranged 5 boxes (use 2 rows? keep 5 across)
xs=[3,22.5,42,61.5,81];
for (titf,desc,c,_),x in zip(steps,xs):
    box(ax,x,55,17,22,fc=PANEL,ec=c,lw=2.2)
    t(ax,x+8.5,71,titf,size=10.5,color=c,w="bold")
    t(ax,x+8.5,62,desc,size=8.3,color=CREAM)
for x in xs[:-1]: arr(ax,x+17,66,x+19.5,66,color=CYAN)
# IA layer
box(ax,10,30,80,12,fc=PANEL2,ec=AI,lw=2)
t(ax,50,38,"CAMADA DE IA / CHATGPT (o que substitui o esforço manual)",size=11,color=AI,w="bold")
for x,lab in zip([14,32,50,68,82],["criativos","copy do anúncio","laudo CMA","follow-up","scripts de objeção"]):
    chip(ax,x-6,31.5,13 if len(lab)>8 else 11,lab,AI)
arr(ax,50,55,50,42,color=AI,lw=2)
# bottom note
t(ax,50,22,"Resultado prometido: 30–50 captações/mês — sem cold calling",size=11,color=AMBER,w="bold")
t(ax,50,16,"Atenção: o motor são ANÚNCIOS PAGOS (há custo de mídia, minimizado na copy do produto)",size=8.6,color=MUTE,style="italic")
save(f,"A1_funil.png")

# A2 — ONDE A IA ENTRA
f,ax=fig(11,6.6)
t(ax,50,94,"ONDE A IA/CHATGPT ENTRA NO FUNIL",size=18,color=AI,w="bold")
t(ax,50,89,"cinco tarefas que antes consumiam horas, agora em minutos",size=10,color=MUTE,style="italic")
items=[("Criativos & ângulos","Gera variações de anúncio (imagem/headline) por bairro e perfil",CYAN),
       ("Laudo de avaliação (CMA)","Transforma dados em um relatório claro e persuasivo de valor do imóvel",AI),
       ("Sequência de follow-up","Escreve SMS/e-mail para cada etapa e cada objeção do vendedor",AMBER),
       ("Scripts de objeção","“Vou pensar”, “comissão”, “outro corretor” — respostas prontas",GOOD),
       ("Apresentação de listing","Monta a listing presentation para a reunião de captação",CY2)]
y=76
for i,(titf,desc,c) in enumerate(items):
    box(ax,8,y-7,84,9.5,fc=PANEL,ec=c,lw=1.8)
    ax.add_patch(Circle((14,y-2.2),3,fc=c,ec=BG,lw=1.5,zorder=5));t(ax,14,y-2.2,str(i+1),size=12,color="#0E1B2A",w="bold")
    t(ax,20,y+0.5,titf,size=11,color=c,w="bold",ha="left")
    t(ax,20,y-4,desc,size=8.7,color=CREAM,ha="left")
    y-=13.2
save(f,"A2_camada_ia.png")

# A3 — CADENCIA FOLLOW-UP VENDEDOR
f,ax=fig(11,6)
t(ax,50,93,"CADÊNCIA DE FOLLOW-UP DO VENDEDOR",size=17,color=CYAN,w="bold")
t(ax,50,87,"o lead de avaliação esfria rápido — IA dispara na hora certa",size=10,color=MUTE,style="italic")
fu=[("0 min","Entrega do laudo + “posso te explicar em 2 min?”",CYAN),
    ("5 min","SMS: “recebeu sua avaliação? alguma dúvida?”",CY2),
    ("Dia 1","Prova social local: “vendi 3 casas no seu bairro”",AMBER),
    ("Dia 3","Gatilho de mercado: “demanda alta na sua região agora”",AMBER),
    ("Dia 7","Oferta da reunião: “15 min p/ um plano de venda”",GOOD),
    ("Dia 14","Reativação: “posso refazer a avaliação atualizada?”",MUTE)]
x=8
for d,desc,c in fu:
    box(ax,x,40,13.5,28,fc=PANEL,ec=c,lw=1.8)
    t(ax,x+6.75,63,d,size=10.5,color=c,w="bold")
    t(ax,x+6.75,52,desc,size=7.4,color=CREAM)
    x+=15
for xx in [21.5,36.5,51.5,66.5,81.5]: arr(ax,xx,54,xx+1.5,54,color=CYAN,lw=1.8)
t(ax,50,30,"Tudo escrito pela IA e disparado por automação (CRM/SMS/e-mail).",size=9.5,color=AMBER,w="bold")
save(f,"A3_cadencia.png")

# A4 — STACK
f,ax=fig(11,5.6)
t(ax,50,92,"STACK DE FERRAMENTAS",size=17,color=CYAN,w="bold")
tools=[("Meta Ads","tráfego frio p/ proprietários",CYAN),
       ("Landing + Form","avaliação grátis (endereço)",CYAN),
       ("ChatGPT","criativo · laudo · follow-up · scripts",AI),
       ("CRM + Automação","SMS/e-mail · qualificação · agenda",AMBER),
       ("Agendamento","reunião de listing (Calendly)",GOOD)]
xs=[4,23,42,61,80]
for (n,d,c),x in zip(tools,xs):
    box(ax,x,40,17,30,fc=PANEL,ec=c,lw=2)
    t(ax,x+8.5,62,n,size=11,color=c,w="bold")
    t(ax,x+8.5,50,d,size=8,color=CREAM)
for x in xs[:-1]: arr(ax,x+17,55,x+19,55,color=MUTE,lw=1.6)
t(ax,50,28,"Pixel da Meta + eventos do CRM realimentam a otimização e o público semelhante.",size=9.2,color=MUTE,style="italic")
save(f,"A4_stack.png")

# ============ CREATIVES (PIL) ============
GOLD=(242,178,62);DARK=(14,27,42);CREAMc=(234,242,247);CYANc=(56,198,224);WA=(37,211,102)
def load(name,size,foc=0.5):
    im=Image.open(f"{OUT}/{name}").convert("RGB");return ImageOps.fit(im,size,Image.LANCZOS,centering=(0.5,foc))
def grad(img,a0=20,a1=200):
    w,h=img.size;ov=Image.new("L",(1,h),0)
    for y in range(h):ov.putpixel((0,y),int(a0+(a1-a0)*(y/h)**1.4))
    return Image.composite(Image.new("RGB",(w,h),(0,0,0)),img,ov.resize((w,h)))
def wrap(d,txt,f,mw):
    out=[];cur=""
    for w in txt.split():
        tt=(cur+" "+w).strip()
        if d.textlength(tt,font=f)<=mw:cur=tt
        else:out.append(cur);cur=w
    if cur:out.append(cur)
    return out

# Meta ad (feed) — homeowner valuation
def ad_feed(fn,photo,name,copy,headline,cta,foc=0.5):
    W=760;tb=66;ih=560;bh=210;H=tb+ih+bh
    c=Image.new("RGB",(W,H),(255,255,255));d=ImageDraw.Draw(c,"RGBA")
    d.ellipse((14,12,54,52),fill=DARK);d.text((20,22),"RE",font=F(15),fill=CYANc)
    d.text((64,16),name,font=F(19),fill=(20,20,20));d.text((64,40),"Sponsored",font=F(14,False),fill=(120,120,120))
    ph=load(photo,(W,ih),foc);pd=ImageDraw.Draw(ph,"RGBA")
    # headline band
    pd.rectangle((0,ih-150,W,ih),fill=(14,27,42,210))
    yy=ih-135
    for ln in wrap(pd,headline,F(38),W-60)[:3]:
        pd.text((28,yy),ln,font=F(38),fill=(255,255,255));yy+=46
    c.paste(ph,(0,tb))
    by=tb+ih
    d.text((18,by+10),"♥   \U0001F4AC   ➤",font=F(22),fill=(40,40,40)) if False else d.text((18,by+12),"Like   Comment   Share",font=F(15,False),fill=(90,90,90))
    yy=by+44
    for ln in wrap(d,copy,F(18,False),W-150)[:3]:
        d.text((18,yy),ln,font=F(18,False),fill=(30,30,30));yy+=24
    d.rounded_rectangle((W-230,by+150,W-18,by+200),10,fill=(242,178,62))
    d.text((W-214,by+165),cta,font=F(18),fill=(20,20,20))
    c.save(f"{OUT}/{fn}",quality=90);print("creative",fn)

# Landing mockup — What's your home worth
def landing(fn,photo,foc=0.45):
    W,H=820,560
    img=load(photo,(W,H),foc);img=grad(img,30,150)
    d=ImageDraw.Draw(img,"RGBA")
    # top bar
    d.rectangle((0,0,W,54),fill=(14,27,42,235));d.ellipse((16,14,44,42),fill=CYANc);d.text((22,18),"RE",font=F(14),fill=DARK)
    d.text((54,18),"AI Listings",font=F(18),fill=CREAMc)
    yy=120
    for ln in wrap(d,"What's Your Home Worth in 2026?",F(46),W-120):
        d.text((60,yy),ln,font=F(46),fill=(255,255,255));yy+=54
    d.text((60,yy+6),"Get a free, instant AI valuation — no phone call needed.",font=F(20,False),fill=CREAMc)
    # form
    fy=yy+60
    d.rounded_rectangle((60,fy,560,fy+52),8,fill=(255,255,255));d.text((78,fy+15),"Enter your home address…",font=F(19,False),fill=(120,120,120))
    d.rounded_rectangle((580,fy,780,fy+52),8,fill=(242,178,62));d.text((600,fy+14),"Get my value →",font=F(19),fill=(20,20,20))
    d.text((60,fy+70),"\U0001F512 100% free · takes 30 seconds · 1,200+ homeowners this month",font=F(15,False),fill=CREAMc)
    img.save(f"{OUT}/{fn}",quality=90);print("creative",fn)

ad_feed("CR_ad_feed.jpg","house.jpg","RE · AI Listings",
        "Thinking of selling? See what your home is worth in 30 seconds — free, no calls.",
        "What's your home worth in 2026?","Learn more",foc=0.55)
ad_feed("CR_ad_feed2.jpg","house2.jpg","RE · AI Listings",
        "Homeowners in your area are getting instant AI valuations. Curious about yours?",
        "Free instant home valuation","Get my value",foc=0.5)
landing("CR_landing.jpg","luxo.jpg",foc=0.5)
print("DONE_AI_ASSETS")

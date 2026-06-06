#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera mockups de criativos de anúncio (exemplos) para o playbook de mídia."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os, textwrap

IMG="/tmp/apostila/img"; OUT="/tmp/apostila/creatives"; os.makedirs(OUT, exist_ok=True)
FD="/usr/local/lib/python3.11/dist-packages/matplotlib/mpl-data/fonts/ttf"
def F(sz,bold=True,obl=False):
    name="DejaVuSans-Bold.ttf" if bold else ("DejaVuSans-Oblique.ttf" if obl else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FD,name),sz)

GOLD=(224,184,76); GOLD2=(240,203,110); DARK=(20,17,14); CREAM=(244,238,226)
GREEN=(37,211,102); WA=(37,211,102); BLUE=(26,115,232); GREY=(110,110,110)

def load_cover(name, size, focus=0.5):
    im=Image.open(f"{IMG}/{name}").convert("RGB")
    return ImageOps.fit(im, size, method=Image.LANCZOS, centering=(0.5,focus))

def grad_overlay(img, top_a=0, bot_a=210, color=(0,0,0)):
    w,h=img.size; ov=Image.new("L",(1,h),0)
    for y in range(h):
        t=y/h; a=int(top_a+(bot_a-top_a)*(t**1.4))
        ov.putpixel((0,y),a)
    ov=ov.resize((w,h)); shade=Image.new("RGB",(w,h),color)
    return Image.composite(shade,img,ov)

def rounded(draw, xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def wrap(draw, text, font, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def label(img, txt):
    """add a small caption banner on top to identify the mockup type."""
    return img

# ---------------------------------------------------------------
# STORY / REELS vertical 9:16
# ---------------------------------------------------------------
def story(fname, photo, badge, headline, price, sub, cta, handle, focus=0.5, accent=GOLD):
    W,H=720,1280
    img=load_cover(photo,(W,H),focus)
    img=grad_overlay(img, 60, 30, (0,0,0))            # slight top
    img=grad_overlay(img, 0, 220, (0,0,0))            # heavy bottom
    d=ImageDraw.Draw(img,"RGBA")
    # top profile bar
    d.ellipse((24,30,84,90),fill=(0,0,0,0),outline=accent,width=3)
    d.ellipse((30,36,78,84),fill=accent)
    d.text((45,46),"AQV",font=F(20),fill=DARK)
    d.text((98,38),handle,font=F(24),fill=CREAM)
    d.text((98,68),"Patrocinado",font=F(18,bold=False),fill=(220,220,220))
    # badge top-right
    bw=d.textlength(badge,font=F(20));
    rounded(d,(W-bw-60,38,W-24,80),18,fill=(accent[0],accent[1],accent[2],235))
    d.text((W-bw-44,46),badge,font=F(20),fill=DARK)
    # headline block bottom
    y=H-430
    for ln in wrap(d,headline,F(46),W-90):
        d.text((45,y),ln,font=F(46),fill=CREAM); y+=56
    # price chip
    y+=8
    pw=d.textlength(price,font=F(40))
    rounded(d,(45,y,45+pw+44,y+62),14,fill=(accent[0],accent[1],accent[2],255))
    d.text((67,y+12),price,font=F(40),fill=DARK);
    d.text((45+pw+70,y+16),sub,font=F(24,bold=False),fill=CREAM)
    y+=92
    # CTA bar (whatsapp)
    rounded(d,(45,y,W-45,y+74),16,fill=WA)
    d.text((78,y+22),"➜  "+cta,font=F(30),fill=(255,255,255))
    img.save(f"{OUT}/{fname}",quality=90); print("story",fname)

# ---------------------------------------------------------------
# FEED square 1:1  (Instagram/Facebook feed)
# ---------------------------------------------------------------
def feed(fname, photo, name, copy, headline, sub, cta, focus=0.5, tag="Patrocinado", accent=GOLD):
    W=760; topbar=70; imgH=560; botH=230; H=topbar+imgH+botH
    canvas=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(canvas,"RGBA")
    # top bar
    d.ellipse((14,14,56,56),fill=accent); d.text((24,24),"AQV",font=F(16),fill=DARK)
    d.text((68,16),name,font=F(20),fill=(20,20,20))
    d.text((68,40),tag,font=F(15,bold=False),fill=GREY)
    d.text((W-40,20),"⋯",font=F(26),fill=(60,60,60))
    # photo
    ph=load_cover(photo,(W,imgH),focus);
    # price tag overlay on photo
    pd=ImageDraw.Draw(ph,"RGBA")
    th=headline
    rounded(pd,(20,imgH-70,20+pd.textlength(th,font=F(34))+40,imgH-12),12,fill=(accent[0],accent[1],accent[2],240))
    pd.text((40,imgH-62),th,font=F(34),fill=DARK)
    canvas.paste(ph,(0,topbar))
    # bottom: action row + copy + CTA
    by=topbar+imgH
    d.text((18,by+12),"♥   💬   ➤",font=F(24),fill=(40,40,40))
    yy=by+52
    for ln in wrap(d,copy,F(19,bold=False),W-140)[:2]:
        d.text((18,yy),ln,font=F(19,bold=False),fill=(30,30,30)); yy+=26
    # CTA button
    rounded(d,(W-220,by+150,W-18,by+205),10,fill=WA)
    d.text((W-205,by+165),cta,font=F(20),fill=(255,255,255))
    d.text((18,by+170),sub,font=F(16,bold=False),fill=GREY)
    canvas.save(f"{OUT}/{fname}",quality=90); print("feed",fname)

# ---------------------------------------------------------------
# GOOGLE SEARCH SERP
# ---------------------------------------------------------------
def serp(fname, query, ads):
    W=820; H=120+len(ads)*215
    c=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(c)
    # search bar
    rounded(d,(20,24,W-20,76),26,outline=(220,220,220),width=2)
    d.text((44,38),query,font=F(22,bold=False),fill=(40,40,40))
    d.ellipse((W-66,38,W-90+24,38+24),fill=(66,133,244))
    y=104
    for (title,url,desc,sl) in ads:
        d.text((24,y),"Patrocinado",font=F(15),fill=(32,33,36))
        d.text((150,y),"· "+url,font=F(15,bold=False),fill=(32,120,40))
        y+=30
        for ln in wrap(d,title,F(24),W-60)[:2]:
            d.text((24,y),ln,font=F(24),fill=(26,13,171)); y+=30
        for ln in wrap(d,desc,F(17,bold=False),W-60)[:2]:
            d.text((24,y),ln,font=F(17,bold=False),fill=(70,70,70)); y+=24
        # sitelinks
        sx=24
        for s in sl:
            d.text((sx,y),s,font=F(16),fill=(26,13,171)); sx+=d.textlength(s,font=F(16))+34
        y+=58
    c.save(f"{OUT}/{fname}",quality=92); print("serp",fname)

# ---------------------------------------------------------------
# YOUTUBE in-stream
# ---------------------------------------------------------------
def youtube(fname, photo, headline, cta, focus=0.5):
    W,H=820,470
    img=load_cover(photo,(W,H),focus); img=grad_overlay(img,40,140,(0,0,0))
    d=ImageDraw.Draw(img,"RGBA")
    # ad marker
    rounded(d,(20,20,80,48),5,fill=(255,255,0)); d.text((30,24),"Anúncio",font=F(16),fill=(0,0,0))
    # skip button
    rounded(d,(W-185,H-70,W-20,H-22),4,fill=(0,0,0,160),outline=(255,255,255),width=2)
    d.text((W-170,H-60),"Pular anúncio ▷|",font=F(18),fill=(255,255,255))
    # bottom-left CTA companion
    rounded(d,(20,H-150,360,H-86),8,fill=(255,255,255,235))
    d.text((34,H-140),headline[:34],font=F(20),fill=(20,20,20))
    rounded(d,(34,H-104,200,H-92),6,fill=WA)
    d.text((40,H-108),cta,font=F(15),fill=(255,255,255))
    # play bar
    d.rectangle((0,H-10,int(W*0.25),H-6),fill=(255,0,0))
    img.save(f"{OUT}/{fname}",quality=90); print("yt",fname)

# ---------------------------------------------------------------
# LEAD FORM (instant form) phone
# ---------------------------------------------------------------
def leadform(fname, photo, title, fields, cta, focus=0.5, accent=GOLD):
    W,H=620,1100
    c=Image.new("RGB",(W,H),(245,246,248)); d=ImageDraw.Draw(c,"RGBA")
    hero=load_cover(photo,(W,300),focus); c.paste(hero,(0,0))
    rounded(d,(0,0,W,300),0,fill=None)
    d.rectangle((0,260,W,300),fill=(245,246,248)) if False else None
    # card
    rounded(d,(30,250,W-30,H-30),22,fill=(255,255,255),outline=(225,225,225),width=2)
    yy=285
    for ln in wrap(d,title,F(30),W-100):
        d.text((55,yy),ln,font=F(30),fill=(25,25,25)); yy+=40
    yy+=10
    for lab in fields:
        d.text((55,yy),lab,font=F(20,bold=False),fill=(90,90,90)); yy+=30
        rounded(d,(55,yy,W-55,yy+50),10,fill=(247,247,247),outline=(215,215,215),width=2); yy+=72
    yy+=6
    rounded(d,(55,yy,W-55,yy+64),12,fill=WA)
    d.text((90,yy+18),cta,font=F(24),fill=(255,255,255))
    d.text((55,yy+86),"🔒 Suas informações são tratadas com segurança.",font=F(15,bold=False),fill=(140,140,140))
    c.save(f"{OUT}/{fname}",quality=92); print("leadform",fname)

# ---------------------------------------------------------------
# CAROUSEL 3 cards (retargeting prova)
# ---------------------------------------------------------------
def carousel(fname, cards):
    cw,ch=300,300; gap=20; W=3*cw+4*gap; H=ch+90
    c=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(c,"RGBA")
    d.text((gap,16),"Carrossel · deslize  ▶",font=F(22),fill=(40,40,40))
    x=gap
    for (photo,cap,foc,accent) in cards:
        card=load_cover(photo,(cw,ch),foc); card=grad_overlay(card,20,170,(0,0,0))
        cd=ImageDraw.Draw(card,"RGBA")
        yy=ch-78
        for ln in wrap(cd,cap,F(22),cw-30)[:3]:
            cd.text((16,yy),ln,font=F(22),fill=CREAM); yy+=26
        c.paste(card,(x,60)); x+=cw+gap
    c.save(f"{OUT}/{fname}",quality=90); print("carousel",fname)

# ---------------------------------------------------------------
# TIKTOK vertical
# ---------------------------------------------------------------
def tiktok(fname, photo, headline, price, cta, handle, focus=0.5):
    W,H=720,1280; img=load_cover(photo,(W,H),focus); img=grad_overlay(img,30,160,(0,0,0))
    d=ImageDraw.Draw(img,"RGBA")
    # right side icons
    for i,ic in enumerate(["♥","💬","➤","♫"]):
        cy=560+i*150; d.ellipse((W-86,cy,W-26,cy+60),fill=(255,255,255,40)); d.text((W-74,cy+12),ic,font=F(30),fill=CREAM)
    # bottom text
    d.text((28,H-300),"@"+handle,font=F(28),fill=CREAM)
    yy=H-258
    for ln in wrap(d,headline,F(34),W-160)[:3]:
        d.text((28,yy),ln,font=F(34),fill=CREAM); yy+=42
    pw=d.textlength(price,font=F(32)); rounded(d,(28,yy+6,28+pw+34,yy+58),12,fill=GOLD)
    d.text((45,yy+14),price,font=F(32),fill=DARK)
    # sponsored CTA bar
    rounded(d,(28,H-86,W-28,H-26),10,fill=(255,255,255,235))
    d.text((50,H-74),"➜  "+cta,font=F(26),fill=(20,20,20))
    d.rectangle((0,0,W,46),fill=(0,0,0,90)); d.text((20,10),"Patrocinado · TikTok",font=F(20),fill=CREAM)
    img.save(f"{OUT}/{fname}",quality=90); print("tiktok",fname)

# ================= GERAR TODOS =================
# 1. Meta Reels frio - walkthrough
story("cr01_meta_reels.jpg","frente_mar.jpg","FRENTE-MAR",
      "Cobertura frente-mar, pronta para morar",
      "R$ 1,2 mi","· 3 suítes · 2 vagas","FALAR NO WHATSAPP","imoveis.aqv", focus=0.4)
# 2. Meta Feed oportunidade preço
feed("cr02_meta_feed.jpg","interior.jpg","Imóveis AQV",
     "2 quartos no [Bairro], pronto pra morar. Financia pela Caixa e usa o FGTS na entrada.",
     "R$ 389.000 · 68m²","Saiba a condição","CHAMAR", focus=0.5)
# 3. Lead form MCMV
leadform("cr03_leadform.jpg","mcmv.jpg","Saia do aluguel: simule seu financiamento",
     ["Seu nome","WhatsApp","Renda familiar aproximada","Já tem FGTS? (8+ anos de carteira)"],
     "QUERO SIMULAR", focus=0.45)
# 4. Google Search
serp("cr04_google_search.jpg","apartamento 2 quartos maceió financiamento",
     [("Apartamento 2 Quartos em Maceió | A partir de R$ 389 mil",
       "imoveis-aqv.com.br/maceio",
       "Pronto pra morar, financia pela Caixa e usa FGTS. Fale agora no WhatsApp e agende sua visita.",
       ["Ver unidades","Simular financiamento","Falar no WhatsApp"]),
      ("Imóveis Frente-Mar em Maceió | Visita no Mesmo Dia",
       "imoveis-aqv.com.br/frente-mar",
       "Seleção de apartamentos com vista mar. Atendimento rápido, sem burocracia.",
       ["Alto padrão","Investimento"])])
# 5. YouTube retargeting
youtube("cr05_youtube.jpg","luxo.jpg","Ainda pensando no apê? Veja por dentro","Ver agora", focus=0.5)
# 6. Carousel retargeting prova
carousel("cr06_carrossel.jpg",[
    ("chaves.jpg","“Comprei sem nunca ter visto o corretor antes.”",0.5,GOLD),
    ("cozinha.jpg","Financiou pela Caixa em 5 dias",0.5,GOLD),
    ("varanda.jpg","Visita no mesmo dia do anúncio",0.5,GOLD)])
# 7. TikTok MCMV jovem
tiktok("cr07_tiktok.jpg","casal.jpg","Saiu do aluguel aos 26. Olha o apê novo 👀",
       "Entrada facilitada","Ver como","imoveis.aqv", focus=0.4)
# 8. BOFU urgência (story)
story("cr08_bofu_urgencia.jpg","piscina.jpg","ÚLTIMAS UNIDADES",
      "Condição especial termina sexta",
      "12% OFF","na entrada","QUERO GARANTIR","imoveis.aqv", focus=0.5, accent=(197,82,74))
# 9. Lookalike escala (feed)
feed("cr09_lookalike.jpg","cidade.jpg","Imóveis AQV",
     "Quem comprou com a gente tinha esse perfil. Será que é o seu momento também?",
     "Simulação grátis","Descubra em 2 min","SIMULAR", focus=0.4, accent=GOLD)
# 10. Investidor (feed)
feed("cr10_investidor.jpg","praia_apt.jpg","Imóveis AQV",
     "Studio frente-mar para renda de temporada. O aluguel paga a parcela.",
     "ROI estimado 0,9%/mês","Receba o estudo","QUERO O ESTUDO", focus=0.4)
print("DONE_CREATIVES")

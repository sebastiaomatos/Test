#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera tiras de storyboard (frames 9:16 com timecode e texto na tela)."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
SRC="/tmp/apostila/img"; OUT="/home/user/Test/03-storyboards/img"; os.makedirs(OUT,exist_ok=True)
FD="/usr/local/lib/python3.11/dist-packages/matplotlib/mpl-data/fonts/ttf"
def F(sz,bold=True): return ImageFont.truetype(os.path.join(FD,"DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),sz)
GOLD=(224,184,76); DARK=(20,17,14); CREAM=(244,238,226); WA=(37,211,102); BAD=(197,82,74)

def fit(name,size,foc=0.5):
    im=Image.open(f"{SRC}/{name}").convert("RGB")
    return ImageOps.fit(im,size,Image.LANCZOS,centering=(0.5,foc))
def grad(img,a0=20,a1=180):
    w,h=img.size; ov=Image.new("L",(1,h),0)
    for y in range(h): ov.putpixel((0,y),int(a0+(a1-a0)*(y/h)**1.4))
    return Image.composite(Image.new("RGB",(w,h),(0,0,0)),img,ov.resize((w,h)))
def wrap(d,txt,f,mw):
    out=[];cur=""
    for w in txt.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=mw:cur=t
        else:out.append(cur);cur=w
    if cur:out.append(cur)
    return out

FW,FH=300,533  # frame 9:16
def frame(photo, tc, ostext, foc=0.5, card=None, accent=GOLD):
    if card is None:
        img=grad(fit(photo,(FW,FH),foc))
    else:
        img=Image.new("RGB",(FW,FH),DARK)
    d=ImageDraw.Draw(img,"RGBA")
    # timecode chip
    d.rounded_rectangle((10,10,10+d.textlength(tc,font=F(18))+20,42),8,fill=(0,0,0,170))
    d.text((20,15),tc,font=F(18),fill=GOLD)
    if card:
        # centered card text
        title,sub=card
        y=FH//2-60
        for ln in wrap(d,title,F(30),FW-50):
            d.text((25,y),ln,font=F(30),fill=accent); y+=38
        if sub:
            y+=8
            for ln in wrap(d,sub,F(20,False),FW-50):
                d.text((25,y),ln,font=F(20,False),fill=CREAM); y+=26
    if ostext:
        # on-screen text bottom
        y=FH-110
        for ln in wrap(d,ostext,F(24),FW-30)[:3]:
            d.text((16,y),ln,font=F(24),fill=CREAM); y+=30
    return img

def strip(fname, title, frames, accent=GOLD):
    pad=18; cap_h=72; lblw=FW
    n=len(frames); W=pad+n*(FW+pad); H=70+FH+cap_h+pad
    c=Image.new("RGB",(W,H),(26,23,19)); d=ImageDraw.Draw(c,"RGBA")
    d.text((pad,20),title,font=F(30),fill=accent)
    x=pad
    for (img, cap) in frames:
        c.paste(img,(x,70))
        # arrow between
        if x>pad: d.text((x-15,70+FH//2-12),"›",font=F(34),fill=GOLD)
        # caption under
        yy=70+FH+8
        for ln in wrap(d,cap,F(16,False),FW-6)[:3]:
            d.text((x+2,yy),ln,font=F(16,False),fill=CREAM); yy+=20
        x+=FW+pad
    c.save(f"{OUT}/{fname}",quality=90); print("strip",fname,c.size)

# ---------- FORMATO 1 — WALKTHROUGH ----------
f1=[
 (frame("hero_predio.jpg","0–3s","Apê 2 quartos no [Bairro]",0.4), "Cena 1 · Fachada/entrada. Texto identifica o imóvel já no 1º frame (filtro)."),
 (frame("interior.jpg","3–9s","68m² · sala integrada",0.5), "Cena 2 · Caminhada pela sala. Luz natural, plano estável."),
 (frame("cozinha.jpg","9–15s","Cozinha c/ armários planejados",0.5), "Cena 3 · Cozinha. Mostra acabamento, sem narração de adjetivos."),
 (frame("quarto.jpg","15–21s","2 quartos · suíte",0.5), "Cena 4 · Quartos/suíte. Sequência de visita real."),
 (frame("varanda.jpg","21–27s","Varanda + vista livre",0.4), "Cena 5 · Varanda e vista. Diferencial emocional."),
 (frame("piscina.jpg","27–33s","Piscina · academia · salão",0.5), "Cena 6 · Lazer do condomínio."),
 (frame(None,"33–40s",None,card=("R$ 389.000","Financia + usa FGTS · Chama no WhatsApp")), "Cena 7 · Card final: preço + condição + CTA. Botão WhatsApp."),
]
strip("sb1_walkthrough.png","FORMATO 1 · TOUR OBJETIVO (WALKTHROUGH) — 40s · 9:16", f1)

# ---------- FORMATO 2 — OPORTUNIDADE DE PREÇO ----------
f2=[
 (frame(None,"0–3s",None,card=("R$ 389.000","abaixo da tabela do bairro")), "Cena 1 · Abre com o NÚMERO. O preço é o gancho que filtra."),
 (frame("interior.jpg","3–8s","68m² · pronto pra morar",0.5), "Cena 2 · Tour rápido da sala (corte ágil)."),
 (frame("cozinha.jpg","8–13s","2 quartos · 1 vaga",0.5), "Cena 3 · Cozinha + quarto em cortes rápidos."),
 (frame(None,"13–18s",None,card=("Financia pela Caixa","Usa o FGTS na entrada")), "Cena 4 · Condição comercial na tela."),
 (frame("varanda.jpg","18–24s","Últimas unidades",0.4,accent=BAD), "Cena 5 · CTA com urgência real + botão WhatsApp."),
]
strip("sb2_preco.png","FORMATO 2 · OPORTUNIDADE DE PREÇO — 24s · 9:16", f2, accent=GOLD)

# ---------- FORMATO 3 — RECORTE POR MOTIVAÇÃO ----------
f3=[
 (frame("casal.jpg","0–4s","Cansado de pagar aluguel?",0.4,accent=GOLD), "Cena 1 · Gancho na DOR do ICP (sair do aluguel)."),
 (frame("interior.jpg","4–9s","Esse apê resolve isso",0.5), "Cena 2 · Promessa + sala."),
 (frame("quarto.jpg","9–15s","2 quartos pra família crescer",0.5), "Cena 3 · Conecta recurso à motivação."),
 (frame(None,"15–21s",None,card=("Parcela ≈ seu aluguel","simulação na descrição")), "Cena 4 · Quebra de objeção preço (comparativo)."),
 (frame("chaves.jpg","21–27s","Financiou em 5 dias",0.5), "Cena 5 · Prova social rápida."),
 (frame(None,"27–32s",None,card=("Quero sair do aluguel","Chama no WhatsApp"),accent=WA), "Cena 6 · CTA emocional + botão WhatsApp."),
]
strip("sb3_motivacao.png","FORMATO 3 · RECORTE POR MOTIVAÇÃO (ICP) — 32s · 9:16", f3, accent=GOLD)
print("DONE_STORYBOARDS")

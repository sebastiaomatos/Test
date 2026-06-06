#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta o PDF de apresentação das landing pages (capa + desktop fatiado + mobile filmstrip)."""
import os, math
from PIL import Image
from weasyprint import HTML
BASE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.join(BASE,"..")
SHOT=os.path.join(ROOT,"shots")
SL=os.path.join(SHOT,"slices"); os.makedirs(SL,exist_ok=True)

PROPS=[
 dict(slug="apartamento-jardim-italia", nome="Residencial Cuiabá Park",
      sub="Apartamento 3 quartos · 78m² · Jardim Itália, Cuiabá/MT", preco="R$ 539.000", cod="AP-1042"),
 dict(slug="apartamento-pedra-90", nome="Residencial Bem Viver",
      sub="Apartamento 2 quartos (MCMV) · 48m² · Pedra 90, Cuiabá/MT", preco="R$ 219.000", cod="AP-2087"),
]

CONTENT_ASPECT = 271/184   # A4 portrait content area (h/w) with ~13mm margins
def slice_desktop(slug):
    im=Image.open(os.path.join(SHOT,f"{slug}_desktop.png")).convert("RGB")
    W,H=im.size; strip=int(round(W*CONTENT_ASPECT)); n=math.ceil(H/strip); out=[]
    for i in range(n):
        y0=i*strip; y1=min(H,y0+strip)
        p=os.path.join(SL,f"{slug}_d{i}.png"); im.crop((0,y0,W,y1)).save(p); out.append((os.path.relpath(p,ROOT),y1-y0,W))
    return out
def slice_mobile(slug,parts=5):
    im=Image.open(os.path.join(SHOT,f"{slug}_mobile.png")).convert("RGB")
    W,H=im.size; step=math.ceil(H/parts); out=[]
    for i in range(parts):
        y0=i*step; y1=min(H,y0+step)
        if y0>=H: break
        p=os.path.join(SL,f"{slug}_m{i}.png"); im.crop((0,y0,W,y1)).save(p); out.append(os.path.relpath(p,ROOT))
    return out

GREEN="#004310"; ORANGE="#F57F17"
CSS=f"""
@page{{size:A4; margin:12mm 13mm 14mm;
  @bottom-center{{content:"Landing pages · Aprovar Negócios Imobiliários · Cuiabá/MT"; font-family:Arial; font-size:7.5pt; color:#8fae97;}}
  @bottom-right{{content:counter(page); font-family:Arial; font-size:8.5pt; color:{ORANGE};}}}}
@page cover{{margin:0; @bottom-center{{content:""}} @bottom-right{{content:""}}}}
@page land{{size:A4 landscape; margin:12mm;
  @bottom-center{{content:"Versão mobile (responsiva) · Aprovar"; font-family:Arial; font-size:7.5pt; color:#8fae97;}}}}
*{{box-sizing:border-box;margin:0;padding:0}} html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'Helvetica Neue',Arial,sans-serif;color:#1f2a24}}
.cover{{page:cover;height:297mm;background:{GREEN};color:#fff;padding:34mm 26mm;position:relative;page-break-after:always}}
.cover::before{{content:"";position:absolute;left:0;top:0;width:100%;height:14px;background:{ORANGE}}}
.cover img.logo{{height:64px;margin-bottom:30mm}}
.cover .kick{{color:{ORANGE};font-weight:800;letter-spacing:3px;text-transform:uppercase;font-size:11pt}}
.cover h1{{font-size:38pt;font-weight:800;line-height:1.08;margin:8mm 0 6mm}}
.cover h1 span{{color:{ORANGE}}}
.cover p{{color:#cfe6d6;font-size:13pt;max-width:150mm;line-height:1.6}}
.cover .meta{{position:absolute;bottom:30mm;left:26mm;border-left:3px solid {ORANGE};padding-left:6mm;color:#dfeee2;font-size:10.5pt;line-height:1.8}}
.cover img.round{{position:absolute;bottom:28mm;right:26mm;width:90px;border-radius:50%}}

.sec{{page-break-before:always}}
h2.t{{color:{GREEN};font-size:18pt;font-weight:800;margin-bottom:1mm}}
.kick{{color:{ORANGE};font-weight:800;letter-spacing:2px;text-transform:uppercase;font-size:8.5pt}}
.divider{{page-break-before:always;background:{GREEN};color:#fff;border-radius:14px;padding:9mm 11mm;margin-bottom:6mm}}
.divider .kick{{color:{ORANGE}}}
.divider h2{{font-size:21pt;font-weight:800;margin:2mm 0}}
.divider p{{color:#cfe6d6;font-size:10.5pt}}
.divider .price{{display:inline-block;background:{ORANGE};color:#fff;font-weight:800;padding:5px 14px;border-radius:999px;margin-top:3mm;font-size:11pt}}

.slice{{page-break-before:always;text-align:center}}
.slice img{{width:100%;border:1px solid #e0ddd2}}
.slice.first{{page-break-before:auto}}

.land{{page:land;page-break-before:always}}
.filmrow{{display:flex;gap:6mm;justify-content:center;align-items:flex-start}}
.phone{{background:#0c1015;border-radius:18px;padding:8px 6px 10px;box-shadow:0 8px 20px rgba(0,0,0,.25)}}
.phone .scr{{width:46mm;border-radius:8px;overflow:hidden;display:block}}
.phone .scr img{{width:100%;display:block}}
.landhead{{margin-bottom:5mm}}

table.spec{{width:100%;border-collapse:collapse;font-size:9pt;margin-top:3mm}}
table.spec th{{background:{GREEN};color:#fff;text-align:left;padding:2mm 3mm}}
table.spec td{{padding:2mm 3mm;border-bottom:1px solid #e7ddc7}}
table.spec tr:nth-child(even) td{{background:#f7f5ee}}
.sw{{display:inline-block;width:42mm;border-radius:8px;overflow:hidden;border:1px solid #e0ddd2;margin:2mm 2mm 0 0;vertical-align:top}}
.sw .c{{height:20mm}} .sw .l{{padding:2mm 3mm;font-size:8pt}} .sw .l b{{display:block;color:{GREEN}}}
.note{{background:#f7f5ee;border-left:4px solid {ORANGE};border-radius:0 8px 8px 0;padding:3mm 4mm;font-size:9pt;margin-top:4mm}}
"""

H=['<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><style>'+CSS+'</style></head><body>']
# COVER
H.append(f'''<div class="cover">
  <img class="logo" src="landing/assets/logo-aprovar-branco.png">
  <div class="kick">Landing pages prontas para campanha</div>
  <h1>Imóveis em <span>Cuiabá</span><br>landing pages de <span>alta conversão</span></h1>
  <p>Duas páginas de captação 100% prontas, com a identidade da Aprovar Negócios Imobiliários — para anúncios de Meta e Google que viram conversa no WhatsApp.</p>
  <div class="meta">Residencial Cuiabá Park · Jardim Itália<br>Residencial Bem Viver · Pedra 90 (MCMV)<br>
  <span style="color:{ORANGE}">CRECI 9770J · (65) 99232-6461</span></div>
  <img class="round" src="landing/assets/logo-aprovar-redondo.png">
</div>''')

# BRAND + FICHA
H.append(f'''<div class="sec"><span class="kick">Identidade & especificações</span>
  <h2 class="t">Branding aplicado e ficha dos imóveis</h2>
  <p style="color:#5a655d;font-size:10pt;margin-top:1mm">Cores, logo e tom extraídos de imobiliariaaprovar.com.br e aplicados nas duas landing pages.</p>
  <div style="margin-top:4mm">
   <div class="sw"><div class="c" style="background:{ORANGE}"></div><div class="l"><b>Laranja Aprovar</b>#F57F17 · CTA, destaques</div></div>
   <div class="sw"><div class="c" style="background:{GREEN}"></div><div class="l"><b>Verde-floresta</b>#004310 · topo, rodapé</div></div>
   <div class="sw"><div class="c" style="background:#25D366"></div><div class="l"><b>Verde WhatsApp</b>#25D366 · conversão</div></div>
   <div class="sw"><div class="c" style="background:#f7f5ee;border-bottom:1px solid #e0ddd2"></div><div class="l"><b>Areia / claro</b>#F7F5EE · seções</div></div>
  </div>
  <table class="spec">
   <tr><th>Imóvel</th><th>Tipo</th><th>Bairro</th><th>Área</th><th>Preço</th><th>Cód.</th></tr>
   <tr><td>Residencial Cuiabá Park</td><td>Apto 3q (1 suíte), 2 vagas</td><td>Jardim Itália</td><td>78 m²</td><td>R$ 539.000</td><td>AP-1042</td></tr>
   <tr><td>Residencial Bem Viver</td><td>Apto 2q, 1 vaga (MCMV)</td><td>Pedra 90</td><td>48 m²</td><td>R$ 219.000</td><td>AP-2087</td></tr>
  </table>
  <div class="note"><b>Imóveis fictícios, dados realistas para Cuiabá/MT.</b> Telefone, endereço e CRECI são os públicos da Aprovar. As páginas estão prontas em <code>07-landing-aprovar/landing/</code> (HTML/CSS/JS) — basta publicar e trocar as fotos pelas reais do imóvel.</div>
</div>''')

# PER PROPERTY
for P in PROPS:
    H.append(f'''<div class="divider"><span class="kick">Landing page · {P['cod']}</span>
      <h2>{P['nome']}</h2><p>{P['sub']}</p><div class="price">{P['preco']}</div>
      &nbsp;<span style="font-size:9pt;color:#cfe6d6">— a seguir: versão desktop (rolagem) e versão mobile</span></div>''')
    dslices=slice_desktop(P["slug"])
    for i,(rp,h,w) in enumerate(dslices):
        cls="slice first" if i==0 else "slice"
        H.append(f'<div class="{cls}"><img src="{rp}"></div>')
    # mobile filmstrip
    msl=slice_mobile(P["slug"],5)
    phones="".join(f'<div class="phone"><div class="scr"><img src="{rp}"></div></div>' for rp in msl)
    H.append(f'''<div class="land"><div class="landhead"><span class="kick">{P['cod']} · responsivo</span>
      <h2 class="t">{P['nome']} — versão mobile</h2></div>
      <div class="filmrow">{phones}</div></div>''')

H.append('</body></html>')
htmlpath=os.path.join(BASE,"_apresentacao.html")
open(htmlpath,"w",encoding="utf-8").write("\n".join(H))
out=os.path.join(ROOT,"Landing-Pages-Aprovar-Cuiaba.pdf")
HTML(htmlpath, base_url=ROOT).write_pdf(out)
import fitz; print("PDF:",out,"·",fitz.open(out).page_count,"páginas")

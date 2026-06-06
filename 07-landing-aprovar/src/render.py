#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renderiza as landings como screenshots de página inteira (desktop + mobile)."""
import os, fitz
from weasyprint import HTML, CSS
from PIL import Image
BASE=os.path.dirname(os.path.abspath(__file__))
LAND=os.path.join(BASE,"..","landing")
SHOT=os.path.join(BASE,"..","shots"); os.makedirs(SHOT,exist_ok=True)

def trim_bottom(png, bg_thresh=246, pad=24):
    im=Image.open(png).convert("RGB"); w,h=im.size; px=im.load()
    last=h-1
    for y in range(h-1,-1,-1):
        blank=True
        for x in range(0,w,9):
            r,g,b=px[x,y]
            if r<bg_thresh or g<bg_thresh or b<bg_thresh: blank=False; break
        if not blank: last=y; break
    im.crop((0,0,w,min(h,last+pad))).save(png)
    return last+pad

def shot(slug, width_px, dpi, tag, h_start=12000, h_max=60000):
    out=os.path.join(SHOT,f"{slug}_{tag}.png")
    h=h_start
    while True:
        css=CSS(string=f"@page{{size:{width_px}px {h}px;margin:0}} .wa-float{{display:none!important}} .top{{position:static!important}} html,body{{background:#fff}}")
        pdf=os.path.join(SHOT,f"_{slug}_{tag}.pdf")
        HTML(os.path.join(LAND,slug+".html"), base_url=LAND).write_pdf(pdf, stylesheets=[css])
        d=fitz.open(pdf); pc=d.page_count
        if pc==1 or h>=h_max:
            zoom=dpi/72.0
            d[0].get_pixmap(matrix=fitz.Matrix(zoom,zoom)).save(out)
            d.close(); os.remove(pdf); break
        d.close(); os.remove(pdf); h=int(h*1.6)
    finalh=trim_bottom(out)
    print(f"  {tag}: page_h_css={h} -> {Image.open(out).size} (pages={pc})")
    return out

for slug in ["apartamento-jardim-italia","apartamento-pedra-90"]:
    print(slug)
    shot(slug, 1280, 110, "desktop")
    shot(slug, 414, 150, "mobile")
print("DONE_SHOTS")

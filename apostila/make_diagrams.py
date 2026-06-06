#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm
import numpy as np
import os

OUT="/tmp/apostila/img"
os.makedirs(OUT, exist_ok=True)

# ---- Brand palette ----
BG     = "#14110E"   # near-black warm
PANEL  = "#1d1915"
GOLD   = "#D8A84B"
GOLD2  = "#F0CB6E"
CREAM  = "#F4EEE2"
MUTE   = "#9c9286"
GOOD   = "#4CB286"
BAD    = "#C5524A"
BLUE   = "#5B8DB8"

plt.rcParams.update({
    "font.family":"DejaVu Sans",
    "font.size":13,
    "text.color":CREAM,
    "axes.edgecolor":"none",
})

def fig(w,h):
    f=plt.figure(figsize=(w,h), dpi=170)
    ax=f.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(0,100)
    ax.axis("off"); f.patch.set_facecolor(BG); ax.set_facecolor(BG)
    return f,ax

def box(ax,x,y,w,h,fc=PANEL,ec=GOLD,lw=1.8,rad=2.5,alpha=1):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.2,rounding_size={rad}",
                     fc=fc,ec=ec,lw=lw,alpha=alpha,mutation_aspect=1)
    ax.add_patch(p); return p

def txt(ax,x,y,s,size=13,color=CREAM,weight="normal",ha="center",va="center",style="normal",wrap=True):
    return ax.text(x,y,s,fontsize=size,color=color,weight=weight,ha=ha,va=va,style=style,wrap=wrap,zorder=5)

def arrow(ax,x1,y1,x2,y2,color=GOLD,lw=2.4,style="-|>",rad=0.0):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=20,
                      lw=lw,color=color,connectionstyle=f"arc3,rad={rad}",zorder=3)
    ax.add_patch(a); return a

def save(f,name):
    f.savefig(f"{OUT}/{name}",facecolor=BG,bbox_inches=None); plt.close(f)
    print("saved",name)

# ============================================================
# 1. ATENÇÃO vs INTENÇÃO  (two funnels)
# ============================================================
f,ax=fig(11,7)
txt(ax,50,95,"OS DOIS MARKETINGS",size=22,color=GOLD,weight="bold")
txt(ax,50,89,"por que um queima dinheiro e o outro vende imóveis",size=12,color=MUTE,style="italic")

def funnel(cx, levels, colors, labels, title, tcolor):
    txt(ax,cx,80,title,size=15,color=tcolor,weight="bold")
    top=74; widths=[34,26,18,9]; h=11
    y=top
    for i,(lab,col) in enumerate(zip(labels,colors)):
        w=widths[i]
        poly=Polygon([(cx-w/2,y),(cx+w/2,y),(cx+widths[min(i+1,3)]/2,y-h),(cx-widths[min(i+1,3)]/2,y-h)],
                     closed=True,fc=col,ec=BG,lw=2,alpha=0.92,zorder=2)
        ax.add_patch(poly)
        txt(ax,cx,y-h/2,lab,size=11,color="#14110E",weight="bold")
        y-=h
# left: attention
funnel(27,4,[ "#7a3a35","#94443d","#b35047","#C5524A"],
       ["TODO MUNDO vê","curiosos param","\"quanto custa?\"","some"],
       "MARKETING DE ATENÇÃO", BAD)
txt(ax,27,14,"Hook que atrai todos →\nleads ruins → verba queimada",size=11,color=BAD,weight="bold")
# right: intention
funnel(73,4,["#2f5f4a","#3a7a5e","#429a72","#4CB286"],
       ["só o PÚBLICO CERTO","interesse real","quer saber +","COMPRA"],
       "MARKETING DE INTENÇÃO", GOOD)
txt(ax,73,14,"Hook que repele curioso →\nleads bons → comissão",size=11,color=GOOD,weight="bold")
# divider
ax.add_line(Line2D([50,50],[8,82],color=GOLD,lw=1,alpha=0.4,ls=(0,(4,4))))
save(f,"01_atencao_vs_intencao.png")

# ============================================================
# 2. COMO O ALGORITMO OTIMIZA (cycle)
# ============================================================
f,ax=fig(10,7)
txt(ax,50,94,"O CICLO DA OTIMIZAÇÃO",size=22,color=GOLD,weight="bold")
txt(ax,50,88,"o algoritmo não sabe se o lead é bom — ele só copia quem reagiu",size=12,color=MUTE,style="italic")
nodes=[("1. ENTREGA TESTE\npara público variado",50,72,BLUE),
       ("2. MEDE A REAÇÃO\nviu? parou? mandou msg?",80,45,BLUE),
       ("3. APRENDE O PADRÃO\nquem reagiu = \"sucesso\"",50,18,GOLD),
       ("4. DOBRA A APOSTA\nbusca mais gente igual",20,45,GOOD)]
for s,x,y,c in nodes:
    box(ax,x-15,y-7,30,14,fc=PANEL,ec=c,lw=2.2)
    txt(ax,x,y,s,size=11,color=CREAM,weight="bold")
arrow(ax,58,68,74,52,rad=-0.25)
arrow(ax,74,40,58,22,rad=-0.25)
arrow(ax,42,22,26,40,rad=-0.25)
arrow(ax,26,52,42,68,rad=-0.25)
txt(ax,50,45,"VOCÊ ESCOLHE\nO QUE ELE\nVAI COPIAR",size=12,color=GOLD2,weight="bold")
save(f,"02_ciclo_otimizacao.png")

# ============================================================
# 3. BOLA DE NEVE  (negative vs positive)
# ============================================================
f,ax=fig(11,6.5)
txt(ax,50,94,"A BOLA DE NEVE DA OTIMIZAÇÃO",size=21,color=GOLD,weight="bold")
txt(ax,50,88,"o mesmo mecanismo trabalha a seu favor ou contra você",size=12,color=MUTE,style="italic")
# negative (left) growing red circles downhill
txt(ax,27,80,"❄  BOLA DE NEVE RUIM",size=14,color=BAD,weight="bold")
xs=[12,19,28,39]; ys=[68,60,50,38]; rs=[3,4.5,6.5,9]
for i,(x,y,r) in enumerate(zip(xs,ys,rs)):
    ax.add_patch(Circle((x,y),r,fc="#C5524A",ec="#7a3a35",lw=2,alpha=0.85,zorder=3))
ax.add_line(Line2D([8,46],[64,30],color=MUTE,lw=2,alpha=0.5))
txt(ax,27,22,"curioso manda msg → algoritmo acha bom →\ntraz + curiosos → leads cada vez piores",size=10.5,color=BAD,ha="center")
# positive (right) growing green circles uphill
txt(ax,73,80,"❄  BOLA DE NEVE BOA",size=14,color=GOOD,weight="bold")
xs2=[60,69,78,88]; ys2=[40,50,60,70];
for i,(x,y,r) in enumerate(zip(xs2,ys2,rs)):
    ax.add_patch(Circle((x,y),r,fc="#4CB286",ec="#2f5f4a",lw=2,alpha=0.85,zorder=3))
ax.add_line(Line2D([54,92],[34,66],color=MUTE,lw=2,alpha=0.5))
txt(ax,73,22,"comprador real reage → algoritmo copia →\ntraz + compradores → leads cada vez melhores",size=10.5,color=GOOD,ha="center")
ax.add_line(Line2D([50,50],[18,82],color=GOLD,lw=1,alpha=0.3,ls=(0,(4,4))))
save(f,"03_bola_de_neve.png")

# ============================================================
# 4. OS TRÊS ELEMENTOS (pillars)
# ============================================================
f,ax=fig(11,6.5)
txt(ax,50,94,"OS 3 ELEMENTOS DO MARKETING DE INTENÇÃO",size=19,color=GOLD,weight="bold")
txt(ax,50,88,"erre um e a máquina inteira trava",size=12,color=MUTE,style="italic")
cols=[("1","ICP REAL","Mire na MOTIVAÇÃO\nde compra, não em\nidade/gênero.\nRegra, não exceção.",GOLD),
      ("2","IMÓVEL\nPROTAGONISTA","O astro é o imóvel,\nnão o corretor.\nQuem é fisgado pelo\nimóvel é qualificado.",GOLD2),
      ("3","ELEMENTOS\nQUALIFICATIVOS","Preço, metragem,\ncondição explícitos.\nExpulsa o curioso,\natrai o comprador.",GOLD)]
xs=[18,50,82]
for (num,t,d,c),x in zip(cols,xs):
    box(ax,x-14,30,28,46,fc=PANEL,ec=c,lw=2.4)
    ax.add_patch(Circle((x,70),5.5,fc=c,ec=BG,lw=2,zorder=4))
    txt(ax,x,70,num,size=20,color="#14110E",weight="bold")
    txt(ax,x,60,t,size=13.5,color=c,weight="bold")
    txt(ax,x,45,d,size=11,color=CREAM)
txt(ax,50,18,"ICP  +  IMÓVEL EM FOCO  +  FILTRO EXPLÍCITO  =  LEAD QUE COMPRA",
    size=12.5,color=GOOD,weight="bold")
save(f,"04_tres_elementos.png")

# ============================================================
# 5. MAPA DE ICP por faixa (motivações)
# ============================================================
f,ax=fig(11,7)
txt(ax,50,95,"MAPA DE MOTIVAÇÃO POR FAIXA DE IMÓVEL",size=18,color=GOLD,weight="bold")
txt(ax,50,90,"o mesmo imóvel, dores e desejos completamente diferentes",size=11.5,color=MUTE,style="italic")
rows=[("Minha Casa Minha Vida","Sair do aluguel, começar a vida,\nrealizar o 1º imóvel, segurança","Casal jovem / 1º emprego estável",GOOD),
      ("Médio padrão (upgrade)","Espaço p/ os filhos, melhor bairro,\nsubir de vida, status discreto","Família formada, 30–45 anos",BLUE),
      ("Alto padrão / 2 milhões+","Upgrade de lazer e espaço, conforto,\nendereço, troca do compacto","Já tem imóvel, 40+, renda alta",GOLD),
      ("Investimento / frente-mar","Renda de aluguel, valorização,\ndiversificar patrimônio","Investidor de outro estado",GOLD2)]
y=78
for t,m,p,c in rows:
    box(ax,6,y-13,88,12,fc=PANEL,ec=c,lw=1.8)
    ax.add_patch(Rectangle((6,y-13),2.5,12,fc=c,ec="none",zorder=4))
    txt(ax,11,y-7,t,size=12.5,color=c,weight="bold",ha="left")
    txt(ax,40,y-7,m,size=10.5,color=CREAM,ha="left")
    txt(ax,72,y-7,p,size=10.5,color=MUTE,ha="left")
    y-=16
txt(ax,50,6,"O anúncio precisa falar com UMA motivação — a da regra, não da exceção.",
    size=11.5,color=GOLD2,weight="bold")
save(f,"05_mapa_icp.png")

# ============================================================
# 6. ANATOMIA DO ANÚNCIO (phone mockup annotated)
# ============================================================
f,ax=fig(10,7.5)
txt(ax,50,96,"ANATOMIA DO ANÚNCIO QUE VENDE",size=20,color=GOLD,weight="bold")
# phone
px,py,pw,ph=38,8,24,80
box(ax,px,py,pw,ph,fc="#0d0b09",ec=GOLD,lw=2.5,rad=3)
# screen sections
ax.add_patch(Rectangle((px+1.5,py+58),pw-3,18,fc="#33506b",ec="none"))  # imovel video
txt(ax,px+pw/2,py+67,"VÍDEO DO\nIMÓVEL",size=10,color=CREAM,weight="bold")
ax.add_patch(Rectangle((px+1.5,py+44),pw-3,12,fc="#1d1915",ec="none"))
txt(ax,px+pw/2,py+50,"R$ 389.000\n68m² · 2 qts · 1 vaga",size=9,color=GOLD2,weight="bold")
ax.add_patch(Rectangle((px+1.5,py+30),pw-3,12,fc="#1d1915",ec="none"))
txt(ax,px+pw/2,py+36,"Bairro X · pronto\np/ morar",size=9,color=CREAM)
ax.add_patch(FancyBboxPatch((px+3,py+18),pw-6,7,boxstyle="round,pad=0.1,rounding_size=1.5",fc=GOOD,ec="none"))
txt(ax,px+pw/2,py+21.5,"CHAMAR NO WHATSAPP",size=8.5,color="#0d2a1d",weight="bold")
# annotations
def ann(x,y,tx,ty,s,c):
    arrow(ax,tx,ty,x,y,color=c,lw=1.8,style="-|>")
    box(ax,tx-0.5 if tx<50 else tx-23,ty-3.5,23,7,fc=PANEL,ec=c,lw=1.5)
    txt(ax,(tx-0.5 if tx<50 else tx-23)+11.5,ty,s,size=9,color=CREAM)
ann(px+1.5,py+67, 8,72,"Imóvel como 1º frame\n(gancho que filtra)",GOLD)
ann(px+1.5,py+50, 8,52,"Preço já no anúncio\n= repele curioso",GOLD)
ann(px+1.5,py+36, 8,34,"Qualificativos:\nmetragem, vagas, status",GOLD)
ann(px+pw+1.5,py+21, 92,24,"CTA direto p/ WhatsApp\n(conversa, não link)",GOOD)
ann(px+pw+1.5,py+67, 92,68,"Sem dancinha,\nsem o corretor na tela",GOLD2)
save(f,"06_anatomia_anuncio.png")

# ============================================================
# 7. ESTRUTURA META ADS (hierarchy)
# ============================================================
f,ax=fig(10,6.5)
txt(ax,50,94,"ESTRUTURA DA CAMPANHA NO META ADS",size=19,color=GOLD,weight="bold")
txt(ax,50,88,"3 níveis — cada um com uma decisão diferente",size=12,color=MUTE,style="italic")
levels=[("CAMPANHA","Objetivo: Engajamento (mensagens)\nou Vendas/Conversa no WhatsApp",GOLD,72,60),
        ("CONJUNTO DE ANÚNCIOS","Público (ICP), região, orçamento (R$30/dia),\nposicionamento, otimização da entrega",GOLD2,48,72),
        ("ANÚNCIO","Criativo: vídeo do imóvel + copy com\nqualificativos + CTA p/ WhatsApp",GOOD,24,80)]
for t,d,c,y,w in levels:
    box(ax,50-w/2,y-9,w,15,fc=PANEL,ec=c,lw=2.2)
    txt(ax,50,y+1,t,size=13,color=c,weight="bold")
    txt(ax,50,y-5,d,size=10,color=CREAM)
arrow(ax,50,63,50,57,color=GOLD)
arrow(ax,50,39,50,33,color=GOLD2)
save(f,"07_estrutura_meta_ads.png")

# ============================================================
# 8. FLUXO WHATSAPP (qualification)
# ============================================================
f,ax=fig(9.5,8)
txt(ax,50,96,"SCRIPT DE QUALIFICAÇÃO NO WHATSAPP",size=18,color=GOLD,weight="bold")
txt(ax,50,91,"um lead não é um cliente — qualifique antes de gastar tempo",size=11,color=MUTE,style="italic")
steps=[("Lead chega pelo anúncio","Resposta rápida (<5 min)\n\"Oi! Vi que você se interessou\npelo [imóvel]. Posso te ajudar?\"",GOLD,80),
       ("Pergunta de intenção","\"Você procura para morar\nou para investir?\"",BLUE,63),
       ("Pergunta de capacidade","\"Já tem o valor de entrada /\nfinanciamento aprovado?\"",BLUE,46),
       ("Agendar visita","\"Posso te mostrar pessoalmente?\nQue dia fica melhor?\"",GOOD,29),
       ("Visita → proposta","Foco total no comprador\nqualificado que sobrou",GOOD,12)]
for t,d,c,y in steps:
    box(ax,18,y-6,64,11,fc=PANEL,ec=c,lw=1.9)
    txt(ax,50,y+1.5,t,size=12,color=c,weight="bold")
    txt(ax,50,y-3.5,d,size=9.5,color=CREAM)
for y in [74,57,40,23]:
    arrow(ax,50,y,50,y-6,color=GOLD)
save(f,"08_fluxo_whatsapp.png")

# ============================================================
# 9. MATEMÁTICA DA ESCALA (snowball reinvest)
# ============================================================
f=plt.figure(figsize=(10,6),dpi=170); f.patch.set_facecolor(BG)
ax=f.add_axes([0.1,0.14,0.85,0.72]); ax.set_facecolor(PANEL)
meses=["Mês 1","Mês 2","Mês 3","Mês 4","Mês 5","Mês 6"]
invest=[900,1800,2700,3600,4500,5400]
retorno=[12000,24000,36000,48000,60000,72000]
x=np.arange(len(meses)); w=0.38
ax.bar(x-w/2, invest, w, color=BAD, label="Investido (R$30/dia reinvestido)")
ax.bar(x+w/2, retorno, w, color=GOOD, label="Comissão (1 venda/mês ~R$12k)")
for i,v in enumerate(retorno):
    ax.text(i+w/2, v+1500, f"R${v//1000}k", ha="center", color=GOLD2, fontsize=9, weight="bold")
ax.set_xticks(x); ax.set_xticklabels(meses, color=CREAM)
ax.tick_params(colors=MUTE); ax.set_ylim(0,82000)
for s in ax.spines.values(): s.set_color("none")
ax.set_title("A BOLA DE NEVE DO REINVESTIMENTO", color=GOLD, fontsize=17, weight="bold", pad=14)
ax.legend(facecolor=PANEL, edgecolor=GOLD, labelcolor=CREAM, fontsize=10, loc="upper left")
ax.grid(axis="y", color=MUTE, alpha=0.15)
f.text(0.5,0.03,"Cenário pessimista: 1 venda/mês. Reinveste parte da comissão → mais campanhas → mais vendas.",
       ha="center", color=MUTE, fontsize=10, style="italic")
f.savefig(f"{OUT}/09_escala_matematica.png", facecolor=BG); plt.close(f); print("saved 09")

# ============================================================
# 10. FUNIL COMPLETO
# ============================================================
f,ax=fig(10,7)
txt(ax,50,95,"O FUNIL COMPLETO DA VENDA",size=20,color=GOLD,weight="bold")
stages=[("META ADS","vídeo do imóvel que filtra o curioso","#33506b",82),
        ("ALGORITMO OTIMIZA","aprende e busca + compradores reais","#3a6d8a",67),
        ("WHATSAPP","resposta rápida + script de qualificação","#b8893a",52),
        ("VISITA","só o lead qualificado que sobrou","#ca9b46",37),
        ("PROPOSTA & VENDA","financiamento → comissão","#4CB286",22)]
wlist=[80,68,56,42,30]
for (t,d,c,y),w in zip(stages,wlist):
    poly=Polygon([(50-w/2,y),(50+w/2,y),(50+ (wlist[min(stages.index((t,d,c,y))+1,4)])/2 ,y-13),
                  (50-(wlist[min(stages.index((t,d,c,y))+1,4)])/2,y-13)],closed=True,
                 fc=c,ec=BG,lw=2,alpha=0.92,zorder=2)
    ax.add_patch(poly)
    txt(ax,50,y-5,t,size=13,color="#14110E",weight="bold")
    txt(ax,50,y-9.5,d,size=9.5,color="#14110E")
txt(ax,50,6,"Cada etapa REMOVE o curioso e CONCENTRA o comprador real.",size=11.5,color=GOLD2,weight="bold")
save(f,"10_funil_completo.png")

print("ALL DIAGRAMS DONE")
PY_DONE = True

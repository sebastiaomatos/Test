#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D
import os
OUT="/tmp/apostila/img"; os.makedirs(OUT,exist_ok=True)

BG="#14110E"; PANEL="#1d1915"; PANEL2="#262019"; GOLD="#D8A84B"; GOLD2="#F0CB6E"
CREAM="#F4EEE2"; MUTE="#9c9286"; GOOD="#4CB286"; BAD="#C5524A"; BLUE="#5B8DB8"
META="#5B8DB8"; GOOGLE="#E0A93B"; YT="#C5524A"; TT="#7FB7C9"; WA="#4CB286"; MAIL="#C58FBf".replace("Bf","BF")

plt.rcParams.update({"font.family":"DejaVu Sans","text.color":CREAM})
def fig(w,h):
    f=plt.figure(figsize=(w,h),dpi=170); ax=f.add_axes([0,0,1,1])
    ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
    f.patch.set_facecolor(BG); ax.set_facecolor(BG); return f,ax
def box(ax,x,y,w,h,fc=PANEL,ec=GOLD,lw=1.8,rad=2.2,alpha=1):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.15,rounding_size={rad}",
                 fc=fc,ec=ec,lw=lw,alpha=alpha));
def t(ax,x,y,s,size=11,color=CREAM,w="normal",ha="center",va="center",style="normal"):
    ax.text(x,y,s,fontsize=size,color=color,weight=w,ha=ha,va=va,style=style,zorder=6)
def arr(ax,x1,y1,x2,y2,color=GOLD,lw=2.2,style="-|>",rad=0.0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=18,
                 lw=lw,color=color,connectionstyle=f"arc3,rad={rad}",zorder=3))
def chip(ax,x,y,w,label,color):
    box(ax,x,y,w,5.2,fc=color,ec=color,rad=2.6); t(ax,x+w/2,y+2.6,label,size=9,color="#14110E",w="bold")
def save(f,n): f.savefig(f"{OUT}/{n}",facecolor=BG); plt.close(f); print("saved",n)

# =====================================================================
# M1 — MAPA GERAL FULL-FUNNEL
# =====================================================================
f,ax=fig(12,8.2)
t(ax,50,96,"A MÁQUINA COMPLETA DE AQUISIÇÃO",size=22,color=GOLD,w="bold")
t(ax,50,91.5,"4 camadas, várias plataformas, um único objetivo: lead de qualidade barato e em escala",size=11,color=MUTE,style="italic")
# Layer bands
def band(y,h,title,sub,col):
    box(ax,5,y,78,h,fc=PANEL,ec=col,lw=2);
    t(ax,9,y+h-2.5,title,size=12.5,color=col,w="bold",ha="left")
    if sub: t(ax,9,y+2.2,sub,size=8.7,color=MUTE,ha="left")
# 1 Aquisição
band(70,16,"1 · AQUISIÇÃO  (tráfego frio — volume barato)","objetivo: iniciar conversa / capturar lead",META)
for x,(lab,c) in zip([26,41,56,70.5],[("Meta CTWA",META),("Meta Lead Ads",META),("Google Search",GOOGLE),("Google PMax",GOOGLE)]):
    chip(ax,x,77,13,lab,c)
chip(ax,26,71.4,13,"TikTok (MCMV)",TT)
# 2 Nutrição
band(50.5,16,"2 · NUTRIÇÃO & RETARGETING","reaquecer quem engajou mas não respondeu",GOLD)
for x,(lab,c) in zip([26,41,56,71],[("Meta RMKT",META),("YouTube RMKT",YT),("E-mail (auto)",MAIL),("WhatsApp (auto)",WA)]):
    chip(ax,x,57.5,13,lab,c)
t(ax,55,52.4,"para leads que viram 50–75% do vídeo, clicaram, ou pararam de responder",size=8.5,color=MUTE)
# 3 Conversão
band(31,16,"3 · CONVERSÃO  (atendimentos atuais)","acelerar fechamento + subir taxa de conversão",GOOD)
for x,(lab,c) in zip([26,44,62],[("Meta BOFU (lista CRM)",META),("WhatsApp fechamento",WA),("E-mail simulação",MAIL)]):
    chip(ax,x,38,16,lab,c)
t(ax,50,32.8,"públicos: agendou visita · recebeu proposta · lead quente sem decisão",size=8.5,color=MUTE)
# 4 Escala
band(13.5,14,"4 · ESCALA DE QUALIDADE","baratear o lead e multiplicar o que já funciona",GOLD2)
for x,(lab,c) in zip([26,44,62],[("Lookalike 1–3% compradores",GOLD2),("CBO/Advantage+ vencedores",META),("Ampliar verba dos top ads",GOOGLE)]):
    chip(ax,x,20,16,lab,c)
# down arrows
for y in [70,50.5,31]: arr(ax,44,y,44,y-2.6,color=GOLD)
# feedback loop (right)
arr(ax,83,20,90,20,color=GOOD,lw=2.4)
arr(ax,90,20,90,79,color=GOOD,lw=2.4,style="-")
arr(ax,90,79,83,79,color=GOOD,lw=2.4)
t(ax,93.5,50,"DADOS DE VENDA / CONVERSA QUALIFICADA\n(via CAPI + eventos offline do CRM)\nrealimentam o algoritmo → Lookalike",
  size=8.6,color=GOOD,w="bold",ha="center"); ax.text(93.5,50,"",rotation=90)
save(f,"M1_mapa_geral.png")

# =====================================================================
# M2 — SEQUÊNCIA META
# =====================================================================
f,ax=fig(12,6.6)
t(ax,50,95,"SEQUÊNCIA META ADS  (Instagram + Facebook)",size=18,color=META,w="bold")
t(ax,50,90,"do tráfego frio à escala via Lookalike alimentado por CAPI",size=10.5,color=MUTE,style="italic")
steps=[
 ("FRIO · TOPO","CTWA + Lead Ads\nReels/Story + Feed\nAdvantage+ público",META,12,"R$ 60+40 /dia"),
 ("EVENTO","Conversa iniciada\nLead capturado\n→ Pixel + CAPI",GOLD,33,"—"),
 ("RETARGETING","Viu 50–75% vídeo\nEngajou 30–90d\nMsg sem resposta",GOLD2,54,"R$ 25 /dia"),
 ("CONVERSÃO","Lista CRM (BOFU)\nVisitou / proposta\nUrgência + prova",GOOD,75,"R$ 20 /dia"),
]
for (titf,desc,c,x,bud) in steps:
    box(ax,x-9,52,18,26,fc=PANEL,ec=c,lw=2.2)
    t(ax,x,73,titf,size=11.5,color=c,w="bold")
    t(ax,x,62,desc,size=8.8,color=CREAM)
    chip(ax,x-7,45,14,bud,c if bud!="—" else MUTE)
for x in [21,42,63]: arr(ax,x+3,65,x+12,65,color=META)
# lookalike feedback
box(ax,33,18,42,12,fc=PANEL2,ec=GOLD2,lw=2)
t(ax,54,26,"ESCALA · LOOKALIKE 1–3%",size=12,color=GOLD2,w="bold")
t(ax,54,21.5,"semelhantes a quem comprou / iniciou conversa qualificada · CBO escala os criativos vencedores",size=8.6,color=CREAM)
arr(ax,75,52,70,30,color=GOOD,lw=2.2,rad=-0.3)
arr(ax,33,24,12,52,color=GOLD2,lw=2.2,rad=-0.3)
t(ax,20,38,"alimenta\no topo",size=8.5,color=GOLD2,style="italic")
save(f,"M2_sequencia_meta.png")

# =====================================================================
# M3 — SEQUÊNCIA GOOGLE
# =====================================================================
f,ax=fig(12,6.6)
t(ax,50,95,"SEQUÊNCIA GOOGLE ADS",size=18,color=GOOGLE,w="bold")
t(ax,50,90,"capturar a demanda que já procura + escalar e reimpactar",size=10.5,color=MUTE,style="italic")
tracks=[("SEARCH · ALTA INTENÇÃO","palavras: \"apartamento 2 qtos [bairro]\",\n\"imóvel financiamento [cidade]\"\nnegativadas: aluguel, vagas, curso",GOOGLE,78),
        ("PERFORMANCE MAX","asset groups por empreendimento\nfeed + criativos · IA do Google\nescala multi-rede",GOOD,58),
        ("DEMAND GEN / YOUTUBE","frio (vídeo do imóvel) +\nretargeting de quem visitou\nShorts / In-stream",YT,38)]
for (titf,desc,c,y) in tracks:
    box(ax,6,y-8,40,14,fc=PANEL,ec=c,lw=2.1)
    t(ax,9,y+3,titf,size=11,color=c,w="bold",ha="left")
    t(ax,9,y-3.5,desc,size=8.6,color=CREAM,ha="left")
    arr(ax,46,y-1,60,46,color=c,rad=0.05)
box(ax,60,40,32,12,fc=PANEL2,ec=GOLD,lw=2.2)
t(ax,76,47,"LANDING RÁPIDA + WHATSAPP",size=11,color=GOLD,w="bold")
t(ax,76,42.5,"form curto · conversão = clique no WhatsApp / lead",size=8.4,color=CREAM)
arr(ax,76,40,76,30,color=GOLD)
box(ax,60,18,32,11,fc=PANEL,ec=WA,lw=2)
t(ax,76,24.5,"ATENDIMENTO WHATSAPP",size=11,color=WA,w="bold")
t(ax,76,20,"entra no fluxo automático de qualificação",size=8.3,color=CREAM)
# budgets
t(ax,26,11,"Orçamento sugerido:  Search R$ 50/dia  ·  PMax R$ 50/dia  ·  Demand Gen R$ 30/dia",
  size=9.5,color=GOLD2,w="bold")
save(f,"M3_sequencia_google.png")

# =====================================================================
# M4 — FLUXO WHATSAPP AUTOMÁTICO
# =====================================================================
f,ax=fig(10,8.4)
t(ax,50,96.5,"FLUXO DE WHATSAPP AUTOMÁTICO",size=18,color=WA,w="bold")
t(ax,50,92.5,"acelera o fechamento e recupera o lead que esfria — disparos automáticos",size=10,color=MUTE,style="italic")
items=[("D0 · 0–5 min","Resposta imediata + qualificação: \"morar ou investir?\" / \"como pretende comprar?\"",WA),
       ("D0 · +10 min (sem resposta)","Reforço com PROVA: foto/vídeo do imóvel + \"esse costuma sair rápido\"",GOLD2),
       ("D1","Convite de visita com 2 horários fechados (\"amanhã à tarde ou sábado?\")",WA),
       ("D2","Quebra de objeção preço: simulação de financiamento + comparativo aluguel × parcela",BLUE),
       ("D4","Escassez real: \"últimas unidades / condição da entrada termina sexta\"",BAD),
       ("D7","Última chamada + ALTERNATIVA: outro imóvel do mesmo perfil (ICP)",GOLD),
       ("D15 / D30","Reativação: novidade, novo empreendimento, mudança de condição",MUTE)]
y=84
for (d,desc,c) in items:
    ax.add_patch(Circle((12,y),1.5,fc=c,ec=BG,lw=1.5,zorder=5))
    box(ax,16,y-4,78,7.5,fc=PANEL,ec=c,lw=1.7)
    t(ax,19,y+1.2,d,size=10.5,color=c,w="bold",ha="left")
    t(ax,19,y-2.3,desc,size=8.7,color=CREAM,ha="left")
    y-=11.4
ax.add_line(Line2D([12,12],[8,84],color=MUTE,lw=2,alpha=0.4,zorder=1))
save(f,"M4_fluxo_whatsapp.png")

# =====================================================================
# M5 — SEQUÊNCIA E-MAIL
# =====================================================================
f,ax=fig(10,8)
t(ax,50,96.5,"SEQUÊNCIA DE E-MAIL (NUTRIÇÃO AUTOMÁTICA)",size=16.5,color=MAIL,w="bold")
t(ax,50,92.5,"para leads que deixaram e-mail (Lead Ads / landing) — constrói desejo e confiança",size=9.5,color=MUTE,style="italic")
mails=[("E1 · imediato","Assunto: \"Recebi seu interesse — próximos passos\"","Boas-vindas + link direto do WhatsApp"),
       ("E2 · Dia 1","Assunto: \"Vendi um imóvel de R$400 mil com R$16 de anúncio\"","História/prova → autoridade"),
       ("E3 · Dia 2","Assunto: \"Financiamento Caixa: o passo a passo (sem letra miúda)\"","Conteúdo útil → reciprocidade"),
       ("E4 · Dia 4","Assunto: \"Separei este apê pensando em você\"","Imóvel do ICP + condição"),
       ("E5 · Dia 6","Assunto: \"A condição da entrada termina sexta\"","Escassez + CTA visita"),
       ("E6 · Dia 10","Assunto: \"Ainda procurando? Tenho 3 opções novas\"","Reativação")]
y=85
for (e,subj,goal) in mails:
    box(ax,8,y-5.5,84,9.5,fc=PANEL,ec=MAIL,lw=1.7)
    t(ax,11,y+1,e,size=10.5,color=MAIL,w="bold",ha="left")
    t(ax,11,y-2.2,subj,size=8.8,color=CREAM,ha="left")
    t(ax,11,y-5,goal,size=8,color=MUTE,ha="left",style="italic")
    if y>20: arr(ax,50,y-5.5,50,y-7.4,color=MAIL,lw=1.6)
    y-=13.3
save(f,"M5_sequencia_email.png")

# =====================================================================
# M6 — ENGINE DE DADOS (Pixel/CAPI/CRM -> Lookalike)
# =====================================================================
f,ax=fig(11,6.6)
t(ax,50,95,"A ENGINE DE DADOS (o que baratea o lead)",size=18,color=GOLD,w="bold")
t(ax,50,90,"sem medir a conversa/venda, o algoritmo otimiza para curiosos. com dados, ele caça compradores.",size=9.6,color=MUTE,style="italic")
nodes=[("ANÚNCIO\n+ clique",14,62,META),
       ("PIXEL + CAPI\n(evento de conversa)",38,62,GOLD),
       ("CRM\n(estágios do lead)",62,62,GOOD),
       ("EVENTO DE VALOR\nvisita · proposta · VENDA",86,62,GOOD)]
for s,x,y,c in nodes:
    box(ax,x-10,y-6,20,12,fc=PANEL,ec=c,lw=2.1); t(ax,x,y,s,size=9.5,color=CREAM,w="bold")
for x1,x2 in [(24,28),(48,52),(72,76)]: arr(ax,x1,62,x2,62,color=GOLD)
# feedback down to optimization
box(ax,30,24,40,12,fc=PANEL2,ec=GOLD2,lw=2.2)
t(ax,50,31,"DE VOLTA AO META/GOOGLE COMO CONVERSÃO",size=11,color=GOLD2,w="bold")
t(ax,50,26.5,"otimização para quem CONVERTE + base do Lookalike de compradores",size=8.6,color=CREAM)
arr(ax,86,56,70,36,color=GOOD,lw=2.2,rad=-0.25)
arr(ax,30,30,14,56,color=GOLD2,lw=2.2,rad=-0.25)
t(ax,12,42,"melhora\no público\ndo topo",size=8.4,color=GOLD2,style="italic")
t(ax,50,12,"Resultado: CPL cai mês a mês · leads mais qualificados · maior taxa de conversão",
  size=10,color=GOOD,w="bold")
save(f,"M6_engine_dados.png")
print("DONE_FLOWS")

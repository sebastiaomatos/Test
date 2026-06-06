#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera landing pages com branding da Imobiliária Aprovar para 2 imóveis em Cuiabá-MT."""
import os, html
BASE=os.path.dirname(os.path.abspath(__file__))
LAND=os.path.join(BASE,"..","landing")

PHONE_DISPLAY="(65) 99232-6461"; PHONE_WA="5565992326461"
def wa(msg): return f"https://wa.me/{PHONE_WA}?text={html.escape(msg).replace(' ','%20')}"

def _svg(inner): return f'<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#F57F17" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
ICONS={
 "key":_svg('<circle cx="8" cy="8" r="4"/><path d="M11 11l8 8M16 16l2-2M19 19l1.5-1.5"/>'),
 "bank":_svg('<path d="M3 9l9-5 9 5"/><path d="M5 9v8M9 9v8M15 9v8M19 9v8"/><path d="M3 21h18"/>'),
 "pool":_svg('<path d="M3 16c1.5 0 1.5-1 3-1s1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1"/><path d="M3 20c1.5 0 1.5-1 3-1s1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1"/><path d="M8 13V5a2 2 0 0 1 4 0M16 13V5"/>'),
 "pin":_svg('<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
 "money":_svg('<circle cx="12" cy="12" r="9"/><path d="M14.5 9.2C14 8.4 13.1 8 12 8c-1.5 0-2.5.8-2.5 2s1 1.7 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1.1 0-2-.4-2.5-1.2M12 6.5v11"/>'),
 "chart":_svg('<path d="M4 7l5 5 3-3 7 7"/><path d="M19 16v-4h-4"/>'),
}

CSS = """
:root{
  --orange:#F57F17; --orange-d:#D96B00; --green:#004310; --green2:#2E9B4F;
  --wa:#25D366; --ink:#1f2a24; --mute:#6b7670; --cream:#FFFDF7; --line:#e6e3d8;
  --radius:16px; --shadow:0 16px 44px rgba(0,30,12,.16);
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Manrope',system-ui,Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.wrap--narrow{max-width:780px}
img{max-width:100%;display:block}
h1,h2,h3,h4{line-height:1.14;font-weight:800}
.center{text-align:center}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-weight:800;border-radius:999px;
  padding:15px 28px;text-decoration:none;cursor:pointer;border:0;font-size:1rem;transition:transform .12s,box-shadow .12s}
.btn:hover{transform:translateY(-2px)}
.btn--orange{background:var(--orange);color:#fff;box-shadow:0 10px 26px rgba(245,127,23,.4)}
.btn--wa{background:var(--wa);color:#fff;box-shadow:0 10px 26px rgba(37,211,102,.4)}
.btn--ghost{background:transparent;color:#fff;border:1.6px solid rgba(255,255,255,.55)}
.btn--lg{padding:18px 32px;font-size:1.08rem}
.btn--block{width:100%}

/* topbar */
.top{background:var(--green);color:#fff;position:sticky;top:0;z-index:50;border-bottom:3px solid var(--orange)}
.top__in{display:flex;align-items:center;justify-content:space-between;padding:12px 0;gap:16px}
.top__logo{height:46px}
.top__right{display:flex;align-items:center;gap:18px}
.top__phone{color:#fff;text-decoration:none;font-weight:700;font-size:.98rem;opacity:.95}
.top__phone span{display:block;font-size:.72rem;opacity:.7;font-weight:600}

/* hero */
.hero{position:relative;color:#fff;padding:60px 0 70px;overflow:hidden}
.hero__bg{position:absolute;inset:0;background-size:cover;background-position:center;z-index:-2}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;
  background:linear-gradient(110deg,rgba(0,40,14,.93) 32%,rgba(0,52,16,.78) 58%,rgba(0,40,14,.45))}
.hero__grid{display:grid;grid-template-columns:1.12fr .88fr;gap:42px;align-items:center}
.badge{display:inline-flex;align-items:center;gap:8px;background:var(--orange);color:#fff;font-weight:800;
  font-size:.8rem;letter-spacing:.5px;padding:7px 15px;border-radius:999px;margin-bottom:16px;text-transform:uppercase}
.hero h1{font-size:clamp(2rem,4.2vw,3rem);margin-bottom:10px}
.hero .loc{font-size:1.05rem;color:#dfeee2;margin-bottom:20px}
.hero .loc b{color:#fff}
.price{display:flex;align-items:baseline;gap:10px;margin-bottom:20px}
.price b{font-size:2.4rem;color:#fff}
.price small{color:#cfe6d6;font-size:.95rem}
.specs{list-style:none;display:flex;gap:14px;flex-wrap:wrap;margin-bottom:26px}
.specs li{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:12px;padding:10px 16px;
  display:flex;flex-direction:column;min-width:84px}
.specs b{font-size:1.15rem;color:#fff}
.specs span{font-size:.74rem;color:#cfe6d6}
.hero__cta{display:flex;gap:13px;flex-wrap:wrap}
.microtrust{margin-top:18px;font-size:.86rem;color:#cfe6d6}

/* form card */
.card{background:#fff;color:var(--ink);border-radius:var(--radius);box-shadow:var(--shadow);padding:28px}
.form-card h3{font-size:1.32rem;color:var(--green)}
.form-card .sub{color:var(--mute);font-size:.92rem;margin:6px 0 16px}
.form-card label{display:block;font-size:.82rem;font-weight:800;color:#3a463f;margin-bottom:12px}
.form-card input,.form-card select{width:100%;margin-top:5px;padding:13px 14px;border:1.5px solid var(--line);
  border-radius:11px;font-size:1rem;font-family:inherit;background:#fbfaf4}
.form-card input:focus,.form-card select:focus{outline:none;border-color:var(--orange)}
.form-card .priv{color:var(--mute);font-size:.76rem;margin-top:12px;text-align:center}

/* sections */
.sec{padding:74px 0}
.sec--soft{background:#f7f5ee}
.sec--green{background:var(--green);color:#fff}
.sec__head{text-align:center;max-width:680px;margin:0 auto 40px}
.sec__kick{color:var(--orange);font-weight:800;letter-spacing:2px;text-transform:uppercase;font-size:.82rem}
.sec__title{font-size:clamp(1.6rem,3vw,2.25rem);margin:8px 0;color:var(--green)}
.sec--green .sec__title{color:#fff}
.sec__sub{color:var(--mute)}
.sec--green .sec__sub{color:#cfe6d6}

/* features */
.feats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.feat{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:26px;text-align:center}
.feat__ic{width:56px;height:56px;border-radius:14px;background:rgba(245,127,23,.12);color:var(--orange);
  display:flex;align-items:center;justify-content:center;font-size:1.6rem;margin:0 auto 14px}
.feat h4{font-size:1.06rem;margin-bottom:6px;color:var(--green)}
.feat p{color:#5a655d;font-size:.92rem}

/* gallery */
.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.gallery figure{position:relative;border-radius:13px;overflow:hidden;aspect-ratio:4/3}
.gallery img{width:100%;height:100%;object-fit:cover}
.gallery figcaption{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;font-size:.85rem;font-weight:700;color:#fff;
  background:linear-gradient(transparent,rgba(0,40,14,.8))}

/* ficha tecnica */
.ficha{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ficha .row{display:flex;justify-content:space-between;gap:10px;padding:14px 18px;background:#fff;border:1px solid var(--line);border-radius:12px}
.ficha .row span{color:var(--mute)} .ficha .row b{color:var(--green)}

/* finance band */
.band{display:grid;grid-template-columns:1.05fr .95fr;gap:42px;align-items:center;background:var(--orange);color:#fff;
  border-radius:22px;padding:40px}
.band h2{font-size:clamp(1.5rem,2.6vw,2rem);margin-bottom:10px}
.band p{color:#fff;opacity:.95;margin-bottom:20px}
.band__box{background:#fff;color:var(--ink);border-radius:16px;padding:24px}
.band__row{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--line)}
.band__row b{color:var(--green)} .band__note{font-size:.74rem;color:var(--mute);margin-top:10px}

/* localizacao */
.loc-grid{display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center}
.loc-list{list-style:none;padding:0}
.loc-list li{padding:9px 0 9px 30px;position:relative;border-bottom:1px dashed var(--line);color:#3a463f}
.loc-list li::before{content:"";position:absolute;left:4px;top:15px;width:9px;height:9px;border-radius:50%;background:var(--orange)}
.map{height:320px;border-radius:16px;background:linear-gradient(135deg,#dfeee2,#cfe6d6);position:relative;overflow:hidden;border:1px solid var(--line)}
.map__pin{position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);text-align:center}
.map__pin .dot{width:22px;height:22px;background:var(--orange);border:4px solid #fff;border-radius:50%;margin:0 auto 6px;box-shadow:0 4px 10px rgba(0,0,0,.25)}
.map__pin span{background:#fff;padding:4px 10px;border-radius:8px;font-weight:700;font-size:.85rem;box-shadow:0 4px 10px rgba(0,0,0,.12)}
.map__grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,67,16,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(0,67,16,.06) 1px,transparent 1px);background-size:40px 40px}

/* prova */
.quotes{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.quotes blockquote{background:#fff;border-top:4px solid var(--orange);border-radius:14px;padding:24px;font-size:1rem;box-shadow:0 8px 24px rgba(0,30,12,.06)}
.quotes .stars{color:var(--orange);margin-bottom:8px}
.quotes cite{display:block;margin-top:12px;font-style:normal;font-size:.82rem;color:var(--mute);font-weight:800}

/* corretor */
.corretor{display:flex;gap:20px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;max-width:620px;margin:0 auto}
.corretor img{width:84px;height:84px;border-radius:50%;object-fit:cover;border:3px solid var(--orange)}
.corretor h4{color:var(--green);font-size:1.15rem}
.corretor p{color:var(--mute);font-size:.9rem}

/* faq */
details{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:12px;background:#fff}
summary{font-weight:800;cursor:pointer;list-style:none;display:flex;justify-content:space-between;color:var(--green)}
summary::after{content:"+";color:var(--orange);font-size:1.3rem;font-weight:800}
details[open] summary::after{content:"–"}
details p{color:#5a655d;margin-top:10px}

/* cta final */
.ctaf{text-align:center}
.ctaf h2{font-size:clamp(1.7rem,3.2vw,2.5rem);margin-bottom:12px}
.ctaf p{color:#cfe6d6;margin-bottom:24px;font-size:1.08rem}

/* footer */
.foot{background:#00310c;color:#bcd3c2;padding:40px 0 24px;font-size:.9rem}
.foot__grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:30px;margin-bottom:24px}
.foot__logo{height:50px;margin-bottom:14px}
.foot a{color:#dfeee2;text-decoration:none}
.foot h5{color:#fff;font-size:1rem;margin-bottom:12px}
.foot__bottom{border-top:1px solid rgba(255,255,255,.12);padding-top:16px;color:#8fae97;font-size:.8rem;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}

/* whatsapp float */
.wa-float{position:fixed;right:20px;bottom:20px;z-index:60;width:62px;height:62px;border-radius:50%;background:var(--wa);
  display:flex;align-items:center;justify-content:center;box-shadow:0 12px 28px rgba(37,211,102,.5)}

@media(max-width:920px){
  .hero__grid,.band,.loc-grid{grid-template-columns:1fr;gap:28px}
  .feats{grid-template-columns:repeat(2,1fr)} .gallery{grid-template-columns:repeat(2,1fr)}
  .ficha{grid-template-columns:1fr 1fr} .quotes{grid-template-columns:1fr} .foot__grid{grid-template-columns:1fr}
  .top__phone{display:none}
}
"""

def page(p):
    g=lambda i:f"assets/{i}"
    feats="".join(f'<div class="feat"><div class="feat__ic">{ICONS.get(ic,"")}</div><h4>{t}</h4><p>{d}</p></div>'
                  for ic,t,d in p["feats"])
    gallery="".join(f'<figure><img src="{g(img)}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
                    for img,cap in p["gallery"])
    ficha="".join(f'<div class="row"><span>{k}</span><b>{v}</b></div>' for k,v in p["ficha"])
    specs="".join(f'<li><b>{b}</b><span>{s}</span></li>' for b,s in p["specs"])
    nearby="".join(f"<li>{x}</li>" for x in p["nearby"])
    quotes="".join(f'<blockquote><div class="stars">★★★★★</div>{q}<cite>{c}</cite></blockquote>'
                   for q,c in p["quotes"])
    faqs="".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in p["faq"])
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="theme-color" content="#004310">
<title>{p['titulo']} — {p['bairro']}, Cuiabá/MT | Aprovar Negócios Imobiliários</title>
<meta name="description" content="{p['titulo']} no {p['bairro']}, Cuiabá-MT. {p['preco_label']}. {p['sub']} Fale com a Aprovar pelo WhatsApp.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>

<header class="top"><div class="wrap top__in">
  <img class="top__logo" src="assets/logo-aprovar-branco.png" alt="Aprovar Negócios Imobiliários">
  <div class="top__right">
    <a class="top__phone" href="tel:+{PHONE_WA}">{PHONE_DISPLAY}<span>seg–sex 9h–18h · sáb 9h–13h</span></a>
    <a class="btn btn--wa" href="{wa(p['wa_top'])}" target="_blank" rel="noopener">WhatsApp</a>
  </div>
</div></header>

<section class="hero">
  <div class="hero__bg" style="background-image:url('assets/{p['hero']}')"></div>
  <div class="wrap hero__grid">
    <div>
      <span class="badge">{p['badge']}</span>
      <h1>{p['titulo']}</h1>
      <p class="loc"><span class="locpin"><svg viewBox="0 0 24 24" width="16" height="16" fill="#F57F17"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg></span> <b>{p['bairro']}</b> · Cuiabá/MT — {p['ref']}</p>
      <div class="price"><b>{p['preco']}</b><small>{p['preco_obs']}</small></div>
      <ul class="specs">{specs}</ul>
      <div class="hero__cta">
        <a class="btn btn--orange btn--lg" href="{wa(p['wa_hero'])}" target="_blank" rel="noopener">{p['cta_hero']}</a>
        <a class="btn btn--ghost btn--lg" href="#financiamento">Simular financiamento</a>
      </div>
      <p class="microtrust">★★★★★ Atendimento no mesmo dia · CRECI 9770J · Aprovar Negócios Imobiliários</p>
    </div>
    <aside class="card">
      <h3>Agende sua visita</h3>
      <p class="sub">Preencha e fale agora com um corretor pelo WhatsApp.</p>
      <form onsubmit="return false">
        <label>Nome<input type="text" placeholder="Seu nome completo"></label>
        <label>WhatsApp<input type="tel" placeholder="(65) 90000-0000"></label>
        <label>Você procura para
          <select><option>Morar</option><option>Investir</option></select></label>
        <label>Como pretende comprar
          <select><option>Financiamento</option><option>À vista</option><option>Ainda não sei</option></select></label>
        <a class="btn btn--wa btn--block btn--lg" href="{wa(p['wa_form'])}" target="_blank" rel="noopener">Quero falar no WhatsApp</a>
        <p class="priv">🔒 Seus dados são tratados com segurança pela Aprovar.</p>
      </form>
    </aside>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head"><span class="sec__kick">Por que esse imóvel</span>
      <h2 class="sec__title">{p['feats_title']}</h2></div>
    <div class="feats">{feats}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="wrap">
    <div class="sec__head"><span class="sec__kick">Conheça por dentro</span>
      <h2 class="sec__title">Galeria do imóvel</h2></div>
    <div class="gallery">{gallery}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head"><span class="sec__kick">Ficha técnica</span>
      <h2 class="sec__title">Tudo o que você precisa saber</h2></div>
    <div class="ficha">{ficha}</div>
  </div>
</section>

<section class="sec" id="financiamento">
  <div class="wrap"><div class="band">
    <div>
      <h2>{p['fin_title']}</h2>
      <p>{p['fin_sub']}</p>
      <a class="btn btn--orange btn--lg" href="{wa(p['wa_fin'])}" target="_blank" rel="noopener" style="background:#fff;color:var(--orange-d)">Quero minha simulação grátis</a>
    </div>
    <div class="band__box">
      <div class="band__row"><span>Valor do imóvel</span><b>{p['preco']}</b></div>
      <div class="band__row"><span>{p['fin_l1']}</span><b>{p['fin_v1']}</b></div>
      <div class="band__row"><span>{p['fin_l2']}</span><b>{p['fin_v2']}</b></div>
      <p class="band__note">*Valores ilustrativos, sujeitos à análise de crédito da instituição financeira.</p>
    </div>
  </div></div>
</section>

<section class="sec sec--soft">
  <div class="wrap">
    <div class="sec__head"><span class="sec__kick">Localização</span>
      <h2 class="sec__title">No coração do {p['bairro']}</h2></div>
    <div class="loc-grid">
      <ul class="loc-list">{nearby}</ul>
      <div class="map"><div class="map__grid"></div><div class="map__pin"><div class="dot"></div><span>{p['titulo']}</span></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head"><span class="sec__kick">Quem comprou com a Aprovar</span>
      <h2 class="sec__title">Histórias de quem realizou o sonho</h2></div>
    <div class="quotes">{quotes}</div>
  </div>
</section>

<section class="sec sec--soft">
  <div class="wrap">
    <div class="corretor">
      <img src="assets/{p['corretor_img']}" alt="Corretor Aprovar">
      <div>
        <h4>{p['corretor_nome']} — Aprovar Negócios Imobiliários</h4>
        <p>{p['corretor_desc']}<br>CRECI 9770J · {PHONE_DISPLAY}</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--narrow">
    <div class="sec__head"><span class="sec__kick">Dúvidas</span>
      <h2 class="sec__title">Perguntas frequentes</h2></div>
    {faqs}
  </div>
</section>

<section class="sec sec--green">
  <div class="wrap ctaf">
    <h2>Vamos agendar a sua visita?</h2>
    <p>Em poucos minutos no WhatsApp você descobre a parcela e marca o melhor horário.</p>
    <a class="btn btn--orange btn--lg" href="{wa(p['wa_final'])}" target="_blank" rel="noopener">Falar no WhatsApp agora</a>
  </div>
</section>

<footer class="foot"><div class="wrap">
  <div class="foot__grid">
    <div>
      <img class="foot__logo" src="assets/logo-aprovar-branco.png" alt="Aprovar">
      <p>Os melhores imóveis de Cuiabá e região. Compra, venda, avaliação e administração de imóveis.</p>
    </div>
    <div><h5>Contato</h5>
      <p>WhatsApp/Tel: <a href="tel:+{PHONE_WA}">{PHONE_DISPLAY}</a><br>
      Av. Gov. Dante Martins de Oliveira, Qd 02, 01<br>Carumbé — Cuiabá/MT</p></div>
    <div><h5>Horário</h5><p>Seg a Sex: 9h às 18h<br>Sábado: 9h às 13h</p>
      <p style="margin-top:10px"><b style="color:#fff">CRECI 9770J</b></p></div>
  </div>
  <div class="foot__bottom">
    <span>© Aprovar Negócios Imobiliários — Cuiabá/MT</span>
    <span>Imagens meramente ilustrativas. Valores sujeitos a alteração e análise de crédito.</span>
  </div>
</div></footer>

<a class="wa-float" href="{wa(p['wa_top'])}" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 32 32" width="32" height="32" fill="#fff"><path d="M16 3C9.4 3 4 8.4 4 15c0 2.1.6 4.2 1.6 6L4 29l8.2-1.6c1.7.9 3.7 1.4 5.8 1.4 6.6 0 12-5.4 12-12S22.6 3 16 3zm0 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-4.9 1 1-4.7-.3-.5c-1-1.6-1.5-3.4-1.5-5.3C4.9 9.4 9.9 4.9 16 4.9S27.1 9.4 27.1 15 22.1 24.8 16 24.8zm5.7-7.3c-.3-.2-1.8-.9-2.1-1-.3-.1-.5-.2-.7.2s-.8 1-1 1.2c-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.5-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.2-1.2 2.9s1.2 3.4 1.4 3.6c.2.2 2.4 3.7 5.9 5.1.8.4 1.5.6 2 .7.8.3 1.6.2 2.2.1.7-.1 1.8-.7 2.1-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>
</a>
</body></html>"""

# ============== IMÓVEL 1 — médio/alto padrão ==============
P1=dict(
 slug="apartamento-jardim-italia",
 titulo="Residencial Cuiabá Park — 3 quartos com lazer completo",
 bairro="Jardim Itália", ref="próximo à Av. Miguel Sutil e Shopping Estação",
 badge="Pronto pra morar · Cód. AP-1042",
 preco="R$ 539.000", preco_obs="ou entrada + financiamento Caixa",
 preco_label="A partir de R$ 539.000",
 sub="3 quartos (1 suíte), 78m², 2 vagas e lazer completo.",
 hero="luxo.jpg",
 specs=[("78 m²","área privativa"),("3","quartos · 1 suíte"),("2","vagas"),("Lazer","completo")],
 cta_hero="Quero agendar minha visita",
 feats_title="Conforto, localização e um bom negócio",
 feats=[("key","Pronto pra morar","Sem obra, sem espera. Recebeu a chave, mudou."),
        ("bank","Financia pela Caixa","Use o financiamento com as menores taxas e o FGTS na entrada."),
        ("pool","Lazer de clube","Piscina, academia, salão de festas, playground e espaço gourmet."),
        ("pin","Bem localizado","No Jardim Itália, perto de tudo: shopping, escolas e a Av. Miguel Sutil.")],
 gallery=[("interior.jpg","Living integrado"),("cozinha.jpg","Cozinha planejada"),("quarto.jpg","Suíte master"),
          ("varanda.jpg","Varanda"),("piscina.jpg","Piscina e lazer"),("luxo.jpg","Acabamento de alto padrão")],
 ficha=[("Tipo","Apartamento"),("Dormitórios","3 (1 suíte)"),("Banheiros","2"),
        ("Vagas","2 cobertas"),("Área privativa","78 m²"),("Andar","médio/alto"),
        ("Situação","Pronto pra morar"),("Lazer","Piscina, academia, salão"),("Cód.","AP-1042")],
 fin_title="A parcela pode caber no seu orçamento", fin_sub="Faça uma simulação gratuita e descubra em 2 minutos sua parcela — com FGTS na entrada e financiamento pela Caixa.",
 fin_l1="Entrada (com FGTS)*", fin_v1="a partir de R$ 0", fin_l2="Parcela estimada*", fin_v2="sob simulação",
 nearby=["Shopping Estação Cuiabá — 5 min","Av. Miguel Sutil — 3 min","Escolas e faculdades — 5 min",
         "Supermercados e farmácias — 2 min","Parque das Águas — 8 min","Aeroporto Marechal Rondon — 18 min"],
 quotes=[("“Atendimento da Aprovar foi rápido e sem enrolação. Visitei no mesmo dia.”","— Renata, Cuiabá/MT"),
         ("“Consegui financiar pela Caixa e usar o FGTS. Equipe me ajudou em tudo.”","— Anderson, Várzea Grande/MT"),
         ("“Apartamento exatamente como nos anúncios. Recomendo a Aprovar.”","— Patrícia, Cuiabá/MT")],
 corretor_img="logo-aprovar-redondo.png", corretor_nome="Equipe Aprovar",
 corretor_desc="Especialistas no mercado de Cuiabá e região, prontos pra te atender.",
 faq=[("Preciso de entrada?","Em muitos casos o FGTS cobre parte ou toda a entrada. Fazemos a simulação e mostramos a melhor condição."),
      ("Posso usar o FGTS?","Sim, com 3 anos de carteira (somados) e sem imóvel registrado. Confirmamos isso na conversa."),
      ("O imóvel está pronto?","Sim, pronto pra morar. Você visita e, aprovado o financiamento, recebe a chave."),
      ("Como agendo a visita?","Pelo WhatsApp, no horário que for melhor pra você — muitas vezes no mesmo dia.")],
 wa_top="Olá! Vim pelo site e quero saber mais sobre o Residencial Cuiabá Park (AP-1042), no Jardim Itália.",
 wa_hero="Olá! Quero agendar uma visita ao apê de 3 quartos no Jardim Itália (AP-1042) e simular o financiamento.",
 wa_form="Olá! Vim pelo formulário do site. Tenho interesse no apê AP-1042 (Jardim Itália).",
 wa_fin="Olá! Quero simular o financiamento do apê AP-1042 (Jardim Itália). Pode me ajudar?",
 wa_final="Olá! Quero agendar uma visita ao Residencial Cuiabá Park (AP-1042)."
)

# ============== IMÓVEL 2 — primeiro imóvel / MCMV ==============
P2=dict(
 slug="apartamento-pedra-90",
 titulo="Residencial Bem Viver — seu primeiro apê em Cuiabá",
 bairro="Pedra 90", ref="região do Coxipó, fácil acesso ao Centro",
 badge="Minha Casa Minha Vida · Cód. AP-2087",
 preco="R$ 219.000", preco_obs="entrada facilitada + subsídio MCMV",
 preco_label="A partir de R$ 219.000",
 sub="2 quartos, 48m², 1 vaga. Parcelas a partir de R$ 1.100.",
 hero="mcmv.jpg",
 specs=[("48 m²","área privativa"),("2","quartos"),("1","vaga"),("~R$1.100","parcela*")],
 cta_hero="Quero sair do aluguel",
 feats_title="O empurrão que faltava pra sair do aluguel",
 feats=[("money","Subsídio do governo","Pelo Minha Casa Minha Vida, você pode receber subsídio e reduzir a parcela."),
        ("bank","Use o FGTS","Tem 3 anos de carteira? Pode usar o FGTS como entrada."),
        ("chart","Parcela de aluguel","A partir de ~R$ 1.100/mês — parecida com o aluguel que você já paga."),
        ("key","Pronto pra morar","Apartamento novo, é só levar a mudança.")],
 gallery=[("interior.jpg","Sala"),("cozinha.jpg","Cozinha"),("quarto.jpg","Quarto"),
          ("varanda.jpg","Área externa"),("piscina.jpg","Lazer do condomínio"),("chaves.jpg","Chave na mão")],
 ficha=[("Tipo","Apartamento (MCMV)"),("Dormitórios","2"),("Banheiros","1"),
        ("Vagas","1"),("Área privativa","48 m²"),("Entrada","facilitada / subsídio"),
        ("Parcela*","a partir de ~R$ 1.100"),("Situação","Pronto pra morar"),("Cód.","AP-2087")],
 fin_title="Saia do aluguel ainda este ano", fin_sub="Simule grátis e veja como o subsídio do MCMV e o FGTS deixam a parcela parecida com um aluguel.",
 fin_l1="Entrada (com FGTS/subsídio)*", fin_v1="a partir de R$ 0", fin_l2="Parcela estimada*", fin_v2="a partir de ~R$ 1.100",
 nearby=["Acesso à Av. das Torres — 6 min","Terminal Pedra 90 — 4 min","Escolas e creches — 3 min",
         "UPA e postos de saúde — 5 min","Mercados e comércio — 2 min","Centro de Cuiabá — 20 min"],
 quotes=[("“Achei que nunca sairia do aluguel. Em poucos dias o financiamento foi aprovado.”","— Jéssica, Cuiabá/MT"),
         ("“Usei meu FGTS de entrada e a parcela ficou igual ao aluguel. Valeu demais!”","— Marcos, Cuiabá/MT"),
         ("“A Aprovar explicou tudo com paciência. Hoje moro no que é meu.”","— Cleia, Cuiabá/MT")],
 corretor_img="logo-aprovar-redondo.png", corretor_nome="Equipe Aprovar",
 corretor_desc="Te ajudamos do primeiro contato à entrega das chaves.",
 faq=[("Quem pode usar o Minha Casa Minha Vida?","Famílias dentro das faixas de renda do programa. A gente verifica seu enquadramento na conversa."),
      ("Preciso de entrada?","Com subsídio e FGTS, muitas vezes a entrada fica próxima de zero. Simulamos pra você."),
      ("A parcela cabe no meu bolso?","O objetivo é deixar a parcela parecida com um aluguel. Fazemos a simulação na hora."),
      ("Como começo?","É só chamar no WhatsApp. Pedimos alguns dados e já fazemos a simulação.")],
 wa_top="Olá! Vim pelo site e quero saber mais sobre o Residencial Bem Viver (AP-2087), na Pedra 90.",
 wa_hero="Olá! Quero sair do aluguel! Tenho interesse no apê MCMV AP-2087 (Pedra 90). Pode simular pra mim?",
 wa_form="Olá! Vim pelo formulário do site. Tenho interesse no apê AP-2087 (Pedra 90, MCMV).",
 wa_fin="Olá! Quero simular o financiamento MCMV do apê AP-2087 (Pedra 90).",
 wa_final="Olá! Quero agendar uma visita ao Residencial Bem Viver (AP-2087)."
)

for P in (P1,P2):
    open(os.path.join(LAND,P["slug"]+".html"),"w",encoding="utf-8").write(page(P))
    print("gerada:",P["slug"]+".html")
print("DONE")

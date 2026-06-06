/* =====================================================================
   Imóveis AQV — Landing de captação
   CONFIGURE AQUI antes de publicar:
   ===================================================================== */
const CONFIG = {
  phone: "5582990000000",                 // DDI + DDD + número (só dígitos)
  formEndpoint: "",                       // URL do seu CRM/webhook (POST). Vazio = só WhatsApp.
  redirectToWhatsAppAfterForm: true       // após enviar o form, abre o WhatsApp
};

/* ---- 1. Captura de UTMs e dados de origem (atribuição) ---- */
function getTracking() {
  const p = new URLSearchParams(location.search);
  const keys = ["utm_source","utm_medium","utm_campaign","utm_content","utm_term","fbclid","gclid"];
  const t = {};
  keys.forEach(k => { const v = p.get(k); if (v) t[k] = v; });
  t.page = location.href;
  t.referrer = document.referrer || "";
  return t;
}
const TRACKING = getTracking();

/* ---- 2. Monta o link do WhatsApp com mensagem + origem ---- */
function waLink(message) {
  const src = TRACKING.utm_source ? ` (origem: ${TRACKING.utm_source}/${TRACKING.utm_campaign || "-"})` : "";
  const text = encodeURIComponent((message || "Olá! Vim pelo site.") + src);
  return `https://wa.me/${CONFIG.phone}?text=${text}`;
}

/* ---- 3. Liga todos os botões [data-wa] ---- */
document.querySelectorAll("[data-wa]").forEach(el => {
  el.setAttribute("href", waLink(el.dataset.msg));
  el.setAttribute("target", "_blank");
  el.setAttribute("rel", "noopener");
  el.addEventListener("click", () => track("click_whatsapp", { msg: el.dataset.msg }));
});

/* ---- 4. Formulário: valida, envia ao CRM e abre o WhatsApp ---- */
const form = document.getElementById("leadForm");
const formErr = document.getElementById("formErr");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  // validação simples
  let ok = true;
  form.querySelectorAll("[required]").forEach(f => {
    const bad = !f.value.trim();
    f.classList.toggle("invalid", bad);
    if (bad) ok = false;
  });
  formErr.hidden = ok;
  if (!ok) return;

  const payload = { ...data, ...TRACKING, ts: new Date().toISOString() };

  // envia ao CRM/webhook (se configurado)
  if (CONFIG.formEndpoint) {
    try {
      await fetch(CONFIG.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    } catch (err) { console.warn("Falha ao enviar lead ao CRM:", err); }
  }

  track("lead_submit", { intencao: data.intencao, pagamento: data.pagamento });

  // mensagem personalizada para o WhatsApp
  const msg = `Oi! Sou ${data.nome}. Quero ${data.intencao === "Investir" ? "investir" : "morar"} `
    + `no apê do [Bairro]. Pretendo comprar via ${data.pagamento}. Meu WhatsApp: ${data.telefone}.`;

  if (CONFIG.redirectToWhatsAppAfterForm) {
    window.open(waLink(msg), "_blank", "noopener");
  }
  form.reset();
  form.querySelector("button").textContent = "✓ Enviado! Abrindo o WhatsApp…";
});

/* ---- 5. Disparo de eventos para Pixel/GA (se existirem) ---- */
function track(event, params = {}) {
  if (window.fbq) fbq("trackCustom", event, params);          // Meta Pixel
  if (window.gtag) gtag("event", event, params);              // GA4 / Google Ads
  if (window.dataLayer) window.dataLayer.push({ event, ...params });
}
/* dispara visualização qualificada após 15s na página (sinal de intenção) */
setTimeout(() => track("engaged_15s", {}), 15000);

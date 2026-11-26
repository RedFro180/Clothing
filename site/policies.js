// Fills the policies page from config.js. Text only (textContent), so nothing in config can inject HTML.
(() => {
  const C = window.SITE_CONFIG || {};
  const val = k => (typeof C[k] === "string" ? C[k].trim() : "");
  const money = n => new Intl.NumberFormat("en-US", { style: "currency", currency: C.CURRENCY || "USD", maximumFractionDigits: 0 }).format(n);
  document.querySelectorAll("[data-brand]").forEach(e => { e.textContent = C.BRAND || "Brand"; });
  document.title = `Policies | ${C.BRAND || "Brand"}`;
  document.querySelectorAll("[data-c]").forEach(e => { e.textContent = val(e.dataset.c) || e.dataset.fallback || ""; });
  const email = val("CONTACT_EMAIL");
  document.querySelectorAll("[data-contact]").forEach(a => {
    a.textContent = email || "(email to be set)";
    if (/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email)) a.href = "mailto:" + email;
  });
  const f = Number(C.SHIPPING_FLAT) || 0, o = Number(C.FREE_SHIP_OVER) || 0, q = Number(C.FREE_SHIP_QTY) || 0;
  const line = !f ? "free" : o ? `${money(f)} per order, free on orders of ${money(o)} or more` : q ? `${money(f)} per order, free on ${q}+ items` : `${money(f)} per order`;
  document.querySelectorAll("[data-ship-line]").forEach(e => { e.textContent = line; });
})();

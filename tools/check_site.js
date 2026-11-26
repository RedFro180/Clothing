// Safety check for the website. Run before publishing:  node tools/check_site.js
// Catches the mistakes that break a live shop: a typo in config.js, a sold-out design number that
// doesn't exist, a missing image, a negative price, an http link, a missing security header.
// Exit code 0 = safe to publish, 1 = fix the errors listed.
const fs = require("fs"), path = require("path"), vm = require("vm");
const SITE = path.join(__dirname, "..", "site");
const errors = [], warnings = [];
const err = m => errors.push(m), warn = m => warnings.push(m);

function load(file, global) {
  const box = { window: {} };
  try { vm.runInNewContext(fs.readFileSync(path.join(SITE, file), "utf8"), box, { filename: file }); }
  catch (e) { err(`${file} has a typo and would break the whole site: ${e.message}`); return null; }
  return box.window[global];
}
const C = load("config.js", "SITE_CONFIG"), CAT = load("products.js", "CATALOG");

if (C) {
  const str = k => typeof C[k] === "string", num = k => typeof C[k] === "number" && isFinite(C[k]);
  for (const k of ["BRAND", "TAGLINE", "FEATURED_LABEL", "CONTACT_EMAIL", "CURRENCY"]) if (!str(k)) err(`config.js: ${k} must be text in quotes.`);
  if (str("BRAND") && C.BRAND === "Brand Name") warn("config.js: BRAND is still the placeholder \"Brand Name\".");
  if (str("CONTACT_EMAIL") && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(C.CONTACT_EMAIL)) err("config.js: CONTACT_EMAIL is not a valid email.");
  if (str("CONTACT_EMAIL") && /example\.com$/.test(C.CONTACT_EMAIL)) warn("config.js: CONTACT_EMAIL is still the example address.");
  if (C.FEATURED_LABEL && /best ?sell/i.test(C.FEATURED_LABEL)) warn("config.js: FEATURED_LABEL says best seller. Only use that once real sales back it up.");
  for (const k of ["SHIPPING_FLAT", "FREE_SHIP_QTY", "MAX_QTY_PER_ITEM", "MAX_ITEMS_PER_ORDER", "LARGE_ORDER_ITEMS", "HERO_SPEED"])
    if (!num(k) || C[k] < 0) err(`config.js: ${k} must be a number of 0 or more (no quotes).`);
  if (num("MAX_QTY_PER_ITEM") && C.MAX_QTY_PER_ITEM < 1) err("config.js: MAX_QTY_PER_ITEM must be at least 1.");
  if (num("MAX_ITEMS_PER_ORDER") && num("LARGE_ORDER_ITEMS") && C.LARGE_ORDER_ITEMS > C.MAX_ITEMS_PER_ORDER) warn("config.js: LARGE_ORDER_ITEMS is above MAX_ITEMS_PER_ORDER, so the large-order flag never shows.");
  for (const k of ["FORM_ENDPOINT", "INSTAGRAM", "TIKTOK", "POSTHOG_HOST"]) if (C[k] && !/^https:\/\/\S+$/.test(C[k])) err(`config.js: ${k} must start with https://`);
  if (!C.FORM_ENDPOINT) warn("config.js: FORM_ENDPOINT is empty, so orders open the shopper's email app (many won't finish).");
  if (C.POSTHOG_KEY && !/^phc_[A-Za-z0-9]+$/.test(C.POSTHOG_KEY)) err("config.js: POSTHOG_KEY should look like phc_ followed by letters/numbers.");
  if (C.SMS_ENABLED && !C.FORM_ENDPOINT) warn("config.js: SMS_ENABLED is on but there's no FORM_ENDPOINT to receive the phone numbers.");
  if (!Array.isArray(C.SIZE_CHART)) err("config.js: SIZE_CHART must be a list.");
  else if (!C.SIZE_CHART.some(r => r.chest || r.length || r.sleeve)) warn("config.js: SIZE_CHART has no measurements yet (all sales are final, so add them).");
  if (C.SIZE_CHARTS !== undefined) {
    if (typeof C.SIZE_CHARTS !== "object" || Array.isArray(C.SIZE_CHARTS)) err("config.js: SIZE_CHARTS must look like { tee: [...], underwear: [...], socks: [...] }.");
    else for (const [t, rows] of Object.entries(C.SIZE_CHARTS)) {
      if (!Array.isArray(rows)) err(`config.js SIZE_CHARTS.${t} must be a list.`);
      else if (!rows.some(r => Object.entries(r).some(([k, v]) => k !== "size" && v))) warn(`config.js: SIZE_CHARTS.${t} has no measurements yet.`);
    }
  }
  const headers = fs.existsSync(path.join(SITE, "_headers")) ? fs.readFileSync(path.join(SITE, "_headers"), "utf8") : "";
  if (!headers.includes("Content-Security-Policy")) err("site/_headers is missing the security policy.");
  if (C.FORM_ENDPOINT && headers) {
    const host = new URL(C.FORM_ENDPOINT).origin;
    if (!headers.includes(host)) err(`site/_headers: add ${host} to connect-src and form-action, or orders will be blocked.`);
  }
  if (C.POSTHOG_HOST && headers && !headers.includes(new URL(C.POSTHOG_HOST).origin)) err(`site/_headers: add ${new URL(C.POSTHOG_HOST).origin} to connect-src.`);
}

if (CAT) {
  const ids = new Set(CAT.products.map(p => p.id));
  for (const p of CAT.products) {
    if (!(p.price > 0)) err(`products.js: #${p.id} has a bad price.`);
    for (const im of [p.img, ...(p.imgs || []).map(i => i.src)])
      if (!fs.existsSync(path.join(SITE, im))) err(`Missing picture for #${p.id}: site/${im}`);
  }
  for (const t of (CAT.types || []).filter(t => t.live)) {
    const pr = [...new Set(CAT.products.filter(p => p.type === t.id).map(p => p.price))];
    if (!pr.length) warn(`${t.label} is marked live but has no products.`);
    if (pr.length > 1) warn(`${t.label} have different prices (${pr.join(", ")}), so prices show under each item instead of once.`);
  }
  if ((CAT.products || []).some(p => !p.imgs || p.imgs.length < 4)) err("products.js: some products have fewer than 4 pictures.");
  if (!CAT.products.some(p => p.featured)) warn("No featured hoodies: the spinning ring will be empty.");
  if (C && C.SOLD_OUT) {
    if (typeof C.SOLD_OUT !== "object" || Array.isArray(C.SOLD_OUT)) err("config.js: SOLD_OUT must look like { 11: [\"S\", \"XL\"] }.");
    else for (const [k, v] of Object.entries(C.SOLD_OUT)) {
      if (!ids.has(Number(k))) err(`config.js SOLD_OUT: design ${k} doesn't exist.`);
      const p = CAT.products.find(x => x.id === Number(k));
      if (!Array.isArray(v)) err(`config.js SOLD_OUT ${k}: sizes must be a list like ["S", "M"].`);
      else if (p) for (const s of v) if (!p.sizes.includes(s)) err(`config.js SOLD_OUT ${k}: "${s}" is not a size (use ${p.sizes.join(", ")}).`);
      if (p && Array.isArray(v) && v.length === p.sizes.length) warn(`Design ${k} is sold out in every size.`);
    }
  }
}
for (const f of ["index.html", "app.js", "style.css", "analytics.js", "fog.js", "icon.svg", "share.png"])
  if (!fs.existsSync(path.join(SITE, f))) err(`Missing file: site/${f}`);
const html = fs.existsSync(path.join(SITE, "index.html")) ? fs.readFileSync(path.join(SITE, "index.html"), "utf8") : "";
if (/\son[a-z]+="/i.test(html)) err("index.html has an inline on...= handler; the security policy will block it. Move it into app.js.");
if (/<script>(?!\s*<\/script>)/.test(html)) err("index.html has an inline <script>; the security policy will block it.");

for (const w of warnings) console.log("  warning: " + w);
for (const e of errors) console.log("  ERROR:   " + e);
console.log(errors.length ? `\nNOT SAFE to publish: ${errors.length} error(s).` : `\nSafe to publish. (${warnings.length} warning(s) to look at.)`);
process.exit(errors.length ? 1 : 0);

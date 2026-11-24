(() => {
  "use strict";
  const C = window.SITE_CONFIG, CAT = window.CATALOG, P = CAT.products;
  const $ = (s, r = document) => r.querySelector(s);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") n.className = v; else if (k === "text") n.textContent = v;
      else if (k.startsWith("on")) n.addEventListener(k.slice(2), v); else if (v !== false && v != null) n.setAttribute(k, v);
    }
    kids.flat().forEach(c => c != null && n.append(c));
    return n;
  };
  const money = n => new Intl.NumberFormat("en-US", { style: "currency", currency: C.CURRENCY, maximumFractionDigits: 0 }).format(n);
  const byId = Object.fromEntries(P.map(p => [p.id, p]));
  const bySlug = Object.fromEntries(P.map(p => [p.slug, p]));

  // ---------- branding ----------
  document.title = `${C.BRAND} | Dark-humor hoodies, no plastic`;
  document.querySelectorAll("[data-brand]").forEach(n => n.textContent = C.BRAND);
  $("[data-tagline]").textContent = C.TAGLINE;
  $("[data-featured-label]").textContent = C.FEATURED_LABEL;
  $("#year").textContent = new Date().getFullYear();

  // ---------- cards ----------
  function card(p) {
    return el("button", { class: "card", type: "button", "aria-label": `${p.name}, ${p.color}, ${money(p.price)}`, onclick: () => openProduct(p) },
      el("div", { class: "tile" + (p.light ? " dark" : "") },
        el("img", { src: p.img, alt: `${p.color} hoodie, ${p.placement.toLowerCase()}: ${p.name}`, loading: "lazy", width: 560, height: 570 }),
        p.featured ? el("span", { class: "badge", text: C.FEATURED_LABEL }) : null,
        el("span", { class: "place", text: p.placement.replace(" print", "") })),
      el("h3", { text: p.name }),
      el("div", { class: "row" },
        el("span", {}, el("span", { class: "swatch", style: `background:${p.hex}` }), p.color),
        el("span", { class: "price", text: money(p.price) })));
  }

  // ---------- featured row ----------
  const feat = P.filter(p => p.featured).sort((a, b) => a.featured - b.featured);
  $("#featRow").append(...feat.map(card));
  document.querySelectorAll("[data-scroll]").forEach(b => b.addEventListener("click", () => {
    const row = $("#featRow"); row.scrollBy({ left: Number(b.dataset.scroll) * row.clientWidth * 0.8, behavior: "smooth" });
  }));

  // ---------- filters ----------
  const fCat = $("#fCat"), fTheme = $("#fTheme"), fColor = $("#fColor"), fSort = $("#fSort"), fSearch = $("#fSearch");
  const countType = id => P.filter(p => p.type === id).length;
  fCat.append(el("option", { value: "", text: `All products (${P.length})` }),
    ...CAT.types.map(t => el("option", { value: t.id, text: t.live ? `${t.label} (${countType(t.id)})` : `${t.label} (coming soon)` })));
  fTheme.append(el("option", { value: "", text: "All themes" }),
    ...Object.entries(CAT.themes).map(([k, v]) => el("option", { value: k, text: `${v} (${P.filter(p => p.theme === k).length})` })));
  const colors = [...new Set(P.map(p => p.color))].sort();
  fColor.append(el("option", { value: "", text: "All colors" }), ...colors.map(c => el("option", { value: c, text: c })));

  // read filters from the URL so filtered views can be shared
  const q = new URLSearchParams(location.search);
  const setIf = (sel, v) => { if (v && [...sel.options].some(o => o.value === v)) sel.value = v; };
  setIf(fCat, q.get("cat")); setIf(fTheme, q.get("theme")); setIf(fColor, q.get("color")); setIf(fSort, q.get("sort"));
  fSearch.value = q.get("q") || "";

  function writeURL() {
    const u = new URLSearchParams();
    if (fCat.value) u.set("cat", fCat.value); if (fTheme.value) u.set("theme", fTheme.value);
    if (fColor.value) u.set("color", fColor.value); if (fSort.value !== "featured") u.set("sort", fSort.value);
    if (fSearch.value.trim()) u.set("q", fSearch.value.trim());
    const s = u.toString();
    history.replaceState(null, "", location.pathname + (s ? "?" + s : "") + location.hash);
  }

  function render() {
    const grid = $("#grid"); grid.replaceChildren();
    const type = CAT.types.find(t => t.id === fCat.value);
    const any = fCat.value || fTheme.value || fColor.value || fSearch.value.trim();
    $("#clearBtn").hidden = !any;
    if (type && !type.live) {
      $("#resultCount").textContent = `${type.label}: coming soon`;
      grid.append(soonCard(type));
      writeURL(); return;
    }
    const words = fSearch.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let list = P.filter(p =>
      (!fCat.value || p.type === fCat.value) && (!fTheme.value || p.theme === fTheme.value) &&
      (!fColor.value || p.color === fColor.value) &&
      words.every(w => `${p.name} ${p.sub} ${p.color} ${CAT.themes[p.theme]} ${p.placement}`.toLowerCase().includes(w)));
    if (fSort.value === "az") list.sort((a, b) => a.name.localeCompare(b.name));
    else if (fSort.value === "new") list.sort((a, b) => b.id - a.id);
    else list.sort((a, b) => (a.featured || 999) - (b.featured || 999) || a.id - b.id);
    $("#resultCount").textContent = `${list.length} ${list.length === 1 ? "hoodie" : "hoodies"}`;
    if (!list.length) grid.append(el("p", { class: "empty", text: "Nothing matches. Try fewer filters." }));
    else grid.append(...list.map(card));
    writeURL();
  }

  function soonCard(t) {
    const msg = el("p", { class: "pd-msg", role: "status" });
    const email = el("input", { type: "email", required: true, placeholder: "you@email.com", "aria-label": "Email" });
    return el("div", { class: "soon" },
      el("h3", { text: `${t.label} are coming` }),
      el("p", { text: `Same rules as the hoodies: natural fiber, no plastic. Planned price around ${money(t.price)}. Leave your email and you'll hear first.` }),
      el("form", { onsubmit: e => { e.preventDefault(); send({ type: "notify", product: t.label, email: email.value }, msg); } },
        email, el("button", { class: "btn", type: "submit", text: "Notify me" })), msg);
  }

  [fCat, fTheme, fColor, fSort].forEach(s => s.addEventListener("change", render));
  let t; fSearch.addEventListener("input", () => { clearTimeout(t); t = setTimeout(render, 150); });
  $("#clearBtn").addEventListener("click", () => { fCat.value = fTheme.value = fColor.value = ""; fSearch.value = ""; render(); });

  // ---------- product dialog ----------
  const pd = $("#pd"); let cur = null, size = null;
  function openProduct(p, push = true) {
    cur = p; size = null;
    $("#pdImg").src = p.img; $("#pdImg").alt = `${p.color} hoodie, ${p.placement.toLowerCase()}: ${p.name}`;
    $("#pdImgWrap").className = "pd-img" + (p.light ? " dark" : "");
    $("#pdMeta").textContent = `${CAT.themes[p.theme]} · ${p.placement}`;
    $("#pdName").textContent = p.name; $("#pdSub").textContent = p.sub || "";
    $("#pdPrice").textContent = money(p.price);
    $("#pdQty").value = 1; $("#pdMsg").textContent = "";
    $("#pdSizes").replaceChildren(...p.sizes.map(s => el("button", { type: "button", "aria-pressed": "false", text: s,
      onclick: e => { size = s; $("#pdSizes").querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === e.currentTarget)); $("#pdMsg").textContent = ""; } })));
    $("#pdDetails").replaceChildren(...[
      `Color: ${p.colorNote}`, "~30% hemp / 70% cotton brushed fleece, heavyweight",
      "Cotton rib, thread, drawcord and labels. No plastic.", `${p.placement}, natural-dye or embroidered`,
      "Natural dyes fade gradually with sun and washing", "Preorder: no charge until we confirm a ship date",
    ].map(s => el("li", { text: s })));
    if (push) history.replaceState(null, "", location.pathname + location.search + "#" + p.slug);
    if (!pd.open) pd.showModal();
  }
  pd.addEventListener("close", () => { if (bySlug[location.hash.slice(1)]) history.replaceState(null, "", location.pathname + location.search); });
  $("#pdAdd").addEventListener("click", () => {
    if (!size) { $("#pdMsg").textContent = "Pick a size first."; return; }
    const n = Math.max(1, Math.min(20, parseInt($("#pdQty").value, 10) || 1));
    addToBag(cur.id, size, n);
    $("#pdMsg").textContent = `Added ${n} × ${size}. `;
    $("#pdMsg").append(el("button", { class: "link", type: "button", text: "View list", onclick: () => { pd.close(); openBag(); } }));
  });
  $("#pdShare").addEventListener("click", async () => {
    const url = location.origin + location.pathname + "#" + cur.slug;
    try { await navigator.clipboard.writeText(url); $("#pdMsg").textContent = "Link copied."; }
    catch { $("#pdMsg").textContent = url; }
  });
  function fromHash() {
    const p = bySlug[decodeURIComponent(location.hash.slice(1))];
    if (p) openProduct(p, false);
  }
  window.addEventListener("hashchange", fromHash);

  // close any dialog on backdrop click or close button
  document.querySelectorAll("dialog").forEach(d => {
    d.addEventListener("click", e => { if (e.target === d) d.close(); });
    d.querySelectorAll("[data-close]").forEach(b => b.addEventListener("click", () => d.close()));
  });

  // ---------- preorder list (saved in this browser) ----------
  const KEY = "preorder-list-v1";
  let bag = [];
  try { bag = JSON.parse(localStorage.getItem(KEY)) || []; } catch { bag = []; }
  bag = bag.filter(i => byId[i.id]);
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(bag)); } catch {} updateCount(); };
  const updateCount = () => { $("#bagCount").textContent = bag.reduce((s, i) => s + i.qty, 0); };
  function addToBag(id, sz, n) {
    const hit = bag.find(i => i.id === id && i.size === sz);
    if (hit) hit.qty = Math.min(20, hit.qty + n); else bag.push({ id, size: sz, qty: n });
    save();
  }
  const bagEl = $("#bag");
  function drawBag() {
    const box = $("#bagItems"); box.replaceChildren();
    if (!bag.length) box.append(el("p", { class: "note", text: "Your list is empty. Open a hoodie, pick a size and add it." }));
    bag.forEach((i, idx) => {
      const p = byId[i.id];
      box.append(el("div", { class: "bag-item" },
        el("div", { class: "tile" + (p.light ? " dark" : "") }, el("img", { src: p.img, alt: "" })),
        el("div", {}, el("h3", { text: p.name }), el("p", { text: `${p.color} · Size ${i.size} · ${money(p.price)}` }),
          el("button", { class: "link", type: "button", text: "Remove", onclick: () => { bag.splice(idx, 1); save(); drawBag(); } })),
        el("input", { type: "number", min: 1, max: 20, value: i.qty, "aria-label": `Quantity for ${p.name}`,
          onchange: e => { i.qty = Math.max(1, Math.min(20, parseInt(e.target.value, 10) || 1)); save(); drawBag(); } })));
    });
    const total = bag.reduce((s, i) => s + byId[i.id].price * i.qty, 0);
    $("#bagTotal").textContent = bag.length ? `Estimated total: ${money(total)} + shipping. Nothing is charged now.` : "";
    $("#reqForm").hidden = !bag.length;
  }
  $("#bagNote").textContent = `No payment now. Send the list and we'll email a ship date and payment link. Or email ${C.CONTACT_EMAIL} directly.`;
  function openBag() { drawBag(); $("#reqMsg").textContent = ""; bagEl.showModal(); }
  $("#bagBtn").addEventListener("click", openBag);

  $("#reqForm").addEventListener("submit", e => {
    e.preventDefault();
    const f = new FormData(e.target);
    const items = bag.map(i => `${i.qty} x #${i.id} ${byId[i.id].name} (${byId[i.id].color}, ${i.size})`);
    send({ type: "preorder", name: f.get("name"), email: f.get("email"), note: f.get("note"), items: items.join("\n") }, $("#reqMsg"),
      () => { bag = []; save(); drawBag(); });
  });

  // ---------- sending requests ----------
  async function send(data, msg, done) {
    if (C.FORM_ENDPOINT) {
      msg.textContent = "Sending…";
      try {
        const r = await fetch(C.FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) });
        if (!r.ok) throw new Error(r.status);
        msg.textContent = "Sent. We'll email you."; done && done();
      } catch { msg.textContent = `Couldn't send. Email ${C.CONTACT_EMAIL} instead.`; }
      return;
    }
    // no form service set up: open the visitor's email app with everything filled in
    const subject = data.type === "preorder" ? `Preorder request from ${data.name}` : `Notify me: ${data.product}`;
    const body = Object.entries(data).filter(([k]) => k !== "type").map(([k, v]) => `${k}: ${v}`).join("\n");
    location.href = `mailto:${C.CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    msg.textContent = `Your email app should open. If not, email ${C.CONTACT_EMAIL}.`;
  }

  updateCount(); render(); fromHash();
})();

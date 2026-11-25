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
      el("p", { class: "price", text: money(p.price) }),
      el("h3", { text: p.name }),
      el("div", { class: "row" },
        el("span", {}, el("span", { class: "swatch", style: `background:${p.hex}` }), p.color)));
  }

  // ---------- featured ring: featured hoodies standing in a slowly turning 3-D circle ----------
  (function ring() {
    const box = $("#ring"); if (!box) return;
    const list = P.filter(p => p.featured).sort((a, b) => a.featured - b.featured);
    if (!list.length) { box.closest(".ring-sec").hidden = true; return; }
    const N = list.length, step = Math.PI * 2 / N;
    const items = list.map(p => el("button", { class: "ring-card", type: "button", "aria-label": `${p.name}, ${p.color}, ${money(p.price)}. View`, onclick: () => openProduct(p) },
      el("div", { class: "tile" + (p.light ? " dark" : "") }, el("img", { src: p.img, alt: `${p.color} hoodie: ${p.name}`, width: 560, height: 570 })),
      el("p", { class: "price", text: money(p.price) })));
    box.append(...items);
    const still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    const speed = (Math.PI * 2) / ((Number(C.HERO_SPEED) || 40) * 1000);   // radians per ms
    let angle = 0, target = null, paused = false, last = 0;
    function place() {
      const W = box.clientWidth, R = Math.min(W * (W < 600 ? 0.44 : 0.36), 520), lift = Math.min(W * 0.05, 46);
      items.forEach((it, i) => {
        const t = angle + i * step, x = Math.sin(t) * R, z = Math.cos(t);       // z: 1 front, -1 back
        const s = 0.55 + 0.45 * (z + 1) / 2;
        it.style.transform = `translate(-50%, -50%) translate3d(${x.toFixed(1)}px, ${(z * lift).toFixed(1)}px, 0) scale(${s.toFixed(3)})`;
        it.style.zIndex = String(Math.round((z + 1) * 50));
        it.style.filter = `brightness(${(0.45 + 0.55 * (z + 1) / 2).toFixed(3)}) saturate(${(0.6 + 0.4 * (z + 1) / 2).toFixed(3)})`;
        it.tabIndex = z > 0.7 ? 0 : -1;
        it.classList.toggle("front", z > 0.97);
      });
    }
    function turn(dir) {   // step to the next/previous hoodie
      const k = Math.round(-angle / step) + dir; target = -k * step;
    }
    function frame(now) {
      const dt = last ? Math.min(now - last, 50) : 16; last = now;
      if (target !== null) {
        const d = target - angle; angle += d * 0.12; if (Math.abs(d) < 0.002) { angle = target; target = null; }
      } else if (!still && !paused && !document.hidden) angle -= speed * dt;
      place(); requestAnimationFrame(frame);
    }
    $("#ringPrev").addEventListener("click", () => turn(-1));
    $("#ringNext").addEventListener("click", () => turn(1));
    const sec = box.closest(".ring-sec");
    sec.addEventListener("mouseenter", () => paused = true); sec.addEventListener("mouseleave", () => paused = false);
    sec.addEventListener("focusin", () => paused = true); sec.addEventListener("focusout", () => paused = false);
    let sx = null, swiped = false;
    box.addEventListener("pointerdown", e => { sx = e.clientX; swiped = false; });
    box.addEventListener("pointerup", e => { if (sx !== null && Math.abs(e.clientX - sx) > 40) { swiped = true; turn(e.clientX < sx ? 1 : -1); } sx = null; });
    box.addEventListener("click", e => { if (swiped) { e.stopPropagation(); e.preventDefault(); swiped = false; } }, true);
    window.addEventListener("resize", place);
    place(); requestAnimationFrame(frame);
  })();

  // ---------- filters ----------
  const fCat = $("#fCat"), fTheme = $("#fTheme"), fColor = $("#fColor"), fSort = $("#fSort"), fSearch = $("#fSearch");
  const countType = id => P.filter(p => p.type === id).length;
  fCat.append(el("option", { value: "", text: `All products (${P.length})` }),
    ...CAT.types.map(t => el("option", { value: t.id, text: t.live ? `${t.label} (${countType(t.id)})` : `${t.label} (coming soon)` })));
  fTheme.append(el("option", { value: "", text: "All themes" }),
    ...Object.entries(CAT.themes).map(([k, v]) => el("option", { value: k, text: `${v} (${P.filter(p => p.theme === k).length})` })));
  const colors = [...new Set(P.map(p => p.color))].sort();
  fColor.append(el("option", { value: "", text: "All colors" }), ...colors.map(c => el("option", { value: c, text: c })));

  // ---------- styled drop-downs on top of the native selects (selects stay the source of truth) ----------
  const menus = [];
  function fancy(sel) {
    const lab = sel.closest("label"), title = lab ? lab.firstChild.textContent.trim() : "";
    const field = el("div", { class: "field" }, el("span", { class: "field-label", id: sel.id + "Lbl", text: title }));
    if (lab) { lab.replaceWith(field); }
    sel.classList.add("sr"); sel.tabIndex = -1; sel.setAttribute("aria-hidden", "true");
    const btn = el("button", { type: "button", class: "dd-btn", "aria-haspopup": "listbox", "aria-expanded": "false", "aria-labelledby": `${sel.id}Lbl ${sel.id}Val` },
      el("span", { class: "dd-val", id: sel.id + "Val" }), el("span", { class: "dd-chev", "aria-hidden": "true" }));
    const list = el("ul", { class: "dd-list", role: "listbox", "aria-labelledby": sel.id + "Lbl", hidden: true });
    const items = [...sel.options].map(o => {
      const soon = /\(coming soon\)/.test(o.text), txt = o.text.replace(/\s*\(coming soon\)/, "");
      const li = el("li", { role: "option", tabindex: "-1", "data-v": o.value, class: soon ? "soon" : "" },
        el("span", { text: txt }), soon ? el("span", { class: "tag", text: "soon" }) : null);
      li.addEventListener("click", () => choose(o.value));
      return li;
    });
    list.append(...items);
    const wrap = el("div", { class: "dd" }, btn, list);
    field.append(sel, wrap);
    const isOpen = () => !list.hidden;
    function open() {
      menus.forEach(m => m !== api && m.close());
      list.hidden = false; btn.setAttribute("aria-expanded", "true"); wrap.classList.add("open");
      (items.find(li => li.dataset.v === sel.value) || items[0]).focus();
    }
    function close(focusBtn) { if (!isOpen()) return; list.hidden = true; btn.setAttribute("aria-expanded", "false"); wrap.classList.remove("open"); if (focusBtn) btn.focus(); }
    function choose(v) { if (sel.value !== v) { sel.value = v; sel.dispatchEvent(new Event("change")); } sync(); close(true); }
    function sync() {
      const o = sel.options[sel.selectedIndex]; $("#" + sel.id + "Val").textContent = o ? o.text.replace(/\s*\(coming soon\)/, "") : "";
      items.forEach(li => li.setAttribute("aria-selected", li.dataset.v === sel.value));
    }
    btn.addEventListener("click", () => isOpen() ? close() : open());
    btn.addEventListener("keydown", e => { if (["ArrowDown", "ArrowUp"].includes(e.key)) { e.preventDefault(); open(); } });
    list.addEventListener("keydown", e => {
      const i = items.indexOf(document.activeElement);
      const go = k => { e.preventDefault(); items[Math.max(0, Math.min(items.length - 1, k))].focus(); };
      if (e.key === "ArrowDown") go(i + 1); else if (e.key === "ArrowUp") go(i - 1);
      else if (e.key === "Home") go(0); else if (e.key === "End") go(items.length - 1);
      else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); if (i >= 0) choose(items[i].dataset.v); }
      else if (e.key === "Escape") { e.preventDefault(); close(true); }
      else if (e.key === "Tab") close();
    });
    const api = { sync, close, wrap };
    menus.push(api); return api;
  }
  document.addEventListener("click", e => menus.forEach(m => { if (!m.wrap.contains(e.target)) m.close(); }));
  [fCat, fTheme, fColor, fSort].forEach(fancy);

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
    menus.forEach(m => m.sync());
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
    gallery(p);
    $("#sizeGuide").hidden = true; $("#sgBtn").setAttribute("aria-expanded", "false");
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
      "All sales final: check the size guide",
    ].map(s => el("li", { text: s })));
    if (push) history.replaceState(null, "", location.pathname + location.search + "#" + p.slug);
    if (!pd.open) pd.showModal();
  }
  // ---------- product pictures ----------
  let pics = [], gi = 0;
  function gallery(p) {
    pics = (p.imgs && p.imgs.length) ? p.imgs : [{ src: p.img, alt: p.placement }];
    $("#gThumbs").replaceChildren(...pics.map((im, i) => el("button", { type: "button", class: "g-thumb", "aria-label": `Picture ${i + 1}: ${im.alt}`, onclick: () => show(i) },
      el("img", { src: im.src, alt: "", loading: "lazy" }))));
    $("#pdImgWrap").className = "pd-img" + (p.light ? " dark" : "");
    const multi = pics.length > 1;
    $("#gPrev").hidden = $("#gNext").hidden = $("#gCount").hidden = !multi; $("#gThumbs").hidden = !multi;
    show(0);
  }
  function show(i) {
    gi = (i + pics.length) % pics.length;
    $("#pdImg").src = pics[gi].src; $("#pdImg").alt = `${cur.color} hoodie, ${cur.name}: ${pics[gi].alt}`;
    $("#gCount").textContent = `${gi + 1} / ${pics.length}`;
    $("#gThumbs").querySelectorAll(".g-thumb").forEach((b, k) => b.setAttribute("aria-current", k === gi));
  }
  $("#gPrev").addEventListener("click", () => show(gi - 1));
  $("#gNext").addEventListener("click", () => show(gi + 1));
  pd.addEventListener("keydown", e => {
    if (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
    if (e.key === "ArrowLeft") { show(gi - 1); e.preventDefault(); }
    if (e.key === "ArrowRight") { show(gi + 1); e.preventDefault(); }
  });
  let sx = null;
  $("#pdImgWrap").addEventListener("pointerdown", e => { sx = e.clientX; });
  $("#pdImgWrap").addEventListener("pointerup", e => { if (sx !== null && Math.abs(e.clientX - sx) > 40) show(gi + (e.clientX < sx ? 1 : -1)); sx = null; });

  // ---------- size guide ----------
  (function sizeGuide() {
    const rows = C.SIZE_CHART || [], u = C.SIZE_UNITS || "in";
    const filled = rows.some(r => r.chest || r.length || r.sleeve);
    const box = $("#sizeGuide");
    box.append(
      el("p", { class: "sg-title", text: "How to measure" }),
      el("ol", {},
        el("li", { text: "Use a hoodie you own that fits the way you like. Lay it flat." }),
        el("li", { text: "Chest: armpit to armpit, then double it." }),
        el("li", { text: "Length: top of the shoulder next to the collar, straight down to the hem." }),
        el("li", { text: "Sleeve: center back of the collar to the end of the cuff." })),
      filled
        ? el("table", {}, el("thead", {}, el("tr", {}, ...["Size", `Chest (${u})`, `Length (${u})`, `Sleeve (${u})`].map(t => el("th", { text: t })))),
            el("tbody", {}, ...rows.map(r => el("tr", {}, ...[r.size, r.chest || "–", r.length || "–", r.sleeve || "–"].map(t => el("td", { text: String(t) }))))))
        : el("p", { class: "sg-note", text: "Measurements coming soon." }),
      el("p", { class: "sg-note", text: "All sales are final, so please check before ordering." }));
    $("#sgBtn").addEventListener("click", () => { box.hidden = !box.hidden; $("#sgBtn").setAttribute("aria-expanded", !box.hidden); });
  })();

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

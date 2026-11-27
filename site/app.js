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
  const track = (n, p) => { try { window.track && window.track(n, p); } catch (e) {} };
  const trackPurchase = (...x) => { try { window.trackPurchase && window.trackPurchase(...x); } catch (e) {} };
  // One price per item type? Then prices come off the cards and the shop says each type's price once, clearly.
  const typeOf = id => CAT.types.find(t => t.id === id) || { id, label: "Items", one: "item", many: "items" };
  const LIVE = CAT.types.filter(t => P.some(p => p.type === t.id));
  const ONE_BY = {};
  LIVE.forEach(t => { const pr = [...new Set(P.filter(p => p.type === t.id).map(p => p.price))]; if (pr.length === 1) ONE_BY[t.id] = pr[0]; });
  // one price per item kind (Crew socks $24, Ankle socks $16...): cards still hide prices when each kind has a single price
  const KIND = {}; P.forEach(p => { (KIND[p.typeLabel] = KIND[p.typeLabel] || new Set()).add(p.price); });
  const EACH = LIVE.length > 0 && Object.values(KIND).every(s => s.size === 1);
  const onePrice = p => KIND[p.typeLabel].size === 1;
  const MIN_BY = {}, MAX_BY = {};
  LIVE.forEach(t => { const pr = P.filter(p => p.type === t.id).map(p => p.price); MIN_BY[t.id] = Math.min(...pr); MAX_BY[t.id] = Math.max(...pr); });
  const ONE = LIVE.length === 1 && EACH ? ONE_BY[LIVE[0].id] : null;       // only one type in the shop: say "Every hoodie $150"
  const shipLine = () => {
    const f = Number(C.SHIPPING_FLAT) || 0, q = Number(C.FREE_SHIP_QTY) || 0, o = Number(C.FREE_SHIP_OVER) || 0;
    if (!f) return "Free shipping";
    return o ? `${money(f)} shipping · free on orders ${money(o)}+` : q ? `${money(f)} shipping · free on ${q}+ items` : `${money(f)} shipping`;
  };
  const cfg = k => (typeof C[k] === "string" ? C[k].trim() : "");
  const SHIP_WINDOW = cfg("SHIP_WINDOW"), ORIGIN = cfg("ORIGIN");
  const FIT = C.FIT || {}, WEIGHT = C.WEIGHT || {}, SET_OFF = Math.max(0, Number(C.SET_DISCOUNT) || 0);
  const fitText = t => [typeof FIT[t] === "string" && FIT[t].trim() ? "Fit: " + FIT[t].trim() : "", typeof WEIGHT[t] === "string" && WEIGHT[t].trim() ? "Fabric weight: " + WEIGHT[t].trim() : ""].filter(Boolean).join(" · ");
  // saved items (on this device only)
  const savedIds = () => { try { const v = JSON.parse(localStorage.getItem("saved")); return Array.isArray(v) ? v.filter(id => byId[id]).slice(0, 50) : []; } catch { return []; } };
  const isSaved = id => savedIds().includes(id);
  const SVGNS = "http://www.w3.org/2000/svg";
  const heartIcon = () => { const s = document.createElementNS(SVGNS, "svg"); s.setAttribute("viewBox", "0 0 24 24"); s.setAttribute("width", "20"); s.setAttribute("height", "20"); s.setAttribute("aria-hidden", "true");
    const pth = document.createElementNS(SVGNS, "path"); pth.setAttribute("d", "M12 20s-7-4.4-9.2-8.6C1.2 8.2 3 4.8 6.3 4.5c2-.2 3.6 1 4.4 2.5h.6c.8-1.5 2.4-2.7 4.4-2.5 3.3.3 5.1 3.7 3.5 6.9C19 15.6 12 20 12 20z"); s.append(pth); return s; };
  const MAXQ = Math.max(1, Number(C.MAX_QTY_PER_ITEM) || 3), MAXN = Math.max(1, Number(C.MAX_ITEMS_PER_ORDER) || 8);
  const LARGE = Number(C.LARGE_ORDER_ITEMS) || 4;
  const clampQ = n => Math.max(1, Math.min(MAXQ, parseInt(n, 10) || 1));
  const safeUrl = u => /^https:\/\/[^\s"'<>]+$/i.test(String(u || "")) ? u : "";
  const byId = Object.fromEntries(P.map(p => [p.id, p]));

  const bySlug = Object.fromEntries(P.map(p => [p.slug, p]));

  // ---------- branding ----------
  document.title = `${C.BRAND} | Dark-humor clothing, no plastic`;
  document.querySelectorAll("[data-brand]").forEach(n => n.textContent = C.BRAND);
  document.querySelectorAll("[data-contact]").forEach(a => { a.href = "mailto:" + C.CONTACT_EMAIL; a.textContent = C.CONTACT_EMAIL; });
  $("[data-tagline]").textContent = C.TAGLINE;
  $("[data-featured-label]").textContent = C.FEATURED_LABEL;
  $("#year").textContent = new Date().getFullYear();

  // ---------- cards ----------
  if (!document.getElementById("spinHint")) document.querySelector("main").append(el("p", { id: "spinHint", class: "sr", text: "Left and right arrows turn it." }));
  function card(p) {
    const back = (p.imgs && p.imgs[1] && p.imgs[1].src) || p.img;
    const stage = el("div", { class: "stage" },
      el("div", { class: "turn" },
        el("img", { class: "face front", src: p.img, alt: "", loading: "lazy", width: 560, height: 570, draggable: "false" }),
        el("img", { class: "face back", "data-src": back, alt: "", width: 560, height: 570, draggable: "false" })),
      el("span", { class: "shadow", "aria-hidden": "true" }),
      el("span", { class: "spin-ico", "aria-hidden": "true", text: "\u21BB" }));
    // accessible name = the visible text (WCAG 2.5.3); price stays for screen readers even when it's hidden on the card
    const c = el("button", { class: "card", type: "button", "aria-describedby": "spinHint", onclick: () => openProduct(p) },
      stage,
      ONE_BY[p.type] != null ? el("span", { class: "sr", text: money(p.price) + "," }) : el("p", { class: "price", text: money(p.price) }),
      el("h3", { text: p.name }),
      el("div", { class: "row" },
        el("span", {}, el("span", { class: "swatch", style: `background:${p.hex}` }), `${p.color} · ${p.typeLabel}`)));
    spinnable(stage, c);
    const heart = el("button", { type: "button", class: "save-heart", "data-id": p.id, "aria-pressed": String(isSaved(p.id)), "aria-label": `Save ${p.name}, ${p.typeLabel}`,
      onclick: e => { e.stopPropagation(); toggleSave(p); } }, heartIcon());
    return el("div", { class: "card-cell" }, c, heart);
  }

  // ---------- spin: drag (computer) or swipe sideways (phone) to turn a hoodie between front and back ----------
  const STILL = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function spinnable(stage, card) {
    const turn = stage.querySelector(".turn"), faces = [...stage.querySelectorAll(".face")], shadow = stage.querySelector(".shadow");
    let a = 0, v = 0, raf = 0, down = null, lastX = 0, lastT = 0, moved = false, justSpun = false, hover = false, t0 = 0;
    const loadBack = () => { const b = faces[1]; if (b.dataset.src) { b.src = b.dataset.src; delete b.dataset.src; } };
    function draw() {
      const c = Math.cos(a * Math.PI / 180), lit = 0.55 + 0.45 * Math.abs(c);
      turn.style.transform = `rotateY(${a.toFixed(2)}deg)`;
      faces.forEach(f => f.style.filter = `brightness(${lit.toFixed(3)}) drop-shadow(0 0 1.2px rgba(236,229,216,${(0.5 * lit).toFixed(2)}))`);
      shadow.style.transform = `scaleX(${(0.55 + 0.45 * Math.abs(c)).toFixed(3)})`;
    }
    function loop(now) {
      raf = 0; if (down && moved) return;
      if (Math.abs(v) > 0.05) { a += v; v *= 0.94; }
      else {
        v = 0;
        const target = Math.round(a / 180) * 180, idle = hover && !STILL ? Math.sin((now - t0) / 700) * 10 : 0;
        a += (target + idle - a) * 0.12;
        if (Math.abs(target + idle - a) < 0.05 && !hover) { a = target; draw(); return; }
      }
      draw(); raf = requestAnimationFrame(loop);
    }
    const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };
    stage.addEventListener("pointerdown", e => { if (e.button > 0) return; loadBack(); justSpun = false; down = { x: e.clientX, y: e.clientY, a, id: e.pointerId }; moved = false; v = 0; lastX = e.clientX; lastT = e.timeStamp; });
    stage.addEventListener("pointermove", e => {
      if (!down || e.pointerId !== down.id) return;
      const dx = e.clientX - down.x, dy = e.clientY - down.y;
      if (!moved && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { moved = true; try { stage.setPointerCapture(e.pointerId); } catch {} }
      if (!moved) return;
      a = down.a + dx * 0.7;
      const dt = Math.max(8, e.timeStamp - lastT); v = (e.clientX - lastX) * 0.7 * (16 / dt); lastX = e.clientX; lastT = e.timeStamp;
      draw();
    });
    const end = () => { if (!down) return; if (moved) justSpun = true; down = null; moved = false; kick(); };
    stage.addEventListener("pointerup", end); stage.addEventListener("pointercancel", end);
    card.addEventListener("click", e => { if (justSpun) { e.stopPropagation(); e.preventDefault(); justSpun = false; } }, true);   // a spin isn't a click
    card.addEventListener("keydown", e => { if (e.key === "ArrowRight" || e.key === "ArrowLeft") { e.preventDefault(); loadBack(); v = (e.key === "ArrowRight" ? 1 : -1) * 9; kick(); } });
    card.addEventListener("pointerenter", e => { if (e.pointerType === "mouse") { hover = true; t0 = performance.now(); loadBack(); kick(); } });
    card.addEventListener("pointerleave", () => { hover = false; kick(); });
  }

  // ---------- featured ring: featured hoodies standing in a slowly turning 3-D circle ----------
  (function ring() {
    const box = $("#ring"); if (!box) return;
    const list = P.filter(p => p.featured).sort((a, b) => a.featured - b.featured);
    if (!list.length) { box.closest(".ring-sec").hidden = true; return; }
    const N = list.length, step = Math.PI * 2 / N;
    const items = list.map(p => el("button", { class: "ring-card", type: "button", "aria-label": `${p.name}, ${p.color}, ${money(p.price)}. View`, onclick: () => openProduct(p) },
      el("div", { class: "tile" }, el("img", { src: p.img, alt: `${p.color} ${p.typeLabel.toLowerCase()}: ${p.name}`, width: 560, height: 570, draggable: "false" })),
      el("span", { class: "shadow", "aria-hidden": "true" }),
      ONE_BY[p.type] != null ? null : el("p", { class: "price", text: money(p.price) })));
    box.append(...items);
    const still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    const speed = (Math.PI * 2) / ((Number(C.HERO_SPEED) || 40) * 1000);   // radians per ms
    let angle = 0, target = null, hover = false, kbd = false, stopped = false, last = 0, stepClock = 0;
    function place() {
      const W = box.clientWidth, R = Math.min(W * (W < 600 ? 0.4 : 0.33), 600), lift = Math.min(W * 0.05, 46);
      items.forEach((it, i) => {
        const t = angle + i * step, x = Math.sin(t) * R, z = Math.cos(t);       // z: 1 front, -1 back
        const s = 0.55 + 0.45 * (z + 1) / 2;
        it.style.transform = `translate(-50%, -50%) translate3d(${x.toFixed(1)}px, ${(z * lift).toFixed(1)}px, 0) scale(${s.toFixed(3)})`;
        it.style.zIndex = String(Math.round((z + 1) * 50));
        const op = Math.max(0, Math.min(1, (z + 0.25) / 0.75));      // fades out as it turns away, gone at the back
        it.style.opacity = op.toFixed(3);
        it.style.visibility = op < 0.02 ? "hidden" : "visible";
        it.style.pointerEvents = op > 0.6 ? "auto" : "none";
        it.style.filter = `brightness(${(0.55 + 0.45 * (z + 1) / 2).toFixed(3)})`;
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
      } else if (!stopped && !hover && !kbd && !document.hidden) {
        if (!still) angle -= speed * dt;                       // continuous slow spin
        else if ((stepClock += dt) > 5000) { stepClock = 0; turn(1); }   // reduced motion: gentle step every 5 s
      }
      place(); requestAnimationFrame(frame);
    }
    // keyboard: left/right arrows turn the ring when a hoodie in it has focus (replaces the on-screen arrows)
    box.addEventListener("keydown", e => { if (e.key === "ArrowLeft" || e.key === "ArrowRight") { e.preventDefault(); turn(e.key === "ArrowRight" ? 1 : -1); } });
    const sec = box.closest(".ring-sec");
    // pause only while a mouse is over a hoodie or the keyboard is on one; taps and arrow clicks don't stop it
    items.forEach(it => {
      it.addEventListener("pointerenter", e => { if (e.pointerType === "mouse") hover = true; });
      it.addEventListener("pointerleave", () => { hover = false; });
      it.addEventListener("focus", () => { kbd = it.matches(":focus-visible"); });
      it.addEventListener("blur", () => { kbd = false; });
    });
    const pp = $("#ringPause");
    pp.addEventListener("click", () => { stopped = !stopped; pp.setAttribute("aria-pressed", stopped); pp.textContent = stopped ? "\u25B6" : "\u275A\u275A";
      pp.setAttribute("aria-label", stopped ? "Start spinning" : "Stop spinning"); });
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

  // ---------- one-tap chips on top of the hidden native selects (selects stay the source of truth) ----------
  const menus = [];
  const colorHex = Object.fromEntries(P.map(p => [p.color, p.hex]));
  function chips(sel) {
    const box = document.querySelector(`.chips[data-for="${sel.id}"]`);
    box.setAttribute("role", "radiogroup"); box.setAttribute("aria-labelledby", sel.id + "Lbl");
    const toggle = sel.id === "fCat" || sel.id === "fColor";   // no "All" button: nothing selected = everything; tap the selected one again to clear
    const items = [...sel.options].filter(o => !(toggle && o.value === "")).map(o => {
      const soon = /\(coming soon\)/.test(o.text);
      const m = o.text.replace(/\s*\(coming soon\)/, "").match(/^(.*?)(?:\s*\((\d+)\))?$/);
      let label = m[1], n = m[2];
      if (o.value === "") label = "All";
      const full = label;
      if (sel.id === "fTheme" && o.value) label = label.split(" & ")[0];          // short theme names on the buttons ("Morgue", "Rot"...)
      const dot = sel.id === "fColor";                                              // colors are swatch dots ("All" = a mixed dot); names stay for screen readers
      if (dot && !o.value) label = "All colors";
      const tabPrice = sel.id !== "fCat" || !o.value ? "" : ONE_BY[o.value] != null ? money(ONE_BY[o.value]) : MIN_BY[o.value] != null ? `from ${money(MIN_BY[o.value])}` : "";
      const b = el("button", { type: "button", class: "chip" + (soon ? " is-soon" : "") + (dot ? " dot" : ""), role: "radio", "data-v": o.value,
          "aria-label": tabPrice ? `${full}, ${tabPrice} each` : dot ? label : o.text, title: dot ? label : label !== full ? full : null },
        dot ? el("span", { class: "sw" + (o.value ? "" : " sw-all"), style: o.value ? `background:${colorHex[o.value]}` : null }) : null,
        el("span", { class: dot ? "sr" : "cl", text: label }),
        tabPrice ? el("span", { class: "tp", text: tabPrice }) : null,
        soon ? el("span", { class: "tag", text: "soon" }) : null);
      b.addEventListener("click", e => {
        const next = toggle && sel.value === o.value && e.detail !== -1 ? "" : o.value;   // keyboard arrows (detail -1) never clear
        if (sel.value !== next) { sel.value = next; sel.dispatchEvent(new Event("change")); } sync(); });
      return b;
    });
    box.append(...items);
    box.addEventListener("keydown", e => {   // arrow keys move between chips in the same row
      const i = items.indexOf(document.activeElement); if (i < 0) return;
      const k = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : e.key === "Home" ? 0 : e.key === "End" ? items.length - 1 : null;
      if (k === null) return; e.preventDefault();
      const t = items[Math.max(0, Math.min(items.length - 1, k))]; t.focus(); t.dispatchEvent(new MouseEvent("click", { detail: -1, bubbles: true }));
    });
    function sync() {
      items.forEach(b => { const on = b.dataset.v === sel.value; b.setAttribute("aria-checked", on); b.tabIndex = on ? 0 : -1; });
      if (!items.some(b => b.dataset.v === sel.value) && items[0]) items[0].tabIndex = 0;   // nothing picked: first button is the way in
      const on = items.find(b => b.dataset.v === sel.value);
      if (on && box.scrollWidth > box.clientWidth) {   // keep the selected chip in view in its row
        const l = on.offsetLeft - box.offsetLeft, r = l + on.offsetWidth;
        if (l < box.scrollLeft || r > box.scrollLeft + box.clientWidth) box.scrollTo({ left: l - 16, behavior: "smooth" });
      }
    }
    const api = { sync, close() {}, wrap: box };
    menus.push(api); return api;
  }
  [fCat, fColor, fSort].forEach(chips);   // themes: no buttons (user removed them); the hidden select still honors ?theme= links

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
    history.replaceState(history.state, "", location.pathname + (s ? "?" + s : "") + location.hash);
  }

  // Default order: featured first, then 3 hoodies (or the biggest type) for every 1 other item, cycling through the other types,
  // so tees, hats, boxers and socks show up early instead of after all 107 hoodies.
  function mixTypes(list) {
    const feat = list.filter(p => p.featured), rest = list.filter(p => !p.featured);
    const groups = {}; rest.forEach(p => (groups[p.type] = groups[p.type] || []).push(p));
    const keys = Object.keys(groups).sort((a, b) => groups[b].length - groups[a].length);
    if (keys.length < 2) return list;
    const main = groups[keys[0]], others = keys.slice(1).map(k => groups[k]), out = [...feat];
    let oi = 0;
    while (main.length || others.some(g => g.length)) {
      out.push(...main.splice(0, 3));
      for (let tries = 0; tries < others.length; tries++) { const g = others[oi++ % others.length]; if (g.length) { out.push(g.shift()); break; } }
      if (!main.length) others.forEach(g => out.push(...g.splice(0)));
    }
    return out;
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
    const words = searchWords(fSearch.value);
    let list = P.filter(p =>
      (!fCat.value || p.type === fCat.value) && (!fTheme.value || p.theme === fTheme.value) &&
      (!fColor.value || p.color === fColor.value) &&
      words.every(w => haystack(p).includes(w)));
    if (fSort.value === "az") list.sort((a, b) => a.name.localeCompare(b.name));
    else if (fSort.value === "new") list.sort((a, b) => b.id - a.id);
    else list = mixTypes(list.sort((a, b) => (a.featured || 999) - (b.featured || 999) || a.id - b.id));
    const tt = type || (LIVE.length === 1 ? LIVE[0] : null);
    $("#resultCount").textContent = `${list.length} ${tt ? (list.length === 1 ? tt.one : tt.many) : (list.length === 1 ? "item" : "items")}`
      + (tt && ONE_BY[tt.id] != null ? ` · ${money(ONE_BY[tt.id])} each` : tt && MIN_BY[tt.id] != null ? ` · ${money(MIN_BY[tt.id])}–${money(MAX_BY[tt.id])}` : "") + (fColor.value ? ` · ${fColor.value}` : "") + (fTheme.value && CAT.themes[fTheme.value] ? ` · ${CAT.themes[fTheme.value]}` : "");
    priceTag(type);
    if (!list.length) {
      const tips = ["skull", "coffin", "grief", "gym", "rot", "black"];
      grid.append(el("div", { class: "empty" },
        el("p", { text: words.length ? `Nothing matches "${fSearch.value.trim()}".` : "Nothing matches these filters." }),
        el("p", { class: "tips" }, "Try: ", ...tips.map(w => el("button", { type: "button", class: "chip", text: w,
          onclick: () => { fCat.value = fTheme.value = fColor.value = ""; fSearch.value = w; render(); } })))));
      track("search_no_results", { q: fSearch.value.trim() });
    }
    else grid.append(...list.map(card));
    writeURL();
  }

  // search: ignore filler words, map common shopper words, match picture tags too
  const STOP = new Set(["a", "an", "the", "with", "and", "of", "for"]);
  const ALIAS = { "3am": "3 a.m.", "3": "3 a.m.", "skulls": "skull", "skeletons": "skeleton", "coffins": "coffin", "graves": "grave", "funny": "", "dark": "",
    "sad": "grief", "depressed": "grief", "depression": "grief", "anxiety": "grief", "mental": "grief", "workout": "gym", "lifting": "lift", "weights": "gym",
    "gray": "grey", "dead": "dead", "hoodies": "hoodie", "hoody": "hoodie", "sweatshirt": "hoodie", "sweater": "hoodie", "pullover": "hoodie",
    "tshirt": "tee", "t-shirt": "tee", "tees": "tee", "shirts": "shirt", "hats": "hat", "beanies": "beanie", "caps": "cap", "boxer": "boxers", "sock": "socks", "sweats": "sweatpants", "joggers": "sweatpants", "zip": "", "up": "", "xl": "", "xxl": "", "2xl": "", "3xl": "", "small": "", "medium": "", "large": "" };
  function searchWords(q) {
    return q.toLowerCase().replace(/[^a-z0-9.' -]/g, " ").split(/\s+/).filter(Boolean)
      .map(w => (w in ALIAS ? ALIAS[w] : w)).filter(w => w && !STOP.has(w));
  }
  const hay = {};
  const haystack = p => hay[p.id] || (hay[p.id] = `${p.name} ${p.sub} ${p.color} ${p.colorNote} ${CAT.themes[p.theme]} ${p.placement} ${p.typeLabel} ${p.type} ${p.tags || ""}`.toLowerCase());

  // the one-price tag beside "All products": the chosen type's price, or every type's price on "All"
  function priceTag(type) {
    const op = $("#onePrice"); if (!op) return;
    op.hidden = true; return;   // prices now sit on the item tabs (see chips()); the old price box stays hidden
    if (type && ONE_BY[type.id] != null) {
      op.replaceChildren(el("span", { class: "op-k", text: "One price" }), el("span", { class: "op-v", text: money(ONE_BY[type.id]) }),
        el("span", { class: "op-s", text: `every ${type.one.startsWith("pair of") ? "pair" : type.one}` }));
    } else if (LIVE.length === 1) {
      op.replaceChildren(el("span", { class: "op-k", text: "One price" }), el("span", { class: "op-v", text: money(ONE_BY[LIVE[0].id]) }), el("span", { class: "op-s", text: "every design" }));
    } else {
      op.replaceChildren(el("span", { class: "op-k", text: "One price each" }),
        ...LIVE.map(t => el("span", { class: "op-i" }, el("span", { class: "op-l", text: t.label }), el("span", { class: "op-v", text: money(ONE_BY[t.id]) }))));
    }
  }

  function soonCard(t) {
    const msg = el("p", { class: "pd-msg", role: "status" });
    const email = el("input", { type: "email", required: true, placeholder: "you@email.com", "aria-label": "Email" });
    return el("div", { class: "soon" },
      el("h3", { text: `${t.label} are coming` }),
      el("p", { text: `Same rules as everything else here: natural fiber, no plastic. Planned price around ${money(t.price)}. Leave your email and you'll hear first.` }),
      el("form", { onsubmit: e => { e.preventDefault(); send({ type: "notify", product: t.label, email: email.value }, msg); } },
        email, el("button", { class: "btn", type: "submit", text: "Notify me" })), msg);
  }

  $("#filters").addEventListener("submit", e => e.preventDefault());
  [fCat, fTheme, fColor, fSort].forEach(s => s.addEventListener("change", render));
  let t, ts; fSearch.addEventListener("input", () => { clearTimeout(t); t = setTimeout(render, 150);
    clearTimeout(ts); ts = setTimeout(() => fSearch.value.trim() && track("search", { q: fSearch.value.trim(), results: $("#grid").querySelectorAll(".card").length }), 1200); });
  $("#clearBtn").addEventListener("click", () => { fCat.value = fTheme.value = fColor.value = ""; fSearch.value = ""; render(); });

  // ---------- product dialog ----------
  const pd = $("#pd"); let cur = null, size = null;
  function openProduct(p, push = true) {
    cur = p; size = null;
    gallery(p);
    $("#sizeGuide").hidden = true; $("#sgBtn").setAttribute("aria-expanded", "false");
    $("#pdMeta").textContent = [p.featured ? C.FEATURED_LABEL : "", CAT.themes[p.theme], p.placement].filter(Boolean).join(" · ");
    $("#pdName").textContent = p.name; $("#pdSub").textContent = p.sub || "";
    const tp = typeOf(p.type);
    const kindWord = ONE_BY[p.type] != null ? (p.type === "hats" ? "hat" : p.type === "underwear" ? "pair of boxers" : p.type === "socks" ? "pair of socks" : tp.one)
      : (p.type === "socks" ? `pair of ${p.typeLabel.toLowerCase()}` : p.typeLabel.toLowerCase());
    $("#pdPrice").replaceChildren(money(p.price), onePrice(p) ? el("span", { class: "same-price", text: `Same price for every ${kindWord}` }) : "");
    $("#pdShip").textContent = shipLine() + (SHIP_WINDOW ? ` · ${SHIP_WINDOW}` : "");
    $("#pdShare").textContent = `Copy link to this ${p.typeLabel.toLowerCase()}`;
    const ft = fitText(p.type); $("#pdFit").textContent = ft; $("#pdFit").hidden = !ft;
    syncSave();
    drawAlso(p);
    $("#pdQty").value = 1; $("#pdMsg").textContent = "";
    const out = (C.SOLD_OUT && C.SOLD_OUT[p.id]) || [];
    $("#pdSizes").replaceChildren(...p.sizes.map(s => el("button", { type: "button", "aria-pressed": "false", "data-s": s,
      class: out.includes(s) ? "is-out" : "", "aria-label": out.includes(s) ? `${s}, sold out` : s, text: s,
      onclick: () => pickSize(s, false) })));
    $("#sizeNote").textContent = "";
    track("product_viewed", { id: p.id, name: p.name, theme: p.theme, color: p.color });
    const single = p.sizes.length === 1;
    pd.classList.toggle("one-size", single);
    sizeGuideFor(p);
    const remembered = store.get("last-size-" + p.type) || (p.type === "hoodie" ? store.get("last-size") : null);
    if (single) pickSize(p.sizes[0], true, true);
    else if (remembered && p.sizes.includes(remembered)) pickSize(remembered, true); else setBuyMode(false);
    $("#pdNotes").replaceChildren(...(p.notes || []).map(t => el("li", { text: t })));
    $("#pdNotes").hidden = !(p.notes || []).length;
    // short screens: keep the Add button in view by putting the notes right under it (they're still on screen next to it)
    if (innerHeight < 700) $("#pdAdd").after($("#pdNotes")); else $("#sizeNote").after($("#pdNotes"));
    $("#pdBody").scrollTop = 0; pd.scrollTop = 0;
    $("#pdDetails").replaceChildren(...[...(p.details || []), ...(ORIGIN ? [ORIGIN] : [])].map(s => el("li", { text: s })));
    remember(p.id);
    if (!pd.open) { pd.showModal(); noteOpen(); }   // adds the Back step first, so the link below goes on that step, not the page underneath
    if (push) history.replaceState(history.state, "", location.pathname + location.search + "#" + p.slug);
    // very short screens: if the design picker pushes the Add button off screen, move the picker under the Add button (and its notes)
    $("#pdShip").after($("#pdAlso"));
    const visBottom = Math.min(innerHeight, pd.getBoundingClientRect().bottom);   // the pop-up can end above the screen bottom
    if (!$("#pdAlso").hidden && $("#pdAdd").getBoundingClientRect().bottom > visBottom - 4) {
      const n = $("#pdNotes"); (n.previousElementSibling === $("#pdAdd") && !n.hidden ? n : $("#pdAdd")).after($("#pdAlso"));
    }
    $("#pdName").focus({ preventScroll: true }); // start on the product name, not the close button
  }

  // ---------- small storage helper (works even if storage is blocked) ----------
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };

  // ---------- size memory + sold-out sizes ----------
  function pickSize(s, auto, single) {
    size = s;
    const out = ((C.SOLD_OUT && C.SOLD_OUT[cur.id]) || []).includes(s);
    $("#pdSizes").querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b.dataset.s === s));
    $("#pdMsg").textContent = "";
    if (!auto) store.set("last-size-" + cur.type, s);
    $("#sizeNote").textContent = single ? (out ? "Sold out." : "One size.") : auto ? (out ? `Your size (${s}) is sold out in this one.` : `Size ${s} selected (your last size).`) : (out ? `${s} is sold out.` : "");
    setBuyMode(out);
  }
  function setBuyMode(out) {
    $("#pdAdd").hidden = out; $(".qty").hidden = out;
    $("#notifyForm").hidden = !out;
    if (out) { $("#notifyTitle").textContent = `Tell me when ${size} is back`; setMethod("email"); }
    drawAlts(out);
    drawWith();
    drawSet();
  }
  const soldOut = (p, s) => ((C.SOLD_OUT && C.SOLD_OUT[p.id]) || []).includes(s);
  function similar(p, n, s, sameType = true) {   // same type, same theme first, then same color, never the same item; only ones in size s if given
    const ok = q => q.id !== p.id && (!sameType || q.type === p.type) && (!s || !soldOut(q, s));
    const a = P.filter(q => ok(q) && q.theme === p.theme), b = P.filter(q => ok(q) && q.theme !== p.theme && q.color === p.color);
    return [...a, ...b].slice(0, n);
  }
  function mini(q, btn) {
    return el("div", { class: "mini" },
      el("button", { type: "button", class: "mini-open", "aria-label": `View ${q.name}`, onclick: () => { track("suggestion_opened", { from: cur.id, to: q.id }); openProduct(q); } },
        el("span", { class: "mini-pic" }, el("img", { src: q.img, alt: "", loading: "lazy" })),
        el("span", { class: "mini-name", text: q.name }),
        el("span", { class: "mini-meta", text: `${q.typeLabel} · ${money(q.price)}` })), btn || null);
  }
  function drawAlts(out) {
    const box = $("#pdAlts");
    if (!out) { box.hidden = true; return; }
    const list = similar(cur, 4, size);
    box.hidden = !list.length;
    $("#pdAltsTitle").textContent = `Available in ${size}`;
    $("#pdAltsList").replaceChildren(...list.map(q => mini(q)));
  }
  // ---------- same design + color on the other items (hoodie, tee, hats, boxers, socks, sweatpants) ----------
  const TYPE_ORDER = CAT.types.map(t => t.id);
  const designOf = q => q.design != null ? q.design : q.id % 1000;
  function drawAlso(p) {
    const list = P.filter(q => designOf(q) === designOf(p))
      .sort((a, b) => TYPE_ORDER.indexOf(a.type) - TYPE_ORDER.indexOf(b.type) || b.price - a.price || a.typeLabel.localeCompare(b.typeLabel));
    $("#pdAlso").hidden = list.length < 2;
    if (list.length < 2) { $("#pdAlsoList").replaceChildren(); return; }
    $("#pdAlsoK").textContent = `Also in this design · ${p.color}`;
    const btns = list.map(q => el("button", { type: "button", role: "radio", class: "also", "aria-checked": String(q.id === p.id),
      tabindex: q.id === p.id ? "0" : "-1", "aria-label": `${q.typeLabel}, ${money(q.price)}`,
      onclick: () => { if (q.id === p.id) return; track("variant_switched", { from: p.id, to: q.id, type: q.type }); openProduct(q); } },
      el("span", { class: "also-pic" }, el("img", { src: q.img, alt: "", loading: "lazy" })),
      el("span", { class: "also-l", text: q.typeLabel }), el("span", { class: "also-p", text: money(q.price) })));
    btns.forEach((b, i) => b.addEventListener("keydown", e => {   // radio-group arrow keys
      const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!k) return;
      e.preventDefault(); const n = btns[(i + k + btns.length) % btns.length]; n.focus(); n.click();
    }));
    $("#pdAlsoList").replaceChildren(...btns);
    const on = btns.find(b => b.getAttribute("aria-checked") === "true");
    const row = $("#pdAlsoList");   // center the selected one inside the row only (scrollIntoView would also scroll the page)
    if (on) requestAnimationFrame(() => { row.scrollLeft = Math.max(0, on.offsetLeft - (row.clientWidth - on.offsetWidth) / 2); });
  }
  function drawWith() {
    // 2 of the same type, plus up to 2 add-ons of other types with the same design or theme (socks, hats...)
    const fresh = q => !bag.some(i => i.id === q.id);
    const same = similar(cur, 4, size).filter(fresh);
    const others = P.filter(q => q.type !== cur.type && fresh(q) && designOf(q) !== designOf(cur) && q.theme === cur.theme)
      .sort((a, b) => a.sizes.length - b.sizes.length);
    const pick = [], seen = new Set();
    for (const q of others) { if (pick.length >= 2) break; if (!seen.has(q.type)) { seen.add(q.type); pick.push(q); } }
    const list = [...same.slice(0, 4 - pick.length), ...pick];
    $("#pdWith").hidden = !list.length || !$("#notifyForm").hidden;
    $("#pdWithList").replaceChildren(...list.map(q => {
      // two labels only: "+ Add" when it can be added right now (one size, or same item type in the size already picked), else "Choose size"
      const qOne = q.sizes.length === 1, qSize = qOne ? q.sizes[0] : q.type === cur.type && size && q.sizes.includes(size) ? size : null;
      return mini(q, el("button", { type: "button", class: "mini-add",
      text: qSize ? "+ Add" : "Choose size", "aria-label": qSize ? `Add ${q.name}, ${qOne ? q.typeLabel : qSize}` : `Choose a size for ${q.name}`,
      onclick: e => {
        if (!qSize) { track("suggestion_opened", { from: cur.id, to: q.id }); openProduct(q); return; }
        if (soldOut(q, qSize)) { e.currentTarget.textContent = qOne ? "Sold out" : `${qSize} sold out`; return; }
        if (!addToBag(q.id, qSize, 1, "buy_it_with")) return;
        e.currentTarget.textContent = "Added ✓"; e.currentTarget.disabled = true;
        $("#pdMsg").textContent = `Added ${q.name} (${qOne ? q.typeLabel : qSize}). `;
        $("#pdMsg").append(el("button", { class: "link", type: "button", text: "View list", onclick: () => { pd.close(); openBag(); } }));
      } }));
    }));
  }
  $("#notifyTabs").hidden = !C.SMS_ENABLED;
  function setMethod(m) {
    $("#notifyTabs").querySelectorAll("button").forEach(b => b.setAttribute("aria-checked", b.dataset.m === m));
    $("#notifyForm").querySelectorAll("[data-for]").forEach(l => l.hidden = l.dataset.for !== m);
    $("#nfEmail").required = m === "email"; $("#nfPhone").required = m === "text"; $("#nfConsent").required = m === "text";
    $("#notifyForm").dataset.m = m;
  }
  $("#notifyTabs").querySelectorAll("button").forEach(b => b.addEventListener("click", () => setMethod(b.dataset.m)));
  $("#notifyForm").addEventListener("submit", e => {
    e.preventDefault();
    const m = e.target.dataset.m || "email";
    const data = { type: "restock", product: `#${cur.id} ${cur.name} (${cur.color})`, size, method: m };
    if (m === "text") { data.phone = $("#nfPhone").value; data.sms_consent = "yes, one-time restock text"; } else data.email = $("#nfEmail").value;
    send(data, $("#pdMsg"), () => { $("#pdMsg").textContent = `You're on the list for ${size}.`; });
  });

  // ---------- recently viewed + previous ----------
  let trail = [];   // products opened in this visit, for the Previous button
  function remember(id) {
    if (trail[trail.length - 1] !== id) trail.push(id);
    const list = (store.get("recent") || []).filter(x => x !== id && byId[x]);
    list.unshift(id); store.set("recent", list.slice(0, 8));
    $("#rvBtn").hidden = false;
    const prev = trail.length > 1 ? byId[trail[trail.length - 2]] : null;
    $("#pdPrevBtn").hidden = !prev;
    if (prev) $("#pdPrevBtn").setAttribute("aria-label", `Back to ${prev.name}`);
  }
  $("#pdPrevBtn").addEventListener("click", () => {
    trail.pop(); const id = trail.pop(); if (byId[id]) openProduct(byId[id]);
  });
  const rv = $("#rv");
  $("#rvBtn").hidden = !(store.get("recent") || []).length;
  $("#rvBtn").addEventListener("click", () => { drawList("recent"); rv.showModal(); });
  $("#rvClear").addEventListener("click", () => {
    if (listKind === "saved") { store.set("saved", []); syncSave(); drawList("saved"); return; }
    store.set("recent", []); trail = []; drawList("recent"); $("#rvBtn").hidden = true; });

  // ---------- back to top ----------
  const top = $("#toTop");
  const onScroll = () => { top.hidden = window.scrollY < innerHeight * 1.5; };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  top.addEventListener("click", () => window.scrollTo({ top: 0, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" }));
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
    $("#pdImg").src = pics[gi].src; $("#pdImg").alt = `${cur.color} ${cur.typeLabel.toLowerCase()}, ${cur.name}: ${pics[gi].alt}`;
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

  // ---------- size guide (per item type; numbers come from config.js) ----------
  const GUIDE = {
    hoodie: { cols: [["chest", "Chest"], ["length", "Length"], ["sleeve", "Sleeve"]], how: ["Use a hoodie you own that fits the way you like. Lay it flat.",
      "Chest: armpit to armpit, then double it.", "Length: top of the shoulder next to the collar, straight down to the hem.", "Sleeve: center back of the collar to the end of the cuff."] },
    tee: { cols: [["chest", "Chest"], ["length", "Length"], ["sleeve", "Sleeve"]], how: ["Use a tee you own that fits the way you like. Lay it flat.",
      "Chest: armpit to armpit, then double it.", "Length: top of the shoulder next to the collar, straight down to the hem.", "Sleeve: shoulder seam to the end of the sleeve."] },
    underwear: { cols: [["waist", "Waist"], ["inseam", "Inseam"]], how: ["Measure around your waist where the waistband sits.",
      "Inseam: on boxers you own, crotch seam to the leg hem."] },
    socks: { cols: [["us_men", "US men's shoe"], ["us_women", "US women's shoe"]], how: ["Pick by your usual shoe size."] },
    sweatpants: { cols: [["waist", "Waist (relaxed)"], ["hip", "Hip"], ["inseam", "Inseam"]], how: ["Use sweatpants you own that fit the way you like. Lay them flat.",
      "Waist: edge to edge across the waistband, relaxed, then double it.", "Hip: edge to edge at the widest point, then double it.", "Inseam: crotch seam to the bottom of the cuff."] },
  };
  function sizeGuideFor(p) {
    const box = $("#sizeGuide"); box.replaceChildren();
    const g = GUIDE[p.type], u = C.SIZE_UNITS || "in";
    $("#sgBtn").hidden = !g;
    if (!g) return;
    const rows = (p.type === "hoodie" ? C.SIZE_CHART : ((C.SIZE_CHARTS || {})[p.type])) || [];
    const filled = rows.some(r => g.cols.some(([k]) => r[k]));
    const unit = p.type === "socks" ? "" : ` (${u})`;
    const ftx = fitText(p.type); if (ftx) box.append(el("p", { class: "sg-fit", text: ftx }));
    box.append(
      el("p", { class: "sg-title", text: "How to measure" }),
      el("ol", {}, ...g.how.map(t => el("li", { text: t }))),
      filled
        ? el("table", {}, el("thead", {}, el("tr", {}, ...["Size", ...g.cols.map(([, l]) => l + unit)].map(t => el("th", { text: t })))),
            el("tbody", {}, ...rows.map(r => el("tr", {}, ...[r.size, ...g.cols.map(([k]) => r[k] || "–")].map(t => el("td", { text: String(t) }))))))
        : el("p", { class: "sg-note", text: "Measurements coming soon." }),
      el("p", { class: "sg-note", text: "All sales are final, so please check before ordering." }));
  }
  $("#sgBtn").addEventListener("click", () => { const box = $("#sizeGuide"); box.hidden = !box.hidden; $("#sgBtn").setAttribute("aria-expanded", !box.hidden); });

  pd.addEventListener("close", () => { if (bySlug[location.hash.slice(1)]) history.replaceState(history.state, "", location.pathname + location.search); });
  $("#pdAdd").addEventListener("click", () => {
    if (!size) { $("#pdMsg").textContent = "Pick a size first."; return; }
    const n = clampQ($("#pdQty").value);
    const before = bagQty();
    if (!addToBag(cur.id, size, n)) return;
    $("#pdMsg").textContent = `Added ${bagQty() - before} × ${size}. `;
    $("#pdMsg").append(el("button", { class: "link", type: "button", text: "View list", onclick: () => { pd.close(); openBag(); } }));
  });
  $("#pdShare").addEventListener("click", async () => {
    const url = location.origin + location.pathname + "#" + cur.slug;
    try { await navigator.clipboard.writeText(url); $("#pdMsg").textContent = "Link copied."; }
    catch { $("#pdMsg").textContent = url; }
  });
  let backNav = false;
  function fromHash() {
    if (backNav) return;   // Back just closed a pop-up: don't reopen a product from the older link
    const p = bySlug[decodeURIComponent(location.hash.slice(1))];
    if (p) openProduct(p, false);
  }
  window.addEventListener("hashchange", fromHash);

  // Phone Back button closes pop-ups instead of leaving the shop: opening one adds a history step; closing it any other way removes that step.
  let backClosing = false, skipPop = false, keepY = null;
  // the browser restores an old scroll position when we step history back; hold the page where it is instead
  const holdY = y => { const f = () => { if (Math.abs(scrollY - y) > 1) scrollTo({ top: y, behavior: "instant" }); }; f(); requestAnimationFrame(f); };
  const anyOpen = () => !!document.querySelector("dialog[open]");
  document.querySelectorAll("dialog").forEach(d => {
    const show = d.showModal.bind(d);
    // scrollRestoration is stored per history entry and used when returning TO it: set it on the page's entry before adding the pop-up step
    d.showModal = () => { if (!(history.state && history.state.dlg)) { try { history.scrollRestoration = "manual"; } catch {} history.pushState({ dlg: 1 }, "", location.href); } show(); };
    d.addEventListener("close", () => {
      if (backClosing) return;
      setTimeout(() => { if (!anyOpen() && history.state && history.state.dlg) { skipPop = true; keepY = scrollY; history.back(); } }, 0);
    });
  });
  window.addEventListener("popstate", () => {
    if (skipPop || anyOpen()) { backNav = true; setTimeout(() => { backNav = false; }, 50); }   // only when Back is closing a pop-up, not for a new #product link
    setTimeout(() => { try { if (!(history.state && history.state.dlg)) history.scrollRestoration = "auto"; } catch {} }, 0);   // normal restore for real page visits
    if (skipPop) { skipPop = false; if (keepY != null) { holdY(keepY); keepY = null; } return; }
    const y = scrollY;
    if (anyOpen()) { requestAnimationFrame(() => holdY(y)); backClosing = true; document.querySelectorAll("dialog[open]").forEach(d => d.close()); backClosing = false; }
  });

  // close any dialog on backdrop click or close button
  document.querySelectorAll("dialog").forEach(d => {
    d.addEventListener("click", e => { if (e.target === d) d.close(); });
    d.querySelectorAll("[data-close]").forEach(b => b.addEventListener("click", () => d.close()));
  });

  // ---------- preorder list (saved in this browser) ----------
  const KEY = "preorder-list-v1";
  let bag = [];
  try { bag = JSON.parse(localStorage.getItem(KEY)) || []; } catch { bag = []; }
  bag = (Array.isArray(bag) ? bag : []).filter(i => i && byId[i.id] && byId[i.id].sizes.includes(i.size))
    .map(i => ({ id: i.id, size: i.size, qty: clampQ(i.qty) }));
  while (bag.reduce((s, i) => s + i.qty, 0) > MAXN) { const last = bag[bag.length - 1]; if (last.qty > 1) last.qty--; else bag.pop(); }
  function limitMsg(t) { const m = $("#pd").open ? $("#pdMsg") : $("#reqMsg"); m.textContent = t; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(bag)); } catch {} updateCount(); };
  const updateCount = () => { $("#bagCount").textContent = bag.reduce((s, i) => s + i.qty, 0); };
  const bagQty = () => bag.reduce((s, i) => s + i.qty, 0);
  function addToBag(id, sz, n, from) {
    const room = MAXN - bagQty();
    const hit0 = bag.find(i => i.id === id && i.size === sz);
    n = Math.min(n, room, MAXQ - (hit0 ? hit0.qty : 0));
    if (n <= 0) { limitMsg(hit0 && hit0.qty >= MAXQ ? `Limit is ${MAXQ} of the same item and size.` : `Limit is ${MAXN} items per order. Email us for bigger orders.`); return false; }
    track("added_to_list", { id, name: byId[id].name, size: sz, qty: n, from: from || "product" });
    const hit = bag.find(i => i.id === id && i.size === sz);
    if (hit) hit.qty = Math.min(MAXQ, hit.qty + n); else bag.push({ id, size: sz, qty: n });
    save(); return true;
  }
  const bagEl = $("#bag");
  function shipping(qty, subtotal) {
    if (!qty) return 0;
    const over = Number(C.FREE_SHIP_OVER) || 0, q = Number(C.FREE_SHIP_QTY) || 0;
    if ((over && subtotal >= over) || (q && qty >= q)) return 0;
    return Number(C.SHIPPING_FLAT) || 0;
  }
  function drawBag() {
    const box = $("#bagItems"); box.replaceChildren();
    if (!bag.length) box.append(el("p", { class: "note", text: "Your list is empty. Open something, pick a size and add it." }));
    bag.forEach((i, idx) => {
      const p = byId[i.id];
      box.append(el("div", { class: "bag-item" },
        el("div", { class: "tile" + (p.light ? " dark" : "") }, el("img", { src: p.img, alt: "" })),
        el("div", {}, el("h3", { text: p.name }), el("p", { text: `${p.typeLabel} · ${p.color} · ${p.sizes.length === 1 ? i.size : "Size " + i.size} · ${money(p.price)}` }),
          (p.notes || []).some(n => /latex/i.test(n)) ? el("p", { class: "bag-warn", text: "Contains natural rubber latex" }) : null,
          el("button", { class: "link", type: "button", text: "Remove", onclick: () => { bag.splice(idx, 1); save(); drawBag(); } })),
        el("input", { type: "number", min: 1, max: MAXQ, value: i.qty, "aria-label": `Quantity for ${p.name}`,
          onchange: e => { const others = bagQty() - i.qty; i.qty = Math.min(clampQ(e.target.value), MAXN - others); save(); drawBag(); } })));
    });
    const sub0 = bag.reduce((s, i) => s + byId[i.id].price * i.qty, 0), qty = bag.reduce((s, i) => s + i.qty, 0);
    const disc = setDiscount(bag), sub = sub0 - disc;
    const ship = shipping(qty, sub), over = Number(C.FREE_SHIP_OVER) || 0, fq = Number(C.FREE_SHIP_QTY) || 0;
    const needD = over ? over - sub : 0, need = fq ? fq - qty : 0, hasRule = !!(over || fq);
    $("#bagTotal").replaceChildren(...(bag.length ? [
      ship && over && needD > 0 ? el("p", { class: "ship-nudge", text: `Add ${money(needD)} more for free shipping.` })
      : ship && fq && need > 0 ? el("p", { class: "ship-nudge", text: `Add ${need} more item${need > 1 ? "s" : ""} for free shipping.` })
      : hasRule && !ship ? el("p", { class: "ship-nudge ok", text: "You've got free shipping." }) : null,
      el("div", { class: "sum" }, el("span", { text: "Subtotal" }), el("span", { text: money(sub0) })),
      disc ? el("div", { class: "sum" }, el("span", { text: "Set discount" }), el("span", { text: "−" + money(disc) })) : null,
      el("div", { class: "sum" }, el("span", { text: "Shipping" }), el("span", { text: ship ? money(ship) : "Free" })),
      el("div", { class: "sum total" }, el("span", { text: "Estimated total" }), el("span", { text: money(sub + ship) })),
      el("p", { class: "note", text: "Plus tax where it applies." + (SHIP_WINDOW ? ` ${SHIP_WINDOW}.` : "") })].filter(Boolean) : []));
    $("#reqForm").hidden = !bag.length;
    const qn = bagQty();
    $("#orderFlag").hidden = qn < LARGE;
    $("#orderFlag").textContent = qn >= MAXN ? `That's the most per order (${MAXN}). For bigger orders, email ${C.CONTACT_EMAIL}.`
      : `Large order (${qn} items): we'll confirm by email before sending a payment link.`;
  }
  $("#bagNote").textContent = `No payment now. Send the list and we'll email a ship date and payment link. Or email ${C.CONTACT_EMAIL} directly.`;
  function openBag() { drawBag(); $("#reqMsg").textContent = ""; formOpenedAt = Date.now(); bagEl.showModal(); }
  $("#bagBtn").addEventListener("click", openBag);

  // ---------- preorder request: anti-spam, limits, order id, evidence for disputes ----------
  let formOpenedAt = 0;
  // What the buyer agrees to with the tick box (recorded with each request, with the terms date, as proof of agreement)
  const POLICY = `I agree to the Terms of Sale dated ${cfg("POLICY_UPDATED") || "(undated)"} (policies page), including the warranty disclaimer and limit of liability. All sales are final. Check the size chart before ordering. If we send the wrong item or it's lost or damaged in shipping, email us within 7 days and we'll fix it.`;
  function catalogStamp() {   // short fingerprint of prices so you can spot an edited order
    let h = 0; const s = P.map(p => p.id + ":" + p.price).join("|");
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return h.toString(36);
  }
  function orderId() {
    const d = new Date(), r = Math.random().toString(36).slice(2, 6).toUpperCase();
    return `PO-${d.getFullYear() % 100}${String(d.getMonth() + 1).padStart(2, "0")}${String(d.getDate()).padStart(2, "0")}-${r}`;
  }
  function rateOk() {   // max 3 requests per 10 minutes from this browser
    const now = Date.now(), win = 10 * 60 * 1000;
    let log = []; try { log = JSON.parse(localStorage.getItem("req-log")) || []; } catch {}
    log = log.filter(t => now - t < win);
    if (log.length >= 3) return false;
    log.push(now); try { localStorage.setItem("req-log", JSON.stringify(log)); } catch {}
    return true;
  }
  const emailOk = s => /^[^\s@]{1,64}@[^\s@]{1,190}\.[a-z]{2,24}$/i.test(String(s || "").trim());
  $("#reqForm").addEventListener("submit", e => {
    e.preventDefault();
    const f = new FormData(e.target), msg = $("#reqMsg"), btn = $("#reqBtn");
    if (btn.disabled) return;
    if (f.get("_gotcha")) { msg.textContent = "Sent."; return; }                       // bot filled the hidden field: pretend, send nothing
    if (Date.now() - formOpenedAt < 2500) { msg.textContent = "Please check your details, then send."; return; }  // instant submits are bots
    const name = String(f.get("name") || "").trim().slice(0, 80), email = String(f.get("email") || "").trim().slice(0, 120);
    const note = String(f.get("note") || "").trim().slice(0, 500);
    if (name.length < 2) { msg.textContent = "Please enter your name."; return; }
    if (!emailOk(email)) { msg.textContent = "Please enter a valid email."; return; }
    if (!f.get("agree")) { msg.textContent = "Please confirm you checked the size guide."; return; }
    if (!bag.length) return;
    if (!rateOk()) { msg.textContent = `Too many requests from this device. Try again in a few minutes or email ${C.CONTACT_EMAIL}.`; return; }
    const qty = bagQty(), sub0 = bag.reduce((s, i) => s + byId[i.id].price * i.qty, 0), disc = setDiscount(bag), sub = sub0 - disc, ship = shipping(qty, sub);
    const id = orderId(), large = qty >= LARGE;
    const items = bag.map(i => `${i.qty} x #${i.id} ${byId[i.id].typeLabel.toUpperCase()}: ${byId[i.id].name} (${byId[i.id].color}, ${i.size}) @ ${money(byId[i.id].price)}`);
    const latex = bag.some(i => (byId[i.id].notes || []).some(n => /latex/i.test(n)));
    trackPurchase(bag.map(i => ({ id: i.id, name: byId[i.id].name, size: i.size, qty: i.qty })), sub, ship);
    btn.disabled = true;
    send({ type: "preorder", order_id: id, large_order: large ? "YES - verify before taking payment" : "no",
      name, email, note, items: items.join("\n"), item_count: qty,
      subtotal: money(sub0), set_discount: disc ? "-" + money(disc) : "none", shipping: money(ship), total: money(sub + ship), price_check: catalogStamp(),
      agreed_to: POLICY + (latex ? " I understand this order contains natural rubber latex (waistband elastic)." : ""), agreed_at: new Date().toISOString(), page: location.href.split("#")[0],
      _subject: `${large ? "[LARGE] " : ""}Preorder ${id} from ${name}` }, msg,
      () => { bag = []; save(); drawBag(); msg.textContent = `Sent. Your order number is ${id}. We'll email ${email} with a ship date and payment link.`; });
    setTimeout(() => { btn.disabled = false; }, 4000);
  });

  // ---------- sending requests ----------
  async function send(data, msg, done) {
    const endpoint = safeUrl(C.FORM_ENDPOINT);
    if (endpoint) {
      msg.textContent = "Sending…";
      try {
        const r = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) });
        if (!r.ok) throw new Error(r.status);
        msg.textContent = "Sent. We'll email you."; done && done();
      } catch { msg.textContent = `Couldn't send. Email ${C.CONTACT_EMAIL} instead.`; }
      return;
    }
    // no form service set up: open the visitor's email app with everything filled in
    const subject = data._subject || (data.type === "restock" ? `Restock alert: ${data.product} ${data.size}` : `Notify me: ${data.product}`);
    const body = Object.entries(data).filter(([k]) => k !== "type" && !k.startsWith("_")).map(([k, v]) => `${k}: ${v}`).join("\n");
    location.href = `mailto:${C.CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    msg.textContent = data.order_id
      ? `Your email app should open with order ${data.order_id}. Press Send there to finish. If it doesn't open, email ${C.CONTACT_EMAIL}.`
      : `Your email app should open. If not, email ${C.CONTACT_EMAIL}.`;
  }

  // ---------- save / wishlist (device only) ----------
  function toggleSave(p) {
    let ids = savedIds(); const on = !ids.includes(p.id);
    ids = on ? [p.id, ...ids].slice(0, 50) : ids.filter(x => x !== p.id);
    store.set("saved", ids);
    if (on) track("saved", { id: p.id, name: p.name });
    syncSave();
  }
  function syncSave() {
    const ids = savedIds();
    document.querySelectorAll(".save-heart").forEach(b => b.setAttribute("aria-pressed", String(ids.includes(Number(b.dataset.id)))));
    if (cur) { const on = ids.includes(cur.id); $("#pdSave").setAttribute("aria-pressed", String(on)); $("#pdSave").textContent = on ? "♥ Saved" : "♡ Save"; }
    $("#svBtn").hidden = !ids.length; $("#svCount").textContent = ids.length ? String(ids.length) : "";
  }
  $("#pdSave").addEventListener("click", () => cur && toggleSave(cur));
  let listKind = "recent";
  function drawList(kind) {
    listKind = kind;
    const saved = kind === "saved";
    $("#rvTitle").textContent = saved ? "Saved" : "Recently viewed";
    $("#tabSaved").setAttribute("aria-selected", String(saved)); $("#tabRecent").setAttribute("aria-selected", String(!saved));
    $("#rvClear").textContent = saved ? "Clear saved" : "Clear history";
    const list = (saved ? savedIds() : (store.get("recent") || [])).map(id => byId[id]).filter(Boolean);
    $("#rvClear").hidden = !list.length;
    $("#rvList").replaceChildren(...(list.length ? list.map(p => el("div", { class: "rv-row" },
      el("button", { type: "button", class: "rv-item", onclick: () => { rv.close(); openProduct(p); } },
        el("div", { class: "tile" }, el("img", { src: p.img, alt: "" })),
        el("span", { class: "rv-name", text: p.name }), el("span", { class: "rv-price", text: `${p.typeLabel} · ${money(p.price)}` })),
      saved ? el("button", { type: "button", class: "link rv-x", "aria-label": `Remove ${p.name} from saved`, text: "Remove", onclick: () => { toggleSave(p); drawList("saved"); } }) : null))
      : [el("p", { class: "note", text: saved ? "Nothing saved yet. Tap the heart on anything you like." : "Nothing yet. Items you open show up here." })]));
  }
  $("#tabSaved").addEventListener("click", () => drawList("saved"));
  $("#tabRecent").addEventListener("click", () => drawList("recent"));
  $("#svBtn").addEventListener("click", () => { drawList("saved"); rv.showModal(); });

  // ---------- get the set: hoodie + sweatpants in the same design ----------
  const SET_PAIR = { hoodie: "sweatpants", sweatpants: "hoodie" };
  const setPick = {};
  function drawSet() {
    const box = $("#pdSet"), p = cur;
    const other = p && SET_PAIR[p.type] ? P.find(q => q.type === SET_PAIR[p.type] && designOf(q) === designOf(p)) : null;
    box.hidden = !other || !$("#notifyForm").hidden;
    if (box.hidden) return;
    const pair = p.type === "hoodie" ? [p, other] : [other, p];
    pair.forEach(q => { if (!setPick[q.id] || !q.sizes.includes(setPick[q.id])) setPick[q.id] = (q.id === p.id && size) || store.get("last-size-" + q.type) || (q.type === "hoodie" ? store.get("last-size") : null) || null; });
    if (size) setPick[p.id] = size;
    const total = pair.reduce((s, q) => s + q.price, 0);
    const rows = pair.map(q => el("div", { class: "set-row" },
      el("span", { class: "set-pic" }, el("img", { src: q.img, alt: "" })),
      el("div", { class: "set-info" },
        el("span", { class: "set-name", text: `${q.typeLabel} · ${money(q.price)}` }),
        el("div", { class: "set-sizes", role: "radiogroup", "aria-label": `${q.typeLabel} size` },
          ...q.sizes.map(sz => el("button", { type: "button", role: "radio", "aria-checked": String(setPick[q.id] === sz), class: soldOut(q, sz) ? "is-out" : "", text: sz,
            "aria-label": soldOut(q, sz) ? `${q.typeLabel} ${sz}, sold out` : `${q.typeLabel} ${sz}`,
            onclick: () => { setPick[q.id] = sz; drawSet(); } }))))));
    const btn = el("button", { type: "button", class: "btn wide set-add", text: SET_OFF ? `Add both · ${money(total - SET_OFF)} (save ${money(SET_OFF)})` : `Add both · ${money(total)}`,
      onclick: () => {
        const miss = pair.filter(q => !setPick[q.id]);
        if (miss.length) { $("#pdMsg").textContent = `Pick a size for the ${miss.map(q => q.typeLabel.toLowerCase()).join(" and ")}.`; return; }
        const out = pair.filter(q => soldOut(q, setPick[q.id]));
        if (out.length) { $("#pdMsg").textContent = `${out.map(q => `${q.typeLabel} ${setPick[q.id]}`).join(" and ")} is sold out. Pick another size.`; return; }
        const ok = pair.map(q => addToBag(q.id, setPick[q.id], 1, "set"));
        if (!ok.every(Boolean)) return;
        pair.forEach(q => store.set("last-size-" + q.type, setPick[q.id]));
        track("set_added", { design: designOf(p), hoodie: setPick[pair[0].id], sweatpants: setPick[pair[1].id] });
        $("#pdMsg").textContent = `Added the set: hoodie ${setPick[pair[0].id]} + sweatpants ${setPick[pair[1].id]}. `;
        $("#pdMsg").append(el("button", { class: "link", type: "button", text: "View list", onclick: () => { pd.close(); openBag(); } }));
      } });
    $("#pdSetBody").replaceChildren(el("p", { class: "set-note", text: SET_OFF ? `Hoodie + sweatpants in this design. ${money(SET_OFF)} off when both are in your order.` : "Hoodie + sweatpants in this design." }), ...rows, btn);
  }
  // set discount: one per hoodie + sweatpants pair of the same design in the list
  function setDiscount(items) {
    if (!SET_OFF) return 0;
    const by = {};
    items.forEach(i => { const q = byId[i.id]; if (!q || !SET_PAIR[q.type]) return; const d = by[designOf(q)] = by[designOf(q)] || { hoodie: 0, sweatpants: 0 }; d[q.type] += i.qty; });
    return Object.values(by).reduce((s, d) => s + Math.min(d.hoodie, d.sweatpants), 0) * SET_OFF;
  }

  // ---------- small drop-alert card (once; not again for 30 days; never after joining) ----------
  const dropCard = $("#dropCard"), DAY = 864e5;
  let opens = 0, dropShown = false;
  const dropState = () => store.get("drop-prompt") || {};
  function dropAllowed() { const s = dropState(); return C.DROP_PROMPT !== false && !s.joined && !(s.until > Date.now()) && !dropShown; }
  function showDrop() {
    if (!dropAllowed()) return;
    if (document.querySelector("dialog[open]")) { setTimeout(showDrop, 4000); return; }   // never on top of another pop-up
    dropShown = true; dropCard.hidden = false; track("drop_prompt_shown", {});
  }
  function hideDrop(days) { dropCard.hidden = true; store.set("drop-prompt", { ...dropState(), until: Date.now() + days * DAY }); }
  $("#dropCardX").addEventListener("click", () => hideDrop(30));
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !dropCard.hidden) hideDrop(30); });
  $("#dropCardForm").addEventListener("submit", e => { e.preventDefault();
    const email = e.target.querySelector("input").value.trim();
    if (!emailOk(email)) { $("#dropCardMsg").textContent = "Please enter a valid email."; return; }
    store.set("drop-prompt", { ...dropState(), joined: true });
    track("drop_prompt_joined", {});
    send({ type: "notify", product: "Drop alerts", email }, $("#dropCardMsg"));
    setTimeout(() => { dropCard.hidden = true; }, 3500); });
  if (dropAllowed()) setTimeout(showDrop, 30000);
  const noteOpen = () => { opens++; if (opens === 2) showDrop(); };

  // ---------- About section (only when filled in config) ----------
  (() => {
    const A = C.ABOUT || {}, text = typeof A.text === "string" ? A.text.trim() : "";
    if (!text) return;
    $("#story").hidden = false;
    if (typeof A.title === "string" && A.title.trim()) $("#storyTitle").textContent = A.title.trim();
    $("#storyText").replaceWith(...text.split(/\n\s*\n/).map(t => el("p", { class: "story-text", text: t.trim() })));
    const ph = typeof A.photo === "string" ? A.photo.trim() : "";
    if (/^[\w\-./]+\.(jpe?g|png|webp|svg)$/i.test(ph) && !ph.startsWith("/") && !ph.includes("..")) { $("#storyPhoto").src = ph; $("#storyPhoto").hidden = false; }
    document.querySelectorAll("[data-story-link]").forEach(a => { a.hidden = false; });
  })();

  // ---------- footer: drop alerts + social links ----------
  $("#dropForm").addEventListener("submit", e => { e.preventDefault();
    store.set("drop-prompt", { ...(store.get("drop-prompt") || {}), joined: true });
    send({ type: "notify", product: "Drop alerts", email: e.target.querySelector("input").value }, $("#dropMsg")); });
  const soc = [["Instagram", safeUrl(C.INSTAGRAM)], ["TikTok", safeUrl(C.TIKTOK)]].filter(([, u]) => u);
  $("#social").append(...soc.map(([n, u]) => el("a", { href: u, rel: "noopener", text: n })));

  $("#heroShip").replaceChildren(...(ONE ? [el("strong", { text: `Every ${LIVE[0].one} ${money(ONE)}` }), " · "] : EACH ? [el("strong", { text: "One price per item" }), " · "] : []), shipLine());
  const sf = document.querySelector("[data-ship-faq]");
  if (sf) sf.textContent = `${shipLine()}. ${SHIP_WINDOW ? SHIP_WINDOW + ". " : ""}Shipping is shown on each product and in your preorder list before you send anything. US only for now.`;
  // footer legal line: business name + address once set
  const legal = document.querySelector("[data-business]");
  if (legal) legal.textContent = [cfg("BUSINESS_NAME"), cfg("BUSINESS_ADDRESS")].filter(Boolean).join(" · ");

  syncSave(); updateCount(); render(); fromHash();
})();

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
  // One price for everything? Then prices come off the cards and the shop says it once, clearly.
  const PRICES = [...new Set(P.map(p => p.price))], ONE = PRICES.length === 1 ? PRICES[0] : null;
  const shipLine = () => {
    const f = Number(C.SHIPPING_FLAT) || 0, q = C.FREE_SHIP_QTY;
    if (!f) return "Free shipping";
    return q ? `${money(f)} shipping · free on ${q}+` : `${money(f)} shipping`;
  };
  const MAXQ = Math.max(1, Number(C.MAX_QTY_PER_ITEM) || 3), MAXN = Math.max(1, Number(C.MAX_ITEMS_PER_ORDER) || 8);
  const LARGE = Number(C.LARGE_ORDER_ITEMS) || 4;
  const clampQ = n => Math.max(1, Math.min(MAXQ, parseInt(n, 10) || 1));
  const safeUrl = u => /^https:\/\/[^\s"'<>]+$/i.test(String(u || "")) ? u : "";
  const byId = Object.fromEntries(P.map(p => [p.id, p]));
  const bySlug = Object.fromEntries(P.map(p => [p.slug, p]));

  // ---------- branding ----------
  document.title = `${C.BRAND} | Dark-humor hoodies, no plastic`;
  document.querySelectorAll("[data-brand]").forEach(n => n.textContent = C.BRAND);
  document.querySelectorAll("[data-contact]").forEach(a => { a.href = "mailto:" + C.CONTACT_EMAIL; a.textContent = C.CONTACT_EMAIL; });
  $("[data-tagline]").textContent = C.TAGLINE;
  $("[data-featured-label]").textContent = C.FEATURED_LABEL;
  $("#year").textContent = new Date().getFullYear();

  // ---------- cards ----------
  function card(p) {
    const back = (p.imgs && p.imgs[1] && p.imgs[1].src) || p.img;
    const stage = el("div", { class: "stage" },
      el("div", { class: "turn" },
        el("img", { class: "face front", src: p.img, alt: `${p.color} hoodie, ${p.placement.toLowerCase()}: ${p.name}`, loading: "lazy", width: 560, height: 570, draggable: "false" }),
        el("img", { class: "face back", "data-src": back, alt: "", width: 560, height: 570, draggable: "false" })),
      el("span", { class: "shadow", "aria-hidden": "true" }),
      el("span", { class: "spin-ico", "aria-hidden": "true", text: "\u21BB" }));
    const c = el("button", { class: "card", type: "button", "aria-label": `${p.name}, ${p.color}, ${money(p.price)}. Left and right arrows turn it.`, onclick: () => openProduct(p) },
      stage,
      ONE ? null : el("p", { class: "price", text: money(p.price) }),
      el("h3", { text: p.name }),
      el("div", { class: "row" },
        el("span", {}, el("span", { class: "swatch", style: `background:${p.hex}` }), p.color)));
    spinnable(stage, c);
    return c;
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
      el("div", { class: "tile" }, el("img", { src: p.img, alt: `${p.color} hoodie: ${p.name}`, width: 560, height: 570, draggable: "false" })),
      el("span", { class: "shadow", "aria-hidden": "true" }),
      ONE ? null : el("p", { class: "price", text: money(p.price) })));
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
    const items = [...sel.options].map(o => {
      const soon = /\(coming soon\)/.test(o.text);
      const m = o.text.replace(/\s*\(coming soon\)/, "").match(/^(.*?)(?:\s*\((\d+)\))?$/);
      let label = m[1], n = m[2];
      if (o.value === "") label = sel.id === "fCat" ? "All" : sel.id === "fTheme" ? "All themes" : "All colors";
      const b = el("button", { type: "button", class: "chip" + (soon ? " is-soon" : ""), role: "radio", "data-v": o.value, "aria-label": o.text },
        sel.id === "fColor" && o.value ? el("span", { class: "sw", style: `background:${colorHex[o.value]}` }) : null,
        el("span", { text: label }),
        n && sel.id !== "fCat" ? el("span", { class: "n", text: n }) : null,
        soon ? el("span", { class: "tag", text: "soon" }) : null);
      b.addEventListener("click", () => { if (sel.value !== o.value) { sel.value = o.value; sel.dispatchEvent(new Event("change")); } sync(); });
      return b;
    });
    box.append(...items);
    box.addEventListener("keydown", e => {   // arrow keys move between chips in the same row
      const i = items.indexOf(document.activeElement); if (i < 0) return;
      const k = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : e.key === "Home" ? 0 : e.key === "End" ? items.length - 1 : null;
      if (k === null) return; e.preventDefault();
      const t = items[Math.max(0, Math.min(items.length - 1, k))]; t.focus(); t.click();
    });
    function sync() {
      items.forEach(b => { const on = b.dataset.v === sel.value; b.setAttribute("aria-checked", on); b.tabIndex = on ? 0 : -1; });
      const on = items.find(b => b.dataset.v === sel.value);
      if (on && box.scrollWidth > box.clientWidth) {   // keep the selected chip in view in its row
        const l = on.offsetLeft - box.offsetLeft, r = l + on.offsetWidth;
        if (l < box.scrollLeft || r > box.scrollLeft + box.clientWidth) box.scrollTo({ left: l - 16, behavior: "smooth" });
      }
    }
    const api = { sync, close() {}, wrap: box };
    menus.push(api); return api;
  }
  [fCat, fTheme, fColor, fSort].forEach(chips);

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
    const words = searchWords(fSearch.value);
    let list = P.filter(p =>
      (!fCat.value || p.type === fCat.value) && (!fTheme.value || p.theme === fTheme.value) &&
      (!fColor.value || p.color === fColor.value) &&
      words.every(w => haystack(p).includes(w)));
    if (fSort.value === "az") list.sort((a, b) => a.name.localeCompare(b.name));
    else if (fSort.value === "new") list.sort((a, b) => b.id - a.id);
    else list.sort((a, b) => (a.featured || 999) - (b.featured || 999) || a.id - b.id);
    $("#resultCount").textContent = `${list.length} ${list.length === 1 ? "hoodie" : "hoodies"}` + (ONE ? ` · ${money(ONE)} each` : "");
    if (!list.length) {
      const tips = ["skull", "coffin", "grief", "gym", "rot", "black"];
      grid.append(el("div", { class: "empty" },
        el("p", { text: words.length ? `No hoodies match "${fSearch.value.trim()}".` : "Nothing matches these filters." }),
        el("p", { class: "tips" }, "Try: ", ...tips.map(w => el("button", { type: "button", class: "chip", text: w,
          onclick: () => { fCat.value = fTheme.value = fColor.value = ""; fSearch.value = w; render(); } })))));
      track("search_no_results", { q: fSearch.value.trim() });
    }
    else grid.append(...list.map(card));
    writeURL();
  }

  // search: ignore filler words, map common shopper words, match picture tags too
  const STOP = new Set(["hoodie", "hoodies", "sweatshirt", "sweater", "hoody", "a", "an", "the", "with", "and", "of", "for", "shirt", "pullover"]);
  const ALIAS = { "3am": "3 a.m.", "3": "3 a.m.", "skulls": "skull", "skeletons": "skeleton", "coffins": "coffin", "graves": "grave", "funny": "", "dark": "",
    "sad": "grief", "depressed": "grief", "depression": "grief", "anxiety": "grief", "mental": "grief", "workout": "gym", "lifting": "lift", "weights": "gym",
    "gray": "grey", "dead": "dead", "zip": "", "up": "", "xl": "", "xxl": "", "2xl": "", "3xl": "", "small": "", "medium": "", "large": "" };
  function searchWords(q) {
    return q.toLowerCase().replace(/[^a-z0-9.' -]/g, " ").split(/\s+/).filter(Boolean)
      .map(w => (w in ALIAS ? ALIAS[w] : w)).filter(w => w && !STOP.has(w));
  }
  const hay = {};
  const haystack = p => hay[p.id] || (hay[p.id] = `${p.name} ${p.sub} ${p.color} ${p.colorNote} ${CAT.themes[p.theme]} ${p.placement} ${p.tags || ""}`.toLowerCase());

  function soonCard(t) {
    const msg = el("p", { class: "pd-msg", role: "status" });
    const email = el("input", { type: "email", required: true, placeholder: "you@email.com", "aria-label": "Email" });
    return el("div", { class: "soon" },
      el("h3", { text: `${t.label} are coming` }),
      el("p", { text: `Same rules as the hoodies: natural fiber, no plastic. Planned price around ${money(t.price)}. Leave your email and you'll hear first.` }),
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
    $("#pdPrice").replaceChildren(money(p.price), ONE ? el("span", { class: "same-price", text: "Same price for every design" }) : "");
    $("#pdShip").textContent = shipLine();
    $("#pdQty").value = 1; $("#pdMsg").textContent = "";
    const out = (C.SOLD_OUT && C.SOLD_OUT[p.id]) || [];
    $("#pdSizes").replaceChildren(...p.sizes.map(s => el("button", { type: "button", "aria-pressed": "false", "data-s": s,
      class: out.includes(s) ? "is-out" : "", "aria-label": out.includes(s) ? `${s}, sold out` : s, text: s,
      onclick: () => pickSize(s, false) })));
    $("#sizeNote").textContent = "";
    track("product_viewed", { id: p.id, name: p.name, theme: p.theme, color: p.color });
    const remembered = store.get("last-size");
    if (remembered && p.sizes.includes(remembered)) pickSize(remembered, true); else setBuyMode(false);
    $("#pdBody").scrollTop = 0; pd.scrollTop = 0;
    $("#pdDetails").replaceChildren(...[
      `Color: ${p.colorNote}`, "~30% hemp / 70% cotton brushed fleece, heavyweight",
      "Cotton rib, thread, drawcord and labels. No plastic.", `${p.placement}, natural-dye or embroidered`,
      "Natural dyes fade gradually with sun and washing", "Preorder: no charge until we confirm a ship date",
      "All sales final: check the size guide",
    ].map(s => el("li", { text: s })));
    if (push) history.replaceState(null, "", location.pathname + location.search + "#" + p.slug);
    remember(p.id);
    if (!pd.open) pd.showModal();
    $("#pdName").focus({ preventScroll: true }); // start on the product name, not the close button
  }

  // ---------- small storage helper (works even if storage is blocked) ----------
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };

  // ---------- size memory + sold-out sizes ----------
  function pickSize(s, auto) {
    size = s;
    const out = ((C.SOLD_OUT && C.SOLD_OUT[cur.id]) || []).includes(s);
    $("#pdSizes").querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b.dataset.s === s));
    $("#pdMsg").textContent = "";
    if (!auto) store.set("last-size", s);
    $("#sizeNote").textContent = auto ? (out ? `Your size (${s}) is sold out in this one.` : `Size ${s} selected (your last size).`) : (out ? `${s} is sold out.` : "");
    setBuyMode(out);
  }
  function setBuyMode(out) {
    $("#pdAdd").hidden = out; $(".qty").hidden = out;
    $("#notifyForm").hidden = !out;
    if (out) { $("#notifyTitle").textContent = `Tell me when ${size} is back`; setMethod("email"); }
    drawAlts(out);
    drawWith();
  }
  const soldOut = (p, s) => ((C.SOLD_OUT && C.SOLD_OUT[p.id]) || []).includes(s);
  function similar(p, n, s) {   // same theme first, then same color, never the same hoodie; only ones in size s if given
    const ok = q => q.id !== p.id && (!s || !soldOut(q, s));
    const a = P.filter(q => ok(q) && q.theme === p.theme), b = P.filter(q => ok(q) && q.theme !== p.theme && q.color === p.color);
    return [...a, ...b].slice(0, n);
  }
  function mini(q, btn) {
    return el("div", { class: "mini" },
      el("button", { type: "button", class: "mini-open", "aria-label": `View ${q.name}`, onclick: () => { track("suggestion_opened", { from: cur.id, to: q.id }); openProduct(q); } },
        el("div", { class: "tile" }, el("img", { src: q.img, alt: "", loading: "lazy" })),
        ONE ? null : el("span", { class: "mini-price", text: money(q.price) }), el("span", { class: "mini-name", text: q.name })), btn || null);
  }
  function drawAlts(out) {
    const box = $("#pdAlts");
    if (!out) { box.hidden = true; return; }
    const list = similar(cur, 4, size);
    box.hidden = !list.length;
    $("#pdAltsTitle").textContent = `Available in ${size}`;
    $("#pdAltsList").replaceChildren(...list.map(q => mini(q)));
  }
  function drawWith() {
    const list = similar(cur, 4, size).filter(q => !bag.some(i => i.id === q.id));
    $("#pdWith").hidden = !list.length || !$("#notifyForm").hidden;
    $("#pdWithList").replaceChildren(...list.map(q => mini(q, el("button", { type: "button", class: "mini-add",
      text: size ? `+ Add ${size}` : "Pick size",
      onclick: e => {
        if (!size) { $("#pdMsg").textContent = "Pick a size first, then tap + Add."; return; }
        if (soldOut(q, size)) { e.currentTarget.textContent = `${size} sold out`; return; }
        if (!addToBag(q.id, size, 1, "buy_it_with")) return;
        e.currentTarget.textContent = "Added ✓"; e.currentTarget.disabled = true;
        $("#pdMsg").textContent = `Added ${q.name} (${size}). `;
        $("#pdMsg").append(el("button", { class: "link", type: "button", text: "View list", onclick: () => { pd.close(); openBag(); } }));
      } }))));
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
  function drawRecent() {
    const list = (store.get("recent") || []).map(id => byId[id]).filter(Boolean);
    $("#rvList").replaceChildren(...(list.length ? list.map(p => el("button", { type: "button", class: "rv-item", onclick: () => { rv.close(); openProduct(p); } },
      el("div", { class: "tile" }, el("img", { src: p.img, alt: "" })),
      el("span", { class: "rv-name", text: p.name }), ONE ? null : el("span", { class: "rv-price", text: money(p.price) })))
      : [el("p", { class: "note", text: "Nothing yet. Hoodies you open show up here." })]));
  }
  $("#rvBtn").hidden = !(store.get("recent") || []).length;
  $("#rvBtn").addEventListener("click", () => { drawRecent(); rv.showModal(); });
  $("#rvClear").addEventListener("click", () => { store.set("recent", []); trail = []; drawRecent(); $("#rvBtn").hidden = true; });

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
    if (n <= 0) { limitMsg(hit0 && hit0.qty >= MAXQ ? `Limit is ${MAXQ} of the same hoodie and size.` : `Limit is ${MAXN} hoodies per order. Email us for bigger orders.`); return false; }
    track("added_to_list", { id, name: byId[id].name, size: sz, qty: n, from: from || "product" });
    const hit = bag.find(i => i.id === id && i.size === sz);
    if (hit) hit.qty = Math.min(MAXQ, hit.qty + n); else bag.push({ id, size: sz, qty: n });
    save(); return true;
  }
  const bagEl = $("#bag");
  function shipping(qty, subtotal) {
    if (!qty) return 0;
    if (C.FREE_SHIP_QTY && qty >= C.FREE_SHIP_QTY) return 0;
    return Number(C.SHIPPING_FLAT) || 0;
  }
  function drawBag() {
    const box = $("#bagItems"); box.replaceChildren();
    if (!bag.length) box.append(el("p", { class: "note", text: "Your list is empty. Open a hoodie, pick a size and add it." }));
    bag.forEach((i, idx) => {
      const p = byId[i.id];
      box.append(el("div", { class: "bag-item" },
        el("div", { class: "tile" + (p.light ? " dark" : "") }, el("img", { src: p.img, alt: "" })),
        el("div", {}, el("h3", { text: p.name }), el("p", { text: `${p.color} · Size ${i.size} · ${money(p.price)}` }),
          el("button", { class: "link", type: "button", text: "Remove", onclick: () => { bag.splice(idx, 1); save(); drawBag(); } })),
        el("input", { type: "number", min: 1, max: MAXQ, value: i.qty, "aria-label": `Quantity for ${p.name}`,
          onchange: e => { const others = bagQty() - i.qty; i.qty = Math.min(clampQ(e.target.value), MAXN - others); save(); drawBag(); } })));
    });
    const sub = bag.reduce((s, i) => s + byId[i.id].price * i.qty, 0), qty = bag.reduce((s, i) => s + i.qty, 0);
    const ship = shipping(qty, sub), need = C.FREE_SHIP_QTY ? C.FREE_SHIP_QTY - qty : 0;
    $("#bagTotal").replaceChildren(...(bag.length ? [
      need > 0 ? el("p", { class: "ship-nudge", text: `Add ${need} more hoodie${need > 1 ? "s" : ""} for free shipping.` })
               : C.FREE_SHIP_QTY ? el("p", { class: "ship-nudge ok", text: "You've got free shipping." }) : null,
      el("div", { class: "sum" }, el("span", { text: "Subtotal" }), el("span", { text: money(sub) })),
      el("div", { class: "sum" }, el("span", { text: "Shipping" }), el("span", { text: ship ? money(ship) : "Free" })),
      el("div", { class: "sum total" }, el("span", { text: "Estimated total" }), el("span", { text: money(sub + ship) })),
      el("p", { class: "note", text: "Nothing is charged now." })] : []));
    $("#reqForm").hidden = !bag.length;
    const qn = bagQty();
    $("#orderFlag").hidden = qn < LARGE;
    $("#orderFlag").textContent = qn >= MAXN ? `That's the most per order (${MAXN}). For bigger orders, email ${C.CONTACT_EMAIL}.`
      : `Large order (${qn} hoodies): we'll confirm by email before sending a payment link.`;
  }
  $("#bagNote").textContent = `No payment now. Send the list and we'll email a ship date and payment link. Or email ${C.CONTACT_EMAIL} directly.`;
  function openBag() { drawBag(); $("#reqMsg").textContent = ""; formOpenedAt = Date.now(); bagEl.showModal(); }
  $("#bagBtn").addEventListener("click", openBag);

  // ---------- preorder request: anti-spam, limits, order id, evidence for disputes ----------
  let formOpenedAt = 0;
  const POLICY = "All sales are final. Check the size chart before ordering. If we send the wrong item or it's lost or damaged in shipping, email us within 7 days and we'll fix it.";
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
    const qty = bagQty(), sub = bag.reduce((s, i) => s + byId[i.id].price * i.qty, 0), ship = shipping(qty, sub);
    const id = orderId(), large = qty >= LARGE;
    const items = bag.map(i => `${i.qty} x #${i.id} ${byId[i.id].name} (${byId[i.id].color}, ${i.size}) @ ${money(byId[i.id].price)}`);
    trackPurchase(bag.map(i => ({ id: i.id, name: byId[i.id].name, size: i.size, qty: i.qty })), sub, ship);
    btn.disabled = true;
    send({ type: "preorder", order_id: id, large_order: large ? "YES - verify before taking payment" : "no",
      name, email, note, items: items.join("\n"), item_count: qty,
      subtotal: money(sub), shipping: money(ship), total: money(sub + ship), price_check: catalogStamp(),
      agreed_to: POLICY, agreed_at: new Date().toISOString(), page: location.href.split("#")[0],
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

  // ---------- footer: drop alerts + social links ----------
  $("#dropForm").addEventListener("submit", e => { e.preventDefault();
    send({ type: "notify", product: "Drop alerts", email: e.target.querySelector("input").value }, $("#dropMsg")); });
  const soc = [["Instagram", safeUrl(C.INSTAGRAM)], ["TikTok", safeUrl(C.TIKTOK)]].filter(([, u]) => u);
  $("#social").append(...soc.map(([n, u]) => el("a", { href: u, rel: "noopener", text: n })));

  $("#heroShip").replaceChildren(...(ONE ? [el("strong", { text: `Every hoodie ${money(ONE)}` }), " · "] : []), shipLine());
  const op = $("#onePrice"); if (op) { op.hidden = !ONE; if (ONE) op.replaceChildren(el("span", { class: "op-k", text: "One price" }), el("span", { class: "op-v", text: money(ONE) }), el("span", { class: "op-s", text: "every design" })); }
  const sf = document.querySelector("[data-ship-faq]");
  if (sf) sf.textContent = `${shipLine()}. Shipping is shown on each product and in your preorder list before you send anything.`;

  updateCount(); render(); fromHash();
})();

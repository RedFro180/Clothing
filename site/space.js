// Moving cosmic background, drawn on <canvas id="space"> behind the page.
// Depth comes from layers that move at different speeds (far = slow, near = fast), both over
// time and when the page scrolls or the mouse moves:
//   1. deep field: thousands of faint stars + a milky-way band, panning very slowly
//   2. two nebula cloud layers in purple/magenta/blue, drifting at different speeds
//   3. a distant spiral galaxy, slowly turning
//   4. three layers of bright twinkling stars
//   5. random shooting stars from random directions, sometimes two at once
// Pauses when the tab is hidden; one still frame if the visitor prefers reduced motion.
(() => {
  "use strict";
  const cv = document.getElementById("space");
  if (!cv || !cv.getContext) return;
  const ctx = cv.getContext("2d");
  const still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const rnd = (a, b) => a + Math.random() * (b - a);
  let W = 0, H = 0, dpr = 1, t = 0, last = 0;
  let deep, neb1, neb2, galaxy, stars = [], shooters = [], nextShoot = 1200;
  let scrollY = window.scrollY || 0, mx = 0, my = 0, smx = 0, smy = 0;

  // a soft round blob drawn so it wraps around the edges (image tiles join without seams)
  function wrapBlob(g, w, h, x, y, r, color) {
    for (const dx of [-w, 0, w]) for (const dy of [-h, 0, h]) {
      const cx = x + dx, cy = y + dy;
      if (cx + r < 0 || cx - r > w || cy + r < 0 || cy - r > h) continue;
      const rg = g.createRadialGradient(cx, cy, 0, cx, cy, r);
      rg.addColorStop(0, color); rg.addColorStop(1, "rgba(0,0,0,0)");
      g.fillStyle = rg; g.fillRect(cx - r, cy - r, r * 2, r * 2);
    }
  }

  function offscreen(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }

  // 1. deep field: tiny stars + a soft milky-way band, twice the screen so it can pan and wrap
  function makeDeep() {
    const w = Math.round(W * 2), h = Math.round(H * 1.6), c = offscreen(w, h), g = c.getContext("2d");
    const n = Math.min(5000, Math.round(w * h / 700));
    for (let i = 0; i < n; i++) {
      g.fillStyle = `rgba(255,255,255,${rnd(0.08, 0.5).toFixed(2)})`;
      g.fillRect(Math.random() * w, Math.random() * h, rnd(0.4, 1.1), rnd(0.4, 1.1));
    }
    // milky-way band: dense dust along a wave that repeats exactly across the width, so tiles join seamlessly
    const bandY = u => h * 0.5 + Math.sin(u * Math.PI * 2) * h * 0.18;
    for (let i = 0; i < n * 1.4; i++) {
      const u = Math.random(), off = (Math.random() + Math.random() + Math.random() - 1.5) * h * 0.12;
      g.fillStyle = `rgba(${Math.random() < 0.3 ? "230,190,255" : "255,255,255"},${rnd(0.04, 0.35).toFixed(2)})`;
      g.fillRect(u * w, bandY(u) + off, rnd(0.4, 1.2), rnd(0.4, 1.2));
    }
    for (let i = 0; i < 40; i++) {   // soft glow along the band, wrapped at the edges
      const u = i / 40, r = h * 0.16;
      wrapBlob(g, w, h, u * w, bandY(u), r, "rgba(185,135,255,0.07)");
    }
    return c;
  }

  // 2. nebula layer: many soft colored blobs, rendered small and scaled up (stays soft, cheap)
  function makeNebula(hues, count, alpha) {
    const w = 360, h = Math.round(360 * (H / W) * 1.6) || 360, c = offscreen(w, h), g = c.getContext("2d");
    g.globalCompositeOperation = "lighter";
    for (let i = 0; i < count; i++) {
      const [hr, hg, hb] = hues[Math.floor(Math.random() * hues.length)];
      wrapBlob(g, w, h, Math.random() * w, Math.random() * h, rnd(30, 120), `rgba(${hr},${hg},${hb},${rnd(alpha * 0.4, alpha).toFixed(3)})`);
    }
    // dark dust lanes cut through the glow
    g.globalCompositeOperation = "destination-out";
    for (let i = 0; i < count / 3; i++) {
      wrapBlob(g, w, h, Math.random() * w, Math.random() * h, rnd(15, 50), "rgba(0,0,0,0.35)");
    }
    return c;
  }

  // 3. spiral galaxy sprite
  function makeGalaxy() {
    const s = 420, c = offscreen(s, s), g = c.getContext("2d"), cx = s / 2;
    const core = g.createRadialGradient(cx, cx, 0, cx, cx, s * 0.22);
    core.addColorStop(0, "rgba(255,235,255,0.9)"); core.addColorStop(0.3, "rgba(220,160,255,0.35)"); core.addColorStop(1, "rgba(120,60,200,0)");
    g.fillStyle = core; g.fillRect(0, 0, s, s);
    for (let arm = 0; arm < 2; arm++) {
      for (let i = 0; i < 2600; i++) {
        const k = Math.random(), ang = arm * Math.PI + k * 4.2 * Math.PI / 1.4, rad = 8 + k * s * 0.46;
        const sp = (1 - k * 0.5) * 14;
        const x = cx + Math.cos(ang) * rad + rnd(-sp, sp), y = cx + Math.sin(ang) * rad * 0.55 + rnd(-sp, sp) * 0.55;
        g.fillStyle = `rgba(${k < 0.3 ? "255,220,255" : "190,160,255"},${rnd(0.05, 0.45 * (1 - k * 0.6)).toFixed(2)})`;
        g.fillRect(x, y, rnd(0.5, 1.6), rnd(0.5, 1.6));
      }
    }
    return c;
  }

  // 4. bright stars in three depth layers
  function makeStars() {
    const n = Math.min(520, Math.round(W * H / 3000));
    stars = Array.from({ length: n }, () => {
      const layer = Math.random() < 0.55 ? 0 : Math.random() < 0.7 ? 1 : 2;
      return { x: Math.random() * W, y: Math.random() * H * 1.5, layer,
        r: [0.6, 1.1, 1.8][layer] * rnd(0.7, 1.3),
        vx: [0.006, 0.014, 0.03][layer], vy: [0.001, 0.003, 0.006][layer],
        par: [0.04, 0.12, 0.28][layer],
        tw: Math.random() * 6.28, tws: rnd(0.0008, 0.0035),
        hue: Math.random() < 0.18 ? "255,205,255" : Math.random() < 0.18 ? "195,215,255" : "255,255,255" };
    });
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth; H = window.innerHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    deep = makeDeep();
    neb1 = makeNebula([[150, 60, 230], [220, 70, 190], [100, 60, 240]], 55, 0.55);
    neb2 = makeNebula([[255, 110, 220], [120, 90, 255], [70, 130, 240], [190, 80, 255]], 35, 0.4);
    galaxy = galaxy || makeGalaxy();
    makeStars();
    if (still) frame(0);
  }

  function shootStar() {
    const fromLeft = Math.random() < 0.5;
    const ang = (fromLeft ? rnd(0.15, 0.6) : Math.PI - rnd(0.15, 0.6)); // heading down-right or down-left
    const sp = rnd(0.7, 1.6);                                            // px per ms
    shooters.push({ x: rnd(0.05, 0.95) * W, y: rnd(-0.05, 0.45) * H, vx: Math.cos(ang) * sp, vy: Math.sin(ang) * sp,
      len: rnd(90, 260), life: 0, max: rnd(600, 1300), w: rnd(1.2, 2.4), hue: Math.random() < 0.3 ? "230,200,255" : "255,255,255" });
  }

  // draw an image tiled so it wraps while panning
  function tiled(img, ox, oy, dw, dh, alpha) {
    ctx.globalAlpha = alpha;
    const x0 = ((ox % dw) + dw) % dw - dw, y0 = ((oy % dh) + dh) % dh - dh;
    for (let x = x0; x < W; x += dw) for (let y = y0; y < H; y += dh) ctx.drawImage(img, x, y, dw, dh);
    ctx.globalAlpha = 1;
  }

  function frame(dt) {
    t += dt;
    smx += (mx - smx) * 0.04; smy += (my - smy) * 0.04;   // eased mouse parallax
    const sy = scrollY;

    const base = ctx.createLinearGradient(0, 0, W, H);
    base.addColorStop(0, "#07020f"); base.addColorStop(0.5, "#150628"); base.addColorStop(1, "#0a0419");
    ctx.globalCompositeOperation = "source-over"; ctx.fillStyle = base; ctx.fillRect(0, 0, W, H);

    // far: deep field
    tiled(deep, -t * 0.004 - smx * 6, -sy * 0.03 - smy * 6, deep.width, deep.height, 1);

    // nebulae (screen-blended for glow), two speeds
    ctx.globalCompositeOperation = "lighter";
    const nw = W * 1.6, nh = nw * (neb1.height / neb1.width);
    tiled(neb1, -t * 0.008 - smx * 14, -sy * 0.06 + Math.sin(t * 0.00012) * 30 - smy * 14, nw, nh, 0.85);
    tiled(neb2, -t * 0.016 + 300 - smx * 24, -sy * 0.1 + Math.cos(t * 0.0001) * 40 - smy * 24, nw * 1.2, nh * 1.2, 0.7);

    // galaxy, slowly turning
    const gs = Math.min(W, H) * 0.55;
    ctx.save();
    ctx.translate(W * 0.8 - smx * 18, H * 0.28 - sy * 0.05 - smy * 18);
    ctx.rotate(-0.5 + t * 0.000012); ctx.globalAlpha = 0.75;
    ctx.drawImage(galaxy, -gs / 2, -gs / 2, gs, gs);
    ctx.restore(); ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "source-over";

    // bright stars
    const SH = H * 1.5;
    for (const s of stars) {
      s.x -= s.vx * dt; s.y += s.vy * dt;
      if (s.x < -4) s.x += W + 8; if (s.y > SH) s.y -= SH;
      const px = s.x - smx * s.par * 120, py = ((s.y - sy * s.par) % SH + SH) % SH - smy * s.par * 120;
      if (py > H + 4) continue;
      s.tw += s.tws * dt;
      const a = 0.4 + 0.6 * Math.abs(Math.sin(s.tw));
      if (s.layer === 2) {
        const glow = ctx.createRadialGradient(px, py, 0, px, py, s.r * 5);
        glow.addColorStop(0, `rgba(${s.hue},${(a * 0.35).toFixed(3)})`); glow.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = glow; ctx.fillRect(px - s.r * 5, py - s.r * 5, s.r * 10, s.r * 10);
        if (a > 0.9) {
          ctx.fillStyle = `rgba(${s.hue},0.3)`;
          ctx.fillRect(px - s.r * 5, py - 0.5, s.r * 10, 1); ctx.fillRect(px - 0.5, py - s.r * 5, 1, s.r * 10);
        }
      }
      ctx.fillStyle = `rgba(${s.hue},${a.toFixed(3)})`;
      ctx.beginPath(); ctx.arc(px, py, s.r, 0, 6.283); ctx.fill();
    }

    // shooting stars at random times, random directions
    if (!still) {
      nextShoot -= dt;
      if (nextShoot <= 0) {
        shootStar(); if (Math.random() < 0.2) shootStar();
        nextShoot = rnd(1500, 6000);
      }
      for (let i = shooters.length - 1; i >= 0; i--) {
        const s = shooters[i]; s.life += dt;
        const p = s.life / s.max, hx = s.x + s.vx * s.life, hy = s.y + s.vy * s.life;
        const k = s.len / Math.hypot(s.vx, s.vy), tx = hx - s.vx * k, ty = hy - s.vy * k;
        const fade = p < 0.15 ? p / 0.15 : 1 - (p - 0.15) / 0.85;
        const lg = ctx.createLinearGradient(hx, hy, tx, ty);
        lg.addColorStop(0, `rgba(${s.hue},${(0.95 * fade).toFixed(3)})`); lg.addColorStop(1, `rgba(${s.hue},0)`);
        ctx.strokeStyle = lg; ctx.lineWidth = s.w; ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(tx, ty); ctx.stroke();
        const head = ctx.createRadialGradient(hx, hy, 0, hx, hy, 8);
        head.addColorStop(0, `rgba(255,255,255,${(0.9 * fade).toFixed(3)})`); head.addColorStop(1, "rgba(255,255,255,0)");
        ctx.fillStyle = head; ctx.fillRect(hx - 8, hy - 8, 16, 16);
        if (p >= 1) shooters.splice(i, 1);
      }
    }
  }

  function loop(now) {
    const dt = last ? Math.min(now - last, 50) : 16; last = now;
    if (!document.hidden) frame(dt);
    requestAnimationFrame(loop);
  }

  let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(resize, 150); });
  window.addEventListener("scroll", () => { scrollY = window.scrollY || 0; if (still) frame(0); }, { passive: true });
  window.addEventListener("pointermove", e => { mx = e.clientX / (W || 1) - 0.5; my = e.clientY / (H || 1) - 0.5; }, { passive: true });
  resize();
  if (!still) requestAnimationFrame(loop);
})();

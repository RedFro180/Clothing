// Background: a warm near-black "darkroom" with slow drifting smoke, film grain and a soft vignette.
// Colors come from the brand (bone, a hint of oxblood), not Halloween orange/green/purple.
// Draws on <canvas id="space"> behind the page. Pauses when the tab is hidden;
// one still frame if the visitor prefers reduced motion.
(() => {
  "use strict";
  const cv = document.getElementById("space");
  if (!cv || !cv.getContext) return;
  const ctx = cv.getContext("2d");
  const still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const rnd = (a, b) => a + Math.random() * (b - a);
  let W = 0, H = 0, dpr = 1, last = 0, scrollY = window.scrollY || 0, grainT = 0, gi = 0;
  let plumes = [], sprites = [], grains = [], buf, bx;

  function offscreen(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }

  // a soft smoke puff: many faint blobs clustered along a lazy curve
  function makeSprite(rgb) {
    const s = 512, c = offscreen(s, s), g = c.getContext("2d");
    const a0 = rnd(0, Math.PI * 2);
    for (let i = 0; i < 70; i++) {
      const t = i / 70, ang = a0 + t * rnd(2, 4);
      const x = s / 2 + Math.cos(ang) * s * 0.22 * t + rnd(-40, 40), y = s / 2 + Math.sin(ang) * s * 0.16 * t + rnd(-40, 40);
      const r = rnd(40, 120) * (1 - t * 0.4);
      const rg = g.createRadialGradient(x, y, 0, x, y, r);
      rg.addColorStop(0, `rgba(${rgb},${rnd(0.05, 0.12).toFixed(3)})`); rg.addColorStop(1, `rgba(${rgb},0)`);
      g.fillStyle = rg; g.fillRect(x - r, y - r, r * 2, r * 2);
    }
    return c;
  }

  function makeGrain() {
    const s = 220, c = offscreen(s, s), g = c.getContext("2d"), img = g.createImageData(s, s);
    for (let i = 0; i < img.data.length; i += 4) {
      const v = Math.random() * 255;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    return c;
  }

  function setup() {
    dpr = 1;   // soft smoke needs no extra resolution; keeps it fast on high-DPI screens
    W = window.innerWidth; H = window.innerHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    buf = offscreen(Math.ceil(W / 2), Math.ceil(H / 2)); bx = buf.getContext("2d"); bx.setTransform(0.5, 0, 0, 0.5, 0, 0);
    if (!sprites.length) {
      sprites = [makeSprite("236,229,216"), makeSprite("236,229,216"), makeSprite("214,200,180"), makeSprite("150,50,45")];
      grains = [makeGrain(), makeGrain(), makeGrain()];
    }
    const M = Math.max(W, H);
    plumes = Array.from({ length: 7 }, (_, i) => ({
      sp: sprites[i === 6 ? 3 : i % 3], x: rnd(-0.2, 1.2) * W, y: rnd(-0.1, 1.1) * H,
      size: M * rnd(0.55, 1.1), vx: rnd(0.004, 0.012) * (Math.random() < 0.5 ? -1 : 1), vy: rnd(-0.006, -0.002),
      rot: rnd(0, 6.28), vr: rnd(-0.00003, 0.00003), alpha: i === 6 ? 0.5 : rnd(0.35, 0.7), par: rnd(0.04, 0.14),
    }));
    if (still) frame(0);
  }

  function frame(dt) {
    const out = ctx; let ctx2 = bx;
    const base = ctx2.createLinearGradient(0, 0, 0, H);
    base.addColorStop(0, "#171412"); base.addColorStop(1, "#0d0b0a");
    ctx2.globalCompositeOperation = "source-over"; ctx2.globalAlpha = 1;
    ctx2.fillStyle = base; ctx2.fillRect(0, 0, W, H);

    // smoke
    ctx2.globalCompositeOperation = "screen";
    for (const p of plumes) {
      p.x += p.vx * dt; p.y += p.vy * dt; p.rot += p.vr * dt;
      const half = p.size / 2;
      if (p.x - half > W) p.x = -half; if (p.x + half < 0) p.x = W + half;
      if (p.y + half < 0) { p.y = H + half; p.x = rnd(0, W); }
      const py = p.y - scrollY * p.par;
      ctx2.save(); ctx2.globalAlpha = p.alpha;
      ctx2.translate(p.x, ((py % (H + p.size)) + H + p.size) % (H + p.size) - half / 2);
      ctx2.rotate(p.rot); ctx2.drawImage(p.sp, -half, -half, p.size, p.size); ctx2.restore();
    }

    // vignette
    ctx2.globalCompositeOperation = "source-over"; ctx2.globalAlpha = 1;
    const vg = ctx2.createRadialGradient(W / 2, H * 0.45, Math.min(W, H) * 0.2, W / 2, H * 0.45, Math.max(W, H) * 0.8);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.55)");
    ctx2.fillStyle = vg; ctx2.fillRect(0, 0, W, H);
    out.drawImage(buf, 0, 0, W, H);

    // film grain, flickering a few times a second
    grainT += dt; if (grainT > 110) { grainT = 0; gi = (gi + 1) % grains.length; }
    ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 0.04;
    const pat = ctx.createPattern(grains[gi], "repeat"); ctx.fillStyle = pat; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1;
  }

  function loop(now) {
    const dt = last ? Math.min(now - last, 50) : 16; last = now;
    if (!document.hidden) frame(dt);
    requestAnimationFrame(loop);
  }

  let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(setup, 150); });
  window.addEventListener("scroll", () => { scrollY = window.scrollY || 0; if (still) frame(0); }, { passive: true });
  setup();
  if (!still) requestAnimationFrame(loop);
})();

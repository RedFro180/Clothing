// Moving cosmic background: purple nebula clouds drifting slowly, twinkling stars in three
// depth layers, and an occasional shooting star. Draws on <canvas id="space"> behind the page.
// Stops when the tab is hidden; draws one still frame if the visitor prefers reduced motion.
(() => {
  "use strict";
  const cv = document.getElementById("space");
  if (!cv || !cv.getContext) return;
  const ctx = cv.getContext("2d");
  const still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W = 0, H = 0, dpr = 1, stars = [], shoot = null, nextShoot = 4000, last = 0, t = 0;

  const NEBULAE = [  // x, y (0-1 of screen), radius (of max side), color, drift speed
    [0.18, 0.22, 0.55, "rgba(150, 60, 220, 0.40)", 0.00007],
    [0.82, 0.30, 0.50, "rgba(220, 70, 180, 0.28)", 0.00005],
    [0.55, 0.78, 0.60, "rgba(90, 60, 230, 0.32)", 0.00006],
    [0.10, 0.85, 0.40, "rgba(60, 120, 230, 0.22)", 0.00008],
    [0.70, 0.60, 0.35, "rgba(255, 120, 220, 0.14)", 0.00009],
  ];

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth; H = window.innerHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = Math.min(420, Math.round(W * H / 3800));
    stars = Array.from({ length: n }, () => {
      const layer = Math.random() < 0.6 ? 0 : Math.random() < 0.75 ? 1 : 2;  // far, mid, near
      return { x: Math.random() * W, y: Math.random() * H, layer,
        r: [0.6, 1.0, 1.6][layer] * (0.7 + Math.random() * 0.6),
        speed: [0.004, 0.009, 0.018][layer],
        tw: Math.random() * Math.PI * 2, tws: 0.0008 + Math.random() * 0.0025,
        hue: Math.random() < 0.15 ? "255,210,255" : Math.random() < 0.15 ? "200,220,255" : "255,255,255" };
    });
    if (still) frame(0);
  }

  function frame(dt) {
    t += dt;
    // deep space base
    const g = ctx.createLinearGradient(0, 0, W, H);
    g.addColorStop(0, "#0a0316"); g.addColorStop(0.5, "#1a0833"); g.addColorStop(1, "#0d0620");
    ctx.globalCompositeOperation = "source-over";
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    // nebula clouds, drifting in slow circles
    ctx.globalCompositeOperation = "lighter";
    const M = Math.max(W, H);
    for (const [x, y, r, c, s] of NEBULAE) {
      const cx = (x + Math.sin(t * s) * 0.06) * W, cy = (y + Math.cos(t * s * 1.3) * 0.05) * H;
      const rg = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * M);
      rg.addColorStop(0, c); rg.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = rg; ctx.fillRect(0, 0, W, H);
    }
    // stars
    for (const s of stars) {
      s.x -= s.speed * dt; if (s.x < -2) { s.x = W + 2; s.y = Math.random() * H; }
      s.tw += s.tws * dt;
      const a = 0.45 + 0.55 * Math.abs(Math.sin(s.tw));
      ctx.fillStyle = `rgba(${s.hue},${a.toFixed(3)})`;
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
      if (s.layer === 2 && a > 0.9) {  // sparkle on the nearest stars
        ctx.fillStyle = `rgba(${s.hue},0.25)`;
        ctx.fillRect(s.x - s.r * 4, s.y - 0.4, s.r * 8, 0.8); ctx.fillRect(s.x - 0.4, s.y - s.r * 4, 0.8, s.r * 8);
      }
    }
    // shooting star now and then
    if (!still) {
      nextShoot -= dt;
      if (!shoot && nextShoot <= 0) {
        shoot = { x: W * (0.3 + Math.random() * 0.7), y: H * Math.random() * 0.4, life: 0, len: 120 + Math.random() * 120 };
        nextShoot = 6000 + Math.random() * 9000;
      }
      if (shoot) {
        shoot.life += dt; const p = shoot.life / 900;
        const hx = shoot.x - p * 520, hy = shoot.y + p * 260;
        const lg = ctx.createLinearGradient(hx, hy, hx + shoot.len, hy - shoot.len / 2);
        lg.addColorStop(0, `rgba(255,255,255,${(1 - p).toFixed(3)})`); lg.addColorStop(1, "rgba(255,255,255,0)");
        ctx.strokeStyle = lg; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(hx + shoot.len, hy - shoot.len / 2); ctx.stroke();
        if (p >= 1) shoot = null;
      }
    }
    ctx.globalCompositeOperation = "source-over";
  }

  function loop(now) {
    const dt = last ? Math.min(now - last, 50) : 16; last = now;
    if (!document.hidden) frame(dt);
    requestAnimationFrame(loop);
  }

  window.addEventListener("resize", resize);
  resize();
  if (!still) requestAnimationFrame(loop);
})();

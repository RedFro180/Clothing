// Foldables, dual screens and split screen: layout + a full customer order on each size, plus folding and
// unfolding in the middle of a visit. Sizes are in tools/screens.js (Galaxy Z Fold 8 Ultra cover/inner,
// split screen, half-folded, pop-up window, dual screen, desktop split screen).
// Run:  node tools/fold_test.js   (exit 1 on any failure). Screenshots go to the system temp folder.
// Scrolling on the same sizes:  node tools/scroll_test.js fold
const { chromium } = require("playwright");
const path = require("path"), os = require("os");
const { FOLD, fold } = require("./screens");
const URL0 = "file://" + path.join(__dirname, "..", "site", "index.html");
const SHOTS = path.join(os.tmpdir(), "fold-shots"); require("fs").mkdirSync(SHOTS, { recursive: true });
const fails = [], errs = [];

async function layout(p, ok, touch) {
  const L = await p.evaluate(() => {
    const vw = innerWidth, vh = innerHeight, r = s => document.querySelector(s).getBoundingClientRect();
    const cards = [...document.querySelectorAll("#grid .card")].slice(0, 8).map(c => c.getBoundingClientRect());
    const cols = new Set(cards.map(c => Math.round(c.left))).size;
    const clipped = [...document.querySelectorAll("#grid .card")].slice(0, 12).filter(c => [...c.querySelectorAll("*")].some(e => e.children.length === 0 && !e.classList.contains("sr") && e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow !== "visible" && getComputedStyle(e).textOverflow !== "ellipsis")).length;
    const head = r(".top"), bag = r("#bagBtn"), brand = r(".top .brand");
    const tiny = [...document.querySelectorAll("p, a, button, span, label, summary, h1, h2, h3")].filter(e => e.offsetParent && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 11).length;
    const chips = [...document.querySelectorAll(".chip")].filter(e => e.offsetParent).map(e => e.getBoundingClientRect().height);
    return { vw, vh, overflow: document.documentElement.scrollWidth - vw, headH: head.height, bagIn: bag.left >= 0 && bag.right <= vw + 1, brandIn: brand.left >= 0 && brand.right <= vw + 1 && brand.right <= bag.left + 1,
      cols, cardW: cards[0].width, clipped, tiny, minChip: Math.min(...chips), ringW: r("#ring").width };
  });
  ok("no sideways scrolling", L.overflow <= 1, `(${L.overflow}px too wide)`);
  ok("header under 30% of the screen", L.headH <= L.vh * 0.3, `(${Math.round(L.headH)} of ${L.vh})`);
  ok("logo and preorder button both fit", L.bagIn && L.brandIn);
  ok("product cards readable width (≥130px)", L.cardW >= 130, `(${Math.round(L.cardW)}px, ${L.cols} columns)`);
  ok("no cut-off text in cards", L.clipped === 0, `(${L.clipped})`);
  ok("no text under 11px", L.tiny === 0, `(${L.tiny})`);
  if (touch) ok("filter chips tall enough to tap (≥40px)", L.minChip >= 40, `(${L.minChip})`);
  return L;
}

async function popupFits(p, ok, tag = "") {
  const P = await p.evaluate(() => {
    const d = document.querySelector("#pd").getBoundingClientRect(), x = document.querySelector("#pd .x").getBoundingClientRect();
    return { inside: d.left >= -1 && d.top >= -1 && d.right <= innerWidth + 1 && d.bottom <= innerHeight + 1, close: x.top >= 0 && x.right <= innerWidth && x.bottom <= innerHeight };
  });
  ok("pop-up fits the screen" + tag, P.inside); ok("close button visible" + tag, P.close);
}

(async () => {
  const b = await chromium.launch();
  for (const [name, opts] of FOLD) {
    const ctx = await b.newContext(opts); const p = await ctx.newPage();
    p.on("pageerror", e => errs.push(`${name}: ${e.message}`));
    const mine = [], ok = (label, cond, extra = "") => { if (!cond) mine.push(`${label} ${extra}`); return cond; };
    await p.goto(URL0); await p.waitForTimeout(600);
    const L = await layout(p, ok, !!opts.hasTouch);
    await p.screenshot({ path: path.join(SHOTS, name.replace(/\W+/g, "-") + "-1.png") });

    // full customer order: search, open, size, add, list, form, send
    await p.evaluate(() => document.querySelector("#shop").scrollIntoView({ behavior: "instant" }));
    await p.fill("#fSearch", "skull"); await p.waitForTimeout(400);
    ok("search finds hoodies", (await p.locator("#grid .card").count()) > 0);
    await p.locator("#grid .card").first().click(); await p.waitForTimeout(400);
    await popupFits(p, ok);
    await p.screenshot({ path: path.join(SHOTS, name.replace(/\W+/g, "-") + "-2.png") });
    if (!(await p.evaluate(() => document.querySelector("#pd").classList.contains("one-size")))) {   // one-size items need no size
      const m = p.locator("#pdSizes button", { hasText: /^M$/ });
      await ((await m.count()) ? m.first() : p.locator("#pdSizes button:not(.is-out)").first()).click();
    }
    const add = p.locator("#pdAdd"); await add.scrollIntoViewIfNeeded();
    ok("Add button reachable", await add.isVisible()); await add.click(); await p.waitForTimeout(250);
    ok("added to list", (await p.textContent("#bagCount")).trim() === "1");
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);
    await p.evaluate(() => scrollTo({ top: 0, behavior: "instant" }));
    await p.click("#bagBtn"); await p.waitForTimeout(300);
    ok("preorder list fits the screen", await p.evaluate(() => { const d = document.querySelector("#bag").getBoundingClientRect(); return d.left >= -1 && d.right <= innerWidth + 1 && d.bottom <= innerHeight + 1; }));
    await p.fill("#reqForm input[name=name]", "Test Buyer"); await p.fill("#reqForm input[name=email]", "buyer@example.com");
    await p.locator("#reqForm input[name=agree]").scrollIntoViewIfNeeded(); await p.check("#reqForm input[name=agree]");
    await p.waitForTimeout(2700); await p.locator("#reqBtn").scrollIntoViewIfNeeded(); await p.click("#reqBtn"); await p.waitForTimeout(500);
    ok("order sent with an order number", /PO-\d{6}-|email app/i.test(await p.textContent("#reqMsg")), `("${(await p.textContent("#reqMsg")).slice(0, 60)}")`);
    console.log(`${name.padEnd(28)} ${String(L.vw + "x" + L.vh).padEnd(9)} ${L.cols} col  ${mine.length ? "FAILED" : "all passed"}`);
    for (const m of mine) console.log("    " + m); fails.push(...mine.map(m => name + ": " + m));
    await ctx.close();
  }

  // folding and unfolding in the middle of a visit
  const moves = [["unfold: cover → open", [411, 850], [859, 845]], ["fold: open → cover", [859, 845], [411, 850]],
    ["open → split screen", [859, 845], [427, 845]], ["split screen → full", [427, 845], [859, 845]], ["turn sideways (open)", [859, 845], [954, 750]]];
  for (const [label, from, to] of moves) {
    const ctx = await b.newContext(fold(from[0], from[1])); const p = await ctx.newPage(); const mine = [];
    const ok = (l, c, e = "") => { if (!c) mine.push(`${l} ${e}`); return c; };
    p.on("pageerror", e => errs.push(`${label}: ${e.message}`));
    await p.goto(URL0); await p.waitForTimeout(500);
    await p.locator("#grid .card").nth(3).scrollIntoViewIfNeeded(); await p.locator("#grid .card").nth(3).click(); await p.waitForTimeout(300);
    await p.evaluate(() => document.querySelector("#pdBody").scrollTop = 200);
    await p.setViewportSize({ width: to[0], height: to[1] }); await p.waitForTimeout(500);
    await popupFits(p, ok, " after the change");
    ok("pop-up still open and scrollable", await p.evaluate(() => { const d = document.querySelector("#pdBody"); return document.querySelector("#pd").open && d.scrollHeight > d.clientHeight; }));
    ok("page still locked behind pop-up", await p.evaluate(() => getComputedStyle(document.documentElement).overflow === "hidden"));
    await p.keyboard.press("Escape"); await p.waitForTimeout(250);
    ok("no sideways scrolling after the change", await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await p.evaluate(() => scrollTo({ top: 0, behavior: "instant" })); await p.waitForTimeout(700);
    ok("spinning hoodies fit after the change", await p.evaluate(() => { const r = document.querySelector("#ring").getBoundingClientRect(); return [...document.querySelectorAll("#ring .ring-card")].filter(c => +getComputedStyle(c).opacity > 0.6).every(c => { const q = c.getBoundingClientRect(); return q.left >= r.left - 60 && q.right <= r.right + 60; }); }));
    await p.screenshot({ path: path.join(SHOTS, "move-" + label.replace(/\W+/g, "-") + ".png") });
    console.log(`${label.padEnd(28)} ${mine.length ? "FAILED" : "all passed"}`); for (const m of mine) console.log("    " + m);
    fails.push(...mine.map(m => label + ": " + m)); await ctx.close();
  }
  // real hinge / fold line (emulated): pop-ups must stay on one side of it
  const hinges = [["Dual screen with hinge", 1114, 720, { orientation: "vertical", offset: 540, maskLength: 34 }, "x"],
    ["Fold half-folded (fold line)", 859, 845, { orientation: "horizontal", offset: 410, maskLength: 1 }, "y"]];
  for (const [label, w, h, feat, axis] of hinges) {
    const mine = [], ok = (l, c, e = "") => { if (!c) mine.push(`${l} ${e}`); return c; };
    for (const which of ["#pd", "#bag"]) {
      const ctx = await b.newContext(fold(w, h)); const p = await ctx.newPage(), cdp = await ctx.newCDPSession(p);
      p.on("pageerror", e => errs.push(`${label}: ${e.message}`));
      await p.goto(URL0); await p.waitForTimeout(400);
      // (set after loading: Playwright resets this override on some actions, so only script clicks below)
      await cdp.send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 2.625, mobile: true, displayFeature: feat }); await p.waitForTimeout(200);
      await p.evaluate(s => s === "#pd" ? document.querySelector("#grid .card").click() : document.querySelector("#bagBtn").click(), which); await p.waitForTimeout(400);
      const r = await p.evaluate(s => { const q = document.querySelector(s).getBoundingClientRect(); return [q.left, q.top, q.right, q.bottom]; }, which);
      const a = feat.offset, z = feat.offset + feat.maskLength;
      const clear = axis === "x" ? (r[2] <= a + 1 || r[0] >= z - 1) : (r[3] <= a + 1 || r[1] >= z - 1);
      ok(`${which === "#pd" ? "product pop-up" : "preorder list"} stays off the fold`, clear, `(${r.map(Math.round).join(",")})`);
      await p.screenshot({ path: path.join(SHOTS, "hinge-" + label.replace(/\W+/g, "-") + which.slice(1) + ".png") }); await ctx.close();
    }
    console.log(`${label.padEnd(28)} ${mine.length ? "FAILED" : "all passed"}`); for (const m of mine) console.log("    " + m);
    fails.push(...mine.map(m => label + ": " + m));
  }
  await b.close();
  for (const e of errs) console.log("  PAGE ERROR  " + e);
  console.log(`\nScreenshots: ${SHOTS}`);
  console.log(fails.length || errs.length ? `FOLD TEST FAILED (${fails.length} failures, ${errs.length} page errors)` : "FOLD TEST PASSED");
  process.exit(fails.length || errs.length ? 1 : 0);
})();

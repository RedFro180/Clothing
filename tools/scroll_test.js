// Full scrolling test: every scrollable part of the shop, on 7 screen types.
// Run:  node tools/scroll_test.js        (exit 1 if anything fails)
//       node tools/scroll_test.js fold   (foldables, dual screens and split screen; see FOLD in screens.js)
// Checks: page scroll, product pop-up (wheel/finger, top + bottom edges, size guide, "Buy it with" row,
// opening another product), page locked while any pop-up is open and unlocked after, scroll position kept,
// preorder list with many items, recently viewed, filter chip rows, spinning ring, back to top, shared link.
const { chromium, devices } = require("playwright");
const path = require("path");
const URL0 = "file://" + path.join(__dirname, "..", "site", "index.html");
const SCREENS = process.argv[2] === "fold" ? require("./screens").FOLD : [
  ["desktop 1280", { viewport: { width: 1280, height: 760 } }],
  ["laptop 1366x620", { viewport: { width: 1366, height: 620 } }],
  ["iPad Mini", devices["iPad Mini"]],
  ["iPhone 13", devices["iPhone 13"]],
  ["iPhone SE", devices["iPhone SE"]],
  ["Pixel 7", devices["Pixel 7"]],
  ["iPhone 13 sideways", devices["iPhone 13 landscape"]],
];
const fails = [], errs = [];

(async () => {
  const b = await chromium.launch();
  for (const [name, opts] of SCREENS) {
    const ctx = await b.newContext(opts); const p = await ctx.newPage();
    p.on("pageerror", e => errs.push(`${name}: ${e.message}`));
    const touch = !!opts.hasTouch, cdp = await ctx.newCDPSession(p);
    const ok = (label, cond, extra = "") => { if (!cond) fails.push(`${name}: ${label} ${extra}`); return cond; };
    const pageY = () => p.evaluate(() => scrollY);
    async function still() {   // wait until the page has stopped moving (3 equal readings 100 ms apart, max ~3 s)
      let last = -1, same = 0;
      for (let i = 0; i < 30 && same < 3; i++) { const y = await pageY(); same = y === last ? same + 1 : 0; last = y; await p.waitForTimeout(100); }
    }
    // scroll over a point: wheel on desktop, finger swipe on touch screens. dy > 0 = scroll down the content.
    async function scrollAt(x, y, dy, dx = 0) {
      const vp = await p.evaluate(() => [innerWidth, innerHeight]);
      x = Math.max(5, Math.min(x, vp[0] - 5)); y = Math.max(5, Math.min(y, vp[1] - 5));
      if (!touch) { await p.mouse.move(x, y); await p.mouse.wheel(dx, dy); }
      else await cdp.send("Input.synthesizeScrollGesture", { x: Math.round(x), y: Math.round(y), yDistance: -dy, xDistance: -dx, speed: 1800 });
      await settle();
    }
    // wait until the page and every scroller have stopped moving (the page uses smooth scrolling)
    async function settle() {
      let last = "";
      for (let i = 0; i < 30; i++) {
        await p.waitForTimeout(120);
        const now = await p.evaluate(() => [scrollY, ...[...document.querySelectorAll("#pdBody, #bag, #rv, .chips, .mini-row")].map(e => e.scrollTop + "," + e.scrollLeft)].join("|"));
        if (now === last) return; last = now;
      }
    }
    const mid = async sel => { const r = await p.locator(sel).first().boundingBox(); return [r.x + r.width / 2, r.y + r.height / 2, r]; };

    await p.goto(URL0); await p.waitForTimeout(500);
    const vh = await p.evaluate(() => innerHeight);

    // 1. page scrolls normally, including a vertical swipe that starts on the ring and on a chip row
    let y0 = await pageY(); let [x, y] = await mid("#ring");
    await scrollAt(x, Math.min(y, vh - 40), 300);
    ok("page scrolls from the ring", (await pageY()) > y0);
    await p.evaluate(() => document.querySelector(".chips[data-for=fCat]").scrollIntoView({ block: "center", behavior: "instant" })); await settle();
    y0 = await pageY(); [x, y] = await mid(".chips[data-for=fCat]");
    await scrollAt(x, y, 250);
    ok("page scrolls from a chip row", (await pageY()) > y0);

    // 2. chip row swipes sideways
    const chipRow = ".chips[data-for=fCat]";
    if (await p.evaluate(s => { const c = document.querySelector(s); return c.scrollWidth > c.clientWidth; }, chipRow)) {
      await p.evaluate(s => document.querySelector(s).scrollIntoView({ block: "center", behavior: "instant" }), chipRow); await settle(); [x, y] = await mid(chipRow);
      await scrollAt(x, y, 0, 200);
      ok("chip row swipes sideways", (await p.evaluate(s => document.querySelector(s).scrollLeft, chipRow)) > 0);
    }

    // 3. ring: sideways swipe turns it (touch)
    if (touch) {
      // center it (a sticky header would otherwise sit on top of it on a sideways phone)
      await p.evaluate(() => document.querySelector("#ring").scrollIntoView({ block: "center", behavior: "instant" })); await settle();
      const front = () => p.evaluate(() => [...document.querySelectorAll("#ring .ring-card")].map(e => e.style.transform).join("|"));
      await p.evaluate(() => document.querySelector("#ringPause").click()); await p.waitForTimeout(300); const t0 = await front();
      const r = await p.locator("#ring").boundingBox(), sy = Math.round(Math.max(r.y + 30, Math.min(r.y + r.height / 2, vh - 30))), sx = Math.round(r.x + r.width / 2 + 90);
      await cdp.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: sx, y: sy }] });
      for (let i = 1; i <= 6; i++) await cdp.send("Input.dispatchTouchEvent", { type: "touchMove", touchPoints: [{ x: sx - i * 30, y: sy }] });
      await cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] }); await p.waitForTimeout(900);
      ok("ring turns on a sideways swipe", (await front()) !== t0);
      ok("a swipe on the ring doesn't open a product", !(await p.evaluate(() => document.querySelector("#pd").open)));
      await p.evaluate(() => { const d = document.querySelector("dialog[open]"); if (d) d.close(); });
      await p.evaluate(() => document.querySelector("#ringPause").click());
    }

    // 3b. grid hoodies spin on a sideways drag/swipe, without opening the product or moving the page
    {
      await p.evaluate(() => document.querySelector("#grid .card").scrollIntoView({ block: "center", behavior: "instant" })); await settle();
      const r = await p.locator("#grid .card .stage").first().boundingBox(), sx = Math.round(r.x + r.width / 2), sy = Math.round(r.y + r.height / 2), y0 = await pageY();
      const t0 = await p.evaluate(() => document.querySelector("#grid .card .turn").style.transform);
      let mid;
      if (touch) {
        await cdp.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: sx, y: sy }] });
        for (let i = 1; i <= 8; i++) await cdp.send("Input.dispatchTouchEvent", { type: "touchMove", touchPoints: [{ x: sx - i * 12, y: sy }] });
        mid = await p.evaluate(() => document.querySelector("#grid .card .turn").style.transform);
        await cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
      } else {
        await p.mouse.move(sx, sy); await p.mouse.down(); for (let i = 1; i <= 8; i++) await p.mouse.move(sx + i * 14, sy);
        mid = await p.evaluate(() => document.querySelector("#grid .card .turn").style.transform); await p.mouse.up();
      }
      await p.waitForTimeout(500);
      ok("hoodie spins on a sideways drag/swipe", mid && mid !== t0, `(${t0} → ${mid})`);
      ok("spinning doesn't open the product", !(await p.evaluate(() => document.querySelector("#pd").open)));
      ok("spinning doesn't move the page", Math.abs((await pageY()) - y0) < 2);
      ok("back of the hoodie loads when spun", await p.evaluate(() => !!document.querySelector("#grid .card .face.back").getAttribute("src")));
      await p.evaluate(() => { const d = document.querySelector("dialog[open]"); if (d) d.close(); });
      await p.mouse.move(2, 2);
    }

    // 4. product pop-up
    await p.locator("#grid .card").nth(5).scrollIntoViewIfNeeded(); await settle();
    await p.locator("#grid .card").nth(5).click(); await p.waitForTimeout(350);
    const before = await pageY(); // (Playwright's click may nudge the page first, so measure once it's open)
    ok("page locked while pop-up open", await p.evaluate(() => getComputedStyle(document.documentElement).overflow === "hidden"));
    let [, , box] = await mid("#pdBody");
    const inner = () => p.evaluate(() => document.querySelector("#pdBody").scrollTop);
    // scroll up at the very top: nothing behind moves
    await scrollAt(box.x + box.width * 0.75, box.y + box.height * 0.6, -400);
    ok("scrolling up at the top doesn't move the page", (await pageY()) === before, `(${before} → ${await pageY()}, html overflow ${await p.evaluate(() => getComputedStyle(document.documentElement).overflow)}, open ${await p.evaluate(() => document.querySelector("#pd").open)})`);
    await scrollAt(box.x + box.width * 0.75, box.y + box.height * 0.6, 500);
    ok("pop-up scrolls", (await inner()) > 0);
    ok("page behind stays still", (await pageY()) === before);
    // a vertical swipe on the big picture also scrolls the pop-up (phones)
    if (touch) {
      await p.evaluate(() => document.querySelector("#pdBody").scrollTop = 0);
      const r = await p.locator("#pdImgWrap").boundingBox();
      await scrollAt(r.x + r.width / 2, Math.max(r.y + 20, Math.min(r.y + r.height / 2, vh - 40)), 300);
      ok("swipe on the picture scrolls the pop-up", (await inner()) > 0);
    }
    // scroll far past the bottom: page still still, last item reachable
    for (let i = 0; i < 4; i++) await scrollAt(box.x + box.width * 0.75, box.y + box.height * 0.6, 900);
    ok("page still after scrolling past the bottom", (await pageY()) === before);
    ok("bottom of pop-up reachable", await p.evaluate(() => document.querySelector("#pdShare").getBoundingClientRect().bottom <= document.querySelector("#pdBody").getBoundingClientRect().bottom + 2));
    // size guide opens and can be scrolled fully into view
    await p.evaluate(() => document.querySelector("#pdBody").scrollTop = 0);
    await p.click("#sgBtn"); await p.waitForTimeout(150);
    for (let i = 0; i < 6; i++) {
      const vis = await p.evaluate(() => { const r = document.querySelector("#sizeGuide").getBoundingClientRect(), d = document.querySelector("#pdBody").getBoundingClientRect(); return r.bottom <= d.bottom + 1; });
      if (vis) break; await scrollAt(box.x + box.width * 0.75, box.y + box.height * 0.5, 160);
    }
    // finger/wheel steps can overshoot on very short screens; settle it into place like a reader would
    await p.evaluate(() => document.querySelector("#sizeGuide").scrollIntoView({ block: "nearest", behavior: "instant" })); await settle();
    ok("size guide scrolls fully into view", await p.evaluate(() => { const r = document.querySelector("#sizeGuide").getBoundingClientRect(), d = document.querySelector("#pdBody").getBoundingClientRect(); return r.top >= d.top - 1 && r.bottom <= d.bottom + 1; }));
    ok("page still with size guide open", (await pageY()) === before);
    // "Buy it with" row swipes sideways if it's wider than the screen
    await p.locator("#pdWithList").scrollIntoViewIfNeeded(); await p.waitForTimeout(150);
    if (await p.evaluate(() => { const c = document.querySelector("#pdWithList"); return c.scrollWidth > c.clientWidth + 2; })) {
      [x, y] = await mid("#pdWithList"); await scrollAt(x, y, 0, 200);
      ok("'Buy it with' row swipes sideways", (await p.evaluate(() => document.querySelector("#pdWithList").scrollLeft)) > 0);
    }
    // open a "Buy it with" hoodie: the new one starts at its top
    await p.locator("#pdWithList .mini-img, #pdWithList button").first().click(); await p.waitForTimeout(350);
    ok("next product opens at the top", (await inner()) < 5, `(scrollTop ${await inner()})`);
    // close: page unlocked, same place, scrolls again
    await p.keyboard.press("Escape"); await p.waitForTimeout(250);
    ok("page unlocked after closing", await p.evaluate(() => getComputedStyle(document.documentElement).overflow !== "hidden"));
    ok("page kept its place", Math.abs((await pageY()) - before) < 2, `(${before} → ${await pageY()})`);
    await scrollAt(200, vh / 2, 300);
    ok("page scrolls after closing", (await pageY()) > before);

    // 5. preorder list with many items (8 hoodies across 6 designs)
    await p.evaluate(() => {
      const ids = window.CATALOG.products.slice(0, 6).map(x => x.id);
      localStorage.setItem("preorder-list-v1", JSON.stringify(ids.map((id, i) => ({ id, size: "L", qty: i < 2 ? 2 : 1 }))));
    });
    // reload restores the old scroll position with a smooth animation; turn that off and wait until the page is still,
    // so a scroll that was already running isn't blamed on the list
    await p.evaluate(() => { history.scrollRestoration = "manual"; scrollTo({ top: 0, behavior: "instant" }); });
    await p.reload(); await p.waitForTimeout(400); await p.evaluate(() => scrollTo({ top: 600, behavior: "instant" })); await settle(); await still();
    const b2 = await pageY();
    await p.click("#bagBtn"); await p.waitForTimeout(300);
    const bagBox = await p.locator("#bag").boundingBox();
    for (let i = 0; i < 4; i++) await scrollAt(bagBox.x + bagBox.width / 2, bagBox.y + bagBox.height * 0.5, 600);
    ok("preorder list: page behind stays still", (await pageY()) === b2, `(${b2} → ${await pageY()})`);
    ok("preorder list: send button reachable", await p.evaluate(() => { const r = document.querySelector("#reqBtn").getBoundingClientRect(); return r.bottom <= innerHeight && r.top >= 0; }));
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);
    ok("page unlocked after the list", await p.evaluate(() => getComputedStyle(document.documentElement).overflow !== "hidden"));

    // 6. recently viewed with 8 products
    await p.evaluate(() => localStorage.setItem("recent", JSON.stringify(window.CATALOG.products.slice(10, 18).map(x => x.id))));
    await p.reload(); await p.waitForTimeout(400); await still();
    await p.click("#rvBtn"); await p.waitForTimeout(300);
    const rb = await p.locator("#rv").boundingBox(), r0 = await pageY();
    for (let i = 0; i < 3; i++) await scrollAt(rb.x + rb.width / 2, rb.y + rb.height / 2, 600);
    ok("recently viewed: page behind stays still", (await pageY()) === r0);
    ok("recently viewed: clear button reachable", await p.evaluate(() => document.querySelector("#rvClear").getBoundingClientRect().bottom <= innerHeight));
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);

    // 7. back to top
    await p.evaluate(() => scrollTo(0, document.body.scrollHeight * 0.6)); await p.waitForTimeout(500);
    if (ok("back-to-top button shows", await p.isVisible("#toTop"))) { await p.click("#toTop"); await p.waitForTimeout(300); await settle(); ok("back to top reaches the top", (await pageY()) < 5); }

    // 8. shared product link opens the product with the page locked
    const slug = await p.evaluate(() => window.CATALOG.products[20].slug);
    await p.goto("about:blank"); await p.goto(URL0 + "#" + slug); await p.waitForTimeout(500);
    ok("shared link opens the product", await p.evaluate(() => document.querySelector("#pd").open));
    [, , box] = await mid("#pdBody"); await scrollAt(box.x + box.width * 0.75, box.y + box.height * 0.6, 400);
    ok("shared link pop-up scrolls", (await inner()) > 0);
    ok("shared link page stays still", (await pageY()) === 0);

    const mine = fails.filter(f => f.startsWith(name + ":"));
    console.log(`${name.padEnd(20)} ${mine.length ? "FAILED" : "all passed"}`); for (const f of mine) console.log("    " + f.slice(name.length + 2));
    await ctx.close();
  }
  await b.close();
  for (const e of errs) console.log("  PAGE ERROR  " + e);
  console.log(fails.length || errs.length ? `\nSCROLL TEST FAILED (${fails.length} failures, ${errs.length} page errors)` : "\nSCROLL TEST PASSED");
  process.exit(fails.length || errs.length ? 1 : 0);
})();

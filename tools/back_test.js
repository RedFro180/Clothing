// Phone Back button: must close pop-ups (product, preorder list, recently viewed) and only leave the shop when nothing is open.
// Run: node tools/back_test.js   (exit 1 on failure)
const { chromium, devices } = require("playwright");
const path = require("path");
const URL0 = "file://" + path.join(__dirname, "..", "site", "index.html");
const OTHER = "file://" + path.join(__dirname, "..", "site", "policies.html");
(async () => {
  const b = await chromium.launch(); let fails = 0; const errs = [];
  for (const dev of ["Pixel 7", "iPhone 13"]) {
    const c = await b.newContext({ ...devices[dev] }); const p = await c.newPage(); p.on("pageerror", e => errs.push(e.message));
    const open = () => p.evaluate(() => [...document.querySelectorAll("dialog[open]")].map(d => d.id).join(",") || "-");
    const ok = (name, cond, extra = "") => { if (!cond) { fails++; console.log(`  FAIL ${dev}: ${name} ${extra}`); } };
    const back = async () => { await p.goBack(); await p.waitForTimeout(350); };
    await p.goto(OTHER); await p.goto(URL0); await p.waitForTimeout(500);
    await p.evaluate(() => document.querySelector("#grid .card").click()); await p.waitForTimeout(300);
    ok("product opens", (await open()) === "pd");
    await p.evaluate(() => document.querySelector("#pdAlsoList .also:nth-child(2)") && document.querySelector("#pdAlsoList .also:nth-child(2)").click()); await p.waitForTimeout(300);
    await back(); ok("Back closes the product", (await open()) === "-", await open()); ok("still in the shop", /index\.html/.test(p.url()), p.url());
    await p.evaluate(() => document.querySelector("#grid .card:nth-child(3)").click()); await p.waitForTimeout(300);
    await p.evaluate(() => document.querySelector("#pd [data-close]").click()); await p.waitForTimeout(400);
    ok("X closes without reopening", (await open()) === "-", await open());
    await p.evaluate(() => document.querySelector("#bagBtn").click()); await p.waitForTimeout(300);
    await back(); ok("Back closes the list", (await open()) === "-", await open());
    await p.evaluate(() => document.querySelector("#grid .card").click()); await p.waitForTimeout(300);
    await p.keyboard.press("Escape"); await p.waitForTimeout(400); ok("Esc closes", (await open()) === "-");
    await back(); ok("Back with nothing open leaves the shop", /policies\.html/.test(p.url()), p.url());
    await p.goto(URL0 + "#the-box-will-be-heavy"); await p.waitForTimeout(600); ok("shared link opens product", (await open()) === "pd");
    await back(); ok("Back closes a shared-link product", (await open()) === "-", await open());
    await p.evaluate(() => { location.hash = "everyone-gets-a-toe-tag"; }); await p.waitForTimeout(400);
    ok("changing the #product link opens it", (await open()) === "pd", await open());
    await c.close();
  }
  if (errs.length) { fails++; console.log("  page errors:", errs); }
  console.log(fails ? `BACK TEST FAILED (${fails})` : "BACK TEST PASSED");
  await b.close(); process.exit(fails ? 1 : 0);
})();

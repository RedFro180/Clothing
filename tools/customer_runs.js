// 50 simulated customer journeys. Each logs actions, clicks, scrolls, timing and friction.
const { chromium, devices } = require('playwright');
const fs = require('fs');
const URL0 = 'file://' + require('path').join(__dirname, '..', 'site', 'index.html');
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647; const pick = a => a[Math.floor(rnd() * a.length)];
const SEARCHES = ['skull', 'skeleton', 'black', 'gym', 'grief', 'funny', 'coffin', 'reaper', 'sad', 'death', 'pink', 'heavy', 'lift', 'grave', 'bones', 'rot', 'xl', 'zip up', 'mom', 'depression'];
const PERSONAS = [
  ['ring-impulse', 'Sees the spinning ring, taps a hoodie, buys'],
  ['search', 'Knows a vibe, types a search'],
  ['theme', 'Browses a theme chip'],
  ['color', 'Wants a specific color'],
  ['scroll', 'Scrolls the grid and picks something'],
  ['multi', 'Adds 2–3 items'],
  ['category', 'Taps a type chip (tees, hats, underwear, socks, sweatpants, jackets) and buys one'],
  ['addon', 'Buys a hoodie, adds a one-size add-on from "Buy it with"'],
  ['variant', 'Likes a hoodie design, switches to the same design on another item ("Also in this design") and buys that'],
  ['soldout', 'Wants a size that is sold out'],
  ['sizeunsure', 'Unsure of size, opens size guide'],
  ['shared-link', 'Arrives from a shared product link'],
  ['returning', 'Comes back later, uses recently viewed'],
];
const SOLD = { 10: ['L'], 27: ['M', 'L'], 44: ['XL'], 11: ['S'] };
(async () => {
  const b = await chromium.launch(); const runs = [];
  for (let i = 0; i < 50; i++) {
    const [persona, desc] = PERSONAS[i % PERSONAS.length];
    const phone = rnd() < 0.7;                      // audience mostly on phones
    const ctx = await b.newContext(phone ? { ...devices[pick(['iPhone 13', 'iPhone SE', 'Pixel 7'])] } : { viewport: { width: pick([1280, 1440, 1920]), height: pick([760, 860, 1000]) } });
    await ctx.addInitScript(sold => {
      let cfg; Object.defineProperty(window, 'SITE_CONFIG', { configurable: true, get() { return cfg; }, set(v) { v.SOLD_OUT = sold; cfg = v; } });
    }, SOLD);
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    const log = []; let clicks = 0, taps = 0, scrolls = 0, friction = []; const t0 = Date.now();
    const act = async (label, fn) => { try { await fn(); clicks++; log.push(label); } catch (e) { friction.push('FAILED: ' + label + ' (' + e.message.split('\n')[0].slice(0, 80) + ')'); } };
    const startUrl = persona === 'shared-link' ? URL0 + '#' + pick(['everyone-gets-a-toe-tag', 'grief-has-weight', 'skeleton-wearing-meat', 'the-dirt-always-wins']) : URL0;
    await p.goto(startUrl); await p.waitForTimeout(500);
    const vh = await p.evaluate(() => innerHeight);
    const firstScreen = await p.evaluate(() => ({ products: [...document.querySelectorAll('.ring-card, #grid .card')].filter(e => { const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0 && getComputedStyle(e).visibility !== 'hidden' && +getComputedStyle(e).opacity > .5; }).length,
      priceVisible: [...document.querySelectorAll('.price, #onePrice:not([hidden]), #heroShip, #resultCount')].some(e => { const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }) }));
    if (persona === 'returning') { await p.evaluate(() => localStorage.setItem('recent', JSON.stringify([60, 27, 44]))); await p.reload(); await p.waitForTimeout(400); }
    const openCard = async sel => { await p.locator(sel).scrollIntoViewIfNeeded(); scrolls++; await p.locator(sel).click({ force: true }); await p.waitForTimeout(250); };
    const gridToView = async () => { await p.locator('#filters').scrollIntoViewIfNeeded(); scrolls++; };
    let wantSize = pick(['S', 'M', 'L', 'L', 'XL', 'XL', '2XL']);
    // ---------- journeys ----------
    if (persona === 'ring-impulse') { await act('tap front hoodie in ring', () => p.locator('.ring-card.front').click({ force: true })); }
    if (persona === 'search') {
      await gridToView(); const q = pick(SEARCHES); await act('search "' + q + '"', () => p.fill('#fSearch', q)); await p.waitForTimeout(300);
      const n = await p.locator('#grid .card').count(); log.push(`results: ${n}`);
      if (n === 0) { friction.push(`search "${q}" found nothing`); await act('clear filters', () => p.click('#clearBtn')); }
      await act('open first result', () => openCard('#grid .card >> nth=0'));
    }
    if (persona === 'theme') { await gridToView(); const t = pick(['Morgue', 'Rot', 'Anatomy', 'Graves', 'Grief', 'Iron']); await act('theme chip ' + t, () => p.locator('[data-for="fTheme"] .chip', { hasText: t }).click()); await act('open a result', () => openCard('#grid .card >> nth=' + Math.floor(rnd() * 4))); }
    if (persona === 'color') { await gridToView(); const c = pick(['Black', 'Olive', 'Oxblood', 'Indigo', 'Plum', 'Sand', 'Charcoal']);
      const chip = p.locator('[data-for="fColor"] .chip', { hasText: c }); const inView = await chip.evaluate(e => { const r = e.getBoundingClientRect(); return r.right <= innerWidth && r.left >= 0; });
      if (!inView) friction.push(`color "${c}" chip off-screen; had to swipe the row`);
      await act('color chip ' + c, () => chip.click()); await act('open a result', () => openCard('#grid .card >> nth=0')); }
    if (persona === 'scroll') { const k = 8 + Math.floor(rnd() * 30); await act(`scroll to product #${k + 1}`, () => openCard(`#grid .card >> nth=${k}`)); scrolls += Math.round(k / (phone ? 2 : 4)); }
    if (persona === 'multi') { await act('open product', () => openCard('#grid .card >> nth=1')); }
    if (persona === 'soldout') { await act('open toe tag (L sold out)', async () => { await p.evaluate(() => location.hash = 'everyone-gets-a-toe-tag'); await p.waitForTimeout(300); }); wantSize = 'L'; }
    if (persona === 'sizeunsure') { await act('open product', () => openCard('#grid .card >> nth=' + Math.floor(rnd() * 12))); }
    if (persona === 'category') { await gridToView(); const t = pick(['Tees', 'Hats', 'Underwear', 'Socks', 'Sweatpants', 'Heavy jackets']); await act('type chip ' + t, () => p.locator('[data-for="fCat"] .chip', { hasText: t }).first().click());
      const n = await p.locator('#grid .card').count(); log.push(`${t}: ${n} items`); if (!n) friction.push(`${t}: no items`);
      const tag = await p.textContent('#onePrice'); if (!/\$\d+/.test(tag)) friction.push(`${t}: price not shown`);
      await act('open a result', () => openCard('#grid .card >> nth=' + Math.floor(rnd() * 3))); }
    if (persona === 'addon') { await act('open hoodie', () => openCard('#grid .card >> nth=0')); }
    if (persona === 'variant') {
      await act('open hoodie', () => openCard('#grid .card >> nth=0'));
      const before = await p.textContent('#pdName'); const n = await p.locator('#pdAlsoList .also').count();
      if (n < 2) friction.push('no "Also in this design" picker on a starter design');
      else { const t = pick(['Tee', 'Beanie', 'Dad cap', 'Boxers', 'Socks', 'Sweatpants', 'Heavy jacket']);
        await act('switch to ' + t, () => p.locator('#pdAlsoList .also', { hasText: t }).first().click()); await p.waitForTimeout(300);
        const after = await p.evaluate(() => ({ name: document.querySelector('#pdName').textContent, on: document.querySelector('#pdAlsoList [aria-checked="true"] .also-l').textContent }));
        if (after.name !== before || after.on !== t) friction.push(`picker switch wrong: ${JSON.stringify(after)}`); else log.push('switched to ' + t); } }
    if (persona === 'returning') { const vis = await p.locator('#rvBtn').isVisible(); if (!vis) friction.push('recently viewed button not visible'); await act('open recently viewed', () => p.click('#rvBtn')); await act('pick from recent', () => p.locator('.rv-item').first().click()); }
    // ---------- inside product ----------
    const open = await p.evaluate(() => document.querySelector('#pd').open);
    if (!open) { friction.push('never reached a product'); }
    else {
      const name = await p.textContent('#pdName'); log.push('viewing: ' + name);
      const m = await p.evaluate(() => { const r = document.querySelector('#pdAdd').getBoundingClientRect(); return { addBelow: r.bottom > innerHeight, priceTop: Math.round(document.querySelector('#pdPrice').getBoundingClientRect().top) }; });
      if (m.addBelow) friction.push('Add button below the screen in pop-up');
      if (persona === 'sizeunsure' && !(await p.isVisible('#sgBtn'))) log.push('one-size item: no size guide needed');
      else if (persona === 'sizeunsure') { await act('open size guide', () => p.click('#sgBtn')); const g = await p.textContent('#sizeGuide'); if (g.includes('coming soon')) friction.push('size guide has no measurements'); }
      const oneSize = await p.evaluate(() => document.querySelector('#pd').classList.contains('one-size'));
      const sizes = await p.evaluate(() => [...document.querySelectorAll('#pdSizes button')].map(b => b.dataset.s));
      if (oneSize) log.push('one size: nothing to pick');
      else {
        if (!sizes.includes(wantSize)) wantSize = sizes.includes('M') ? 'M' : sizes.includes('L/XL') ? 'L/XL' : sizes[0];
        await act('pick size ' + wantSize, () => p.locator(`#pdSizes button[data-s="${wantSize}"]`).click());
      }
      const sold = await p.locator('#notifyForm').isVisible();
      if (sold) {
        log.push('size sold out');
        await act('enter email for restock', () => p.fill('#nfEmail', 'test@example.com'));
        await act('submit notify', () => p.click('#notifyBtn')); await p.waitForTimeout(200);
        const mail = /email app/i.test(await p.textContent('#pdMsg')); if (mail) friction.push('restock request opens email app (no form service)');
        const alt = (await p.locator('#pdSizes button:not(.is-out)').count()); log.push(`${alt} other sizes available`);
        const suggest = await p.locator('#pdAlts').isVisible();
        if (!suggest) friction.push('sold out: no suggestion of similar hoodies in that size');
      } else {
        if (!oneSize && rnd() < 0.15) { await act('tap Add without size (mistake)', async () => { await p.locator('#pdSizes button[aria-pressed="true"]').click(); }); }
        await act('add to preorder list', () => p.click('#pdAdd')); await p.waitForTimeout(150);
        const msg = await p.textContent('#pdMsg'); log.push('msg: ' + msg.trim());
        const countVisible = await p.evaluate(() => { const r = document.querySelector('#bagCount').getBoundingClientRect(); return r.width > 0; });
        if (persona === 'addon') {
          const add = p.locator('#pdWithList .mini-add', { hasText: '+ Add' }).filter({ hasNotText: 'M' });
          const one = await p.evaluate(() => [...document.querySelectorAll('#pdWithList .mini')].filter(m => /Beanie|Dad cap/.test(m.textContent) && /\+ Add$/.test(m.querySelector('.mini-add').textContent.trim())).length);
          if (!one) friction.push('no one-size add-on offered under the hoodie');
          else { await act('add a hat from "Buy it with"', () => p.evaluate(() => [...document.querySelectorAll('#pdWithList .mini')].find(m => /Beanie|Dad cap/.test(m.textContent) && /\+ Add$/.test(m.querySelector('.mini-add').textContent.trim())).querySelector('.mini-add').click())); }
          await act('tap "View list"', () => p.locator('#pdMsg .link').click());
        } else if (persona === 'multi') {
          await act('close', () => p.keyboard.press('Escape'));
          for (const k of [5, 14]) { await act('open another', () => openCard(`#grid .card >> nth=${k}`)); const pre = await p.locator('#pdSizes button[aria-pressed="true"]').count(); const one = await p.evaluate(() => document.querySelector('#pd').classList.contains('one-size'));
            if (!pre && !one) { await act('pick size', () => p.locator('#pdSizes button:not(.is-out)').first().click()); } await act('add', () => p.click('#pdAdd')); await act('close', () => p.keyboard.press('Escape')); }
        } else await act('tap "View list"', () => p.locator('#pdMsg .link').click());
      }
    }
    // ---------- checkout (preorder request) ----------
    let submitted = false, mail = null;
    if (await p.locator('#pd').evaluate(d => d.open)) await p.keyboard.press('Escape');
    const items = Number(await p.textContent('#bagCount'));
    const flag = await p.evaluate(() => !document.querySelector('#orderFlag').hidden); if (flag) log.push('large-order flag shown');
    if (items > 0) {
      if (!(await p.locator('#bag').evaluate(d => d.open))) await act('open preorder list', () => p.click('#bagBtn'));
      const total = await p.textContent('#bagTotal'); log.push(total.trim());
      if (!/Shipping/.test(total)) friction.push('shipping cost unknown at checkout');
      await act('type name', () => p.fill('#reqForm input[name=name]', 'Test Buyer'));
      await act('type email', () => p.fill('#reqForm input[name=email]', 'buyer@example.com'));
      const agreeVis = await p.locator('#reqForm input[name=agree]').isVisible(); if (!agreeVis) friction.push('final-sale checkbox not visible');
      await act('tick final-sale checkbox', () => p.check('#reqForm input[name=agree]'));
      await p.waitForTimeout(2600);   // real people take a few seconds; instant submits are treated as bots
      await act('send preorder request', () => p.click('#reqForm button[type=submit]')); await p.waitForTimeout(200);
      const rm = await p.textContent('#reqMsg'); mail = /email app/i.test(rm); submitted = /PO-\d{6}-/.test(rm) || mail;
      if (!submitted) friction.push('preorder not sent: ' + rm.slice(0, 60));
      const sendVisible = await p.evaluate(() => { const r = document.querySelector('#reqBtn').getBoundingClientRect(); return r.bottom <= innerHeight; });
      if (!sendVisible) friction.push('Send button below the screen in the list');
      if (mail) friction.push('preorder request opens email app; buyer must press send there');
      const fields = await p.locator('#reqForm input, #reqForm textarea').count(); log.push(`form fields: ${fields}`);
      if (!/size|ship|address/i.test(await p.textContent('#reqForm'))) {}
    }
    const secs = ((Date.now() - t0) / 1000).toFixed(1);
    runs.push({ i: i + 1, persona, desc, device: phone ? 'phone' : 'desktop', vh, firstScreen, clicks, scrolls, items, submitted, mailto: !!mail, friction, errs, log, secs });
    await ctx.close();
  }
  fs.writeFileSync(require('path').join(__dirname, '..', 'docs', 'testing', 'customer-runs-latest.json'), JSON.stringify(runs, null, 1));
  // summary
  const f = {}; runs.forEach(r => r.friction.forEach(x => { const k = x.replace(/"[^"]*"/g, '"…"').replace(/#\d+/, '#n'); f[k] = (f[k] || 0) + 1; }));
  console.log('runs', runs.length, 'errors', runs.reduce((a, r) => a + r.errs.length, 0));
  console.log('reached a product:', runs.filter(r => !r.friction.includes('never reached a product')).length);
  console.log('submitted preorder:', runs.filter(r => r.submitted).length, ' via email app:', runs.filter(r => r.mailto).length);
  const avg = k => (runs.reduce((a, r) => a + r[k], 0) / runs.length).toFixed(1);
  console.log('avg clicks', avg('clicks'), 'avg scrolls', avg('scrolls'));
  console.log('first screen (phone) products visible:', runs.filter(r => r.device === 'phone').map(r => r.firstScreen.products).join(','));
  console.log('friction counts:'); Object.entries(f).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => console.log('  ' + v + '× ' + k));
  const s = {}; runs.filter(r => r.persona === 'search').forEach(r => { const q = r.log.find(x => x.startsWith('search')); const n = r.log.find(x => x.startsWith('results')); s[q] = n; }); console.log('searches:', s);
  const errCount = runs.reduce((a, r) => a + r.errs.length, 0), sent = runs.filter(r => r.submitted).length;
  await b.close();
  if (errCount || sent < 35) { console.log('FAILED: page errors or too few completed orders'); process.exit(1); }
})();

// Abuse tests: bots, spam, tampering, huge orders.
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const R = {}; const errs = [];
  const fresh = async () => { const c = await b.newContext({ viewport: { width: 1280, height: 860 } }); await c.addInitScript(() => { try { localStorage.setItem("drop-prompt", JSON.stringify({ until: 9e15 })); } catch (e) {} }); const p = await c.newPage(); p.on('pageerror', e => errs.push(e.message));
    await c.addInitScript(() => { window.__mail = []; window.__origOpen = null; });
    await p.goto('file://' + require('path').join(__dirname, '..', 'site', 'index.html')); await p.waitForTimeout(400); return [c, p]; };
  const fill = async (p, o = {}) => { await p.click('#bagBtn'); await p.fill('#reqForm input[name=name]', o.name ?? 'Real Person'); await p.fill('#reqForm input[name=email]', o.email ?? 'real@person.com');
    if (o.gotcha) await p.evaluate(v => document.querySelector('[name=_gotcha]').value = v, o.gotcha); if (o.agree !== false) await p.check('#reqForm input[name=agree]'); };
  const add = async (p, idx, size = 'M', qty = 1) => { await p.locator('#grid .card').nth(idx).click(); await p.click(`#pdSizes button[data-s="${size}"]`); if (qty) await p.fill('#pdQty', String(qty)); await p.click('#pdAdd'); const m = await p.textContent('#pdMsg'); await p.keyboard.press('Escape'); return m; };
  let c, p;
  // 1. qty cap per item: ask for 50
  [c, p] = await fresh(); await add(p, 0, 'M', 50); R.qtyCapped = await p.textContent('#bagCount');
  // 2. adding same item again beyond 3
  R.overLimitMsg = await add(p, 0, 'M', 3); R.afterRepeat = await p.textContent('#bagCount');
  // 3. max hoodies per order (8)
  for (let i = 1; i < 6; i++) await add(p, i, 'L', 3); R.maxOrder = await p.textContent('#bagCount');
  R.largeFlag = await p.evaluate(() => { document.querySelector('#bagBtn').click(); return document.querySelector('#orderFlag').textContent; });
  await p.keyboard.press('Escape'); await c.close();
  // 4. tampered storage: fake ids, 999 qty, bad size, a fake price field
  [c, p] = await fresh(); await p.evaluate(() => localStorage.setItem('preorder-list-v1', JSON.stringify([{ id: 11, size: 'M', qty: 999, price: 1 }, { id: 9999, size: 'M', qty: 1 }, { id: 10, size: 'XXXL', qty: 2 }, '<img src=x onerror=alert(1)>'])));
  await p.reload(); await p.waitForTimeout(300); R.tamperedCount = await p.textContent('#bagCount');
  await p.click('#bagBtn'); R.tamperedTotal = (await p.textContent('#bagTotal')).replace(/\s+/g, ' ').slice(0, 80); await p.keyboard.press('Escape'); await c.close();
  // 5. bot: honeypot filled
  [c, p] = await fresh(); await add(p, 0); await fill(p, { gotcha: 'http://spam' }); await p.waitForTimeout(2700);
  await p.click('#reqBtn'); R.honeypotMsg = await p.textContent('#reqMsg'); R.honeypotKeptList = await p.textContent('#bagCount');
  R.honeypotTracked = await p.evaluate(() => (window.__events || []).some(e => e[0] === 'preorder_sent')); await c.close();
  // 6. bot: instant submit
  [c, p] = await fresh(); await add(p, 0); await fill(p); await p.click('#reqBtn'); R.instantMsg = await p.textContent('#reqMsg'); await c.close();
  // 7. no agreement / bad email / script in name
  [c, p] = await fresh(); await add(p, 0); await fill(p, { agree: false }); await p.waitForTimeout(2700); await p.evaluate(() => document.querySelector('[name=agree]').removeAttribute('required'));
  await p.click('#reqBtn'); R.noAgreeMsg = await p.textContent('#reqMsg');
  await p.check('#reqForm input[name=agree]'); await p.evaluate(() => document.querySelector('[name=email]').setAttribute('type', 'text')); await p.fill('#reqForm input[name=email]', 'notanemail');
  await p.click('#reqBtn'); R.badEmailMsg = await p.textContent('#reqMsg');
  await p.fill('#reqForm input[name=email]', 'ok@ok.com'); await p.fill('#reqForm input[name=name]', '<script>alert(1)</script>');
  let mailto = null; p.on('framenavigated', f => { if (f.url().startsWith('mailto')) mailto = f.url(); });
  await p.click('#reqBtn'); await p.waitForTimeout(300); R.scriptNameMsg = (await p.textContent('#reqMsg')).slice(0, 60);
  R.noScriptRan = await p.evaluate(() => !document.querySelector('script:not([src])') || document.querySelectorAll('script:not([src])').length === 0);
  await c.close();
  // 8. rate limit: 4 sends from same browser
  [c, p] = await fresh(); const msgs = [];
  for (let k = 0; k < 4; k++) { await add(p, k); await fill(p); await p.waitForTimeout(2600); await p.click('#reqBtn'); await p.waitForTimeout(200); msgs.push((await p.textContent('#reqMsg')).slice(0, 40)); await p.keyboard.press('Escape'); await p.evaluate(() => { localStorage.setItem('preorder-list-v1', '[]'); }); await p.reload(); await p.waitForTimeout(300); }
  R.rate = msgs; await c.close();
  // 9. price in the order is from the catalog, not the page
  [c, p] = await fresh(); await p.evaluate(() => { document.querySelectorAll('.price').forEach(e => e.textContent = '$1'); });
  await add(p, 0); await p.click('#bagBtn'); R.priceAfterEdit = (await p.textContent('#bagTotal')).replace(/\s+/g, ' ').slice(0, 40); await c.close();
  console.log(JSON.stringify(R, null, 1)); console.log('page errors', errs); await b.close();
  const ok = R.qtyCapped === '3' && R.maxOrder === '8' && R.tamperedCount === '3' && R.honeypotMsg === 'Sent.' && !R.honeypotTracked
    && /check your details/.test(R.instantMsg) && /size guide/.test(R.noAgreeMsg) && /valid email/.test(R.badEmailMsg) && R.noScriptRan
    && /Too many/.test(R.rate[3]) && !errs.length;
  console.log(ok ? 'ABUSE TESTS PASSED' : 'ABUSE TESTS FAILED'); process.exit(ok ? 0 : 1);
})();

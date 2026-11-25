const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
  for (const [n, o] of [['desktop', { viewport: { width: 1280, height: 760 } }], ['iPhone 13', { ...devices['iPhone 13'] }], ['iPhone SE', { ...devices['iPhone SE'] }]]) {
    const ctx = await b.newContext(o); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + require('path').join(__dirname, '..', 'site', 'index.html')); await p.waitForTimeout(400);
    await p.locator('#grid .card').nth(2).scrollIntoViewIfNeeded(); await p.locator('#grid .card').nth(2).click(); await p.waitForTimeout(300);
    const pageY0 = await p.evaluate(() => scrollY);
    const box = await p.locator('#pdBody').boundingBox();
    // scroll with the wheel (desktop) or a finger swipe (phone) over the pop-up
    if (n === 'desktop') { await p.mouse.move(box.x + box.width * 0.75, box.y + box.height / 2); await p.mouse.wheel(0, 700); }
    else { const s = await p.context().newCDPSession(p); await s.send('Input.synthesizeScrollGesture', { x: Math.round(box.x + box.width / 2), y: Math.round(box.y + box.height * 0.7), yDistance: -500, speed: 1500 }); }
    await p.waitForTimeout(600);
    const inner = await p.evaluate(() => document.querySelector('#pdBody').scrollTop), pageY1 = await p.evaluate(() => scrollY);
    // size guide: open it and make sure it can be scrolled fully into view
    await p.click('#sgBtn'); await p.locator('#sizeGuide').scrollIntoViewIfNeeded(); await p.waitForTimeout(200);
    const sg = await p.evaluate(() => { const r = document.querySelector('#sizeGuide').getBoundingClientRect(), d = document.querySelector('#pdBody').getBoundingClientRect(); return r.top >= d.top - 1 && r.bottom <= d.bottom + 1; });
    const canReachEnd = await p.evaluate(() => { const d = document.querySelector('#pdBody'); d.scrollTop = d.scrollHeight; const last = document.querySelector('#pdShare').getBoundingClientRect(); return last.bottom <= d.getBoundingClientRect().bottom + 1; });
    console.log(n, { popupScrolled: inner > 0, backgroundMoved: pageY1 !== pageY0, sizeGuideVisible: sg, bottomReachable: canReachEnd });
    await p.screenshot({ path: require('os').tmpdir() + `/scroll-${n.replace(/ /g, '')}.png` }); await ctx.close();
  }
  console.log('errors', errs); await b.close(); })();

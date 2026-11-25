# Owner guide: keeping the shop safe and updating it without breaking it

## 1. The honest picture
This site is **static**: plain files, no server, no database, no logins, and no payments on the site. That makes it hard to hack, because there is nothing to break into. The real risks are:
- **spam or fake preorder requests** (bots filling the form)
- **fake or huge orders** that turn into chargebacks once you take payment
- **someone framing or copying the site**, or injecting a script
- **you accidentally breaking it** with a typo when updating

What the site can and can't protect:

| Risk | What the site now does | What still has to happen elsewhere |
|---|---|---|
| Bots / spam | Hidden bot-trap field (`_gotcha`), rejects instant submits (<2.5 s), max 3 requests per 10 min per device, name/email checks, length limits | The form service's spam filter. Formspree supports `_gotcha` on all plans ([Formspree help](https://help.formspree.io/articles/building-your-form/honeypot-spam-filtering.md)) |
| Huge orders | Max 3 of the same design + size, max 8 hoodies per order, **[LARGE]** tag at 4+ | You verify large orders before sending a payment link |
| Price tampering | Prices always come from the catalog file, never from the page. Edited browser storage is cleaned on load. Each request carries a `price_check` stamp | **Always charge from your own price list or payment link, never from the email's numbers** |
| Chargebacks | Required tick box: "I checked the size guide and understand all sales are final". The request records the exact policy text, the time, and an order number | Payment processor tools, tracking with proof of delivery, records (see section 3) |
| Injected scripts / framing | No HTML is ever built from user text. Strict security headers in `site/_headers` (only your own files plus PostHog and Formspree can load; the page can't be put inside another site) | Host must read `_headers` (Cloudflare Pages or Netlify do; GitHub Pages does not) |
| Broken updates | `tools/check_site.js` blocks typos and bad values; a GitHub check runs it plus 50 simulated shoppers on every change | Use the host's preview and **Rollback** button |

**Client-side checks are speed bumps, not walls.** A determined person can bypass anything that runs in the browser. The real walls are the form service (spam), the payment processor (fraud), and you checking large or odd orders before taking money.

## 2. Hosting: recommended setup
- **Cloudflare Pages (free)**, connected to the GitHub repo, with output folder `site`. It reads `site/_headers`, gives a preview link for every branch, and has one-click rollback to any earlier version ([Cloudflare: headers](https://developers.cloudflare.com/pages/configuration/headers/), [rollbacks](https://developers.cloudflare.com/pages/configuration/rollbacks/)). It works with a private repo, so your research files stay private. **Netlify** is a fine alternative and uses the same `_headers` file.
- Turn on **two-factor login** for GitHub, Cloudflare, PostHog, Formspree and your email. Account takeover is the most likely real "hack" of a small shop.
- **Don't** put secrets in `site/`: everything in it is public. The PostHog key and form address are meant to be public; that's normal.

## 3. Chargebacks and fraud: what to do when you take payment
1. **Take payment through Shopify Payments or Stripe**, not by bank transfer or with apps like Zelle. You get fraud scoring, 3D Secure, and address (AVS) and security-code (CVV) checks. Shopify marks each order low/medium/high risk; **don't ship high-risk orders until you've checked them** ([Shopify fraud analysis](https://help.shopify.com/en/manual/orders/fraud-analysis)). When the card's bank verifies a payment with 3D Secure, fraud liability usually shifts off you ([Stripe](https://stripe.com/resources/more/online-store-fraud)).
2. **Large or first-time big orders:** reply by email first. Confirm the name and shipping address, and check that the billing and shipping addresses make sense. Bots and stolen cards rarely answer.
3. **Shipping:** always use tracking. Keep **proof of delivery**, because a "not received" dispute needs delivery proof, not just proof of shipment. Use signature confirmation on high-value orders.
4. **Keep for every order:** the preorder email (with order number, agreement text and time), the payment receipt, the shipping label, tracking and delivery scan, and any messages. That's your evidence pack if a dispute comes in.
5. **Answer customer emails fast.** Many chargebacks come from people who couldn't reach the seller.
6. Make your card-statement name match the brand, so people recognize the charge.

## 4. Updating the site safely (no coding)
**Change settings** (brand, email, shipping, order limits, sold-out sizes, size chart, links, analytics):
1. Open `tools/admin.html` in your browser. Download the repo, or open it from a computer with the files.
2. Make your changes and press **Check**. Fix anything in red.
3. Press **Copy new config.js**.
4. On GitHub: open `site/config.js` → pencil icon → select all → paste → **Commit changes**.
5. Wait for the green check ✓ on GitHub (about 2–5 min). A red ✗ means the change would break something. Don't publish it; fix it or undo the commit.
6. Cloudflare publishes about a minute later. If anything looks wrong: Cloudflare → Deployments → previous one → **Rollback**.

**One price:** while every hoodie has the same price, the site hides prices on the product grid and says "One price $150, every design" once instead. If you ever give one design a different price, prices show under every hoodie again automatically.

**Change designs or prices:** edit `tools/designs_data.py` or `tools/build_site.py`, then run `python3 tools/build_site.py`, then `node tools/check_site.js`. Easiest: ask me to do it.

**Foldables and split screen:** `node tools/fold_test.js` checks the Galaxy Fold cover and inner screens, split screen, half-folded and dual screens (it also runs in the GitHub check). Emulation isn't the real phone, so look at big changes on your Fold too.

**Safer bigger changes:** do them on a new branch. Cloudflare gives that branch its own preview link. Check it on your phone, then merge.

## 5. Your data (backend)
- **Shopper behaviour:** PostHog. See `docs/analytics.md`: bought together, clicks per purchase, time on site, non-buyers, failed searches, funnel.
- **Preorder requests:** your form service inbox. Formspree lists every submission and can export CSV. Each request has an **order number (PO-YYMMDD-XXXX)**, a **[LARGE]** tag when relevant, the items with unit prices, the shipping and total, and the agreement text and time. Free Formspree is about 50 submissions a month according to third-party listings; check formspree.io.
- **Once you move to Shopify:** real orders, refunds, fraud ratings and sales reports live there. Keep PostHog for behaviour.

## 6. Show a friend a private preview (link only)
1. Make the file: `python3 tools/make_share_zip.py` → `site-share.zip`. It holds **only** the shop (`site/`): no research, costs, tech pack, designs or notes. In this copy, search engines and AI crawlers are told not to index, list or archive it (`noindex` page tag + header, `robots.txt` blocks everything). Your real `site/` files are not changed.
2. Go to dash.cloudflare.com (free account) → **Workers & Pages → Create → Pages → Upload assets**.
3. Pick a project name that doesn't identify you or the brand (it becomes the address), upload the zip, press **Deploy**.
4. Copy `https://<name>.pages.dev`, open it on your phone in a private tab to check, then send it.
5. **Update it:** make a new zip and upload it to the same project (same link). **Take it down:** delete the project; the link stops working.

Honest limits: the link isn't a lock. Anyone who has it can open and forward it. To limit it to specific people, add **Cloudflare Access** (Zero Trust → Access → allow only their email); they then enter a one-time code from their email before it opens.

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

**Sizes for tees, boxers, socks and sweatpants:** fill the extra tables in `tools/admin.html` (they're saved as `SIZE_CHARTS` in config.js). Hats are one size.

**Change designs or prices:** prices per item type are in `TYPES` in `tools/build_site.py`; the designs used on tees, hats, boxers, socks and sweatpants are `STARTER` in `tools/items.py`. edit `tools/designs_data.py` or `tools/build_site.py`, then run `python3 tools/build_site.py`, then `node tools/check_site.js`. Easiest: ask me to do it.

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

## 7. Before you take real orders: fill these in (2026-11-26 audit)

Open `tools/admin.html` (or edit `site/config.js`). The checker (`node tools/check_site.js`) warns until each is set.

| Setting | Why |
|---|---|
| `BUSINESS_NAME`, `BUSINESS_ADDRESS` | Shown on the policies page and in the footer. Card networks, Shopify, TikTok Shop and ad platforms expect a business name and contact address. Every marketing email must include a postal address (CAN-SPAM); a registered PO box is allowed. |
| `SHIP_WINDOW` (e.g. "Ships 4–6 weeks after payment") | FTC Mail, Internet, or Telephone Order Rule: if you don't state a ship time you must be able to ship within 30 days, and if you'll miss the time you must get the buyer's consent to the delay or refund them. |
| `ORIGIN` ("Made in USA" / "Imported") | Shown on every product. The FTC Textile Rule covers country of origin in mail-order (online) advertising (16 CFR 303.34). "Made in USA" must be all or virtually all US-made. |
| `CONTACT_EMAIL`, `FORM_ENDPOINT` | Real inbox; a form service so preorders arrive without the shopper's email app. |
| `SHIPPING_FLAT` | $9 is a placeholder. Weigh a packed hoodie. |
| `POLICY_UPDATED` | Date shown on the policies page. |
| Size charts | Every item's size guide still says "coming soon"; all sales are final, so buyers need these. |

`site/policies.html` holds Terms of sale, Shipping, Returns, Privacy and Contact. It fills itself from config. **It is a starting template, not legal advice: have a lawyer review it before launch**, and update it when you add services (payments, email tool, SMS, analytics).

Also: "paper packaging" is what the site claims. Most shipping labels and tape are plastic film or use synthetic adhesive, so use paper tape and paper labels, and keep supplier spec sheets for every "no plastic" claim (FTC Green Guides: environmental claims need proof).

## 8. Legal protection: what actually protects you (2026-11-26)

No website text makes a business lawsuit-proof. Policies reduce risk; these do most of the work. **Have an Ohio lawyer review the policies page before you take real orders** (a one-time review is usually a few hundred dollars; get a quote).

1. **Form the LLC before selling** ($99 in Ohio) and keep it separate: its own bank account and card, sign everything as the LLC. Mixing personal and business money can let a court ignore the LLC and reach your personal assets.
2. **Insurance:** general liability *with product liability* (~$350–750/yr, earlier estimate). This pays lawyers if someone claims an injury or allergic reaction. Terms can't do that.
3. **Flammability (federal law, applies to all clothing):** brushed fleece is a "raised-surface" fabric, and cotton or hemp fleece is **not** in the testing exemption (only plain fabrics ≥2.6 oz/yd², or fabrics of acrylic, modacrylic, nylon, olefin, polyester or wool, are exempt). So **hoodies and sweatpants need a 16 CFR 1610 flammability test and a General Certificate of Conformity (GCC)** before sale; tees (plain jersey ≥2.6 oz) and wool items fall under the exemption. Adult apparel can be tested by any competent lab, not only CPSC-accepted ones. Ask your fabric mill for 16 CFR 1610 results first. ([CPSC clothing FAQ](https://www.cpsc.gov/FAQ/Clothing), [CPSC 2016 enforcement policy](https://www.federalregister.gov/documents/2016/03/10/2016-04533/statement-of-policy-on-enforcement-discretion-regarding-general-conformity-certificates-for-adult))
4. **Labels:** fiber %, country of origin, your name or RN, care instructions, and the latex line on boxers/sweatpants (FTC Textile Rule, Care Labeling Rule).
5. **Keep proof:** every preorder request records the terms date, the exact text agreed to and the time (`agreed_to`, `agreed_at`). Keep these emails. When you move to Shopify, turn on a required "I agree to the Terms" checkbox at checkout (may need an app on Basic) so the agreement stays a "clickwrap", which courts enforce far more often than a link in the footer ("browsewrap").
6. **Refund policy posted before purchase:** Ohio's Consumer Sales Practices Act requires a return policy to be posted clearly before the sale, not only on a receipt; without a posted policy a buyer can demand a refund ([Ohio AG](https://ohioattorneygeneral.gov/Business/Services-for-Business/Business-Guide/Refund-Policies-and-Restocking-Fees)). The site shows "All sales final" on products, in the list and in the tick box.
7. **Accessibility:** website accessibility suits are common and online retailers are the main targets (thousands of federal filings a year). The site passes an automated WCAG check and has an accessibility statement; keep testing after changes.
8. **Brand name:** run a USPTO search (class 25) before you buy labels and a domain; a trademark complaint is one of the most common ways small clothing brands get sued.
9. **Designs:** don't use other brands' marks, lyrics, characters or real people. Keep the no-suicide-method line.
10. **Not included on purpose:** an arbitration clause and class-action waiver (decided 2026-11-26). With the AAA the business registers the clause (~$600 plus $600 a year) and pays most of each case's fees, and "mass arbitration" can be ruinous for a small seller. Revisit with a lawyer once sales grow.

What's in the policies page: who can buy (18+), contract formed at payment, right to cancel errors/fraud, ship-time and delay handling (FTC Mail Order Rule), conspicuous "as is" warranty disclaimer and liability cap (to the extent the law allows), dark-humor/not-advice statement with crisis lines, copyright, informal 60-day dispute step, Ohio law and venue, force majeure, severability, product-safety notes (latex, dye transfer, fire, adult-only drawcords), privacy (retention, security, no selling or targeted-ad sharing, kids, Do Not Track) and accessibility statement.

## 9. Fit, Saved, "Get the set", drop-alert card, About (2026-11-26)

All in `tools/admin.html` → **Fit, sets, drop alerts & About** (or `site/config.js`):
- **FIT / WEIGHT:** one line per item, e.g. "Relaxed, boxy fit. True to size; size down for a closer fit." and "400 GSM". Shown under the sizes on every product and at the top of the size guide. Blank = hidden. Fill these before selling: all sales are final.
- **Saved (hearts):** shoppers tap ♡ on any product; saved items live on their device only and appear under the heart button in the header. Nothing to set up.
- **Get the set:** hoodies and sweatpants that share a design show a "Get the set" box with both size pickers and one "Add both" button. `SET_DISCOUNT` = dollars off per hoodie + sweatpants pair in one order (0 = no discount). Check your margin first (US-made: hoodie ~52%, sweatpants ~44% after card fees).
- **Drop-alert card:** a small card ("Get first access to new drops") shows once, after 30 seconds or the 2nd product opened, never on top of another pop-up, and not again for 30 days after it's closed or ever after someone joins. No discount. Turn it off with `DROP_PROMPT: false`.
- **About:** write 3–6 sentences (who you are, why natural fiber, why the dark humor). Blank paragraphs split it. Optional photo: put it in `site/photos/` and enter `photos/about.jpg`. Blank text hides the section and its footer link.
- **Sizes:** hoodies, tees and sweatpants now go S–4XL. Size-chart rows and tech-pack measurement columns include 4XL; your sewer needs to grade the extra size.

# Project handoff: dark-humor natural-fiber hoodie brand (as of 2026-11-24)

Read this first. Not legal/tax advice. Prices are web research (Nov 2026); "est." = estimate, "verify" = check at source.

## User
- First business ever. Lives in Ohio, may move to Florida.
- Wants unbiased facts, no agreeableness, thorough research before answering.
- Makes own final designs; I give captions, SVG layout sketches, print-method advice.

## Product decisions (current)
- Hoodies only. Audience: alternative + gym culture. Very dark humor (pain, depression, dread, mortality, survival); intent is connection, not glamorizing.
- **No plastics / synthetic polymers anywhere** (fabric, rib, thread, cord, labels, print, packaging). Natural polymers (cotton, guar, starch) are fine.
- **Organic dropped** (saves only ~$2.50/hoodie). Natural fibers stay.
- **Best blend: ~30% hemp / 70% cotton brushed fleece, 330–400 GSM.** 55/45 if durability > first-wear softness. Rib: heavy 100% cotton, no spandex.
- **Margin target: >50%, quality high.**
- Returns: recommended 1 free size exchange, 80% refund (20% restocking) on unworn within 14–30 days, full refund for defects, final sale only for marked seconds. No-returns can't block defect/not-as-described refunds or chargebacks.
- User likes a "Happy Clothing Company" hoodie (thehappyclothingcompany.com, 20% polyester). Site blocked by network; user declined allowing it. Use it as fit/feel reference; RN on label at rn.ftc.gov identifies maker.

## Design line
- I won't make designs that show a suicide method as the image or read as encouragement. Everything else dark is fine.
- User's "noose + keep hanging on": not drawn (method image + US lynching symbol; platform/processor risk). Replaced with dead-hang pull-up version.
- "Cliff + take the leap": drawn as box jump.
- 988 in footer/packaging as plain text (not altered logo). Crisis Text Line: text HOME to 741741.

## Key numbers
- US sewer, mid inputs: ~$106 to make + market (incl. $20 own time, $10 marketing). ~$18/hoodie at $150. Break-even 221 units at $150, 89 at $180 (natural-dye default).
- Gross margin by sourcing (incl. dye/print, 45 min own time, packaging): US conventional ~$72 cost (52% at $150); Portugal full package ~$58 (52% at $120; White Cotton €21–29, MOQ 75); Pakistan ~$47 (61% at $120; Sialkot $13–16 FOB at 30–100 pcs). Tariffs uncertain — verify at hts.usitc.gov.
- Self-sewn: cash cost ~$43 (64% at $120) but ~$103 with own time paid; ~20 hoodies/week full-time; ~$1,050 machines + pattern.
- Decoration (Decoration options sheet): natural dye $5.50/unit + $900 equip; discharge $2 + $525; embroidery (Brother PE900) $2 + $1,500. Method changes margin only ~2 pts.

## Other products (2026-11-24, all estimates; see docs/other-products.md)
- Cost to make incl. own time, paid US maker → margin at high price: tee $41 (31% at $60), sweats $74 (47% at $140), boxer brief $23 (41% at $38), socks $10 (58% at $24), beanie $21 (47% at $40), dad cap $18 (56% at $40), duck jacket $192 (41% at $325). Overseas full package hits 50%+ on all at the high price (only the tee has real listing prices).
- Hard plastic-free parts: waistband/underwear elastic (use cotton-covered natural rubber; latex disclosure, ~1–6% allergy), socks (no nylon/spandex → wear/slide; factory knit-in only, MOQ ~144), cap hidden parts (sweatband, brim board, thread), jacket (lining/insulation → flannel + wool batt + cupro sleeves; zipper tape usually polyester, YKK cotton-tape "Universal" unconfirmed for heavy separating).
- Suggested order: sweatpants → beanie → tee → socks/caps → underwear → jacket last (~$10.6k first run).
- Inputs-sheet bug fixed: legend note had overwritten Inputs!A44 label ("Other" row); now uses legend_row.

## Print / decoration facts
- Plastisol (PVC), water-based/discharge inks (acrylic binders), DTG, DTF, sublimation all fail no-polymer rule. Laser etching not recommended (>20% natural fiber).
- Passes: natural-dye screen printing (mordant or extract paste, steam), block printing, cotton/rayon embroidery (cotton backing or muslin; most cutaways are polyester), discharge (only on reactive/Procion-dyed fabric; confirm Jacquard deColourant SDS has no binder).
- Natural black (logwood + iron) fades in sun; disclose.
- Thread is the weak point: 100% cotton is weaker/linty; stretch-test seams; silk for stress seams.

## Business setup facts
- Ohio LLC $99, no annual report; Florida $125 + $138.75/yr. Ohio CAT exclusion $6M.
- Shopify Basic $39/mo ($29 yearly), 2.9% + 30¢. Insurance ~$350–750/yr.
- FTC labels: fiber %, origin, name or RN, care label. Mail Order Rule for preorders.
- Copyright fees change Jan 5, 2027 (Standard $65 → $85; Single App proposed retired — verify).

## Files in repo
- `docs/report.md` — full research report (also published: https://claude.ai/artifact/XFChP2Bmwv7JcoJgG426N4, slug f4edc7d6-b149-49b7-8038-e73fa9b21271; rebuild HTML from md files and republish).
- `docs/margin-model.xlsx` — edit blue cells; sheets: Inputs, Scenarios, Self-sewn vs sewer, Decoration options, Other products. Built by `tools/build_xlsx.py`; recalc with the xlsx skill's recalc.py.
- `docs/decoration-supplies.md` — tools/materials/prices/how-to for natural dye, discharge, embroidery.
- `docs/other-products.md` — tees, sweatpants, underwear, socks, beanie, dad cap, heavy duck jacket: blend/build, plastic-free problems, sourcing, margins. Workbook sheet "Other products" (blue inputs; margins, price for 50%, break-even, first-run cash).
- `docs/other-products-equipment.md` — every machine/tool/material with prices + how-to per product; core studio $1,951–3,421 if self-sewn ($342–777 with paid sewer); all products incl. decoration ~$5,890–9,410.
- `docs/swatch-order-list.md` — fabric/rib/thread swatches to buy and test.
- `designs/concepts.md` — 40 captions with risk ratings + "Sketch set 2" index table (sketches 08–107: 34 from the list, 66 new captions; new ones web-checked 2026-11-24; round 2 replaced 15 captions with darker death/burial/grief ones (incl. the TM-problem #65, #89 and already-sold #69, #88), cautions #82 DIE TIRED app, #89 Hot Topic "Currently decomposing"; user asked to edge toward method references — declined, line holds; USPTO/Etsy blocked here). `designs/sketches/*.svg`: all 107 built by `tools/svgs_dark.py` from `tools/designs_data.py` (FIRST = 01–07, DESIGNS = 08–107). Style (2026-11-24, user asked for darker content, any hoodie color): dark art (skulls, skeletons, coffins, graves, moths, ravens, dead roses, candles), gothic type outlined from OFL fonts in `tools/fonts`, worn-print texture, 10 natural-dye hoodie colors (black, oatmeal, oxblood, plum, heather, indigo, olive, dusty rose, charcoal, sand) with contrasting ink. Round 3 (2026-11-24): user asked for more morbid, "as close to methods as allowed". Methods and near-misses are still excluded; morbid death/body imagery is fine. Added morgue/autopsy, rot, anatomy/gore and funeral/reaper art and rewrote 32 captions (src "new3"; #103 changed off DEATHGRIP TM, #13 changed off a real pre-workout death). Platform risk M for gore. Round 4 (2026-11-24): user said "too friendly" = captions too punny (art/colors kept). 71 captions rewritten as cold, plain death/decay/grief statements (src "new4"); #94 "The void called" pulled (l'appel du vide = jump urge); swapped off TMs MORTAL, FLATLINE, HEAVY HEART, MEMENTO MORI, ROUTINE and sold "Death Can Wait"/"We Are Not Forever". Rule added: no lines expressing a wish to die. Contact sheets: `overview-01-25.png` … `overview-101-107.png`. Gallery page (all 107, filter by placement): https://claude.ai/artifact/KmKWiokA56KcfBpsBMi7U4, slug 97f4a165-13d7-4e71-9d85-eda9106cfae1.
- Older Claude Docs from a prior session: main points https://claude.ai/artifact/7Ysk53stPEMhTXRDsbfSoN, playbook https://claude.ai/artifact/XxV8rHdC8MJtPCqZPeVC8u, factory kit https://claude.ai/artifact/QQZpmqMPCWcGb6fjaXoUHq (pre-restart; some content outdated).

## Storefront (2026-11-24)
- `site/`: static showcase shop (plain HTML/CSS/JS, no build). User chose: showcase only (no payment; preorder list + email/form request), both category and theme drop-downs, hand-picked featured row labeled "Featured" (not "best sellers" until real sales), all 107 designs, placeholder brand "Brand Name".
- Data/images: `python3 tools/build_site.py` → `site/products.js` + `site/img/` (clean renders via `render(..., clean=True, out=...)` in svgs_dark.py). FEATURED, PRICE ($150), COMING_SOON, icon→theme map live there. Settings in `site/config.js`.
- Design: user chose "Clean" (2026-11-24) after seeing 7 looks; the others and the look generator were deleted. Single page `site/index.html` + `site/style.css` (light store theme block at the end overrides the defaults above it). Fonts on site: Pirata One (logo), Oswald (buttons). 2026-11-25: top of page has no text (user request): a slow endless strip of raised image-only boxes for the hoodies in `HERO_ROTATION` (design numbers), loop length `HERO_SPEED` seconds (default 60), pauses on hover/focus, static swipeable row under reduced motion; tagline moved to About; announcement strip removed. Product boxes: rounded, raised ("bubbled": grey page #ececec, thick bottom edge, deep shadow, lift on hover), price directly under each picture. User wanted the layout like theburntpeanut's store; site unreachable here and user declined network access, so not referenced. User denied republishing the preview this time; artifact still at the previous version.
- Product links are `#slug` (artifact viewer passes plain hashes only). Filters sync to the query string.
- Preview artifact: https://claude.ai/artifact/CJ1kBxHD7rw5FRvQe3Y2H8, slug 5b74a0d4-d6f9-494f-9228-089e5255c623, version 1795559735-2e0f (republish with publish_files; patch mode keeps unlisted files). In the artifact frame, mailto links may not open; the address is shown as text.

## Status / open items
- **GitHub:** pushed to branch `claude/dark-humor-apparel-brand-mbgd2e` on RedFro180/Clothing (2026-11-24) after the Claude GitHub App was given access to the repo. Push new commits there. Report page last republished as version 1795521705-b615 (sections 13 other products, 14 equipment).
- Offered, not yet done: no-plastic spec sheet + quote emails for Pakistan/Portugal/US sewers; marketing "team" (Claude role files and optional weekly scheduled task) — user to pick option, platforms, voice references.
- To do (user): pick brand name; buy swatches and wash-test; buy one 100% cotton heavyweight hoodie to compare with the Happy Clothing hoodie; choose decoration method; get factory samples.

# 50 simulated customer journeys (2026-11-25)

Script: `tools/customer_runs.js` (Playwright; run with `node tools/customer_runs.js`). Raw log: `customer-runs-2026-11-25.json`.

**Setup:** 50 runs, 10 shopper types × 5 each:
- ring impulse buyer, searcher, theme browser, color shopper, grid scroller
- multi-item buyer, wants a sold-out size, unsure of size
- arrived from a shared link, returning visitor

36 runs used phones (iPhone SE, iPhone 13, Pixel 7) and 14 used desktops. For the test only, sizes were marked sold out on 4 designs. Every run went from landing to a submitted preorder request.

## Results
- 0 page errors. All 50 runs reached a product; 41 submitted a preorder and 9 hit a sold-out size and used "Notify me".
- About 7 clicks from landing to preorder request (6.4 from a shared link, 8.4 via search).

| Problem | Runs | Why it hurts sales |
|---|---|---|
| Shipping cost unknown ("$150 + shipping") | 41/41 checkouts | Unexpected or unknown extra costs are the most-cited reason shoppers abandon checkout |
| Sending a preorder opens the email app; buyer must still press Send there | 41/41 | Extra step outside the site; many phones have no mail app set up |
| Restock request also opens the email app | 9/9 | Same |
| Sold-out size: no suggestion of similar hoodies in that size | 9/9 | Dead end |
| Add button below the screen on iPhone SE (568 px tall) | 9/9 SE runs | Must scroll inside the pop-up to buy |
| Size guide has no numbers | 5/5 who opened it | All sales final + no measurements = hesitation / chargebacks |
| Color chip off-screen (had to swipe) | 3 | Minor |

## Search test (28 words a customer might type)
Search only matches caption text, color and theme names. So:
- "hoodie", "skull", "pink", "sad", "depression", "funny", "3am", "tombstone", "xl", "zip up" and "mom" all returned **0 results**.
- "coffin" returned 1 result even though 7 designs show coffins.
- About 9 designs show a skull.

# Your private shop data (PostHog)

The website sends anonymous events to **PostHog**. Only you can see them, in your PostHog login. It's free up to 1 million events a month; check posthog.com/pricing for current limits.

No cookies are set (`persistence: "memory"`), and no names, emails or phone numbers are sent. Preorder details still go only to you, through the preorder form.

## Setup (about 10 minutes)
1. Create a free account at posthog.com and choose the **US** region.
2. Go to **Project settings** and copy the **Project API key**. It starts with `phc_`.
3. In `site/config.js`, set `POSTHOG_KEY: "phc_..."`. If you chose the EU region, also set `POSTHOG_HOST: "https://eu.i.posthog.com"`.
4. Publish the site.

Tracking does **not** run inside the claude.ai preview, which blocks outside connections. It only works on real hosting.

## What the site records

| Event | When | Useful fields |
|---|---|---|
| `$pageview` / `$pageleave` | Page opened / closed | automatic |
| `product_viewed` | Product pop-up opened | `id`, `name`, `theme`, `color`, `seconds_on_site`, `clicks_so_far` |
| `added_to_list` | Added to the preorder list | `id`, `name`, `size`, `qty`, `from` (`product` or `buy_it_with`) |
| `search` / `search_no_results` | A search was typed | `q`, `results` |
| `suggestion_opened` | A "Buy it with" or "Available in" hoodie was opened | `from`, `to` |
| `variant_switched` | Shopper switched to the same design on another item in "Also in this design" | `from`, `to`, `type` (breakdown by `type` shows which items people want in a design they like) |
| `preorder_sent` | The preorder request was sent (your "purchase" until real checkout exists) | `items`, `item_count`, `subtotal`, `shipping`, **`clicks_to_purchase`**, **`seconds_to_purchase`** |
| `bought_together` | One event for each pair of different hoodies in the same preorder | **`pair`** (e.g. "Grief has weight. + The dirt always wins."), `a`, `b` |
| `session_end` | The visitor leaves or switches away | **`seconds_on_site`**, **`clicks`**, `products_viewed`, `viewed_names`, `items_in_list`, **`purchased` (true/false)**, `last_product` |

## The dashboard to build (PostHog → Product analytics → New insight)
1. **Bought together:** Trends → event `bought_together` → breakdown by `pair` → table. It shows the most common pairs.
2. **Clicks per purchase:** Trends → event `preorder_sent` → measure **average** of property `clicks_to_purchase`. Add the median too.
3. **Time on site:** Trends → event `session_end` → **average** of `seconds_on_site`. Breakdown by `purchased` compares buyers with non-buyers.
4. **Non-buyers:** Trends → event `session_end`, filter `purchased = false`:
   - breakdown by `last_product`: the last hoodie they looked at before leaving
   - breakdown by `items_in_list`: people who added to the list but never sent it (abandoned list)
   - Use average `products_viewed`, `seconds_on_site` and `clicks` to see how far they got.
5. **Funnel:** Funnels → `$pageview` → `product_viewed` → `added_to_list` → `preorder_sent`. Shows where people drop off.
6. **Most viewed vs most added:** Trends → `product_viewed` and `added_to_list`, both broken down by `name`.
7. **Failed searches:** Trends → `search_no_results` → breakdown by `q`. Tells you what people want that you don't have, or don't name that way.

## Limits
- **Too few visitors:** numbers mean little until each design has dozens of views.
- **Ad blockers** hide some visitors.
- **"Purchase" means preorder request sent.** Once you move to Shopify, use Shopify's own sales reports for real orders. Shopify and TikTok Shop each have their own analytics.
- **Session end can be missed:** `session_end` is sent when the tab closes or is hidden, and some phones kill the page without warning, so a few sessions will lack it. `$pageleave` from PostHog covers part of that.

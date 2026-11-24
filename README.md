# Dark-humor natural-fiber hoodie brand

- `docs/report.md`: sourcing (no-polymer fabric, rib, thread, natural dye, printing), fit and manufacturing, business setup (Ohio vs Florida), margins, launch steps.
- `docs/margin-model.xlsx`: editable cost and margin model (edit the blue cells).
- `designs/concepts.md`: 40 caption concepts with ratings, plus an index of hoodie sketches 08–107.
- `designs/sketches/`: 107 SVG hoodie placement sketches; `overview*.png` contact sheets show them.
- `docs/other-products.md`, `docs/other-products-equipment.md`: tees, sweatpants, underwear, socks, hats, jackets, and every tool and machine with prices.
- `tools/`: scripts that generate the sketches (`svgs_dark.py`) and the workbook (`build_xlsx.py`); `tools/fonts` holds the open-licensed (OFL) fonts.

Research as of Nov 2026. Not legal, tax or financial advice.

## Storefront website (`site/`)
A showcase shop with no payment yet: a featured row at the top, all 107 hoodies auto-filled below, drop-downs for category (hoodies live, other products "coming soon"), theme and color, plus sort and search. Product pop-ups have a size picker. The preorder list is saved in the visitor's browser and sent as a request by email or a form service.

- **Rebuild after design changes:** `python3 tools/build_site.py`, then `python3 tools/build_looks.py`. The first re-renders `site/img/` and `site/products.js` from `tools/designs_data.py`; the second writes the four pages.
- **Four looks, same products and features**, with a switcher bar at the top of each page:
  - `index.html` (Original): dark, plain grid.
  - `look-poster.html` (Poster): light paper, big hero hoodie, sentence-style filters ("Show me … from … in …"), mixed-size cards.
  - `look-parlor.html` (Parlor): night/candle glow, arched chapel-window frames, staggered columns.
  - `look-zine.html` (Zine): photocopied paper, ransom-note headline, taped tilted polaroids.
  - Page structure lives in `tools/site_template.html` (don't edit the `site/*.html` files directly; they're regenerated). Each look's styling is `site/look-*.css` on top of `site/style.css`. Once you pick one, delete the others from `LOOKS` in `tools/build_looks.py`, or rename your pick to `index`.
- **View locally:** open `site/index.html`, or run `cd site && python3 -m http.server` and go to http://localhost:8000.
- **Brand name, tagline, featured label, contact email, form URL:** `site/config.js`.
- **Featured picks, price, coming-soon list:** top of `tools/build_site.py`. A design's theme can be overridden with `theme="rot"` in its `D(...)` entry.
- **Keep the label "Featured"** until there are real sales. Calling unsold items "best sellers" is a false claim.
- **Requests:** with `FORM_ENDPOINT` empty, the site opens the visitor's email app addressed to `CONTACT_EMAIL`. To receive requests without relying on email apps, paste a form-service URL (e.g. Formspree) into `FORM_ENDPOINT`.
- **Free hosting:** GitHub Pages' "deploy from a branch" only serves `/` or `/docs`, and `docs/` already holds the research files. So either set Pages to "GitHub Actions" with a static-site workflow pointed at `site/`, or put `site/` on Netlify or Cloudflare Pages (drag-and-drop, free tier). GitHub Pages on a free account needs a public repo, which would make the research docs public too.
- **Adding payment later:** either Stripe Payment Links (one link per product/size, no monthly fee, swap the "Add" button for the link) or move to Shopify and reuse the images and copy.

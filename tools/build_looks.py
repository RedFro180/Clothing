"""Build the storefront pages in several looks from one template.
Run: python3 tools/build_looks.py   (after tools/build_site.py)
Template: tools/site_template.html. Every look uses the same app.js, products.js and config.js;
a look changes the hero, the filter bar markup and adds its own stylesheet on top of style.css."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, "..", "site"))
TPL = open(os.path.join(HERE, "site_template.html")).read()

KICK = '<p class="kicker">Hemp &amp; cotton fleece · natural dyes · zero plastic</p>'
LEDE = '<p class="lede">Heavy hoodies for people who lift, grieve and laugh at the wrong things.</p>'
CTA = '<a class="btn" href="#shop">Shop the drop</a>'
def art(i, cls=""):
    return f'<a class="hero-art {cls}" data-hero="{i}" href="#shop"><img alt="" width="560" height="570"></a>'

SENTENCE = '''<form class="filters sentence" id="filters" onsubmit="return false">
      <span>Show me</span>
      <label><span class="sr">Category</span><select id="fCat"></select></label>
      <span>from</span>
      <label><span class="sr">Theme</span><select id="fTheme"></select></label>
      <span>in</span>
      <label><span class="sr">Color</span><select id="fColor"></select></label>
      <span>sorted by</span>
      <label><span class="sr">Sort</span><select id="fSort">
          <option value="featured">featured first</option>
          <option value="new">newest</option>
          <option value="az">A to Z</option>
        </select></label>
      <label class="search"><span class="sr">Search</span>
        <input id="fSearch" type="search" placeholder="search: coffin, grief, rot…" autocomplete="off"></label>
    </form>'''

LOOKS = {
    "index": dict(name="Original", css=None, hero=None, filters=None),
    "look-poster": dict(
        name="Poster", css="look-poster.css", filters=SENTENCE,
        hero=f'''<section class="hero hero-poster">
    <div class="hp-text">{KICK}
      <h1 data-tagline>Dark humor. Natural fiber. No plastic.</h1>
      {LEDE}
      {CTA}
    </div>
    <div class="hp-art">{art(0)}<p class="hp-cap" data-hero-name="0"></p></div>
  </section>'''),
    "look-parlor": dict(
        name="Parlor", css="look-parlor.css", filters=SENTENCE,
        hero=f'''<section class="hero hero-parlor">
    <div class="fan">{art(1, "side")}{art(0, "mid")}{art(2, "side")}</div>
    {KICK}
    <h1 data-tagline>Dark humor. Natural fiber. No plastic.</h1>
    {LEDE}
    {CTA}
  </section>'''),
    "look-zine": dict(
        name="Zine", css="look-zine.css", filters=None,
        hero=f'''<section class="hero hero-zine">
    <div class="zt">
      <h1 class="ransom" aria-label="Dark humor. Natural fiber. No plastic."><span>DARK</span> <span>humor.</span> <span>NATURAL</span> <span>fiber.</span> <span>NO</span> <span>plastic.</span></h1>
      <p class="lede" data-tagline>Dark humor. Natural fiber. No plastic.</p>
      {LEDE}
      {CTA}
    </div>
    <div class="scatter">{art(0, "p1")}{art(1, "p2")}{art(2, "p3")}<span class="sticker">100%<br>no<br>plastic</span></div>
  </section>'''),
}

HERO_JS = '''<script>{
  const f = window.CATALOG.products.filter(p => p.featured).sort((a, b) => a.featured - b.featured);
  document.querySelectorAll("[data-hero]").forEach(a => { const p = f[+a.dataset.hero]; if (!p) return;
    a.href = "#" + p.slug; a.setAttribute("aria-label", p.name); const i = a.querySelector("img"); i.src = p.img; i.alt = p.color + " hoodie: " + p.name; });
  document.querySelectorAll("[data-hero-name]").forEach(e => { const p = f[+e.dataset.heroName]; if (p) e.textContent = p.name + " / " + p.color; });
}</script>'''

def build():
    for key, L in LOOKS.items():
        s = TPL
        bar = "".join(f'<a href="{k}.html"{" aria-current=\"page\"" if k == key else ""}>{v["name"]}</a>' for k, v in LOOKS.items())
        s = s.replace("<!--LOOKS-->", f'<nav class="looks" aria-label="Page design">Design: {bar}</nav>')
        if L["css"]:
            s = s.replace('<link rel="stylesheet" href="style.css">',
                          f'<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="{L["css"]}">')
            s = s.replace("<body>", f'<body class="{key}">')
        if L["hero"]:
            s = re.sub(r'<section class="hero">.*?</section>', lambda m: L["hero"], s, count=1, flags=re.S)
        if L["filters"]:
            s = re.sub(r'<form class="filters".*?</form>', lambda m: L["filters"], s, count=1, flags=re.S)
        s = s.replace('<script src="app.js"></script>', '<script src="app.js"></script>\n' + HERO_JS)
        open(os.path.join(SITE, key + ".html"), "w").write(s)
    print("built", ", ".join(k + ".html" for k in LOOKS))

if __name__ == "__main__":
    build()

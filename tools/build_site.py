"""Build the storefront data and product images.
Run: python3 tools/build_site.py
Writes site/img/*.svg (clean product mockups) and site/products.js (all product data).
Edit FEATURED, PRICE and TYPES/ITEMS here; edit brand name, labels and form settings in site/config.js."""
import os, sys, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import svgs_dark as S
import items as I

SITE = os.path.normpath(os.path.join(HERE, "..", "site"))
IMG = os.path.join(SITE, "img")
PHOTOS = os.path.join(SITE, "photos")   # drop real photos here as NN-anything.jpg (e.g. 11-front.jpg); they show first

# Design numbers shown in the top row, in order. Swap for real best sellers once orders exist.
FEATURED = [11, 10, 27, 44, 29, 60, 13, 48]
PRICE = 150          # hoodie price, USD (docs/margin-model.xlsx: ~52% margin at $150, US conventional)
SIZES = ["S", "M", "L", "XL", "2XL", "3XL"]

# Item types (docs/other-products.md). Live types get products; the rest show as "coming soon".
# id, menu label, singular word, plural word, price (one price per type), live
TYPES = [
    ("hoodie", "Hoodies", "hoodie", "hoodies", PRICE, True),
    ("tee", "Tees", "tee", "tees", 60, True),
    ("hats", "Hats", "hat", "hats", 40, True),
    ("underwear", "Underwear", "pair of boxers", "boxers", 38, True),
    ("socks", "Socks", "pair of socks", "socks", 24, True),
    ("sweatpants", "Sweatpants", "pair of sweatpants", "sweatpants", 140, True),
]
TPRICE = {t[0]: t[4] for t in TYPES}
NATURAL_DYE = "Natural dyes fade gradually with sun and washing"
PREORDER = "Preorder: no charge until we confirm a ship date"
HOODIE_DETAILS = ["~30% hemp / 70% cotton brushed fleece, heavyweight", "Cotton rib, thread, drawcord and labels. No plastic."]
# Non-hoodie items: picture kind (tools/items.py), product type, name suffix, sizes, placement, details, notes
ITEMS = [
    ("tee", "tee", "Tee", SIZES, None,
     ["30% hemp / 70% cotton jersey, heavyweight", "Cotton rib collar, cotton thread and labels. No plastic.",
      "The collar has no spandex, so it can relax over time"], ["All sales final: check the size guide"]),
    ("hats-beanie", "hats", "Beanie", ["One size"], "Embroidered cotton patch on the cuff",
     ["100% cotton or merino rib knit, cuffed", "Cotton patch, cotton thread and label. No plastic.", "Stretches to fit most heads"],
     ["All sales final"]),
    ("hats-cap", "hats", "Dad cap", ["One size"], "Embroidered front",
     ["100% cotton twill, unstructured", "Cotton sweatband and thread, cardboard brim (no plastic), brass buckle strap",
      "Adjustable strap, fits most heads"], ["All sales final"]),
    ("underwear", "underwear", "Boxers", ["S", "M", "L", "XL", "2XL"], "Leg print + printed cotton waistband",
     ["100% woven cotton boxers, loose fit", "Waistband: natural rubber elastic inside a printed cotton casing. No plastic, no spandex.",
      "Line dry or tumble low: heat wears out natural rubber faster"],
     ["Contains natural rubber latex (not for latex allergies)", "Final sale (hygiene)"]),
    ("socks", "socks", "Socks", ["S/M", "L/XL"], "Design knitted in",
     ["Cotton or merino crew sock, knitted with the design in it", "No nylon or spandex. No plastic."],
     ["No nylon or spandex: they slide more and wear faster at heel and toe", "Final sale (hygiene)"]),
    ("sweatpants", "sweatpants", "Sweatpants", SIZES, "Print on the left thigh",
     ["~30% hemp / 70% cotton brushed fleece, same as the hoodies", "Heavy cotton rib cuffs, cotton drawcord, cotton thread and labels",
      "Waist: natural rubber elastic inside a cotton casing. No plastic, no spandex.", "Line dry or tumble low: heat wears out natural rubber faster"],
     ["Contains natural rubber latex (not for latex allergies)", "All sales final: check the size guide"]),
]
SINGULAR = {t[0]: t[2] for t in TYPES}

THEMES = {
    "morgue": "Morgue & autopsy", "rot": "Rot & decay", "anatomy": "Anatomy",
    "grave": "Graves & funerals", "grief": "Grief & the mind", "iron": "Iron & sweat",
}
ICON_THEME = {
    **dict.fromkeys(["toe_tag", "body_bag", "morgue_drawer", "y_incision", "autopsy_report", "bottle"], "morgue"),
    **dict.fromkeys(["rot_skull", "rot_lifter", "flower", "skull_flies", "maggots", "flies"], "rot"),
    **dict.fromkeys(["anatomical_heart", "flayed_figure", "brain", "heart", "flatline", "skull",
                     "death_grip", "hand_skel"], "anatomy"),
    **dict.fromkeys(["coffin", "tombstone", "open_grave", "reaper", "obituary", "wreath", "hourglass"], "grave"),
    **dict.fromkeys(["ghost", "clock", "eye", "moon", "sun", "candle", "battery", "checklist"], "grief"),
    **dict.fromkeys(["barbell", "plate", "rack", "dumbbell", "kettlebell", "figure", "figures2"], "iron"),
}
KEYWORDS = [("rot", ["ROT", "MAGGOT", "WORM"]), ("grave", ["GRAVE", "ASHES", "COFFIN", "BURIED"]),
            ("iron", ["LIFT", "SET", "BAR ", "REP", "CHALK", "SWEAT"]),]
PLACE = {"front": "Front print", "back": "Back print", "chest": "Left-chest print",
         "sleeve": "Sleeve print", "pocket": "Pocket print", "hood": "Hood print"}

def theme_for(d):
    if d.get("theme"):
        return d["theme"]
    if d["icon"] in ICON_THEME:
        return ICON_THEME[d["icon"]]
    text = " ".join(d["lines"]) + " "
    for t, words in KEYWORDS:
        if any(w in text for w in words):
            return t
    return "grief"

# Words a shopper might type, by what is drawn on the hoodie (icon) and by theme, for search.
ICON_TAGS = {
    "skull": "skull bones death", "rot_skull": "skull rot decay bones", "skull_flies": "skull flies rot",
    "skeleton": "skeleton bones", "figure": "skeleton bones gym lift", "figures2": "skeletons friends gym together",
    "rot_lifter": "skeleton rot gym lift", "hand_skel": "skeleton hand bones", "death_grip": "skeleton hands grip bones",
    "coffin": "coffin casket funeral", "tombstone": "tombstone gravestone grave rip cemetery", "open_grave": "grave shovel dirt cemetery",
    "reaper": "grim reaper scythe death", "wreath": "funeral flowers wreath", "obituary": "obituary newspaper funeral",
    "toe_tag": "toe tag morgue tag", "body_bag": "body bag morgue", "morgue_drawer": "morgue drawer", "y_incision": "autopsy surgery",
    "autopsy_report": "autopsy coroner report", "bottle": "jar specimen formaldehyde", "anatomical_heart": "heart anatomy organ",
    "heart": "heart love broken", "brain": "brain mind mental", "flayed_figure": "anatomy muscles body", "flatline": "heartbeat ekg flatline hospital",
    "barbell": "barbell gym lift weights", "plate": "weight plate gym lift", "rack": "squat rack gym", "dumbbell": "dumbbell gym weights",
    "kettlebell": "kettlebell gym", "candle": "candle", "moon": "moon night", "sun": "sun", "eye": "eye watching",
    "ghost": "ghost haunted", "clock": "clock time 3am night", "hourglass": "hourglass time", "battery": "battery tired low",
    "checklist": "list checklist", "flower": "flower rose plants", "maggots": "maggots worms rot", "flies": "flies rot",
}
THEME_TAGS = {"morgue": "morgue corpse dead body coroner", "rot": "rot decay decompose worms", "anatomy": "anatomy body organs blood",
              "grave": "grave funeral burial cemetery buried dead death", "grief": "grief sad depression mental health anxiety loss lonely tired",
              "iron": "gym lift lifting workout fitness weights training"}
COLOR_TAGS = {"Dusty rose": "pink rose", "Undyed oatmeal": "cream white beige natural off-white", "Sand": "beige tan khaki",
              "Heather grey": "gray grey", "Charcoal": "gray grey dark", "Indigo": "blue navy", "Oxblood": "red maroon burgundy wine",
              "Olive": "green army", "Plum": "purple", "Black": "black"}

TYPE_TAGS = {"tee": "tee tees t-shirt tshirt shirt", "hats-beanie": "hat hats beanie toque knit", "hats-cap": "hat hats cap dad cap baseball",
             "underwear": "underwear boxers boxer shorts", "socks": "sock socks crew",
             "sweatpants": "sweatpants sweats joggers pants trackpants bottoms"}
def fab_of(num): return S.color_for(num)[1]

def search_tags(d, theme, color):
    return " ".join([ICON_TAGS.get(d["icon"], ""), THEME_TAGS.get(theme, ""), COLOR_TAGS.get(color, "")]).strip()

def title_case(lines):
    """Sentence case: capitalize each sentence start and the word I (I'm, I'll, I've)."""
    import re
    s = " ".join(lines).strip().lower()
    s = re.sub(r"(^|(?<!a\.m)(?<!p\.m)[.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    s = re.sub(r"\bi\b", "I", s)
    return s

def lum(hexc):
    return sum(int(hexc[i:i + 2], 16) for i in (1, 3, 5))

def dedupe(products):
    """Many pictures are identical (a plain back or a fabric swatch only depends on the color), so keep one copy of each:
    identical files become one shared file named by content (s-<hash>.svg). Fewer files to host (preview limit 512)."""
    import hashlib
    first = {}
    for f in sorted(os.listdir(IMG)):
        h = hashlib.sha1(open(os.path.join(IMG, f), "rb").read()).hexdigest()[:10]
        first.setdefault(h, []).append(f)
    rename = {}
    for h, files in first.items():
        if len(files) > 1:
            shared = f"s-{h}.svg"
            os.replace(os.path.join(IMG, files[0]), os.path.join(IMG, shared))
            for f in files[1:]:
                os.remove(os.path.join(IMG, f))
            for f in files:
                rename["img/" + f] = "img/" + shared
    for p in products:
        p["img"] = rename.get(p["img"], p["img"])
        for im in p["imgs"]:
            im["src"] = rename.get(im["src"], im["src"])

def main():
    os.makedirs(IMG, exist_ok=True)
    for f in os.listdir(IMG):
        os.remove(os.path.join(IMG, f))
    products = []
    for i, d in enumerate(S.all_designs(), 1):
        f = S.render(i, d, clean=True, out=IMG)
        extra = S.extra_views(i, d, IMG)
        cname, fab, ink = S.color_for(i)
        prefix = f.split("-")[0] + "-"
        photos = sorted(x for x in os.listdir(PHOTOS) if x.startswith(prefix) and x.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))) if os.path.isdir(PHOTOS) else []
        main_side = "Back" if d["place"] in ("back", "hood") else "Front"
        other_side = "Front" if main_side == "Back" else "Back"
        imgs = [{"src": "photos/" + x, "alt": "Photo"} for x in photos] + [
            {"src": "img/" + f, "alt": f"{main_side}, with print"},
            {"src": "img/" + extra[0], "alt": f"{other_side}, plain"},
            {"src": "img/" + extra[1], "alt": "Print close-up"},
            {"src": "img/" + extra[2], "alt": f"Fabric color: {cname}"}]
        products.append({
            "id": i, "design": i, "slug": d["slug"], "name": title_case(d["lines"]), "sub": d["sub"],
            "type": "hoodie", "typeLabel": "Hoodie", "word": "hoodie", "theme": theme_for(d), "color": cname.split(" (")[0],
            "colorNote": cname, "tags": search_tags(d, theme_for(d), cname.split(" (")[0]), "hex": fab, "light": lum(fab) > 450,
            "placement": PLACE[d["place"]], "price": PRICE, "sizes": SIZES, "img": "img/" + f, "imgs": imgs,
            "featured": FEATURED.index(i) + 1 if i in FEATURED else None,
            "details": [f"Color: {cname}"] + HOODIE_DETAILS + [f"{PLACE[d['place']]}, natural-dye or embroidered", NATURAL_DYE, PREORDER, "All sales final: check the size guide"],
            "notes": [],
        })
    designs = S.all_designs()
    for k, (kind, typ, label, sizes, placement, details, notes) in enumerate(ITEMS, 1):
        for num in I.STARTER:
            d = designs[num - 1]
            main, extra, sides, cname = I.render_item(kind, num, d, IMG)
            color = cname.split(" (")[0]
            pid = k * 1000 + num        # hoodies keep ids 1-107; tee #10 is 1010, beanie #10 is 2010, etc.
            prefix = f"{kind}-{num:02d}-"
            photos = sorted(x for x in os.listdir(PHOTOS) if x.startswith(prefix) and x.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))) if os.path.isdir(PHOTOS) else []
            imgs = [{"src": "photos/" + x, "alt": "Photo"} for x in photos] + [
                {"src": "img/" + main, "alt": f"{sides[0]}, with design"},
                {"src": "img/" + extra[0], "alt": sides[1] if kind == "socks" else f"{sides[1]}, plain"},
                {"src": "img/" + extra[1], "alt": "Design close-up"},
                {"src": "img/" + extra[2], "alt": f"Fabric color: {cname}"}]
            theme = theme_for(d)
            products.append({
                "id": pid, "design": num, "slug": f"{d['slug']}-{kind.replace('hats-', '')}", "name": title_case(d["lines"]), "sub": d["sub"] if typ == "tee" else "",
                "type": typ, "typeLabel": label, "word": SINGULAR[typ] if typ != "hats" else label.lower(), "theme": theme, "color": color, "colorNote": cname,
                "tags": search_tags(d, theme, color) + " " + TYPE_TAGS[kind], "hex": fab_of(num), "light": lum(fab_of(num)) > 450,
                "placement": placement or PLACE[d["place"]], "price": TPRICE[typ], "sizes": sizes, "img": "img/" + main, "imgs": imgs,
                "featured": None,
                "details": [f"Color: {cname}"] + details + ([f"{placement or PLACE[d['place']]}, natural dye"] if typ in ("tee", "sweatpants") else []) + [NATURAL_DYE, PREORDER],
                "notes": notes,
            })
    dedupe(products)
    fonts = os.path.join(SITE, "fonts")
    os.makedirs(fonts, exist_ok=True)
    for f in os.listdir(S.FD):   # the site uses Pirata One (logo) and Oswald (buttons, labels)
        if f.split("-")[0] in ("pirata", "oswald") or f in ("LICENSE-pirata-one.txt", "LICENSE-oswald.txt"):
            shutil.copy(os.path.join(S.FD, f), fonts)
    data = {"products": products, "themes": THEMES,
            "types": [{"id": i, "label": l, "one": one, "many": many, "live": live, "price": pr} for i, l, one, many, pr, live in TYPES]}
    with open(os.path.join(SITE, "products.js"), "w") as fh:
        fh.write("// Generated by tools/build_site.py. Do not edit by hand.\nwindow.CATALOG = ")
        json.dump(data, fh, indent=1)
        fh.write(";\n")
    counts = {t: sum(p["theme"] == t for p in products) for t in THEMES}
    print(len(products), "products;", counts, {t[0]: sum(p["type"] == t[0] for p in products) for t in TYPES if t[5]})

if __name__ == "__main__":
    main()

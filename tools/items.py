"""Mockups for the non-hoodie items: tee, boxers, socks, beanie, dad cap, sweatpants, heavy jacket.
Same look as the hoodie mockups in svgs_dark.py (flat fabric + soft gradient shading, no filters on the garment),
and the same art: tees use the full hoodie layout, small items use the design's icon plus at most one short word.
Used by tools/build_site.py. Each item gets 4 pictures: main, other side, close-up, fabric color."""
import os
import svgs_dark as S

VB = "20 36 560 570"          # same frame as the hoodie pictures, so cards and spin behave the same
E = S.E

# The starter set (same 12 designs on every new item) and the one short word used on small items.
STARTER = [10, 11, 14, 25, 44, 48, 60, 66, 72, 83, 90, 105]
WORD = {10: "TAGGED", 11: "MEAT", 14: "225", 25: "HEAVY", 44: "PATIENT", 48: "DIRT", 60: "GRIEF",
        66: "JUST MEAT", 72: "SHORT TIME", 83: "GYM LOUD", 90: "DEATH", 105: "FLIES"}

def _shade_layers(k, body):
    """Clip + soft side/top shading for any garment outline (same recipe as hoodie())."""
    defs = (f'<defs><clipPath id="{k}c"><path d="{body}"/></clipPath>'
            f'<linearGradient id="{k}x" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".24"/>'
            '<stop offset=".22" stop-color="#000" stop-opacity=".08"/><stop offset=".38" stop-color="#000" stop-opacity="0"/>'
            '<stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset=".78" stop-color="#000" stop-opacity=".08"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".24"/></linearGradient>'
            f'<linearGradient id="{k}y" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".12"/>'
            '<stop offset=".4" stop-color="#fff" stop-opacity="0"/><stop offset=".82" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient></defs>')
    over = (f'<g clip-path="url(#{k}c)"><rect x="20" y="36" width="560" height="570" fill="url(#{k}x)"/>'
            f'<rect x="20" y="36" width="560" height="570" fill="url(#{k}y)"/>')
    return defs, over

def _fold(d, o=.12, w=4): return f'<path d="{d}" stroke="#000" stroke-opacity="{o}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
def _stitch(d, c, w=1.2): return f'<path d="{d}" stroke="{c}" stroke-width="{w}" stroke-dasharray="3 3" fill="none"/>'
def _lum(h): return sum(int(h[i:i + 2], 16) for i in (1, 3, 5))

# ---------------- tee ----------------
TEE = ("M235 112 Q300 128 365 112 L452 136 L548 228 L503 284 L458 244 L462 590 L138 590 "
       "L142 244 L97 284 L52 228 L148 136 Z")
def tee(view):
    FAB = S.FAB; line, seam = S.shade(FAB, .62), S.shade(FAB, .8)
    k = "tf" if view == "front" else "tb"
    defs, over = _shade_layers(k, TEE)
    g = defs + f'<path d="{TEE}" fill="{FAB}"/>' + over
    g += _fold("M148 140 L142 244", .16, 6) + _fold("M452 140 L458 244", .16, 6)
    g += _fold("M110 196 Q96 214 92 238") + _fold("M490 196 Q504 214 508 238")
    g += _fold("M180 330 Q190 430 176 540", .06, 6) + _fold("M420 330 Q410 430 424 540", .06, 6) + '</g>'
    g += f'<path d="{TEE}" fill="none" stroke="{line}" stroke-width="2" stroke-linejoin="round"/>'
    g += _stitch("M144 574 L456 574", seam) + _stitch("M64 222 L108 276", seam) + _stitch("M536 222 L492 276", seam)
    if view == "front":
        g += f'<path d="M235 112 Q300 172 365 112 Q300 128 235 112 Z" fill="{S.shade(FAB, .5)}"/>'
        g += f'<path d="M235 112 Q300 172 365 112" fill="none" stroke="{S.shade(FAB, .82)}" stroke-width="10" stroke-linecap="round"/>'
        g += f'<path d="M235 112 Q300 172 365 112" fill="none" stroke="{line}" stroke-width="1.5"/>'
    else:
        g += f'<path d="M235 112 Q300 128 365 112" fill="none" stroke="{S.shade(FAB, .82)}" stroke-width="9" stroke-linecap="round"/>'
        g += f'<path d="M235 112 Q300 128 365 112" fill="none" stroke="{line}" stroke-width="1.5"/>'
    return g

# ---------------- boxers (woven cotton, natural-rubber waist in a printed cotton casing) ----------------
BOX = "M148 198 L452 198 L488 470 Q402 484 318 470 L300 352 L282 470 Q198 484 112 470 Z"
def boxers(view, word=""):
    FAB, INK = S.FAB, S.INK; line, seam = S.shade(FAB, .62), S.shade(FAB, .8)
    k = "bf" if view == "front" else "bb"
    defs, over = _shade_layers(k, BOX)
    g = defs + f'<path d="{BOX}" fill="{FAB}"/>' + over
    g += _fold("M200 230 Q214 320 196 440", .07, 6) + _fold("M400 230 Q386 320 404 440", .07, 6)
    g += _fold("M286 400 Q296 430 292 466", .1, 3) + _fold("M314 400 Q304 430 308 466", .1, 3) + '</g>'
    g += f'<path d="{BOX}" fill="none" stroke="{line}" stroke-width="2" stroke-linejoin="round"/>'
    g += _stitch("M118 456 Q198 468 278 456", seam) + _stitch("M322 456 Q402 468 482 456", seam)
    if view == "front":
        g += _stitch("M300 202 L300 300", seam) + f'<path d="M302 204 Q336 250 316 312" fill="none" stroke="{seam}" stroke-width="1.5"/>'
    else:
        g += f'<path d="M300 202 Q306 290 300 352" fill="none" stroke="{seam}" stroke-width="1.5"/>'
    # printed cotton waistband with the word repeated
    g += f'<path d="M146 150 L454 150 L452 200 L148 200 Z" fill="{INK}"/>'
    g += f'<path d="M146 150 L454 150 L452 200 L148 200 Z" fill="none" stroke="{S.shade(INK, .7) if _lum(INK) > 300 else S.shade(INK, 1.6)}" stroke-width="1.5"/>'
    if word:
        fs = S.fitsize(word, "osw", 80, 22)
        for x in (196, 300, 404):
            g += S.tpath(word, "osw", fs, x, 183, fill=FAB)
    return g

# ---------------- sock (factory knit, design knitted in) ----------------
SOCK = ("M232 70 L368 70 L368 372 Q368 418 412 436 L508 470 Q556 488 548 532 Q540 568 492 566 "
        "L262 566 Q214 566 212 518 L222 372 Z")
def sock(view, k="s"):
    FAB = S.FAB; line = S.shade(FAB, .62)
    dark = _lum(FAB) < 300
    knit = S.shade(FAB, 1.35 if dark else .82)
    defs, over = _shade_layers(k, SOCK)
    defs = defs.replace("</defs>", f'<pattern id="{k}k" width="7" height="7" patternUnits="userSpaceOnUse">'
                        f'<path d="M0 7 L3.5 1 L7 7" fill="none" stroke="{knit}" stroke-width="1.1" opacity=".55"/></pattern></defs>')
    g = defs + f'<path d="{SOCK}" fill="{FAB}"/>' + over
    g += f'<path d="M212 500 Q214 566 262 566 L304 566 Q264 520 222 462 Z" fill="#000" fill-opacity=".14"/>'   # heel
    g += f'<path d="M492 566 Q540 568 548 532 Q556 488 508 470 L468 456 Q500 512 478 566 Z" fill="#000" fill-opacity=".14"/>'  # toe
    g += f'<rect x="230" y="66" width="140" height="84" fill="#000" fill-opacity=".08"/>'
    g += "".join(f'<line x1="{x}" y1="70" x2="{x}" y2="148" stroke="#000" stroke-opacity=".16" stroke-width="2"/>' for x in range(240, 368, 9))
    g += f'<rect x="20" y="36" width="560" height="570" fill="url(#{k}k)"/></g>'
    g += f'<path d="{SOCK}" fill="none" stroke="{line}" stroke-width="2" stroke-linejoin="round"/>'
    return g
def sock_art(num, d):
    """Knitted-in: the icon only, flat ink, with the knit texture laid over it."""
    ic = d.get("icon", "none")
    if ic in ("none", "checklist", "obituary", "autopsy_report"): ic = "skull"
    art = S.ICONS[ic](300, 262, .6, **d.get("args", {}))
    knit = S.shade(S.INK, .8 if _lum(S.INK) > 300 else 1.5)
    return (f'<g>{art}</g>'
            f'<defs><pattern id="sk2" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 7 L3.5 1 L7 7" fill="none" stroke="{knit}" stroke-width="1" opacity=".35"/></pattern></defs>'
            f'<rect x="232" y="150" width="136" height="230" fill="url(#sk2)" clip-path="url(#scc)"/>')

# ---------------- beanie (cotton or merino rib knit, embroidered cuff patch) ----------------
CROWN = "M168 396 Q156 176 300 150 Q444 176 432 396 Z"
def beanie(view):
    FAB = S.FAB; line = S.shade(FAB, .62)
    defs, over = _shade_layers("bn" + view[0], CROWN)
    g = defs + f'<path d="{CROWN}" fill="{FAB}"/>' + over
    for x in range(176, 428, 13):
        cx = 300 + (x - 300) * .45
        g += f'<path d="M{x} 396 Q{cx:.0f} 220 300 152" stroke="#000" stroke-opacity=".11" stroke-width="2" fill="none"/>'
    g += '</g>' + f'<path d="{CROWN}" fill="none" stroke="{line}" stroke-width="2"/>'
    g += f'<rect x="146" y="380" width="308" height="122" rx="16" fill="{S.shade(FAB, .93)}" stroke="{line}" stroke-width="2"/>'
    g += "".join(f'<line x1="{x}" y1="384" x2="{x}" y2="498" stroke="#000" stroke-opacity=".13" stroke-width="2"/>' for x in range(156, 450, 9))
    g += f'<rect x="146" y="380" width="308" height="20" rx="10" fill="#000" fill-opacity=".1"/>'
    if view == "back":
        g += f'<rect x="288" y="470" width="24" height="16" rx="2" fill="{S.shade(FAB, .7)}"/>'   # small cotton label tab
    return g
def patch(x, y, w, h, num, d, word, icon_s=.22):
    """An embroidered cotton patch: contrasting ground, stitched edge, icon + one word."""
    INK, FAB = S.INK, S.FAB
    ground = S.shade(FAB, .78) if _lum(FAB) > 360 else S.shade(FAB, 1.32)
    ic = d.get("icon", "none")
    if ic in ("none", "checklist", "obituary", "autopsy_report"): ic = "skull"
    g = (f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="10" fill="{ground}"/>'
         f'<rect x="{x - w / 2 + 5}" y="{y - h / 2 + 5}" width="{w - 10}" height="{h - 10}" rx="7" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    g += S.ICONS[ic](x, y - h * .12, icon_s, **d.get("args", {}))
    if word:
        g += S.tpath(word, "osw", S.fitsize(word, "osw", w - 26, 15), x, y + h / 2 - 12, fill=INK)
    return g

# ---------------- dad cap (unstructured cotton twill, embroidered front) ----------------
CAP = "M138 330 Q132 160 300 142 Q468 160 462 330 Z"
def cap(view):
    FAB = S.FAB; line, seam = S.shade(FAB, .62), S.shade(FAB, .8)
    defs, over = _shade_layers("cp" + view[0], CAP)
    g = defs + f'<path d="{CAP}" fill="{FAB}"/>' + over
    g += _fold("M300 142 Q214 196 186 330", .1, 3) + _fold("M300 142 Q386 196 414 330", .1, 3) + '</g>'
    g += f'<path d="{CAP}" fill="none" stroke="{line}" stroke-width="2"/>'
    g += f'<circle cx="300" cy="146" r="9" fill="{S.shade(FAB, .85)}" stroke="{line}" stroke-width="1.5"/>'
    if view == "front":
        g += f'<path d="M300 152 L300 330" stroke="{seam}" stroke-width="1.5"/>' + _stitch("M292 156 L292 328", seam) + _stitch("M308 156 L308 328", seam)
        for cx in (214, 386):
            g += f'<circle cx="{cx}" cy="212" r="4" fill="{S.shade(FAB, .6)}"/>'
        brim = "M110 322 Q300 296 490 322 Q504 362 470 384 Q300 424 130 384 Q96 362 110 322 Z"
        g += f'<path d="{brim}" fill="{S.shade(FAB, .9)}" stroke="{line}" stroke-width="2"/>'
        g += f'<path d="M118 330 Q300 306 482 330" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="5"/>'
        for off in (14, 26, 38):
            g += _stitch(f"M{130 + off * .4:.0f} {350 + off * .3:.0f} Q300 {384 + off:.0f} {470 - off * .4:.0f} {350 + off * .3:.0f}", seam)
    else:
        g += f'<path d="M232 330 Q300 236 368 330 Z" fill="{S.shade(FAB, .45)}"/>'
        g += f'<path d="M222 318 L378 318 L378 336 L222 336 Z" fill="{S.shade(FAB, .9)}" stroke="{line}" stroke-width="1.5"/>'
        g += '<rect x="318" y="312" width="26" height="30" rx="3" fill="#b08d57" stroke="#7a5f36" stroke-width="2"/>'   # brass buckle
        g += '<rect x="325" y="319" width="12" height="16" rx="2" fill="none" stroke="#7a5f36" stroke-width="2"/>'
        g += _stitch("M300 152 L300 236", seam)
    return g


# ---------------- sweatpants (hoodie fleece, natural-rubber waist in a cotton casing + cotton drawcord, rib cuffs) ----------------
PANTS = "M176 104 L424 104 L442 240 L422 536 L318 536 L304 272 L296 272 L282 536 L178 536 L158 240 Z"
def sweatpants(view):
    FAB = S.FAB; line, seam = S.shade(FAB, .62), S.shade(FAB, .8)
    k = "pf" if view == "front" else "pb"
    defs, over = _shade_layers(k, PANTS)
    g = defs + f'<path d="{PANTS}" fill="{FAB}"/>' + over
    g += _fold("M300 104 L300 272", .1, 3)
    g += _fold("M196 300 Q210 400 198 520", .07, 6) + _fold("M404 300 Q390 400 402 520", .07, 6)
    for y in (470, 496, 520):   # fabric stacking above the cuffs
        g += _fold(f"M186 {y} Q230 {y + 12} 276 {y - 2}", .1, 3) + _fold(f"M324 {y - 2} Q370 {y + 12} 414 {y}", .1, 3)
    g += '</g>' + f'<path d="{PANTS}" fill="none" stroke="{line}" stroke-width="2" stroke-linejoin="round"/>'
    rib = S.shade(FAB, .9)
    for x0, x1 in ((184, 278), (322, 416)):   # rib cuffs
        g += f'<rect x="{x0}" y="530" width="{x1 - x0}" height="52" rx="6" fill="{rib}" stroke="{line}" stroke-width="2"/>'
        g += "".join(f'<line x1="{x}" y1="534" x2="{x}" y2="578" stroke="#000" stroke-opacity=".14" stroke-width="2"/>' for x in range(x0 + 7, x1 - 3, 8))
    g += f'<rect x="172" y="62" width="256" height="46" rx="8" fill="{rib}" stroke="{line}" stroke-width="2"/>'   # waistband casing
    g += _stitch("M178 100 L422 100", seam) + _stitch("M178 70 L422 70", seam)
    if view == "front":
        g += f'<path d="M186 112 Q196 160 166 214" fill="none" stroke="#000" stroke-opacity=".28" stroke-width="3"/>'
        g += f'<path d="M414 112 Q404 160 434 214" fill="none" stroke="#000" stroke-opacity=".28" stroke-width="3"/>'
        cord = S.shade(FAB, 1.4) if _lum(FAB) < 300 else S.shade(FAB, .55)
        g += f'<circle cx="286" cy="90" r="4" fill="{line}"/><circle cx="314" cy="90" r="4" fill="{line}"/>'
        g += f'<path d="M286 92 Q280 130 288 168" fill="none" stroke="{cord}" stroke-width="5" stroke-linecap="round"/>'
        g += f'<path d="M314 92 Q322 128 310 162" fill="none" stroke="{cord}" stroke-width="5" stroke-linecap="round"/>'
        g += f'<circle cx="288" cy="172" r="6" fill="{cord}"/><circle cx="310" cy="166" r="6" fill="{cord}"/>'   # knotted ends
    else:
        g += f'<path d="M332 140 L404 140 L400 214 L336 214 Z" fill="#000" fill-opacity=".05" stroke="{seam}" stroke-width="1.5"/>'
        g += _stitch("M336 146 L400 146", seam)
    return g
def pants_art(num, d, word):
    """Left-thigh print (viewer's right): the icon, then the word running down the leg."""
    ic = d.get("icon", "none")
    if ic in ("none", "checklist", "obituary", "autopsy_report"): ic = "skull"
    g = S.ICONS[ic](366, 196, .3, **d.get("args", {}))
    if word:
        fs = S.fitsize(word, "osw", 200, 30)
        g += f'<g transform="rotate(90 366 360)">' + S.tpath(word, "osw", fs, 366, 360 + fs * .35, fill=S.INK) + '</g>'
    return g

# ---------------- heavy jacket (12 oz cotton duck, corduroy collar, brass snaps, quilted flannel + wool lining) ----------------
JACKET = ("M150 170 L95 200 L40 470 L95 485 L130 330 L135 590 L465 590 L470 330 L505 485 L560 470 L505 200 L450 170 "
          "Q420 150 390 142 Q300 160 210 142 Q180 150 150 170 Z")
def jacket(view):
    FAB = S.FAB; line, seam = S.shade(FAB, .62), S.shade(FAB, .8)
    k = "jf" if view == "front" else "jb"
    defs, over = _shade_layers(k, JACKET)
    dark = _lum(FAB) < 300
    weave = S.shade(FAB, 1.25 if dark else .84)
    defs = defs.replace("</defs>", f'<pattern id="{k}w" width="6" height="6" patternUnits="userSpaceOnUse">'
                        f'<path d="M0 6 L6 0" stroke="{weave}" stroke-width="1" opacity=".35"/></pattern></defs>')
    g = defs + f'<path d="{JACKET}" fill="{FAB}"/>' + over + f'<rect x="20" y="36" width="560" height="570" fill="url(#{k}w)"/>'
    g += _fold("M150 172 L131 332", .18, 7) + _fold("M450 172 L469 332", .18, 7)
    g += _fold("M118 268 Q104 286 98 312") + _fold("M104 352 Q90 366 84 392") + _fold("M482 268 Q496 286 502 312") + _fold("M496 352 Q510 366 516 392")
    g += _fold("M175 360 Q185 440 170 530", .07, 6) + _fold("M425 360 Q415 440 430 530", .07, 6) + '</g>'
    g += f'<path d="{JACKET}" fill="none" stroke="{line}" stroke-width="2" stroke-linejoin="round"/>'
    g += _stitch("M150 176 L132 330", seam) + _stitch("M450 176 L468 330", seam)
    g += f'<path d="M135 564 L465 564" stroke="{line}" stroke-width="1.5"/>' + _stitch("M137 580 L463 580", seam) + _stitch("M137 570 L463 570", seam)
    cuff = S.shade(FAB, .82)
    g += f'<rect x="38" y="458" width="60" height="30" rx="3" fill="{cuff}" stroke="{line}" stroke-width="1.5" transform="rotate(5 68 473)"/>'
    g += f'<rect x="502" y="458" width="60" height="30" rx="3" fill="{cuff}" stroke="{line}" stroke-width="1.5" transform="rotate(-5 532 473)"/>'
    cord = "#5b3f2c" if _lum(FAB) > 200 else "#4a3426"    # brown cotton corduroy collar, like classic duck work jackets
    brass, brass_d = "#b08d57", "#7a5f36"
    if view == "front":
        g += f'<path d="M300 196 L300 590" stroke="{line}" stroke-width="2"/>' + _stitch("M292 200 L292 588", seam)
        for y in (250, 318, 386, 454, 522):
            g += f'<circle cx="300" cy="{y}" r="7" fill="{brass}" stroke="{brass_d}" stroke-width="2"/>'
        for x0 in (178, 332):    # chest pockets with flaps
            g += f'<rect x="{x0}" y="262" width="90" height="82" rx="3" fill="#000" fill-opacity=".05" stroke="{seam}" stroke-width="1.5"/>'
            g += f'<path d="M{x0 - 2} 256 L{x0 + 92} 256 L{x0 + 92} 284 L{x0 + 45} 292 L{x0 - 2} 284 Z" fill="{S.shade(FAB, .93)}" stroke="{line}" stroke-width="1.5"/>'
            g += f'<circle cx="{x0 + 45}" cy="282" r="4.5" fill="{brass}" stroke="{brass_d}" stroke-width="1.5"/>'
        for x0 in (164, 326):    # lower patch pockets
            g += f'<path d="M{x0} 420 L{x0 + 110} 420 L{x0 + 110} 530 L{x0} 530 Z" fill="#000" fill-opacity=".05" stroke="{seam}" stroke-width="1.5"/>'
            g += _stitch(f"M{x0 + 4} 426 L{x0 + 106} 426", seam)
        g += f'<path d="M300 158 L212 140 L194 170 L254 240 L300 200 Z" fill="{cord}" stroke="{line}" stroke-width="1.5"/>'
        g += f'<path d="M300 158 L388 140 L406 170 L346 240 L300 200 Z" fill="{cord}" stroke="{line}" stroke-width="1.5"/>'
        g += "".join(f'<path d="M{212 + i * 9} {144 + i * 2} L{232 + i * 8} {196 + i * 3}" stroke="#000" stroke-opacity=".12" stroke-width="2"/>' for i in range(8))
        g += "".join(f'<path d="M{388 - i * 9} {144 + i * 2} L{368 - i * 8} {196 + i * 3}" stroke="#000" stroke-opacity=".12" stroke-width="2"/>' for i in range(8))
    else:
        g += f'<path d="M150 226 Q300 236 450 226" stroke="{seam}" stroke-width="1.5" fill="none"/>' + _stitch("M150 232 Q300 242 450 232", seam)
        g += f'<path d="M210 142 Q300 160 390 142 L394 166 Q300 184 206 166 Z" fill="{cord}" stroke="{line}" stroke-width="1.5"/>'
        g += f'<rect x="290" y="176" width="20" height="12" rx="2" fill="{S.shade(FAB, .7)}"/>'   # hang loop
    return g

# ---------------- items table ----------------
# fit: transform that fills the 560x570 frame like the hoodie does; crop: close-up window (after the transform)
ITEMS = {
    "tee":       {"fit": ""},
    "underwear": {"fit": "translate(300 322) scale(1.3) translate(-300 -317)", "crop": "100 80 400 390"},
    "socks":     {"fit": "translate(-44 0)", "crop": "170 60 200 340"},
    "hats-beanie": {"fit": "translate(300 326) scale(1.2) translate(-300 -326)", "crop": "150 370 300 180"},
    "hats-cap":  {"fit": "translate(300 328) scale(1.16) translate(-300 -280)", "crop": "160 180 280 200"},
    "sweatpants": {"fit": "", "crop": "226 150 280 340"},
    "jackets":   {"fit": "", "crop": "140 180 320 360"},
}
def _fit(kind, body):
    tf = ITEMS[kind]["fit"]
    return f'<g transform="{tf}">{body}</g>' if tf else body
CROP_TEE = {"front": "135 120 330 380", "back": "125 80 350 470", "hood": "125 80 350 470", "chest": "292 150 180 200",
            "sleeve": "30 140 540 360", "pocket": "165 160 270 350"}

def _svg(title, body, vb=VB, defs=""):
    w, h = vb.split()[2:]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}"><title>{E(title)}</title>{defs}{body}</svg>'

def fabric(cname, duck=False):
    FAB = S.FAB
    knit = S.shade(FAB, .86) if _lum(FAB) > 300 else S.shade(FAB, 1.18)
    if duck:   # canvas weave instead of knit
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 570" width="560" height="570"><title>{E(cname)} cotton duck</title>'
                f'<defs><pattern id="k" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 1.5 H6 M1.5 0 V6" stroke="{knit}" stroke-width="1.4" opacity=".5"/></pattern>'
                f'<radialGradient id="v" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/>'
                f'<stop offset="1" stop-color="#000" stop-opacity=".22"/></radialGradient></defs>'
                f'<rect width="560" height="570" fill="{FAB}"/><rect width="560" height="570" fill="url(#k)"/><rect width="560" height="570" fill="url(#v)"/></svg>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 570" width="560" height="570"><title>{E(cname)} fabric</title>'
            f'<defs><pattern id="k" width="8" height="8" patternUnits="userSpaceOnUse">'
            f'<path d="M0 8 L4 0 L8 8" fill="none" stroke="{knit}" stroke-width="1.2" opacity=".55"/></pattern>'
            f'<radialGradient id="v" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity=".22"/></radialGradient></defs>'
            f'<rect width="560" height="570" fill="{FAB}"/><rect width="560" height="570" fill="url(#k)"/><rect width="560" height="570" fill="url(#v)"/></svg>')

def render_item(kind, num, d, out):
    """Write the 4 pictures for one item + design. Returns (main, [other, close-up, fabric], main_side_label, other_label)."""
    cname, S.FAB, S.INK = S.color_for(num)
    base = f"{kind}-{num:02d}-{d['slug']}"
    word = WORD.get(num, "")
    files = {}
    if kind == "tee":
        view, art = S.layout(num, d)
        other = "front" if view == "back" else "back"
        main = tee(view) + f'<g filter="url(#grunge)">{art}</g>'
        files[""] = _svg(" ".join(d["lines"]).capitalize(), main, defs=S.DEFS)
        files["-b"] = _svg(f"{cname}, {other} (plain)", tee(other))
        vb = CROP_TEE.get(d["place"], "125 80 350 470")
        files["-c"] = _svg("Print close-up", main, vb=vb, defs=S.DEFS)
        labels = ("Back" if view == "back" else "Front", "Front" if view == "back" else "Back")
    elif kind == "underwear":
        ic = d.get("icon", "none")
        if ic in ("none", "checklist", "obituary", "autopsy_report"): ic = "skull"
        main = _fit(kind, boxers("front", word) + S.ICONS[ic](212, 392, .42, **d.get("args", {})))
        files[""] = _svg(f"Boxers: {word}", main)
        files["-b"] = _svg(f"{cname} boxers, back", _fit(kind, boxers("back", word)))
        files["-c"] = _svg("Print close-up", main, vb=ITEMS[kind]["crop"])
        labels = ("Front", "Back")
    elif kind == "socks":
        main = _fit(kind, sock("front", "sc") + sock_art(num, d))
        files[""] = _svg("Crew sock", main)
        pair = (f'<g transform="translate(-64 -6) rotate(-6 300 320)" opacity=".92">{sock("back", "sp")}</g>'
                f'<g transform="translate(16 8)">{sock("front", "sc")}{sock_art(num, d)}</g>')
        pair = f'<g transform="translate(-30 0)">{pair}</g>'
        files["-b"] = _svg(f"{cname} socks, pair", pair)
        files["-c"] = _svg("Knit close-up", main, vb=ITEMS[kind]["crop"])
        labels = ("Side", "Pair")
    elif kind == "hats-beanie":
        main = _fit(kind, beanie("front") + patch(300, 440, 176, 96, num, d, word))
        files[""] = _svg("Beanie", main)
        files["-b"] = _svg(f"{cname} beanie, back", _fit(kind, beanie("back")))
        files["-c"] = _svg("Patch close-up", main, vb=ITEMS[kind]["crop"])
        labels = ("Front", "Back")
    elif kind == "hats-cap":
        ic = d.get("icon", "none")
        if ic in ("none", "checklist", "obituary", "autopsy_report"): ic = "skull"
        emb = S.ICONS[ic](300, 232, .34, **d.get("args", {}))
        if word:
            emb += S.tpath(word, "osw", S.fitsize(word, "osw", 150, 24), 300, 304, fill=S.INK)
        main = _fit(kind, cap("front") + emb)
        files[""] = _svg("Dad cap", main)
        files["-b"] = _svg(f"{cname} cap, back", _fit(kind, cap("back")))
        files["-c"] = _svg("Embroidery close-up", main, vb=ITEMS[kind]["crop"])
        labels = ("Front", "Back")
    elif kind == "sweatpants":
        main = sweatpants("front") + f'<g filter="url(#grunge)">{pants_art(num, d, word)}</g>'
        files[""] = _svg(f"Sweatpants: {word}", main, defs=S.DEFS)
        files["-b"] = _svg(f"{cname} sweatpants, back", sweatpants("back"))
        files["-c"] = _svg("Print close-up", main, vb=ITEMS[kind]["crop"], defs=S.DEFS)
        labels = ("Front", "Back")
    elif kind == "jackets":
        d2 = dict(d, place="back" if d["place"] in ("back", "hood") else "front")
        _, art = S.layout(num, d2)
        main = jacket("back") + f'<g filter="url(#grunge)" transform="translate(300 334) scale(.9) translate(-300 -300)">{art}</g>'
        files[""] = _svg(" ".join(d["lines"]).capitalize() + " (jacket back)", main, defs=S.DEFS)
        files["-b"] = _svg(f"{cname} jacket, front", jacket("front"))
        files["-c"] = _svg("Back print close-up", main, vb=ITEMS[kind]["crop"], defs=S.DEFS)
        labels = ("Back", "Front")
    files["-d"] = fabric(cname, duck=(kind == "jackets"))
    names = {}
    for suf, svg in files.items():
        n = base + suf + ".svg"
        open(os.path.join(out, n), "w").write(svg)
        names[suf] = n
    return names[""], [names["-b"], names["-c"], names["-d"]], labels, cname

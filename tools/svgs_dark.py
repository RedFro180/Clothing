"""Hoodie sketches 01-107 with dark content on a range of natural-dye hoodie colors.
Run: python3 tools/svgs_dark.py [numbers...]
Gothic type is converted to outlines (fonts in tools/fonts, SIL Open Font License), so the SVGs
look the same everywhere. Design data: tools/designs_data.py (FIRST = 01-07, DESIGNS = 08-107)."""
import os, math, html, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "designs", "sketches"))
FD = os.path.join(HERE, "fonts")
E = html.escape
PAGE = "#f3f1ec"
RED = "#9b1b1b"

# Hoodie colors (all reachable with natural dyes or undyed fiber) and the ink that contrasts.
# Light ink on dark fabric = resist print before dyeing, discharge on reactive-dyed fabric, or embroidery.
# Dark ink on light fabric = natural-dye mordant/extract paste print.
PALETTE = [
    ("Black (logwood + iron)", "#151515", "#ece4d0"),
    ("Undyed oatmeal", "#e4d9c2", "#171412"),
    ("Oxblood (madder + iron)", "#5e1a1c", "#efe3cf"),
    ("Plum (logwood)", "#3c2742", "#ece4d0"),
    ("Heather grey", "#b8b5ae", "#161616"),
    ("Indigo", "#1e2a46", "#ece4d0"),
    ("Olive (weld + iron)", "#4a4a2a", "#ece4d0"),
    ("Dusty rose (light madder)", "#cfa39b", "#2a0d0d"),
    ("Charcoal", "#2d2d2d", "#ece4d0"),
    ("Sand (undyed hemp)", "#cdbf9e", "#1a1510"),
]
INK, FAB = PALETTE[0][2], PALETTE[0][1]   # set per design in render()

def shade(hexc, f):
    c = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    c = [max(0, min(255, int(v * f) if f < 1 else int(v + (255 - v) * (f - 1)))) for v in c]
    return "#%02x%02x%02x" % tuple(c)

# ---------------- fonts -> outlined text ----------------
FILES = {"black": "unifrakturcook-latin-700-normal.woff2", "pirata": "pirata-one-latin-400-normal.woff2",
         "type": "special-elite-latin-400-normal.woff2", "osw": "oswald-latin-700-normal.woff2"}
_F = {}
def _font(n):
    if n not in _F:
        f = TTFont(os.path.join(FD, FILES[n]))
        _F[n] = (f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm, f["hmtx"])
    return _F[n]
def _g(cmap, ch):
    ch = {"’": "'", "‘": "'", "“": '"', "”": '"', "—": "-", "…": "."}.get(ch, ch)
    return cmap.get(ord(ch)) or cmap.get(ord("?"))
def measure(text, n, size):
    gs, cmap, upm, hm = _font(n)
    return sum(hm[_g(cmap, c)][0] * size / upm for c in text)
def _ntos(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s
def tpath(text, n, size, x, y, anchor="middle", fill=None):
    fill = fill or INK
    gs, cmap, upm, hm = _font(n); s = size / upm
    w = measure(text, n, size)
    cx = x - (w / 2 if anchor == "middle" else (w if anchor == "end" else 0))
    pen = SVGPathPen(gs, ntos=_ntos)
    for c in text:
        g = _g(cmap, c)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += hm[g][0] * s
    d = pen.getCommands()
    return f'<path d="{d}" fill="{fill}"/>' if d else ""
def fitsize(text, n, width, maxsize):
    return min(maxsize, width / max(measure(text, n, 1), 0.001))
def arctext(text, n, size, cx, cy, r):
    gs, cmap, upm, hm = _font(n); s = size / upm
    pos = -measure(text, n, size) / 2
    pen = SVGPathPen(gs, ntos=_ntos)
    for c in text:
        g = _g(cmap, c); a = hm[g][0] * s
        th = (pos + a / 2) / r; co, si = math.cos(th), math.sin(th)
        px, py = cx + r * si, cy - r * co
        gs[g].draw(TransformPen(pen, (s * co, s * si, s * si, -s * co, px - co * a / 2, py - si * a / 2)))
        pos += a
    return f'<path d="{pen.getCommands()}" fill="{INK}"/>'

# ---------------- hoodie ----------------
def hoodie(view):
    dark = shade(FAB, 0.72); line = shade(FAB, 0.55); cord = shade(FAB, 1.35) if sum(int(FAB[i:i+2], 16) for i in (1, 3, 5)) < 300 else shade(FAB, 0.6)
    g = ('<path d="M150 170 L95 200 L40 470 L95 485 L130 330 L135 590 L465 590 L470 330 L505 485 L560 470 L505 200 L450 170 '
         f'Q420 150 390 145 Q300 60 210 145 Q180 150 150 170 Z" fill="{FAB}" stroke="{line}" stroke-width="3"/>'
         f'<path d="M150 170 L130 330 M450 170 L470 330 M135 560 L465 560" stroke="{line}" stroke-width="2" fill="none"/>'
         f'<g stroke="{shade(FAB,0.8)}" stroke-width="2">' + ''.join(f'<line x1="{140+i*11}" y1="563" x2="{140+i*11}" y2="588"/>' for i in range(30)) + '</g>'
         f'<rect x="38" y="465" width="60" height="22" fill="{dark}" stroke="{line}" stroke-width="2" transform="rotate(5 68 476)"/>'
         f'<rect x="502" y="465" width="60" height="22" fill="{dark}" stroke="{line}" stroke-width="2" transform="rotate(-5 532 476)"/>')
    if view == "front":
        g += (f'<path d="M210 145 Q300 215 390 145 Q300 120 210 145 Z" fill="{shade(FAB,0.5)}"/>'
              f'<path d="M210 145 Q300 215 390 145" fill="none" stroke="{line}" stroke-width="3"/>'
              f'<path d="M200 430 L400 430 L420 520 L180 520 Z" fill="none" stroke="{line}" stroke-width="2" stroke-dasharray="6 4"/>'
              f'<path d="M282 188 Q278 220 276 252 M318 188 Q322 220 324 252" stroke="{cord}" stroke-width="3" fill="none"/>'
              f'<rect x="272" y="250" width="7" height="13" fill="{cord}"/><rect x="321" y="250" width="7" height="13" fill="{cord}"/>')
    else:
        g += (f'<path d="M215 145 Q300 40 385 145 Q300 178 215 145 Z" fill="{dark}" stroke="{line}" stroke-width="3"/>'
              f'<path d="M300 96 L300 160" stroke="{line}" stroke-width="2"/>')
    return g

DEFS = '''<defs><filter id="grunge" x="-5%" y="-5%" width="110%" height="110%">
<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.75" result="m"/>
<feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="3" result="w"/>
<feDisplacementMap in="SourceGraphic" in2="w" scale="2.5" result="d"/>
<feComposite in="d" in2="m" operator="in"/></filter></defs>'''

# ---------------- art library: ink shapes; "cut-outs" use the fabric color ----------------
def F(x, y, s):
    return lambda u, v: f"{x+u*s:.1f} {y+v*s:.1f}"
def C(x, y, s):
    return lambda u, v: f"{x+u*s:.1f},{y+v*s:.1f}"
def bone(x1, y1, x2, y2, w, c=None):
    c = c or INK
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * w * 0.42, dx / L * w * 0.42; r = w * 0.62
    g = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
    for px, py in ((x1, y1), (x2, y2)):
        g += f'<circle cx="{px+nx:.1f}" cy="{py+ny:.1f}" r="{r:.1f}" fill="{c}"/><circle cx="{px-nx:.1f}" cy="{py-ny:.1f}" r="{r:.1f}" fill="{c}"/>'
    return g
def skull(x, y, s=1, fg=None, bg=None, cracked=True):
    fg = fg or INK; bg = bg or FAB; f = F(x, y, s); c = C(x, y, s)
    g = (f'<path d="M{f(-50,-2)} C{f(-56,-72)} {f(56,-72)} {f(50,-2)} C{f(50,14)} {f(42,20)} {f(36,28)} L{f(35,47)} '
         f'C{f(20,58)} {f(-20,58)} {f(-35,47)} L{f(-36,28)} C{f(-42,20)} {f(-50,14)} {f(-50,-2)} Z" fill="{fg}"/>')
    for d in (-1, 1):
        g += f'<path d="M{f(d*6,-6)} C{f(d*8,-20)} {f(d*34,-22)} {f(d*36,-4)} C{f(d*37,12)} {f(d*14,16)} {f(d*8,8)} Z" fill="{bg}"/>'
        g += f'<path d="M{f(d*44,10)} Q{f(d*34,18)} {f(d*30,30)}" stroke="{bg}" stroke-width="{2.2*s:.1f}" fill="none"/>'
    g += f'<path d="M{f(0,14)} L{f(-8,28)} Q{f(0,25)} {f(8,28)} Z" fill="{bg}"/>'
    g += f'<path d="M{f(-28,38)} L{f(28,38)}" stroke="{bg}" stroke-width="{2.5*s:.1f}"/>'
    g += ''.join(f'<line x1="{x+u*s:.1f}" y1="{y+33*s:.1f}" x2="{x+u*s:.1f}" y2="{y+48*s:.1f}" stroke="{bg}" stroke-width="{2.4*s:.1f}"/>' for u in range(-21, 22, 7))
    if cracked:
        g += f'<polyline points="{c(4,-62)} {c(-2,-48)} {c(6,-40)} {c(-4,-26)}" fill="none" stroke="{bg}" stroke-width="{2.4*s:.1f}"/>'
    return g
POSES = {
 "stand": dict(hl=(-30, 94), hr=(30, 94), el=(-28, 62), er=(28, 62), kl=(-14, 140), kr=(14, 140), fl=(-16, 180), fr=(16, 180)),
 "hang":  dict(hl=(-26, -44), hr=(26, -44), el=(-26, -8), er=(26, -8), kl=(-12, 140), kr=(12, 140), fl=(-10, 180), fr=(10, 180)),
 "flex":  dict(hl=(-40, 0), hr=(40, 0), el=(-48, 30), er=(48, 30), kl=(-16, 140), kr=(16, 140), fl=(-22, 180), fr=(22, 180)),
 "press": dict(hl=(-36, -40), hr=(36, -40), el=(-42, -4), er=(42, -4), kl=(-16, 140), kr=(16, 140), fl=(-22, 180), fr=(22, 180)),
 "carry": dict(hl=(-36, 96), hr=(36, 96), el=(-32, 62), er=(32, 62), kl=(-14, 140), kr=(14, 140), fl=(-16, 180), fr=(16, 180)),
 "jump":  dict(hl=(-46, -22), hr=(46, -22), el=(-32, 8), er=(32, 8), kl=(-22, 126), kr=(22, 120), fl=(-34, 158), fr=(30, 160)),
 "sit":   dict(hl=(-30, 94), hr=(30, 94), el=(-28, 62), er=(28, 62), kl=(-30, 112), kr=(30, 112), fl=(-32, 150), fr=(32, 150)),
}
def skeleton(x, y, s=1, pose="stand"):
    J = POSES.get(pose, POSES["stand"]); p = lambda t: (x + t[0] * s, y + t[1] * s); w = 5.5 * s
    g = skull(x, y, 0.27 * s, cracked=False)
    g += ''.join(f'<circle cx="{x:.1f}" cy="{y+(20+i*7)*s:.1f}" r="{3.1*s:.1f}" fill="{INK}"/>' for i in range(11))
    for i in range(4):
        yy = 34 + i * 11
        for d in (-1, 1):
            g += f'<path d="M{x+d*3*s:.1f} {y+yy*s:.1f} C{x+d*24*s:.1f} {y+(yy-3)*s:.1f} {x+d*28*s:.1f} {y+(yy+8)*s:.1f} {x+d*16*s:.1f} {y+(yy+11)*s:.1f}" stroke="{INK}" stroke-width="{3.4*s:.1f}" fill="none" stroke-linecap="round"/>'
    f = F(x, y, s)
    g += f'<path d="M{f(-18,92)} Q{f(-24,106)} {f(-10,108)} Q{f(0,101)} {f(10,108)} Q{f(24,106)} {f(18,92)} Q{f(0,86)} {f(-18,92)} Z" fill="{INK}"/>'
    sl, sr, hl, hr = p((-22, 28)), p((22, 28)), p((-12, 98)), p((12, 98))
    g += bone(*sl, *sr, 3 * s)
    for sh, el, ha in ((sl, p(J["el"]), p(J["hl"])), (sr, p(J["er"]), p(J["hr"]))):
        g += bone(*sh, *el, w) + bone(*el, *ha, w * 0.9) + f'<circle cx="{ha[0]:.1f}" cy="{ha[1]:.1f}" r="{4.5*s:.1f}" fill="{INK}"/>'
    for hp, kn, ft in ((hl, p(J["kl"]), p(J["fl"])), (hr, p(J["kr"]), p(J["fr"]))):
        g += bone(*hp, *kn, w * 1.1) + bone(*kn, *ft, w) + f'<ellipse cx="{ft[0]+(-5 if ft[0]<x else 5)*s:.1f}" cy="{ft[1]+3*s:.1f}" rx="{9*s:.1f}" ry="{4*s:.1f}" fill="{INK}"/>'
    return g
def figure(x, y, s=1, pose="stand"):
    s *= 0.78; hy = y - 75 * s; g = ''
    if pose == "hang":
        hy = y - 20 * s
        g += f'<line x1="{x-70*s:.1f}" y1="{hy-46*s:.1f}" x2="{x+70*s:.1f}" y2="{hy-46*s:.1f}" stroke="{INK}" stroke-width="{9*s:.1f}" stroke-linecap="round"/>'
    if pose == "jump":
        g += f'<rect x="{x+20*s:.1f}" y="{y+40*s:.1f}" width="{90*s:.1f}" height="{70*s:.1f}" fill="{INK}"/>' + tpath('24"', "osw", 26 * s, x + 65 * s, y + 85 * s, fill=FAB)
        g += f'<line x1="{x-110*s:.1f}" y1="{y+110*s:.1f}" x2="{x+130*s:.1f}" y2="{y+110*s:.1f}" stroke="{INK}" stroke-width="{5*s:.1f}"/>'
        x -= 30 * s
    g += skeleton(x, hy, s, pose)
    if pose == "press": g += barbell(x, hy - 44 * s, 0.55 * s)
    if pose == "carry": g += coffin(x - 38 * s, hy + 128 * s, 0.38 * s, "PAST") + coffin(x + 38 * s, hy + 128 * s, 0.38 * s, "NEXT")
    return g
def figures2(x, y, s=1):
    s *= 0.6; hy = y - 80 * s
    return skeleton(x - 42 * s, hy, s) + skeleton(x + 42 * s, hy, s) + bone(x - 20 * s, hy + 30 * s, x + 20 * s, hy + 30 * s, 4.5 * s)
def barbell(x, y, s=1):
    w = 120 * s
    g = f'<line x1="{x-w:.1f}" y1="{y:.1f}" x2="{x+w:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="{8*s:.1f}" stroke-linecap="round"/>'
    for d in (-1, 1):
        for off, h, wd in ((26, 80, 18), (6, 58, 14)):
            xx = x + d * (w - off * s) - (0 if d > 0 else wd * s)
            g += f'<rect x="{xx:.1f}" y="{y-h/2*s:.1f}" width="{wd*s:.1f}" height="{h*s:.1f}" rx="{3*s:.1f}" fill="{INK}"/>'
            g += f'<line x1="{xx+wd*s/2:.1f}" y1="{y-h/2*s+6*s:.1f}" x2="{xx+wd*s/2:.1f}" y2="{y+h/2*s-6*s:.1f}" stroke="{FAB}" stroke-width="{2*s:.1f}"/>'
    return g
def dumbbell(x, y, s=1):
    g = bone(x - 40 * s, y, x + 40 * s, y, 11 * s)
    for d in (-1, 1):
        cx = x + d * 58 * s
        g += '<polygon points="' + " ".join(f"{cx+22*s*math.cos(math.radians(a)):.1f},{y+30*s*math.sin(math.radians(a)):.1f}" for a in range(0, 360, 60)) + f'" fill="{INK}"/>'
        g += f'<line x1="{cx:.1f}" y1="{y-20*s:.1f}" x2="{cx:.1f}" y2="{y+20*s:.1f}" stroke="{FAB}" stroke-width="{2.5*s:.1f}"/>'
    return g
def kettlebell(x, y, s=1):
    f = F(x, y, s)
    g = (f'<path d="M{f(-28,-28)} Q{f(-30,-78)} {f(0,-78)} Q{f(30,-78)} {f(28,-28)}" fill="none" stroke="{INK}" stroke-width="{12*s:.1f}"/>'
         f'<circle cx="{x:.1f}" cy="{y+8*s:.1f}" r="{48*s:.1f}" fill="{INK}"/><rect x="{x-32*s:.1f}" y="{y+46*s:.1f}" width="{64*s:.1f}" height="{9*s:.1f}" fill="{INK}"/>')
    for d in (-1, 1):
        g += f'<ellipse cx="{x+d*16*s:.1f}" cy="{y+2*s:.1f}" rx="{11*s:.1f}" ry="{13*s:.1f}" fill="{FAB}"/>'
    g += f'<path d="M{f(0,14)} L{f(-6,25)} L{f(6,25)} Z" fill="{FAB}"/>'
    g += ''.join(f'<line x1="{x+u*s:.1f}" y1="{y+33*s:.1f}" x2="{x+u*s:.1f}" y2="{y+44*s:.1f}" stroke="{FAB}" stroke-width="{2.6*s:.1f}"/>' for u in (-16, -8, 0, 8, 16))
    return g
def plate(x, y, s=1, label="45"):
    g = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{64*s:.1f}" fill="{INK}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{46*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{3*s:.1f}"/>'
         f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{11*s:.1f}" fill="{FAB}"/>')
    g += tpath(label, "osw", 22 * s, x, y - 20 * s, fill=FAB) + ("" if "LB" in label else tpath("LB", "osw", 14 * s, x, y + 36 * s, fill=FAB))
    g += f'<polyline points="{x+40*s:.1f},{y-40*s:.1f} {x+28*s:.1f},{y-24*s:.1f} {x+36*s:.1f},{y-12*s:.1f} {x+22*s:.1f},{y+2*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{2.5*s:.1f}"/>'
    return g
def coffin(x, y, s=1, label=""):
    pts = lambda k: " ".join(f"{x+u*s*k:.1f},{y+v*s*k:.1f}" for u, v in ((-26, -78), (26, -78), (44, -36), (26, 78), (-26, 78), (-44, -36)))
    g = f'<polygon points="{pts(1)}" fill="{INK}"/><polygon points="{pts(0.86)}" fill="none" stroke="{FAB}" stroke-width="{2.5*s:.1f}"/>'
    for u, v in ((-30, -36), (30, -36), (-18, 62), (18, 62), (-18, -62), (18, -62)):
        g += f'<circle cx="{x+u*s:.1f}" cy="{y+v*s:.1f}" r="{2.6*s:.1f}" fill="{FAB}"/>'
    if label:
        g += tpath(label, "osw", fitsize(label, "osw", 52 * s, 28 * s), x, y + 10 * s, fill=FAB)
    else:
        g += skull(x, y - 6 * s, 0.36 * s, fg=FAB, bg=INK, cracked=False)
    return g
def hand_skel(x, y, s=1):
    g = bone(x - 6 * s, y + 46 * s, x - 6 * s, y, 5 * s) + bone(x + 6 * s, y + 46 * s, x + 6 * s, y, 5 * s)
    g += ''.join(f'<circle cx="{x+u*s:.1f}" cy="{y-6*s:.1f}" r="{4.5*s:.1f}" fill="{INK}"/>' for u in (-9, -3, 3, 9))
    for i, ang in enumerate((-58, -24, -6, 12, 32)):
        a = math.radians(ang - 90); L = (34, 44, 48, 44, 34)[i] * s
        bx, by = x + (i - 2) * 6 * s, y - 12 * s
        mx, my = bx + math.cos(a) * L * 0.55, by + math.sin(a) * L * 0.55
        ex, ey = bx + math.cos(a + 0.18) * L, by + math.sin(a + 0.18) * L
        g += bone(bx, by, mx, my, 3.6 * s) + bone(mx, my, ex, ey, 3.2 * s)
    return g
def tombstone(x, y, s=1, label="RIP", hand=True):
    f = F(x, y, s)
    g = (f'<path d="M{f(-52,62)} L{f(-52,-18)} Q{f(-52,-74)} {f(0,-74)} Q{f(52,-74)} {f(52,-18)} L{f(52,62)} Z" fill="{INK}"/>'
         f'<polyline points="{x+22*s:.1f},{y-70*s:.1f} {x+12*s:.1f},{y-52*s:.1f} {x+24*s:.1f},{y-38*s:.1f} {x+10*s:.1f},{y-20*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{2.6*s:.1f}"/>'
         f'<line x1="{x-100*s:.1f}" y1="{y+62*s:.1f}" x2="{x+100*s:.1f}" y2="{y+62*s:.1f}" stroke="{INK}" stroke-width="{5*s:.1f}" stroke-linecap="round"/>')
    g += tpath(label, "osw", fitsize(label, "osw", 80 * s, 26 * s), x, y + 8 * s, fill=FAB)
    for u in (-84, -66, -42):
        g += f'<path d="M{x+u*s:.1f} {y+60*s:.1f} l{-4*s:.1f} {-14*s:.1f} l{6*s:.1f} {10*s:.1f} l{3*s:.1f} {-16*s:.1f} l{3*s:.1f} {16*s:.1f} l{5*s:.1f} {-10*s:.1f} l{-3*s:.1f} {14*s:.1f}" fill="{INK}"/>'
    if hand: g += hand_skel(x + 80 * s, y + 22 * s, 0.62 * s)
    return g
def ghost(x, y, s=1):
    hem = " ".join(f"L{x+(40-k*10)*s:.1f} {y+(56 if k%2==0 else 42)*s:.1f}" for k in range(9))
    f = F(x, y, s)
    g = f'<path d="M{f(-42,56)} L{f(-42,-10)} Q{f(-42,-66)} {f(0,-66)} Q{f(42,-66)} {f(42,-10)} L{f(42,56)} {hem} Z" fill="{INK}"/>'
    g += f'<ellipse cx="{x-15*s:.1f}" cy="{y-18*s:.1f}" rx="{7*s:.1f}" ry="{13*s:.1f}" fill="{FAB}"/><ellipse cx="{x+15*s:.1f}" cy="{y-18*s:.1f}" rx="{7*s:.1f}" ry="{13*s:.1f}" fill="{FAB}"/>'
    g += f'<ellipse cx="{x:.1f}" cy="{y+12*s:.1f}" rx="{8*s:.1f}" ry="{12*s:.1f}" fill="{FAB}"/>'
    g += f'<path d="M{f(-15,-4)} q{-2*s:.1f} {12*s:.1f} 0 {18*s:.1f} M{f(15,-4)} q{2*s:.1f} {10*s:.1f} 0 {14*s:.1f}" stroke="{FAB}" stroke-width="{2*s:.1f}" fill="none"/>'
    return g
def battery(x, y, s=1, level=1):
    g = f'<rect x="{x-80*s:.1f}" y="{y-40*s:.1f}" width="{160*s:.1f}" height="{80*s:.1f}" rx="{8*s:.1f}" fill="none" stroke="{INK}" stroke-width="{9*s:.1f}"/><rect x="{x+82*s:.1f}" y="{y-16*s:.1f}" width="{14*s:.1f}" height="{32*s:.1f}" fill="{INK}"/>'
    for k in range(level):
        g += f'<rect x="{x-66*s+k*38*s:.1f}" y="{y-27*s:.1f}" width="{30*s:.1f}" height="{54*s:.1f}" fill="{RED if level==1 else INK}"/>'
    g += f'<polyline points="{x+10*s:.1f},{y-44*s:.1f} {x+2*s:.1f},{y-16*s:.1f} {x+16*s:.1f},{y+4*s:.1f} {x+4*s:.1f},{y+44*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{4*s:.1f}"/>'
    return g
def heart(x, y, s=1, cracked=True):
    f = F(x, y, s)
    g = f'<path d="M{f(0,52)} L{f(-52,0)} Q{f(-78,-32)} {f(-50,-52)} Q{f(-20,-72)} {f(0,-36)} Q{f(20,-72)} {f(50,-52)} Q{f(78,-32)} {f(52,0)} Z" fill="{INK}"/>'
    if cracked: g += f'<polyline points="{x:.1f},{y-36*s:.1f} {x-10*s:.1f},{y-10*s:.1f} {x+8*s:.1f},{y+6*s:.1f} {x-4*s:.1f},{y+34*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{4.5*s:.1f}"/>'
    vine = " ".join(f"{x+u*s:.1f},{y+(-8+14*math.sin(u/9))*s:.1f}" for u in range(-62, 63, 4))
    g += f'<polyline points="{vine}" fill="none" stroke="{FAB}" stroke-width="{3*s:.1f}"/>'
    for u in range(-54, 55, 18):
        vy = y + (-8 + 14 * math.sin(u / 9)) * s
        g += f'<path d="M{x+u*s:.1f} {vy:.1f} l{3*s:.1f} {-9*s:.1f} l{3*s:.1f} {9*s:.1f} Z" fill="{FAB}"/>'
    for u, L in ((-14, 22), (2, 34), (16, 16)):
        g += f'<path d="M{x+u*s:.1f} {y+40*s:.1f} q{-5*s:.1f} {L*s:.1f} 0 {L*s:.1f} q{5*s:.1f} 0 0 {-L*s:.1f} Z" fill="{INK}"/>'
    return g
def brain(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(-62,10)} Q{f(-78,-30)} {f(-42,-46)} Q{f(-26,-72)} {f(0,-52)} Q{f(26,-72)} {f(42,-46)} Q{f(78,-30)} {f(62,10)} Q{f(56,42)} {f(20,40)} Q{f(0,52)} {f(-20,40)} Q{f(-56,42)} {f(-62,10)} Z" fill="{INK}"/>'
    for d in (-1, 1):
        g += f'<path d="M{f(d*44,-30)} q{-d*18*s:.1f} {10*s:.1f} {-d*6*s:.1f} {24*s:.1f} q{d*16*s:.1f} {10*s:.1f} {-d*4*s:.1f} {26*s:.1f} M{f(d*20,-44)} q{d*10*s:.1f} {20*s:.1f} {-d*4*s:.1f} {34*s:.1f}" stroke="{FAB}" stroke-width="{3*s:.1f}" fill="none"/>'
    g += f'<line x1="{x:.1f}" y1="{y-50*s:.1f}" x2="{x:.1f}" y2="{y+46*s:.1f}" stroke="{FAB}" stroke-width="{3.5*s:.1f}"/>'
    g += ''.join(f'<line x1="{x-7*s:.1f}" y1="{y+v*s:.1f}" x2="{x+7*s:.1f}" y2="{y+(v+3)*s:.1f}" stroke="{FAB}" stroke-width="{2.5*s:.1f}"/>' for v in range(-40, 40, 11))
    return g
def coffee(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(-42,-30)} L{f(42,-30)} L{f(34,48)} L{f(-34,48)} Z" fill="{INK}"/>'
    g += f'<path d="M{f(40,-14)} Q{f(74,-8)} {f(37,24)}" stroke="{INK}" stroke-width="{8*s:.1f}" fill="none"/>'
    g += skull(x, y + 10 * s, 0.38 * s, fg=FAB, bg=INK, cracked=False)
    g += ''.join(f'<path d="M{f(k*18,-40)} q{-10*s:.1f} {-14*s:.1f} 0 {-28*s:.1f} q{10*s:.1f} {-12*s:.1f} 0 {-24*s:.1f}" stroke="{INK}" stroke-width="{3.5*s:.1f}" fill="none"/>' for k in (-1, 0, 1))
    return g
def clock(x, y, s=1, h=3, m=0, cracked=True):
    g = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{58*s:.1f}" fill="{INK}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{50*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{2.5*s:.1f}"/>'
    for k in range(12):
        a = math.radians(k * 30); L = 10 if k % 3 == 0 else 5
        g += f'<line x1="{x+44*s*math.cos(a):.1f}" y1="{y+44*s*math.sin(a):.1f}" x2="{x+(44-L)*s*math.cos(a):.1f}" y2="{y+(44-L)*s*math.sin(a):.1f}" stroke="{FAB}" stroke-width="{3*s:.1f}"/>'
    for ang, ln, w in ((h * 30 + m * 0.5, 26, 6), (m * 6, 38, 3.5)):
        a = math.radians(ang - 90)
        g += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+ln*s*math.cos(a):.1f}" y2="{y+ln*s*math.sin(a):.1f}" stroke="{FAB}" stroke-width="{w*s:.1f}" stroke-linecap="round"/>'
    if cracked: g += f'<polyline points="{x-50*s:.1f},{y-20*s:.1f} {x-30*s:.1f},{y-10*s:.1f} {x-34*s:.1f},{y+8*s:.1f} {x-12*s:.1f},{y+20*s:.1f}" fill="none" stroke="{FAB}" stroke-width="{2*s:.1f}"/>'
    return g
def stopwatch(x, y, s=1):
    return clock(x, y + 8 * s, s * 0.9, 0, 50) + f'<rect x="{x-11*s:.1f}" y="{y-62*s:.1f}" width="{22*s:.1f}" height="{14*s:.1f}" fill="{INK}"/>'
def star4(cx, cy, r):
    k = r * 0.25
    return f'<path d="M{cx:.1f} {cy-r:.1f} L{cx+k:.1f} {cy-k:.1f} L{cx+r:.1f} {cy:.1f} L{cx+k:.1f} {cy+k:.1f} L{cx:.1f} {cy+r:.1f} L{cx-k:.1f} {cy+k:.1f} L{cx-r:.1f} {cy:.1f} L{cx-k:.1f} {cy-k:.1f} Z" fill="{INK}"/>'
def moon(x, y, s=1):
    g = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{56*s:.1f}" fill="{INK}"/><circle cx="{x+28*s:.1f}" cy="{y-14*s:.1f}" r="{48*s:.1f}" fill="{FAB}"/>'
    return g + star4(x + 44 * s, y + 34 * s, 9 * s) + star4(x + 60 * s, y - 44 * s, 6 * s) + star4(x + 20 * s, y + 62 * s, 5 * s)
def candle(x, y, s=1):
    f = F(x, y, s)
    g = f'<rect x="{x-20*s:.1f}" y="{y-20*s:.1f}" width="{40*s:.1f}" height="{82*s:.1f}" fill="{INK}"/>'
    g += f'<path d="M{f(-12,-20)} q{-3*s:.1f} {20*s:.1f} 0 {30*s:.1f} q{3*s:.1f} {-10*s:.1f} 0 {-30*s:.1f} M{f(10,-20)} q{-3*s:.1f} {12*s:.1f} 0 {18*s:.1f}" stroke="{FAB}" stroke-width="{2*s:.1f}" fill="none"/>'
    g += f'<path d="M{f(0,-74)} Q{f(18,-46)} {f(0,-30)} Q{f(-18,-46)} {f(0,-74)} Z" fill="{INK}"/><path d="M{f(0,-56)} Q{f(7,-44)} {f(0,-36)} Q{f(-7,-44)} {f(0,-56)} Z" fill="{FAB}"/>'
    g += f'<line x1="{x:.1f}" y1="{y-30*s:.1f}" x2="{x:.1f}" y2="{y-20*s:.1f}" stroke="{INK}" stroke-width="{2*s:.1f}"/>'
    g += f'<path d="M{f(-42,64)} Q{f(-30,52)} {f(-20,58)} L{f(20,58)} Q{f(34,50)} {f(46,66)} Z" fill="{INK}"/>'
    return g
def hourglass(x, y, s=1):
    f = F(x, y, s)
    g = f'<rect x="{x-48*s:.1f}" y="{y-70*s:.1f}" width="{96*s:.1f}" height="{10*s:.1f}" fill="{INK}"/><rect x="{x-48*s:.1f}" y="{y+60*s:.1f}" width="{96*s:.1f}" height="{10*s:.1f}" fill="{INK}"/>'
    g += ''.join(f'<rect x="{x+u*s:.1f}" y="{y-60*s:.1f}" width="{6*s:.1f}" height="{120*s:.1f}" fill="{INK}"/>' for u in (-44, 38))
    g += f'<path d="M{f(-32,-58)} L{f(32,-58)} L{f(4,0)} L{f(32,58)} L{f(-32,58)} L{f(-4,0)} Z" fill="none" stroke="{INK}" stroke-width="{4*s:.1f}"/>'
    g += f'<path d="M{f(-20,-34)} L{f(20,-34)} L{f(0,-6)} Z" fill="{INK}"/><line x1="{x:.1f}" y1="{y-6*s:.1f}" x2="{x:.1f}" y2="{y+40*s:.1f}" stroke="{INK}" stroke-width="{2*s:.1f}"/>'
    g += f'<path d="M{f(-28,56)} Q{f(0,26)} {f(28,56)} Z" fill="{INK}"/>' + skull(x, y + 47 * s, 0.14 * s, fg=FAB, bg=INK, cracked=False)
    return g
def rose(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(0,20)} C{f(20,60)} {f(-10,90)} {f(6,130)}" stroke="{INK}" stroke-width="{5*s:.1f}" fill="none"/>'
    for v, d in ((50, 1), (78, -1), (104, 1)):
        g += f'<path d="M{f(8 if d>0 else -2, v)} l{d*10*s:.1f} {-4*s:.1f} l{-d*6*s:.1f} {8*s:.1f} Z" fill="{INK}"/>'
    g += f'<path d="M{f(4,92)} Q{f(-30,80)} {f(-36,104)} Q{f(-12,108)} {f(4,92)} Z" fill="{INK}"/>'
    g += f'<path d="M{f(-34,-6)} Q{f(-40,-44)} {f(0,-46)} Q{f(40,-44)} {f(34,-6)} Q{f(26,24)} {f(0,24)} Q{f(-26,24)} {f(-34,-6)} Z" fill="{INK}" transform="rotate(28 {x:.1f} {y:.1f})"/>'
    g += f'<path d="M{f(-6,-18)} q{10*s:.1f} {-12*s:.1f} {18*s:.1f} 0 q{4*s:.1f} {14*s:.1f} {-14*s:.1f} {16*s:.1f} q{-20*s:.1f} {-2*s:.1f} {-18*s:.1f} {-22*s:.1f} q{4*s:.1f} {-18*s:.1f} {30*s:.1f} {-16*s:.1f} M{f(-28,2)} q{24*s:.1f} {20*s:.1f} {54*s:.1f} {-6*s:.1f}" stroke="{FAB}" stroke-width="{3*s:.1f}" fill="none" transform="rotate(28 {x:.1f} {y:.1f})"/>'
    for u, v, rot in ((40, 50, 30), (-50, 70, -40), (30, 110, 10)):
        g += f'<ellipse cx="{x+u*s:.1f}" cy="{y+v*s:.1f}" rx="{10*s:.1f}" ry="{6*s:.1f}" transform="rotate({rot} {x+u*s:.1f} {y+v*s:.1f})" fill="{INK}"/>'
    return g
def flower(x, y, s=1): return rose(x, y - 30 * s, s * 0.8)
def moth(x, y, s=1):
    f = F(x, y, s); g = ''
    for d in (-1, 1):
        g += f'<path d="M{f(d*6,-12)} C{f(d*40,-60)} {f(d*96,-48)} {f(d*98,-30)} C{f(d*90,-6)} {f(d*40,8)} {f(d*6,6)} Z" fill="{INK}"/>'
        g += f'<path d="M{f(d*6,6)} C{f(d*30,10)} {f(d*60,30)} {f(d*48,52)} C{f(d*30,60)} {f(d*10,36)} {f(d*4,18)} Z" fill="{INK}"/>'
        g += f'<path d="M{f(d*10,-8)} L{f(d*80,-36)} M{f(d*10,-4)} L{f(d*70,-8)} M{f(d*10,12)} L{f(d*40,40)}" stroke="{FAB}" stroke-width="{2*s:.1f}"/>'
        g += f'<circle cx="{x+d*70*s:.1f}" cy="{y-24*s:.1f}" r="{6*s:.1f}" fill="{FAB}"/><circle cx="{x+d*36*s:.1f}" cy="{y+30*s:.1f}" r="{4*s:.1f}" fill="{FAB}"/>'
        g += f'<path d="M{f(d*3,-26)} Q{f(d*14,-50)} {f(d*26,-54)}" stroke="{INK}" stroke-width="{2.2*s:.1f}" fill="none"/>'
    g += f'<ellipse cx="{x:.1f}" cy="{y+12*s:.1f}" rx="{9*s:.1f}" ry="{40*s:.1f}" fill="{INK}"/>'
    g += skull(x, y - 6 * s, 0.16 * s, fg=FAB, bg=INK, cracked=False)
    g += ''.join(f'<line x1="{x-8*s:.1f}" y1="{y+v*s:.1f}" x2="{x+8*s:.1f}" y2="{y+v*s:.1f}" stroke="{FAB}" stroke-width="{2*s:.1f}"/>' for v in (18, 28, 38))
    return g
def raven(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(-26,-24)} C{f(-6,-34)} {f(30,-16)} {f(40,14)} L{f(86,40)} L{f(40,34)} C{f(20,48)} {f(-20,40)} {f(-30,10)} C{f(-36,-4)} {f(-34,-14)} {f(-26,-24)} Z" fill="{INK}"/>'
    g += f'<circle cx="{x-30*s:.1f}" cy="{y-30*s:.1f}" r="{16*s:.1f}" fill="{INK}"/><path d="M{f(-42,-36)} L{f(-74,-26)} L{f(-42,-22)} Z" fill="{INK}"/>'
    g += f'<circle cx="{x-33*s:.1f}" cy="{y-33*s:.1f}" r="{3.5*s:.1f}" fill="{FAB}"/>'
    g += f'<path d="M{f(-14,-6)} C{f(10,-2)} {f(28,10)} {f(50,30)} M{f(-10,6)} C{f(10,12)} {f(24,20)} {f(40,32)}" stroke="{FAB}" stroke-width="{2.5*s:.1f}" fill="none"/>'
    g += f'<path d="M{f(-6,40)} L{f(-10,62)} M{f(6,42)} L{f(4,62)}" stroke="{INK}" stroke-width="{3*s:.1f}"/>'
    return g + bone(x - 50 * s, y + 64 * s, x + 50 * s, y + 64 * s, 7 * s)
def eye(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(-72,0)} Q{f(0,-58)} {f(72,0)} Q{f(0,58)} {f(-72,0)} Z" fill="{INK}"/>'
    g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{24*s:.1f}" fill="{FAB}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{10*s:.1f}" fill="{INK}"/>'
    for k in range(7):
        a = math.radians(-150 + k * 20)
        g += f'<line x1="{x+60*s*math.cos(a):.1f}" y1="{y-6*s+34*s*math.sin(a):.1f}" x2="{x+76*s*math.cos(a):.1f}" y2="{y-6*s+46*s*math.sin(a):.1f}" stroke="{INK}" stroke-width="{3.5*s:.1f}" stroke-linecap="round"/>'
    g += f'<path d="M{f(20,34)} q{-7*s:.1f} {22*s:.1f} 0 {26*s:.1f} q{7*s:.1f} {-4*s:.1f} 0 {-26*s:.1f} Z" fill="{INK}"/>'
    return g
def bones(x, y, s=1):
    return bone(x - 62 * s, y - 50 * s, x + 62 * s, y + 50 * s, 13 * s) + bone(x + 62 * s, y - 50 * s, x - 62 * s, y + 50 * s, 13 * s) + skull(x, y - 4 * s, 0.6 * s)
def bat(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(0,-12)} Q{f(-25,-34)} {f(-86,-28)} Q{f(-64,-10)} {f(-70,12)} Q{f(-48,0)} {f(-38,18)} Q{f(-16,2)} {f(0,28)} Q{f(16,2)} {f(38,18)} Q{f(48,0)} {f(70,12)} Q{f(64,-10)} {f(86,-28)} Q{f(25,-34)} {f(0,-12)} Z" fill="{INK}"/>'
    g += f'<path d="M{f(-8,-12)} L{f(-6,-24)} L{f(-2,-14)} Z M{f(8,-12)} L{f(6,-24)} L{f(2,-14)} Z" fill="{INK}"/>'
    return g + f'<circle cx="{x-4*s:.1f}" cy="{y-4*s:.1f}" r="{2.4*s:.1f}" fill="{FAB}"/><circle cx="{x+4*s:.1f}" cy="{y-4*s:.1f}" r="{2.4*s:.1f}" fill="{FAB}"/>'
def bolt(x, y, s=1):
    f = F(x, y, s)
    return f'<path d="M{f(12,-70)} L{f(-34,8)} L{f(-2,8)} L{f(-16,70)} L{f(36,-14)} L{f(2,-14)} Z" fill="{INK}"/>'
def flame(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(0,-72)} Q{f(48,-20)} {f(36,26)} Q{f(26,62)} {f(0,62)} Q{f(-26,62)} {f(-36,26)} Q{f(-42,-12)} {f(-12,-32)} Q{f(0,-12)} {f(5,-22)} Q{f(10,-48)} {f(0,-72)} Z" fill="{INK}"/>'
    return g + skull(x, y + 26 * s, 0.32 * s, fg=FAB, bg=INK, cracked=False)
def bottle(x, y, s=1):
    f = F(x, y, s)
    g = (f'<path d="M{f(-14,-60)} L{f(14,-60)} L{f(14,-36)} Q{f(40,-26)} {f(40,4)} L{f(40,62)} Q{f(0,72)} {f(-40,62)} L{f(-40,4)} Q{f(-40,-26)} {f(-14,-36)} Z" fill="{INK}"/>'
         f'<rect x="{x-11*s:.1f}" y="{y-76*s:.1f}" width="{22*s:.1f}" height="{18*s:.1f}" rx="{3*s:.1f}" fill="{INK}"/>'
         f'<rect x="{x-30*s:.1f}" y="{y+2*s:.1f}" width="{60*s:.1f}" height="{50*s:.1f}" fill="{FAB}"/>')
    return g + skull(x, y + 26 * s, 0.3 * s, cracked=False)
def chain(x, y, s=1, broken=False):
    g = ''
    for k in range(-2, 3):
        if broken and k == 0:
            g += f'<path d="M{x-14*s:.1f} {y-10*s:.1f} l{8*s:.1f} {6*s:.1f} M{x+14*s:.1f} {y+10*s:.1f} l{-8*s:.1f} {-6*s:.1f}" stroke="{INK}" stroke-width="{6*s:.1f}"/>'; continue
        g += f'<rect x="{x+k*44*s-26*s:.1f}" y="{y-15*s:.1f}" width="{52*s:.1f}" height="{30*s:.1f}" rx="{15*s:.1f}" fill="none" stroke="{INK}" stroke-width="{8*s:.1f}"/>'
    return g
def anchor(x, y, s=1):
    f = F(x, y, s)
    return (f'<circle cx="{x:.1f}" cy="{y-58*s:.1f}" r="{13*s:.1f}" fill="none" stroke="{INK}" stroke-width="{7*s:.1f}"/><line x1="{x:.1f}" y1="{y-45*s:.1f}" x2="{x:.1f}" y2="{y+58*s:.1f}" stroke="{INK}" stroke-width="{9*s:.1f}"/>'
            f'<line x1="{x-32*s:.1f}" y1="{y-22*s:.1f}" x2="{x+32*s:.1f}" y2="{y-22*s:.1f}" stroke="{INK}" stroke-width="{8*s:.1f}"/>'
            f'<path d="M{f(-58,8)} Q{f(-52,62)} {f(0,60)} Q{f(52,62)} {f(58,8)}" fill="none" stroke="{INK}" stroke-width="{9*s:.1f}"/>'
            f'<path d="M{f(-66,14)} L{f(-58,-2)} L{f(-48,12)} Z M{f(66,14)} L{f(58,-2)} L{f(48,12)} Z" fill="{INK}"/>' + chain(x, y + 18 * s, 0.4 * s))
def rack(x, y, s=1):
    g = ''.join(f'<rect x="{x+u*s:.1f}" y="{y-86*s:.1f}" width="{12*s:.1f}" height="{172*s:.1f}" fill="{INK}"/>' for u in (-82, 70))
    g += f'<rect x="{x-100*s:.1f}" y="{y+80*s:.1f}" width="{200*s:.1f}" height="{10*s:.1f}" fill="{INK}"/><rect x="{x-82*s:.1f}" y="{y-92*s:.1f}" width="{164*s:.1f}" height="{10*s:.1f}" fill="{INK}"/>'
    for u in (-58, 56):
        g += ''.join(f'<ellipse cx="{x+u*s:.1f}" cy="{y+(-74+k*13)*s:.1f}" rx="{4*s:.1f}" ry="{7*s:.1f}" fill="none" stroke="{INK}" stroke-width="{2.2*s:.1f}"/>' for k in range(6))
    return g + barbell(x, y - 10 * s, 0.78 * s)
def sun(x, y, s=1, rising=False):
    g = ''
    for k in range(16):
        a = math.radians(k * 22.5); L = 82 if k % 2 == 0 else 64
        if rising and math.sin(a) > 0.05: continue
        g += f'<polygon points="{x+46*s*math.cos(a-0.09):.1f},{y+46*s*math.sin(a-0.09):.1f} {x+L*s*math.cos(a):.1f},{y+L*s*math.sin(a):.1f} {x+46*s*math.cos(a+0.09):.1f},{y+46*s*math.sin(a+0.09):.1f}" fill="{INK}"/>'
    g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{42*s:.1f}" fill="{INK}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{34*s:.1f}" fill="{FAB}"/>'
    if rising: g += f'<rect x="{x-90*s:.1f}" y="{y:.1f}" width="{180*s:.1f}" height="{90*s:.1f}" fill="{FAB}"/><line x1="{x-90*s:.1f}" y1="{y:.1f}" x2="{x+90*s:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="{5*s:.1f}"/>'
    return g
def web(x, y, s=1):
    g = ''
    ang = [math.radians(k * 45 + 10) for k in range(9)]
    for a in ang[:8]:
        g += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+80*s*math.cos(a):.1f}" y2="{y+80*s*math.sin(a):.1f}" stroke="{INK}" stroke-width="{2.5*s:.1f}"/>'
    for r in (18, 36, 54, 72):
        pts = [(x + r * s * math.cos(a), y + r * s * math.sin(a)) for a in ang]
        g += f'<path d="M{pts[0][0]:.1f} {pts[0][1]:.1f} ' + " ".join(f"Q{(pts[i][0]+pts[i+1][0])/2*0.9+x*0.1:.1f} {(pts[i][1]+pts[i+1][1])/2*0.9+y*0.1:.1f} {pts[i+1][0]:.1f} {pts[i+1][1]:.1f}" for i in range(8)) + f'" fill="none" stroke="{INK}" stroke-width="{2.2*s:.1f}"/>'
    sx, sy = x + 30 * s, y + 46 * s
    g += f'<line x1="{sx:.1f}" y1="{y+20*s:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{INK}" stroke-width="{1.5*s:.1f}"/><ellipse cx="{sx:.1f}" cy="{sy+8*s:.1f}" rx="{8*s:.1f}" ry="{11*s:.1f}" fill="{INK}"/><circle cx="{sx:.1f}" cy="{sy-2*s:.1f}" r="{5*s:.1f}" fill="{INK}"/>'
    for d in (-1, 1):
        for k in range(4):
            g += f'<polyline points="{sx:.1f},{sy+(2+k*4)*s:.1f} {sx+d*14*s:.1f},{sy+(-6+k*6)*s:.1f} {sx+d*20*s:.1f},{sy+(6+k*6)*s:.1f}" fill="none" stroke="{INK}" stroke-width="{1.8*s:.1f}"/>'
    return g
def cloud(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(-64,14)} Q{f(-86,-16)} {f(-48,-22)} Q{f(-38,-58)} {f(0,-48)} Q{f(32,-70)} {f(48,-26)} Q{f(86,-22)} {f(64,14)} Z" fill="{INK}"/>'
    return g + bolt(x + 8 * s, y + 52 * s, 0.5 * s)
def checklist(x, y, s=1, items=()):
    g = ''
    for i, t in enumerate(items):
        yy = y + i * 40 * s
        g += f'<rect x="{x-120*s:.1f}" y="{yy-22*s:.1f}" width="{24*s:.1f}" height="{24*s:.1f}" fill="none" stroke="{INK}" stroke-width="{3.5*s:.1f}"/>'
        g += f'<path d="M{x-116*s:.1f} {yy-10*s:.1f} L{x-108*s:.1f} {yy-1*s:.1f} L{x-92*s:.1f} {yy-28*s:.1f}" stroke="{INK}" stroke-width="{4.5*s:.1f}" fill="none"/>'
        g += tpath(t, "type", 22 * s, x - 84 * s, yy, anchor="start")
    return g
def none(x, y, s=1): return ""

# ---------------- morbid set: morgue / rot / anatomy / funeral ----------------
def toe_tag(x, y, s=1, label="DOA", line1="NAME: ________", line2="CAUSE: ________"):
    g = f'<g transform="rotate(-12 {x:.1f} {y:.1f})">'
    g += f'<path d="M{x-80*s:.1f} {y-38*s:.1f} L{x+70*s:.1f} {y-38*s:.1f} L{x+92*s:.1f} {y-16*s:.1f} L{x+92*s:.1f} {y+16*s:.1f} L{x+70*s:.1f} {y+38*s:.1f} L{x-80*s:.1f} {y+38*s:.1f} Z" fill="{INK}"/>'
    g += f'<circle cx="{x+72*s:.1f}" cy="{y:.1f}" r="{8*s:.1f}" fill="{FAB}"/>'
    g += tpath(label, "osw", fitsize(label, "osw", 130 * s, 30 * s), x - 6 * s, y - 6 * s, fill=FAB)
    g += tpath(line1, "type", 11 * s, x - 70 * s, y + 13 * s, anchor="start", fill=FAB) + tpath(line2, "type", 11 * s, x - 70 * s, y + 28 * s, anchor="start", fill=FAB)
    g += '</g>'
    g += f'<path d="M{x+70*s:.1f} {y-14*s:.1f} C{x+120*s:.1f} {y-40*s:.1f} {x+110*s:.1f} {y-90*s:.1f} {x+60*s:.1f} {y-96*s:.1f}" stroke="{INK}" stroke-width="{3*s:.1f}" fill="none"/>'
    return g
def body_bag(x, y, s=1):
    g = f'<rect x="{x-110*s:.1f}" y="{y-38*s:.1f}" width="{220*s:.1f}" height="{76*s:.1f}" rx="{38*s:.1f}" fill="{INK}"/>'
    g += f'<path d="M{x-50*s:.1f} {y:.1f} L{x+96*s:.1f} {y:.1f}" stroke="{FAB}" stroke-width="{3*s:.1f}"/>'
    g += ''.join(f'<line x1="{x+u*s:.1f}" y1="{y-5*s:.1f}" x2="{x+u*s:.1f}" y2="{y+5*s:.1f}" stroke="{FAB}" stroke-width="{2*s:.1f}"/>' for u in range(-44, 96, 7))
    g += f'<rect x="{x+92*s:.1f}" y="{y-6*s:.1f}" width="{14*s:.1f}" height="{12*s:.1f}" rx="{3*s:.1f}" fill="{FAB}"/>'
    g += f'<path d="M{x-104*s:.1f} {y:.1f} Q{x-80*s:.1f} {y-34*s:.1f} {x-50*s:.1f} {y:.1f} Q{x-80*s:.1f} {y+34*s:.1f} {x-104*s:.1f} {y:.1f} Z" fill="{FAB}"/>'
    g += f'<g transform="rotate(-90 {x-78*s:.1f} {y:.1f})">' + skull(x - 78 * s, y, 0.32 * s, cracked=False) + '</g>'
    return g
def morgue_drawer(x, y, s=1):
    g = f'<rect x="{x-110*s:.1f}" y="{y-70*s:.1f}" width="{90*s:.1f}" height="{90*s:.1f}" fill="none" stroke="{INK}" stroke-width="{6*s:.1f}"/>'
    g += f'<rect x="{x-90*s:.1f}" y="{y-58*s:.1f}" width="{50*s:.1f}" height="{18*s:.1f}" fill="{INK}"/><rect x="{x-82*s:.1f}" y="{y-20*s:.1f}" width="{34*s:.1f}" height="{8*s:.1f}" rx="{4*s:.1f}" fill="{INK}"/>'
    g += f'<rect x="{x-24*s:.1f}" y="{y-6*s:.1f}" width="{150*s:.1f}" height="{12*s:.1f}" fill="{INK}"/>'
    g += f'<path d="M{x-20*s:.1f} {y-6*s:.1f} Q{x+10*s:.1f} {y-40*s:.1f} {x+40*s:.1f} {y-22*s:.1f} Q{x+70*s:.1f} {y-32*s:.1f} {x+100*s:.1f} {y-20*s:.1f} L{x+112*s:.1f} {y-6*s:.1f} Z" fill="{INK}"/>'
    for u in (106, 122):
        g += f'<path d="M{x+u*s:.1f} {y-8*s:.1f} q{2*s:.1f} {-26*s:.1f} {10*s:.1f} {-28*s:.1f} q{6*s:.1f} {2*s:.1f} {2*s:.1f} {28*s:.1f} Z" fill="{INK}"/>'
    g += f'<path d="M{x+118*s:.1f} {y-30*s:.1f} l{14*s:.1f} {-16*s:.1f}" stroke="{INK}" stroke-width="{2*s:.1f}"/><rect x="{x+126*s:.1f}" y="{y-62*s:.1f}" width="{28*s:.1f}" height="{18*s:.1f}" fill="{INK}" transform="rotate(-20 {x+140*s:.1f} {y-53*s:.1f})"/>'
    return g
def y_incision(x, y, s=1):
    f = F(x, y, s)
    g = skull(x, y - 92 * s, 0.42 * s, cracked=False)
    g += f'<rect x="{x-8*s:.1f}" y="{y-70*s:.1f}" width="{16*s:.1f}" height="{14*s:.1f}" fill="{INK}"/>'
    g += f'<path d="M{f(-62,-56)} Q{f(0,-64)} {f(62,-56)} L{f(54,30)} Q{f(40,70)} {f(30,74)} L{f(-30,74)} Q{f(-40,70)} {f(-54,30)} Z" fill="{INK}"/>'
    g += f'<path d="M{f(-44,-48)} L{f(0,-6)} L{f(44,-48)} M{f(0,-6)} L{f(0,66)}" stroke="{FAB}" stroke-width="{3*s:.1f}" fill="none"/>'
    for (x1, y1, x2, y2) in ((-44, -48, 0, -6), (44, -48, 0, -6), (0, -6, 0, 66)):
        for t in range(1, 8):
            px, py = x1 + (x2 - x1) * t / 8, y1 + (y2 - y1) * t / 8
            dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); nx, ny = -dy / L * 6, dx / L * 6
            g += f'<line x1="{x+(px-nx)*s:.1f}" y1="{y+(py-ny)*s:.1f}" x2="{x+(px+nx)*s:.1f}" y2="{y+(py+ny)*s:.1f}" stroke="{FAB}" stroke-width="{1.8*s:.1f}"/>'
    for v in (-30, -14, 2):
        for d in (-1, 1):
            g += f'<path d="M{f(d*14,v)} Q{f(d*40,v-4)} {f(d*50,v+8)}" stroke="{FAB}" stroke-width="{1.6*s:.1f}" fill="none" stroke-dasharray="{3*s:.1f} {3*s:.1f}"/>'
    return g
def autopsy_report(x, y, s=1, fields=(("CAUSE OF DEATH", "leg day"), ("TIME OF DEATH", "5:00 a.m."))):
    w, h = 250 * s, (44 + 30 * len(fields)) * s
    g = f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{INK}" stroke-width="{4*s:.1f}"/>'
    g += f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{30*s:.1f}" fill="{INK}"/>'
    g += tpath("AUTOPSY REPORT", "osw", 20 * s, x, y - h / 2 + 23 * s, fill=FAB)
    for i, (k, v) in enumerate(fields):
        yy = y - h / 2 + (58 + i * 30) * s
        g += tpath(k + ":", "type", 12 * s, x - w / 2 + 10 * s, yy, anchor="start")
        kw = measure(k + ":", "type", 12 * s)
        g += tpath(v, "type", fitsize(v, "type", w - kw - 30 * s, 17 * s), x - w / 2 + 18 * s + kw, yy, anchor="start")
        g += f'<line x1="{x-w/2+14*s+kw:.1f}" y1="{yy+4*s:.1f}" x2="{x+w/2-10*s:.1f}" y2="{yy+4*s:.1f}" stroke="{INK}" stroke-width="{1.2*s:.1f}"/>'
    return g
def maggots(x, y, s=1, n=7, spread=60):
    g = ''
    for k in range(n):
        a = k * 2.399; r = spread * math.sqrt((k + 0.5) / n)
        cx, cy = x + r * math.cos(a) * s, y + r * math.sin(a) * s * 0.6; rot = (k * 47) % 180
        g += f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})"><ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{8*s:.1f}" ry="{3.6*s:.1f}" fill="{INK}"/>'
        g += ''.join(f'<line x1="{cx+u*s:.1f}" y1="{cy-3.6*s:.1f}" x2="{cx+u*s:.1f}" y2="{cy+3.6*s:.1f}" stroke="{FAB}" stroke-width="{0.9*s:.1f}"/>' for u in (-3, 0, 3)) + '</g>'
    return g
def flies(x, y, s=1, n=4, spread=70):
    g = ''
    for k in range(n):
        a = k * 2.1 + 0.6; r = spread * (0.5 + 0.5 * ((k * 37) % 10) / 10)
        cx, cy = x + r * math.cos(a) * s, y + r * math.sin(a) * s * 0.7
        g += f'<ellipse cx="{cx-5*s:.1f}" cy="{cy-5*s:.1f}" rx="{6*s:.1f}" ry="{3.5*s:.1f}" fill="none" stroke="{INK}" stroke-width="{1.4*s:.1f}" transform="rotate(-30 {cx:.1f} {cy:.1f})"/>'
        g += f'<ellipse cx="{cx+5*s:.1f}" cy="{cy-5*s:.1f}" rx="{6*s:.1f}" ry="{3.5*s:.1f}" fill="none" stroke="{INK}" stroke-width="{1.4*s:.1f}" transform="rotate(30 {cx:.1f} {cy:.1f})"/>'
        g += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{3.4*s:.1f}" ry="{5*s:.1f}" fill="{INK}"/>'
        g += f'<path d="M{cx-20*s:.1f} {cy+8*s:.1f} q{6*s:.1f} {-8*s:.1f} {12*s:.1f} 0 q{4*s:.1f} {6*s:.1f} {6*s:.1f} {-4*s:.1f}" stroke="{INK}" stroke-width="{1*s:.1f}" fill="none" stroke-dasharray="{2*s:.1f} {2*s:.1f}"/>'
    return g
def rot_skull(x, y, s=1):
    f = F(x, y, s)
    g = skull(x, y, s)
    g += (f'<path d="M{f(2,-66)} C{f(-40,-70)} {f(-58,-34)} {f(-54,0)} C{f(-54,22)} {f(-46,36)} {f(-36,50)} L{f(-24,56)} '
          f'L{f(-20,44)} L{f(-12,50)} L{f(-10,36)} L{f(-2,40)} L{f(-4,26)} L{f(4,22)} L{f(-2,12)} L{f(6,4)} L{f(-2,-6)} L{f(6,-16)} L{f(-2,-24)} L{f(6,-34)} L{f(-2,-44)} L{f(6,-54)} Z" fill="{INK}"/>')
    g += f'<path d="M{f(6,-54)} L{f(-2,-44)} L{f(6,-34)} L{f(-2,-24)} L{f(6,-16)} L{f(-2,-6)} L{f(6,4)} L{f(-2,12)} L{f(4,22)} L{f(-4,26)} L{f(-2,40)} L{f(-10,36)} L{f(-12,50)} L{f(-20,44)} L{f(-24,56)}" stroke="{FAB}" stroke-width="{2.4*s:.1f}" fill="none"/>'
    g += f'<path d="M{f(-36,-12)} Q{f(-22,-24)} {f(-8,-12)} Q{f(-22,-2)} {f(-36,-12)} Z" fill="{FAB}"/><circle cx="{x-22*s:.1f}" cy="{y-12*s:.1f}" r="{4.5*s:.1f}" fill="{INK}"/>'
    g += f'<path d="M{f(-40,-26)} Q{f(-22,-34)} {f(-6,-26)}" stroke="{FAB}" stroke-width="{2*s:.1f}" fill="none"/>'
    g += ''.join(f'<path d="M{f(u,v)} q{3*s:.1f} {6*s:.1f} 0 {12*s:.1f}" stroke="{FAB}" stroke-width="{1.2*s:.1f}" fill="none"/>' for u, v in ((-44, 8), (-36, 16), (-28, 4), (-46, -40), (-30, -50)))
    g += f'<path d="M{f(-30,30)} Q{f(-16,34)} {f(-6,30)}" stroke="{FAB}" stroke-width="{2.4*s:.1f}" fill="none"/>'
    g += maggots(x + 22 * s, y - 2 * s, 0.7 * s, n=5, spread=18)
    for u, L in ((-38, 22), (-26, 30), (-12, 16)):
        g += f'<path d="M{f(u,54)} q{-4*s:.1f} {L*s:.1f} 0 {L*s:.1f} q{4*s:.1f} 0 0 {-L*s:.1f} Z" fill="{INK}"/>'
    return g
def rot_lifter(x, y, s=1):
    s2 = s * 0.78 * 0.85
    g = figure(x, y, s * 0.85, "press")
    hy = y - 75 * s2
    for u, v, L in ((-30, 40, 16), (24, 52, 22), (-12, 120, 14), (20, 150, 18)):
        g += f'<path d="M{x+u*s2:.1f} {hy+v*s2:.1f} q{-6*s2:.1f} {6*s2:.1f} {-2*s2:.1f} {L*s2:.1f} q{6*s2:.1f} {-2*s2:.1f} {8*s2:.1f} {-L*s2:.1f} Z" fill="{INK}"/>'
    return g + flies(x, hy - 20 * s2, s * 0.8, n=4, spread=90)
def anatomical_heart(x, y, s=1, drips=True):
    f = F(x, y, s)
    g = (f'<path d="M{f(-10,-34)} C{f(-46,-50)} {f(-66,-14)} {f(-54,16)} C{f(-42,50)} {f(-8,70)} {f(10,82)} C{f(24,60)} {f(58,36)} {f(56,0)} '
         f'C{f(54,-30)} {f(30,-46)} {f(10,-34)} Z" fill="{INK}"/>')
    g += f'<path d="M{f(-6,-34)} L{f(-8,-70)} Q{f(-6,-86)} {f(14,-86)} Q{f(36,-86)} {f(38,-62)} L{f(36,-30)}" fill="none" stroke="{INK}" stroke-width="{16*s:.1f}"/>'
    for u, v in ((4, -84), (16, -90), (28, -84)):
        g += f'<line x1="{x+u*s:.1f}" y1="{y+(v+6)*s:.1f}" x2="{x+(u+2)*s:.1f}" y2="{y+(v-12)*s:.1f}" stroke="{INK}" stroke-width="{6*s:.1f}" stroke-linecap="round"/>'
    g += f'<path d="M{f(-30,-30)} Q{f(-44,-52)} {f(-34,-66)}" fill="none" stroke="{INK}" stroke-width="{10*s:.1f}" stroke-linecap="round"/>'
    g += f'<path d="M{f(-6,-20)} C{f(-14,0)} {f(-2,20)} {f(-10,44)} M{f(-6,-2)} L{f(-30,10)} M{f(-8,24)} L{f(10,40)} M{f(26,-24)} C{f(30,-4)} {f(40,10)} {f(34,30)}" stroke="{FAB}" stroke-width="{2.4*s:.1f}" fill="none"/>'
    g += f'<circle cx="{x-8*s:.1f}" cy="{y-82*s:.1f}" r="{4*s:.1f}" fill="{FAB}"/><circle cx="{x+36*s:.1f}" cy="{y-58*s:.1f}" r="{4*s:.1f}" fill="{FAB}"/>'
    if drips:
        for u, L in ((-20, 26), (6, 40), (22, 18)):
            g += f'<path d="M{f(u,62 if u<0 else 70)} q{-5*s:.1f} {L*s:.1f} 0 {L*s:.1f} q{5*s:.1f} 0 0 {-L*s:.1f} Z" fill="{INK}"/>'
    return g
def ekg(x, y, s=1, w=220):
    pts = [(-w / 2, 0), (-40, 0), (-30, -8), (-22, 0), (-14, 0), (-8, 34), (0, -62), (8, 18), (16, 0), (34, 0), (42, -10), (52, 0), (w / 2, 0)]
    return f'<polyline points="{" ".join(f"{x+u*s:.1f},{y+v*s:.1f}" for u, v in pts)}" fill="none" stroke="{INK}" stroke-width="{4.5*s:.1f}" stroke-linejoin="round" stroke-linecap="round"/>'
def flatline(x, y, s=1):
    return anatomical_heart(x, y - 18 * s, s * 0.72, drips=False) + ekg(x, y + 62 * s, s, 240)
def flayed_figure(x, y, s=1, labels=("SPITE", "GRIEF", "CAFFEINE", "REGRET")):
    f = F(x, y, s)
    g = skull(x, y - 98 * s, 0.34 * s, cracked=False)
    g += (f'<path d="M{f(-10,-80)} L{f(-44,-70)} Q{f(-62,-64)} {f(-64,-44)} L{f(-70,10)} L{f(-58,12)} L{f(-48,-34)} L{f(-40,-2)} '
          f'L{f(-34,40)} L{f(-30,110)} L{f(-12,110)} L{f(-4,46)} L{f(4,46)} L{f(12,110)} L{f(30,110)} L{f(34,40)} L{f(40,-2)} L{f(48,-34)} '
          f'L{f(58,12)} L{f(70,10)} L{f(64,-44)} Q{f(62,-64)} {f(44,-70)} L{f(10,-80)} Z" fill="{INK}"/>')
    lines = [((0, -66), (0, 30)), ((-34, -50), (0, -38)), ((34, -50), (0, -38)), ((-30, -36), (-4, -24)), ((30, -36), (4, -24))]
    for v in (-12, 2, 16, 30):
        lines.append(((-18, v), (18, v)))
    for (a, b) in lines:
        g += f'<line x1="{x+a[0]*s:.1f}" y1="{y+a[1]*s:.1f}" x2="{x+b[0]*s:.1f}" y2="{y+b[1]*s:.1f}" stroke="{FAB}" stroke-width="{1.8*s:.1f}"/>'
    for d in (-1, 1):
        g += f'<path d="M{f(d*52,-52)} Q{f(d*60,-40)} {f(d*54,-26)} M{f(d*22,50)} Q{f(d*14,74)} {f(d*20,100)}" stroke="{FAB}" stroke-width="{1.8*s:.1f}" fill="none"/>'
    pts = [((-26, -46), (-118, -60)), ((26, -46), (118, -60)), ((-12, 8), (-118, 20)), ((20, 70), (118, 80))]
    for (a, b), lab in zip(pts, labels):
        g += f'<line x1="{x+a[0]*s:.1f}" y1="{y+a[1]*s:.1f}" x2="{x+b[0]*s:.1f}" y2="{y+b[1]*s:.1f}" stroke="{INK}" stroke-width="{1.4*s:.1f}"/><circle cx="{x+a[0]*s:.1f}" cy="{y+a[1]*s:.1f}" r="{2.6*s:.1f}" fill="{FAB}" stroke="{INK}" stroke-width="{1.2*s:.1f}"/>'
        g += tpath(lab, "type", 12 * s, x + b[0] * s, y + (b[1] - 4) * s, anchor="end" if b[0] < 0 else "start")
    return g
def open_grave(x, y, s=1):
    f = F(x, y, s)
    g = f'<path d="M{f(-110,20)} L{f(70,20)} L{f(100,-14)} L{f(-80,-14)} Z" fill="{INK}"/>'
    g += f'<path d="M{f(-60,10)} L{f(40,10)} L{f(58,-8)} L{f(-42,-8)} Z" fill="{FAB}"/>' + f'<path d="M{f(-50,6)} L{f(34,6)} L{f(48,-5)} L{f(-36,-5)} Z" fill="none" stroke="{INK}" stroke-width="{2*s:.1f}"/>'
    g += f'<path d="M{f(70,20)} Q{f(90,-40)} {f(130,-30)} Q{f(160,-20)} {f(170,20)} Z" fill="{INK}"/>'
    g += ''.join(f'<circle cx="{x+u*s:.1f}" cy="{y+v*s:.1f}" r="{2.4*s:.1f}" fill="{FAB}"/>' for u, v in ((100, -10), (122, -2), (140, -14), (150, 6), (112, 10)))
    g += f'<line x1="{x+130*s:.1f}" y1="{y-30*s:.1f}" x2="{x+150*s:.1f}" y2="{y-110*s:.1f}" stroke="{INK}" stroke-width="{5*s:.1f}"/><path d="M{f(122,-30)} L{f(140,-30)} L{f(136,-4)} L{f(126,-4)} Z" fill="{INK}"/>'
    g += f'<path d="M{f(142,-112)} L{f(158,-108)}" stroke="{INK}" stroke-width="{6*s:.1f}" stroke-linecap="round"/>'
    g += tombstone(x - 90 * s, y - 64 * s, 0.55 * s, "RIP", hand=False)
    return g
def reaper(x, y, s=1, spot=True):
    f = F(x, y, s)
    g = (f'<path d="M{f(0,-96)} C{f(-36,-96)} {f(-44,-60)} {f(-44,-36)} L{f(-62,40)} L{f(-70,96)} L{f(-50,86)} L{f(-38,98)} L{f(-22,88)} L{f(-6,100)} '
         f'L{f(10,88)} L{f(26,100)} L{f(40,88)} L{f(56,98)} L{f(68,96)} L{f(60,40)} L{f(44,-36)} C{f(44,-60)} {f(36,-96)} {f(0,-96)} Z" fill="{INK}"/>')
    g += f'<path d="M{f(-24,-62)} Q{f(0,-82)} {f(24,-62)} L{f(22,-28)} Q{f(0,-18)} {f(-22,-28)} Z" fill="{FAB}"/>'
    g += skull(x, y - 46 * s, 0.24 * s, fg=INK, bg=FAB, cracked=False)
    g += f'<line x1="{x+70*s:.1f}" y1="{y-130*s:.1f}" x2="{x+70*s:.1f}" y2="{y+100*s:.1f}" stroke="{INK}" stroke-width="{5*s:.1f}"/>'
    g += f'<path d="M{f(70,-130)} Q{f(10,-150)} {f(-40,-112)} Q{f(10,-128)} {f(70,-116)} Z" fill="{INK}"/>'
    if spot:
        g += barbell(x, y - 14 * s, 0.72 * s)
        for d in (-1, 1):
            g += hand_skel(x + d * 30 * s, y + 6 * s, 0.34 * s)
    return g
def obituary(x, y, s=1, lines=("Beloved. Tired.", "Survived by a squat rack", "and three friends.", "In lieu of flowers,", "rack your weights.")):
    w = 240 * s
    g = tpath("Obituaries", "black", 30 * s, x, y - 70 * s)
    g += f'<line x1="{x-w/2:.1f}" y1="{y-60*s:.1f}" x2="{x+w/2:.1f}" y2="{y-60*s:.1f}" stroke="{INK}" stroke-width="{3*s:.1f}"/><line x1="{x-w/2:.1f}" y1="{y-55*s:.1f}" x2="{x+w/2:.1f}" y2="{y-55*s:.1f}" stroke="{INK}" stroke-width="{1.2*s:.1f}"/>'
    g += f'<rect x="{x-w/2:.1f}" y="{y-46*s:.1f}" width="{70*s:.1f}" height="{84*s:.1f}" fill="{INK}"/>' + skull(x - w / 2 + 35 * s, y - 2 * s, 0.4 * s, fg=FAB, bg=INK, cracked=False)
    for i, t in enumerate(lines):
        g += tpath(t, "type", fitsize(t, "type", 160 * s, 13 * s), x - w / 2 + 80 * s, y + (-30 + i * 17) * s, anchor="start")
    for i in range(3):
        g += f'<line x1="{x-w/2:.1f}" y1="{y+(54+i*9)*s:.1f}" x2="{x+w/2-(30 if i==2 else 0)*s:.1f}" y2="{y+(54+i*9)*s:.1f}" stroke="{INK}" stroke-width="{2.4*s:.1f}"/>'
    return g
def wreath(x, y, s=1):
    g = ''
    for k in range(22):
        a = k * 2 * math.pi / 22; cx, cy = x + 58 * s * math.cos(a), y + 58 * s * math.sin(a)
        g += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{14*s:.1f}" ry="{6*s:.1f}" transform="rotate({math.degrees(a)+60:.0f} {cx:.1f} {cy:.1f})" fill="{INK}"/>'
    for k in range(0, 22, 4):
        a = k * 2 * math.pi / 22 + 0.15
        g += f'<circle cx="{x+58*s*math.cos(a):.1f}" cy="{y+58*s*math.sin(a):.1f}" r="{7*s:.1f}" fill="{INK}" stroke="{FAB}" stroke-width="{1.5*s:.1f}"/>'
    g += f'<path d="M{x-14*s:.1f} {y+56*s:.1f} L{x-30*s:.1f} {y+100*s:.1f} L{x-14*s:.1f} {y+92*s:.1f} L{x-4*s:.1f} {y+62*s:.1f} Z M{x+14*s:.1f} {y+56*s:.1f} L{x+30*s:.1f} {y+100*s:.1f} L{x+14*s:.1f} {y+92*s:.1f} L{x+4*s:.1f} {y+62*s:.1f} Z" fill="{INK}"/>'
    return g + f'<circle cx="{x:.1f}" cy="{y+58*s:.1f}" r="{9*s:.1f}" fill="{INK}"/>' + skull(x, y, 0.4 * s)
def death_grip(x, y, s=1):
    g = f'<line x1="{x-120*s:.1f}" y1="{y-20*s:.1f}" x2="{x+120*s:.1f}" y2="{y-20*s:.1f}" stroke="{INK}" stroke-width="{10*s:.1f}" stroke-linecap="round"/>'
    g += bone(x - 6 * s, y + 80 * s, x - 6 * s, y + 20 * s, 7 * s) + bone(x + 8 * s, y + 80 * s, x + 8 * s, y + 20 * s, 7 * s)
    g += ''.join(f'<circle cx="{x+u*s:.1f}" cy="{y+12*s:.1f}" r="{6*s:.1f}" fill="{INK}"/>' for u in (-14, -4, 6, 16))
    for i, u in enumerate((-22, -8, 6, 20)):
        g += bone(x + u * s, y + 4 * s, x + (u - 2) * s, y - 14 * s, 5 * s) + f'<path d="M{x+(u-2)*s:.1f} {y-14*s:.1f} q{-4*s:.1f} {-16*s:.1f} {8*s:.1f} {-14*s:.1f}" stroke="{INK}" stroke-width="{5*s:.1f}" fill="none" stroke-linecap="round"/>'
    g += bone(x + 26 * s, y + 16 * s, x + 40 * s, y - 8 * s, 5 * s)
    for d in (-1, 1):
        g += f'<rect x="{x+d*96*s-(16*s if d<0 else 0):.1f}" y="{y-60*s:.1f}" width="{16*s:.1f}" height="{80*s:.1f}" rx="{3*s:.1f}" fill="{INK}"/>'
    return g
def skull_flies(x, y, s=1):
    return rot_skull(x, y, s) + flies(x, y - 10 * s, s, n=5, spread=95)
def blood_drips(x, y, w, seed=0, size=1.0):
    g = ''
    k = 0
    for i in range(int(w // 18)):
        if (i * 7 + seed) % 3 == 0: continue
        xx = x - w / 2 + 9 + i * 18 + ((i * 5 + seed) % 7) - 3
        L = (10 + ((i * 13 + seed * 3) % 5) * 7) * size
        g += f'<path d="M{xx-3*size:.1f} {y:.1f} L{xx-2*size:.1f} {y+L:.1f} Q{xx:.1f} {y+L+7*size:.1f} {xx+2*size:.1f} {y+L:.1f} L{xx+3*size:.1f} {y:.1f} Z" fill="{INK}"/><circle cx="{xx:.1f}" cy="{y+L+1*size:.1f}" r="{3.2*size:.1f}" fill="{INK}"/>'
    return f'<rect x="{x-w/2:.1f}" y="{y-2:.1f}" width="{w:.1f}" height="4" fill="{INK}"/>' + g
ICONS = {k: globals()[k] for k in (
    "skull figure figures2 barbell dumbbell kettlebell plate coffin tombstone ghost battery heart brain coffee clock stopwatch "
    "moon candle hourglass rose flower moth raven eye bones bat bolt flame bottle anchor rack chain sun web cloud checklist none hand_skel "
    "toe_tag body_bag morgue_drawer y_incision autopsy_report maggots flies rot_skull rot_lifter anatomical_heart ekg flatline flayed_figure open_grave reaper obituary wreath death_grip skull_flies").split()}

# ---------------- type helpers ----------------
KEEP = {"PR", "A.M.", "A.M", "LB", "LBS", "ATG", "988"}
def sentence(t):
    out = []
    for i, w in enumerate(t.split()):
        core = w.strip(".,:;?!()'\"")
        if core in KEEP or core.isdigit(): out.append(w)
        elif core.upper() in ("I", "I'M", "I'LL", "I'VE"): out.append(w.upper()[0] + w.lower()[1:])
        else: out.append(w.capitalize() if i == 0 else w.lower())
    return " ".join(out)
def stack(lines, font, x, y, width, maxsize, upper=True):
    out = ''; yy = y; asc = 0.92 if font == "osw" else 0.78
    for ln in lines:
        t = ln.upper() if upper else sentence(ln)
        fs = fitsize(t, font, width, maxsize)
        yy += fs * asc
        out += tpath(t, font, fs, x, yy)
        yy += fs * 0.22
    return out, yy
def banner(x, y, w, text):
    h = 30
    g = (f'<path d="M{x-w/2-38:.1f} {y-8} L{x-w/2-10:.1f} {y-8} L{x-w/2-10:.1f} {y+20} L{x-w/2-38:.1f} {y+20} L{x-w/2-27:.1f} {y+6} Z '
         f'M{x+w/2+38:.1f} {y-8} L{x+w/2+10:.1f} {y-8} L{x+w/2+10:.1f} {y+20} L{x+w/2+38:.1f} {y+20} L{x+w/2+27:.1f} {y+6} Z" fill="{INK}"/>'
         f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h}" fill="{INK}"/>'
         f'<path d="M{x-w/2:.1f} {y+h/2} L{x-w/2-10:.1f} {y+20} M{x+w/2:.1f} {y+h/2} L{x+w/2+10:.1f} {y+20}" stroke="{FAB}" stroke-width="2"/>')
    fs = fitsize(text, "type", w - 16, 18)
    return g + tpath(text, "type", fs, x, y + fs * 0.33, fill=FAB)
def thorns(x, y, w):
    pts = " ".join(f"{x-w/2+i:.1f},{y+3*math.sin(i/7):.1f}" for i in range(0, int(w) + 1, 3))
    g = f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    for i in range(6, int(w), 16):
        xx = x - w / 2 + i; yy = y + 3 * math.sin(i / 7); d = -1 if (i // 16) % 2 else 1
        g += f'<path d="M{xx-3:.1f} {yy:.1f} L{xx+1:.1f} {yy+d*9:.1f} L{xx+4:.1f} {yy:.1f} Z" fill="{INK}"/>'
    return g
ORN = ["moth", "raven", "candle", "rose", "skull", "hourglass", "bat", "moon"]

# ---------------- layouts ----------------
def layout(num, d):
    lines, sub, ic, place = d["lines"], d.get("sub", ""), d.get("icon", "none"), d["place"]
    args = d.get("args", {}); sc = d.get("s", 0.85)
    view = "back" if place in ("back", "hood") else "front"
    orn = ORN[num % len(ORN)]
    a = ''
    if place == "front":
        if ic == "none":
            a += ICONS[orn](300, 226, 0.4)
            t, yy = stack(lines, "osw", 300, 268, 270, min(52, 150 / len(lines))); a += t
            a += thorns(300, yy + 8, 200)
            if sub: a += tpath(sub, "type", fitsize(sub, "type", 270, 17), 300, yy + 34)
        else:
            a += ICONS[ic](300, 240, sc * 0.88, **args) if ic in ("figure", "figures2") else ICONS[ic](300, 258, sc * 1.0, **args)
            first, rest = sentence(lines[0]), lines[1:]
            fs = fitsize(first, "black", 270, 38 if rest else 44)
            a += tpath(first, "black", fs, 300, 340 + fs * 0.75)
            if d.get("drip"): a += blood_drips(300, 340 + fs * 0.82, min(260, measure(first, "black", fs)), num, 0.5)
            yy = 340 + fs * 0.95 + (26 if d.get("drip") else 0)
            if rest:
                t, yy = stack(rest, "pirata", 300, yy, 270, 30, upper=False); a += t
            if sub: a += tpath(sub, "type", fitsize(sub, "type", 260, 15), 300, yy + 18)
    elif place in ("back", "hood"):
        head, rest = sentence(lines[0]), lines[1:]
        if place == "hood":
            hv = d.get("hood", "")
            a += f'<path d="M244 120 Q300 98 356 120 L356 142 Q300 122 244 142 Z" fill="{INK}"/>' + tpath(hv, "osw", fitsize(hv, "osw", 90, 15), 300, 137, fill=FAB)
        if ic == "none" and rest:
            a += arctext(head, "black", fitsize(head, "black", 230, 34), 300, 410, 200)
            t, yy = stack(rest, "osw", 300, 236, 290, min(58, 220 / len(rest))); a += t
            a += thorns(300, yy + 12, 240) + skull(300, yy + 70, 0.4)
            if sub: a += banner(300, min(yy + 124, 530), 250, sub)
        else:
            if fitsize(head, "black", 240, 36) >= 24:
                a += arctext(head, "black", fitsize(head, "black", 240, 36), 300, 410, 200); yy = 232
            else:
                fs = fitsize(head, "black", 290, 34); a += tpath(head, "black", fs, 300, 226); yy = 238
            icon_name = ic if ic != "none" else orn
            if ic == "checklist":
                a += checklist(300, yy + 30, 1, **args); yy += 190
            else:
                a += ICONS[icon_name](300, yy + (112 if ic == "reaper" else 78), (sc * 0.95) if ic != "none" else 0.72, **(args if ic != "none" else {}))
                yy += 168 + (26 if ic == "reaper" else 0)
            if rest:
                t, yy = stack(rest, "pirata", 300, yy, 290, 36, upper=False); a += t
                if d.get("drip"): a += blood_drips(300, yy + 4, 250, num, 0.8); yy += 22
            if sub: a += banner(300, min(yy + 26, 532), 250, sub)
    elif place == "chest":
        cx = 382; joined = " ".join(lines)
        a += ICONS[ic if ic != "none" else orn](cx, 226, d.get("s", 0.4) if ic != "none" else 0.32, **(args if ic != "none" else {}))
        head = sentence(joined if len(joined) < 26 else lines[0])
        a += tpath(head, "black", fitsize(head, "black", 118, 24), cx, 286)
        if len(joined) >= 26 and len(lines) > 1:
            r = sentence(" ".join(lines[1:])); a += tpath(r, "pirata", fitsize(r, "pirata", 118, 16), cx, 304)
        if sub: a += tpath(sub, "type", fitsize(sub, "type", 120, 11), cx, 322)
    elif place == "sleeve":
        txt = " ".join(lines); fs = fitsize(txt, "pirata", 270, 22)
        a += f'<g transform="translate(140 206) rotate(105.6)">{tpath(txt, "pirata", fs, 0, 0, anchor="start")}</g>'
        if sub: a += f'<g transform="translate(460 206) rotate(74.4)">{tpath(sub, "type", fitsize(sub, "type", 270, 14), 0, 0, anchor="start")}</g>'
        a += ICONS[ic if ic != "none" else orn](382, 240, 0.38)
    elif place == "pocket":
        a += ICONS[ic if ic != "none" else orn](382, 236, 0.36, **(args if ic != "none" else {}))
        t, yy = stack(lines, "osw", 300, 444, 190, 26); a += t
        if sub: a += tpath(sub, "type", fitsize(sub, "type", 200, 13), 300, yy + 14)
    return view, a

PLACE = {"front": "front center", "back": "back", "chest": "left chest", "sleeve": "sleeve", "pocket": "pocket + chest", "hood": "hood + back"}
def fname(num, d): return (f"{num:02d}" if num < 100 else f"{num:03d}") + "-" + d["slug"] + ".svg"
def color_for(num):
    return PALETTE[(num * 7) % len(PALETTE)]
def render(num, d):
    global INK, FAB
    cname, FAB, INK = color_for(num)
    view, art = layout(num, d)
    full = " ".join(d["lines"]).strip()
    title = full if len(full) <= 38 else full[:36].rsplit(" ", 1)[0] + "…"
    title = title[0] + title[1:].lower()
    light_ink = sum(int(INK[i:i+2], 16) for i in (1, 3, 5)) > 450
    method = ("Light ink: resist print, discharge (reactive dye) or embroidery" if light_ink
              else "Dark ink: natural-dye paste print")
    if RED in art: method += " + red embroidery"
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 720" width="600" height="720" font-family="Arial, Helvetica, sans-serif">
{DEFS}
<rect width="600" height="720" fill="{PAGE}"/>
{hoodie(view)}
<g filter="url(#grunge)">{art}</g>
<text x="300" y="636" text-anchor="middle" font-size="16" font-weight="bold" fill="#1a1a1a">{num:02d}. {E(title)} ({PLACE[d["place"]]})</text>
<text x="300" y="657" text-anchor="middle" font-size="12" fill="#444">{E(d["note"])}</text>
<text x="300" y="677" text-anchor="middle" font-size="11" fill="#555">Hoodie: {E(cname)}. {E(method)}.</text>
<text x="300" y="702" text-anchor="middle" font-size="10" fill="#777">Placement sketch only. Redraw in your own hand before use.</text>
</svg>'''
    open(os.path.join(OUT, fname(num, d)), "w").write(s)
    return fname(num, d)

def all_designs():
    sys.path.insert(0, HERE)
    from designs_data import FIRST, DESIGNS
    return FIRST + DESIGNS

if __name__ == "__main__":
    D = all_designs()
    only = {int(a) for a in sys.argv[1:]}
    names = [render(i + 1, d) for i, d in enumerate(D) if not only or i + 1 in only]
    print(len(names), names[0], names[-1])

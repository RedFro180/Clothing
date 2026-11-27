"""Variety for the line-art redraws: per-design font, sky and tree type, so the scenes don't all look the same.
Fonts (tools/fonts): Caveat, Amatic SC, Shadows Into Light, Indie Flower (SIL OFL); Permanent Marker, Rock Salt (Apache 2.0)."""
import math, random
import svgs_dark as sd
import svgs_night as nt
from svgs_night import jl, pl, pine, dead_tree, stars, moon, clouds

sd.FILES.update({"hand": "caveat-latin-600-normal.woff2", "marker": "permanent-marker-latin-400-normal.woff2",
                 "amatic": "amatic-sc-latin-700-normal.woff2", "shadows": "shadows-into-light-latin-400-normal.woff2",
                 "rocksalt": "rock-salt-latin-400-normal.woff2", "indie": "indie-flower-latin-400-normal.woff2"})
FONTS = ["hand", "marker", "amatic", "shadows", "rocksalt", "indie"]
FONT_SIZE = {"hand": 1.0, "marker": 0.82, "amatic": 1.25, "shadows": 0.95, "rocksalt": 0.62, "indie": 0.88}   # size factor (Rock Salt runs wide)
SKIES = ["none", "none", "night", "crescent", "milky", "sun", "dusk"]
TREES = ["pine", "leafy", "birch", "cypress", "dead", "mixed"]
OVERRIDE = {}          # filled by redo_specs: OVERRIDE[n] = dict(sky=..., trees=..., font=...)

def variant(num):
    r = random.Random(num * 101 + 7)
    v = dict(font=FONTS[num % len(FONTS)], sky=r.choice(SKIES), trees=r.choice(TREES), scale=r.uniform(1.25, 1.5), side=1 if num % 2 else -1)
    v.update(OVERRIDE.get(num, {}))
    return v

# ---------- trees ----------
def leafy(x, base, h, r, w=2.2):                # round leafy tree with a scalloped (bumpy) canopy edge, no inner marks
    g = jl([(x - 3, base), (x - 2, base - h * 0.45)], r, w * 1.4, 0.5) + jl([(x + 3, base), (x + 2, base - h * 0.45)], r, w * 1.2, 0.5)
    cy, rx, ry, n = base - h * 0.68, h * 0.32, h * 0.3, 11
    d = ""
    for i in range(n):
        a0, a1 = i / n * 2 * math.pi, (i + 1) / n * 2 * math.pi; am = (a0 + a1) / 2
        p0 = (x + rx * math.cos(a0), cy + ry * math.sin(a0)); p1 = (x + rx * math.cos(a1), cy + ry * math.sin(a1))
        c = (x + rx * 1.22 * math.cos(am), cy + ry * 1.22 * math.sin(am))
        d += (f"M{p0[0]:.1f} {p0[1]:.1f}" if i == 0 else "") + f" Q{c[0]:.1f} {c[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}"
    g += f'<path d="{d} Z" fill="{nt.B()}" stroke="{nt.I()}" stroke-width="{w}"/>'
    return g + jl([(x - 2, base - h * 0.45), (x - 12, base - h * 0.58)], r, 1.6) + jl([(x + 2, base - h * 0.5), (x + 12, base - h * 0.62)], r, 1.6)
def birch(x, base, h, r):
    g = jl([(x - 3, base), (x - 2, base - h)], r, 1.8, 0.6) + jl([(x + 3, base), (x + 2, base - h)], r, 1.8, 0.6)
    g += ''.join(pl([(x - 3, base - v), (x + (1 if i % 2 else -1), base - v - 2)], 2) for i, v in enumerate(range(12, int(h), 14)))
    for v, d in ((0.55, -1), (0.7, 1), (0.82, -1), (0.92, 1)):
        g += jl([(x, base - h * v), (x + d * 18, base - h * v - 10)], r, 1.2)
        g += ''.join(nt.ell(x + d * (10 + k * 6), base - h * v - 8 - k * 3, 3.2, 2, 1) if hasattr(nt, "ell") else
                     f'<ellipse cx="{x + d * (10 + k * 6):.1f}" cy="{base - h * v - 8 - k * 3:.1f}" rx="3.2" ry="2" fill="none" stroke="{nt.I()}" stroke-width="1"/>' for k in range(3))
    return g
def cypress(x, base, h, r):
    pts = [(x - 2, base), (x - 12, base - h * 0.35), (x - 9, base - h * 0.75), (x, base - h), (x + 9, base - h * 0.75), (x + 12, base - h * 0.35), (x + 2, base)]
    g = jl(pts, r, 2, 0.8, 5)
    return g + ''.join(jl([(x - 6 + (i % 2) * 6, base - h * t), (x + (i % 2) * 4, base - h * t - 10)], r, 1.1, 0.4, 3) for i, t in enumerate((0.2, 0.32, 0.44, 0.56, 0.68, 0.8)))
def tree(kind, x, base, h, r, i=0):
    if kind == "mixed": kind = ("pine", "leafy", "birch", "cypress")[i % 4]
    if kind == "leafy": return leafy(x, base, h * 0.9, r)
    if kind == "birch": return birch(x, base, h, r)
    if kind == "cypress": return cypress(x, base, h, r)
    if kind == "dead": return dead_tree(r, x, base, h * 0.85)
    return pine(x, base, h, r)

# ---------- skies (scene y ~30-150) ----------
def crescent(x, y, rad):
    return (f'<path d="M{x} {y-rad} A{rad} {rad} 0 1 0 {x} {y+rad} A{rad*0.78:.1f} {rad*0.95:.1f} 0 1 1 {x} {y-rad} Z" fill="{nt.I()}"/>')
def sky(kind, r, side):
    sx = 96 * side
    if kind == "night": return stars(r, 30, -150, 150, 34, 150) + moon(sx, 64, 18, r) + clouds(r, sx - 20, 92, 90)
    if kind == "crescent": return stars(r, 24, -150, 150, 34, 150) + crescent(sx, 62, 16)
    if kind == "milky":
        g = stars(r, 26, -150, 150, 34, 150)
        return g + ''.join(nt.dot(t * 300 - 150 + r.uniform(-14, 14), 40 + t * 80 + r.uniform(-14, 14), r.choice((0.6, 0.8, 1.0))) for t in [r.random() for _ in range(140)])
    if kind == "sun":
        g = f'<circle cx="{sx}" cy="62" r="14" fill="none" stroke="{nt.I()}" stroke-width="2.2"/>'
        g += ''.join(pl([(sx + 20 * math.cos(a), 62 + 20 * math.sin(a)), (sx + 28 * math.cos(a), 62 + 28 * math.sin(a))], 1.8) for a in [i * math.pi / 6 for i in range(12)])
        return g + ''.join(pl([(u - 6, v), (u, v + 4), (u + 6, v)], 1.4) for u, v in ((-60 * side, 70), (-40 * side, 60), (-20 * side, 76)))
    if kind == "dusk":
        g = f'<path d="M{sx-30} 140 A30 30 0 0 1 {sx+30} 140" fill="none" stroke="{nt.I()}" stroke-width="2"/>'
        return g + ''.join(jl([(-150 + k * 40, 100 + k * 8), (40 + k * 30, 100 + k * 8)], r, 1.2, 0.6, 10) for k in range(3))
    return ""

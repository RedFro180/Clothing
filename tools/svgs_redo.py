"""Night-style REDRAWS of sketches 01-207 (originals in designs/sketches stay untouched).
Everything is redrawn in the night line-art style of 208-219: shaky single-ink pen outlines, plain moon, stars,
night landscape, stick figure, handwritten caption. No filled icons from the old style.
Each design's subject (coffin, toe tag, skull, reaper, barbell, heart...) is drawn as pen line art in the scene.
Figures are never near a drop. Same hoodie color as the original.
Run: python3 tools/svgs_redo.py [numbers...]   -> designs/sketches-night/NNN-slug.svg"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import svgs_dark as sd
import svgs_night as nt
from svgs_night import jitter, jl, pl, pine, forest, mountains, river, in_river, clouds, tufts, ground, stars, head, moon
from svgs_night import sit_lean, sit_hug, kneel, lie, walk, grave_mound, cross, coffin_side, dead_tree

OUT = os.path.normpath(os.path.join(HERE, "..", "designs", "sketches-night"))
I, B = nt.I, nt.B
G = 236   # ground line in scene units

# ---------- pen-outline helpers ----------
def shape(r, pts, w=2.3, fill=True, amt=0.7):
    p = jitter(pts + [pts[0]], r, amt, 5)
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p) + " Z"
    return f'<path d="{d}" fill="{B() if fill else "none"}" stroke="{I()}" stroke-width="{w}" stroke-linejoin="round"/>'
def ell(x, y, rx, ry, w=2.2, fill=True):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{B() if fill else "none"}" stroke="{I()}" stroke-width="{w}"/>'
def hand(t, size, x, y): return sd.tpath(t, "hand", size, x, y) if t else ""
def rect_pts(x, y, w, h): return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

# ---------- figures ----------
def stand(x, y, k=1):
    return (head(x, y - 42 * k, 7.5 * k) + pl([(x, y - 34 * k), (x, y - 16 * k)], 2.6 * k) + pl([(x - 6 * k, y), (x, y - 16 * k), (x + 6 * k, y)], 2.6 * k)
            + pl([(x - 8 * k, y - 18 * k), (x, y - 30 * k), (x + 8 * k, y - 18 * k)], 2.2 * k))
def barbell_l(x, y, w):
    g = pl([(x - w, y), (x + w, y)], 2.6)
    for d in (-1, 1):
        for off, h in ((4, 26), (12, 18)):
            xx = x + d * (w - off)
            g += f'<rect x="{xx-3:.1f}" y="{y-h/2:.1f}" width="6" height="{h}" rx="1.5" fill="{B()}" stroke="{I()}" stroke-width="1.8"/>'
    return g
def press(x, y):
    return (head(x, y - 44) + pl([(x, y - 36), (x, y - 16)], 2.6) + pl([(x - 10, y), (x, y - 16), (x + 10, y)], 2.6)
            + pl([(x - 3, y - 32), (x - 16, y - 46), (x - 18, y - 64)], 2.3) + pl([(x + 3, y - 32), (x + 16, y - 46), (x + 18, y - 64)], 2.3)) + barbell_l(x, y - 64, 48)
def deadlift(x, y):
    return (head(x + 14, y - 34) + pl([(x + 8, y - 28), (x - 10, y - 18)], 2.6) + pl([(x - 10, y - 18), (x - 6, y - 8), (x - 12, y)], 2.6)
            + pl([(x - 10, y - 18), (x + 2, y - 10), (x - 2, y)], 2.6) + pl([(x + 6, y - 26), (x + 6, y - 12)], 2.3)) + barbell_l(x, y - 12, 48)

# ---------- line-art subjects (anchor = ground point x, y) ----------
def stone(r, x, y):
    return shape(r, [(x - 34, y), (x - 30, y - 12), (x - 10, y - 18), (x + 18, y - 16), (x + 34, y - 8), (x + 36, y)])
def rain_cloud(r, x, y):
    g = shape(r, [(x - 30, y), (x - 34, y - 12), (x - 22, y - 22), (x - 6, y - 24), (x + 6, y - 32), (x + 24, y - 28), (x + 34, y - 14), (x + 30, y)], 2)
    return g + ''.join(jl([(x + u, y + 6), (x + u - 4, y + 18)], r, 1.6, 0.3) for u in (-20, -8, 4, 16, 26))
def skull_l(r, x, y, k=1):
    g = shape(r, [(x - 22 * k, y + 4 * k), (x - 24 * k, y - 14 * k), (x - 14 * k, y - 26 * k), (x, y - 29 * k), (x + 14 * k, y - 26 * k), (x + 24 * k, y - 14 * k),
                   (x + 22 * k, y + 4 * k), (x + 14 * k, y + 8 * k), (x + 13 * k, y + 18 * k), (x - 13 * k, y + 18 * k), (x - 14 * k, y + 8 * k)], max(1.4, 2.2 * k), amt=0.4 * k)
    g += ell(x - 9 * k, y - 4 * k, 6 * k, 6.5 * k, max(1.2, 2 * k)) + ell(x + 9 * k, y - 4 * k, 6 * k, 6.5 * k, max(1.2, 2 * k))
    g += pl([(x - 2 * k, y + 8 * k), (x, y + 3 * k), (x + 2 * k, y + 8 * k)], max(1, 1.6 * k))
    return g + ''.join(pl([(x + u * k, y + 12 * k), (x + u * k, y + 18 * k)], max(.9, 1.3 * k)) for u in (-8, -4, 0, 4, 8))
def skeleton_l(r, x, y, pose="stand"):
    g = skull_l(r, x, y - 46, 0.34) + pl([(x, y - 38), (x, y - 14)], 2.2)
    g += ''.join(pl([(x - 7, y + v), (x, y + v - 2), (x + 7, y + v)], 1.4) for v in (-32, -27, -22))
    if pose == "sit": g += pl([(x, y - 14), (x + 14, y - 12), (x + 16, y)], 2.2) + pl([(x, y - 14), (x + 10, y - 10), (x + 10, y)], 2.2)
    else: g += pl([(x - 6, y), (x, y - 14), (x + 6, y)], 2.2)
    return g + pl([(x - 9, y - 16), (x, y - 30), (x + 9, y - 16)], 1.8)
def coffin_up(r, x, y, k=1):
    g = shape(r, [(x - 14 * k, y), (x - 22 * k, y - 50 * k), (x - 14 * k, y - 76 * k), (x + 14 * k, y - 76 * k), (x + 22 * k, y - 50 * k), (x + 14 * k, y)])
    return g + jl([(x, y - 62 * k), (x, y - 30 * k)], r, 2) + jl([(x - 9 * k, y - 52 * k), (x + 9 * k, y - 52 * k)], r, 2)
def grave_open(r, x, y):
    g = shape(r, [(x - 50, y - 2), (x + 34, y - 2), (x + 44, y - 14), (x - 40, y - 14)])
    g += f'<path d="M{x-38} {y-6} L{x+34} {y-6} L{x+40} {y-12} L{x-32} {y-12} Z" fill="{I()}" opacity=".35"/>'
    g += jl([(x + 46, y), (x + 60, y - 18), (x + 78, y - 22), (x + 92, y - 8), (x + 96, y)], r, 2.3)
    g += jl([(x + 76, y - 20), (x + 92, y - 64)], r, 2.6) + jl([(x + 88, y - 66), (x + 98, y - 62)], r, 3)
    return g + shape(r, [(x + 70, y - 24), (x + 80, y - 20), (x + 76, y - 6), (x + 68, y - 8)])
def tomb(r, x, y, k=1, text="RIP"):
    g = shape(r, [(x - 22 * k, y), (x - 22 * k, y - 40 * k), (x - 16 * k, y - 52 * k), (x, y - 56 * k), (x + 16 * k, y - 52 * k), (x + 22 * k, y - 40 * k), (x + 22 * k, y)])
    g += hand(text, 14 * k, x, y - 30 * k) + (jl([(x - 12 * k, y - 18 * k), (x + 12 * k, y - 18 * k)], r, 1.4) if text else "")
    return g + jl([(x - 30 * k, y), (x + 30 * k, y)], r, 2)
def gurney(r, x, y, tag=True):
    g = jl([(x - 56, y), (x - 50, y - 26)], r, 2.2) + jl([(x + 56, y), (x + 50, y - 26)], r, 2.2) + jl([(x - 62, y - 26), (x + 62, y - 26)], r, 2.6)
    g += shape(r, [(x - 56, y - 28), (x - 50, y - 44), (x - 34, y - 48), (x - 20, y - 40), (x + 10, y - 42), (x + 30, y - 38), (x + 48, y - 40), (x + 56, y - 28)])
    g += ''.join(ell(x + 60, y - 34 + dd, 4, 6) for dd in (-4, 4))
    if tag:
        g += jl([(x + 64, y - 34), (x + 72, y - 18)], r, 1.4) + shape(r, [(x + 66, y - 18), (x + 86, y - 24), (x + 90, y - 10), (x + 70, y - 4)], 1.8) + ell(x + 70, y - 14, 1.6, 1.6, 1)
    return g
def drawer(r, x, y):
    g = shape(r, rect_pts(x - 90, y - 92, 76, 92))
    for i in range(3):
        for j in range(2):
            g += shape(r, rect_pts(x - 84 + j * 36, y - 86 + i * 30, 30, 24), 1.6) + jl([(x - 76 + j * 36, y - 74 + i * 30), (x - 64 + j * 36, y - 74 + i * 30)], r, 1.6)
    g += shape(r, rect_pts(x - 14, y - 34, 110, 10)) + jl([(x - 8, y - 24), (x - 8, y)], r, 1.6) + jl([(x + 88, y - 24), (x + 88, y)], r, 1.6)
    return g + shape(r, [(x - 12, y - 34), (x + 4, y - 50), (x + 40, y - 46), (x + 70, y - 52), (x + 94, y - 34)])
def bodybag(r, x, y):
    g = shape(r, [(x - 70, y), (x - 76, y - 12), (x - 60, y - 24), (x + 60, y - 24), (x + 76, y - 12), (x + 70, y)])
    g += jl([(x - 50, y - 12), (x + 60, y - 12)], r, 1.4) + ''.join(pl([(x + u, y - 15), (x + u, y - 9)], 1) for u in range(-46, 60, 6))
    return g + shape(r, rect_pts(x + 60, y - 16, 8, 8), 1.4)
def reaper_l(r, x, y, k=1):
    g = shape(r, [(x - 30 * k, y), (x - 22 * k, y - 50 * k), (x - 20 * k, y - 80 * k), (x - 10 * k, y - 96 * k), (x + 6 * k, y - 98 * k), (x + 20 * k, y - 84 * k),
                   (x + 22 * k, y - 50 * k), (x + 30 * k, y)])
    g += f'<path d="M{x-10*k:.1f} {y-80*k:.1f} Q{x:.1f} {y-92*k:.1f} {x+10*k:.1f} {y-80*k:.1f} L{x+8*k:.1f} {y-66*k:.1f} Q{x:.1f} {y-62*k:.1f} {x-8*k:.1f} {y-66*k:.1f} Z" fill="{I()}"/>'
    g += jl([(x + 34 * k, y), (x + 34 * k, y - 120 * k)], r, 2.2)
    g += shape(r, [(x + 34 * k, y - 120 * k), (x + 4 * k, y - 126 * k), (x - 24 * k, y - 112 * k), (x + 4 * k, y - 118 * k), (x + 34 * k, y - 112 * k)], 1.8)
    return g + jl([(x - 8 * k, y - 40 * k), (x + 34 * k, y - 56 * k)], r, 1.8)
def heart_l(r, x, y, k=1):
    g = shape(r, [(x - 4 * k, y - 50 * k), (x - 28 * k, y - 48 * k), (x - 34 * k, y - 28 * k), (x - 26 * k, y - 8 * k), (x - 6 * k, y + 8 * k), (x + 4 * k, y + 16 * k),
                   (x + 14 * k, y + 2 * k), (x + 32 * k, y - 16 * k), (x + 32 * k, y - 38 * k), (x + 18 * k, y - 50 * k)])
    for u, h in ((-4, 22), (8, 26), (20, 18)):
        g += shape(r, rect_pts(x + (u - 4) * k, y - (50 + h) * k, 8 * k, h * k + 2), 1.8)
    return g + jl([(x - 8 * k, y - 38 * k), (x - 2 * k, y - 18 * k), (x - 8 * k, y)], r, 1.5) + jl([(x + 14 * k, y - 36 * k), (x + 20 * k, y - 16 * k)], r, 1.5)
def rack_l(r, x, y):
    g = jl([(x - 44, y), (x - 44, y - 104)], r, 2.6) + jl([(x + 44, y), (x + 44, y - 104)], r, 2.6) + jl([(x - 56, y), (x + 56, y)], r, 2.4)
    g += ''.join(pl([(x - 44, y + v), (x - 38, y + v)], 1.8) + pl([(x + 44, y + v), (x + 38, y + v)], 1.8) for v in (-80, -64, -48))
    return g
def candle_l(r, x, y):
    g = shape(r, [(x - 22, y), (x - 18, y - 12), (x + 18, y - 14), (x + 24, y)]) + shape(r, rect_pts(x - 7, y - 44, 14, 32))
    return g + f'<path d="M{x} {y-48} Q{x-7} {y-58} {x} {y-72} Q{x+7} {y-58} {x} {y-48} Z" fill="none" stroke="{I()}" stroke-width="2"/>' + pl([(x - 7, y - 40), (x - 9, y - 32)], 1.8)
def hourglass_l(r, x, y, k=1):
    g = jl([(x - 24 * k, y), (x + 24 * k, y)], r, 3) + jl([(x - 24 * k, y - 90 * k), (x + 24 * k, y - 90 * k)], r, 3)
    g += jl([(x - 20 * k, y - 2), (x - 20 * k, y - 88 * k)], r, 1.6) + jl([(x + 20 * k, y - 2), (x + 20 * k, y - 88 * k)], r, 1.6)
    g += shape(r, [(x - 15 * k, y - 86 * k), (x + 15 * k, y - 86 * k), (x + 2 * k, y - 46 * k), (x + 15 * k, y - 4 * k), (x - 15 * k, y - 4 * k), (x - 2 * k, y - 46 * k)], 1.8)
    return g + f'<path d="M{x-11*k:.1f} {y-6:.1f} Q{x:.1f} {y-24*k:.1f} {x+11*k:.1f} {y-6:.1f} Z" fill="{I()}"/>' + pl([(x, y - 46 * k), (x, y - 20 * k)], 1.2)
def clock_l(r, x, y):
    g = jl([(x, y), (x, y - 50)], r, 2.6) + ell(x, y - 74, 26, 26)
    g += ''.join(pl([(x + 22 * math.cos(a), y - 74 + 22 * math.sin(a)), (x + 18 * math.cos(a), y - 74 + 18 * math.sin(a))], 1.4) for a in [i * math.pi / 6 for i in range(12)])
    return g + pl([(x, y - 74), (x, y - 92)], 2) + pl([(x, y - 74), (x + 12, y - 74)], 2)
def rose_l(r, x, y):
    g = jl([(x, y), (x + 4, y - 40), (x + 18, y - 58)], r, 1.8) + jl([(x + 2, y - 22), (x - 10, y - 30)], r, 1.4)
    return g + shape(r, [(x + 12, y - 56), (x + 18, y - 68), (x + 28, y - 64), (x + 30, y - 52), (x + 22, y - 48)], 1.8)
def ghost_l(r, x, y):
    pts = [(x - 20, y)] + [(x - 20 + i * 8, y - (6 if i % 2 else 0)) for i in range(6)] + [(x + 20, y), (x + 20, y - 46), (x + 12, y - 60), (x, y - 64), (x - 12, y - 60), (x - 20, y - 46)]
    return shape(r, pts) + ell(x - 7, y - 44, 3, 5, 1.4, False) + ell(x + 7, y - 44, 3, 5, 1.4, False)
def sign_l(r, x, y, lines=()):
    g = jl([(x, y), (x, y - 40)], r, 2.6) + shape(r, rect_pts(x - 40, y - 100, 80, 60))
    return g + ''.join(hand(t[:16], 10, x, y - 84 + i * 13) for i, t in enumerate(lines[:4]))
def wreath_l(r, x, y):
    return tomb(r, x, y, 1.2, "") + ''.join(ell(x + 13 * math.cos(a), y - 36 + 13 * math.sin(a), 4, 2, 1.2) for a in [i * 0.52 for i in range(12)])
def bottle_l(r, x, y):
    g = shape(r, [(x - 22, y), (x - 18, y - 8), (x + 20, y - 8), (x + 26, y)])
    g += shape(r, [(x - 14, y - 8), (x - 14, y - 40), (x - 6, y - 48), (x - 6, y - 62), (x + 6, y - 62), (x + 6, y - 48), (x + 14, y - 40), (x + 14, y - 8)])
    return g + skull_l(r, x, y - 26, 0.32)
def table_l(r, x, y, n=2):
    g = jl([(x - 60, y - 34), (x + 60, y - 34)], r, 2.6) + jl([(x - 50, y - 34), (x - 50, y)], r, 2.2) + jl([(x + 50, y - 34), (x + 50, y)], r, 2.2)
    return g + ''.join(ell(x + u, y - 37, 16, 3) for u in ((-26, 26) if n == 2 else ()))
def jar_l(r, x, y):
    g = shape(r, [(x - 22, y), (x - 24, y - 56), (x - 18, y - 62), (x + 18, y - 62), (x + 24, y - 56), (x + 22, y)]) + shape(r, rect_pts(x - 20, y - 70, 40, 8), 1.8)
    return g + jl([(x - 12, y - 30), (x - 6, y - 40), (x + 2, y - 34), (x + 10, y - 42), (x + 14, y - 30), (x + 4, y - 22), (x - 8, y - 22), (x - 12, y - 30)], r, 1.6, 0.8, 3)
def scale_l(r, x, y):
    g = dead_tree(r, x - 40, y, 150) + jl([(x - 26, y - 100), (x + 10, y - 104)], r, 2) + jl([(x + 10, y - 104), (x + 10, y - 82)], r, 1.4)
    g += ell(x + 10, y - 74, 9, 9) + jl([(x + 10, y - 66), (x - 4, y - 46)], r, 1.2) + jl([(x + 10, y - 66), (x + 24, y - 46)], r, 1.2)
    return g + shape(r, [(x - 6, y - 46), (x + 26, y - 46), (x + 20, y - 38), (x, y - 38)], 1.8) + heart_l(r, x + 10, y - 50, 0.22)
def crem_l(r, x, y):
    g = shape(r, rect_pts(x - 60, y - 40, 120, 40)) + shape(r, rect_pts(x + 20, y - 92, 20, 52))
    g += ''.join(shape(r, rect_pts(x - 50 + i * 22, y - 30, 14, 12), 1.4) for i in range(3))
    return g + jl([(x + 30, y - 96), (x + 22, y - 112), (x + 34, y - 126), (x + 20, y - 142), (x + 40, y - 156)], r, 2, 1.6, 4)
def urn_l(r, x, y, k=1):
    g = shape(r, [(x - 12 * k, y), (x - 18 * k, y - 22 * k), (x - 14 * k, y - 40 * k), (x - 8 * k, y - 46 * k), (x + 8 * k, y - 46 * k), (x + 14 * k, y - 40 * k), (x + 18 * k, y - 22 * k), (x + 12 * k, y)])
    return g + shape(r, rect_pts(x - 9 * k, y - 54 * k, 18 * k, 8 * k), 1.6) + jl([(x - 14 * k, y - 26 * k), (x + 14 * k, y - 26 * k)], r, 1.2)
def chair_l(r, x, y):
    g = jl([(x - 14, y), (x - 14, y - 70)], r, 2.4) + jl([(x + 14, y), (x + 14, y - 30)], r, 2.4) + jl([(x - 20, y - 30), (x + 20, y - 30)], r, 2.6)
    return g + shape(r, [(x - 16, y - 70), (x - 6, y - 66), (x - 8, y - 38), (x - 18, y - 40)], 1.6)
def phone_l(r, x, y):
    g = table_l(r, x, y, 0) + shape(r, rect_pts(x - 22, y - 52, 44, 18)) + shape(r, [(x - 26, y - 54), (x - 20, y - 62), (x + 20, y - 62), (x + 26, y - 54)])
    return g + ell(x, y - 43, 6, 6, 1.4)
def bed_l(r, x, y):
    g = jl([(x - 80, y), (x - 80, y - 46)], r, 2.6) + jl([(x + 80, y), (x + 80, y - 30)], r, 2.6)
    g += shape(r, rect_pts(x - 80, y - 30, 160, 14)) + shape(r, [(x - 74, y - 30), (x - 70, y - 40), (x - 46, y - 40), (x - 44, y - 30)], 1.8)
    return g + head(x - 56, y - 40, 7) + shape(r, [(x - 44, y - 30), (x - 40, y - 42), (x + 60, y - 40), (x + 74, y - 30)], 1.8)
def trap_l(r, x, y):
    g = jl([(x - 50, y), (x + 50, y)], r, 2.6)
    for d in (-1, 1):
        g += jl([(x + d * 48, y), (x + d * 40, y - 30), (x + d * 12, y - 46)], r, 2.4)
        g += ''.join(pl([(x + d * u, y - v), (x + d * (u - 6), y - v - 2), (x + d * (u - 2), y - v + 6)], 1.4) for u, v in ((42, 14), (36, 30), (22, 40)))
    return g + heart_l(r, x, y - 8, 0.5)
def hearse_l(r, x, y):
    g = shape(r, [(x - 80, y - 8), (x - 80, y - 26), (x - 58, y - 30), (x - 48, y - 52), (x + 64, y - 52), (x + 80, y - 30), (x + 80, y - 8)])
    g += shape(r, rect_pts(x - 40, y - 46, 40, 16), 1.6) + shape(r, rect_pts(x + 8, y - 46, 52, 16), 1.6)
    return g + ell(x - 52, y - 8, 11, 11) + ell(x + 52, y - 8, 11, 11) + ell(x - 52, y - 8, 3, 3, 1.4) + ell(x + 52, y - 8, 3, 3, 1.4)
def bones_pile(r, x, y):
    g = ''.join(skull_l(r, x + u, y - v, 0.42) for u, v in ((-30, 10), (0, 12), (30, 10), (-15, 28), (15, 28), (0, 44)))
    return g + ''.join(jl([(x + a, y - 2), (x + b, y - 8)], r, 2.2) for a, b in ((-60, -40), (40, 62)))
def shrooms_l(r, x, y):
    g = skull_l(r, x, y - 12, 0.8)
    for u, h, w in ((-26, 30, 12), (24, 38, 14), (4, 52, 10)):
        g += jl([(x + u, y - 20), (x + u, y - h)], r, 2) + shape(r, [(x + u - w, y - h), (x + u, y - h - w * 0.9), (x + u + w, y - h)], 1.8)
    return g
def roots_skull(r, x, y):
    g = skull_l(r, x, y - 18, 0.9) + jl([(x, y - 44), (x - 2, y - 120)], r, 3)
    for v, d in ((-100, -1), (-86, 1), (-110, 1), (-70, -1)):
        g += jl([(x - 1, y + v), (x + d * 30, y + v - 16)], r, 1.8)
    return g
def crows_tree(r, x, y):
    g = dead_tree(r, x, y, 150)
    for u, v in ((-30, -96), (28, -112), (-14, -128)):
        g += f'<path d="M{x+u-8:.1f} {y+v:.1f} Q{x+u:.1f} {y+v-10:.1f} {x+u+8:.1f} {y+v-2:.1f} L{x+u+12:.1f} {y+v-4:.1f} L{x+u+6:.1f} {y+v+4:.1f} Z" fill="{I()}"/>'
    return g
def flies_skull(r, x, y):
    return skull_l(r, x, y - 18, 1.0) + ''.join(nt.dot(x + r.uniform(-50, 50), y - r.uniform(50, 100), 1.6) for _ in range(8))
def ekg_ridge(r, y):
    pts = [(-150, y), (-60, y), (-50, y - 12), (-40, y), (-30, y), (-22, y + 26), (-10, y - 56), (2, y + 14), (12, y), (150, y)]
    return jl(pts, r, 2.4, 0.4, 4)
def body_gore(r, x, y):
    return gurney(r, x, y, False) + ''.join(pl([(x - 14 + i * 7, y - 44), (x - 14 + i * 7, y - 36)], 1.2) for i in range(5))
def skeleton_lie(r, x, y):
    g = skull_l(r, x - 40, y - 10, 0.38) + pl([(x - 30, y - 8), (x + 10, y - 6)], 2.2)
    g += ''.join(pl([(x - 26 + i * 6, y - 14), (x - 26 + i * 6, y - 2)], 1.3) for i in range(5))
    return g + pl([(x + 10, y - 6), (x + 40, y - 2)], 2.2) + pl([(x + 10, y - 6), (x + 38, y - 10)], 2.2)
def dance(r, x, y):
    g = ''.join(skeleton_l(r, x + u, y) for u in (-60, -20, 20, 60))
    return g + ''.join(pl([(x + u + 8, y - 18), (x + u + 32, y - 18)], 1.6) for u in (-60, -20, 20))
def two_at_grave(r, x, y):
    return stand(x - 40, y) + stand(x - 14, y) + pl([(x - 32, y - 22), (x - 22, y - 22)], 2) + grave_mound(r, x + 40, y, 44) + cross(r, x + 40, y - 6, 32)
def two_carry(r, x, y):
    g = coffin_side(x, y - 56, 74, 14)
    for u, f in ((-34, 1), (34, -1)):
        g += head(x + u, y - 58) + pl([(x + u, y - 50), (x + u, y - 16)], 2.6) + pl([(x + u - 8, y), (x + u, y - 16), (x + u + 8, y)], 2.6)
        g += pl([(x + u, y - 44), (x + u + 10 * f, y - 52), (x + u + 18 * f, y - 62)], 2.2)
    return g
def ash_lake_l(r, x, y):
    g = ''.join(jl([(x - 120, y - v), (x + 120, y - v)], r, 1.6, 1.2, 8) for v in (2, 12, 22))
    return g + ''.join(nt.dot(x + r.uniform(-60, 80), y - r.uniform(40, 110), r.choice((1, 1.4, 1.8))) for _ in range(40))

# icon -> (subject, figure pose, background)
S = {}
def m(icons, subj, pose, bg): S.update({i: (subj, pose, bg) for i in icons.split()})
m("toe_tag triptych", "gurney", "stand", "pines")
m("morgue_drawer slabs thermo", "drawer", "stand", "pines")
m("body_bag", "bodybag", "kneel", "meadow")
m("y_incision rib_spreader layers lividity flayed_figure skinless_face butcher face_muscles", "body_gore", "stand", "pines")
m("autopsy_report obituary checklist eulogy", "sign", "stand", "meadow")
m("coffin nailed vault bell_coffin", "coffin_up", "lean", "cemetery")
m("lowering", "carry", "none", "cemetery")
m("tombstone markers wax_grave", "tomb", "lean", "cemetery")
m("open_grave grave_tape shovel_pile robber stain", "grave", "walk", "valley")
m("wreath", "wreath", "kneel", "cemetery")
m("rot_skull skull skull_flies eye_beetle beetle_skull cycle stages bloat big_fly petri", "flies_skull", "hug", "meadow")
m("skin_glove mummy_hand marbled torn_palm", "skeleton_lie", "hug", "meadow")
m("shroom_ribs", "shrooms", "hug", "meadow")
m("root_skull", "roots", "lean_far", "valley")
m("crow_ribs moth_ribs", "crows", "walk", "meadow")
m("anatomical_heart heart sutured_heart heart_box nerves fibers microtear thigh_section knee torn_bicep molars", "heart", "kneel", "meadow")
m("heart_trap", "trap", "hug", "pines")
m("organ_scale", "scale", "stand", "valley")
m("brain_jar jaw_xray vials", "jar", "stand", "pines")
m("embalm bottle", "bottle", "hug", "pines")
m("reaper reaper_glass reaper_clip reaper_sharpen reaper_ticket plague", "reaper", "sit_far", "valley")
m("skel_hoodie two_skulls skel_bench hand_skel", "skeleton", "hug", "pines")
m("danse", "dance", "none", "meadow")
m("ossuary barrow tray_bones", "bones", "kneel", "pines")
m("hearse", "hearse", "walk", "valley")
m("retort chimney", "crem", "walk", "pines")
m("urn_label urn_books ash_scale id_disc pacemaker", "urn", "hug", "cabin")
m("ash_lake", "ashlake", "lean_far", "valley")
m("chair plates_table casseroles", "chair", "none", "cabin")
m("phone_old phone_screen monitor", "phone", "hug", "cabin")
m("candle candle_out skull_candle", "candle", "hug", "pines")
m("hourglass", "hourglass", "lean", "meadow")
m("clock calendar", "clock", "lean", "meadow")
m("flower", "rose", "kneel", "cemetery")
m("ghost", "ghost", "hug", "pines")
m("eye moon sun brain brain_storm cloud skull_thread", "sky", "hug", "valley")
m("flatline", "ekg", "lie", "meadow")
m("battery mattress wristband", "bed", "none", "cabin")
m("figures2", "grave2", "none", "cemetery")
m("figure same_bones rot_lifter", "rack", "press", "pines")
m("barbell plate dumbbell kettlebell rack death_grip spine_bar spine_yoke rib_rack heart_plates flayed_arm ecorche_squat chalk_squat", "rack", "dead", "pines")
m("none", "none", "lean_far", "valley")

def subject(r, key, d):
    x, y = 30, G
    items = d.get("args", {}).get("items") or d.get("args", {}).get("lines") or ()
    F = {"gurney": lambda: gurney(r, x, y), "drawer": lambda: drawer(r, x + 20, y), "bodybag": lambda: bodybag(r, x + 10, y),
         "body_gore": lambda: body_gore(r, x, y), "sign": lambda: sign_l(r, x, y, items), "coffin_up": lambda: coffin_up(r, x, y),
         "carry": lambda: two_carry(r, 0, y), "grave": lambda: grave_open(r, x - 10, y), "tomb": lambda: tomb(r, x, y, 1.3),
         "wreath": lambda: wreath_l(r, x, y), "flies_skull": lambda: flies_skull(r, x, y), "skeleton_lie": lambda: skeleton_lie(r, x, y),
         "shrooms": lambda: shrooms_l(r, x, y), "roots": lambda: roots_skull(r, x, y), "crows": lambda: crows_tree(r, x + 20, y),
         "heart": lambda: "", "trap": lambda: trap_l(r, x, y), "scale": lambda: scale_l(r, x, y),
         "jar": lambda: table_l(r, x, y, 0) + jar_l(r, x, y - 34), "bottle": lambda: bottle_l(r, x, y), "reaper": lambda: reaper_l(r, x + 30, y),
         "skeleton": lambda: skeleton_l(r, x, y, "sit"), "dance": lambda: dance(r, 0, y), "bones": lambda: bones_pile(r, x, y),
         "hearse": lambda: hearse_l(r, x + 20, y), "crem": lambda: crem_l(r, x, y), "urn": lambda: table_l(r, x, y, 0) + urn_l(r, x, y - 34, 0.9),
         "ashlake": lambda: ash_lake_l(r, x, y), "chair": lambda: chair_l(r, x - 80, y) + table_l(r, x + 10, y),
         "phone": lambda: phone_l(r, x, y), "candle": lambda: candle_l(r, x, y), "hourglass": lambda: hourglass_l(r, x, y),
         "clock": lambda: clock_l(r, x, y), "rose": lambda: tomb(r, x, y, 1.1) + rose_l(r, x - 30, y), "ghost": lambda: ghost_l(r, x, y),
         "sky": lambda: "", "ekg": lambda: "", "bed": lambda: bed_l(r, 0, y), "grave2": lambda: two_at_grave(r, 0, y),
         "rack": lambda: "", "none": lambda: ""}
    return F[key]()

def figure(r, pose):
    y = G
    return {"lean": lambda: sit_lean(-50, y, 1), "lean_far": lambda: pine(-110, y, 110, r) + sit_lean(-94, y, 1),
            "sit_far": lambda: pine(-112, y, 110, r) + sit_hug(-80, y, 1), "hug": lambda: sit_hug(-40, y, 1),
            "kneel": lambda: kneel(-32, y, 1), "lie": lambda: lie(-10, y, 1), "walk": lambda: walk(-50, y, 1),
            "stand": lambda: stand(-60, y), "press": lambda: press(0, y), "dead": lambda: deadlift(0, y), "none": lambda: ""}[pose]()

def background(r, bg, num, sky_free=False):
    g = ''   # no sky: the style is ground-level line art (night only for 208-219)
    if bg == "valley":
        g += mountains(r, 170, ((-120, 34), (-50, 50), (30, 38), (110, 54)))
        rv = [(110, 172), (126, 186), (100, 200), (132, 214)]
        g += river(r, rv, 2, 10) + forest(r, 174, 210, 40, 150, 22, in_river(rv, 2, 10))
    elif bg == "meadow":
        g += mountains(r, 196, ((-110, 34), (-30, 50), (60, 36), (126, 44))) + forest(r, 198, 222, n=26, avoid=lambda x, y: -80 < x < 100)
    elif bg == "cemetery":
        g += mountains(r, 196, ((-60, 30), (40, 40), (120, 30)), snow=False) + ''.join(tomb(r, u, G - 4, 0.5, "") for u in (-130, -106, 112, 134))
    elif bg == "cabin":
        g += pine(-132, G, 120, r) + pine(134, G, 130, r) + forest(r, 206, 226, n=14, avoid=lambda x, y: -114 < x < 114)
    else:
        g += ''.join(pine(u, G, h, r) for u, h in ((-138, 130), (-116, 96), (116, 100), (138, 134)))
    return g + ground(r, [(-150, G), (150, G)])

def scene(num, d):
    r = random.Random(num * 17 + 3)
    import redo_specs as RS                     # per-design scenes chosen from the caption
    if num in RS.SPEC:
        bg, fn = RS.SPEC[num]
        g = RS.eyes_forest(r) + ground(r, [(-150, G), (150, G)]) if bg == "eyes" else background(r, bg, num)
        return g + fn(r) + tufts(r, (-124, 124), G)
    subj, pose, bg = S.get(d.get("icon", "none"), S["none"])
    g = background(r, bg, num, sky_free=subj in ("heart", "sky"))
    if subj == "heart": g += stone(r, 30, G) + heart_l(r, 30, G - 26, 0.62)
    if subj == "sky": g += rain_cloud(r, -40, 150)
    if subj == "ekg": g += ekg_ridge(r, 150)
    if subj == "rack" and pose == "press": g += rack_l(r, 0, G)
    return g + subject(r, subj, d) + figure(r, pose) + tufts(r, (-124, 124), G)

# ---------- caption ----------
KEEP = {"A.M.", "P.M.", "LBS.", "LBS", "LB", "988", "PR", "ATG"}
def cap_text(t):
    out, start = [], True
    for w in t.split():
        core = w.strip(".,:;?!()'\"")
        if core.upper() in KEEP or core.isdigit():
            out.append(w.lower() if core.upper() in ("A.M.", "P.M.") else w.upper()); start = w.endswith((".", "?", "!")); continue
        lw = w.lower()
        if core.upper() in ("I", "I'M", "I'LL", "I'VE", "I'D"): lw = "I" + lw[1:]
        elif start: lw = (lw[0].upper() + lw[1:]) if lw[0].isalpha() else (lw[0] + lw[1:2].upper() + lw[2:])
        out.append(lw); start = w.endswith((".", "?", "!"))
    return " ".join(out)
def wrap(text, width, size):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if cur and sd.measure(t, "hand", size) > width: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
def caption(text, x, y, width, size, minsize):
    for sz in range(int(size), int(minsize) - 1, -2):
        lines = wrap(text, width, sz)
        if len(lines) <= 3 and all(sd.measure(l, "hand", sz) <= width for l in lines): break
    g = ''.join(sd.tpath(l, "hand", sz, x, y + sz * 0.8 + i * sz * 0.95) for i, l in enumerate(lines))
    return g, y + sz * 0.95 * len(lines) + sz * 0.1

def redo_layout(num, d):
    main = cap_text(" ".join(d["lines"]))
    sub = cap_text(d["sub"]) if d.get("sub") else ""
    if d["place"] in ("back", "hood"):
        a, yy = caption(main, 300, 186, 292, 44, 26)
        if sub: a += sd.tpath(sub, "hand", sd.fitsize(sub, "hand", 280, 24), 300, yy + 18); yy += 26
        k = min(1.15, (556 - yy) / 164)
        return "back", a + f'<g transform="translate(300 {yy+2:.1f}) scale({k:.3f}) translate(0 -80)">{scene(num, d)}</g>'
    a, yy = caption(main, 300, 214, 262, 34, 22)
    if sub: a += sd.tpath(sub, "hand", sd.fitsize(sub, "hand", 250, 18), 300, yy + 12); yy += 18
    k = min(0.9, (456 - yy) / 164)
    return "front", a + f'<g transform="translate(300 {yy:.1f}) scale({k:.3f}) translate(0 -80)">{scene(num, d)}</g>'

def all_designs():
    from designs_data import FIRST, DESIGNS
    from designs_data3 import SET3
    return FIRST + DESIGNS + SET3

def render_all(only=()):
    os.makedirs(OUT, exist_ok=True)
    lay0 = sd.layout; sd.layout = redo_layout; names = []
    try:
        for i, d in enumerate(all_designs()):
            n = i + 1
            if only and n not in only: continue
            dd = dict(d); dd["note"] = "Line-art redraw of sketch %02d. %s" % (n, d["note"])
            names.append(sd.render(n, dd, out=OUT))
    finally:
        sd.layout = lay0
    return names

if __name__ == "__main__":
    names = render_all({int(a) for a in sys.argv[1:]})
    print(len(names), names[0], names[-1])

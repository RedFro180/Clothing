"""Night-landscape line-art sketches (208-219), in the style of the user's reference images:
hand-drawn single-ink line art, lone stick figure, pines, mountains, river, moon, handwritten caption.
Figures are never placed at a cliff edge or any drop (design line: no height/jump method imagery).
Run: python3 tools/svgs_night.py [numbers...]"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import svgs_dark as sd
sd.FILES["hand"] = "caveat-latin-600-normal.woff2"     # Caveat, SIL OFL (tools/fonts/LICENSE-caveat.txt)

W = 2.4   # base pen width in scene units (scene = 300 x 260, scaled onto the hoodie)
def I(): return sd.INK
def B(): return sd.FAB

# ---------- pen helpers ----------
def jitter(pts, r, amt=1.2, step=6):
    out = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for k in range(n):
            t = k / n
            out.append((x1 + (x2 - x1) * t + r.uniform(-amt, amt), y1 + (y2 - y1) * t + r.uniform(-amt, amt)))
    out.append(pts[-1])
    return out
def pl(pts, w=W, c=None, fill="none", close=False):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")
    return f'<path d="{d}" fill="{fill}" stroke="{c or I()}" stroke-width="{w:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
def jl(pts, r, w=W, amt=1.2, step=6, **kw): return pl(jitter(pts, r, amt, step), w, **kw)
def circ(x, y, rad, w=W, fill=None): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{fill or B()}" stroke="{I()}" stroke-width="{w:.2f}"/>'
def dot(x, y, rad, c=None, op=1): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{c or I()}" opacity="{op}"/>'

# ---------- landscape parts ----------
def pine(x, base, h, r, w=W, lean=0):
    g = jl([(x, base), (x + lean, base - h)], r, w * 1.1, 0.6)
    levels = max(4, int(h / 9))
    for i in range(levels):
        t = (i + 1) / levels; yy = base - h + h * t * 0.92; span = 3 + h * 0.24 * t
        cx = x + lean * (1 - t)
        for d in (-1, 1):
            g += jl([(cx, yy - 4), (cx + d * span * 0.55, yy - 1), (cx + d * span, yy + 2 + r.uniform(0, 3))], r, w * 0.8, 0.8, 4)
            if span > 10:
                g += jl([(cx + d * span * 0.45, yy), (cx + d * span * 0.6, yy + 5)], r, w * 0.6, 0.6, 3)
    g += jl([(x - 6, base), (x + 6, base)], r, w * 0.7, 0.6)
    return g
def tiny_pine(x, y, h, r, w):
    return pl([(x - h * 0.28, y), (x - h * 0.1, y - h * 0.45), (x - h * 0.2, y - h * 0.45), (x, y - h), (x + h * 0.2, y - h * 0.45), (x + h * 0.1, y - h * 0.45), (x + h * 0.28, y)], w)
def forest(r, y0, y1, x0=-150, x1=150, n=70, avoid=None, hmin=5, hmax=16):
    g = ''; pts = []
    for _ in range(n * 3):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        if avoid and avoid(x, y): continue
        pts.append((x, y))
        if len(pts) >= n: break
    for x, y in sorted(pts, key=lambda p: p[1]):
        t = (y - y0) / max(1, (y1 - y0)); h = hmin + (hmax - hmin) * t
        g += tiny_pine(x, y, h, r, 1.1 + t * 0.9)
    return g
def mountains(r, y, peaks=((-120, 40), (-60, 62), (10, 46), (80, 70), (140, 44)), x0=-150, x1=150, snow=True):
    pts = [(x0, y)]
    for px, ph in peaks:
        pts += [(px - 22, y - ph * 0.45), (px, y - ph), (px + 20, y - ph * 0.5)]
    pts.append((x1, y))
    g = jl(pts, r, W * 0.9, 0.8, 5)
    if snow:
        for px, ph in peaks:
            g += jl([(px - 8, y - ph + 10), (px, y - ph + 4), (px + 7, y - ph + 12)], r, W * 0.6, 0.4, 3)
            g += jl([(px + 4, y - ph + 8), (px + 14, y - ph * 0.62)], r, W * 0.5, 0.6, 4)
    return g
def river(r, pts, w0=3, w1=18):
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        t = i / (len(pts) - 1); hw = w0 + (w1 - w0) * t
        left.append((x - hw, y)); right.append((x + hw, y))
    g = jl(left, r, W * 0.75, 0.8, 5) + jl(right, r, W * 0.75, 0.8, 5)
    for i in range(1, len(pts) - 1):
        x, y = pts[i]; t = i / (len(pts) - 1)
        g += pl([(x - 3 * t - 2, y + 1), (x + 4 * t + 2, y + 1)], 1.3)
    return g
def in_river(pts, w0=3, w1=18, pad=6):
    def f(x, y):
        for i, (px, py) in enumerate(pts):
            t = i / (len(pts) - 1)
            if abs(py - y) < 8 and abs(px - x) < w0 + (w1 - w0) * t + pad: return True
        return False
    return f
def moon(x, y, rad, r):
    g = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{I()}"/>'
    for _ in range(int(rad / 2.2)):
        a, d = r.uniform(0, 6.28), r.uniform(0, rad * 0.8)
        g += dot(x + math.cos(a) * d, y + math.sin(a) * d, r.uniform(rad * 0.05, rad * 0.16), B(), 0.55)
    return g
def clouds(r, x, y, w):
    g = ''
    for k in range(3):
        yy = y + k * 6; xx = x + r.uniform(-w * 0.2, w * 0.2); ww = w * r.uniform(0.6, 1)
        g += jl([(xx - ww / 2, yy), (xx - ww / 4, yy - 2), (xx - ww / 6, yy - 5), (xx, yy - 2), (xx + ww / 5, yy - 4), (xx + ww / 2, yy)], r, W * 0.6, 0.5, 5)
    return g
def tufts(r, xs, y, k=1):
    return ''.join(jl([(x - 4 * k, y), (x - 2 * k, y - 6 * k), (x, y), (x + 2 * k, y - 8 * k), (x + 4 * k, y)], r, W * 0.6, 0.3, 2) for x in xs)
def ground(r, pts, w=W): return jl(pts, r, w, 1.0, 5)
def stars(r, n, x0=-150, x1=150, y0=0, y1=60):
    return ''.join(dot(r.uniform(x0, x1), r.uniform(y0, y1), r.choice((0.8, 1, 1.4))) for _ in range(n))

# ---------- figures (stick people like the reference; head = outlined circle) ----------
def head(x, y, rad=7.5): return circ(x, y, rad, 2.4)
def sit_hug(x, y, f=1):      # sitting on the ground, knees hugged; faces direction f
    return (head(x + 2 * f, y - 40) + pl([(x + 1 * f, y - 32), (x - 3 * f, y - 14), (x, y)], 2.6)
            + pl([(x, y), (x + 12 * f, y - 16), (x + 22 * f, y)], 2.6)
            + pl([(x + 1 * f, y - 28), (x + 10 * f, y - 20), (x + 13 * f, y - 16)], 2.4)
            + pl([(x, y - 26), (x + 8 * f, y - 18)], 2.2))
def sit_lean(x, y, f=1):     # sitting with back against something, legs out
    return (head(x, y - 40) + pl([(x, y - 32), (x - 1 * f, y)], 2.6) + pl([(x - 1 * f, y), (x + 16 * f, y - 6), (x + 28 * f, y)], 2.6)
            + pl([(x, y - 26), (x + 10 * f, y - 12), (x + 14 * f, y - 8)], 2.3) + pl([(x, y - 24), (x - 6 * f, y - 10)], 2.3))
def kneel(x, y, f=1):
    return (head(x + 4 * f, y - 40) + pl([(x + 3 * f, y - 32), (x, y - 14)], 2.6) + pl([(x, y - 14), (x - 12 * f, y), (x - 20 * f, y)], 2.6)
            + pl([(x, y - 14), (x + 10 * f, y - 8), (x + 10 * f, y)], 2.6) + pl([(x + 3 * f, y - 26), (x + 12 * f, y - 18)], 2.3))
def lie(x, y, f=1):
    return (head(x - 30 * f, y - 7) + pl([(x - 22 * f, y - 5), (x + 4 * f, y - 4)], 2.6) + pl([(x + 4 * f, y - 4), (x + 20 * f, y - 12), (x + 32 * f, y - 2)], 2.6)
            + pl([(x + 4 * f, y - 4), (x + 34 * f, y - 4)], 2.6) + pl([(x - 16 * f, y - 5), (x - 28 * f, y - 18), (x - 36 * f, y - 12)], 2.3))
def walk(x, y, f=1, k=1):
    return (head(x + 2 * f * k, y - 40 * k, 7.5 * k) + pl([(x + 1 * f * k, y - 32 * k), (x - 1 * f * k, y - 16 * k)], 2.6 * k)
            + pl([(x - 8 * f * k, y), (x - 1 * f * k, y - 16 * k), (x + 8 * f * k, y)], 2.6 * k)
            + pl([(x - 7 * f * k, y - 18 * k), (x, y - 28 * k), (x + 8 * f * k, y - 18 * k)], 2.2 * k))
def carry_rock(x, y, f=1):
    g = (head(x + 5 * f, y - 38) + pl([(x + 4 * f, y - 30), (x - 2 * f, y - 14)], 2.6) + pl([(x - 10 * f, y), (x - 2 * f, y - 14), (x + 6 * f, y - 2)], 2.6)
         + pl([(x + 3 * f, y - 26), (x - 6 * f, y - 40)], 2.3) + pl([(x + 4 * f, y - 24), (x + 4 * f, y - 40)], 2.3))
    g += f'<path d="M{x-22*f:.1f} {y-40:.1f} Q{x-18*f:.1f} {y-62:.1f} {x+2*f:.1f} {y-62:.1f} Q{x+18*f:.1f} {y-60:.1f} {x+14*f:.1f} {y-42:.1f} Q{x-2*f:.1f} {y-34:.1f} {x-22*f:.1f} {y-40:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="2.4"/>'
    g += pl([(x - 10 * f, y - 52), (x - 2 * f, y - 56)], 1.4) + pl([(x + 4 * f, y - 48), (x + 8 * f, y - 52)], 1.4)
    return g
def sit_on(x, y, f=1):       # sitting on a log/step at height y, feet on ground at y+14
    return (head(x, y - 38) + pl([(x, y - 30), (x - 1 * f, y)], 2.6) + pl([(x - 1 * f, y), (x + 12 * f, y + 2), (x + 12 * f, y + 14)], 2.6)
            + pl([(x - 1 * f, y), (x + 8 * f, y + 1), (x + 6 * f, y + 14)], 2.4) + pl([(x, y - 24), (x + 10 * f, y - 4)], 2.3))

# ---------- props ----------
def grave_mound(r, x, y, w=34):
    g = jl([(x - w / 2, y), (x - w / 3, y - 7), (x, y - 9), (x + w / 3, y - 7), (x + w / 2, y)], r, W, 0.5, 4)
    g += ''.join(dot(x + r.uniform(-w / 3, w / 3), y - r.uniform(1, 6), 0.9) for _ in range(8))
    return g
def cross(r, x, y, h=36):
    return jl([(x, y), (x, y - h)], r, 3.2, 0.4) + jl([(x - h * 0.3, y - h * 0.72), (x + h * 0.3, y - h * 0.72)], r, 3.2, 0.4)
def headstone(x, y, w=16, h=24, fill=None):
    return f'<path d="M{x-w/2:.1f} {y:.1f} L{x-w/2:.1f} {y-h+w/2:.1f} Q{x-w/2:.1f} {y-h:.1f} {x:.1f} {y-h:.1f} Q{x+w/2:.1f} {y-h:.1f} {x+w/2:.1f} {y-h+w/2:.1f} L{x+w/2:.1f} {y:.1f} Z" fill="{fill or B()}" stroke="{I()}" stroke-width="2.2"/>'
def campfire(r, x, y):
    g = jl([(x - 16, y), (x + 14, y - 6)], r, 3.4, 0.4) + jl([(x - 14, y - 6), (x + 16, y)], r, 3.4, 0.4)
    for dx, h in ((-6, 18), (0, 28), (6, 20)):
        g += f'<path d="M{x+dx-4:.1f} {y-4:.1f} Q{x+dx-6:.1f} {y-h*0.5:.1f} {x+dx:.1f} {y-h:.1f} Q{x+dx+5:.1f} {y-h*0.5:.1f} {x+dx+4:.1f} {y-4:.1f} Z" fill="none" stroke="{I()}" stroke-width="2"/>'
    g += ''.join(dot(x + r.uniform(-10, 10), y - r.uniform(32, 60), 1.1) for _ in range(6))
    return g
def coffin_side(x, y, w=60, h=14):
    return f'<path d="M{x-w/2:.1f} {y:.1f} L{x-w/2+8:.1f} {y-h:.1f} L{x+w/2-4:.1f} {y-h:.1f} L{x+w/2:.1f} {y-h/2:.1f} L{x+w/2-4:.1f} {y:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="2.4"/>'
def dead_tree(r, x, base, h):
    g = jl([(x - 4, base), (x - 2, base - h * 0.5), (x, base - h)], r, 4, 0.6)
    for t, d, L in ((0.35, -1, 34), (0.5, 1, 40), (0.65, -1, 30), (0.78, 1, 24), (0.88, -1, 16)):
        yy = base - h * t
        g += jl([(x, yy), (x + d * L * 0.6, yy - L * 0.4), (x + d * L, yy - L * 0.7)], r, 2.4, 0.6, 4)
        g += jl([(x + d * L * 0.6, yy - L * 0.4), (x + d * L * 0.7, yy - L * 0.9)], r, 1.6, 0.5, 3)
    g += jl([(x - 4, base), (x - 18, base + 4)], r, 2.4, 0.4) + jl([(x - 2, base), (x + 14, base + 3)], r, 2.4, 0.4)
    return g
def cabin(r, x, y):
    g = jl([(x - 40, y), (x - 40, y - 34), (x + 40, y - 34), (x + 40, y)], r, W, 0.5)
    g += jl([(x - 48, y - 32), (x, y - 62), (x + 48, y - 32)], r, W * 1.1, 0.5)
    g += ''.join(jl([(x - 38, y - 34 + k * 8), (x + 38, y - 34 + k * 8)], r, 1.1, 0.6) for k in range(1, 4))
    g += f'<rect x="{x+12:.1f}" y="{y-26:.1f}" width="16" height="12" fill="{I()}"/>' + pl([(x + 20, y - 26), (x + 20, y - 14)], 1.4, B())
    g += f'<rect x="{x-24:.1f}" y="{y-26:.1f}" width="14" height="26" fill="{B()}" stroke="{I()}" stroke-width="2"/>'
    g += jl([(x + 24, y - 50), (x + 24, y - 66), (x + 34, y - 66), (x + 34, y - 44)], r, W, 0.4)
    g += jl([(x + 29, y - 70), (x + 22, y - 84), (x + 34, y - 98), (x + 24, y - 112), (x + 40, y - 126)], r, 2, 1.4, 4)
    g += jl([(x - 30, y), (x - 30, y + 6), (x - 4, y + 6), (x - 4, y)], r, 2, 0.3)   # step
    return g

# ---------- scenes (local units: x -150..150, y 0..260; ground ~200-250) ----------
def sc_bury(r):
    g = stars(r, 18) + moon(70, 54, 22, r) + clouds(r, 70, 80, 110) + clouds(r, -60, 70, 80)
    g += mountains(r, 132)
    rv = [(30, 134), (50, 150), (24, 168), (60, 188), (40, 206)]
    g += river(r, rv) + forest(r, 136, 206, -20, 150, 60, in_river(rv))
    hill = [(-150, 214), (-110, 196), (-60, 188), (0, 190), (60, 200), (110, 214), (150, 222)]
    g += f'<path d="M-150 260 L' + " L".join(f"{x} {y}" for x, y in hill) + f' L150 260 Z" fill="{B()}"/>'
    g += ground(r, hill)
    g += pine(-92, 194, 140, r) + sit_lean(-76, 192, 1) + grave_mound(r, -30, 192) + cross(r, -30, 182, 22)
    g += tufts(r, (-130, -118, 10, 40, 80), 204)
    return g
def sc_forest_keeps(r):
    g = stars(r, 14, y1=50) + moon(0, 40, 18, r)
    for x, h in ((-132, 150), (-104, 120), (104, 130), (134, 160), (-70, 90), (74, 96)):
        g += pine(x, 226, h, r)
    g += ground(r, [(-150, 226), (150, 226)]) + cross(r, 14, 226, 44) + grave_mound(r, 14, 228, 46) + kneel(-14, 226, 1)
    g += tufts(r, (-50, -30, 40, 56), 226)
    return g
def sc_outlives(r):
    g = stars(r, 30, y1=90) + moon(-70, 50, 26, r) + clouds(r, 40, 60, 120)
    g += mountains(r, 160, ((-110, 60), (-30, 84), (50, 56), (120, 72)))
    g += forest(r, 162, 196, n=45)
    g += ground(r, [(-150, 214), (-60, 208), (40, 212), (150, 206)]) + lie(-6, 214, 1)
    g += tufts(r, [x for x in range(-140, 150, 16) if not -50 < x < 50], 216, 0.9)
    return g
def sc_heavy(r):
    g = stars(r, 14, y1=60) + moon(100, 40, 16, r) + mountains(r, 120, ((-80, 50), (20, 70), (110, 46)))
    g += jl([(-150, 240), (-20, 226), (120, 214), (150, 210)], r, W)
    g += jl([(150, 196), (40, 186), (-90, 176), (-150, 170)], r, W * 0.9)
    g += jl([(-150, 152), (0, 140), (150, 132)], r, W * 0.8)
    g += pine(-120, 236, 70, r) + pine(126, 208, 60, r) + carry_rock(10, 223, 1)
    g += tufts(r, (-70, -50, 60, 80), 232)
    return g
def sc_survived(r):
    g = stars(r, 16, y1=60) + moon(-90, 40, 14, r)
    for x, h in ((-134, 170), (-100, 130), (-64, 96), (70, 104), (104, 140), (136, 176)):
        g += pine(x, 226, h, r)
    g += ground(r, [(-150, 226), (150, 226)]) + campfire(r, 22, 226) + sit_hug(-18, 226, 1)
    g += ''.join(pl([(22 + dx, 238), (22 + dx * 2, 244)], 1.2) for dx in (-14, -6, 6, 14))
    return g
def sc_dirt(r):
    g = stars(r, 16, y1=60) + moon(90, 46, 20, r) + clouds(r, 90, 70, 90) + mountains(r, 140, ((-60, 40), (40, 60), (120, 40)))
    rv = [(70, 142), (90, 160), (60, 180), (96, 200)]
    g += river(r, rv, 2, 12) + forest(r, 144, 196, 0, 150, 40, in_river(rv, 2, 12))
    g += ground(r, [(-150, 206), (-80, 196), (-20, 204), (20, 222), (40, 248)])
    for x, y in ((-130, 206), (-104, 200), (-50, 200), (-20, 206)):
        g += headstone(x, y)
    g += headstone(-78, 198, 20, 30) + sit_lean(-64, 198, 1)
    g += tufts(r, (-140, -116, -90, -36, -6), 206)
    return g
def sc_dead_trees(r):
    g = stars(r, 22, y1=80) + moon(80, 44, 20, r) + mountains(r, 168, ((-110, 34), (-20, 50), (90, 40)))
    g += forest(r, 170, 204, n=30, avoid=lambda x, y: -70 < x < 40)
    g += ground(r, [(-150, 226), (150, 226)]) + dead_tree(r, -16, 226, 190) + walk(18, 226, -1)
    g += pl([(10, 196), (-12, 196)], 2.2)
    g += tufts(r, (-110, -90, 60, 90, 120), 226)
    return g
def sc_carried(r):
    g = stars(r, 24, y1=90) + moon(0, 54, 30, r) + clouds(r, -70, 80, 90) + clouds(r, 80, 90, 90)
    g += jl([(-150, 216), (-80, 200), (0, 194), (80, 200), (150, 216)], r, W)
    g += forest(r, 214, 238, n=30)
    g += coffin_side(0, 160, 74, 14)
    for x, f in ((-34, 1), (34, -1)):
        g += head(x, 158) + pl([(x, 166), (x, 182)], 2.6) + pl([(x - 8, 196), (x, 182), (x + 8, 196)], 2.6)
        g += pl([(x, 170), (x + 10 * f, 164), (x + 18 * f, 154)], 2.2)
    return g
def sc_long_walk(r):
    g = stars(r, 26, y1=70) + moon(-80, 40, 18, r) + clouds(r, -40, 66, 120)
    g += mountains(r, 118, ((-120, 30), (-40, 50), (40, 36), (120, 52)))
    rv = [(-10, 120), (20, 140), (-30, 162), (30, 186), (0, 214), (40, 246)]
    g += river(r, rv, 2, 26) + forest(r, 122, 236, n=90, avoid=in_river(rv, 2, 26, 22))
    g += walk(-6, 236, -1, 0.7)
    return g
def sc_rest(r):
    g = stars(r, 20, y1=60) + moon(0, 40, 16, r)
    g += pine(-110, 226, 170, r) + pine(110, 226, 160, r) + forest(r, 200, 222, n=20, avoid=lambda x, y: -100 < x < 100)
    g += ground(r, [(-150, 226), (150, 226)])
    g += jl([(-104, 140), (-60, 170), (0, 178), (60, 170), (104, 142)], r, 2.2, 0.4)
    g += jl([(-104, 140), (-60, 162), (0, 168), (60, 162), (104, 142)], r, 1.4, 0.4)
    g += head(-46, 158) + pl([(-38, 162), (30, 166)], 2.6) + pl([(-30, 162), (10, 160), (20, 162)], 2.0)
    g += ''.join(sd.tpath(z, "hand", s, x, y) for z, s, x, y in (("z", 12, -40, 138), ("z", 9, -30, 126), ("z", 7, -22, 116)))
    return g
def sc_moon(r):
    g = stars(r, 24, y1=120) + moon(30, 86, 62, r) + clouds(r, -20, 140, 140)
    g += mountains(r, 196, ((-110, 26), (-30, 40), (60, 30), (130, 38)), snow=False)
    g += ground(r, [(-150, 232), (150, 232)])
    g += f'<path d="M-56 230 L-56 218 L4 216 L4 230 Z" fill="{B()}" stroke="{I()}" stroke-width="2.4"/>' + circ(4, 223, 7, 2)
    g += sit_on(-30, 216, 1) + tufts(r, (-100, -80, 40, 70, 100), 232)
    return g
def sc_home(r):
    g = stars(r, 20, y1=70) + moon(-90, 44, 16, r)
    g += pine(-120, 226, 150, r) + pine(126, 226, 170, r) + pine(96, 226, 110, r)
    g += ground(r, [(-150, 226), (150, 226)]) + cabin(r, 0, 226)
    g += sit_on(-14, 214, 1)
    g += tufts(r, (-90, -70, 60, 72), 226)
    return g
SCENES = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}

# ---------- layout ----------
def night_layout(num, d):
    r = random.Random(num * 31)
    scene = SCENES[d["scene"]](r)
    cap = d["lines"][0]
    if d["place"] == "back":
        a = sd.tpath(cap, "hand", sd.fitsize(cap, "hand", 290, 46), 300, 214)
        a += f'<g transform="translate(300 236) scale(1.0)">{scene}</g>'
        return "back", a
    a = sd.tpath(cap, "hand", sd.fitsize(cap, "hand", 230, 32), 300, 248)
    a += f'<g transform="translate(300 252) scale(0.72)">{scene}</g>'
    return "front", a

COLORS = {p[0].split(" (")[0]: p for p in sd.PALETTE}
def render_all(only=()):
    from designs_data_night import NIGHT
    lay0, col0 = sd.layout, sd.color_for
    sd.layout = night_layout
    names = []
    try:
        for i, d in enumerate(NIGHT):
            n = 208 + i
            if only and n not in only: continue
            sd.color_for = (lambda c: (lambda _n: COLORS[c]))(d["color"])
            names.append(sd.render(n, d))
    finally:
        sd.layout, sd.color_for = lay0, col0
    return names

if __name__ == "__main__":
    names = render_all({int(a) for a in sys.argv[1:]})
    print(len(names), names[0], names[-1])

"""Vignette composition for line-art redraws (v2 samples).
Rules from research + the user's reference image:
- three line weights: foreground 3.0, midground 1.6, background 1.0
- overlapping layers: far mountains -> dense forest band -> foreground mound with hatching
- one focal subject drawn LARGE on the mound (about 40% of the scene height)
- edges thin out into a rounded vignette (forest and ground taper at the sides)
- smooth, confident curves (low jitter), not scribbles
Scene box: x -150..150, y 0..260 (ground crest ~ y 200)."""
import math, random, re
import svgs_dark as sd
import svgs_night as nt

def I(): return sd.INK
def B(): return sd.FAB
FG, MG, BG = 3.0, 1.6, 1.0

def path(d, w, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{I()}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'
def smooth(pts):
    """Catmull-Rom through points -> cubic bezier path string (smooth, hand-inked look)."""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d

# ---------- background ----------
def mountains(r, y=150):
    pts = [(-150, y + 10)]
    x = -150
    while x < 150:
        x += r.uniform(30, 55); pts.append((min(x, 150), y - r.uniform(10, 46)))
        x += r.uniform(14, 28); pts.append((min(x, 150), y + r.uniform(-4, 6)))
    g = path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts), BG)
    for a, b in pts[1::2]:
        g += path(f"M{a-6:.1f} {b+8:.1f} L{a:.1f} {b+2:.1f} L{a+5:.1f} {b+9:.1f}", BG * 0.8)
    return g
def sky(r, kind="night", side=1):
    g = ""
    if kind in ("night", "milky"):
        g += ''.join(f'<circle cx="{r.uniform(-140, 140):.1f}" cy="{r.uniform(20, 120):.1f}" r="{r.choice((0.7, 0.9, 1.2)):.1f}" fill="{I()}"/>' for _ in range(34))
        mx = 96 * side
        g += f'<circle cx="{mx}" cy="52" r="17" fill="{I()}"/>' + ''.join(f'<circle cx="{mx + r.uniform(-10, 10):.1f}" cy="{52 + r.uniform(-10, 10):.1f}" r="{r.uniform(1.5, 3.5):.1f}" fill="{B()}" opacity=".5"/>' for _ in range(7))
        for k in range(3):
            y = 70 + k * 6; x0 = mx - 60 + k * 10
            g += path(smooth([(x0, y), (x0 + 30, y - 3), (x0 + 60, y + 1), (x0 + 100, y - 2)]), BG)
    if kind == "milky":
        for t in [r.random() for _ in range(70)]:                  # soft diagonal band: sparse fine stars + two faint drift lines
            g += f'<circle cx="{t*280-140 + r.gauss(0, 8):.1f}" cy="{36 + t*60 + r.gauss(0, 6):.1f}" r="0.6" fill="{I()}"/>'

    return g

# ---------- midground forest band (dense, tapering to the edges) ----------
def pine(x, base, h, w=MG):
    g = f'<path d="M{x:.1f} {base-h:.1f} L{x-h*0.26:.1f} {base:.1f} L{x+h*0.26:.1f} {base:.1f} Z" fill="{B()}" stroke="none"/>'
    g += path(f"M{x:.1f} {base:.1f} L{x:.1f} {base-h:.1f}", w * 0.8)
    n = max(4, int(h / 7))
    for i in range(n):
        t = (i + 1) / n; yy = base - h + h * t * 0.95; span = h * 0.27 * t
        for d in (-1, 1):
            g += path(f"M{x:.1f} {yy-4:.1f} Q{x+d*span*0.6:.1f} {yy-2:.1f} {x+d*span:.1f} {yy+3:.1f}", w)
    return g
def forest_band(r, y=196, n=42, hmin=26, hmax=58, gap=None):
    g, items = "", []
    for i in range(n):
        x = -140 + 280 * (i + r.uniform(-0.3, 0.3)) / (n - 1)
        if gap and gap[0] < x < gap[1]: continue
        edge = 1 - (abs(x) / 150) ** 2                          # taper toward the vignette edges
        h = (hmin + (hmax - hmin) * r.random()) * (0.45 + 0.55 * edge)
        items.append((x, y + r.uniform(-4, 4) + (1 - edge) * 10, h))
    for x, b, h in sorted(items, key=lambda t: t[1]):
        g += pine(x, b, h)
    return g

# ---------- foreground mound with hatching + grass ----------
def mound(r, crest=206, half=128):
    """Foreground hill: heavy crest line, contour hatching on the shadow side, tufts, and a soft fading base (vignette)."""
    top = [(-half - 6, 244), (-half * 0.7, crest + 13), (-half * 0.3, crest + 2), (0, crest), (half * 0.35, crest + 3), (half * 0.72, crest + 15), (half + 6, 246)]
    d = smooth(top)
    g = path(d, FG)
    for k in range(9):                                           # contour hatching, right (shadow) slope, parallel strokes
        t = 0.25 + k * 0.07; x = half * t; yb = crest + 3 + (t ** 2) * 40
        g += path(f"M{x:.1f} {yb+5:.1f} l-7 9", MG * 0.8)
    for k in range(5):
        t = 0.45 + k * 0.1; x = -half * t; yb = crest + 2 + (t ** 2) * 38
        g += path(f"M{x:.1f} {yb+6:.1f} l-5 7", MG * 0.7)
    for x in (-96, -60, -22, 30, 70, 104):                     # grass tufts along the crest
        yb = crest + (abs(x) / half) ** 2 * 26 + 1
        g += path(f"M{x-4:.1f} {yb:.1f} l2 -7 M{x:.1f} {yb:.1f} l0 -9 M{x+4:.1f} {yb:.1f} l-2 -7", MG)
    for k, w in enumerate((0.62, 0.42, 0.24)):                  # fading base lines close the vignette
        y = 238 + k * 8
        g += path(f"M{-half*w:.1f} {y:.1f} Q0 {y+3:.1f} {half*w:.1f} {y:.1f}", BG * (1 - k * 0.2), extra=' stroke-dasharray="14 6"' if k else "")
    return g

def halo(svg, extra=6):
    """Fabric-colored outline under a subject so the background lines don't run through it."""
    h = svg.replace(f'stroke="{I()}"', f'stroke="{B()}"').replace(f'fill="{I()}"', f'fill="{B()}"')
    h = re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) + extra:.1f}"', h)
    return h + svg

MOUND_TOP = [(-134, 244), (-89.6, 219), (-38.4, 208), (0, 206), (44.8, 209), (92.2, 221), (134, 246)]
def knockout(svg, extra=7):
    """Black version of a subject for a mask: strokes widened, fills solid."""
    k = re.sub(r'(stroke|fill)="#[0-9a-fA-F]{6}"', lambda m: f'{m.group(1)}="#000"', svg)
    return re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) + extra:.1f}"', k)
SEQ = [0]
def compose(r, subject, sky_kind="none", side=1, forest_gap=None, solid=None):
    """Background (sky, mountains, forest) is masked so the hill and the subject cut a clean hole in it:
    nothing is painted in fabric color, so no flat boxes show on the garment."""
    SEQ[0] += 1; mid = f"vg{SEQ[0]}"
    back = (sky(r, sky_kind, side) if sky_kind != "none" else "") + mountains(r) + forest_band(r, gap=forest_gap)
    hill = f'<path d="{smooth(MOUND_TOP)} L134 270 L-134 270 Z" fill="#000"/>'
    mask = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-200" y="-60" width="400" height="360">'
            f'<rect x="-200" y="-60" width="400" height="360" fill="#fff"/>{hill}{knockout(subject)}{solid or ""}</mask>')
    return mask + f'<g mask="url(#{mid})">{back}</g>' + mound(r) + subject

# ---------- subjects (drawn at scale; foreground weight) ----------
def fig_parts(x, y, s=1.0, w=FG):
    """Helpers in subject space: returns functions for limbs/head at scale s."""
    L = lambda pts: path("M" + " L".join(f"{x+a*s:.1f} {y+b*s:.1f}" for a, b in pts), w)
    Hd = lambda a, b, rad=9: f'<circle cx="{x+a*s:.1f}" cy="{y+b*s:.1f}" r="{rad*s:.1f}" fill="{B()}" stroke="{I()}" stroke-width="{w}"/>'
    return L, Hd
def barbell(x, y, w=74, s=1.0, plates=None):
    g = path(f"M{x-w*s:.1f} {y:.1f} L{x+w*s:.1f} {y:.1f}", FG)
    for d in (-1, 1):
        for off, hh, ww in ((6, 34, 9), (16, 24, 7)):
            px = x + d * (w - off) * s
            g += f'<rect x="{px - ww*s/2:.1f}" y="{y - hh*s/2:.1f}" width="{ww*s:.1f}" height="{hh*s:.1f}" rx="{2*s:.1f}" fill="{B()}" stroke="{I()}" stroke-width="{MG+0.4}"/>'
    return g
def skull(x, y, s=1.0, w=MG + 0.4):
    g = f'<path d="M{x-14*s:.1f} {y+2*s:.1f} C{x-17*s:.1f} {y-20*s:.1f} {x+17*s:.1f} {y-20*s:.1f} {x+14*s:.1f} {y+2*s:.1f} L{x+9*s:.1f} {y+6*s:.1f} L{x+8*s:.1f} {y+13*s:.1f} L{x-8*s:.1f} {y+13*s:.1f} L{x-9*s:.1f} {y+6*s:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="{w}"/>'
    g += ''.join(f'<ellipse cx="{x+d*6*s:.1f}" cy="{y-2*s:.1f}" rx="{4*s:.1f}" ry="{4.5*s:.1f}" fill="{I()}"/>' for d in (-1, 1))
    g += path(f"M{x-1.5*s:.1f} {y+6*s:.1f} L{x:.1f} {y+3*s:.1f} L{x+1.5*s:.1f} {y+6*s:.1f}", 1.2)
    return g + ''.join(path(f"M{x+u*s:.1f} {y+8*s:.1f} L{x+u*s:.1f} {y+13*s:.1f}", 1) for u in (-4, 0, 4))
def skeleton_grip(x, y, s=1.0):
    """Standing skeleton, arms straight down, hands on a barbell at the hips. Feet at (x, y)."""
    g = skull(x, y - 104 * s, 1.1 * s)
    g += path(f"M{x:.1f} {y-90*s:.1f} L{x:.1f} {y-50*s:.1f}", FG * 0.9)                                   # spine
    for k in range(4):                                                                                    # ribs
        v = y - (84 - k * 7) * s; ww = (15 - k) * s
        g += path(f"M{x:.1f} {v:.1f} Q{x-ww:.1f} {v-2*s:.1f} {x-ww:.1f} {v+5*s:.1f} M{x:.1f} {v:.1f} Q{x+ww:.1f} {v-2*s:.1f} {x+ww:.1f} {v+5*s:.1f}", MG)
    g += path(f"M{x-16*s:.1f} {y-88*s:.1f} L{x+16*s:.1f} {y-88*s:.1f}", MG + 0.4)                            # collarbone
    g += path(f"M{x-12*s:.1f} {y-50*s:.1f} Q{x:.1f} {y-42*s:.1f} {x+12*s:.1f} {y-50*s:.1f}", MG + 0.4)        # pelvis
    for d in (-1, 1):
        g += path(f"M{x+d*16*s:.1f} {y-88*s:.1f} L{x+d*19*s:.1f} {y-64*s:.1f} L{x+d*20*s:.1f} {y-44*s:.1f}", FG * 0.85)   # arms straight down
        g += path(f"M{x+d*8*s:.1f} {y-48*s:.1f} L{x+d*10*s:.1f} {y-24*s:.1f} L{x+d*10*s:.1f} {y:.1f}", FG * 0.9)        # legs
        g += path(f"M{x+d*10*s:.1f} {y:.1f} L{x+d*18*s:.1f} {y:.1f}", FG * 0.9)
    return g + barbell(x, y - 44 * s, 70, s)
def tomb_plate(x, y, s=1.0):
    g = f'<path d="M{x-14*s:.1f} {y+22*s:.1f} L{x-14*s:.1f} {y-10*s:.1f} Q{x-14*s:.1f} {y-24*s:.1f} {x:.1f} {y-24*s:.1f} Q{x+14*s:.1f} {y-24*s:.1f} {x+14*s:.1f} {y-10*s:.1f} L{x+14*s:.1f} {y+22*s:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="{FG*0.8}"/>'
    return g + sd.tpath("RIP", "hand", 11 * s, x, y + 2 * s)
def back_carry(x, y, s=1.0):
    """Figure standing with a bar across the shoulders; RIP headstones as the plates. Feet at (x, y)."""
    L, Hd = fig_parts(x, y, s)
    g = path(f"M{x-92*s:.1f} {y-88*s:.1f} L{x+92*s:.1f} {y-88*s:.1f}", FG)
    g += tomb_plate(x - 78 * s, y - 88 * s, s) + tomb_plate(x + 78 * s, y - 88 * s, s)
    g += Hd(0, -100, 11) + L([(0, -89), (0, -46)]) + L([(-12, 0), (-6, -24), (0, -46), (6, -24), (12, 0)])
    g += L([(-3, -84), (-24, -82), (-30, -90)]) + L([(3, -84), (24, -82), (30, -90)])
    return g
def lying_stargazer(x, y, s=1.0):
    L, Hd = fig_parts(x, y, s)
    g = Hd(-46, -10, 10) + L([(-36, -8), (12, -6)]) + L([(12, -6), (30, -20), (46, -2)]) + L([(12, -6), (50, -4)])
    g += L([(-24, -8), (-34, -26), (-46, -24)])           # hand behind the head
    g += path(f"M{x-50*s:.1f} {y-24*s:.1f} l-6 -6 M{x-44*s:.1f} {y-28*s:.1f} l-2 -8", 1)     # gaze lines up
    return g + barbell(x + 104 * s, y - 15 * s, 40, 0.75 * s)
def half_face(x, y, s=1.0):
    """Bust: left half skull, right half living face (matches the original #11 art). Base at (x, y)."""
    g = f'<path d="M{x-46*s:.1f} {y:.1f} Q{x-40*s:.1f} {y-30*s:.1f} {x-16*s:.1f} {y-36*s:.1f} L{x+16*s:.1f} {y-36*s:.1f} Q{x+40*s:.1f} {y-30*s:.1f} {x+46*s:.1f} {y:.1f}" fill="{B()}" stroke="{I()}" stroke-width="{FG}"/>'
    cy = y - 84 * s
    g += f'<path d="M{x:.1f} {cy-46*s:.1f} C{x-40*s:.1f} {cy-46*s:.1f} {x-44*s:.1f} {cy+10*s:.1f} {x-30*s:.1f} {cy+30*s:.1f} L{x-16*s:.1f} {cy+46*s:.1f} L{x:.1f} {cy+48*s:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="{FG}"/>'
    g += f'<path d="M{x:.1f} {cy-46*s:.1f} C{x+40*s:.1f} {cy-46*s:.1f} {x+44*s:.1f} {cy+10*s:.1f} {x+30*s:.1f} {cy+30*s:.1f} Q{x+16*s:.1f} {cy+48*s:.1f} {x:.1f} {cy+48*s:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="{FG}"/>'
    g += path(f"M{x:.1f} {cy-46*s:.1f} L{x-3*s:.1f} {cy-30*s:.1f} L{x+2*s:.1f} {cy-18*s:.1f} L{x-2*s:.1f} {cy-4*s:.1f} L{x+2*s:.1f} {cy+12*s:.1f} L{x:.1f} {cy+48*s:.1f}", MG + 0.4)
    # skull half
    g += f'<ellipse cx="{x-17*s:.1f}" cy="{cy-2*s:.1f}" rx="{10*s:.1f}" ry="{11*s:.1f}" fill="{I()}"/>'
    g += f'<path d="M{x-2*s:.1f} {cy+16*s:.1f} L{x-7*s:.1f} {cy+10*s:.1f} L{x-2*s:.1f} {cy+6*s:.1f} Z" fill="{I()}"/>'
    g += path(f"M{x-26*s:.1f} {cy+28*s:.1f} L{x:.1f} {cy+28*s:.1f}", MG) + ''.join(path(f"M{x-u*s:.1f} {cy+24*s:.1f} L{x-u*s:.1f} {cy+34*s:.1f}", 1.2) for u in (3, 9, 15, 21))
    g += path(f"M{x-32*s:.1f} {cy-20*s:.1f} Q{x-24*s:.1f} {cy-30*s:.1f} {x-12*s:.1f} {cy-26*s:.1f}", 1.2) + path(f"M{x-30*s:.1f} {cy+12*s:.1f} q4 6 10 4", 1.2)
    # living half
    g += f'<path d="M{x+8*s:.1f} {cy-2*s:.1f} Q{x+17*s:.1f} {cy-9*s:.1f} {x+26*s:.1f} {cy-2*s:.1f} Q{x+17*s:.1f} {cy+5*s:.1f} {x+8*s:.1f} {cy-2*s:.1f} Z" fill="{B()}" stroke="{I()}" stroke-width="{MG}"/>'
    g += f'<circle cx="{x+17*s:.1f}" cy="{cy-2*s:.1f}" r="{3.2*s:.1f}" fill="{I()}"/>' + path(f"M{x+7*s:.1f} {cy-14*s:.1f} Q{x+17*s:.1f} {cy-19*s:.1f} {x+28*s:.1f} {cy-13*s:.1f}", MG + 0.6)
    g += path(f"M{x+3*s:.1f} {cy+2*s:.1f} L{x+8*s:.1f} {cy+15*s:.1f} L{x+3*s:.1f} {cy+17*s:.1f}", MG)
    g += path(f"M{x+4*s:.1f} {cy+29*s:.1f} Q{x+13*s:.1f} {cy+33*s:.1f} {x+21*s:.1f} {cy+28*s:.1f}", MG + 0.4)
    g += ''.join(path(f"M{x+u*s:.1f} {cy-46*s:.1f} Q{x+(u+10)*s:.1f} {cy-54*s:.1f} {x+(u+16)*s:.1f} {cy-40*s:.1f}", MG) for u in (2, 12, 22))   # hair
    return g

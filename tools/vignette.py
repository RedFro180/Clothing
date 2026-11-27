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
    """Two soft ridges (far = thinner, dashed snow lines on the near peaks)."""
    g = ""
    for layer, (yb, amp, w) in enumerate(((y - 6, 40, BG * 0.8), (y + 10, 30, BG))):
        pts, x = [(-150, yb + 14)], -150
        peaks = []
        while x < 150:
            x += r.uniform(36, 64); px = min(x, 150); py = yb - r.uniform(amp * 0.4, amp); pts.append((px, py)); peaks.append((px, py))
            x += r.uniform(20, 34); pts.append((min(x, 150), yb + r.uniform(-2, 8)))
        g += path(smooth(pts), w, extra=' opacity=".75"' if layer == 0 else "")
        if layer == 1:
            for px, py in peaks:
                g += path(f"M{px-7:.1f} {py+9:.1f} Q{px-2:.1f} {py+4:.1f} {px:.1f} {py+6:.1f} Q{px+3:.1f} {py+3:.1f} {px+6:.1f} {py+10:.1f}", BG * 0.8)
    return g
def star(x, y, k=1.0):
    return path(f"M{x-3*k:.1f} {y:.1f} L{x+3*k:.1f} {y:.1f} M{x:.1f} {y-3*k:.1f} L{x:.1f} {y+3*k:.1f}", 0.8)
def sky(r, kind="night", side=1):
    g, mx = "", 96 * side
    if kind in ("night", "crescent", "milky"):
        g += ''.join(f'<circle cx="{r.uniform(-140, 140):.1f}" cy="{r.uniform(24, 118):.1f}" r="{r.choice((0.6, 0.8, 1.0)):.1f}" fill="{I()}"/>' for _ in range(26))
        g += ''.join(star(r.uniform(-130, 130), r.uniform(28, 100), r.uniform(0.8, 1.3)) for _ in range(6))
    if kind == "night":
        g += f'<circle cx="{mx}" cy="54" r="17" fill="none" stroke="{I()}" stroke-width="{MG}"/>'
        g += ''.join(f'<circle cx="{mx+u}" cy="{54+v}" r="{rr}" fill="none" stroke="{I()}" stroke-width="0.9"/>' for u, v, rr in ((-5, -4, 4), (6, 3, 3), (-2, 8, 2.2), (7, -7, 1.6)))
        for k in range(3):
            y = 76 + k * 6; x0 = mx - 70 + k * 12
            g += path(smooth([(x0, y), (x0 + 30, y - 3), (x0 + 60, y + 1), (x0 + 96, y - 2)]), BG)
    if kind == "crescent":
        g += f'<path d="M{mx} {37} A17 17 0 1 0 {mx} {71} A13 17 0 1 1 {mx} {37} Z" fill="none" stroke="{I()}" stroke-width="{MG}"/>'
    if kind == "milky":
        for t in [r.random() for _ in range(80)]:
            g += f'<circle cx="{t*280-140 + r.gauss(0, 9):.1f}" cy="{34 + t*58 + r.gauss(0, 6):.1f}" r="0.55" fill="{I()}"/>'
    if kind == "sun":
        g += f'<circle cx="{mx}" cy="58" r="15" fill="none" stroke="{I()}" stroke-width="{MG}"/>'
        g += ''.join(path(f"M{mx+21*math.cos(a):.1f} {58+21*math.sin(a):.1f} L{mx+29*math.cos(a):.1f} {58+29*math.sin(a):.1f}", BG * 1.2) for a in [i * math.pi / 6 for i in range(12)])
        g += ''.join(path(f"M{u-6} {v} q3 -4 6 0 q3 -4 6 0", 1.1) for u, v in ((-70 * side, 70), (-46 * side, 60), (-30 * side, 78)))
    if kind == "dusk":
        g += f'<path d="M{mx-34} 150 A34 34 0 0 1 {mx+34} 150" fill="none" stroke="{I()}" stroke-width="{MG}"/>'
        g += ''.join(path(f"M{mx+40*math.cos(a):.1f} {150-40*math.sin(a):.1f} L{mx+50*math.cos(a):.1f} {150-50*math.sin(a):.1f}", BG) for a in [i * math.pi / 9 for i in range(1, 9)])
        g += ''.join(path(smooth([(-140 + k * 26, 96 + k * 10), (-60 + k * 20, 92 + k * 10), (20 + k * 16, 98 + k * 10)]), BG) for k in range(3))
    return g

# ---------- midground forest band (dense, tapering to the edges) ----------
def pine(x, base, h, w=MG):
    g = path(f"M{x:.1f} {base:.1f} L{x:.1f} {base-h:.1f}", w * 0.8)
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
    for k in range(3):                                           # cross-contour arcs that follow the hill (shadow side denser)
        yk = crest + 12 + k * 8; w = half * (0.55 - k * 0.12)
        g += path(f"M{w*0.15:.1f} {yk:.1f} Q{w*0.7:.1f} {yk+2:.1f} {w*1.25:.1f} {yk+10+k*3:.1f}", MG * 0.7)
        g += path(f"M{-w*1.15:.1f} {yk+12+k*3:.1f} Q{-w*0.8:.1f} {yk+4:.1f} {-w*0.45:.1f} {yk+2:.1f}", BG * 0.8)
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
def frame_tree(kind, x, base, h, w=MG + 0.3):
    if kind == "dead":
        g = path(f"M{x:.1f} {base:.1f} Q{x-2:.1f} {base-h*0.5:.1f} {x+1:.1f} {base-h:.1f}", w + 0.8)
        for t, d, L in ((0.35, -1, 0.3), (0.5, 1, 0.34), (0.66, -1, 0.26), (0.8, 1, 0.2)):
            yy = base - h * t
            g += path(f"M{x:.1f} {yy:.1f} Q{x+d*h*L*0.5:.1f} {yy-h*0.05:.1f} {x+d*h*L:.1f} {yy-h*L*0.6:.1f}", w)
        return g
    if kind == "leafy":
        cy, rx, ry, n, d = base - h * 0.66, h * 0.3, h * 0.3, 11, ""
        for i in range(n):
            a0, a1 = i / n * 2 * math.pi, (i + 1) / n * 2 * math.pi; am = (a0 + a1) / 2
            p0 = (x + rx * math.cos(a0), cy + ry * math.sin(a0)); p1 = (x + rx * math.cos(a1), cy + ry * math.sin(a1)); c = (x + rx * 1.2 * math.cos(am), cy + ry * 1.2 * math.sin(am))
            d += (f"M{p0[0]:.1f} {p0[1]:.1f}" if i == 0 else "") + f" Q{c[0]:.1f} {c[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}"
        return path(f"M{x-3:.1f} {base:.1f} L{x-2:.1f} {cy+ry*0.6:.1f} M{x+3:.1f} {base:.1f} L{x+2:.1f} {cy+ry*0.6:.1f}", w + 0.4) + f'<path d="{d} Z" fill="none" stroke="{I()}" stroke-width="{w}"/>'
    if kind == "birch":
        g = path(f"M{x-3:.1f} {base:.1f} L{x-2:.1f} {base-h:.1f} M{x+3:.1f} {base:.1f} L{x+2:.1f} {base-h:.1f}", w)
        g += ''.join(path(f"M{x-3:.1f} {base-v:.1f} l{4 if i%2 else 3} -1", w + 0.4) for i, v in enumerate(range(14, int(h), 13)))
        return g + ''.join(path(f"M{x:.1f} {base-h*t:.1f} Q{x+d*10:.1f} {base-h*t-6:.1f} {x+d*20:.1f} {base-h*t-14:.1f}", BG) for t, d in ((0.6, -1), (0.72, 1), (0.84, -1), (0.94, 1)))
    if kind == "cypress":
        return path(smooth([(x - 2, base), (x - 13, base - h * 0.35), (x - 9, base - h * 0.75), (x, base - h), (x + 9, base - h * 0.75), (x + 13, base - h * 0.35), (x + 2, base)]), w) + ''.join(path(f"M{x-5:.1f} {base-h*t:.1f} q5 -6 10 0", BG) for t in (0.25, 0.4, 0.55, 0.7, 0.85))
    return pine(x, base, h, w)
GROUND_Y = 206
def ground_line(r, y=GROUND_Y, x0=-142, x1=142):
    """Near-flat horizon: heavy in the middle, thinning and breaking into dashes toward the ends (no curl, no closed shape)."""
    g, x = "", -46
    pts = [(xx, y + r.uniform(-0.8, 0.8)) for xx in range(-50, 51, 10)]
    g += path(smooth(pts), FG)
    for d in (-1, 1):                                             # broken, thinning strokes outward
        x, w = 50, FG * 0.8
        while x < 138:
            L = r.uniform(12, 22) * (1 - (x - 50) / 150); gap = r.uniform(3, 6) + (x - 50) * 0.06
            a, b = x, min(x + L, 140)
            g += path(f"M{d*a:.1f} {y + r.uniform(-0.6, 0.6):.1f} L{d*b:.1f} {y + r.uniform(-0.6, 0.6):.1f}", max(0.7, w))
            x = b + gap; w -= 0.32
    return g
def tufts(r, xs, y=GROUND_Y):
    return ''.join(path(f"M{x-3:.1f} {y:.1f} l1.5 -6 M{x:.1f} {y:.1f} l0.4 -8 M{x+3:.1f} {y:.1f} l-1.2 -5.5", MG * 0.9) for x in xs)
def furrows(r, x0, x1, y=GROUND_Y):
    """Short horizontal texture strokes below the line, sparse and fading downward (reads as flat land, not a dome)."""
    g = ""
    for k, (yy, n, w) in enumerate(((y + 8, 7, BG), (y + 16, 5, BG * 0.85), (y + 26, 3, BG * 0.7))):
        for i in range(n):
            cx = r.uniform(-110 + k * 22, 110 - k * 22); L = r.uniform(8, 20) * (1 - k * 0.2)
            if x0 - 6 < cx < x1 + 6 and k == 0: continue
            g += path(f"M{cx-L/2:.1f} {yy + r.uniform(-1, 1):.1f} L{cx+L/2:.1f} {yy + r.uniform(-1, 1):.1f}", w)
    return g
def shadow(x0, x1, y=GROUND_Y):
    """Short cast-shadow hatching right under the subject so it sits on the ground."""
    w = max(16, x1 - x0); c = (x0 + x1) / 2
    return ''.join(path(f"M{c - w*s/2:.1f} {y + 4 + k*3.5:.1f} L{c + w*s/2:.1f} {y + 4 + k*3.5:.1f}", MG * (0.8 - k * 0.2)) for k, s in enumerate((0.9, 0.62, 0.34)))

def ground(r, kind, gx=(-30, 30), side=1):
    """Foreground ground (drawn on top, unmasked). kind: field | path | lake | cemetery | platform."""
    x0, x1 = gx; y = GROUND_Y
    g = ground_line(r)
    side_xs = [x for x in (-92, -66, -38, 40, 70, 96) if not (x0 - 8 < x < x1 + 8)]
    g += tufts(r, r.sample(side_xs, min(4, len(side_xs))))
    if kind == "path":                                            # dirt path coming toward the viewer from the subject's feet
        c = (x0 + x1) / 2
        for d in (-1, 1):
            g += path(smooth([(c + d * 10, y + 3), (c + d * 18, y + 22), (c + d * 34 + 6 * d, y + 50)]), MG)
        g += ''.join(path(f"M{c + u:.1f} {y + v:.1f} l{3 + v * 0.06:.1f} 0", BG) for u, v in ((-4, 14), (6, 24), (-10, 34), (8, 42)))
        g += furrows(r, c - 46, c + 46)
    elif kind == "lake":
        g += furrows(r, x0, x1)
    elif kind == "platform":                                      # lifting platform: wood boards in light perspective
        c = (x0 + x1) / 2; hw = max(46, (x1 - x0) / 2 + 18)
        g += path(f"M{c-hw:.1f} {y+1:.1f} L{c-hw-10:.1f} {y+16:.1f} L{c+hw+10:.1f} {y+16:.1f} L{c+hw:.1f} {y+1:.1f}", MG)
        g += path(f"M{c-hw*0.34:.1f} {y+1:.1f} L{c-hw*0.38-3:.1f} {y+16:.1f} M{c+hw*0.34:.1f} {y+1:.1f} L{c+hw*0.38+3:.1f} {y+16:.1f}", BG)
        g += furrows(r, c - hw - 14, c + hw + 14)
    else:
        g += furrows(r, x0, x1)
    if kind != "platform": g += shadow(x0 * 0.8, x1 * 0.8)
    return g

def lake(r, y=GROUND_Y, gap=None):
    """Still water between the far shore and the horizon (behind the subject)."""
    g = ""
    for k, yy in enumerate((y - 18, y - 13, y - 8.5, y - 4.5)):
        x = -132 + k * 8
        while x < 130 - k * 8:
            L = r.uniform(10, 26); g += path(f"M{x:.1f} {yy:.1f} L{x+L:.1f} {yy:.1f}", BG * 1.2); x += L + r.uniform(6, 16)
    return g
def far_stones(r, y, gap):
    g = ""
    for x in (-112, -84, -58, 56, 82, 110):
        if gap and gap[0] - 10 < x < gap[1] + 10: continue
        h = r.uniform(7, 11); w = h * 0.7; b = y + r.uniform(-1, 1)
        g += path(f"M{x-w/2:.1f} {b:.1f} L{x-w/2:.1f} {b-h+w/2:.1f} Q{x-w/2:.1f} {b-h:.1f} {x:.1f} {b-h:.1f} Q{x+w/2:.1f} {b-h:.1f} {x+w/2:.1f} {b-h+w/2:.1f} L{x+w/2:.1f} {b:.1f}", BG * 1.1)
        if r.random() < 0.5: g += path(f"M{x:.1f} {b-h+2:.1f} l0 4 M{x-2:.1f} {b-h+3.5:.1f} l4 0", 0.8)
    return g

def compose(r, subject, sky_kind="none", side=1, forest_gap=None, solid=None, trees="pine", frame=True, kind="field", gx=(-30, 30), tree_top=0):
    """Background (sky, mountains, forest) is masked so the ground band and the subject cut a clean hole in it:
    nothing is painted in fabric color, so no flat boxes show on the garment. Ground is FLAT (no hill)."""
    SEQ[0] += 1; mid = f"vg{SEQ[0]}"
    fy = 182 if kind == "lake" else (198 if kind == "cemetery" else 200)
    back = (sky(r, sky_kind, side) if sky_kind != "none" else "") + mountains(r, 150 if kind != "lake" else 134) + forest_band(r, y=fy, gap=forest_gap)
    if kind == "lake": back += lake(r)
    if kind == "cemetery": back += far_stones(r, 203, forest_gap)
    front = ""
    if frame:                                                     # tall framing pines standing on the ground line (in front)
        a, b = r.uniform(-4, 4), r.uniform(-4, 4); H = lambda base, lo, hi: min(r.uniform(lo, hi), base - tree_top)
        wide_l, wide_r = gx[0] < -78, gx[1] > 78
        front += pine(-124 + a, 214, H(214, 142, 160), MG + 0.3) + pine(122 + b, 214, H(214, 142, 160), MG + 0.3)
        if not wide_l: front += pine(-100 + b, 208, H(208, 96, 116) * (0.75 if tree_top > 80 else 1), MG + 0.2)
        if not wide_r: front += pine(99 + a, 208, H(208, 92, 112) * (0.75 if tree_top > 80 else 1), MG + 0.2)
        front += tufts(r, (-124 + a, 122 + b), 214)
    band = f'<rect x="-200" y="{GROUND_Y + 1}" width="400" height="120" fill="#000"/>'
    mask = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-200" y="-60" width="400" height="360">'
            f'<rect x="-200" y="-60" width="400" height="360" fill="#fff"/>{band}{knockout(front, 4)}{knockout(subject)}{solid or ""}</mask>')
    return mask + f'<g mask="url(#{mid})">{back}</g>' + ground(r, kind, gx, side) + front + subject

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
    return g + barbell(x + 90 * s, y - 15 * s, 32, 0.75 * s)
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

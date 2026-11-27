"""Sketch set 3 (numbers 108-207): the 100 ideas in designs/ideas-100.md, drawn in the same style as 01-107.
Run: python3 tools/svgs_set3.py            -> designs/sketches/108-...svg ... 207-...svg
New art lives here and is added to svgs_dark.ICONS; colors come from svgs_dark (INK/FAB set per design)."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import svgs_dark as sd

def I(): return sd.INK
def B(): return sd.FAB
_num = re.compile(r"-?\d+(?:\.\d+)?")
def P(x, y, s, d):
    """Scale an absolute path written in icon units (M L Q C Z only): every number pair is a point."""
    out, nums = [], []
    for tok in re.findall(r"[MLQCZ]|-?\d+(?:\.\d+)?", d):
        if tok in "MLQCZ":
            out.append(tok)
        else:
            nums.append(float(tok))
            if len(nums) == 2:
                out.append(f"{x+nums[0]*s:.1f} {y+nums[1]*s:.1f}"); nums = []
    return " ".join(out)
def fp(x, y, s, d, fill=None, op=1):
    o = f' fill-opacity="{op}"' if op < 1 else ""
    return f'<path d="{P(x,y,s,d)}" fill="{fill or I()}"{o}/>'
def sp(x, y, s, d, w=4, c=None, dash=None, cap="round"):
    da = f' stroke-dasharray="{dash[0]*s:.1f} {dash[1]*s:.1f}"' if dash else ""
    return f'<path d="{P(x,y,s,d)}" fill="none" stroke="{c or I()}" stroke-width="{w*s:.1f}" stroke-linecap="{cap}" stroke-linejoin="round"{da}/>'
def ci(x, y, s, u, v, r, fill=None, stroke=None, w=0):
    st = f' stroke="{stroke}" stroke-width="{w*s:.1f}"' if stroke else ""
    return f'<circle cx="{x+u*s:.1f}" cy="{y+v*s:.1f}" r="{r*s:.1f}" fill="{fill or I()}"{st}/>'
def el(x, y, s, u, v, rx, ry, fill=None, rot=0):
    t = f' transform="rotate({rot} {x+u*s:.1f} {y+v*s:.1f})"' if rot else ""
    return f'<ellipse cx="{x+u*s:.1f}" cy="{y+v*s:.1f}" rx="{rx*s:.1f}" ry="{ry*s:.1f}" fill="{fill or I()}"{t}/>'
def rc(x, y, s, u, v, w, h, fill=None, rx=0, stroke=None, sw=0, rot=0):
    f = "none" if fill == "none" else (fill or I())
    st = f' stroke="{stroke}" stroke-width="{sw*s:.1f}"' if stroke else ""
    t = f' transform="rotate({rot} {x+(u+w/2)*s:.1f} {y+(v+h/2)*s:.1f})"' if rot else ""
    return f'<rect x="{x+u*s:.1f}" y="{y+v*s:.1f}" width="{w*s:.1f}" height="{h*s:.1f}" rx="{rx*s:.1f}" fill="{f}"{st}{t}/>'
def tx(x, y, s, u, v, text, size, font="osw", fill=None, anchor="middle", width=None):
    sz = sd.fitsize(text, font, width * s, size * s) if width else size * s
    return sd.tpath(text, font, sz, x + u * s, y + v * s, anchor=anchor, fill=fill)
def skull(x, y, s, u=0, v=0, k=1, **kw): return sd.skull(x + u * s, y + v * s, k * s, **kw)

# ---------- shared parts ----------
def ribcage(x, y, s=1, c=None, n=5, w=6):
    c = c or I(); g = ''
    g += ''.join(ci(x, y, s, 0, -62 + i * 13, 4.2, c) for i in range(11))
    for i in range(n):
        v = -52 + i * 21; L = 1 - i * 0.06
        for d in (-1, 1):
            g += sp(x, y, s, f"M{d*5} {v} C{d*58*L} {v-10} {d*70*L} {v+22} {d*44*L} {v+34}", w * (1 - i * 0.06), c)
    g += rc(x, y, s, -5, -58, 10, 52, c, 4)
    return g
def figure_lying(x, y, s=1, fill=None):
    return (el(x, y, s, -92, 0, 20, 17, fill) + fp(x, y, s, "M-74 -14 L60 -16 Q74 -16 76 -8 L120 -8 L120 8 L76 8 Q74 16 60 16 L-74 14 Z", fill))
def scythe(x, y, s=1, u=70):
    return (sp(x, y, s, f"M{u} -130 L{u} 100", 5) + fp(x, y, s, f"M{u} -130 Q{u-60} -150 {u-110} -112 Q{u-60} -128 {u} -116 Z"))
def reaper_body(x, y, s=1): return sd.reaper(x, y, s, spot=False)
def beetle(x, y, s=1, rot=0):
    g = (el(x, y, s, 0, 0, 11, 15) + ci(x, y, s, 0, -16, 6) + sp(x, y, s, "M0 -14 L0 14", 1.5, B()))
    for v in (-6, 2, 10):
        g += sp(x, y, s, f"M-9 {v} L-20 {v-6} M9 {v} L20 {v-6}", 2)
    g += sp(x, y, s, "M-3 -20 L-8 -30 M3 -20 L8 -30", 1.5)
    return f'<g transform="rotate({rot} {x:.1f} {y:.1f})">{g}</g>' if rot else g
def fly(x, y, s=1): return sd.flies(x, y, s, n=1, spread=1)
def bar(x, y, s=1, w=110, u=0, v=0): return sp(x, y, s, f"M{u-w} {v} L{u+w} {v}", 8)
def plates(x, y, s, u, v, k=1):
    return rc(x, y, s, u - 9 * k, v - 34 * k, 18 * k, 68 * k, None, 3) + rc(x, y, s, u - 6 * k + (14 if u > 0 else -14) * k, v - 26 * k, 12 * k, 52 * k, None, 3)
def muscle_lines(x, y, s, pts, c=None):
    return ''.join(sp(x, y, s, d, 1.6, c or B()) for d in pts)
def tray(x, y, s, u=0, v=0, w=180, h=26):
    return rc(x, y, s, u - w / 2, v, w, h, None, 4) + sp(x, y, s, f"M{u-w/2+8} {v+6} L{u+w/2-8} {v+6}", 1.5, B())
def candle_lit(x, y, s, u, v, h=60):
    return (rc(x, y, s, u - 12, v - h, 24, h, None, 2) + fp(x, y, s, f"M{u} {v-h-6} Q{u-9} {v-h-20} {u} {v-h-36} Q{u+9} {v-h-20} {u} {v-h-6} Z")
            + sp(x, y, s, f"M{u-12} {v-h+4} Q{u-16} {v-h+16} {u-14} {v-h+22}", 3))

# ---------- morgue / autopsy ----------
def organ_scale(x, y, s=1):
    g = sp(x, y, s, "M0 -96 L0 -78", 5) + ci(x, y, s, 0, -60, 22) + ci(x, y, s, 0, -60, 16, B())
    g += sp(x, y, s, "M0 -60 L10 -72", 2.5) + tx(x, y, s, 0, -44, "GRAMS", 7, fill=B())
    g += sp(x, y, s, "M0 -38 L0 -10 M0 -10 L-46 22 M0 -10 L46 22", 2.5)
    g += fp(x, y, s, "M-60 22 Q0 62 60 22 Z")
    g += fp(x, y, s, "M-44 18 C-48 -6 -10 -14 10 -4 C34 -16 52 0 42 14 C30 26 -30 30 -44 18 Z")
    g += sp(x, y, s, "M-30 10 Q0 2 30 8", 2, B())
    g += ''.join(fp(x, y, s, f"M{u} 40 Q{u-3} {40+L} {u} {44+L} Q{u+3} {40+L} {u} 40 Z") for u, L in ((-14, 18), (6, 28), (22, 12)))
    return g
def rib_spreader(x, y, s=1):
    g = ribcage(x, y, s, w=6.5)
    g += rc(x, y, s, -110, -16, 220, 12, None, 3) + rc(x, y, s, -102, -20, 20, 20, None, 3)
    for d in (-1, 1):
        g += fp(x, y, s, f"M{d*58} -10 L{d*58} 40 L{d*44} 40 L{d*44} -10 Z") + sp(x, y, s, f"M{d*50} 0 L{d*50} 34", 1.5, B())
    g += ''.join(sp(x, y, s, f"M{u} -22 L{u} -14", 1.5, B()) for u in range(-90, 100, 12))
    return g
def skull_saw(x, y, s=1):
    g = skull(x, y, s, 0, 0, 1.15, cracked=False)
    g += sp(x, y, s, "M-62 -30 Q0 -44 62 -30", 3, B(), dash=(7, 6))
    g += sp(x, y, s, "M-74 -32 Q0 -48 74 -32", 2, I(), dash=(7, 6))
    g += tx(x, y, s, 92, -52, "CUT", 12, anchor="start") + sp(x, y, s, "M76 -38 L88 -48", 2)
    return g
def brain_jar(x, y, s=1):
    g = rc(x, y, s, -60, -88, 120, 16, None, 4) + rc(x, y, s, -56, -72, 112, 152, "none", 16, I(), 6)
    g += rc(x, y, s, -50, -40, 100, 114, I(), 10) if False else ''
    g += sp(x, y, s, "M-50 -40 L50 -40", 2, dash=(4, 4))
    g += sd.brain(x, y + 14 * s, 0.85 * s)
    g += ''.join(ci(x, y, s, u, v, 3, None, None) for u, v in ((-36, -24), (30, -30), (40, 52), (-40, 50)))
    g += rc(x, y, s, -34, 58, 68, 16, None, 2) + tx(x, y, s, 0, 70, "SPECIMEN", 9, fill=B(), width=60)
    return g
def slabs(x, y, s=1):
    g = ''
    for k, u in enumerate((-70, 70)):
        g += rc(x, y, s, u - 62, 34, 124, 10, None, 2) + sp(x, y, s, f"M{u-50} 44 L{u-50} 80 M{u+50} 44 L{u+50} 80", 4)
        g += f'<g transform="rotate(-90 {x+u*s:.1f} {y+28*s:.1f})">' + sd.skeleton(x + u * s - 20 * s, y + 28 * s - 76 * s, 0.62 * s) + '</g>'
        g += rc(x, y, s, u + 46, 2, 16, 12, None, 2) + tx(x, y, s, u + 54, -4, f"{k+17:02d}", 9)
    return g
def embalm(x, y, s=1):
    g = rc(x, y, s, -96, -60, 64, 92, None, 6) + ci(x, y, s, -64, -32, 14, B()) + sp(x, y, s, "M-64 -32 L-56 -42", 2.5)
    g += tx(x, y, s, -64, 16, "PUMP", 11, fill=B())
    g += rc(x, y, s, -86, -86, 44, 26, None, 4) + rc(x, y, s, -80, -82, 32, 18, "none", 3, B(), 2)
    g += sp(x, y, s, "M-32 -20 C10 -20 0 40 40 40 L96 40", 4)
    g += sp(x, y, s, "M-32 0 C0 0 -10 70 30 70 L96 70", 4)
    g += figure_lying(x + 40 * s, y + 55 * s, 0.4 * s)
    g += sd.bottle(x + 60 * s, y - 40 * s, 0.6 * s)
    return g
def lividity(x, y, s=1):
    g = sp(x, y, s, "M-120 -2 Q-120 -26 -96 -26 Q-74 -26 -74 -12 L60 -16 Q78 -16 80 -8 L124 -8 L124 10 L80 10 Q78 22 60 22 L-74 20 Q-74 24 -96 24 Q-120 24 -120 -2", 3)
    g += f'<path d="{P(x,y,s,"M-116 8 Q-96 26 -76 14 L60 18 Q76 18 80 8 L122 8 L122 10 L80 10 Q78 22 60 22 L-74 20 Q-74 24 -96 24 Q-114 22 -116 8 Z")}" fill="{sd.RED}"/>'
    g += ''.join(ci(x, y, s, u, 14, 2.5, sd.RED) for u in range(-60, 60, 14))
    g += sp(x, y, s, "M-140 40 L140 40", 5)
    return g
def thermo(x, y, s=1):
    g = rc(x, y, s, -12, -96, 24, 120, "none", 12, I(), 6) + rc(x, y, s, -5, -20, 10, 46, None, 4)
    g += skull(x, y, s, 0, 54, 0.62, cracked=False)
    for i, t in enumerate(("98.6", "80", "60", "38")):
        v = -86 + i * 22
        g += sp(x, y, s, f"M14 {v} L30 {v}", 2.5) + tx(x, y, s, 36, v + 5, t + "°", 12, anchor="start")
    g += fp(x, y, s, "M-24 -70 L-40 -64 L-24 -58 Z") + tx(x, y, s, -46, -60, "-1.5/HR", 10, anchor="end")
    return g
def jaw_xray(x, y, s=1):
    g = rc(x, y, s, -110, -70, 220, 140, None, 10)
    g += fp(x, y, s, "M-90 -10 Q-90 50 0 56 Q90 50 90 -10 L74 -10 Q70 34 0 38 Q-70 34 -74 -10 Z", B())
    for i in range(14):
        u = -80 + i * 12.3; v = -24 + abs(u) * 0.08
        g += rc(x, y, s, u - 4.5, v - 22, 9, 22, B(), 3) + sp(x, y, s, f"M{u-2} {v} L{u-2} {v+10} M{u+2} {v} L{u+2} {v+12}", 1.8, B())
    g += rc(x, y, s, 50, -62, 52, 14, B(), 2) + tx(x, y, s, 76, -51, "ID: 4471", 9, width=46)
    return g
def triptych(x, y, s=1):
    g = ''
    for u in (-80, 0, 80):
        g += rc(x, y, s, u - 36, -56, 72, 112, "none", 6, I(), 3)
    g += sd.toe_tag(x - 80 * s, y, 0.36 * s)
    g += sd.body_bag(x, y, 0.29 * s)
    g += rc(x, y, s, 54, -4, 52, 10, None, 3) + figure_lying(x + 80 * s, y - 14 * s, 0.22 * s)
    g += sp(x, y, s, "M58 6 L58 36 M102 6 L102 36", 3) + ci(x, y, s, 58, 40, 4) + ci(x, y, s, 102, 40, 4)
    g += ''.join(tx(x, y, s, u, 72, t, 11) for u, t in ((-80, "1"), (0, "2"), (80, "3")))
    return g
def layers(x, y, s=1):
    g = ''
    names = ("SKIN", "FAT", "MUSCLE", "BONE")
    for i, n in enumerate(names):
        u = -96 + i * 18; v = -60 + i * 10
        g += fp(x, y, s, f"M{u} {v} L{u+150} {v-20} L{u+170} {v+80} L{u+20} {v+100} Z", I() if i % 2 == 0 else sd.shade(I(), 0.8))
        g += sp(x, y, s, f"M{u} {v} L{u+150} {v-20}", 2, B())
        g += tx(x, y, s, u + 8, v + 24, n, 10, fill=B(), anchor="start")
    g += muscle_lines(x, y, s, ["M-20 0 L110 -14", "M-16 12 L112 -2", "M-12 24 L114 10"])
    g += fp(x, y, s, "M0 60 Q60 40 120 50 L124 66 Q60 58 4 76 Z", B())
    return g

# ---------- decay ----------
def bloat(x, y, s=1):
    g = el(x, y, s, -92, 10, 20, 18) + fp(x, y, s, "M-74 0 Q-60 -60 0 -62 Q70 -60 80 -6 L124 -4 L124 14 L80 14 Q60 34 -74 26 Z")
    g += sp(x, y, s, "M-40 -30 Q0 -48 40 -30", 2, B()) + sp(x, y, s, "M-30 -12 Q0 -24 30 -12", 2, B())
    g += sp(x, y, s, "M-140 40 L140 40", 5)
    g += sd.flies(x, y - 60 * s, s, n=7, spread=120)
    return g
def skin_glove(x, y, s=1):
    g = ''
    for i, (ang, L) in enumerate(((-40, 44), (-16, 58), (0, 62), (16, 56), (36, 40))):
        a = math.radians(ang - 90); bx = -24 + i * 12
        g += sd.bone(x + bx * s, y - 10 * s, x + (bx + math.cos(a) * L) * s, y + (-10 + math.sin(a) * L) * s, 7 * s)
    g += fp(x, y, s, "M-36 -14 L36 -14 L30 30 L-30 30 Z")
    g += sd.bone(x - 12 * s, y + 30 * s, x - 12 * s, y + 92 * s, 9 * s) + sd.bone(x + 12 * s, y + 30 * s, x + 12 * s, y + 92 * s, 9 * s)
    g += fp(x, y, s, "M40 -8 Q70 -30 98 -18 Q110 -6 104 12 L96 40 Q80 52 70 36 Q60 60 44 48 Q36 30 40 -8 Z")
    g += ''.join(fp(x, y, s, f"M{u} -16 Q{u+4} -46 {u+12} -50 Q{u+18} -44 {u+12} -14 Z") for u in (54, 70, 86))
    g += sp(x, y, s, "M46 0 Q70 10 96 2", 2, B()) + sp(x, y, s, "M50 20 L58 26 L66 18 L74 28 L82 20 L90 30", 2, B())
    return g
def marbled(x, y, s=1):
    g = fp(x, y, s, "M-70 -80 Q0 -96 70 -80 L80 -40 Q66 0 64 40 L60 86 L-60 86 L-64 40 Q-66 0 -80 -40 Z")
    import random; r = random.Random(7)
    for k in range(9):
        u, v = r.randint(-50, 50), r.randint(-70, 70)
        d = f"M{u} {v}"
        for j in range(5):
            u += r.randint(-18, 18); v += r.randint(-14, 14); d += f" L{u} {v}"
        g += sp(x, y, s, d, 1.6, B())
    g += sp(x, y, s, "M-40 -50 Q0 -40 40 -50", 2.4, B())
    return g
def big_fly(x, y, s=1):
    g = el(x, y, s, 0, 22, 22, 46) + ci(x, y, s, 0, -34, 22) + el(x, y, s, -12, -38, 10, 12, sd.RED) + el(x, y, s, 12, -38, 10, 12, sd.RED)
    for d in (-1, 1):
        g += f'<path d="{P(x,y,s,f"M{d*8} -6 Q{d*100} -70 {d*112} -10 Q{d*90} 30 {d*10} 6 Z")}" fill="{I()}" fill-opacity=".55"/>'
        g += sp(x, y, s, f"M{d*14} -2 Q{d*70} -40 {d*100} -16 M{d*20} 2 Q{d*60} 0 {d*96} -4", 1.4, B())
        for v in (0, 20, 40):
            g += sp(x, y, s, f"M{d*18} {v} L{d*40} {v+14} L{d*46} {v+40}", 2.5)
    g += ''.join(sp(x, y, s, f"M-18 {v} L18 {v}", 1.6, B()) for v in (16, 30, 44, 58))
    g += sp(x, y, s, "M-80 70 L-40 70 M-80 66 L-80 74 M-40 66 L-40 74", 1.5) + tx(x, y, s, -60, 84, "PL. 7", 9)
    return g
def cycle(x, y, s=1):
    g = skull(x, y, s, 0, 0, 0.55, cracked=False)
    g += sp(x, y, s, "M0 -78 Q78 -78 78 0 Q78 78 0 78 Q-78 78 -78 0 Q-78 -78 0 -78", 2, dash=(5, 5))
    g += el(x, y, s, 0, -78, 4, 7) + el(x, y, s, 4, -72, 4, 7)
    g += fp(x, y, s, "M70 -10 Q86 -4 84 12 Q80 22 70 18 Q76 6 66 -2 Z")
    g += el(x, y, s, 0, 78, 8, 16, rot=90)
    g += fly(x - 78 * s, y, 1.2 * s)
    g += ''.join(tx(x, y, s, u, v, t, 9, anchor=a) for u, v, t, a in ((14, -82, "EGG", "start"), (92, 6, "LARVA", "start"), (0, 104, "PUPA", "middle"), (-96, 6, "FLY", "end")))
    return g
def beetle_skull(x, y, s=1):
    g = skull(x, y, s, 0, 0, 1.05, cracked=False)
    for u, v, r in ((-30, -40, 30), (26, -48, -20), (40, -10, 60), (-44, 10, -60), (6, 36, 10), (-16, -60, 80)):
        g += beetle(x + u * s, y + v * s, 0.55 * s, r)
    g += ''.join(beetle(x + u * s, y + 84 * s, 0.95 * s, 90) for u in (-80, -20, 40, 100))
    return g
def wax_grave(x, y, s=1):
    g = fp(x, y, s, "M-130 -30 L130 -30 L110 60 L-110 60 Z") + fp(x, y, s, "M-104 -16 L104 -16 L90 46 L-90 46 Z", B())
    g += figure_lying(x - 6 * s, y + 18 * s, 0.7 * s, sd.shade(I(), 0.85) if sum(int(I()[i:i+2], 16) for i in (1, 3, 5)) > 300 else I())
    g += ''.join(ci(x, y, s, u, 18 + (u % 7), 3, B()) for u in range(-60, 60, 15))
    g += sp(x, y, s, "M100 -30 L130 -110", 5) + fp(x, y, s, "M92 -34 L112 -30 L104 -4 L94 -6 Z")
    return g
def mummy_hand(x, y, s=1):
    g = sd.bone(x - 12 * s, y + 40 * s, x - 12 * s, y + 96 * s, 10 * s) + sd.bone(x + 12 * s, y + 40 * s, x + 12 * s, y + 96 * s, 10 * s)
    g += fp(x, y, s, "M-44 -10 Q-46 40 -24 46 L24 46 Q46 40 40 -10 Z")
    for i, (u, ang) in enumerate(((-34, -150), (-18, -100), (0, -92), (18, -84), (34, -60))):
        a = math.radians(ang); L = (40, 64, 70, 62, 44)[i]
        mx, my = u + math.cos(a) * L * 0.5, -10 + math.sin(a) * L * 0.5
        ex, ey = mx + math.cos(a + 0.9) * L * 0.4, my + math.sin(a + 0.9) * L * 0.4
        g += sp(x, y, s, f"M{u} -10 L{mx:.0f} {my:.0f} L{ex:.0f} {ey:.0f}", 11)
    g += muscle_lines(x, y, s, ["M-30 0 Q-20 20 -26 40", "M-6 -4 Q0 20 -6 42", "M16 -4 Q22 20 16 42", "M-36 20 L36 22"])
    g += ''.join(sp(x, y, s, f"M{u} {v} L{u+4} {v+4}", 1.4, B()) for u, v in ((-20, 4), (4, 10), (24, 16), (-10, 30)))
    return g
def stain(x, y, s=1):
    g = ''
    for u in range(-130, 131, 13):
        g += fp(x, y, s, f"M{u} 34 L{u+3} 20 L{u+5} 34 L{u+8} 24 L{u+9} 34 Z")
    g += fp(x, y, s, "M-130 34 L130 34 L130 80 L-130 80 Z")
    g += fp(x, y, s, "M-100 50 Q-110 44 -100 40 Q-84 36 -72 44 L60 40 Q90 36 104 42 Q112 48 104 56 Q90 64 60 60 L-72 62 Q-90 64 -100 50 Z", B())
    g += ''.join(ci(x, y, s, u, v, 2, B()) for u, v in ((-120, 70), (-40, 72), (30, 70), (110, 66), (80, 74)))
    g += ''.join(sp(x, y, s, f"M{u} 34 Q{u+4} -10 {u+14} -30", 2.5) for u in (-80, -20, 50))
    g += ''.join(el(x, y, s, u + 14, -32, 5, 9, rot=20) for u in (-80, -20, 50))
    return g
def shroom_ribs(x, y, s=1):
    g = ribcage(x, y + 10 * s, s * 0.9)
    for u, v, k in ((-30, -64, 1), (24, -70, 0.8), (54, -40, 0.6), (-58, -36, 0.7), (4, -92, 0.6)):
        g += sp(x, y, s, f"M{u} {v+30*k} L{u} {v}", 6 * k) + fp(x, y, s, f"M{u-22*k} {v} Q{u} {v-28*k} {u+22*k} {v} Z")
        g += ''.join(ci(x, y, s, u + d * 8 * k, v - 8 * k, 2.5 * k, B()) for d in (-1, 1))
    g += sp(x, y, s, "M-120 74 L120 74", 5)
    return g
def root_skull(x, y, s=1):
    g = skull(x, y, s, 0, -10, 1.0, cracked=False)
    for d in ("M-20 -80 Q-30 -40 -60 -10 Q-90 20 -110 70", "M10 -82 Q30 -50 20 -20 Q10 20 40 50 Q60 70 100 80",
              "M-40 -60 Q-70 -80 -110 -70", "M40 -60 Q80 -70 110 -50", "M-10 30 Q-20 60 -50 90", "M20 40 Q40 70 30 96"):
        g += sp(x, y, s, d, 4)
    g += sp(x, y, s, "M0 -80 L0 -98", 7) + ''.join(el(x, y, s, u, v, 9, 4.5, rot=r) for u, v, r in ((-12, -92, -30), (12, -98, 30)))
    return g
def eye_beetle(x, y, s=1):
    g = skull(x, y, s, 0, 0, 1.15, cracked=False)
    g += beetle(x - 24 * s, y - 6 * s, 0.75 * s, -20)
    g += ''.join(beetle(x + u * s, y + v * s, 0.8 * s, r) for u, v, r in ((-96, -40, -60), (90, -20, 50), (-80, 50, -120), (84, 60, 140)))
    return g
def stages(x, y, s=1):
    g = ''
    names = ("FRESH", "BLOAT", "ACTIVE", "ADV.", "DRY")
    for i, n in enumerate(names):
        u = -112 + i * 56
        g += rc(x, y, s, u - 26, -60, 52, 112, "none", 4, I(), 2.5)
        if i < 4:
            k = (0.9, 1.25, 0.9, 0.7)[i]
            g += el(x, y, s, u, -40, 9, 9) + fp(x, y, s, f"M{u-10*k} -30 L{u+10*k} -30 L{u+8*k} 30 L{u-8*k} 30 Z")
            if i >= 2: g += ''.join(sp(x, y, s, f"M{u-6} {v} L{u+6} {v}", 1.5, B()) for v in (-20, -10, 0))
            if i == 1: g += fly(x + (u + 16) * s, y - 54 * s, 0.6 * s)
        else:
            g += sd.skeleton(x + u * s, y - 48 * s, 0.38 * s)
        g += tx(x, y, s, u, 72, n, 9, width=50)
    return g
def petri(x, y, s=1):
    g = ci(x, y, s, 0, 0, 80, "none", I(), 6) + ci(x, y, s, 0, 0, 70, "none", I(), 2)
    g += fp(x, y, s, "M-30 -40 Q20 -60 34 -20 Q46 14 20 30 Q40 50 10 52 Q-20 54 -16 30 Q-50 20 -40 -10 Q-46 -30 -30 -40 Z")
    import random; r = random.Random(3)
    g += ''.join(ci(x, y, s, r.randint(-55, 55), r.randint(-55, 55), r.choice((2, 3, 4))) for _ in range(30))
    g += ''.join(ci(x, y, s, r.randint(-20, 20), r.randint(-30, 30), 2.2, B()) for _ in range(10))
    return g
def crow_ribs(x, y, s=1):
    g = f'<g transform="rotate(-90 {x:.1f} {y+30*s:.1f})">' + ribcage(x, y + 30 * s, 0.75 * s) + '</g>'
    g += sd.raven(x - 50 * s, y - 20 * s, 0.6 * s) + sd.raven(x + 60 * s, y - 34 * s, 0.5 * s)
    g += sp(x, y, s, "M-130 80 L130 80", 5)
    return g

# ---------- anatomy / gym ----------
def flayed_arm(x, y, s=1):
    g = fp(x, y, s, "M-110 70 Q-60 40 -10 50 L-4 74 Q-60 80 -110 96 Z")
    g += fp(x, y, s, "M-16 52 Q-30 0 -6 -46 L18 -40 Q8 10 14 60 Z")
    g += muscle_lines(x, y, s, ["M-100 76 Q-60 60 -14 60", "M-96 86 Q-60 72 -12 70", "M-10 40 Q-14 0 0 -34", "M2 44 Q0 10 10 -36"])
    g += sd.bone(x - 2 * s, y - 50 * s, x + 6 * s, y - 70 * s, 9 * s)
    g += sd.dumbbell(x + 4 * s, y - 80 * s, 0.6 * s)
    g += ''.join(fp(x, y, s, f"M{u} {v} Q{u-3} {v+L} {u} {v+L+4} Q{u+3} {v+L} {u} {v} Z") for u, v, L in ((-70, 92, 18), (-40, 86, 26), (6, 66, 14)))
    return g
def torn_bicep(x, y, s=1):
    g = fp(x, y, s, "M-120 -20 Q-60 -70 10 -40 L14 -10 Q-60 -20 -120 10 Z")
    g += fp(x, y, s, "M20 -40 Q60 -30 110 10 L96 30 Q60 0 24 -6 Z")
    g += muscle_lines(x, y, s, ["M-110 -10 Q-60 -40 6 -26", "M-104 2 Q-60 -26 8 -16"])
    g += sp(x, y, s, "M14 -26 Q30 -60 60 -50 Q74 -40 64 -24", 4) + sp(x, y, s, "M60 -50 L70 -60 M64 -24 L76 -24", 2)
    g += sd.bone(x - 110 * s, y + 40 * s, x + 100 * s, y + 50 * s, 10 * s)
    g += ''.join(fp(x, y, s, f"M{u} {v} Q{u-3} {v+L} {u} {v+L+4} Q{u+3} {v+L} {u} {v} Z", sd.RED) for u, v, L in ((10, -8, 22), (22, -4, 30)))
    g += tx(x, y, s, 74, -62, "SNAP", 12, anchor="start")
    return g
def spine_bar(x, y, s=1):
    g = rc(x, y, s, -60, -86, 120, 176, None, 8)
    for i in range(9):
        v = -60 + i * 17
        g += rc(x, y, s, -16 + i * 0.5, v, 32 - i * 0.2, 12, B(), 3) + sp(x, y, s, f"M-16 {v+6} L-28 {v+2} M16 {v+6} L28 {v+2}", 3, B())
    g += sp(x, y, s, "M-130 -70 L130 -70", 9)
    g += plates(x, y, s, -112, -70) + plates(x, y, s, 112, -70)
    g += fp(x, y, s, "M-10 -50 L0 -40 L10 -50 Z", sd.RED)
    return g
def ecorche_squat(x, y, s=1):
    g = sd.skeleton(x, y - 92 * s, 0.9 * s, "sit")
    g += sd.barbell(x, y - 70 * s, 0.75 * s)
    g += fp(x, y, s, "M-28 -24 Q-40 30 -30 58 L-18 56 Q-24 30 -14 -20 Z", op=1) + fp(x, y, s, "M28 -24 Q40 30 30 58 L18 56 Q24 30 14 -20 Z")
    g += fp(x, y, s, "M-30 24 Q-46 44 -36 66 L-24 64 Q-30 46 -20 28 Z") + fp(x, y, s, "M30 24 Q46 44 36 66 L24 64 Q30 46 20 28 Z")
    g += muscle_lines(x, y, s, ["M-26 -10 L-22 40", "M26 -10 L22 40"])
    return g
def heart_plates(x, y, s=1):
    g = sd.anatomical_heart(x, y, 0.9 * s, drips=False)
    g += sp(x, y, s, "M-40 -50 L-110 -50 M40 -50 L110 -50", 7)
    g += plates(x, y, s, -112, -50, 0.8) + plates(x, y, s, 112, -50, 0.8)
    return g
def torn_palm(x, y, s=1):
    g = ''
    for d in (-1, 1):
        u = d * 56
        g += fp(x, y, s, f"M{u-34} 70 L{u-36} -10 Q{u-34} -30 {u-26} -30 L{u+26} -30 Q{u+34} -30 {u+36} -10 L{u+34} 70 Z")
        for k, (fu, L) in enumerate(((-26, 34), (-9, 44), (9, 42), (25, 32))):
            g += rc(x, y, s, u + fu - 7, -30 - L, 14, L + 4, None, 7)
        g += fp(x, y, s, f"M{u-22} -8 Q{u} -18 {u+22} -8 Q{u+10} 6 {u-8} 2 Z", sd.RED)
        g += fp(x, y, s, f"M{u-18} 10 L{u-4} 6 L{u-8} 18 Z", sd.RED)
        g += sp(x, y, s, f"M{u-20} 30 Q{u} 40 {u+22} 26", 1.6, B())
    return g
def same_bones(x, y, s=1):
    g = sd.skeleton(x, y - 92 * s, 0.85 * s, "carry")
    g += sp(x, y, s, "M-120 -12 L120 -12", 6)
    g += ''.join(sd.bone(x + u * s, y - 40 * s, x + u * s, y + 16 * s, 12 * s) for u in (-112, -96, 96, 112))
    return g
def knee(x, y, s=1):
    g = sd.bone(x, y - 96 * s, x, y - 18 * s, 34 * s) + sd.bone(x - 4 * s, y + 18 * s, x - 4 * s, y + 96 * s, 30 * s)
    g += el(x, y, s, 26, -6, 14, 20)
    g += fp(x, y, s, "M-30 -14 Q0 -4 30 -14 L30 -6 Q0 4 -30 -6 Z", B()) + fp(x, y, s, "M-28 10 Q0 2 28 10 L28 16 Q0 8 -28 16 Z", B())
    g += sp(x, y, s, "M-40 -4 Q-60 0 -70 10 M-40 4 Q-60 10 -72 24", 3)
    g += tx(x, y, s, -76, 18, "0 MM", 11, anchor="end")
    return g
def fibers(x, y, s=1):
    g = fp(x, y, s, "M-120 -30 Q0 -80 120 -30 L120 30 Q0 80 -120 30 Z")
    g += ''.join(sp(x, y, s, f"M-112 {v} Q0 {v*1.6} 112 {v}", 1.6, B()) for v in (-20, -10, 0, 10, 20))
    g += ''.join(sd.flame(x + u * s, y + v * s, 0.32 * s) for u, v in ((-60, -48), (0, -66), (60, -48)))
    return g
def thigh_section(x, y, s=1):
    g = fp(x, y, s, "M-90 0 Q-90 -70 0 -76 Q96 -70 92 0 Q88 70 0 74 Q-86 70 -90 0 Z")
    g += fp(x, y, s, "M-80 0 Q-78 -60 0 -64 Q82 -60 80 0 Q76 60 0 62 Q-76 60 -80 0 Z", B()) + fp(x, y, s, "M-74 0 Q-72 -54 0 -58 Q76 -54 74 0 Q70 54 0 56 Q-70 54 -74 0 Z")
    g += sp(x, y, s, "M-40 -50 Q-10 -10 -50 30 M10 -56 Q0 -20 40 10 M50 -30 Q20 20 30 50 M-60 -10 L-10 10", 2, B())
    g += ci(x, y, s, 6, 4, 16, B()) + ci(x, y, s, 6, 4, 8)
    for k, (u, v, n) in enumerate(((-40, -30, "1"), (30, -26, "2"), (40, 30, "3"), (-36, 30, "4"))):
        g += sp(x, y, s, f"M{u} {v} L{u + (-70 if u < 0 else 70)} {v}", 1.2) + tx(x, y, s, u + (-76 if u < 0 else 76), v + 4, n, 11, anchor="end" if u < 0 else "start")
    return g
def sutured_heart(x, y, s=1):
    g = sd.anatomical_heart(x, y, s, drips=False)
    g += sp(x, y, s, "M-30 -20 Q0 10 6 60", 2.6, B())
    g += ''.join(sp(x, y, s, f"M{u-10} {v-4} L{u+10} {v+4}", 2.6, B()) for u, v in ((-24, -12), (-12, 6), (-2, 24), (2, 42)))
    return g
def microtear(x, y, s=1):
    g = ''
    for i, v in enumerate((-48, -24, 0, 24, 48)):
        if i == 2:
            g += fp(x, y, s, f"M-120 {v-9} L-14 {v-9} L-4 {v} L-14 {v+9} L-120 {v+9} Z") + fp(x, y, s, f"M120 {v-9} L18 {v-9} L8 {v} L18 {v+9} L120 {v+9} Z")
            g += ''.join(sp(x, y, s, f"M{u} {v-6} L{u+6} {v+6}", 1.4, B()) for u in (-10, 4))
        else:
            g += rc(x, y, s, -120, v - 9, 240, 18, None, 9) + ''.join(sp(x, y, s, f"M{u} {v-7} L{u} {v+7}", 1.2, B()) for u in range(-108, 110, 16))
    g += tx(x, y, s, 0, 82, "MICROTEAR, 400X", 10)
    return g
def nerves(x, y, s=1):
    g = skull(x, y, s, 0, -82, 0.3, cracked=False) + sp(x, y, s, "M0 -66 L0 30", 6)
    import random; r = random.Random(11)
    for v in range(-56, 30, 12):
        for d in (-1, 1):
            u2, v2 = d * r.randint(40, 90), v + r.randint(-6, 30)
            g += sp(x, y, s, f"M0 {v} Q{d*20} {v} {u2} {v2}", 2.2, sd.RED if v % 24 == 0 else I())
            g += sp(x, y, s, f"M{u2} {v2} L{u2+d*12} {v2+10}", 1.4)
    g += sp(x, y, s, "M0 30 Q-20 60 -30 100 M0 30 Q20 60 30 100", 4)
    return g
def molars(x, y, s=1):
    g = ''
    for d in (-1, 1):
        u = d * 42
        g += fp(x, y, s, f"M{u-36} -40 Q{u-38} -66 {u-20} -66 Q{u} -58 {u+20} -66 Q{u+38} -66 {u+36} -40 L{u+30} 10 Q{u+26} 70 {u+12} 76 Q{u+4} 40 {u} 20 Q{u-4} 40 {u-12} 76 Q{u-26} 70 {u-30} 10 Z")
        g += sp(x, y, s, f"M{u-6} -64 L{u+4} -40 L{u-6} -20 L{u+6} 0 L{u-2} 24", 3.2, B())
    g += sp(x, y, s, "M-100 -76 L100 -76", 4) + ''.join(sp(x, y, s, f"M{u} -86 L{u+10} -96", 2) for u in (-60, -20, 20, 60))
    return g
def spine_yoke(x, y, s=1):
    g = ''.join(rc(x, y, s, -15, -66 + i * 17, 30, 13, None, 4) + sp(x, y, s, f"M-15 {-60+i*17} L-30 {-64+i*17} M15 {-60+i*17} L30 {-64+i*17}", 4) for i in range(9))
    g += sp(x, y, s, "M-130 -80 L130 -80", 9) + plates(x, y, s, -112, -80) + plates(x, y, s, 112, -80)
    g += fp(x, y, s, "M-26 90 Q0 70 26 90 Q20 104 0 100 Q-20 104 -26 90 Z")
    g += ''.join(sp(x, y, s, f"M{d*36} {v} L{d*48} {v+4}", 2) for d in (-1, 1) for v in (-30, -10, 10))
    return g
def skinless_face(x, y, s=1):
    g = skull(x, y, s, 0, 0, 1.25, cracked=False)
    for d in (-1, 1):
        g += fp(x, y, s, f"M{d*56} -20 Q{d*66} 20 {d*44} 52 L{d*36} 50 Q{d*50} 20 {d*46} -16 Z")
        g += muscle_lines(x, y, s, [f"M{d*54} -10 Q{d*58} 20 {d*42} 46"])
    g += ''.join(rc(x, y, s, u - 4, 44, 8, 16, B(), 2) for u in range(-30, 34, 10))
    g += sp(x, y, s, "M-38 52 L38 52", 1.5)
    return g
def rib_rack(x, y, s=1):
    g = ribcage(x, y, s * 1.1, w=7)
    g += sp(x, y, s, "M-90 -100 L-90 90 M90 -100 L90 90", 8) + sp(x, y, s, "M-110 90 L110 90", 6)
    g += sp(x, y, s, "M-120 -46 L120 -46", 7) + plates(x, y, s, -112, -46, 0.7) + plates(x, y, s, 112, -46, 0.7)
    g += ''.join(rc(x, y, s, d * 90 - 10, -44, 20, 8, None, 2) for d in (-1, 1))
    return g
def vials(x, y, s=1):
    g = rc(x, y, s, -96, 30, 192, 12, None, 3) + sp(x, y, s, "M-90 42 L-90 80 M90 42 L90 80", 5)
    for u, t, lvl in ((-56, "BLOOD", 0.7), (0, "SWEAT", 0.5), (56, "LYMPH", 0.6)):
        g += rc(x, y, s, u - 14, -80, 28, 140, "none", 14, I(), 4) + rc(x, y, s, u - 16, -90, 32, 14, None, 3)
        h = 120 * lvl; g += rc(x, y, s, u - 10, 54 - h, 20, h, sd.RED if t == "BLOOD" else I(), 9)
        g += tx(x, y, s, u, 74, t, 9, width=48)
    return g
def butcher(x, y, s=1):
    g = skull(x, y, s, 0, -88, 0.36, cracked=False)
    body = "M-20 -70 L-56 -60 Q-70 -54 -70 -36 L-76 20 L-62 22 L-52 -26 L-42 4 L-36 46 L-32 104 L-10 104 L-4 50 L4 50 L10 104 L32 104 L36 46 L42 4 L52 -26 L62 22 L76 20 L70 -36 Q70 -54 56 -60 L20 -70 Z"
    g += fp(x, y, s, body)
    g += sp(x, y, s, "M-62 -36 L62 -36 M-44 0 L44 0 M-38 24 L38 24 M0 -66 L0 24 M-34 60 L-6 60 M6 60 L34 60", 2, B(), dash=(5, 4))
    for u, v, t in ((-30, -46, "CHUCK"), (30, -46, "RIB"), (-22, 14, "LOIN"), (22, 14, "FLANK"), (-20, 84, "SHANK"), (20, 84, "SHANK")):
        g += tx(x, y, s, u, v, t, 8, fill=B(), width=34)
    return g

# ---------- burial / funeral ----------
def grave_tape(x, y, s=1):
    g = sd.open_grave(x, y + 40 * s, 0.9 * s)
    g += rc(x, y, s, -44, -10, 14, 90, None, 2) + ''.join(sp(x, y, s, f"M-30 {v} L-38 {v}", 1.5, B()) for v in range(-4, 76, 8))
    g += tx(x, y, s, -52, 36, "6 FT", 12, anchor="end")
    return g
def nailed(x, y, s=1):
    g = f'<g transform="rotate(-90 {x:.1f} {y:.1f})">' + sd.coffin(x, y, 0.9 * s) + '</g>'
    g += ''.join(sp(x, y, s, f"M{u} -60 L{u} -40", 3) + rc(x, y, s, u - 5, -64, 10, 4) for u in (-50, -10, 30, 70))
    g += f'<g transform="rotate(-30 {x+90*s:.1f} {y-70*s:.1f})">' + rc(x, y, s, 86, -120, 8, 70, None, 3) + rc(x, y, s, 70, -126, 40, 14, None, 3) + '</g>'
    return g
def lowering(x, y, s=1):
    g = fp(x, y, s, "M-130 40 L-60 40 L-60 90 L60 90 L60 40 L130 40 L130 50 L70 50 L70 100 L-70 100 L-70 50 L-130 50 Z")
    g += rc(x, y, s, -56, 4, 112, 34, None, 8) + sp(x, y, s, "M-50 14 L50 14", 1.5, B())
    g += sp(x, y, s, "M-40 4 L-40 -50 M40 4 L40 -50", 3) + sp(x, y, s, "M-90 -50 L90 -50", 5)
    g += sp(x, y, s, "M-90 -50 L-90 40 M90 -50 L90 40", 5)
    return g
def shovel_pile(x, y, s=1):
    g = fp(x, y, s, "M-130 80 Q-60 -40 0 -30 Q60 -40 130 80 Z")
    g += ''.join(ci(x, y, s, u, v, 3, B()) for u, v in ((-60, 30), (-20, 10), (20, 40), (60, 20), (0, 60), (-80, 60), (90, 60)))
    g += sp(x, y, s, "M20 -30 L50 -120", 6) + fp(x, y, s, "M4 -36 L36 -24 L24 24 Q10 30 0 20 Z") + sp(x, y, s, "M40 -126 L62 -118", 8)
    return g
def markers(x, y, s=1):
    g = ''
    for r, v in enumerate((-50, 20)):
        for k in range(5):
            u = -100 + k * 50 + (r * 25 - 12)
            n = 1100 + r * 5 + k * 7
            g += rc(x, y, s, u - 16, v - 30, 32, 40, None, 2) + tx(x, y, s, u, v - 4, str(n), 10, fill=B(), width=26)
            g += sp(x, y, s, f"M{u-24} {v+12} L{u+24} {v+12}", 2)
    return g
def robber(x, y, s=1):
    g = fp(x, y, s, "M-120 20 L30 6 L60 40 L-90 54 Z")
    g += fp(x, y, s, "M-60 4 L-30 -40 L20 -48 L10 0 Z", op=0.85)
    g += sp(x, y, s, "M-100 26 L40 12", 2, B())
    g += sp(x, y, s, "M70 50 L110 -90", 5) + fp(x, y, s, "M62 54 L84 58 L76 82 L64 78 Z")
    g += rc(x, y, s, -110, -70, 30, 40, "none", 3, I(), 4) + fp(x, y, s, "M-95 -40 Q-104 -50 -95 -64 Q-86 -50 -95 -40 Z", sd.RED)
    g += sp(x, y, s, "M-110 -74 Q-95 -90 -80 -74", 3)
    return g
def bell_coffin(x, y, s=1):
    g = fp(x, y, s, "M-130 0 L130 0 L130 80 L-130 80 Z") + rc(x, y, s, -70, 30, 140, 36, B(), 8)
    g += sp(x, y, s, "M-60 48 L60 48", 2) + sp(x, y, s, "M40 40 L40 0 L40 -90", 2.5)
    g += sp(x, y, s, "M20 -90 L20 -10 M20 -90 L70 -90", 5)
    g += fp(x, y, s, "M56 -88 Q56 -64 46 -56 L94 -56 Q84 -64 84 -88 Q70 -98 56 -88 Z") + ci(x, y, s, 70, -52, 5)
    return g
def ossuary(x, y, s=1):
    g = ''
    for r in range(3):
        for k in range(5):
            g += skull(x, y, s, -96 + k * 48 + (r % 2) * 24, -64 + r * 62, 0.36, cracked=False)
        if r < 2:
            g += ''.join(sd.bone(x + (-118 + k * 40) * s, y + (-30 + r * 62) * s, x + (-90 + k * 40) * s, y + (-30 + r * 62) * s, 7 * s) for k in range(7))
    return g
def hearse(x, y, s=1):
    g = fp(x, y, s, "M-130 30 L-130 -10 Q-126 -20 -110 -22 L-80 -24 L-70 -60 L90 -60 Q110 -58 116 -40 L130 -10 L130 30 Z")
    g += rc(x, y, s, -60, -52, 60, 30, B(), 3) + rc(x, y, s, 10, -52, 90, 30, B(), 3)
    g += sp(x, y, s, "M24 -46 Q32 -30 24 -26 M80 -46 Q72 -30 80 -26", 3) + sp(x, y, s, "M24 -36 L80 -36", 2)
    for u in (-86, 80):
        g += ci(x, y, s, u, 32, 20) + ci(x, y, s, u, 32, 8, B())
    g += sp(x, y, s, "M-150 52 L150 52", 4)
    return g
def vault(x, y, s=1):
    g = fp(x, y, s, "M-130 -60 L130 -60 L130 90 L-130 90 Z", op=1)
    g += ''.join(ci(x, y, s, u, v, 2, B()) for u, v in ((-110, -40), (-80, 70), (100, -30), (110, 60), (-100, 20)))
    g += rc(x, y, s, -90, -20, 180, 90, B(), 2) + rc(x, y, s, -82, -12, 164, 74, None, 2)
    g += rc(x, y, s, -60, 6, 120, 40, B(), 10) + sp(x, y, s, "M-52 20 L52 20", 1.5)
    g += ''.join(sp(x, y, s, f"M{u} -60 L{u+4} -72 L{u+8} -60", 3) for u in range(-120, 130, 18))
    return g

# ---------- grief ----------
def chair(x, y, s=1):
    g = sp(x, y, s, "M-40 -90 L-40 90 M40 -90 L40 90 M-40 20 L40 20 M-44 90 L-44 20 M44 90 L44 20", 7)
    g += rc(x, y, s, -50, 14, 100, 12, None, 3) + sp(x, y, s, "M-40 -60 L40 -60 M-40 -36 L40 -36", 5)
    g += fp(x, y, s, "M-30 -92 Q0 -104 30 -92 L46 -40 L36 10 L20 0 L22 -50 L-22 -50 L-20 0 L-36 10 L-46 -40 Z")
    g += sp(x, y, s, "M0 -96 L0 -40", 2, B())
    return g
def phone_old(x, y, s=1):
    g = rc(x, y, s, -90, -30, 180, 110, None, 16) + rc(x, y, s, -70, -14, 80, 36, B(), 4)
    g += tx(x, y, s, -30, 10, "1 SAVED", 12, width=70)
    g += ''.join(rc(x, y, s, 24 + c * 18, -12 + r * 18, 12, 12, B(), 3) for r in range(4) for c in range(3))
    g += ci(x, y, s, -60, 50, 8, sd.RED)
    g += fp(x, y, s, "M-100 -40 Q-104 -78 -60 -80 L60 -80 Q104 -78 100 -40 L70 -40 L60 -60 L-60 -60 L-70 -40 Z")
    return g
def phone_screen(x, y, s=1):
    g = rc(x, y, s, -48, -96, 96, 192, None, 16) + rc(x, y, s, -40, -80, 80, 160, B(), 6)
    g += ci(x, y, s, 0, -44, 18) + tx(x, y, s, 0, -6, "MOM", 14, width=70) + tx(x, y, s, 0, 12, "(last seen 2019)", 7, font="type", width=70)
    g += rc(x, y, s, -32, 30, 64, 18, None, 9) + tx(x, y, s, 0, 43, "CALL", 9, fill=B())
    g += rc(x, y, s, -32, 54, 64, 18, "none", 9, I(), 1.5) + tx(x, y, s, 0, 67, "DELETE", 8, width=50)
    g += sp(x, y, s, "M-36 54 L36 72", 2, sd.RED)
    return g
def urn_books(x, y, s=1):
    g = sp(x, y, s, "M-130 80 L130 80", 6)
    for k, (u, h) in enumerate(((-120, 120), (-100, 110), (-80, 126), (-60, 100), (64, 116), (84, 104), (104, 124))):
        g += rc(x, y, s, u, 78 - h, 18, h, None, 2) + sp(x, y, s, f"M{u+4} {90-h} L{u+14} {90-h}", 1.5, B())
    g += fp(x, y, s, "M-26 -40 L26 -40 L20 -30 Q44 0 34 40 Q26 72 0 78 Q-26 72 -34 40 Q-44 0 -20 -30 Z") + rc(x, y, s, -18, -58, 36, 20, None, 6)
    g += sp(x, y, s, "M-30 10 L30 10 M-28 18 L28 18", 1.5, B())
    return g
def monitor(x, y, s=1):
    g = rc(x, y, s, -110, -76, 220, 130, None, 10) + rc(x, y, s, -98, -64, 196, 106, B(), 4) + rc(x, y, s, -94, -60, 188, 98, None, 3)
    g += sp(x, y, s, "M-80 -10 L80 -10", 2, B()) + tx(x, y, s, 76, -34, "4:12", 14, fill=B(), anchor="end")
    g += sp(x, y, s, "M0 54 L0 80 M-40 86 L40 86", 6)
    g += sp(x, y, s, "M100 70 L130 76", 3) + rc(x, y, s, 124, 70, 14, 10, None, 2)
    return g
def casseroles(x, y, s=1):
    g = ''
    for k in range(5):
        v = 70 - k * 30; u = (k % 2) * 8 - 4
        g += fp(x, y, s, f"M{u-80} {v} L{u+80} {v} L{u+70} {v+24} L{u-70} {v+24} Z")
        g += sp(x, y, s, f"M{u-76} {v+4} L{u+76} {v+4}", 1.5, B())
    g += rc(x, y, s, -30, -110, 60, 40, B(), 2, I(), 2, rot=-8) + tx(x, y, s, 0, -86, "SORRY", 10)
    return g
def heart_box(x, y, s=1):
    g = fp(x, y, s, "M-90 -10 L90 -10 L90 80 L-90 80 Z") + fp(x, y, s, "M-90 -10 L-60 -50 L-20 -40 L-50 -2 Z", op=0.8)
    g += fp(x, y, s, "M90 -10 L60 -50 L20 -40 L50 -2 Z", op=0.8)
    g += rc(x, y, s, -60, 20, 70, 34, B(), 2) + tx(x, y, s, -25, 42, "NO RETURNS", 8, width=62)
    g += sp(x, y, s, "M-90 0 L90 0", 3, B(), dash=(6, 5))
    g += sd.anatomical_heart(x, y - 50 * s, 0.5 * s, drips=False)
    return g
def eulogy(x, y, s=1):
    g = fp(x, y, s, "M-80 -90 L50 -96 L80 90 L-50 96 Z") + sp(x, y, s, "M-66 -4 L66 -8", 2.5, B())
    for i in range(9):
        v = -76 + i * 18 + (6 if i > 3 else 0)
        g += sp(x, y, s, f"M{-60+i*1.6} {v} L{50+i*1.8} {v-4}", 2, B())
    g += ''.join(ci(x, y, s, u, v, 4, B()) for u, v in ((20, 40), (-20, 64)))
    return g
def candle_out(x, y, s=1):
    g = fp(x, y, s, "M-30 80 L30 80 L30 40 Q20 30 22 22 L-22 22 Q-24 34 -30 40 Z") + rc(x, y, s, -50, 80, 100, 10, None, 4)
    g += fp(x, y, s, "M-22 22 Q-30 44 -26 60 Q-22 46 -18 30 Z") + sp(x, y, s, "M0 22 L2 10", 2.5)
    g += sp(x, y, s, "M2 8 Q-20 -20 6 -40 Q30 -60 0 -90 Q-20 -110 10 -130", 3)
    return g
def plates_table(x, y, s=1):
    g = rc(x, y, s, -130, 20, 260, 12, None, 3) + sp(x, y, s, "M-110 32 L-110 90 M110 32 L110 90", 6)
    for u, full in ((-56, True), (56, False)):
        g += el(x, y, s, u, 12, 44, 9) + el(x, y, s, u, 10, 30, 5, B())
        if full: g += el(x, y, s, u, 6, 18, 6)
        g += sp(x, y, s, f"M{u-56} -4 L{u-56} 18 M{u+56} -4 L{u+56} 18", 3)
    g += sp(x, y, s, "M-56 -60 Q-70 -40 -56 -20", 2, dash=(3, 3))
    return g

# ---------- reaper / skeletons ----------
def reaper_glass(x, y, s=1):
    return reaper_body(x, y, 0.9 * s) + sd.hourglass(x - 2 * s, y + 6 * s, 0.42 * s) + sp(x, y, s, "M-14 -6 L10 18", 2, B())
def skel_hoodie(x, y, s=1):
    g = sd.skeleton(x, y - 90 * s, 0.95 * s)
    g += fp(x, y, s, "M-40 -70 Q0 -126 40 -70 L44 -54 Q0 -80 -44 -54 Z")
    g += fp(x, y, s, "M-44 -64 L-60 -60 L-74 0 L-62 4 L-50 -30 L-44 4 L44 4 L50 -30 L62 4 L74 0 L60 -60 L44 -64 Q0 -50 -44 -64 Z")
    g += fp(x, y, s, "M-26 -16 L26 -16 L32 2 L-32 2 Z", B())
    return g
def reaper_clip(x, y, s=1):
    g = reaper_body(x, y, 0.9 * s)
    g += rc(x, y, s, -34, -6, 50, 64, B(), 3, I(), 3) + rc(x, y, s, -18, -12, 18, 10, None, 2)
    g += ''.join(sp(x, y, s, f"M-26 {v} L8 {v}", 2) for v in (10, 20, 30, 40))
    g += sp(x, y, s, "M-28 30 L8 30", 2.4, sd.RED)
    return g
def danse(x, y, s=1):
    g = ''
    for k, u in enumerate((-90, -30, 30, 90)):
        g += sd.skeleton(x + u * s, y - 86 * s, 0.6 * s, ("flex", "stand", "flex", "stand")[k])
    g += ''.join(sd.bone(x + (u + 16) * s, y - 60 * s, x + (u + 44) * s, y - 60 * s, 3.6 * s) for u in (-90, -30, 30))
    g += sp(x, y, s, "M-130 30 L130 30", 4)
    return g
def reaper_sharpen(x, y, s=1):
    g = reaper_body(x, y, 0.9 * s)
    g += rc(x, y, s, -60, -40, 46, 12, None, 3, rot=-20)
    g += ''.join(sp(x, y, s, f"M{u} {v} L{u+d1} {v+d2}", 2) for u, v, d1, d2 in ((-80, -60, -10, -14), (-74, -66, -2, -18), (-66, -64, 8, -14)))
    return g
def two_skulls(x, y, s=1):
    g = skull(x, y, s, -54, 10, 0.8, cracked=False) + skull(x, y, s, 54, 10, 0.8, cracked=False)
    g += fp(x, y, s, "M-90 -48 L-90 -76 L-78 -60 L-66 -84 L-54 -60 L-42 -84 L-30 -60 L-18 -76 L-18 -48 Z")
    g += ''.join(ci(x, y, s, u, -50, 3, B()) for u in (-78, -54, -30))
    g += tx(x, y, s, 0, 88, "=", 30)
    return g
def skull_candle(x, y, s=1):
    g = skull(x, y, s, 0, 26, 1.0, cracked=False)
    g += candle_lit(x, y, s, 0, -26, 50)
    g += ''.join(fp(x, y, s, f"M{u} -30 Q{u-4} {-30+L} {u} {-26+L} Q{u+4} {-30+L} {u} -30 Z") for u, L in ((-30, 30), (24, 40), (40, 20)))
    return g
def plague(x, y, s=1):
    g = fp(x, y, s, "M-40 -60 Q-44 -96 0 -98 Q44 -96 40 -60 Z") + rc(x, y, s, -60, -66, 120, 10, None, 4)
    g += fp(x, y, s, "M-30 -56 Q-36 -10 -10 0 L80 60 L70 64 L-10 20 Q-40 10 -40 -30 Z")
    g += ci(x, y, s, -14, -36, 12, B()) + ci(x, y, s, -14, -36, 6)
    g += fp(x, y, s, "M-40 0 L-70 100 L30 100 L10 30 Z")
    g += sp(x, y, s, "M50 40 L50 100", 4)
    return g
def reaper_ticket(x, y, s=1):
    g = reaper_body(x, y, 0.9 * s)
    g += rc(x, y, s, -34, 0, 34, 22, B(), 2, I(), 2) + tx(x, y, s, -17, 16, "713", 10)
    g += rc(x, y, s, -128, -110, 60, 30, None, 4) + tx(x, y, s, -98, -89, "712", 14, fill=sd.RED)
    return g
def barrow(x, y, s=1):
    g = fp(x, y, s, "M-80 -10 L60 -10 L40 40 L-60 40 Z") + ci(x, y, s, 30, 56, 20) + ci(x, y, s, 30, 56, 7, B())
    g += sp(x, y, s, "M-80 -10 L-130 20 M-60 40 L-70 70", 5)
    g += ''.join(sd.bone(x + u * s, y + v * s, x + (u + 50) * s, y + (v + w) * s, 8 * s) for u, v, w in ((-70, -26, -10), (-30, -36, 6), (0, -22, -14)))
    g += skull(x, y, s, 10, -48, 0.4, cracked=False)
    g += sd.skeleton(x + 90 * s, y - 80 * s, 0.6 * s, "carry")
    return g

# ---------- cremation ----------
def retort(x, y, s=1):
    g = rc(x, y, s, -110, -80, 220, 160, None, 8) + rc(x, y, s, -80, -50, 160, 100, B(), 30)
    g += ''.join(sd.flame(x + u * s, y + 20 * s, 0.55 * s) for u in (-46, 0, 46))
    g += tx(x, y, s, 0, -60, "1,800°F", 13, fill=B())
    g += rc(x, y, s, 80, -10, 20, 26, B(), 3)
    return g
def tray_bones(x, y, s=1):
    g = tray(x, y, s, 0, 20, 220, 30)
    import random; r = random.Random(5)
    for _ in range(18):
        u, v = r.randint(-90, 90), r.randint(-6, 14)
        g += sd.bone(x + u * s, y + v * s, x + (u + r.randint(-14, 14)) * s, y + (v - r.randint(4, 10)) * s, r.choice((4, 5, 6)) * s)
    g += ''.join(ci(x, y, s, r.randint(-90, 90), r.randint(-2, 16), 1.8) for _ in range(30))
    g += fp(x, y, s, "M60 -80 L100 -40 L90 -30 L50 -70 Z") + rc(x, y, s, 36, -96, 30, 26, None, 4, rot=45)
    return g
def urn_label(x, y, s=1):
    g = fp(x, y, s, "M-30 -60 L30 -60 L22 -46 Q56 -10 44 40 Q34 82 0 88 Q-34 82 -44 40 Q-56 -10 -22 -46 Z") + rc(x, y, s, -24, -84, 48, 26, None, 8)
    g += rc(x, y, s, -42, -6, 84, 44, B(), 3) + tx(x, y, s, 0, 10, "CONTENTS:", 9, width=74) + tx(x, y, s, 0, 28, "1 PERSON", 12, width=74)
    g += sp(x, y, s, "M-34 -6 L-34 38", 1.5, dash=(2, 3))
    return g
def chimney(x, y, s=1):
    g = rc(x, y, s, -130, 30, 260, 60, None, 2) + rc(x, y, s, 30, -60, 40, 92, None, 2) + rc(x, y, s, 24, -66, 52, 10, None, 2)
    g += ''.join(rc(x, y, s, u, 46, 24, 20, B(), 2) for u in (-110, -70, -30))
    g += sp(x, y, s, "M50 -70 Q34 -84 0 -84 Q-40 -82 -70 -92 Q-100 -100 -126 -90", 9)
    return g
def ash_lake(x, y, s=1):
    g = ''.join(sp(x, y, s, f"M-130 {v} Q-100 {v-6} -70 {v} Q-40 {v+6} -10 {v} Q20 {v-6} 50 {v} Q80 {v+6} 110 {v} L130 {v}", 3) for v in (40, 56, 72))
    import random; r = random.Random(9)
    g += ''.join(ci(x, y, s, r.randint(-90, 100), r.randint(-80, 20), r.choice((1.8, 2.4, 3))) for _ in range(70))
    g += fp(x, y, s, "M-110 -10 L-90 -40 L-70 -40 L-70 -4 Z") + sp(x, y, s, "M-90 -40 Q-60 -60 -30 -40", 3)
    return g
def pacemaker(x, y, s=1):
    g = fp(x, y, s, "M-60 -40 Q-60 -70 -20 -70 L10 -70 Q40 -70 40 -30 L40 10 Q40 40 0 40 L-30 40 Q-60 40 -60 10 Z")
    g += rc(x, y, s, -40, -60, 40, 14, B(), 4) + sp(x, y, s, "M0 -60 Q40 -100 80 -60 Q110 -30 80 0", 4)
    g += rc(x, y, s, 60, 20, 70, 80, B(), 2, I(), 2.5, rot=6)
    g += ''.join(sp(x, y, s, f"M{70} {v} L{118} {v+4}", 1.6) for v in (36, 48, 60, 72))
    g += tx(x, y, s, 96, 92, "REMOVED ✓", 8, font="osw", width=60) if False else rc(x, y, s, 72, 82, 10, 10, "none", 0, I(), 2)
    return g
def ash_scale(x, y, s=1):
    g = rc(x, y, s, -80, 30, 160, 50, None, 8) + rc(x, y, s, -50, 44, 100, 24, B(), 3) + tx(x, y, s, 0, 63, "5.2 LB", 16, width=90)
    g += rc(x, y, s, -96, 20, 192, 12, None, 4)
    g += fp(x, y, s, "M-50 20 Q-60 -40 -20 -60 L20 -60 Q60 -40 50 20 Z") + sp(x, y, s, "M-24 -60 L-14 -80 L14 -80 L24 -60", 4)
    g += rc(x, y, s, -24, -30, 48, 26, B(), 2)
    return g
def id_disc(x, y, s=1):
    g = ci(x, y, s, 0, 0, 70) + ci(x, y, s, 0, 0, 60, "none", B(), 2) + ci(x, y, s, 0, -50, 7, B())
    g += tx(x, y, s, 0, -14, "CREM. NO.", 11, fill=B()) + tx(x, y, s, 0, 18, "26-0417", 22, fill=B(), width=100)
    g += sp(x, y, s, "M0 -57 Q30 -110 70 -100", 3)
    return g

# ---------- dread ----------
def calendar(x, y, s=1):
    g = rc(x, y, s, -100, -80, 200, 166, "none", 6, I(), 5) + rc(x, y, s, -100, -80, 200, 34, None, 6)
    g += tx(x, y, s, 0, -56, "SOMEDAY", 14, fill=B()) + sp(x, y, s, "M-60 -92 L-60 -70 M60 -92 L60 -70", 6)
    for r in range(4):
        for c in range(7):
            g += rc(x, y, s, -92 + c * 26.6, -38 + r * 30, 22, 26, "none", 2, I(), 1.5)
    g += sp(x, y, s, "M-12 26 L6 48", 2, sd.RED) if False else ''
    return g
def brain_storm(x, y, s=1):
    return sd.brain(x, y + 30 * s, 1.0 * s) + sd.cloud(x, y - 56 * s, 0.9 * s) + ''.join(
        sp(x, y, s, f"M{u} -34 L{u-6} -14", 2.4) for u in (-50, -30, 20, 40)) + sd.bolt(x - 4 * s, y - 20 * s, 0.4 * s)
def mattress(x, y, s=1):
    g = fp(x, y, s, "M-130 0 L130 0 L130 50 L-130 50 Z") + sp(x, y, s, "M-130 50 L-130 80 M130 50 L130 80", 6)
    g += fp(x, y, s, "M-110 -8 Q-110 -36 -80 -36 L-50 -36 Q-40 -36 -40 -8 Z")
    g += fp(x, y, s, "M-30 4 Q-20 18 20 14 L100 12 Q110 12 112 6 L-30 6 Z", B())
    g += ''.join(sp(x, y, s, f"M{u} 22 L{u} 34", 1.5, B()) for u in range(-110, 120, 20))
    g += tx(x, y, s, 60, -24, "Z", 14) + tx(x, y, s, 80, -40, "Z", 11) + tx(x, y, s, 94, -52, "Z", 8)
    return g
def moth_ribs(x, y, s=1):
    return ribcage(x, y, s * 1.05) + sd.moth(x, y + 10 * s, 0.55 * s)
def heart_trap(x, y, s=1):
    g = sd.anatomical_heart(x, y - 10 * s, 0.75 * s, drips=True)
    for d in (-1, 1):
        g += sp(x, y, s, f"M{d*100} 30 Q{d*90} -40 {d*30} -60", 6)
        g += ''.join(fp(x, y, s, f"M{d*u} {v} L{d*(u-12)} {v-4} L{d*(u-4)} {v+10} Z") for u, v in ((96, 10), (90, -16), (76, -38), (54, -54)))
    g += sp(x, y, s, "M-110 34 L110 34", 7) + ci(x, y, s, 0, 34, 12) + sp(x, y, s, "M12 34 L60 70 L120 72", 3)
    return g
def chalk_squat(x, y, s=1):
    c = I()
    g = f'<g stroke-dasharray="{6*s:.1f} {4*s:.1f}">' + ci(x, y, s, 0, -86, 18, "none", c, 3) + '</g>'
    g += sp(x, y, s, "M-16 -66 L-24 -20 L-60 -4 L-62 20 L-36 34 L-40 70 L-20 70 L-14 40 L-4 0 M16 -66 L24 -20 L60 -4 L62 20 L36 34 L40 70 L20 70 L14 40 L4 0", 3, dash=(6, 4))
    g += sp(x, y, s, "M-18 -60 L-90 -66 M18 -60 L90 -66", 3, dash=(6, 4))
    g += sp(x, y, s, "M-120 -66 L120 -66", 8) + plates(x, y, s, -112, -66, 0.8) + plates(x, y, s, 112, -66, 0.8)
    g += sp(x, y, s, "M-140 80 L140 80", 4)
    return g
def wristband(x, y, s=1):
    g = fp(x, y, s, "M-120 -20 Q0 -40 120 -20 L120 20 Q0 0 -120 20 Z") + fp(x, y, s, "M-60 -26 L60 -26 L60 10 L-60 10 Z")
    g += rc(x, y, s, -56, -22, 112, 28, B(), 3)
    g += tx(x, y, s, 0, -10, "COMFORT", 10, width=100) + tx(x, y, s, 0, 2, "CARE ONLY", 10, width=100)
    g += ''.join(ci(x, y, s, u, 0, 3, B()) for u in (80, 96, 112))
    return g
def face_muscles(x, y, s=1):
    g = skull(x, y, s, 0, 0, 1.2, cracked=False)
    for d in (-1, 1):
        g += fp(x, y, s, f"M{d*14} 38 Q{d*50} 20 {d*58} -20 L{d*48} -22 Q{d*40} 12 {d*8} 30 Z")
        g += sp(x, y, s, f"M{d*58} -24 L{d*100} -50", 1.2) + ci(x, y, s, d * 100, -50, 2.5)
    g += tx(x, y, s, -104, -56, "ZYGOMATICUS", 8, anchor="end") + tx(x, y, s, 104, -56, "MAJOR", 8, anchor="start")
    g += sp(x, y, s, "M-30 52 Q0 66 30 52", 3)
    return g
def skull_thread(x, y, s=1):
    g = skull(x, y, s, 0, 0, 1.2, cracked=False)
    g += fp(x, y, s, "M-52 -30 Q0 -96 52 -30 Q0 -40 -52 -30 Z", B())
    import random; r = random.Random(4)
    d = "M-40 -36"
    for _ in range(22):
        d += f" Q{r.randint(-46,46)} {r.randint(-80,-34)} {r.randint(-46,46)} {r.randint(-74,-38)}"
    g += sp(x, y, s, d, 1.6)
    g += sp(x, y, s, "M40 -40 Q80 -60 90 -20 Q100 20 120 30", 1.6)
    return g
def skel_bench(x, y, s=1):
    g = rc(x, y, s, -110, 20, 220, 14, None, 4) + sp(x, y, s, "M-90 34 L-90 80 M90 34 L90 80", 6)
    g += sd.skeleton(x - 10 * s, y - 60 * s, 0.8 * s, "sit")
    g += sd.dumbbell(x + 80 * s, y + 6 * s, 0.38 * s)
    g += ''.join(ci(x, y, s, u, v, 2, None) for u, v in ((-40, 10), (-30, 14), (20, 12)))
    return g

NEW = {k: v for k, v in dict(globals()).items() if callable(v) and v.__module__ == __name__ and k not in
       ("I", "B", "P", "fp", "sp", "ci", "el", "rc", "tx", "skull", "ribcage", "figure_lying", "scythe", "reaper_body", "beetle", "fly", "bar", "plates", "muscle_lines", "tray", "candle_lit", "render_all")}
sd.ICONS.update(NEW)

def render_all(only=()):
    from designs_data3 import SET3
    sd.OUT and os.makedirs(sd.OUT, exist_ok=True)
    names = []
    for i, d in enumerate(SET3):
        n = 108 + i
        if only and n not in only: continue
        names.append(sd.render(n, d))
    return names

if __name__ == "__main__":
    only = {int(a) for a in sys.argv[1:]}
    names = render_all(only)
    print(len(names), names[0], names[-1])

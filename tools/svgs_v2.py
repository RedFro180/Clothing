"""V2 line-art set: every design 01-207 on the vignette composition (tools/vignette.py).
Subject = the caption-matched scene from tools/redo_specs.py (or a native v2 subject), drawn large on the hill,
smoother lines, per-design sky / tree type / font. Output: designs/sketches-v2/NNN-slug.svg
Run: python3 tools/svgs_v2.py [numbers...]"""
import os, sys, re, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import svgs_dark as sd
import svgs_night as nt
import svgs_redo as R
import redo_vary as RV          # registers the extra fonts
import redo_specs as RS
import vignette as VG

OUT = os.path.normpath(os.path.join(HERE, "..", "designs", "sketches-v2"))
NATIVE = {16: lambda: watch_eyes(), 1: lambda: VG.skeleton_grip(0, 206, 1.05), 4: lambda: VG.back_carry(0, 206, 1.1),
          11: lambda: VG.half_face(0, 212, 1.0), 12: lambda: VG.lying_stargazer(-24, 206, 1.35)}
def watch_eyes():
    g = VG.path("M-8 206 L-6 186 L0 172 L6 186 L8 206", 2.6) + '<circle cx="0" cy="162" r="9" fill="none" stroke="%s" stroke-width="2.6"/>' % VG.I()
    g += VG.path("M-14 180 L0 176 L14 180", 2.4)
    for x, y in ((-104, 150), (-70, 168), (88, 146), (116, 172), (-120, 186), (60, 182)):
        g += ''.join('<ellipse cx="%.1f" cy="%.1f" rx="4" ry="2.6" fill="none" stroke="%s" stroke-width="1.2"/><circle cx="%.1f" cy="%.1f" r="1.4" fill="%s"/>' % (x + d, y, VG.I(), x + d, y, VG.I()) for d in (-5, 5))
    return g
SKIES = ["none", "none", "none", "night", "crescent", "milky", "sun", "dusk"]
TREES = ["pine"]
FONTS = ["hand", "hand", "marker", "amatic", "shadows", "indie", "rocksalt"]
FIX = {12: dict(sky="milky", trees="pine"), 1: dict(sky="night"), 4: dict(sky="none"), 11: dict(sky="none")}

def variant(n):
    r = random.Random(n * 7919)
    v = dict(sky=r.choice(SKIES), trees=r.choice(TREES), font=FONTS[n % len(FONTS)], side=1 if n % 2 else -1)
    v.update(FIX.get(n, {}))
    return v

_jit = nt.jitter
def smooth_jitter(pts, r, amt=1.2, step=6): return _jit(pts, r, amt * 0.3, step)

NUM = re.compile(r"-?\d+(?:\.\d+)?")
def bbox(svg):
    xs, ys = [], []
    for d in re.findall(r' d="([^"]+)"', svg):
        for seg in re.findall(r"[MLQCT]([^MLQCTZmlqcaAhHvVsSz]*)", d):
            nums = [float(v) for v in NUM.findall(seg)]
            xs += nums[0::2]; ys += nums[1::2]
    for tag in re.findall(r"<(?:circle|ellipse|rect)[^>]+>", svg):
        a = dict(re.findall(r'(\w+)="([-\d.]+)"', tag))
        if "cy" in a: ys.append(float(a["cy"]) - float(a.get("r", a.get("ry", 0)))); xs.append(float(a["cx"]))
        if "y" in a and "x" in a: ys.append(float(a["y"])); xs += [float(a["x"]), float(a["x"]) + float(a.get("width", 0))]
    return (min(xs), min(ys), max(xs), max(ys)) if xs and ys else (-50, 150, 50, 236)

def subject(n, d, v):
    r = random.Random(n * 31)
    if n in NATIVE:
        return NATIVE[n](), (0, 0)
    nt.jitter = smooth_jitter; R.jitter = smooth_jitter
    try:
        raw = RS.SPEC[n][1](r)
    finally:
        nt.jitter = _jit; R.jitter = _jit
    x0, y0, x1, y1 = bbox(raw)
    room = 206 - (40 if v["sky"] == "none" else 70)                 # keep clear of the sky / caption
    k = min(1.45, room / max(30, 236 - y0), 100 / max(30, abs(x0), abs(x1)))
    return f'<g transform="translate(0 206) scale({k:.3f}) translate(0 -236)">{raw}</g>', (x0 * k, x1 * k)

def scene(n, d):
    v = variant(n); r = random.Random(n * 17 + 3)
    sub, (gx0, gx1) = subject(n, d, v)
    gap = (gx0 * 0.85, gx1 * 0.85) if gx1 - gx0 > 4 else None
    if n in NATIVE: gap = {1: (-26, 26), 4: (-18, 18)}.get(n)
    return VG.compose(r, sub, v["sky"], v["side"], forest_gap=gap, trees=v["trees"]), sub

def layout(n, d):
    v = variant(n); f = RV.FONT_SIZE[v["font"]]; R.FONT[0] = v["font"]
    body, sub = scene(n, d)
    _, sy0, _, _ = bbox(sub) if n not in NATIVE else (0, {1: 82, 4: 90, 11: 80, 12: 150, 16: 140}[n], 0, 0)
    if n not in NATIVE:
        k = float(re.search(r"scale\(([\d.]+)\)", sub).group(1)); sy0 = 206 - (236 - sy0) * k
    top = max(14, min(24 if v["sky"] != "none" else 84, sy0 - 8))
    main = R.cap_text(" ".join(d["lines"])); subl = R.cap_text(d["sub"]) if d.get("sub") else ""
    try:
        if d["place"] in ("back", "hood"):
            a, yy = R.caption(main, 300, 176, 296, 46 * f, 26 * f)
            if subl: a += sd.tpath(subl, v["font"], sd.fitsize(subl, v["font"], 280, 24 * f), 300, yy + 16); yy += 24
            k = min(1.05, (558 - yy) / (262 - top))
            return "back", a + f'<g transform="translate(300 {yy+4:.1f}) scale({k:.3f}) translate(0 -{top:.1f})">{body}</g>'
        a, yy = R.caption(main, 300, 210, 262, 34 * f, 20 * f)
        if subl: a += sd.tpath(subl, v["font"], sd.fitsize(subl, v["font"], 250, 18 * f), 300, yy + 12); yy += 18
        k = min(0.82, (452 - yy) / (262 - top))
        return "front", a + f'<g transform="translate(300 {yy+2:.1f}) scale({k:.3f}) translate(0 -{top:.1f})">{body}</g>'
    finally:
        R.FONT[0] = "hand"

def render_all(only=()):
    os.makedirs(OUT, exist_ok=True)
    lay0 = sd.layout; sd.layout = layout; names = []
    try:
        for i, d in enumerate(R.all_designs()):
            n = i + 1
            if only and n not in only: continue
            dd = dict(d); dd["note"] = "V2 line-art redraw of sketch %02d. %s" % (n, d["note"])
            names.append(sd.render(n, dd, out=OUT))
    finally:
        sd.layout = lay0
    return names

if __name__ == "__main__":
    names = render_all({int(a) for a in sys.argv[1:]})
    print(len(names), names[0], names[-1])

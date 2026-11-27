"""Render v2 vignette samples (01, 04, 11, 12) on hoodies -> designs/samples-v2/."""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import svgs_dark as sd, svgs_night  # noqa: F401  (svgs_night registers the Caveat font)
import vignette as VG
from svgs_redo import cap_text, caption
OUT = os.path.join(HERE, "..", "designs", "samples-v2"); os.makedirs(OUT, exist_ok=True)

SAMPLES = {
 1:  (20, lambda r: VG.compose(r, VG.skeleton_grip(0, 206, 1.05), "night", 1, forest_gap=(-26, 26))),
 4:  (64, lambda r: VG.compose(r, VG.back_carry(0, 206, 1.1), "none", forest_gap=(-18, 18))),
 11: (60, lambda r: VG.compose(r, VG.half_face(0, 212, 1.0), "none")),
 12: (20, lambda r: VG.compose(r, VG.lying_stargazer(-24, 206, 1.35), "milky", 1)),
}
def layout(num, d):
    top, fn = SAMPLES[num]
    r = random.Random(num * 31)
    main = cap_text(" ".join(d["lines"])); sub = cap_text(d["sub"]) if d.get("sub") else ""
    a, yy = caption(main, 300, 176, 300, 46, 28)
    if sub: a += sd.tpath(sub, "hand", sd.fitsize(sub, "hand", 280, 24), 300, yy + 16); yy += 24
    k = min(1.05, (560 - yy) / (262 - top))
    return "back", a + f'<g transform="translate(300 {yy+4:.1f}) scale({k:.3f}) translate(0 -{top})">{fn(r)}</g>'
if __name__ == "__main__":
    from designs_data import FIRST, DESIGNS
    D = FIRST + DESIGNS
    lay0 = sd.layout; sd.layout = layout
    try:
        for n in SAMPLES:
            d = dict(D[n - 1]); d["place"] = "back"; d["note"] = "v2 sample: vignette composition (3 line weights, layered depth, large subject)."
            print(sd.render(n, d, out=OUT))
    finally:
        sd.layout = lay0

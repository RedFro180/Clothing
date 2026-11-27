"""Per-design scenes for the line-art redraws (01-207): each scene is chosen from the CAPTION, not the old icon.
SPEC[n] = (background, function(r) -> svg). Used by svgs_redo.scene(). Audit table: designs/redraw-audit.md."""
import math
import svgs_night as nt
from svgs_night import jl, pl, pine, head, sit_lean, sit_hug, kneel, lie, walk, sit_on, grave_mound, cross, coffin_side, dead_tree, carry_rock, campfire, tufts
import svgs_redo as R
from svgs_redo import (shape, ell, hand, rect_pts, stand, press, deadlift, barbell_l, skull_l, skeleton_l, coffin_up, grave_open, tomb, gurney,
                       drawer, bodybag, reaper_l, heart_l, rack_l, candle_l, hourglass_l, clock_l, rose_l, ghost_l, sign_l, wreath_l, bottle_l,
                       table_l, jar_l, scale_l, crem_l, urn_l, chair_l, phone_l, bed_l, trap_l, hearse_l, bones_pile, shrooms_l, roots_skull,
                       crows_tree, flies_skull, ekg_ridge, body_gore, skeleton_lie, dance, two_at_grave, two_carry, ash_lake_l, stone, rain_cloud)
G = R.G
I, B = nt.I, nt.B

# ---------- new line-art pieces ----------
def skel_hang(r, x, y):                       # skeleton in a dead hang from a pull-up bar (grip, not a rope)
    g = jl([(x - 50, y), (x - 50, y - 118)], r, 2.6) + jl([(x + 50, y), (x + 50, y - 118)], r, 2.6) + jl([(x - 56, y - 118), (x + 56, y - 118)], r, 3)
    g += skull_l(r, x, y - 92, 0.34) + pl([(x, y - 84), (x, y - 56)], 2.2) + ''.join(pl([(x - 7, y + v), (x, y + v - 2), (x + 7, y + v)], 1.4) for v in (-80, -75, -70))
    g += pl([(x - 3, y - 82), (x - 10, y - 100), (x - 12, y - 116)], 1.8) + pl([(x + 3, y - 82), (x + 10, y - 100), (x + 12, y - 116)], 1.8)
    return g + pl([(x - 5, y - 30), (x, y - 56), (x + 5, y - 30)], 2.2)
def skel_lift(r, x, y):                      # skeleton holding a loaded barbell at the hips (grip, never hanging)
    g = skull_l(r, x, y - 66, 0.34) + pl([(x, y - 58), (x, y - 30)], 2.2) + ''.join(pl([(x - 7, y + v), (x, y + v - 2), (x + 7, y + v)], 1.4) for v in (-54, -49, -44))
    g += pl([(x - 6, y), (x - 3, y - 16), (x, y - 30), (x + 3, y - 16), (x + 6, y)], 2.2)
    g += pl([(x - 3, y - 54), (x - 12, y - 42), (x - 12, y - 30)], 1.8) + pl([(x + 3, y - 54), (x + 12, y - 42), (x + 12, y - 30)], 1.8)
    return g + barbell_l(x, y - 30, 56)
def scale_stand(r, x, y):                    # flat platform scale with a dial; the heart sits on top (nothing hangs)
    g = table_l(r, x, y, 0) + shape(r, rect_pts(x - 28, y - 58, 56, 24)) + ell(x, y - 46, 8, 8, 1.6) + pl([(x, y - 46), (x + 5, y - 51)], 1.4)
    g += shape(r, rect_pts(x - 34, y - 62, 68, 4), 1.6) + heart_l(r, x, y - 66, 0.36)
    return g + hand("grams", 9, x, y - 26)
def bench_spot(r, x, y, spotter=True, skel=False):   # lifter on a bench pressing, spotter standing at the head
    g = jl([(x - 40, y - 22), (x + 30, y - 22)], r, 3) + jl([(x - 32, y - 22), (x - 32, y)], r, 2) + jl([(x + 22, y - 22), (x + 22, y)], r, 2)
    g += head(x - 46, y - 28, 6.5) + pl([(x - 38, y - 26), (x + 4, y - 26)], 2.4) + pl([(x + 4, y - 26), (x + 16, y - 14), (x + 18, y)], 2.4)
    g += pl([(x - 30, y - 28), (x - 30, y - 56)], 2.2) + pl([(x - 22, y - 28), (x - 22, y - 56)], 2.2) + barbell_l(x - 26, y - 58, 44)
    if spotter:
        sx = x - 74
        g += (skeleton_l(r, sx, y) if skel else stand(sx, y)) + pl([(sx + 2, y - 30), (x - 52, y - 54)], 2) + pl([(sx + 2, y - 26), (x - 44, y - 54)], 2)
    return g
def farmer_coffins(r, x, y):                  # walking, a small coffin in each hand (farmer's carry)
    g = walk(x, y, 1)
    for d in (-1, 1):
        cx = x + d * 14
        g += shape(r, [(cx - 5, y - 16), (cx - 8, y - 4), (cx - 5, y + 2), (cx + 5, y + 2), (cx + 8, y - 4), (cx + 5, y - 16)], 1.6)
    return g
def coffin_backpack(r, x, y):                 # walking with a small coffin strapped on the back
    return walk(x, y, 1) + shape(r, [(x - 14, y - 40), (x - 20, y - 26), (x - 16, y - 8), (x - 4, y - 8), (x - 2, y - 26), (x - 6, y - 40)], 1.8) + pl([(x - 4, y - 34), (x + 2, y - 30)], 1.4)
def cracked(r, x, y):                         # standing figure with a zigzag crack across the chest
    return stand(x, y) + pl([(x - 9, y - 32), (x - 3, y - 26), (x + 2, y - 30), (x + 9, y - 24)], 1.6)
def bar_floor(r, x, y): return barbell_l(x, y - 12, 50)
def eyes_forest(r):
    g = ''.join(pine(u, G, h, r) for u, h in ((-136, 130), (-108, 100), (-80, 120), (80, 110), (108, 126), (136, 104)))
    for u, v in ((-96, 160), (-66, 186), (92, 170), (120, 196), (-124, 200)):
        g += ell(u - 3, v, 2.4, 1.6, 1.2) + ell(u + 3, v, 2.4, 1.6, 1.2) + nt.dot(u - 3, v, 0.9) + nt.dot(u + 3, v, 0.9)
    return g
def two_on_log(r, x, y):
    g = shape(r, [(x - 50, y), (x - 50, y - 10), (x + 50, y - 10), (x + 50, y)])
    return g + sit_on(x - 22, y - 10, 1) + sit_on(x + 16, y - 10, -1) + ell(x + 50, y - 5, 4, 5)
def mailbox(r, x, y, text=""):
    return jl([(x, y), (x, y - 34)], r, 2.4) + shape(r, [(x - 14, y - 34), (x - 14, y - 46), (x - 8, y - 52), (x + 14, y - 52), (x + 14, y - 34)]) + hand(text, 8, x, y - 40)
def belt_on(r, x, y):
    return shape(r, rect_pts(x - 26, y - 44, 52, 10), 1.8) + shape(r, rect_pts(x - 6, y - 46, 12, 14), 1.6)
def worms_soil(r, x, y):
    g = ''.join(jl([(u, y + 4), (u + 6, y + 14)], r, 1, 0.4) for u in range(-140, 140, 22))
    g += skull_l(r, x, y + 26, 0.5)
    for u, v in ((-60, 20), (-30, 34), (40, 22), (70, 36), (10, 44)):
        g += jl([(x + u, y + v), (x + u + 6, y + v - 4), (x + u + 12, y + v), (x + u + 18, y + v - 4)], r, 1.8, 0.3, 3)
    return g
def tape(r, x1, x2, y):
    return jl([(x1, y), (x2, y)], r, 1.4) + ''.join(pl([(u, y - 3), (u, y + 3)], 1) for u in range(int(x1), int(x2), 6))
def six_carry(r, x, y):
    g = coffin_side(x, y - 56, 110, 14)
    for u in (-40, -12, 16, 44):
        g += head(x + u, y - 60, 6.5) + pl([(x + u, y - 52), (x + u, y - 16)], 2.4) + pl([(x + u - 7, y), (x + u, y - 16), (x + u + 7, y)], 2.4)
    return g
def cave(r, x, y):
    g = jl([(x - 90, y), (x - 60, y - 70), (x, y - 96), (x + 60, y - 70), (x + 90, y)], r, 2.4)
    return g + f'<path d="M{x-24} {y} Q{x-24} {y-46} {x} {y-48} Q{x+24} {y-46} {x+24} {y} Z" fill="{I()}"/>'
def cradle(r, x, y):
    g = jl([(x - 30, y), (x - 20, y - 8), (x + 20, y - 8), (x + 30, y)], r, 2) + shape(r, [(x - 24, y - 8), (x - 26, y - 28), (x + 26, y - 28), (x + 24, y - 8)])
    return g + ''.join(pl([(x + u, y - 28), (x + u, y - 10)], 1.2) for u in (-16, -6, 4, 14))
def thermometer(r, x, y):
    return jl([(x, y), (x, y - 20)], r, 2) + shape(r, rect_pts(x - 6, y - 96, 12, 76)) + ell(x, y - 14, 9, 9) + pl([(x, y - 22), (x, y - 50)], 3) + ''.join(pl([(x + 6, y - v), (x + 12, y - v)], 1.2) for v in (40, 52, 64, 76, 88))
def bell_post(r, x, y):
    return jl([(x, y), (x, y - 70), (x + 18, y - 70)], r, 2.4) + shape(r, [(x + 10, y - 66), (x + 12, y - 56), (x + 26, y - 56), (x + 28, y - 66), (x + 19, y - 72)], 1.8) + jl([(x + 19, y - 56), (x + 6, y - 4)], r, 1)
def barrow(r, x, y):
    g = shape(r, [(x - 40, y - 34), (x + 30, y - 34), (x + 20, y - 12), (x - 30, y - 12)]) + ell(x + 18, y - 8, 9, 9) + jl([(x - 40, y - 30), (x - 70, y - 22)], r, 2.2)
    return g + bones_pile(r, x - 5, y - 32)
def moth(r, x, y):
    return ''.join(shape(r, [(x, y), (x + d * 16, y - 12), (x + d * 20, y + 2), (x + d * 8, y + 10)], 1.4) for d in (-1, 1)) + pl([(x, y - 6), (x, y + 10)], 2)
def maggots(r, x, y, n=7):
    return ''.join(ell(x + r.uniform(-24, 24), y - r.uniform(0, 30), 3.4, 1.6, 1.2) for _ in range(n))
def crown_skulls(r, x, y):
    g = skull_l(r, x - 34, y - 18, 0.8) + skull_l(r, x + 34, y - 18, 0.8)
    return g + jl([(x - 54, y - 42), (x - 54, y - 56), (x - 44, y - 48), (x - 34, y - 60), (x - 24, y - 48), (x - 14, y - 56), (x - 14, y - 42)], r, 1.8, 0.3, 3)
def candle_out(r, x, y):
    g = shape(r, [(x - 22, y), (x - 18, y - 12), (x + 18, y - 14), (x + 24, y)]) + shape(r, rect_pts(x - 7, y - 30, 14, 18))
    return g + jl([(x, y - 32), (x - 6, y - 46), (x + 4, y - 60), (x - 4, y - 76)], r, 1.6, 1, 4)
def monitor_bed(r, x, y):
    g = bed_l(r, x - 20, y) + jl([(x + 80, y), (x + 80, y - 60)], r, 2.2) + shape(r, rect_pts(x + 62, y - 92, 36, 28))
    return g + jl([(x + 66, y - 78), (x + 94, y - 78)], r, 1.4)
def skull_dashed(r, x, y):
    return skull_l(r, x, y - 18, 1.3) + f'<path d="M{x-30} {y-40} Q{x} {y-52} {x+30} {y-40}" fill="none" stroke="{I()}" stroke-width="2" stroke-dasharray="5 4"/>'
def big_fly(r, x, y):
    g = ell(x, y, 6, 10) + ell(x, y - 13, 5, 5) + ''.join(shape(r, [(x, y - 6), (x + d * 24, y - 18), (x + d * 22, y - 4)], 1.3) for d in (-1, 1))
    return g + ''.join(pl([(x + d * 5, y + v), (x + d * 14, y + v + 6)], 1.2) for d in (-1, 1) for v in (-2, 4))
def sweat(r, x, y): return ''.join(f'<path d="M{x+u} {y+v} q-3 6 0 8 q3 -2 0 -8 Z" fill="none" stroke="{I()}" stroke-width="1.4"/>' for u, v in ((-14, -70), (16, -66), (22, -50)))
def ghosts(r, xs): return ''.join(ghost_l(r, x, G - 10 - (i % 2) * 14) for i, x in enumerate(xs))
def dye_pot(r, x, y):
    g = campfire(r, x, y) + shape(r, [(x - 22, y - 16), (x - 18, y - 40), (x + 18, y - 40), (x + 22, y - 16)])
    return g + ''.join(jl([(x + u, y - 40), (x + u + 4, y - 58), (x + u + 10, y - 56)], r, 1.4) for u in (-10, 0, 8))
def scale_urn(r, x, y):
    return shape(r, rect_pts(x - 30, y - 16, 60, 16)) + hand("5.2 lb", 10, x, y - 4) + urn_l(r, x, y - 16, 0.7)
def row_markers(r, x, y): return ''.join(shape(r, rect_pts(x + u - 6, y - 20, 12, 20), 1.6) for u in (-80, -56, -32, -8, 16, 40, 64, 88))
def skull_teeth(r, x, y): return skull_l(r, x, y - 20, 1.4)
def two_lifters(r, x, y): return deadlift(x - 50, y) + deadlift(x + 50, y)

def C(*parts): return lambda r: ''.join(p(r) if callable(p) else p for p in parts)
X = lambda f, *a: (lambda r: f(r, *a))
F = lambda f, *a: (lambda r: f(*a))

SPEC = {
1: ("pines", C(X(skel_lift, 0, G))),
2: ("meadow", C(X(skeleton_l, 0, G))),
3: ("pines", C(X(bench_spot, 20, G))),
4: ("valley", C(X(farmer_coffins, 0, G))),
5: ("meadow", C(X(sign_l, 30, G, ("wake up", "miss them", "lift anyway", "sleep, maybe")), F(sit_hug, -40, G, 1))),
6: ("cabin", C(X(bed_l, 0, G), X(nt.dot, 60, G - 50, 0) if False else "")),
7: ("valley", C(X(coffin_backpack, -10, G))),
8: ("meadow", C(X(cracked, -20, G), X(cracked, 20, G))),
9: ("pines", C(X(bar_floor, 30, G), F(sit_hug, -40, G, 1))),
10: ("pines", C(X(gurney, 30, G), F(stand, -60, G))),
11: ("meadow", C(F(stand, -30, G), X(skeleton_l, 30, G))),
12: ("valley", C(X(bar_floor, 40, G), X(stone, 90, G), F(sit_hug, -30, G, 1))),
13: ("pines", C(X(scale_stand, 50, G), X(gurney, -50, G, False))),
14: ("pines", C(F(deadlift, 0, G))),
15: ("pines", C(X(campfire, 30, G), F(sit_hug, -10, G, 1))),
16: ("eyes", C(F(walk, 0, G, 1))),
17: ("meadow", C(X(bodybag, 30, G), F(kneel, -60, G, 1))),
18: ("meadow", C(X(skull_l, 30, G - 18, 1.0), F(kneel, -30, G, 1))),
19: ("valley", C(F(carry_rock, 0, G, 1))),
20: ("pines", C(X(drawer, 20, G), F(stand, -80, G))),
21: ("pines", C(X(bench_spot, 20, G))),
22: ("pines", C(F(deadlift, 0, G), X(sweat, 0, G))),
23: ("valley", C(X(stone, 30, G), X(urn_l, 30, G - 16, 0.7), lambda r: ''.join(nt.dot(30 + r.uniform(10, 90), G - r.uniform(40, 90), 1.2) for _ in range(18)), F(sit_hug, -40, G, 1))),
24: ("meadow", C(X(two_on_log, 0, G))),
25: ("cemetery", C(X(two_carry, 0, G))),
26: ("meadow", C(X(sign_l, 30, G, ("TIME OF DEATH:", "__________", "pending")), F(stand, -50, G))),
27: ("meadow", C(X(skull_l, 30, G - 18, 1.0), X(maggots, 30, G - 4), F(sit_hug, -40, G, 1))),
28: ("meadow", C(X(skeleton_l, 0, G), lambda r: ''.join(nt.dot(r.uniform(-30, 30), G - r.uniform(60, 90), 1.6) for _ in range(6)))),
29: ("valley", C(F(stand, 0, G))),
30: ("pines", C(F(deadlift, 0, G))),
31: ("cabin", C(X(phone_l, 30, G), F(sit_hug, -40, G, 1))),
32: ("meadow", C(X(stone, 30, G), X(heart_l, 30, G - 26, 0.62), F(stand, -40, G))),
33: ("pines", C(X(gurney, 30, G))),
34: ("pines", C(X(coffin_up, 0, G), X(mailbox, 60, G, "PINE"))),
35: ("cemetery", C(X(tomb, 30, G, 1.3, ""), F(stand, -30, G))),
36: ("cabin", C(X(bed_l, 0, G), X(clock_l, 100, G))),
37: ("meadow", C(X(two_on_log, 0, G))),
38: ("pines", C(X(bench_spot, 20, G))),
39: ("pines", C(F(deadlift, 20, G), X(ghost_l, -60, G))),
40: ("meadow", C(X(dye_pot, 30, G), F(stand, -40, G))),
41: ("meadow", C(X(rose_l, 10, G), lambda r: ''.join(nt.dot(r.uniform(10, 50), G - r.uniform(60, 90), 1.4) for _ in range(5)))),
42: ("cemetery", C(X(tomb, 30, G, 1.3, "TRIED"), F(kneel, -30, G, 1))),
43: ("valley", C(X(grave_open, 20, G), F(stand, -70, G))),
44: ("pines", C(F(deadlift, 30, G), X(reaper_l, -60, G, 0.9))),
45: ("meadow", C(X(skeleton_l, 0, G))),
46: ("pines", C(F(sit_hug, 10, G, 1), X(ghost_l, -40, G))),
47: ("meadow", C(X(cracked, 0, G))),
48: ("valley", C(X(grave_open, 0, G), F(walk, -70, G, 1))),
49: ("meadow", C(F(lie, 0, G, 1))),
50: ("cemetery", C(X(coffin_up, 0, G), X(belt_on, 0, G), F(stand, -50, G))),
51: ("meadow", C(X(stone, 30, G), X(heart_l, 30, G - 26, 0.62), X(ekg_ridge, 200) if False else "", F(kneel, -30, G, 1))),
52: ("valley", C(X(grave_open, 40, G), X(bar_floor, -70, G), F(stand, -20, G))),
53: ("meadow", C(X(worms_soil, 20, G), F(stand, -40, G))),
54: ("cemetery", C(X(coffin_up, 20, G), X(tape, -2, 42, G - 80), F(stand, -40, G))),
55: ("meadow", C(X(skeleton_l, 0, G), lambda r: ''.join(nt.dot(r.uniform(-30, 30), G - r.uniform(60, 90), 1.6) for _ in range(6)))),
56: ("valley", C(F(carry_rock, 0, G, 1))),
57: ("pines", C(F(press, 0, G), X(rain_cloud, 0, G - 104))),
58: ("meadow", C(X(skull_l, 30, G - 18, 1.0), F(sit_hug, -40, G, 1))),
59: ("cemetery", C(X(tomb, 30, G, 1.1), X(tomb, 80, G, 0.9), F(sit_lean, -40, G, 1))),
60: ("valley", C(F(carry_rock, 0, G, 1))),
61: ("pines", C(X(bench_spot, 20, G))),
62: ("valley", C(X(scale_stand, 30, G), F(stand, -50, G))),
63: ("pines", C(F(deadlift, 20, G), F(stand, -50, G))),
64: ("meadow", C(X(bodybag, 20, G))),
65: ("cemetery", C(X(six_carry, 0, G))),
66: ("meadow", C(X(stone, 20, G), X(heart_l, 20, G - 26, 0.62))),
67: ("valley", C(F(sit_hug, 0, G, 1))),
68: ("pines", C(X(bar_floor, 40, G), F(sit_hug, -10, G, 1), F(stand, -50, G))),
69: ("pines", C(X(bottle_l, 30, G), F(sit_hug, -40, G, 1))),
70: ("cemetery", C(X(two_at_grave, 0, G))),
71: ("meadow", C(X(skull_l, 20, G - 18, 1.1))),
72: ("meadow", C(X(hourglass_l, 30, G), F(sit_lean, -50, G, 1))),
73: ("meadow", C(X(cave, 40, G), F(sit_hug, -60, G, 1))),
74: ("meadow", C(X(dead_tree, 20, G, 150), F(stand, -40, G))),
75: ("cemetery", C(X(wreath_l, 30, G), F(stand, -30, G))),
76: ("meadow", C(X(rose_l, 20, G), F(kneel, -30, G, 1))),
77: ("pines", C(X(skeleton_l, 0, G, "sit"))),
78: ("pines", C(F(press, 0, G))),
79: ("pines", C(F(sit_hug, 10, G, 1), X(ghost_l, -40, G))),
80: ("pines", C(X(drawer, 20, G), F(stand, -80, G))),
81: ("cabin", C(X(bed_l, 0, G))),
82: ("cemetery", C(X(cradle, -50, G), X(tomb, 50, G, 1.0, ""))),
83: ("cemetery", C(F(deadlift, 20, G))),
84: ("pines", C(F(sit_hug, 0, G, 1), lambda r: ghosts(r, (-80, -44, 44, 84)))),
85: ("pines", C(X(drawer, 20, G), F(stand, -80, G))),
86: ("pines", C(X(clock_l, -80, G), F(deadlift, 30, G))),
87: ("cemetery", C(X(tomb, 30, G, 1.2), X(rose_l, 0, G), F(kneel, -40, G, 1))),
88: ("valley", C(X(grave_open, 20, G), F(walk, -80, G, -1))),
89: ("meadow", C(X(rose_l, 10, G), lambda r: ''.join(nt.dot(r.uniform(10, 50), G - r.uniform(60, 90), 1.4) for _ in range(5)))),
90: ("cemetery", C(X(tomb, 30, G, 1.3, "R.I.P."), F(stand, -30, G))),
91: ("meadow", C(X(hourglass_l, 0, G), X(skull_l, 50, G - 12, 0.5))),
92: ("meadow", C(X(skeleton_l, 0, G))),
93: ("cemetery", C(X(coffin_up, 20, G), X(bar_floor, -50, G))),
94: ("cabin", C(X(bed_l, 0, G), X(clock_l, 100, G))),
95: ("meadow", C(X(ekg_ridge, 150), F(lie, 0, G, 1))),
96: ("valley", C(F(carry_rock, 0, G, 1))),
97: ("pines", C(X(two_lifters, 0, G))),
98: ("meadow", C(X(two_on_log, 0, G))),
99: ("meadow", C(F(lie, 0, G, 1))),
100: ("meadow", C(X(stone, 30, G), X(heart_l, 30, G - 26, 0.62), F(kneel, -30, G, 1))),
101: ("pines", C(X(bar_floor, 30, G), F(sit_hug, -40, G, 1))),
102: ("pines", C(F(deadlift, 30, G), X(reaper_l, -60, G, 0.9))),
103: ("pines", C(X(skel_lift, 0, G))),
104: ("pines", C(X(candle_l, -70, G), F(deadlift, 30, G))),
105: ("meadow", C(X(flies_skull, 20, G))),
106: ("pines", C(X(rack_l, 0, G), F(stand, -80, G), F(stand, 70, G), F(stand, 92, G), F(press, 0, G))),
107: ("meadow", C(X(sign_l, 30, G, ("wake up", "eat something", "lift something", "text a friend")), F(stand, -40, G))),
108: ("pines", C(X(body_gore, 30, G), F(stand, -60, G))),
109: ("valley", C(X(scale_stand, 30, G), F(stand, -50, G))),
110: ("pines", C(X(drawer, 20, G), X(thermometer, -90, G))),
111: ("meadow", C(X(sign_l, 30, G, ("MANNER OF DEATH:", "pending")), F(stand, -40, G))),
112: ("pines", C(X(body_gore, 30, G), F(stand, -60, G))),
113: ("meadow", C(X(skull_dashed, 20, G))),
114: ("pines", C(X(table_l, 30, G, 0), X(jar_l, 30, G - 34), F(stand, -60, G))),
115: ("pines", C(X(gurney, -40, G, True), X(gurney, 60, G, True))),
116: ("pines", C(X(bottle_l, -70, G), X(body_gore, 30, G))),
117: ("pines", C(X(body_gore, 30, G))),
118: ("pines", C(X(thermometer, -60, G), X(gurney, 40, G, True))),
119: ("pines", C(X(table_l, 30, G, 0), X(skull_l, 30, G - 50, 0.8), F(stand, -60, G))),
120: ("pines", C(X(gurney, 0, G))),
121: ("meadow", C(X(sign_l, 30, G, ("SKIN:", "MUSCLE:", "BONE:", "REPORT:")), F(stand, -40, G))),
122: ("meadow", C(X(sign_l, 30, G, ("height 5'10\"", "weight 190", "pulse: none")), F(stand, -40, G))),
123: ("meadow", C(X(bodybag, 20, G), lambda r: ''.join(nt.dot(20 + r.uniform(-50, 50), G - r.uniform(40, 90), 1.6) for _ in range(10)))),
124: ("meadow", C(X(skeleton_lie, 20, G))),
125: ("meadow", C(X(skeleton_lie, 20, G))),
126: ("meadow", C(X(bodybag, 20, G), X(big_fly, 20, G - 80))),
127: ("meadow", C(X(skull_l, 20, G - 18, 1.0), X(maggots, 20, G - 4), lambda r: ''.join(nt.dot(20 + r.uniform(-40, 40), G - r.uniform(60, 100), 1.5) for _ in range(6)))),
128: ("meadow", C(X(skull_l, 20, G - 18, 1.2), lambda r: ''.join(ell(20 + r.uniform(-26, 26), G - r.uniform(6, 40), 3, 2, 1.2) for _ in range(8)))),
129: ("cemetery", C(X(grave_open, 10, G))),
130: ("meadow", C(X(skeleton_lie, 20, G))),
131: ("valley", C(X(grave_open, 0, G))),
132: ("meadow", C(X(shrooms_l, 20, G), F(sit_hug, -50, G, 1))),
133: ("valley", C(X(roots_skull, 20, G))),
134: ("meadow", C(X(skull_l, 20, G - 18, 1.2), lambda r: ''.join(ell(20 + u, G - 22 + v, 3, 2, 1.2) for u, v in ((-11, -2), (11, 0), (-14, 8))))),
135: ("meadow", C(X(bodybag, -60, G), X(skeleton_lie, 70, G))),
136: ("meadow", C(X(skeleton_lie, 20, G))),
137: ("meadow", C(X(crows_tree, 20, G))),
138: ("pines", C(F(deadlift, 0, G))),
139: ("pines", C(X(bar_floor, 40, G), F(sit_hug, -20, G, 1))),
140: ("pines", C(F(press, 0, G))),
141: ("pines", C(X(skeleton_l, 0, G))),
142: ("meadow", C(X(stone, -60, G), X(heart_l, -60, G - 26, 0.62), F(deadlift, 40, G))),
143: ("pines", C(X(bar_floor, 40, G), F(stand, -30, G))),
144: ("pines", C(F(deadlift, -40, G), X(skeleton_l, 50, G))),
145: ("pines", C(X(bar_floor, 50, G), F(sit_hug, -20, G, 1))),
146: ("pines", C(X(campfire, 30, G), F(stand, -30, G))),
147: ("pines", C(X(body_gore, 30, G), X(sign_l, -80, G, ("1", "2", "3")))),
148: ("meadow", C(X(stone, 20, G), X(heart_l, 20, G - 26, 0.62))),
149: ("pines", C(F(deadlift, 0, G))),
150: ("pines", C(X(skel_lift, 0, G))),
151: ("pines", C(X(campfire, 30, G), F(stand, -30, G))),
152: ("meadow", C(X(skull_teeth, 0, G))),
153: ("pines", C(F(press, 0, G))),
154: ("meadow", C(X(skull_teeth, 0, G))),
155: ("pines", C(X(rack_l, 0, G), X(skeleton_l, 0, G))),
156: ("pines", C(X(table_l, 30, G, 0), X(jar_l, 30, G - 34), F(stand, -60, G))),
157: ("pines", C(X(body_gore, 30, G), F(stand, -60, G))),
158: ("valley", C(X(grave_open, 10, G), X(tape, -40, 34, G - 22), F(stand, -80, G))),
159: ("cemetery", C(X(coffin_up, 20, G), F(stand, -40, G))),
160: ("cemetery", C(X(grave_open, 0, G), F(coffin_side, -10, G - 40, 60, 12))),
161: ("valley", C(X(grave_open, 0, G), F(walk, -70, G, 1))),
162: ("cemetery", C(X(tomb, 20, G, 1.3, "____"))),
163: ("meadow", C(X(row_markers, 0, G))),
164: ("cemetery", C(X(grave_open, 10, G))),
165: ("cemetery", C(X(grave_mound, 0, G, 50), X(bell_post, 10, G))),
166: ("pines", C(X(bones_pile, 20, G))),
167: ("valley", C(X(hearse_l, 20, G))),
168: ("cemetery", C(X(wreath_l, 20, G))),
169: ("cemetery", C(X(coffin_up, 20, G))),
170: ("cabin", C(X(chair_l, -40, G), X(table_l, 40, G))),
171: ("cabin", C(X(phone_l, 30, G), F(sit_hug, -40, G, 1))),
172: ("cabin", C(X(phone_l, 30, G), F(sit_hug, -40, G, 1))),
173: ("cabin", C(X(table_l, 30, G, 0), X(urn_l, 30, G - 34, 0.9), F(sit_hug, -50, G, 1))),
174: ("cabin", C(X(monitor_bed, 0, G))),
175: ("cabin", C(X(table_l, 20, G), lambda r: ''.join(shape(r, rect_pts(-10 + i * 4, G - 44 - i * 8, 50, 7), 1.4) for i in range(4)))),
176: ("meadow", C(lambda r: shape(r, rect_pts(0, G - 30, 60, 30)), X(heart_l, 30, G - 34, 0.5), F(stand, -40, G))),
177: ("cemetery", C(X(tomb, 40, G, 1.1), F(stand, -20, G), lambda r: shape(r, rect_pts(-12, G - 34, 12, 14), 1.2))),
178: ("pines", C(X(candle_out, 20, G), F(sit_hug, -40, G, 1))),
179: ("cabin", C(X(table_l, 20, G), X(chair_l, -70, G))),
180: ("valley", C(X(hourglass_l, -40, G), X(reaper_l, 50, G, 0.9))),
181: ("meadow", C(F(stand, -25, G), X(skeleton_l, 25, G))),
182: ("valley", C(X(sign_l, -40, G, ("NAMES:", "_____", "_____", "you")), X(reaper_l, 50, G, 0.9))),
183: ("meadow", C(X(dance, 0, G))),
184: ("valley", C(X(reaper_l, 20, G, 1.0), X(stone, -40, G))),
185: ("meadow", C(X(crown_skulls, 0, G))),
186: ("pines", C(X(skull_l, 20, G - 18, 0.9), X(candle_l, 20, G - 40))),
187: ("valley", C(X(barrow, 20, G), F(walk, -60, G, 1))),
188: ("valley", C(X(sign_l, -40, G, ("NOW SERVING", "713")), X(reaper_l, 50, G, 0.9))),
189: ("valley", C(X(barrow, 20, G), F(walk, -60, G, 1))),
190: ("pines", C(X(crem_l, 20, G), F(walk, -80, G, 1))),
191: ("pines", C(X(bones_pile, 20, G), X(urn_l, -60, G, 0.8))),
192: ("cabin", C(X(table_l, 20, G, 0), X(urn_l, 20, G - 34, 0.9))),
193: ("pines", C(X(crem_l, 20, G))),
194: ("valley", C(X(ash_lake_l, 20, G), X(urn_l, -80, G, 0.6), F(stand, -110, G))),
195: ("pines", C(X(gurney, 30, G, False), X(sign_l, -80, G, ("REMOVE", "battery: done")))),
196: ("cabin", C(X(table_l, 20, G, 0), X(scale_urn, 20, G - 34))),
197: ("cabin", C(X(table_l, 20, G, 0), X(urn_l, 20, G - 34, 0.9), lambda r: ell(56, G - 44, 8, 8, 1.6) + hand("#", 8, 56, G - 41))),
198: ("meadow", C(X(sign_l, 30, G, ("SOMEDAY", "_ _ _ _ _", "_ _ _ _ _")), F(stand, -40, G))),
199: ("valley", C(F(sit_hug, 0, G, 1), X(rain_cloud, 0, G - 72))),
200: ("cabin", C(X(bed_l, 0, G))),
201: ("pines", C(F(sit_hug, 0, G, 1), X(moth, 10, G - 70), X(moth, -30, G - 90))),
202: ("pines", C(X(trap_l, 30, G), F(sit_hug, -50, G, 1))),
203: ("pines", C(F(press, 0, G))),
204: ("cabin", C(X(monitor_bed, 0, G))),
205: ("meadow", C(X(skull_teeth, 0, G))),
206: ("valley", C(X(skull_l, 20, G - 18, 1.2), lambda r: jl([(0, G - 46), (10, G - 60), (24, G - 44), (36, G - 58), (44, G - 40)], r, 1.4, 1.5, 3))),
207: ("pines", C(lambda r: shape(r, rect_pts(-50, G - 18, 100, 6)) + jl([(-40, G - 12), (-40, G)], r, 2) + jl([(40, G - 12), (40, G)], r, 2), X(skeleton_l, 0, G - 18, "sit"))),
}

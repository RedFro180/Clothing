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

# ---------- pass 2 (2026-11-27): closer caption matches + visual puns ----------
def lifter_up(x, y):                           # overhead-press body without a bar
    return (head(x, y - 44) + pl([(x, y - 36), (x, y - 16)], 2.6) + pl([(x - 10, y), (x, y - 16), (x + 10, y)], 2.6)
            + pl([(x - 3, y - 32), (x - 16, y - 46), (x - 18, y - 64)], 2.3) + pl([(x + 3, y - 32), (x + 16, y - 46), (x + 18, y - 64)], 2.3))
def bear(r, x, y, k=1):                        # little seated bear (load-BEARING)
    g = ell(x, y - 10 * k, 9 * k, 10 * k) + ell(x, y - 26 * k, 7.5 * k, 7 * k) + ell(x - 6 * k, y - 32 * k, 2.8 * k, 2.8 * k, 1.4) + ell(x + 6 * k, y - 32 * k, 2.8 * k, 2.8 * k, 1.4)
    g += ell(x, y - 23 * k, 3.4 * k, 2.4 * k, 1.2) + nt.dot(x - 3 * k, y - 28 * k, 1.1) + nt.dot(x + 3 * k, y - 28 * k, 1.1)
    return g + ell(x - 7 * k, y - 2 * k, 3.5 * k, 2.5 * k, 1.3) + ell(x + 7 * k, y - 2 * k, 3.5 * k, 2.5 * k, 1.3)
def bear_press(r, x, y):
    return lifter_up(x, y) + pl([(x - 52, y - 64), (x + 52, y - 64)], 2.6) + bear(r, x - 44, y - 64, 0.9) + bear(r, x + 44, y - 64, 0.9)
def champ_skull(r, x, y):                      # mortality = undefeated champion
    g = skull_l(r, x, y - 30, 1.1) + shape(r, rect_pts(x - 40, y - 8, 80, 12), 2) + ell(x, y - 2, 14, 11) + hand("1", 12, x, y + 2)
    return g + ''.join(ell(x + u, y - 2, 3, 3, 1.2) for u in (-28, 28))
def cloud_plates(r, x, y):                     # thoughts as the plates
    g = lifter_up(x, y) + pl([(x - 56, y - 64), (x + 56, y - 64)], 2.6)
    for d in (-1, 1):
        cx = x + d * 50
        g += shape(r, [(cx - 14, y - 60), (cx - 16, y - 70), (cx - 8, y - 78), (cx + 2, y - 76), (cx + 10, y - 82), (cx + 16, y - 70), (cx + 14, y - 60)], 1.8)
    return g
def cutting_board(r, x, y):
    return table_l(r, x, y, 0) + shape(r, rect_pts(x - 40, y - 42, 80, 8)) + heart_l(r, x - 6, y - 46, 0.4) + jl([(x + 24, y - 44), (x + 44, y - 60)], r, 2.4) + shape(r, [(x + 40, y - 56), (x + 52, y - 74), (x + 46, y - 54)], 1.4)
def mirror(r, x, y):
    return jl([(x - 16, y), (x - 8, y - 20)], r, 2) + jl([(x + 16, y), (x + 8, y - 20)], r, 2) + shape(r, rect_pts(x - 22, y - 100, 44, 80)) + skull_l(r, x, y - 64, 0.6)
def sunrise(r, x, y):
    g = f'<path d="M{x-36} {y} A36 36 0 0 1 {x+36} {y}" fill="none" stroke="{I()}" stroke-width="2.2"/>'
    return g + ''.join(pl([(x + 44 * math.cos(a), y - 44 * math.sin(a)), (x + 56 * math.cos(a), y - 56 * math.sin(a))], 1.8) for a in [i * math.pi / 8 for i in range(1, 8)])
def banana(r, x, y, spots=False):
    g = f'<path d="M{x-30} {y-30} Q{x-24} {y} {x+26} {y-4} Q{x+30} {y-10} {x+24} {y-12} Q{x-12} {y-10} {x-22} {y-34} Z" fill="{B()}" stroke="{I()}" stroke-width="2"/>'
    return g + (''.join(nt.dot(x + u, y + v, 2.2) for u, v in ((-14, -14), (-4, -10), (8, -8), (16, -9), (-18, -22))) if spots else '')
def crime_tape(r, y):
    return jl([(-150, y), (150, y - 14)], r, 9, 0.3) + jl([(-150, y), (150, y - 14)], r, 6, 0.3, c=B()) + ''.join(hand("DO NOT CROSS", 7, u, y - 7 * (u + 150) / 300 + 2) for u in (-90, 10, 100))
def steak(r, x, y):                           # cartoon meat drumstick (reads as "meat" at any size)
    g = f'<path d="M{x-14} {y-4} Q{x-16} {y-18} {x-2} {y-18} Q{x+12} {y-16} {x+10} {y-2} Q{x+6} {y+8} {x-4} {y+8} Q{x-14} {y+6} {x-14} {y-4} Z" fill="{B()}" stroke="{I()}" stroke-width="2"/>'
    g += jl([(x + 6, y + 4), (x + 16, y + 14)], r, 3, 0.2) + ell(x + 18, y + 13, 3, 3, 1.4) + ell(x + 14, y + 17, 3, 3, 1.4)
    return g + jl([(x - 8, y - 10), (x - 2, y - 6)], r, 1.2)
def steak_lift(r, x, y):
    return (head(x + 14, y - 34) + pl([(x + 8, y - 28), (x - 10, y - 18)], 2.6) + pl([(x - 10, y - 18), (x - 6, y - 8), (x - 12, y)], 2.6)
            + pl([(x - 10, y - 18), (x + 2, y - 10), (x - 2, y)], 2.6) + pl([(x + 6, y - 26), (x + 6, y - 12)], 2.3) + pl([(x - 50, y - 12), (x + 50, y - 12)], 2.6)
            + steak(r, x - 46, y - 12) + steak(r, x + 46, y - 12))
def tear(r, x, y): return f'<path d="M{x} {y} q-4 7 0 9 q4 -2 0 -9 Z" fill="{I()}"/>'
def heart_pump(r, x, y):
    g = heart_l(r, x - 30, y - 30, 0.6) + shape(r, rect_pts(x + 30, y - 60, 10, 60)) + jl([(x + 22, y - 62), (x + 48, y - 62)], r, 3) + jl([(x + 35, y - 60), (x + 35, y - 72)], r, 2)
    return g + jl([(x + 30, y - 4), (x + 10, y - 2), (x - 4, y - 16), (x - 20, y - 28)], r, 1.6)
def sprout(r, x, y):
    return jl([(x - 16, y), (x - 6, y + 6), (x + 4, y), (x + 14, y + 6)], r, 1.6) + jl([(x, y), (x, y - 28)], r, 2) + shape(r, [(x, y - 20), (x - 14, y - 30), (x - 4, y - 18)], 1.4) + shape(r, [(x, y - 26), (x + 14, y - 36), (x + 4, y - 24)], 1.4)
def molar_roots(r, x, y):
    g = shape(r, [(x - 26, y), (x - 30, y - 30), (x - 18, y - 42), (x, y - 34), (x + 18, y - 42), (x + 30, y - 30), (x + 26, y)])
    g += jl([(x - 18, y), (x - 22, y + 20), (x - 30, y + 34)], r, 2.2) + jl([(x + 18, y), (x + 22, y + 20), (x + 32, y + 34)], r, 2.2) + jl([(x, y), (x + 2, y + 26)], r, 2)
    return g + jl([(x - 2, y - 34), (x + 4, y - 20), (x - 4, y - 8)], r, 1.6)
def easel_steak(r, x, y):
    g = jl([(x - 30, y), (x, y - 110)], r, 2.2) + jl([(x + 30, y), (x, y - 110)], r, 2.2) + jl([(x, y - 100), (x + 10, y)], r, 2)
    return g + shape(r, rect_pts(x - 34, y - 96, 68, 56)) + shape(r, rect_pts(x - 28, y - 90, 56, 44), 1.4) + steak(r, x, y - 68)
def vault_box(r, x, y):
    g = shape(r, rect_pts(x - 70, y - 50, 140, 50)) + ''.join(nt.dot(x + r.uniform(-64, 64), y - r.uniform(4, 46), 1.1) for _ in range(20))
    return g + coffin_side(x, y - 20, 90, 14)
def flex_smile(r, x, y):
    g = head(x, y - 44, 9) + f'<path d="M{x-5} {y-42} Q{x} {y-36} {x+5} {y-42}" fill="none" stroke="{I()}" stroke-width="1.6"/>'
    g += pl([(x, y - 35), (x, y - 16)], 2.6) + pl([(x - 8, y), (x, y - 16), (x + 8, y)], 2.6)
    return g + pl([(x - 2, y - 32), (x - 18, y - 32), (x - 20, y - 48)], 2.4) + pl([(x + 2, y - 32), (x + 18, y - 32), (x + 20, y - 48)], 2.4)
def runner_battery(r, x, y):
    g = (head(x + 6, y - 42) + pl([(x + 4, y - 34), (x - 2, y - 16)], 2.6) + pl([(x - 16, y - 2), (x - 2, y - 16), (x + 10, y - 8), (x + 12, y)], 2.6)
         + pl([(x - 10, y - 26), (x + 2, y - 30), (x + 14, y - 22)], 2.2))
    return g + shape(r, rect_pts(x + 30, y - 76, 40, 18), 1.8) + shape(r, rect_pts(x + 70, y - 71, 4, 8), 1.4) + f'<rect x="{x+33}" y="{y-73}" width="7" height="12" fill="{I()}"/>'
def xray(r, x, y):                            # body outline with the skeleton showing inside
    g = ell(x, y - 50, 10, 10.5, 2, False)
    g += f'<path d="M{x-14} {y-38} L{x+14} {y-38} L{x+16} {y-16} L{x+10} {y} L{x-10} {y} L{x-16} {y-16} Z" fill="none" stroke="{I()}" stroke-width="2" stroke-dasharray="4 3"/>'
    return g + skeleton_l(r, x, y)
def steam(r, x, y): return ''.join(jl([(x + u, y), (x + u - 4, y - 10), (x + u + 2, y - 20), (x + u - 2, y - 30)], r, 1.4, 0.6, 4) for u in (-10, 0, 10))
def sling(r, x, y): return stand(x, y) + shape(r, [(x - 2, y - 34), (x + 10, y - 18), (x - 6, y - 20)], 1.6)
def thought(r, x, y): return ell(x, y, 22, 14, 1.8) + ell(x - 22, y + 18, 4, 4, 1.4) + ell(x - 30, y + 26, 2.5, 2.5, 1.2) + jl([(x - 12, y), (x - 4, y - 4), (x + 4, y + 2), (x + 12, y - 2)], r, 1.4, 1.2, 3)
def glove_bones(r, x, y):
    g = ''.join(jl([(x - 30 + i * 8, y - 30), (x - 32 + i * 9, y - 60 + abs(i - 2) * 6)], r, 2, 0.4) for i in range(5)) + jl([(x - 20, y - 30), (x - 20, y)], r, 3) + jl([(x - 8, y - 30), (x - 8, y)], r, 3)
    return g + shape(r, [(x + 20, y), (x + 22, y - 18), (x + 34, y - 22), (x + 52, y - 18), (x + 58, y - 6), (x + 54, y)], 1.8)
def life_row(r, x, y):
    g = ell(x - 100, y - 8, 6, 8) + ''.join(ell(x - 60 + i * 6, y - 6, 3.5, 4.5, 1.4) for i in range(4)) + ell(x - 8, y - 8, 7, 11) + big_fly(r, x + 40, y - 14) + skull_l(r, x + 100, y - 18, 0.55)
    return g + ''.join(pl([(x + u, y - 10), (x + u + 10, y - 10)], 1.4) + pl([(x + u + 6, y - 14), (x + u + 10, y - 10), (x + u + 6, y - 6)], 1.4) for u in (-90, -40, 8, 62))
def body_outline(r, x, y):
    return f'<path d="M{x-70} {y-6} Q{x-72} {y-18} {x-60} {y-20} L{x+40} {y-16} L{x+70} {y-22} L{x+74} {y-12} L{x+44} {y-6} L{x+70} {y-2} L{x+66} {y+4} L{x+36} {y+2} L{x-56} {y+4} Q{x-70} {y+6} {x-70} {y-6} Z" fill="none" stroke="{I()}" stroke-width="2" stroke-dasharray="5 4"/>'
def squashed(r, x, y):
    g = head(x, y - 22) + pl([(x, y - 14), (x - 2, y - 6)], 2.6) + pl([(x - 2, y - 6), (x - 14, y - 10), (x - 12, y)], 2.4) + pl([(x - 2, y - 6), (x + 12, y - 10), (x + 12, y)], 2.4)
    g += pl([(x - 4, y - 18), (x - 18, y - 30)], 2) + pl([(x + 4, y - 18), (x + 18, y - 30)], 2) + pl([(x - 70, y - 30), (x + 70, y - 30)], 3)
    return g + ''.join(f'<rect x="{x+d*(52+k*8)-3:.0f}" y="{y-30-(26-k*3)}" width="6" height="{2*(26-k*3)}" rx="1.5" fill="{B()}" stroke="{I()}" stroke-width="1.8"/>' for d in (-1, 1) for k in range(3))
def flame_in(r, x, y, arms=False):           # figure with a fire showing in the chest (and on the limbs for "every nerve")
    g = stand(x, y, 1.3)
    g += f'<path d="M{x} {y-18} Q{x-18} {y-26} {x-6} {y-44} Q{x-2} {y-36} {x} {y-56} Q{x+4} {y-38} {x+8} {y-46} Q{x+18} {y-28} {x} {y-18} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>'
    g += f'<path d="M{x} {y-22} Q{x-8} {y-28} {x} {y-42} Q{x+8} {y-28} {x} {y-22} Z" fill="{I()}"/>'
    if arms:
        g += ''.join(f'<path d="M{x+u} {y+v} q-4 -6 0 -12 q4 6 0 12 Z" fill="none" stroke="{I()}" stroke-width="1.6"/>' for u, v in ((-16, -18), (16, -18), (-10, 2), (10, 2), (0, -70)))
    return g
def hammer(r, x, y): return jl([(x, y), (x + 20, y - 26)], r, 2.4) + shape(r, rect_pts(x + 12, y - 36, 22, 9), 1.6)
def clock_at(r, x, y, h):
    a = math.radians(h * 30 - 90)
    return jl([(x, y), (x, y - 50)], r, 2.6) + ell(x, y - 74, 22, 22) + pl([(x, y - 74), (x + 12 * math.cos(a), y - 74 + 12 * math.sin(a))], 2.2) + pl([(x, y - 74), (x, y - 92)], 1.8)
def chalk_squat(r, x, y):
    da = ' stroke-dasharray="5 4"'
    g = f'<circle cx="{x}" cy="{y-54}" r="8" fill="none" stroke="{I()}" stroke-width="2"{da}/>'
    g += f'<path d="M{x} {y-46} L{x-6} {y-24} L{x+10} {y-18} L{x+6} {y} M{x-6} {y-24} L{x-14} {y-14} L{x-12} {y} M{x-2} {y-42} L{x-14} {y-56} M{x+2} {y-42} L{x+14} {y-56}" fill="none" stroke="{I()}" stroke-width="2.2"{da}/>'
    return g + barbell_l(x, y - 58, 50)
def gut(r, x, y): return sit_hug(x, y, 1) + jl([(x + 6, y - 20), (x + 10, y - 22), (x + 8, y - 16), (x + 4, y - 18)], r, 1.2, 0.2, 2) + ''.join(nt.dot(x + r.uniform(0, 12), y - r.uniform(12, 26), 0.9) for _ in range(6))

SPEC.update({
6: ("valley", C(X(runner_battery, -20, G))),
11: ("meadow", C(X(xray, 0, G))),
15: ("pines", C(F(deadlift, 0, G), X(steam, 14, G - 50))),
18: ("meadow", C(X(champ_skull, 20, G), F(kneel, -50, G, 1))),
29: ("valley", C(X(sling, 0, G))),
35: ("cemetery", C(X(tomb, 30, G, 1.3, "YOU"), F(stand, -30, G))),
36: ("cabin", C(X(bed_l, 0, G), X(thought, -30, G - 70), X(clock_l, 100, G))),
57: ("pines", C(X(cloud_plates, 0, G))),
66: ("pines", C(X(cutting_board, 20, G))),
71: ("meadow", C(X(mirror, 30, G), F(stand, -20, G))),
74: ("meadow", C(X(cracked, 0, G), X(dead_tree, 70, G, 120))),
87: ("cemetery", C(X(sunrise, 40, G - 20), X(tomb, 40, G, 1.1), X(rose_l, 10, G), F(kneel, -40, G, 1))),
124: ("meadow", C(X(glove_bones, 0, G))),
125: ("meadow", C(X(banana, -40, G), X(banana, 40, G, True))),
126: ("meadow", C(X(bodybag, 20, G), X(big_fly, 20, G - 80), X(crime_tape, G - 40))),
127: ("meadow", C(X(life_row, 0, G))),
129: ("cemetery", C(X(grave_open, 10, G), X(candle_l, -70, G))),
130: ("meadow", C(X(skeleton_l, 0, G), lambda r: shape(r, rect_pts(-9, G - 36, 18, 6), 1.6))),
131: ("meadow", C(X(body_outline, 0, G - 6))),
136: ("meadow", C(X(gut, 0, G))),
138: ("pines", C(X(steak_lift, 0, G))),
139: ("pines", C(X(bar_floor, 40, G), F(sit_hug, -20, G, 1), X(tear, -10, G - 36))),
140: ("pines", C(X(squashed, 0, G))),
141: ("meadow", C(X(xray, 0, G))),
142: ("meadow", C(X(heart_pump, 0, G))),
146: ("pines", C(X(flame_in, 0, G))),
149: ("pines", C(F(deadlift, -30, G), X(sprout, 60, G))),
151: ("pines", C(X(flame_in, 0, G, True))),
152: ("meadow", C(X(molar_roots, 0, G))),
153: ("pines", C(X(bear_press, 0, G))),
157: ("pines", C(X(easel_steak, 20, G), F(stand, -50, G))),
159: ("cemetery", C(X(coffin_up, 20, G), X(hammer, -30, G), F(stand, -60, G))),
160: ("cemetery", C(X(grave_open, 0, G), F(coffin_side, -10, G - 40, 60, 12), X(clock_at, -90, G, 2))),
169: ("cemetery", C(X(vault_box, 0, G))),
203: ("pines", C(X(chalk_squat, 0, G))),
205: ("meadow", C(X(flex_smile, 0, G))),
})

# ---------- pass 3 (2026-11-27): user notes on 01-12 + variety ----------
import redo_vary as V
def skel_lift(r, x, y):                       # skeleton holding a barbell at the hips, arms straight down to the bar
    g = skull_l(r, x, y - 70, 0.36) + pl([(x, y - 60), (x, y - 30)], 2.4) + ''.join(pl([(x - 8, y + v), (x, y + v - 2), (x + 8, y + v)], 1.4) for v in (-56, -50, -44))
    g += pl([(x - 9, y - 56), (x + 9, y - 56)], 2) + pl([(x - 9, y - 56), (x - 12, y - 30)], 2) + pl([(x + 9, y - 56), (x + 12, y - 30)], 2)
    g += pl([(x - 6, y - 30), (x - 7, y - 14), (x - 6, y)], 2.2) + pl([(x + 6, y - 30), (x + 7, y - 14), (x + 6, y)], 2.2) + pl([(x - 8, y - 30), (x + 8, y - 30)], 2)
    return g + ''.join(nt.dot(x + u, y - 30, 2.4) for u in (-12, 12)) + barbell_l(x, y - 30, 58)
def meat_pile(r, x, y):                       # low lumpy heap of flesh with a bone sticking out
    g = shape(r, [(x - 34, y), (x - 30, y - 8), (x - 20, y - 14), (x - 8, y - 12), (x + 2, y - 18), (x + 14, y - 14), (x + 26, y - 10), (x + 34, y)])
    g += jl([(x - 22, y - 6), (x - 10, y - 9)], r, 1.1) + jl([(x + 4, y - 8), (x + 18, y - 6)], r, 1.1) + jl([(x - 4, y - 3), (x + 8, y - 2)], r, 1.1)
    return g + jl([(x + 10, y - 14), (x + 22, y - 28)], r, 3.2, 0.2) + ell(x + 24, y - 30, 3, 3, 1.4) + ell(x + 20, y - 32, 3, 3, 1.4)
def bench_spot(r, x, y, spotter=True, skel=False):   # clean bench press: lifter on the bench, spotter behind the head
    g = jl([(x - 46, y - 20), (x + 40, y - 20)], r, 3) + jl([(x - 38, y - 20), (x - 38, y)], r, 2) + jl([(x + 32, y - 20), (x + 32, y)], r, 2)
    hx = x - 40
    g += head(hx, y - 28, 6.5) + pl([(hx + 8, y - 26), (x + 8, y - 26)], 2.6)          # body along the bench
    g += pl([(x + 8, y - 26), (x + 22, y - 40), (x + 30, y)], 2.4)                       # knee up, foot on floor
    g += pl([(x - 22, y - 26), (x - 22, y - 62)], 2.2) + pl([(x - 10, y - 26), (x - 10, y - 62)], 2.2)   # arms straight up
    g += barbell_l(x - 16, y - 62, 46)
    if spotter:
        sx = x - 72
        g += head(sx + 4, y - 64) + pl([(sx + 2, y - 56), (sx, y - 30)], 2.6) + pl([(sx - 8, y), (sx, y - 30), (sx + 6, y)], 2.6)
        g += pl([(sx + 2, y - 52), (x - 40, y - 58)], 2.1) + pl([(sx + 2, y - 48), (x - 36, y - 64)], 2.1)   # hands under the bar
    return g
def tomb_plates_carry(r, x, y):               # bar across the shoulders, RIP headstones as the plates
    g = head(x, y - 48) + pl([(x, y - 40), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6)
    g += pl([(x - 3, y - 36), (x - 16, y - 44), (x - 18, y - 52)], 2.2) + pl([(x + 3, y - 36), (x + 16, y - 44), (x + 18, y - 52)], 2.2)
    g += pl([(x - 74, y - 52), (x + 74, y - 52)], 2.8)
    for d in (-1, 1):
        g += tomb(r, x + d * 62, y - 34, 0.5, "RIP")
    return g
def skel_run(r, x, y):
    g = skull_l(r, x + 4, y - 64, 0.34) + pl([(x + 2, y - 54), (x - 2, y - 28)], 2.2) + ''.join(pl([(x - 6, y + v), (x, y + v - 2), (x + 6, y + v)], 1.3) for v in (-50, -44, -38))
    g += pl([(x, y - 48), (x + 12, y - 40), (x + 18, y - 48)], 1.9) + pl([(x, y - 48), (x - 12, y - 38), (x - 20, y - 42)], 1.9)
    g += pl([(x - 2, y - 28), (x + 14, y - 16), (x + 12, y - 2), (x + 20, y)], 2.1) + pl([(x - 2, y - 28), (x - 14, y - 18), (x - 26, y - 22), (x - 30, y - 16)], 2.1)
    return g + ''.join(jl([(x - 40 - k * 8, y - 30 + k * 8), (x - 52 - k * 8, y - 30 + k * 8)], r, 1, 0.3) for k in range(3))
def piggyback(r, x, y):                       # walking, a skeleton riding on the back with its arms around the neck
    g = walk(x, y, 1)
    s = skull_l(r, x - 9, y - 50, 0.3)
    s += pl([(x - 10, y - 42), (x - 14, y - 22)], 2) + ''.join(pl([(x - 17, y + v), (x - 12, y + v - 2), (x - 7, y + v)], 1.2) for v in (-38, -33, -28))
    s += pl([(x - 10, y - 38), (x - 2, y - 34), (x + 4, y - 32)], 1.8) + pl([(x - 12, y - 36), (x - 4, y - 30), (x + 4, y - 30)], 1.6)
    s += pl([(x - 14, y - 22), (x - 2, y - 20), (x + 4, y - 12)], 1.8) + pl([(x - 14, y - 22), (x - 4, y - 16), (x - 2, y - 8)], 1.6)
    return g + s
def two_bone_piles(r, x, y): return bones_pile(r, x - 55, y) + bones_pile(r, x + 55, y)
def tagged_feet(r, x, y):                     # one long sheet, a row of feet poking out, every foot tagged: everyone
    g = jl([(x - 100, y - 24), (x + 80, y - 24)], r, 2.6) + ''.join(jl([(x + u, y - 24), (x + u, y)], r, 2) for u in (-92, 72))
    g += shape(r, [(x - 100, y - 26), (x - 94, y - 40), (x - 40, y - 44), (x + 20, y - 40), (x + 70, y - 42), (x + 80, y - 26)])
    for i, u in enumerate((-60, -30, 0, 30)):
        g += ell(x + u, y - 46, 4, 6) + jl([(x + u + 3, y - 50), (x + u + 8, y - 60)], r, 1) + shape(r, [(x + u + 4, y - 60), (x + u + 16, y - 66), (x + u + 18, y - 58), (x + u + 6, y - 54)], 1.2)
    return g
def half_face(r, x, y):                       # matches the original #11 art: half living face, half skull
    g = f'<path d="M{x} {y-118} Q{x-40} {y-116} {x-42} {y-76} Q{x-40} {y-46} {x-18} {y-38} L{x} {y-36} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>'
    g += f'<path d="M{x} {y-118} Q{x+40} {y-116} {x+42} {y-76} Q{x+40} {y-46} {x+18} {y-38} L{x} {y-36} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>'
    g += ell(x - 18, y - 82, 9, 10) + jl([(x - 6, y - 64), (x - 2, y - 72), (x + 2, y - 64)], r, 1.6) + ''.join(pl([(x - u, y - 52), (x - u, y - 42)], 1.4) for u in (2, 8, 14, 20))
    g += pl([(x - 26, y - 46), (x - 2, y - 48)], 1.6) + jl([(x - 4, y - 104), (x - 10, y - 96), (x - 4, y - 88), (x - 10, y - 78), (x - 4, y - 68)], r, 1.2, 0.3, 3)
    g += ell(x + 17, y - 82, 7, 4.5) + nt.dot(x + 17, y - 82, 2.4) + jl([(x + 8, y - 92), (x + 26, y - 94)], r, 1.6)
    g += jl([(x + 4, y - 74), (x + 8, y - 64), (x + 3, y - 62)], r, 1.6) + f'<path d="M{x+4} {y-50} Q{x+14} {y-46} {x+22} {y-50}" fill="none" stroke="{I()}" stroke-width="1.8"/>'
    g += jl([(x + 6, y - 118), (x + 18, y - 124), (x + 32, y - 116), (x + 40, y - 104)], r, 1.6)
    g += pl([(x - 22, y - 36), (x - 46, y - 24), (x - 60, y)], 2.2) + pl([(x + 22, y - 36), (x + 46, y - 24), (x + 60, y)], 2.2)
    return g
def stargazer(r, x, y):
    return lie(x, y, 1) + barbell_l(x + 70, y - 12, 34)

SPEC.update({
1: ("pines", C(X(skel_lift, 0, G))),
2: ("meadow", C(X(skeleton_l, -20, G), X(meat_pile, 30, G))),
3: ("pines", C(X(bench_spot, 30, G))),
4: ("valley", C(X(tomb_plates_carry, 0, G))),
6: ("valley", C(X(skel_run, 0, G))),
7: ("valley", C(X(piggyback, 0, G))),
8: ("meadow", C(X(two_bone_piles, 0, G))),
10: ("pines", C(X(tagged_feet, 10, G))),
11: ("meadow", C(X(half_face, 0, G))),
12: ("pines", C(X(stargazer, -30, G))),
21: ("pines", C(X(bench_spot, 30, G))),
38: ("pines", C(X(bench_spot, 30, G))),
61: ("pines", C(X(bench_spot, 30, G))),
})
V.OVERRIDE.update({12: dict(sky="milky", trees="pine"), 1: dict(sky="none"), 3: dict(sky="none"), 11: dict(sky="none"), 10: dict(sky="none")})

# ---------- v2 critique fixes (no frame / hanging silhouettes) ----------
def bearers(r, x, y, n=2):                     # coffin carried at shoulder height; heads clearly above it
    us = [-34, 34] if n == 2 else [-48, -16, 16, 48]
    g = ''
    for u in us:
        g += head(x + u, y - 62) + pl([(x + u, y - 54), (x + u, y - 18)], 2.6) + pl([(x + u - 8, y), (x + u, y - 18), (x + u + 8, y)], 2.6)
    g += coffin_side(x, y - 40, 120 if n > 2 else 96, 16)
    return g
def friends_lift(r, x, y):                     # lifter deadlifting, three friends standing round cheering
    g = deadlift(x, y)
    for u in (-80, 70, 96):
        g += stand(x + u, y) + pl([(x + u - 8, y - 18), (x + u - 12, y - 36)], 2)
    return g
def bell_grave(r, x, y):                       # handbell resting on the grave mound, string running into the ground
    g = grave_mound(r, x, y, 70) + jl([(x + 10, y - 6), (x + 30, y - 4), (x + 38, y)], r, 1, 0.4)
    return g + shape(r, [(x - 6, y - 8), (x - 12, y - 8), (x - 8, y - 22), (x, y - 28), (x + 8, y - 22), (x + 12, y - 8), (x + 6, y - 8)], 2) + jl([(x, y - 28), (x, y - 34)], r, 2.4)
SPEC.update({
25: ("cemetery", C(X(bearers, 0, G, 2))),
65: ("cemetery", C(X(bearers, 0, G, 4))),
106: ("pines", C(X(friends_lift, 0, G))),
155: ("pines", C(X(skel_lift, 0, G))),
165: ("cemetery", C(X(bell_grave, 0, G))),
})
def bearers_walk(r, x, y):
    g = ''.join(walk(x + u, y, 1) for u in (-50, -18, 14, 46))
    return g + coffin_side(x - 2, y - 17, 128, 15)
SPEC.update({25: ("cemetery", C(X(coffin_backpack, 0, G))), 65: ("cemetery", C(X(bearers_walk, 0, G)))})

# ---------- v3 review fixes (flat ground) ----------
def bench_spot(r, x, y, spotter=True, skel=False):
    """Side view bench press: the bar is seen end-on (plate circle) over the chest; spotter stands behind the head."""
    g = jl([(x - 46, y - 20), (x + 40, y - 20)], r, 3) + jl([(x - 38, y - 20), (x - 38, y)], r, 2) + jl([(x + 32, y - 20), (x + 32, y)], r, 2)
    g += head(x - 38, y - 28, 6.5) + pl([(x - 30, y - 26), (x + 8, y - 26)], 2.6)
    g += pl([(x + 8, y - 26), (x + 22, y - 42), (x + 28, y)], 2.4)
    g += pl([(x - 24, y - 26), (x - 22, y - 44), (x - 20, y - 60)], 2.4)                 # arms locked out
    g += ell(x - 20, y - 68, 13, 13) + ell(x - 20, y - 68, 3, 3)                          # plate, bar end-on
    if spotter:
        sx = x - 74
        g += (skeleton_l(r, sx, y) if skel else head(sx, y - 66) + pl([(sx, y - 58), (sx, y - 30)], 2.6) + pl([(sx - 8, y), (sx, y - 30), (sx + 8, y)], 2.6))
        g += pl([(sx + 2, y - 52), (x - 50, y - 60), (x - 36, y - 66)], 2.1) + pl([(sx + 2, y - 48), (x - 48, y - 54), (x - 34, y - 60)], 2.1)
    return g
SPEC.update({n: ("pines", C(X(bench_spot, 30, G))) for n in (3, 21, 38, 61)})
def tag_gurney(r, x, y):                     # covered body on a gurney, feet out, a big toe tag hanging off
    g = gurney(r, x - 14, y, tag=False)
    g += jl([(x + 50, y - 36), (x + 56, y - 22)], r, 1.4)
    g += shape(r, [(x + 48, y - 22), (x + 74, y - 28), (x + 80, y - 6), (x + 54, y)], 2)
    g += ell(x + 54, y - 17, 2, 2, 1.2) + ''.join(jl([(x + 60 + u * 0.1, y - 16 + u), (x + 74, y - 20 + u)], r, 1.1) for u in (0, 6))
    return g
def meat_pile(r, x, y):                      # butcher's heap: two steaks flat, one leaning, a drumstick bone on top
    g = ell(x - 12, y - 7, 22, 7) + ell(x - 14, y - 7, 15, 4, 1.1, False) + ell(x - 20, y - 8, 3, 2, 1.1, False)
    g += ell(x + 16, y - 9, 20, 8) + ell(x + 15, y - 9, 13, 4.5, 1.1, False) + ell(x + 22, y - 10, 3, 2, 1.1, False)
    g += shape(r, [(x - 4, y - 14), (x + 2, y - 30), (x + 18, y - 34), (x + 26, y - 22), (x + 18, y - 14)], 2.2)
    g += jl([(x + 4, y - 22), (x + 16, y - 28)], r, 1) + jl([(x + 8, y - 18), (x + 20, y - 22)], r, 1)
    g += jl([(x - 18, y - 16), (x - 34, y - 30)], r, 3.4, 0.2) + ell(x - 36, y - 33, 3.2, 3.2, 1.4) + ell(x - 32, y - 35, 3.2, 3.2, 1.4)
    g += shape(r, [(x - 22, y - 12), (x - 10, y - 14), (x - 12, y - 24), (x - 20, y - 22)], 1.8)
    return g
SPEC.update({10: ("pines", C(X(tag_gurney, 0, G))), 2: ("meadow", C(X(skeleton_l, -34, G), X(meat_pile, 34, G)))})
def tag_feet(r, x, y):                       # foot end of a covered gurney: two bare feet up, a big toe tag hanging
    g = jl([(x - 34, y), (x - 30, y - 24)], r, 2.2) + jl([(x + 34, y), (x + 30, y - 24)], r, 2.2) + jl([(x - 44, y - 24), (x + 44, y - 24)], r, 2.8)
    g += shape(r, [(x - 44, y - 26), (x - 40, y - 40), (x - 24, y - 46), (x + 24, y - 46), (x + 40, y - 40), (x + 44, y - 26)], 2)
    g += jl([(x - 30, y - 34), (x - 14, y - 40)], r, 1) + jl([(x + 14, y - 40), (x + 30, y - 34)], r, 1)
    for d in (-1, 1):
        fx = x + d * 13
        g += f'<path d="M{fx-8:.1f} {y-40:.1f} C{fx-11:.1f} {y-58:.1f} {fx-9:.1f} {y-70:.1f} {fx:.1f} {y-71:.1f} C{fx+9:.1f} {y-70:.1f} {fx+11:.1f} {y-58:.1f} {fx+8:.1f} {y-40:.1f}" fill="{B()}" stroke="{I()}" stroke-width="2.4"/>'
        for i, u in enumerate((-6, -2.5, 1, 4.5, 7.5)):
            g += ell(fx + d * u, y - 73 + abs(u) * 0.5 + (0 if i else -1), 2.6 if i == 0 else 1.9, 2.6 if i == 0 else 1.9, 1.3)
    g += jl([(x + 7, y - 74), (x + 26, y - 66), (x + 36, y - 56)], r, 1.2, 0.3)
    g += shape(r, [(x + 30, y - 56), (x + 52, y - 60), (x + 56, y - 38), (x + 34, y - 34)], 2) + ell(x + 35, y - 52, 1.8, 1.8, 1.1)
    g += jl([(x + 39, y - 47), (x + 51, y - 49)], r, 1) + jl([(x + 39, y - 41), (x + 52, y - 43)], r, 1)
    return g
SPEC.update({10: ("pines", C(X(tag_feet, -6, G)))})
def tagged_self(r, x, y):                    # standing figure looking down at the toe tag on its own foot
    g = head(x + 3, y - 50) + pl([(x, y - 42), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 9, y - 1)], 2.6)
    g += pl([(x, y - 36), (x - 10, y - 24)], 2.2) + pl([(x, y - 36), (x + 8, y - 26), (x + 12, y - 30)], 2.2)
    g += jl([(x + 11, y - 1), (x + 18, y + 2), (x + 22, y - 6)], r, 1.1, 0.2)
    g += shape(r, [(x + 18, y - 6), (x + 36, y - 12), (x + 40, y + 2), (x + 22, y + 6)], 1.8) + ell(x + 22, y - 2, 1.4, 1.4, 1)
    return g + jl([(x + 26, y - 4), (x + 36, y - 7)], r, 0.9) + jl([(x + 26, y + 1), (x + 37, y - 2)], r, 0.9)
def shared_bar(r, x, y):                     # two lifters under one bar, each with a hand on the other's back
    g = jl([(x - 70, y - 46), (x + 70, y - 46)], r, 3)
    for d in (-1, 1):
        g += shape(r, rect_pts(x + d * 66 - 4, y - 62, 8, 32), 2) + shape(r, rect_pts(x + d * 56 - 3, y - 56, 6, 20), 1.8)
    for u in (-20, 20):
        g += head(x + u, y - 54) + pl([(x + u, y - 46), (x + u, y - 18)], 2.6) + pl([(x + u - 8, y), (x + u, y - 18), (x + u + 8, y)], 2.6)
        g += pl([(x + u, y - 42), (x + u + (-10 if u < 0 else 10), y - 46)], 2.2)
    return g + pl([(x - 20, y - 38), (x, y - 34), (x + 18, y - 34)], 2) + pl([(x + 20, y - 38), (x, y - 30), (x - 18, y - 32)], 2)
SPEC.update({33: ("meadow", C(X(tagged_self, -8, G))), 38: ("pines", C(X(shared_bar, 0, G)))})
def phone_call(r, x, y):                     # sitting on a chair, old phone to the ear, the phone base on a small table, cord between
    g = jl([(x - 30, y), (x - 30, y - 30), (x - 33, y - 58)], r, 2.2) + jl([(x - 30, y - 30), (x - 6, y - 30)], r, 2.4) + jl([(x - 8, y - 30), (x - 8, y)], r, 2.2)
    g += head(x - 22, y - 70) + pl([(x - 24, y - 62), (x - 22, y - 32)], 2.6) + pl([(x - 22, y - 32), (x + 2, y - 32), (x + 4, y)], 2.6)
    g += pl([(x - 23, y - 56), (x - 12, y - 64), (x - 15, y - 72)], 2.2) + shape(r, [(x - 17, y - 78), (x - 13, y - 78), (x - 13, y - 66), (x - 17, y - 66)], 1.6)
    g += pl([(x - 23, y - 54), (x - 8, y - 44)], 2.2)
    g += jl([(x + 24, y), (x + 24, y - 30)], r, 2.2) + jl([(x + 52, y), (x + 52, y - 30)], r, 2.2) + jl([(x + 18, y - 30), (x + 58, y - 30)], r, 2.6)
    g += shape(r, [(x + 26, y - 32), (x + 28, y - 44), (x + 48, y - 44), (x + 50, y - 32)], 2) + ell(x + 38, y - 38, 4, 3, 1.2)
    return g + jl([(x - 14, y - 64), (x - 4, y - 54), (x + 4, y - 62), (x + 14, y - 50), (x + 26, y - 40)], r, 1, 0.2, 3)
SPEC.update({31: ("cabin", C(X(phone_call, -10, G)))})
def wilted_rose(r, x, y):                    # tall rose bent over, head hanging, petals fallen on the ground, flies
    g = f'<path d="M{x} {y} C{x-2} {y-40} {x+4} {y-78} {x+26} {y-86} C{x+40} {y-90} {x+46} {y-78} {x+42} {y-66}" fill="none" stroke="{I()}" stroke-width="2.4"/>'
    g += f'<path d="M{x+33} {y-64} Q{x+30} {y-50} {x+38} {y-44} Q{x+42} {y-40} {x+46} {y-44} Q{x+54} {y-50} {x+51} {y-64} Q{x+46} {y-60} {x+42} {y-66} Q{x+38} {y-60} {x+33} {y-64} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>'
    g += f'<path d="M{x+42} {y-48} Q{x+36} {y-52} {x+40} {y-58} M{x+42} {y-48} Q{x+48} {y-52} {x+45} {y-58}" fill="none" stroke="{I()}" stroke-width="1.2"/>'
    g += f'<path d="M{x+34} {y-66} l-4 -4 M{x+50} {y-66} l4 -4" fill="none" stroke="{I()}" stroke-width="1.6"/>'
    g += shape(r, [(x + 2, y - 44), (x - 14, y - 52), (x - 22, y - 44), (x - 10, y - 40)], 1.6) + jl([(x - 2, y - 42), (x - 16, y - 46)], r, 1)
    g += ''.join(shape(r, [(x + u, y), (x + u + 4, y - 4), (x + u + 9, y - 2), (x + u + 7, y)], 1.4) for u in (30, 46, 58))
    return g + ''.join(ell(x + u, y + v, 1.4, 1.4, 1) + pl([(x + u - 2, y + v - 2), (x + u - 4, y + v - 4)], 0.8) for u, v in ((24, -96), (54, -84), (60, -100)))
def six_feet(r, x, y):                       # cut-away grave: a tape measure running down the side reads 6 FT; figure at the edge
    g = jl([(x - 30, y), (x - 30, y + 0.1)], r, 1)
    g += head(x - 70, y - 50) + pl([(x - 70, y - 42), (x - 70, y - 18)], 2.6) + pl([(x - 78, y), (x - 70, y - 18), (x - 62, y)], 2.6) + pl([(x - 70, y - 36), (x - 56, y - 28)], 2.2)
    g += shape(r, [(x - 40, y), (x - 36, y - 12), (x + 40, y - 12), (x + 44, y)], 2) + jl([(x - 28, y - 6), (x + 30, y - 6)], r, 1)    # dirt pile
    g += shape(r, [(x + 46, y - 4), (x + 50, y - 64), (x + 58, y - 64), (x + 54, y - 4)], 2)                         # tape measure strip
    g += ''.join(pl([(x + 50 + i * 0.07, y - 10 - i * 9), (x + 54 + i * 0.07, y - 10 - i * 9)], 1) for i in range(6))
    g += shape(r, rect_pts(x + 44, y - 76, 18, 14), 2.2) + hand("6 FT", 9, x + 72, y - 64)
    return g
def dirt_tug(r, x, y):                       # tug of war with a dirt mound: the rope runs into the ground
    g = shape(r, [(x + 10, y), (x + 20, y - 12), (x + 40, y - 18), (x + 62, y - 12), (x + 72, y)], 2.2)
    g += ''.join(jl([(x + u, y - 6), (x + u + 6, y - 8)], r, 1) for u in (24, 40, 54))
    hx = x - 46
    g += head(hx - 12, y - 46) + pl([(hx - 9, y - 38), (hx + 6, y - 18)], 2.6) + pl([(hx - 6, y), (hx + 6, y - 18), (hx + 16, y - 2)], 2.6)
    g += pl([(hx - 4, y - 32), (hx + 14, y - 28)], 2.2) + pl([(hx - 2, y - 30), (hx + 14, y - 24)], 2.2)
    return g + jl([(hx + 12, y - 27), (x + 10, y - 20), (x + 36, y - 14)], r, 1.8, 0.2)
def broken_heart_hold(r, x, y):              # figure holding out a heart with a crack through it
    g = head(x - 14, y - 50) + pl([(x - 14, y - 42), (x - 14, y - 18)], 2.6) + pl([(x - 22, y), (x - 14, y - 18), (x - 6, y)], 2.6)
    g += pl([(x - 14, y - 36), (x + 2, y - 30), (x + 10, y - 34)], 2.2) + pl([(x - 14, y - 34), (x + 2, y - 26), (x + 12, y - 28)], 2.2)
    hx, hy = x + 22, y - 44
    g += f'<path d="M{hx} {hy+14} C{hx-18} {hy+2} {hx-16} {hy-14} {hx-6} {hy-14} C{hx-2} {hy-14} {hx} {hy-10} {hx} {hy-8} C{hx} {hy-10} {hx+2} {hy-14} {hx+6} {hy-14} C{hx+16} {hy-14} {hx+18} {hy+2} {hx} {hy+14} Z" fill="{B()}" stroke="{I()}" stroke-width="2.4"/>'
    return g + pl([(hx, hy - 8), (hx - 3, hy - 2), (hx + 2, hy + 2), (hx - 2, hy + 7), (hx, hy + 14)], 1.6)
SPEC.update({41: ("meadow", C(X(wilted_rose, -14, G))), 43: ("valley", C(X(six_feet, 10, G))), 48: ("valley", C(X(dirt_tug, 0, G))), 47: ("meadow", C(X(broken_heart_hold, -4, G)))})
def six_feet(r, x, y):                       # figure at the edge of a grave shown in cut-away below the ground line, tape measure down the side: 6 FT
    g = head(x - 44, y - 50) + pl([(x - 44, y - 42), (x - 44, y - 18)], 2.6) + pl([(x - 52, y), (x - 44, y - 18), (x - 36, y)], 2.6)
    g += pl([(x - 44, y - 36), (x - 32, y - 26)], 2.2) + pl([(x - 44, y - 34), (x - 54, y - 24)], 2.2)
    g += shape(r, [(x + 34, y), (x + 40, y - 12), (x + 62, y - 14), (x + 74, y)], 2)                                  # dirt pile
    g += jl([(x - 24, y), (x - 24, y + 30), (x + 24, y + 30), (x + 24, y)], r, 2.2)                                    # the hole, cut away
    g += shape(r, [(x - 18, y + 28), (x - 20, y + 22), (x - 12, y + 18), (x + 16, y + 18), (x + 20, y + 22), (x + 18, y + 28)], 1.8)
    g += jl([(x + 30, y - 2), (x + 30, y + 30)], r, 1.6) + ''.join(pl([(x + 30, y + 3 + i * 5.4), (x + 34 - (i % 2) * 2, y + 3 + i * 5.4)], 1) for i in range(6))
    return g + jl([(x + 26, y + 30), (x + 34, y + 30)], r, 1.6) + hand("6 FT", 9, x + 48, y + 20)
SPEC.update({43: ("valley", C(X(six_feet, 0, G)))})
V.OVERRIDE.setdefault(41, {})
def chalk_and_dirt(r, x, y):                 # figure with chalk dust puffing off the hands; barbell on one side, shovel in a dirt pile on the other
    g = head(x, y - 52) + pl([(x, y - 44), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6)
    g += pl([(x, y - 38), (x - 12, y - 26)], 2.2) + pl([(x, y - 38), (x + 12, y - 26)], 2.2)
    g += ''.join(ell(x + d * 14 + u, y - 24 + v, 1.6, 1.6, 0.9, False) for d in (-1, 1) for u, v in ((-3, -3), (2, -5), (4, 1), (-1, 3)))
    g += shape(r, [(x - 6, y - 2), (x - 9, y + 1), (x - 2, y + 1)], 1.4) + shape(r, [(x + 6, y - 2), (x + 10, y + 1), (x + 3, y + 1)], 1.4)
    g += jl([(x - 82, y - 10), (x - 30, y - 10)], r, 2.6) + ''.join(shape(r, rect_pts(x + u - 3, y - 22, 6, 22), 1.8) for u in (-76, -36))
    g += shape(r, [(x + 30, y), (x + 38, y - 12), (x + 58, y - 16), (x + 74, y - 8), (x + 80, y)], 2)
    return g + jl([(x + 56, y - 14), (x + 62, y - 50)], r, 2.4, 0.2) + jl([(x + 56, y - 54), (x + 68, y - 50)], r, 2.6) + shape(r, [(x + 52, y - 14), (x + 60, y - 14), (x + 58, y - 4), (x + 52, y - 4)], 1.6)
def worms_wait(r, x, y):                     # figure on the ground; below, in cut-away soil, three worms look up at it
    g = head(x, y - 50) + pl([(x, y - 42), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6)
    g += pl([(x, y - 36), (x - 10, y - 24)], 2.2) + pl([(x, y - 36), (x + 10, y - 24)], 2.2)
    for u, v, d in ((-40, 16, 1), (-6, 20, -1), (32, 15, 1)):
        g += f'<path d="M{x+u-d*16} {y+v+2} q{d*4} -6 {d*8} 0 t{d*8} 0 q{d*3} -2 {d*4} -8" fill="none" stroke="{I()}" stroke-width="2.6" stroke-linecap="round"/>'
        g += nt.dot(x + u + d * 4, y + v - 7, 1.1) + nt.dot(x + u + d * 1, y + v - 7, 1.1)
    return g + ''.join(ell(x + u, y + v, 1.2, 1.2, 0.9, False) for u, v in ((-60, 10), (-24, 12), (14, 9), (50, 18), (-50, 20), (20, 22)))
SPEC.update({52: ("valley", C(X(chalk_and_dirt, 0, G))), 53: ("meadow", C(X(worms_wait, 0, G)))})
def under_rows(r, x, y):                     # two headstones above; cut-away below shows a coffin under each; a figure stands between
    g = nt.headstone(x - 44, y, 22, 32) + nt.headstone(x + 44, y, 22, 32) + hand("RIP", 8, x - 44, y - 14) + hand("RIP", 8, x + 44, y - 14)
    g += head(x, y - 50) + pl([(x, y - 42), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6) + pl([(x - 10, y - 26), (x, y - 36), (x + 10, y - 26)], 2.2)
    g += nt.coffin_side(x - 44, y + 22, 48, 12) + nt.coffin_side(x + 44, y + 22, 48, 12) + nt.coffin_side(x, y + 22, 34, 10)
    return g + ''.join(ell(x + u, y + v, 1.2, 1.2, 0.9, False) for u, v in ((-74, 8), (-14, 6), (20, 9), (72, 12)))
def grief_scale(r, x, y):                    # figure on a platform scale, the needle pinned past the top
    g = shape(r, rect_pts(x - 26, y - 8, 52, 8), 2.2) + shape(r, rect_pts(x + 10, y - 40, 4, 32), 1.6)
    g += ell(x + 12, y - 52, 13, 13) + pl([(x + 12, y - 52), (x + 22, y - 62)], 1.8) + ''.join(pl([(x + 12 + 10 * c, y - 52 - 10 * s2), (x + 12 + 12 * c, y - 52 - 12 * s2)], 1) for c, s2 in ((-0.7, 0.7), (0, 1), (0.7, 0.7), (1, 0)))
    g += head(x - 10, y - 58) + pl([(x - 10, y - 50), (x - 10, y - 26)], 2.6) + pl([(x - 17, y - 8), (x - 10, y - 26), (x - 3, y - 8)], 2.6)
    return g + pl([(x - 10, y - 44), (x - 16, y - 32)], 2.2) + pl([(x - 10, y - 44), (x - 4, y - 32)], 2.2)
def bench_talk(r, x, y):                     # two people sitting on a gym bench talking; barbell resting on the floor in front
    g = jl([(x - 40, y - 18), (x + 40, y - 18)], r, 3) + jl([(x - 34, y - 18), (x - 34, y)], r, 2) + jl([(x + 34, y - 18), (x + 34, y)], r, 2)
    for u, d in ((-18, 1), (18, -1)):
        g += head(x + u, y - 56) + pl([(x + u, y - 48), (x + u, y - 22)], 2.6) + pl([(x + u, y - 22), (x + u + d * 14, y - 22), (x + u + d * 16, y)], 2.4)
        g += pl([(x + u, y - 42), (x + u + d * 10, y - 30)], 2.2)
    g += jl([(x - 8, y - 76), (x - 2, y - 82), (x + 6, y - 78)], r, 1.1) + ''.join(nt.dot(x + u, y - 70, 1.2) for u in (-4, 0, 4))
    return g + jl([(x - 56, y - 8), (x + 56, y - 8)], r, 2.4) + ''.join(shape(r, rect_pts(x + u - 3, y - 18, 6, 18), 1.6) for u in (-52, 52))
def bag_fit(r, x, y):                        # an empty body bag laid on the ground; the figure beside it, holding out an arm span to compare
    g = shape(r, [(x - 6, y), (x - 10, y - 8), (x - 2, y - 14), (x + 82, y - 14), (x + 90, y - 8), (x + 86, y)], 2.2)
    g += jl([(x + 4, y - 7), (x + 78, y - 7)], r, 1.2) + ''.join(pl([(x + u, y - 9), (x + u, y - 5)], 0.8) for u in range(8, 78, 5)) + shape(r, rect_pts(x + 76, y - 10, 6, 6), 1.2)
    hx = x - 30
    g += head(hx, y - 52) + pl([(hx, y - 44), (hx, y - 18)], 2.6) + pl([(hx - 8, y), (hx, y - 18), (hx + 8, y)], 2.6)
    return g + pl([(hx - 16, y - 38), (hx, y - 38), (hx + 16, y - 38)], 2.2)
SPEC.update({59: ("cemetery", C(X(under_rows, 0, G))), 60: ("valley", C(X(grief_scale, 0, G))), 61: ("pines", C(X(bench_talk, 0, G))), 64: ("pines", C(X(bag_fit, -16, G)))})
def bearers_walk(r, x, y):                   # three bearers seen from the side (six in all), coffin on the shoulders, heads clear above it
    g = ''
    for u in (-44, 0, 44):
        g += head(x + u, y - 52) + pl([(x + u, y - 44), (x + u, y - 36)], 2.6) + pl([(x + u - 9, y), (x + u, y - 20), (x + u + 9, y - 2)], 2.6)
        g += pl([(x + u, y - 26), (x + u, y - 20)], 2.6)
    return g + nt.coffin_side(x, y - 26, 134, 13)
SPEC.update({65: ("cemetery", C(X(bearers_walk, 0, G)))})
def scatter_ash(r, x, y):                    # figure at the shore tipping an urn; ash drifts out over the water
    g = head(x, y - 50) + pl([(x, y - 42), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6)
    g += pl([(x, y - 36), (x + 12, y - 34), (x + 16, y - 40)], 2.2) + pl([(x, y - 34), (x + 10, y - 30), (x + 18, y - 34)], 2.2)
    g += f'<path d="M{x+14} {y-40} l12 -8 l6 6 l-4 4 l-12 6 Z" fill="{B()}" stroke="{I()}" stroke-width="2"/>'
    return g + ''.join(ell(x + 34 + i * 6 + r.uniform(-2, 2), y - 50 - i * 1.2 + r.uniform(-4, 4), 0.9, 0.9, 0.8) for i in range(14))
SPEC.update({194: ("valley", C(X(scatter_ash, -30, G)))})
def balloon_away(r, x, y):                   # figure with an arm up; the balloon has already drifted off, string trailing
    g = head(x, y - 50) + pl([(x, y - 42), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6)
    g += pl([(x, y - 38), (x + 8, y - 50), (x + 12, y - 64)], 2.2) + pl([(x, y - 36), (x - 10, y - 24)], 2.2)
    bx, by = x + 46, y - 96
    g += f'<path d="M{bx} {by+13} C{bx-12} {by+6} {bx-11} {by-12} {bx} {by-12} C{bx+11} {by-12} {bx+12} {by+6} {bx} {by+13} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>'
    g += pl([(bx - 2, by + 13), (bx, by + 16), (bx + 2, by + 13)], 1.4) + pl([(bx - 4, by - 6), (bx - 6, by - 2)], 1.2)
    return g + jl([(bx, by + 16), (bx - 4, by + 26), (bx + 2, by + 36), (bx - 6, by + 44)], r, 1.1, 0.3, 4)
def rigor_plank(r, x, y):                    # plank hold, body dead straight and stiff; stopwatch beside
    g = head(x - 44, y - 26) + pl([(x - 36, y - 22), (x + 40, y - 4)], 2.8) + pl([(x + 40, y - 4), (x + 46, y)], 2.4)
    g += pl([(x - 30, y - 20), (x - 30, y)], 2.4) + pl([(x - 30, y), (x - 18, y)], 2.4)
    g += ell(x + 30, y - 40, 11, 11) + pl([(x + 30, y - 40), (x + 30, y - 47)], 1.6) + pl([(x + 30, y - 40), (x + 35, y - 37)], 1.4) + shape(r, rect_pts(x + 27, y - 56, 6, 4), 1.4)
    return g + ''.join(jl([(x + u, y - 34 + u * 0.24), (x + u, y - 28 + u * 0.24)], r, 1) for u in (-20, -6, 8))
SPEC.update({76: ("meadow", C(X(balloon_away, -30, G))), 80: ("pines", C(X(rigor_plank, 0, G)))})
def rot_apple(r, x, y):                      # big apple gone soft: bruise spots, a worm out of the side, flies over it
    g = f'<path d="M{x} {y-50} C{x-10} {y-58} {x-36} {y-54} {x-36} {y-28} C{x-36} {y-8} {x-20} {y} {x-8} {y-2} C{x-4} {y-1} {x+4} {y-1} {x+8} {y-2} C{x+20} {y} {x+36} {y-8} {x+36} {y-28} C{x+36} {y-54} {x+10} {y-58} {x} {y-50} Z" fill="{B()}" stroke="{I()}" stroke-width="2.6"/>'
    g += jl([(x, y - 50), (x + 2, y - 62)], r, 2.2, 0.2) + shape(r, [(x + 2, y - 58), (x + 12, y - 66), (x + 18, y - 60), (x + 8, y - 56)], 1.6)
    g += ell(x - 14, y - 26, 6, 5, 1.4, False) + ell(x + 12, y - 16, 4, 3.5, 1.4, False) + ell(x + 18, y - 36, 3, 2.6, 1.2, False)
    g += f'<path d="M{x+34} {y-24} q8 -4 10 -12 q2 -6 8 -4" fill="none" stroke="{I()}" stroke-width="2.6" stroke-linecap="round"/>' + nt.dot(x + 50, y - 41, 1)
    return g + ''.join(ell(x + u, y + v, 1.3, 1.3, 1) + pl([(x + u - 2, y + v - 2), (x + u - 4, y + v - 5)], 0.8) for u, v in ((-20, -70), (10, -80), (28, -70)))
def all_seasons(r, x, y):                    # figure kneeling at a headstone; snow on one side, falling leaves on the other
    g = nt.headstone(x + 22, y, 28, 40) + hand("RIP", 10, x + 22, y - 20)
    g += head(x - 22, y - 38) + pl([(x - 22, y - 30), (x - 18, y - 14)], 2.6) + pl([(x - 18, y - 14), (x - 6, y - 14), (x - 4, y)], 2.4) + pl([(x - 18, y - 14), (x - 28, y)], 2.4)
    g += pl([(x - 20, y - 26), (x + 4, y - 22)], 2.2)
    for u, v in ((-60, -80), (-40, -64), (-70, -50), (-30, -90), (-52, -34), (-14, -76)):
        g += pl([(x + u - 3, y + v), (x + u + 3, y + v)], 1) + pl([(x + u, y + v - 3), (x + u, y + v + 3)], 1) + pl([(x + u - 2, y + v - 2), (x + u + 2, y + v + 2)], 0.8)
    for u, v in ((52, -78), (66, -56), (44, -50), (60, -30)):
        g += f'<path d="M{x+u} {y+v} q5 -5 10 0 q-5 5 -10 0 Z" fill="none" stroke="{I()}" stroke-width="1.2"/>'
    return g
SPEC.update({41: ("meadow", C(X(rot_apple, 0, G))), 89: ("meadow", C(X(wilted_rose, -14, G))), 96: ("cemetery", C(X(all_seasons, 0, G)))})
def hurts_here(r, x, y):                     # figure with a hand on the chest; a hand-drawn arrow points at the heart
    g = head(x, y - 52) + pl([(x, y - 44), (x, y - 18)], 2.6) + pl([(x - 8, y), (x, y - 18), (x + 8, y)], 2.6)
    g += pl([(x, y - 38), (x + 8, y - 32), (x + 2, y - 34)], 2.2) + pl([(x, y - 38), (x - 10, y - 26)], 2.2)
    g += f'<path d="M{x+3} {y-33} c-3 -4 -8 -1 -4 3 l4 4 l4 -4 c4 -4 -1 -7 -4 -3 Z" fill="{I()}"/>'
    g += jl([(x + 50, y - 72), (x + 38, y - 56), (x + 16, y - 38)], r, 1.4, 0.3) + pl([(x + 16, y - 38), (x + 24, y - 40)], 1.4) + pl([(x + 16, y - 38), (x + 18, y - 46)], 1.4)
    return g + hand("here", 11, x + 54, y - 76)
SPEC.update({100: ("pines", C(X(hurts_here, -10, G)))})
def open_arms_skel(r, x, y):                 # skeleton standing with its arms held wide open: nothing left to hide
    g = skull_l(r, x, y - 50, 0.4) + pl([(x, y - 40), (x, y - 14)], 2.2)
    g += ''.join(pl([(x - 8, y + v), (x, y + v - 2), (x + 8, y + v)], 1.4) for v in (-34, -29, -24))
    g += pl([(x - 9, y - 14), (x, y - 10), (x + 9, y - 14)], 1.6)
    g += pl([(x - 6, y - 12), (x - 8, y)], 2) + pl([(x + 6, y - 12), (x + 8, y)], 2) + pl([(x - 8, y), (x - 14, y)], 2) + pl([(x + 8, y), (x + 14, y)], 2)
    g += pl([(x, y - 37), (x - 20, y - 46), (x - 32, y - 58)], 2) + pl([(x, y - 37), (x + 20, y - 46), (x + 32, y - 58)], 2)
    return g + ''.join(pl([(x + d * 32, y - 58), (x + d * (32 + u), y - 64 - abs(u))], 1.2) for d in (-1, 1) for u in (-2, 1, 4))
SPEC.update({112: ("meadow", C(X(open_arms_skel, 0, G)))})
def class_skeleton(r, x, y):                 # teaching skeleton hung from a rolling stand by the skull hook (stand, not a gallows: short post, wheeled base)
    g = jl([(x - 24, y - 4), (x + 24, y - 4)], r, 2.4) + ell(x - 22, y - 2, 3, 3, 1.4) + ell(x + 22, y - 2, 3, 3, 1.4) + jl([(x, y - 4), (x, y - 30)], r, 2.4)
    g += skeleton_l(r, x, y - 26)
    g += pl([(x + 34, y - 20), (x + 56, y - 64)], 1.6) + shape(r, [(x + 44, y - 4), (x + 48, y - 38), (x + 74, y - 38), (x + 76, y - 4)], 1.8)
    return g + jl([(x + 50, y - 30), (x + 70, y - 30)], r, 1) + jl([(x + 50, y - 22), (x + 66, y - 22)], r, 1) + hand("DONATED", 7, x + 60, y - 9)
SPEC.update({120: ("valley", C(X(hearse_l, 0, G))), 115: ("cabin", C(X(class_skeleton, -16, G)))})
def class_skeleton(r, x, y):                 # classroom skeleton on a low wheeled base beside a chalkboard: "206 BONES"
    g = jl([(x - 20, y - 5), (x + 20, y - 5)], r, 2.4) + ell(x - 16, y - 2, 3, 3, 1.4) + ell(x + 16, y - 2, 3, 3, 1.4)
    g += skeleton_l(r, x, y - 6)
    g += shape(r, rect_pts(x + 34, y - 56, 52, 34), 2) + jl([(x + 40, y - 22), (x + 36, y)], r, 2) + jl([(x + 80, y - 22), (x + 84, y)], r, 2)
    return g + hand("206", 12, x + 60, y - 40) + hand("BONES", 9, x + 60, y - 28)
SPEC.update({115: ("cabin", C(X(class_skeleton, -24, G)))})
def glove_off(r, x, y):                      # skeleton pulling a lifting glove off its bony hand, the other glove already on the ground
    g = skeleton_l(r, x, y)
    g += shape(r, [(x + 12, y - 40), (x + 28, y - 46), (x + 34, y - 38), (x + 30, y - 30), (x + 16, y - 30)], 2)
    g += ''.join(pl([(x + 30 + u * 0.4, y - 44 + u), (x + 38 + u * 0.4, y - 48 + u)], 1.6) for u in (0, 4, 8))
    g += pl([(x + 7, y - 33), (x + 14, y - 36)], 1.6)
    return g + shape(r, [(x - 40, y), (x - 38, y - 10), (x - 24, y - 12), (x - 20, y - 4), (x - 24, y)], 2) + ''.join(pl([(x - 22 + u, y - 10), (x - 16 + u, y - 14)], 1.4) for u in (0, 3))
SPEC.update({124: ("pines", C(X(glove_off, 0, G)))})
def chalk_outline(r, x, y):                  # dashed chalk outline of a body lying on the ground (arms out, one knee bent), no body
    d = (f"M{x-62} {y-12} m-9 0 a9 9 0 1 0 18 0 a9 9 0 1 0 -18 0 "
         f"M{x-52} {y-16} L{x-36} {y-26} L{x-30} {y-34} L{x-26} {y-30} L{x-30} {y-20} L{x-14} {y-16} L{x+20} {y-16} L{x+34} {y-28} L{x+42} {y-26} L{x+32} {y-12} "
         f"L{x+60} {y-12} L{x+64} {y-6} L{x+32} {y-4} L{x+16} {y-2} L{x-16} {y-2} L{x-26} {y+4} L{x-34} {y+2} L{x-30} {y-6} L{x-52} {y-8}")
    return f'<path d="{d}" fill="none" stroke="{I()}" stroke-width="2.2" stroke-dasharray="5 3.5" stroke-linecap="round"/>'
def oak_roots(r, x, y):                      # broad oak; in the cut-away below, its roots wrap a skull
    g = f'<path d="M{x-8} {y} C{x-6} {y-30} {x-10} {y-50} {x-26} {y-64} M{x+8} {y} C{x+6} {y-30} {x+12} {y-52} {x+28} {y-66} M{x-2} {y-40} C{x} {y-56} {x} {y-66} {x+2} {y-74}" fill="none" stroke="{I()}" stroke-width="2.6"/>'
    pts = [(x - 60, y - 66), (x - 50, y - 96), (x - 20, y - 112), (x + 14, y - 114), (x + 48, y - 100), (x + 62, y - 72), (x + 40, y - 56), (x + 10, y - 60), (x - 16, y - 54), (x - 44, y - 54)]
    d = f"M{pts[0][0]} {pts[0][1]}"
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; cx, cy = mx + (mx - x) * 0.18, my + (my - (y - 84)) * 0.3
        d += f" Q{cx:.1f} {cy:.1f} {b[0]} {b[1]}"
    g += f'<path d="{d} Z" fill="none" stroke="{I()}" stroke-width="2.2"/>'
    g += skull_l(r, x + 4, y + 24, 0.42)
    return g + ''.join(jl(p, r, 1.4, 0.3, 4) for p in ([(x - 6, y), (x - 14, y + 12), (x - 6, y + 28), (x + 4, y + 34)], [(x + 6, y), (x + 20, y + 10), (x + 16, y + 26), (x + 8, y + 32)], [(x - 4, y), (x - 34, y + 10), (x - 50, y + 8)], [(x + 6, y), (x + 40, y + 8), (x + 56, y + 16)]))
def four_stages(r, x, y):                    # four roses in a row: fresh, heavy, bowed, dry stalk
    g = ''
    for i, u in enumerate((-66, -22, 22, 66)):
        bend = i * 12
        tipx, tipy = x + u + bend * 0.8, y - 56 + bend * 0.6
        g += f'<path d="M{x+u} {y} C{x+u} {y-30} {x+u+bend*0.2} {y-48} {tipx:.1f} {tipy:.1f}" fill="none" stroke="{I()}" stroke-width="2.2"/>'
        if i < 3:
            rr = 9 - i * 1.5
            g += ell(tipx, tipy - (rr - 2) * (1 if i == 0 else 0.3), rr, rr * 0.9, 2) + pl([(tipx - rr * 0.5, tipy - rr * 0.6), (tipx, tipy - rr * 0.1), (tipx + rr * 0.5, tipy - rr * 0.6)], 1.2)
        g += shape(r, [(x + u, y - 20), (x + u - 10, y - 26), (x + u - 14, y - 20 + i * 2), (x + u - 4, y - 18)], 1.4) if i < 3 else jl([(x + u, y - 18), (x + u - 8, y - 14)], r, 1.2)
    return g + ''.join(shape(r, [(x + u, y), (x + u + 3, y - 3), (x + u + 7, y - 1)], 1.2) for u in (30, 40, 74, 82, 90))
SPEC.update({131: ("meadow", C(X(chalk_outline, 0, G))), 133: ("meadow", C(X(oak_roots, 0, G))), 135: ("meadow", C(X(four_stages, 0, G)))})
def empty_chair(r, x, y):                    # a chair with a dashed seated outline where someone used to sit
    g = jl([(x - 20, y), (x - 20, y - 30), (x - 22, y - 72)], r, 2.4) + jl([(x - 20, y - 30), (x + 18, y - 30)], r, 2.6) + jl([(x + 16, y - 30), (x + 16, y)], r, 2.4)
    g += jl([(x - 21, y - 52), (x - 4, y - 52)], r, 1.4) + jl([(x - 22, y - 66), (x - 4, y - 66)], r, 1.4)
    dash = 'fill="none" stroke="%s" stroke-width="2" stroke-dasharray="4 3" stroke-linecap="round"' % I()
    g += f'<circle cx="{x-8}" cy="{y-66}" r="8" {dash}/>' + f'<path d="M{x-10} {y-58} L{x-10} {y-34} L{x+14} {y-34} L{x+16} {y} M{x-10} {y-50} L{x+6} {y-42} L{x+10} {y-46}" {dash}/>'
    return g + jl([(x + 36, y), (x + 36, y - 26)], r, 2) + jl([(x + 30, y - 26), (x + 50, y - 26)], r, 2.2) + ell(x + 44, y - 30, 4, 3, 1.4)
def oak_roots(r, x, y):                      # wide, low oak (lobed crown wider than tall, thick flared trunk); below, roots wrap a skull
    g = f'<path d="M{x-14} {y} Q{x-8} {y-6} {x-8} {y-20} L{x-8} {y-40} Q{x-20} {y-50} {x-44} {y-56} M{x+14} {y} Q{x+8} {y-6} {x+8} {y-20} L{x+8} {y-38} Q{x+24} {y-48} {x+50} {y-54} M{x-2} {y-40} L{x+4} {y-62}" fill="none" stroke="{I()}" stroke-width="2.6"/>'
    lobes = [(-76, -60), (-70, -80), (-50, -92), (-24, -96), (0, -92), (24, -98), (50, -92), (72, -80), (78, -62), (56, -52), (30, -58), (0, -54), (-30, -58), (-56, -52)]
    d = f"M{x+lobes[0][0]} {y+lobes[0][1]}"
    for i in range(len(lobes)):
        a, b = lobes[i], lobes[(i + 1) % len(lobes)]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; nx, ny = mx * 0.12, (my + 74) * 0.5
        d += f" Q{x+mx+nx:.1f} {y+my+ny:.1f} {x+b[0]} {y+b[1]}"
    g += f'<path d="{d} Z" fill="none" stroke="{I()}" stroke-width="2.2"/>'
    g += ''.join(jl([(x + u, y - 72 + v), (x + u + 8, y - 74 + v)], r, 1) for u, v in ((-50, -4), (-20, -10), (20, -8), (46, 0)))
    g += skull_l(r, x + 2, y + 26, 0.55)
    return g + ''.join(jl(p, r, 1.6, 0.3, 4) for p in ([(x - 8, y), (x - 20, y + 12), (x - 14, y + 30), (x - 2, y + 36)], [(x + 8, y), (x + 22, y + 12), (x + 18, y + 30), (x + 6, y + 36)], [(x - 12, y), (x - 40, y + 8), (x - 60, y + 6)], [(x + 12, y), (x + 42, y + 8), (x + 62, y + 14)]))
def apple_stages(r, x, y):                   # four apples left to right: fresh, swollen, rotting with flies, dried core
    def apple(cx, s, spots=False):
        g = f'<path d="M{cx} {y-34*s} C{cx-8*s} {y-40*s} {cx-24*s} {y-36*s} {cx-24*s} {y-18*s} C{cx-24*s} {y-4*s} {cx-12*s} {y} {cx} {y-2*s} C{cx+12*s} {y} {cx+24*s} {y-4*s} {cx+24*s} {y-18*s} C{cx+24*s} {y-36*s} {cx+8*s} {y-40*s} {cx} {y-34*s} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>'
        g += pl([(cx, y - 34 * s), (cx + 2, y - 42 * s)], 1.8)
        if spots: g += ell(cx - 8, y - 18 * s, 4, 3.5, 1.2, False) + ell(cx + 8, y - 10 * s, 3, 2.6, 1.2, False) + ''.join(ell(cx + u, y - v, 1.2, 1.2, 0.9) for u, v in ((-10, 48), (6, 56), (16, 44)))
        return g
    g = apple(x - 72, 0.9) + apple(x - 22, 1.15) + apple(x + 30, 1.0, True)
    cx = x + 78
    g += f'<path d="M{cx-8} {y-30} Q{cx-2} {y-16} {cx-8} {y-2} L{cx+8} {y-2} Q{cx+2} {y-16} {cx+8} {y-30} Z" fill="{B()}" stroke="{I()}" stroke-width="2.2"/>' + pl([(cx, y - 30), (cx + 2, y - 38)], 1.8)
    return g
SPEC.update({131: ("cabin", C(X(empty_chair, 0, G))), 133: ("meadow", C(X(oak_roots, 0, G))), 135: ("meadow", C(X(apple_stages, 0, G)))})
def bare_oak(r, x, y):                       # bare winter oak (forked branches, no crown blob); below in cut-away, roots wrap a skull
    import math as _m
    import random as _r; rr = _r.Random(133)
    def br(x0, y0, ang, L, w, depth):
        x1, y1 = x0 + L * _m.cos(ang), y0 - L * _m.sin(ang)
        s = f'<path d="M{x0:.1f} {y0:.1f} Q{(x0+x1)/2 + rr.uniform(-3,3):.1f} {(y0+y1)/2:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{I()}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
        if depth:
            for da in (-0.5, 0.45) if depth > 1 else (-0.55, 0.05, 0.55):
                s += br(x1, y1, ang + da + rr.uniform(-0.12, 0.12), L * rr.uniform(0.62, 0.76), max(0.8, w * 0.62), depth - 1)
        return s
    g = br(x, y, _m.pi / 2, 34, 5.5, 4)
    g += skull_l(r, x + 2, y + 26, 0.55)
    return g + ''.join(jl(p, r, 1.6, 0.3, 4) for p in ([(x - 4, y), (x - 20, y + 12), (x - 14, y + 30), (x - 2, y + 36)], [(x + 4, y), (x + 22, y + 12), (x + 18, y + 30), (x + 6, y + 36)], [(x - 6, y), (x - 40, y + 8), (x - 60, y + 6)], [(x + 6, y), (x + 42, y + 8), (x + 62, y + 14)]))
SPEC.update({133: ("meadow", C(X(bare_oak, 0, G)))})
def crows_wait(r, x, y):                     # bare tree, three crows on the branches, a picked skull and a bone at its foot
    import math as _m, random as _r
    rr = _r.Random(137)
    def br(x0, y0, ang, L, w, depth):
        x1, y1 = x0 + L * _m.cos(ang), y0 - L * _m.sin(ang)
        s = f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" fill="none" stroke="{I()}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
        if depth:
            for da in (-0.55, 0.5):
                s += br(x1, y1, ang + da + rr.uniform(-0.1, 0.1), L * 0.68, max(0.9, w * 0.6), depth - 1)
        return s
    g = br(x - 20, y, _m.pi / 2, 36, 5, 3)
    def crow(cx, cy, d=1):
        return (f'<path d="M{cx-7*d} {cy} Q{cx-2*d} {cy-8} {cx+4*d} {cy-6} L{cx+8*d} {cy-9} L{cx+6*d} {cy-4} Q{cx+4*d} {cy+2} {cx-2*d} {cy+2} L{cx-10*d} {cy+5} Z" fill="{I()}"/>'
                + pl([(cx, cy + 2), (cx, cy + 5)], 1))
    g += crow(x - 46, y - 62) + crow(x + 6, y - 74, -1) + crow(x - 22, y - 92)
    g += skull_l(r, x + 30, y - 8, 0.45) + jl([(x + 46, y - 3), (x + 64, y - 6)], r, 2.6, 0.2) + ell(x + 66, y - 7, 2.4, 2.4, 1.2)
    return g
SPEC.update({137: ("meadow", C(X(crows_wait, 0, G)))})
def molar_roots(r, x, y):                    # a molar planted in the ground like a stump; short roots in the cut-away soil
    g = shape(r, [(x - 26, y), (x - 30, y - 30), (x - 18, y - 42), (x, y - 34), (x + 18, y - 42), (x + 30, y - 30), (x + 26, y)])
    g += jl([(x - 16, y), (x - 20, y + 10), (x - 26, y + 18)], r, 2.2) + jl([(x + 16, y), (x + 20, y + 10), (x + 26, y + 18)], r, 2.2) + jl([(x, y), (x + 2, y + 14)], r, 2)
    return g + jl([(x - 2, y - 34), (x + 4, y - 20), (x - 4, y - 8)], r, 1.6) + ''.join(ell(x + u, y - 46 - v, 1.2, 1.2, 0.9, False) for u, v in ((-24, 4), (18, 8), (30, 0)))
def sutured_heart(r, x, y):                  # big heart resting on a stone, a stitched seam down the middle
    g = shape(r, [(x - 40, y), (x - 34, y - 12), (x + 34, y - 12), (x + 40, y)], 2.2)
    hx, hy, s = x, y - 46, 2.2
    g += f'<path d="M{hx} {hy+16*s} C{hx-18*s} {hy+2*s} {hx-16*s} {hy-14*s} {hx-6*s} {hy-14*s} C{hx-2*s} {hy-14*s} {hx} {hy-10*s} {hx} {hy-8*s} C{hx} {hy-10*s} {hx+2*s} {hy-14*s} {hx+6*s} {hy-14*s} C{hx+16*s} {hy-14*s} {hx+18*s} {hy+2*s} {hx} {hy+16*s} Z" fill="{B()}" stroke="{I()}" stroke-width="2.6"/>'
    g += pl([(hx - 2, hy - 16), (hx + 3, hy - 4), (hx - 2, hy + 8), (hx + 2, hy + 22), (hx, hy + 34)], 1.6)
    return g + ''.join(pl([(hx - 5, hy + v - 2), (hx + 5, hy + v + 2)], 1.4) + pl([(hx - 5, hy + v + 2), (hx + 5, hy + v - 2)], 1.4) for v in (-10, 0, 10, 20))
SPEC.update({152: ("meadow", C(X(molar_roots, 0, G))), 148: ("meadow", C(X(sutured_heart, 0, G)))})
SPEC.update({158: ("cemetery", C(X(six_feet, 0, G)))})
def bell_grave(r, x, y):                     # a hand bell resting on a fresh grave mound; its cord runs down into the soil
    g = grave_mound(r, x, y, 76)
    by = y - 12
    g += (f'<path d="M{x-20} {by} Q{x-14} {by-4} {x-13} {by-18} Q{x-12} {by-36} {x} {by-38} Q{x+12} {by-36} {x+13} {by-18} Q{x+14} {by-4} {x+20} {by} Z" '
          f'fill="{B()}" stroke="{I()}" stroke-width="2.4"/>')
    g += jl([(x, by - 38), (x, by - 50)], r, 3, 0.2) + ell(x, by - 52, 4, 3, 2) + ell(x + 2, by + 3, 3, 3, 1.6)
    g += jl([(x - 16, by - 6), (x + 16, by - 6)], r, 1.1)
    return g + jl([(x + 4, by + 4), (x + 16, y + 6), (x + 30, y + 16)], r, 1.1, 0.3, 4)
def unclaimed(r, x, y):                      # a row of identical numbered stakes, no names
    g = ''
    for i, u in enumerate((-66, -22, 22, 66)):
        g += jl([(x + u, y), (x + u, y - 30)], r, 2.4) + shape(r, rect_pts(x + u - 12, y - 46, 24, 16), 2)
        g += hand(str(1041 + i * 3), 8, x + u, y - 34)
    return g
SPEC.update({165: ("cemetery", C(X(bell_grave, 0, G))), 163: ("cemetery", C(X(unclaimed, 0, G)))})
def chair_at_table(r, x, y):                 # table set for two; one chair pulled in and empty, the other person sitting alone
    g = jl([(x - 30, y - 34), (x + 30, y - 34)], r, 2.8) + jl([(x - 24, y - 34), (x - 24, y)], r, 2.2) + jl([(x + 24, y - 34), (x + 24, y)], r, 2.2)
    g += ell(x - 14, y - 37, 8, 2.4, 1.6) + ell(x + 14, y - 37, 8, 2.4, 1.6) + pl([(x + 2, y - 36), (x + 2, y - 46)], 1.4)
    g += jl([(x + 44, y), (x + 44, y - 24), (x + 62, y - 24), (x + 62, y)], r, 2.2) + jl([(x + 62, y - 24), (x + 64, y - 62)], r, 2.2)   # empty chair
    g += jl([(x - 62, y), (x - 62, y - 24), (x - 44, y - 24), (x - 44, y)], r, 2.2) + jl([(x - 62, y - 24), (x - 64, y - 60)], r, 2.2)
    g += head(x - 52, y - 62) + pl([(x - 54, y - 54), (x - 52, y - 28)], 2.6) + pl([(x - 52, y - 28), (x - 34, y - 28), (x - 32, y)], 2.4)
    return g + pl([(x - 53, y - 48), (x - 34, y - 38)], 2.2)
def phone_glow(r, x, y):                     # sitting on the ground, knees up, looking at a phone; a contact card glows on the screen
    g = head(x - 10, y - 48) + pl([(x - 14, y - 40), (x - 18, y - 2)], 2.6) + pl([(x - 18, y - 2), (x + 4, y - 22), (x + 10, y)], 2.4)
    g += pl([(x - 15, y - 34), (x, y - 30), (x + 4, y - 36)], 2.2)
    g += shape(r, rect_pts(x + 2, y - 46, 9, 14), 1.8) + ''.join(pl([(x + 6.5 + 12 * c, y - 39 - 12 * s), (x + 6.5 + 17 * c, y - 39 - 17 * s)], 1) for c, s in ((0.9, 0.4), (0.6, 0.8), (1, -0.1)))
    return g + ell(x + 6.5, y - 42, 2, 2, 1) + pl([(x + 4, y - 37), (x + 9, y - 37)], 0.9)
def casseroles(r, x, y):                     # a stack of covered casserole dishes on a table, one more being handed over
    g = jl([(x - 40, y - 30), (x + 40, y - 30)], r, 2.8) + jl([(x - 34, y - 30), (x - 34, y)], r, 2.2) + jl([(x + 34, y - 30), (x + 34, y)], r, 2.2)
    for i in range(4):
        b = y - 32 - i * 13
        g += f'<path d="M{x-22} {b-9} L{x-20} {b} L{x+20} {b} L{x+22} {b-9} Z" fill="{B()}" stroke="{I()}" stroke-width="2"/>'
        g += pl([(x - 26, b - 7), (x - 22, b - 7)], 2) + pl([(x + 22, b - 7), (x + 26, b - 7)], 2)
        g += f'<path d="M{x-20} {b-9} Q{x} {b-15} {x+20} {b-9}" fill="none" stroke="{I()}" stroke-width="1.6"/>'
    return g + ell(x, y - 32 - 3 * 13 - 13, 2, 2, 1.4)
SPEC.update({170: ("cabin", C(X(chair_at_table, 0, G))), 171: ("cabin", C(X(phone_call, -10, G))), 172: ("pines", C(X(phone_glow, 0, G))), 175: ("cabin", C(X(casseroles, 0, G)))})
def their_chair(r, x, y):                    # an empty armchair with a jacket over its back; someone standing looking at it
    g = shape(r, [(x + 6, y), (x + 6, y - 26), (x + 2, y - 62), (x + 12, y - 70), (x + 52, y - 70), (x + 60, y - 62), (x + 56, y - 26), (x + 56, y)], 2.4)
    g += jl([(x + 6, y - 26), (x + 56, y - 26)], r, 2) + jl([(x + 2, y - 40), (x - 4, y - 36), (x - 2, y - 24), (x + 6, y - 24)], r, 2) + jl([(x + 60, y - 40), (x + 66, y - 36), (x + 64, y - 24), (x + 56, y - 24)], r, 2)
    g += shape(r, [(x + 18, y - 70), (x + 40, y - 70), (x + 44, y - 40), (x + 36, y - 44), (x + 30, y - 36), (x + 22, y - 44), (x + 14, y - 40)], 1.8)
    hx = x - 40
    return g + head(hx, y - 52) + pl([(hx, y - 44), (hx, y - 18)], 2.6) + pl([(hx - 8, y), (hx, y - 18), (hx + 8, y)], 2.6) + pl([(hx - 9, y - 26), (hx, y - 38), (hx + 9, y - 26)], 2.2)
SPEC.update({170: ("cabin", C(X(their_chair, 0, G))), 179: ("cabin", C(X(chair_at_table, 0, G)))})
def dead_cart(r, x, y):                      # figure pulling a two-wheeled handcart with a coffin, ringing a hand bell overhead
    g = shape(r, [(x - 10, y - 16), (x + 70, y - 16), (x + 66, y - 28), (x - 6, y - 28)], 2.2) + ell(x + 30, y - 9, 9, 9) + ell(x + 30, y - 9, 2, 2, 1.2)
    g += nt.coffin_side(x + 30, y - 30, 70, 12)
    g += jl([(x - 10, y - 22), (x - 34, y - 30)], r, 2.2)
    hx = x - 44
    g += head(hx, y - 52) + pl([(hx + 2, y - 44), (hx + 6, y - 18)], 2.6) + pl([(hx - 4, y), (hx + 6, y - 18), (hx + 14, y)], 2.6)
    g += pl([(hx + 3, y - 38), (hx + 12, y - 32), (x - 34, y - 30)], 2.2) + pl([(hx + 3, y - 38), (hx - 8, y - 50), (hx - 10, y - 62)], 2.2)
    g += f'<path d="M{hx-17} {y-62} Q{hx-16} {y-74} {hx-10} {y-76} Q{hx-4} {y-74} {hx-3} {y-62} Z" fill="{B()}" stroke="{I()}" stroke-width="2"/>'
    return g + ''.join(pl([(hx - 10 + c * 10, y - 70 - s * 10), (hx - 10 + c * 14, y - 70 - s * 14)], 1.1) for c, s in ((-0.9, 0.4), (0.9, 0.4), (0, 1)))
def mortar_bone(r, x, y):                    # big mortar and pestle; a bone end sticks out, powder spilling
    g = f'<path d="M{x-40} {y-46} L{x+40} {y-46} Q{x+38} {y-10} {x+14} {y-4} L{x+18} {y} L{x-18} {y} L{x-14} {y-4} Q{x-38} {y-10} {x-40} {y-46} Z" fill="{B()}" stroke="{I()}" stroke-width="2.6"/>'
    g += jl([(x - 40, y - 46), (x + 40, y - 46)], r, 3)
    g += f'<path d="M{x+8} {y-40} L{x+40} {y-92} Q{x+48} {y-98} {x+50} {y-88} L{x+16} {y-38} Z" fill="{B()}" stroke="{I()}" stroke-width="2.4"/>'
    g += jl([(x - 16, y - 44), (x - 30, y - 70)], r, 3, 0.2) + ell(x - 33, y - 73, 3.4, 3.4, 1.4) + ell(x - 28, y - 75, 3.4, 3.4, 1.4)
    return g + ''.join(ell(x + u, y + v, 1, 1, 0.8) for u, v in ((-48, -4), (-54, -1), (46, -3), (52, -1), (-44, -1), (58, -2)))
SPEC.update({187: ("valley", C(X(dead_cart, 0, G))), 191: ("meadow", C(X(mortar_bone, 0, G)))})
def full_skull(r, x, y):                     # big skull; a tangled scribble of thoughts spills out of a crack in the top
    g = skull_l(r, x, y - 40, 1.8)
    g += jl([(x - 6, y - 92), (x - 2, y - 82), (x - 8, y - 74)], r, 1.6, 0.2) + jl([(x + 10, y - 92), (x + 6, y - 80)], r, 1.6, 0.2)
    import math as _m
    pts = []
    for i in range(46):
        t = i / 45 * 6.2 * _m.pi; rad = 6 + i * 0.55
        pts.append((x + rad * _m.cos(t) * 1.4, y - 126 - rad * _m.sin(t) * 0.7))
    return g + jl([(x, y - 92), (x + 2, y - 104)] + pts, r, 1.2, 0.6, 3)
SPEC.update({206: ("pines", C(X(full_skull, 0, G)))})
def bearers_walk(r, x, y):                   # coffin (classic six-sided shape, cross on the lid) on the shoulders of three walking bearers; heads drawn over its edge
    g = f'<path d="M{x-70} {y-46} L{x-58} {y-62} L{x+40} {y-64} L{x+70} {y-54} L{x+66} {y-44} L{x-66} {y-40} Z" fill="{B()}" stroke="{I()}" stroke-width="2.6"/>'
    g += jl([(x - 20, y - 60), (x - 20, y - 46)], r, 1.6) + jl([(x - 27, y - 55), (x - 13, y - 55)], r, 1.6)
    for u in (-46, 0, 46):
        g += head(x + u + 4, y - 44) + pl([(x + u, y - 36), (x + u, y - 20)], 2.6) + pl([(x + u - 9, y), (x + u, y - 20), (x + u + 9, y - 2)], 2.6)
        g += pl([(x + u, y - 32), (x + u - 4, y - 42)], 2.2)
    return g
SPEC.update({65: ("cemetery", C(X(bearers_walk, 0, G)))})
def heart_beat(r, x, y):                     # anatomical heart on a stone, beat lines around it, a pulse line running off along the ground
    g = shape(r, [(x - 34, y), (x - 28, y - 12), (x + 28, y - 12), (x + 34, y)], 2.2) + heart_l(r, x, y - 30, 0.75)
    g += ''.join(jl([(x + d * 34, y - 50 + v), (x + d * 44, y - 54 + v)], r, 1.6, 0.2) for d in (-1, 1) for v in (-8, 4))
    return g + jl([(x + 36, y - 4), (x + 50, y - 4), (x + 55, y - 18), (x + 60, y + 4), (x + 64, y - 4), (x + 86, y - 4)], r, 1.6, 0.2)
SPEC.update({142: ("meadow", C(X(heart_beat, -16, G)))})
def molar_roots(r, x, y):                    # a molar sitting on the ground like a stump; curling roots spread into the cut-away soil
    g = shape(r, [(x - 26, y), (x - 30, y - 30), (x - 18, y - 42), (x, y - 34), (x + 18, y - 42), (x + 30, y - 30), (x + 26, y)])
    g += jl([(x - 2, y - 34), (x + 4, y - 20), (x - 4, y - 8)], r, 1.6)
    for d in (-1, 1):
        g += f'<path d="M{x+d*16} {y} C{x+d*22} {y+8} {x+d*38} {y+6} {x+d*46} {y+14} M{x+d*24} {y+5} C{x+d*26} {y+12} {x+d*22} {y+18} {x+d*28} {y+24} M{x+d*40} {y+9} q{d*6} -2 {d*10} 2" fill="none" stroke="{I()}" stroke-width="1.6" stroke-linecap="round"/>'
    return g + f'<path d="M{x} {y} C{x+2} {y+8} {x-3} {y+14} {x+1} {y+22}" fill="none" stroke="{I()}" stroke-width="1.6" stroke-linecap="round"/>'
SPEC.update({152: ("meadow", C(X(molar_roots, 0, G)))})

"""Builds designs/review-viewer/: one page that shows every sketch (01-219) next to its night-style redraw (01-207).
Run after svgs_dark.py / svgs_set3.py / svgs_night.py / svgs_redo.py:  python3 tools/build_review.py"""
import os, sys, json, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SK, NI = os.path.join(ROOT, "designs", "sketches"), os.path.join(ROOT, "designs", "sketches-night")
OUT = os.path.join(ROOT, "designs", "review-viewer")
from designs_data import FIRST, DESIGNS
from designs_data3 import SET3
from designs_data_night import NIGHT

GROUP_ICONS = {
    "Morgue": "toe_tag body_bag morgue_drawer y_incision autopsy_report organ_scale rib_spreader skull_saw brain_jar slabs embalm lividity thermo jaw_xray triptych layers",
    "Decay": "maggots flies rot_skull rot_lifter skull_flies bloat skin_glove marbled big_fly cycle beetle_skull wax_grave mummy_hand stain shroom_ribs root_skull eye_beetle stages petri crow_ribs flower rose",
    "Anatomy": "anatomical_heart flayed_figure torn_bicep fibers thigh_section sutured_heart microtear nerves molars skinless_face vials butcher knee torn_palm heart brain",
    "Burial": "coffin tombstone open_grave obituary wreath grave_tape nailed lowering shovel_pile markers robber bell_coffin ossuary hearse vault",
    "Grief": "chair phone_old phone_screen urn_books monitor casseroles heart_box eulogy candle_out plates_table candle flatline ekg figures2",
    "Reaper": "reaper skull skeleton reaper_glass skel_hoodie reaper_clip danse reaper_sharpen two_skulls skull_candle plague reaper_ticket barrow ghost bones bat raven moth hand_skel",
    "Cremation": "retort tray_bones urn_label chimney ash_lake pacemaker ash_scale id_disc bottle",
    "Gym": "barbell dumbbell kettlebell plate rack death_grip figure same_bones spine_bar spine_yoke rib_rack heart_plates flayed_arm ecorche_squat chalk_squat",
}
ICON_GROUP = {i: g for g, s in GROUP_ICONS.items() for i in s.split()}

# Review of the ORIGINAL sketches (2026-11-27). Originals are unchanged; these are notes only.
NOTES = {
    7: "Sleeve text reads small; the chest icon is tiny.", 23: "Sleeve text reads small.", 67: "Sleeve text reads small.",
    92: "Sleeve text reads small.", 101: "Sleeve text reads small.",
    26: "Form text is too small to print or read at a distance.", 35: "Obituary text is too small to print.",
    45: "Flayed-figure labels are too small to read.", 63: "Typewriter banner text is small.",
    98: "Hood-band text is small.", 99: "Hood-band text is small.", 100: "Hood-band text is small.",
    25: "Same coffin icon as 34, 50, 54, 65, 93.", 34: "Same coffin icon as 25, 50, 54, 65, 93.", 54: "Same coffin icon as 25, 34, 50, 65, 93.",
    65: "Same coffin icon as 25, 34, 50, 54, 93.", 93: "Same coffin icon as 25, 34, 50, 54, 65.", 50: "Same coffin icon as 25, 34, 54, 65, 93.",
    27: "Same half-rotted skull as 11, 53, 58, 71.", 53: "Same half-rotted skull as 11, 27, 58, 71.", 58: "Same half-rotted skull as 11, 27, 53, 71.",
    71: "Same half-rotted skull as 11, 27, 53, 58.", 11: "Same half-rotted skull as 27, 53, 58, 71.",
    32: "Same anatomical heart as 24, 51, 62, 66.", 62: "Same anatomical heart as 24, 32, 51, 66.",
    80: "Same morgue drawer as 20 and 85.", 85: "Same morgue drawer as 20 and 80.",
    43: "Same tombstone-with-hand as 42 and 59.", 59: "Same tombstone-with-hand as 42 and 43.", 88: "Same 'NOT YET' tombstone as 83.",
    97: "Same two skeletons as 08, 21, 38, 70.", 70: "Same two skeletons as 08, 21, 38, 97.",
    29: "Type-only stack looks like 22, 37, 39, 79, 94, 96 (thorns + skull).", 79: "Type-only stack looks like 22, 29, 37, 39, 94, 96.",
    113: "Dotted saw line is faint at size.", 124: "Hand-shedding-skin art is hard to read.", 129: "The body in the grave is hard to see.",
    141: "Skinless squat figure is rough.", 187: "Plague doctor reads more like a bird than a person.",
}
NIGHT_NOTE = "Line-art redraws share about 30 line-art subjects, so some are less specific than the original (e.g. gore anatomy becomes a sheeted body on a gurney)."

def risk_of(note):
    m = re.search(r"Ad risk ([HML])", note or "")
    return m.group(1) if m else ""

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "o")); os.makedirs(os.path.join(OUT, "n"))
    sk = {int(f.split("-")[0]): f for f in os.listdir(SK) if re.match(r"^\d+-.*\.svg$", f)}
    ni = {int(f.split("-")[0]): f for f in os.listdir(NI) if re.match(r"^\d+-.*\.svg$", f)}
    rows = []
    for i, d in enumerate(FIRST + DESIGNS + SET3 + NIGHT):
        n = i + 1
        shutil.copy(os.path.join(SK, sk[n]), os.path.join(OUT, "o", f"{n:03d}.svg"))
        has = n in ni
        if has: shutil.copy(os.path.join(NI, ni[n]), os.path.join(OUT, "n", f"{n:03d}.svg"))
        cap = " ".join(d["lines"]) + (" / " + d["sub"] if d.get("sub") else "")
        rows.append({"n": n, "cap": cap, "place": d["place"], "group": "Night designs" if n >= 208 else ICON_GROUP.get(d.get("icon"), "Dread"),
                     "risk": risk_of(d.get("note")), "note": NOTES.get(n, ""), "night": has, "newstyle": n >= 208})
    with open(os.path.join(OUT, "data.json"), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r) for r in rows) + "\n]\n")
    shutil.copy(os.path.join(HERE, "review_index.html"), os.path.join(OUT, "index.html"))
    print(len(rows), "designs,", sum(r["night"] for r in rows), "redraws,", sum(1 for r in rows if r["note"]), "notes")

if __name__ == "__main__":
    main()

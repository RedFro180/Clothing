"""Writes designs/redraw-audit.md: caption -> what the line-art redraw shows -> checks. Run after editing tools/redo_specs.py."""
import re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from svgs_redo import all_designs
WORDS = {"skel_lift":"skeleton gripping a loaded barbell","bench_spot":"bench press with a spotter","farmer_coffins":"walking with a small coffin in each hand",
"coffin_backpack":"small coffin carried on the back","cracked":"figure with a crack across the chest","bar_floor":"barbell on the floor","eyes_forest":"eyes watching from the trees",
"two_on_log":"two people sitting together on a log","mailbox":"mailbox","belt_on":"lifting belt on the coffin","worms_soil":"skull underground with worms","tape":"tape measure",
"six_carry":"pallbearers carrying a coffin","cave":"dark cave mouth (the void)","cradle":"cradle","thermometer":"thermometer","bell_post":"bell on a post above a grave",
"barrow":"wheelbarrow of bones","moth":"moths","maggots":"maggots","crown_skulls":"crowned skull beside a plain skull","candle_out":"blown-out candle with smoke",
"monitor_bed":"hospital bed and monitor","skull_dashed":"skull with a dotted cut line","big_fly":"large fly","sweat":"sweat drops","ghosts":"several ghosts","ghost_l":"ghost",
"dye_pot":"dye pot over a fire with plants","scale_urn":"urn on a scale","row_markers":"row of numbered grave markers","skull_teeth":"large skull with teeth",
"two_lifters":"two people lifting side by side","scale_stand":"platform scale with a heart on it","skeleton_l":"skeleton","stand":"standing figure","press":"overhead press",
"deadlift":"deadlift","coffin_up":"upright coffin","grave_open":"open grave and shovel","tomb":"headstone","gurney":"covered body on a gurney","drawer":"morgue drawers",
"bodybag":"body bag","reaper_l":"reaper","heart_l":"heart","rack_l":"squat rack","candle_l":"candle","hourglass_l":"hourglass","clock_l":"clock","rose_l":"wilted rose",
"sign_l":"sign with text","wreath_l":"wreath","bottle_l":"bottle","table_l":"table","jar_l":"specimen jar","crem_l":"crematorium","urn_l":"urn","chair_l":"empty chair",
"phone_l":"phone","bed_l":"bed","trap_l":"heart in a trap","hearse_l":"hearse","bones_pile":"pile of skulls/bones","shrooms_l":"mushrooms from a skull","roots_skull":"roots through a skull",
"crows_tree":"crows in a dead tree","flies_skull":"skull with flies","ekg_ridge":"flatline ridge","body_gore":"body on a gurney","skeleton_lie":"skeleton lying in grass",
"dance":"dancing skeletons","two_at_grave":"two people at a grave","two_carry":"two people carrying a coffin","ash_lake_l":"ash over a lake","stone":"stone","rain_cloud":"rain cloud over the head",
"sit_hug":"figure hugging knees","sit_lean":"figure sitting back","kneel":"kneeling figure","lie":"figure lying down","walk":"walking figure","carry_rock":"carrying a heavy rock",
"campfire":"campfire","dead_tree":"dead tree","grave_mound":"grave mound","coffin_side":"coffin","bear_press":"overhead press with little BEARS as the weights",
"champ_skull":"skull wearing a champion belt","cloud_plates":"overhead press with thought clouds as the plates","cutting_board":"heart on a butcher's cutting board with a knife",
"mirror":"mirror showing a skull","sunrise":"sunrise behind the grave","banana":"banana","crime_tape":"'DO NOT CROSS' tape","steak_lift":"deadlift with meat drumsticks as plates",
"tear":"teardrop","heart_pump":"heart hooked to a pump","sprout":"sprout growing from a crack","molar_roots":"molar with roots in the ground","easel_steak":"meat in a picture frame on an easel",
"vault_box":"coffin inside a concrete block","flex_smile":"figure flexing with a big smile","runner_battery":"runner with a one-bar battery","xray":"body outline with the skeleton showing",
"steam":"steam rising","sling":"figure with an arm sling","thought":"thought bubble","glove_bones":"bone hand beside a lifting glove","life_row":"egg → larva → pupa → fly → skull",
"body_outline":"dashed body-shaped outline in the grass","squashed":"figure squashed under a huge bar","flame_in":"figure with fire inside","hammer":"hammer","clock_at":"clock at 2:00",
"chalk_squat":"chalk-outline figure squatting a bar","gut":"figure holding the stomach"}
PUN = {153:"Visual pun: load-BEARING = bears on the bar.",18:"Visual pun: undefeated champion belt.",57:"Visual pun: thoughts are literally the plates.",
66:"Visual pun: heart as butcher's meat.",71:"Visual pun: the mirror shows death.",87:"Visual pun: mourning / morning sunrise.",125:"Visual pun: ripening banana (green, then black).",
126:"Visual pun: crime-scene tape.",138:"Visual pun: meat as the plates.",139:"Visual pun: tear (rip) and tear (cry).",142:"Visual pun: pumping.",149:"Visual pun: growth from a tear in the ground.",
152:"Visual pun: tooth roots in the ground.",157:"Visual pun: meat on a picture frame.",169:"Visual pun: concrete vault.",205:"Visual pun: flexing a smile.",35:"Headstone reads YOU.",
29:"Arm sling = everything hurts.",6:"One-bar battery = running on what's left.",11:"X-ray: skeleton inside the body.",141:"X-ray: under the skin.",
15:"Steam = still warm after lifting.",203:"Chalk outline squatting = 'not yet' (alive, training).",160:"Clock at 2:00."}
FACT = {110:"Morgue coolers 36–39°F (Wikipedia: Morgue).",118:"1.5°F/hr is a rough rule of thumb (StatPearls, Wikipedia: Algor mortis).",190:"Retorts ~1,400–1,800°F (ICCFA).",
196:"Remains ~3–9 lb (ICCFA, HowStuffWorks).",195:"Pacemakers removed before cremation (Neptune Society, PMC1279940).",80:"Rigor: ~2 h onset, 6–8 h complete (StatPearls).",
129:"Adipocere = grave wax (Wikipedia).",165:"Victorian safety-coffin bells (Wikipedia).",139:"Distal biceps tear (AAOS).",135:"5 decomposition stages (Wikipedia: Decomposition).",
123:"Bloat timing varies with heat.",126:"Early blowfly arrival: not time-confirmed in sources checked."}
SAFE = {1:"Dead hang read as gallows at sketch size → barbell grip.",103:"Same → barbell grip.",150:"Same → barbell grip.",13:"Branch-hung scale read as a hanging → platform scale.",62:"Same.",109:"Same."}
def main():
    src = open(os.path.join(HERE, "redo_specs.py")).read()
    rows = {}
    for line in src.splitlines():
        m = re.match(r"^(\d+): \(\"(\w+)\", (.*)\),?$", line)
        if not m: continue
        fns = re.findall(r"[XF]\((\w+)", m.group(3)) + re.findall(r"(ghosts)\(", m.group(3))
        seen = []
        for f in fns:
            w = WORDS.get(f, f)
            if w not in seen: seen.append(w)
        rows[int(m.group(1))] = (m.group(2), "; ".join(seen))   # later entries (pass 2) override earlier ones
    D = all_designs()
    out = ["# Redraw audit (2026-11-27, pass 2)", "",
           "Every line-art redraw checked against its own caption. Pass 1 replaced icon-based pictures with caption-based scenes; pass 2 (user: 'some still look incorrect', add puns like bears for load-bearing) fixed 36 more and added visual puns.", "",
           "Rules held: no figure near a drop; nothing hanging (no gallows shapes, nothing dangling from branches); no self-harm; no wish to die.", "",
           "| # | Caption | Picture | Notes |", "|---|---|---|---|"]
    for n in sorted(rows):
        bg, desc = rows[n]; d = D[n - 1]
        cap = " ".join(d["lines"]) + (" / " + d["sub"] if d.get("sub") else "")
        note = " ".join(x for x in (PUN.get(n), SAFE.get(n), FACT.get(n)) if x)
        out.append(f"| {n:03d} | {cap} | {desc} ({bg}) | {note} |")
    out += ["", "Sources: [Wikipedia: Morgue](https://en.wikipedia.org/wiki/Morgue), [StatPearls](https://www.ncbi.nlm.nih.gov/books/NBK539741/), [Wikipedia: Algor mortis](https://en.wikipedia.org/wiki/Algor_mortis), [ICCFA](https://iccfa.com/faq-items/how-long-does-it-take-to-cremate-a-body/), [HowStuffWorks](https://science.howstuffworks.com/cremation1.htm), [Neptune Society](https://neptunesociety.com/resources/cremation-planning/why-pacemaker-should-be-removed-prior-to-cremation), [PMC1279940](https://pmc.ncbi.nlm.nih.gov/articles/PMC1279940), [Wikipedia: Adipocere](https://en.wikipedia.org/wiki/Adipocere), [Wikipedia: Safety coffin](https://en.wikipedia.org/wiki/Safety_coffin), [AAOS](https://orthoinfo.aaos.org/en/diseases--conditions/biceps-tendon-tear-at-the-elbow/), [Wikipedia: Decomposition](https://en.wikipedia.org/wiki/Decomposition)."]
    open(os.path.join(HERE, "..", "designs", "redraw-audit.md"), "w").write("\n".join(out) + "\n")
    print(len(rows), "rows")
if __name__ == "__main__":
    main()

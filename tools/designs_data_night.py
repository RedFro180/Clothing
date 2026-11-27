# Night-landscape line-art set (sketches 208-219), style from the user's reference images (2026-11-27).
# Figures are never at a cliff edge or any drop. scene = a function in tools/svgs_night.py (sc_<scene>).
def N(slug, cap, scene, place, color, note):
    return dict(slug=slug, lines=[cap], sub="", icon="none", place=place, scene=scene, color=color, note=note, src="night")

NIGHT = [
N("bury-me-softly", "Bury me softly", "bury", "back", "Black", "Figure resting against a pine beside a small grave, moon over the valley. Ad risk L."),
N("the-forest-keeps", "The forest keeps what we bury", "forest_keeps", "back", "Charcoal", "Kneeling at a wooden cross in the pines. Ad risk L."),
N("everything-here-outlives-me", "Everything here outlives me", "outlives", "back", "Indigo", "Lying in a meadow under the moon. Ad risk L."),
N("still-here-still-heavy", "Still here. Still heavy.", "heavy", "front", "Plum", "Carrying a boulder up a switchback trail. Ad risk L."),
N("some-nights-are-just-survived", "Some nights are just survived", "survived", "back", "Black", "Knees hugged by a campfire. Ad risk L."),
N("we-all-end-up-in-the-dirt", "We all end up in the dirt", "dirt", "back", "Oxblood", "Hillside cemetery, resting against a headstone. Ad risk L."),
N("dead-trees-still-stand", "Dead trees still stand", "dead_trees", "front", "Undyed oatmeal", "Hand on a dead snag tree. Ad risk L."),
N("two-of-us-carried-it", "Two of us carried it", "carried", "back", "Charcoal", "Two figures carrying a coffin over a ridge. Ad risk M."),
N("grief-is-a-long-walk-home", "Grief is a long walk home", "long_walk", "back", "Indigo", "Tiny figure on a riverside path. Ad risk L."),
N("rest-isnt-quitting", "Rest isn't quitting", "rest", "front", "Sand", "Asleep in a hammock between pines. Ad risk L."),
N("the-moon-doesnt-ask", "The moon doesn't ask", "moon", "back", "Plum", "Sitting on a log under a huge moon. Ad risk L."),
N("home-is-quieter-now", "Home is quieter now", "home", "front", "Black", "On a cabin's porch step, chimney smoke. Ad risk L."),
]
assert len(NIGHT) == 12

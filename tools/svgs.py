import os
OUT="/home/user/Clothing/designs/sketches"
from svgs_base import hoodie, INK, FAB
def svg(name, view, art, title, note):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 720" width="600" height="720" font-family="Arial, Helvetica, sans-serif">
<rect width="600" height="720" fill="#ffffff"/>
{hoodie(view)}
{art}
<text x="300" y="640" text-anchor="middle" font-size="18" font-weight="bold" fill="#222">{title} ({view.upper()})</text>
<text x="300" y="668" text-anchor="middle" font-size="13" fill="#555">{note}</text>
<text x="300" y="700" text-anchor="middle" font-size="11" fill="#999">Placement sketch only. Redraw in your own hand before use.</text>
</svg>'''
    open(os.path.join(OUT,name),"w").write(s)

def fig(x,y,arms="up",s=1.0):
    # stick figure head at (x,y)
    r=14*s
    g=f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK}" stroke-width="6"/>'
    by=y+r; ey=by+55*s
    g+=f'<line x1="{x}" y1="{by}" x2="{x}" y2="{ey}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    if arms=="up":
        g+=f'<polyline points="{x-22*s},{y-38*s} {x-14*s},{by+6*s} {x},{by+10*s} {x+14*s},{by+6*s} {x+22*s},{y-38*s}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
    g+=f'<polyline points="{x-6*s},{ey+52*s} {x},{ey} {x+6*s},{ey+52*s}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    return g

# 1 Keep hanging on: dead hang from pull-up bar
art = (f'<line x1="210" y1="215" x2="390" y2="215" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
       f'<line x1="215" y1="215" x2="215" y2="200" stroke="{INK}" stroke-width="6"/><line x1="385" y1="215" x2="385" y2="200" stroke="{INK}" stroke-width="6"/>'
       + fig(300,268,"up",1.0) +
       f'<text x="300" y="410" text-anchor="middle" font-size="34" font-weight="900" fill="{INK}" letter-spacing="2">KEEP HANGING ON</text>'
       f'<text x="300" y="438" text-anchor="middle" font-size="14" fill="{INK}">day 1 of the dead hang. day 4,000 of everything else.</text>')
svg("01-keep-hanging-on.svg","front",art,"Keep Hanging On","Dead-hang pull-up joke. 1 color. Works as mordant print.")

# 2 Take the leap: box jump
art = (f'<rect x="320" y="330" width="90" height="70" fill="{INK}"/>'
       f'<text x="365" y="372" text-anchor="middle" font-size="16" font-weight="bold" fill="{FAB}">24"</text>'
       + f'<g transform="rotate(20 250 300)">{fig(250,275,"up",0.75)}</g>' +
       f'<path d="M190 400 L430 400" stroke="{INK}" stroke-width="5"/>'
       f'<text x="300" y="215" text-anchor="middle" font-size="30" font-weight="900" fill="{INK}">TAKE THE LEAP</text>'
       f'<text x="300" y="430" text-anchor="middle" font-size="14" fill="{INK}">(it is a 24-inch box. calm down.)</text>')
svg("02-take-the-leap-box-jump.svg","front",art,"Take the Leap","Box-jump version, not a cliff. 1 color.")

# 3 I'll spot you (back)
art = (f'<line x1="170" y1="260" x2="430" y2="260" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
       f'<rect x="160" y="220" width="22" height="80" fill="{INK}"/><rect x="418" y="220" width="22" height="80" fill="{INK}"/>'
       f'<rect x="140" y="232" width="18" height="56" fill="{INK}"/><rect x="442" y="232" width="18" height="56" fill="{INK}"/>'
       + ''.join(f'<rect x="{cx-26}" y="300" width="52" height="34" rx="14" fill="{INK}"/>' + ''.join(f'<rect x="{cx-24+k*13}" y="272" width="10" height="34" rx="5" fill="{INK}"/>' for k in range(4)) + f'<rect x="{cx-14}" y="334" width="28" height="30" fill="{INK}"/>' for cx in (255,345)) +
       f'<text x="300" y="420" text-anchor="middle" font-size="44" font-weight="900" fill="{INK}">I\'LL SPOT YOU.</text>'
       f'<text x="300" y="452" text-anchor="middle" font-size="15" fill="{INK}">heavy days don\'t get lifted alone.</text>'
       f'<text x="300" y="530" text-anchor="middle" font-size="12" fill="{INK}">call or text 988</text>')
svg("03-ill-spot-you.svg","back",art,"I'll Spot You","Back print. Connection theme. 1 color.")

# 4 Emotionally load-bearing: farmer's carry
art = (fig(300,250,"none",1.0) +
       f'<line x1="300" y1="285" x2="250" y2="330" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
       f'<line x1="300" y1="285" x2="350" y2="330" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
       f'<rect x="222" y="330" width="56" height="60" rx="6" fill="{INK}"/><rect x="322" y="330" width="56" height="60" rx="6" fill="{INK}"/>'
       f'<text x="250" y="366" text-anchor="middle" font-size="13" font-weight="bold" fill="{FAB}">PAST</text>'
       f'<text x="350" y="366" text-anchor="middle" font-size="13" font-weight="bold" fill="{FAB}">FUTURE</text>'
       f'<text x="300" y="430" text-anchor="middle" font-size="28" font-weight="900" fill="{INK}">EMOTIONALLY</text><text x="300" y="462" text-anchor="middle" font-size="28" font-weight="900" fill="{INK}">LOAD-BEARING</text>')
svg("04-emotionally-load-bearing.svg","front",art,"Emotionally Load-Bearing","Farmer's carry. Bold shapes + 1 line of type.")

# 5 Mourning routine checklist (back)
items=["black coffee","pre-workout","existential dread","leg day anyway"]
art = f'<text x="300" y="230" text-anchor="middle" font-size="40" font-weight="900" fill="{INK}">MOURNING ROUTINE</text>'
for i,t in enumerate(items):
    y=280+i*48
    art+=f'<rect x="190" y="{y-24}" width="28" height="28" fill="none" stroke="{INK}" stroke-width="5"/>'
    art+=f'<path d="M195 {y-10} L204 {y} L222 {y-30}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    art+=f'<text x="236" y="{y}" font-size="24" fill="{INK}">{t}</text>'
svg("05-mourning-routine.svg","back",art,"Mourning Routine","Back print. Type only, easy to block or screen print.")

# 6 Low battery, high volume
art = (f'<rect x="200" y="250" width="180" height="90" rx="10" fill="none" stroke="{INK}" stroke-width="8"/>'
       f'<rect x="380" y="275" width="16" height="40" fill="{INK}"/><rect x="212" y="262" width="26" height="66" fill="{INK}"/>'
       f'<text x="300" y="390" text-anchor="middle" font-size="30" font-weight="900" fill="{INK}">LOW BATTERY.</text>'
       f'<text x="300" y="426" text-anchor="middle" font-size="30" font-weight="900" fill="{INK}">HIGH VOLUME.</text>')
svg("06-low-battery-high-volume.svg","front",art,"Low Battery. High Volume.","Gym volume joke. 1 color.")

# 7 Grief is love doing reps (sleeve + small chest)
art = (f'<text transform="translate(138 205) rotate(105.6)" font-size="15" font-weight="bold" fill="{INK}">GRIEF IS JUST LOVE DOING REPS</text>'
       f'<circle cx="380" cy="230" r="18" fill="none" stroke="{INK}" stroke-width="5"/><line x1="362" y1="230" x2="398" y2="230" stroke="{INK}" stroke-width="5"/>')
svg("07-grief-is-love-doing-reps.svg","front",art,"Grief Is Just Love Doing Reps","Left sleeve type + small chest mark. Sleeve is hard to hand print; consider embroidery.")
print(sorted(os.listdir(OUT)))

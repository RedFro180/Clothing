"""Sketches 08-107: hoodie placement sketches. Run: python3 tools/svgs_more.py
Same style as tools/svgs.py. Each design = (id, slug, lines, subline, icon, placement, note, source)."""
import os, html, math
from svgs_base import hoodie, INK, FAB

OUT = "/home/user/Clothing/designs/sketches"
E = html.escape

# ---------- icon library: each returns SVG drawn centered on (x, y) at scale s ----------
def stroke(w=6): return f'fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
def barbell(x, y, s=1):
    w = 120*s
    g = f'<line x1="{x-w}" y1="{y}" x2="{x+w}" y2="{y}" stroke="{INK}" stroke-width="{8*s}" stroke-linecap="round"/>'
    for d in (-1, 1):
        g += f'<rect x="{x+d*(w-28*s)-(0 if d>0 else 18*s)}" y="{y-36*s}" width="{18*s}" height="{72*s}" rx="{3*s}" fill="{INK}"/>'
        g += f'<rect x="{x+d*(w-8*s)-(0 if d>0 else 14*s)}" y="{y-26*s}" width="{14*s}" height="{52*s}" rx="{3*s}" fill="{INK}"/>'
    return g
def dumbbell(x, y, s=1):
    g = f'<line x1="{x-45*s}" y1="{y}" x2="{x+45*s}" y2="{y}" stroke="{INK}" stroke-width="{10*s}"/>'
    for d in (-1, 1):
        g += f'<rect x="{x+d*45*s-(22*s if d<0 else 0)}" y="{y-28*s}" width="{22*s}" height="{56*s}" rx="{5*s}" fill="{INK}"/>'
    return g
def kettlebell(x, y, s=1):
    return (f'<path d="M{x-26*s} {y-30*s} Q{x-26*s} {y-70*s} {x} {y-70*s} Q{x+26*s} {y-70*s} {x+26*s} {y-30*s}" {stroke(10*s)}/>'
            f'<circle cx="{x}" cy="{y+5*s}" r="{45*s}" fill="{INK}"/><rect x="{x-30*s}" y="{y+42*s}" width="{60*s}" height="{8*s}" fill="{INK}"/>')
def plate(x, y, s=1, label=""):
    g = f'<circle cx="{x}" cy="{y}" r="{60*s}" fill="{INK}"/><circle cx="{x}" cy="{y}" r="{42*s}" fill="none" stroke="{FAB}" stroke-width="{3*s}"/><circle cx="{x}" cy="{y}" r="{10*s}" fill="{FAB}"/>'
    if label: g += f'<text x="{x}" y="{y-20*s}" text-anchor="middle" font-size="{14*s}" font-weight="bold" fill="{FAB}">{E(label)}</text>'
    return g
def skull(x, y, s=1):
    return (f'<path d="M{x-48*s} {y} Q{x-48*s} {y-62*s} {x} {y-62*s} Q{x+48*s} {y-62*s} {x+48*s} {y} L{x+30*s} {y+18*s} L{x+30*s} {y+42*s} L{x-30*s} {y+42*s} L{x-30*s} {y+18*s} Z" fill="{INK}"/>'
            f'<circle cx="{x-19*s}" cy="{y-10*s}" r="{13*s}" fill="{FAB}"/><circle cx="{x+19*s}" cy="{y-10*s}" r="{13*s}" fill="{FAB}"/>'
            f'<path d="M{x} {y+4*s} L{x-7*s} {y+16*s} L{x+7*s} {y+16*s} Z" fill="{FAB}"/>'
            + ''.join(f'<line x1="{x+k*12*s}" y1="{y+26*s}" x2="{x+k*12*s}" y2="{y+42*s}" stroke="{FAB}" stroke-width="{3*s}"/>' for k in (-1, 0, 1)))
def tombstone(x, y, s=1, label="RIP"):
    return (f'<path d="M{x-50*s} {y+60*s} L{x-50*s} {y-20*s} Q{x-50*s} {y-70*s} {x} {y-70*s} Q{x+50*s} {y-70*s} {x+50*s} {y-20*s} L{x+50*s} {y+60*s} Z" fill="{INK}"/>'
            f'<line x1="{x-80*s}" y1="{y+60*s}" x2="{x+80*s}" y2="{y+60*s}" stroke="{INK}" stroke-width="{6*s}" stroke-linecap="round"/>'
            f'<text x="{x}" y="{y-5*s}" text-anchor="middle" font-size="{20*s}" font-weight="bold" fill="{FAB}">{E(label)}</text>')
def coffin(x, y, s=1, label=""):
    g = f'<path d="M{x-25*s} {y-75*s} L{x+25*s} {y-75*s} L{x+42*s} {y-35*s} L{x+25*s} {y+75*s} L{x-25*s} {y+75*s} L{x-42*s} {y-35*s} Z" fill="{INK}"/>'
    if label: g += f'<text x="{x}" y="{y+5*s}" text-anchor="middle" font-size="{14*s}" font-weight="bold" fill="{FAB}">{E(label)}</text>'
    else: g += f'<line x1="{x}" y1="{y-45*s}" x2="{x}" y2="{y+10*s}" stroke="{FAB}" stroke-width="{5*s}"/><line x1="{x-15*s}" y1="{y-28*s}" x2="{x+15*s}" y2="{y-28*s}" stroke="{FAB}" stroke-width="{5*s}"/>'
    return g
def ghost(x, y, s=1):
    return (f'<path d="M{x-40*s} {y+50*s} L{x-40*s} {y-10*s} Q{x-40*s} {y-60*s} {x} {y-60*s} Q{x+40*s} {y-60*s} {x+40*s} {y-10*s} L{x+40*s} {y+50*s} L{x+27*s} {y+38*s} L{x+13*s} {y+50*s} L{x} {y+38*s} L{x-13*s} {y+50*s} L{x-27*s} {y+38*s} Z" fill="{INK}"/>'
            f'<circle cx="{x-14*s}" cy="{y-14*s}" r="{7*s}" fill="{FAB}"/><circle cx="{x+14*s}" cy="{y-14*s}" r="{7*s}" fill="{FAB}"/>')
def battery(x, y, s=1, level=1):
    g = f'<rect x="{x-80*s}" y="{y-40*s}" width="{160*s}" height="{80*s}" rx="{10*s}" {stroke(8*s)}/><rect x="{x+80*s}" y="{y-16*s}" width="{14*s}" height="{32*s}" fill="{INK}"/>'
    for k in range(level): g += f'<rect x="{x-68*s+k*38*s}" y="{y-28*s}" width="{30*s}" height="{56*s}" fill="{INK}"/>'
    return g
def heart(x, y, s=1, cracked=False):
    g = f'<path d="M{x} {y+50*s} L{x-50*s} {y} Q{x-75*s} {y-30*s} {x-50*s} {y-50*s} Q{x-20*s} {y-70*s} {x} {y-35*s} Q{x+20*s} {y-70*s} {x+50*s} {y-50*s} Q{x+75*s} {y-30*s} {x+50*s} {y} Z" fill="{INK}"/>'
    if cracked: g += f'<polyline points="{x},{y-35*s} {x-10*s},{y-10*s} {x+8*s},{y+5*s} {x-4*s},{y+30*s}" fill="none" stroke="{FAB}" stroke-width="{5*s}"/>'
    return g
def brain(x, y, s=1):
    g = f'<path d="M{x-60*s} {y+10*s} Q{x-75*s} {y-30*s} {x-40*s} {y-45*s} Q{x-25*s} {y-70*s} {x} {y-50*s} Q{x+25*s} {y-70*s} {x+40*s} {y-45*s} Q{x+75*s} {y-30*s} {x+60*s} {y+10*s} Q{x+55*s} {y+40*s} {x+20*s} {y+38*s} Q{x} {y+50*s} {x-20*s} {y+38*s} Q{x-55*s} {y+40*s} {x-60*s} {y+10*s} Z" fill="{INK}"/>'
    g += f'<path d="M{x} {y-48*s} L{x} {y+40*s} M{x-40*s} {y-15*s} Q{x-20*s} {y-5*s} {x-35*s} {y+15*s} M{x+40*s} {y-15*s} Q{x+20*s} {y-5*s} {x+35*s} {y+15*s}" fill="none" stroke="{FAB}" stroke-width="{4*s}"/>'
    return g
def coffee(x, y, s=1):
    return (f'<path d="M{x-40*s} {y-30*s} L{x+40*s} {y-30*s} L{x+32*s} {y+45*s} L{x-32*s} {y+45*s} Z" fill="{INK}"/>'
            f'<path d="M{x+38*s} {y-15*s} Q{x+70*s} {y-10*s} {x+36*s} {y+22*s}" {stroke(7*s)}/>'
            + ''.join(f'<path d="M{x+k*18*s} {y-40*s} Q{x+k*18*s-10*s} {y-55*s} {x+k*18*s} {y-70*s}" {stroke(4*s)}/>' for k in (-1, 0, 1)))
def clock(x, y, s=1, h=3, m=0):
    g = f'<circle cx="{x}" cy="{y}" r="{55*s}" {stroke(8*s)}/>'
    for ang, ln, w in ((h*30+m*0.5, 28, 8), (m*6, 42, 5)):
        a = math.radians(ang-90); g += f'<line x1="{x}" y1="{y}" x2="{x+ln*s*math.cos(a):.1f}" y2="{y+ln*s*math.sin(a):.1f}" stroke="{INK}" stroke-width="{w*s}" stroke-linecap="round"/>'
    return g
def moon(x, y, s=1):
    return f'<circle cx="{x}" cy="{y}" r="{55*s}" fill="{INK}"/><circle cx="{x+28*s}" cy="{y-14*s}" r="{48*s}" fill="{FAB}"/>'
def candle(x, y, s=1):
    return (f'<rect x="{x-18*s}" y="{y-20*s}" width="{36*s}" height="{80*s}" fill="{INK}"/>'
            f'<path d="M{x} {y-65*s} Q{x+16*s} {y-40*s} {x} {y-28*s} Q{x-16*s} {y-40*s} {x} {y-65*s} Z" fill="{INK}"/>')
def hourglass(x, y, s=1):
    return (f'<line x1="{x-40*s}" y1="{y-60*s}" x2="{x+40*s}" y2="{y-60*s}" stroke="{INK}" stroke-width="{8*s}"/><line x1="{x-40*s}" y1="{y+60*s}" x2="{x+40*s}" y2="{y+60*s}" stroke="{INK}" stroke-width="{8*s}"/>'
            f'<path d="M{x-30*s} {y-55*s} L{x+30*s} {y-55*s} L{x+4*s} {y} L{x+30*s} {y+55*s} L{x-30*s} {y+55*s} L{x-4*s} {y} Z" {stroke(5*s)}/>'
            f'<path d="M{x-18*s} {y+52*s} L{x+18*s} {y+52*s} L{x} {y+30*s} Z" fill="{INK}"/>')
def flower(x, y, s=1):
    g = f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+80*s}" stroke="{INK}" stroke-width="{6*s}"/><path d="M{x} {y+50*s} Q{x+30*s} {y+30*s} {x+40*s} {y+45*s} Q{x+20*s} {y+60*s} {x} {y+50*s} Z" fill="{INK}"/>'
    for k in range(6):
        a = math.radians(k*60); g += f'<ellipse cx="{x+22*s*math.cos(a):.1f}" cy="{y+22*s*math.sin(a):.1f}" rx="{14*s}" ry="{9*s}" transform="rotate({k*60} {x+22*s*math.cos(a):.1f} {y+22*s*math.sin(a):.1f})" fill="{INK}"/>'
    return g + f'<circle cx="{x}" cy="{y}" r="{9*s}" fill="{FAB}"/>'
def cloud(x, y, s=1, rain=True):
    g = (f'<path d="M{x-60*s} {y+15*s} Q{x-80*s} {y-15*s} {x-45*s} {y-20*s} Q{x-35*s} {y-55*s} {x} {y-45*s} Q{x+30*s} {y-65*s} {x+45*s} {y-25*s} Q{x+80*s} {y-20*s} {x+60*s} {y+15*s} Z" fill="{INK}"/>')
    if rain: g += ''.join(f'<line x1="{x+k*25*s}" y1="{y+28*s}" x2="{x+k*25*s-8*s}" y2="{y+52*s}" stroke="{INK}" stroke-width="{5*s}" stroke-linecap="round"/>' for k in (-2, -1, 0, 1, 2))
    return g
def eye(x, y, s=1):
    return (f'<path d="M{x-70*s} {y} Q{x} {y-55*s} {x+70*s} {y} Q{x} {y+55*s} {x-70*s} {y} Z" {stroke(7*s)}/><circle cx="{x}" cy="{y}" r="{20*s}" fill="{INK}"/>')
def bones(x, y, s=1):
    g = ''
    for ang in (35, -35):
        g += f'<g transform="rotate({ang} {x} {y})"><rect x="{x-60*s}" y="{y-6*s}" width="{120*s}" height="{12*s}" fill="{INK}"/>'
        for d in (-1, 1):
            g += f'<circle cx="{x+d*60*s}" cy="{y-9*s}" r="{10*s}" fill="{INK}"/><circle cx="{x+d*60*s}" cy="{y+9*s}" r="{10*s}" fill="{INK}"/>'
        g += '</g>'
    return g
def bat(x, y, s=1):
    return (f'<path d="M{x} {y-10*s} Q{x-25*s} {y-30*s} {x-80*s} {y-25*s} Q{x-60*s} {y-10*s} {x-65*s} {y+10*s} Q{x-45*s} {y} {x-35*s} {y+15*s} Q{x-15*s} {y+2*s} {x} {y+25*s} Q{x+15*s} {y+2*s} {x+35*s} {y+15*s} Q{x+45*s} {y} {x+65*s} {y+10*s} Q{x+60*s} {y-10*s} {x+80*s} {y-25*s} Q{x+25*s} {y-30*s} {x} {y-10*s} Z" fill="{INK}"/>')
def bolt(x, y, s=1):
    return f'<path d="M{x+10*s} {y-65*s} L{x-30*s} {y+8*s} L{x} {y+8*s} L{x-12*s} {y+65*s} L{x+32*s} {y-12*s} L{x+2*s} {y-12*s} Z" fill="{INK}"/>'
def flame(x, y, s=1):
    return f'<path d="M{x} {y-70*s} Q{x+45*s} {y-20*s} {x+35*s} {y+25*s} Q{x+25*s} {y+60*s} {x} {y+60*s} Q{x-25*s} {y+60*s} {x-35*s} {y+25*s} Q{x-40*s} {y-10*s} {x-10*s} {y-30*s} Q{x} {y-10*s} {x+5*s} {y-20*s} Q{x+10*s} {y-45*s} {x} {y-70*s} Z" fill="{INK}"/>'
def bottle(x, y, s=1):
    return (f'<rect x="{x-26*s}" y="{y-40*s}" width="{52*s}" height="{110*s}" rx="{12*s}" fill="{INK}"/><rect x="{x-12*s}" y="{y-62*s}" width="{24*s}" height="{22*s}" fill="{INK}"/>'
            + ''.join(f'<line x1="{x-16*s}" y1="{y+k*22*s}" x2="{x+16*s}" y2="{y+k*22*s}" stroke="{FAB}" stroke-width="{3*s}"/>' for k in (0, 1, 2)))
def anchor(x, y, s=1):
    return (f'<circle cx="{x}" cy="{y-55*s}" r="{12*s}" {stroke(6*s)}/><line x1="{x}" y1="{y-43*s}" x2="{x}" y2="{y+55*s}" stroke="{INK}" stroke-width="{8*s}"/>'
            f'<line x1="{x-30*s}" y1="{y-20*s}" x2="{x+30*s}" y2="{y-20*s}" stroke="{INK}" stroke-width="{7*s}"/>'
            f'<path d="M{x-55*s} {y+10*s} Q{x-50*s} {y+60*s} {x} {y+58*s} Q{x+50*s} {y+60*s} {x+55*s} {y+10*s}" {stroke(8*s)}/>')
def rack(x, y, s=1):
    return (f'<line x1="{x-70*s}" y1="{y-80*s}" x2="{x-70*s}" y2="{y+80*s}" stroke="{INK}" stroke-width="{10*s}"/><line x1="{x+70*s}" y1="{y-80*s}" x2="{x+70*s}" y2="{y+80*s}" stroke="{INK}" stroke-width="{10*s}"/>'
            f'<line x1="{x-95*s}" y1="{y+80*s}" x2="{x+95*s}" y2="{y+80*s}" stroke="{INK}" stroke-width="{10*s}"/>' + barbell(x, y-30*s, s*0.9))
def stopwatch(x, y, s=1):
    return clock(x, y+8*s, s*0.9, 0, 50) + f'<rect x="{x-10*s}" y="{y-60*s}" width="{20*s}" height="{14*s}" fill="{INK}"/>'
def chain(x, y, s=1, broken=False):
    g = ''
    for k in range(-2, 3):
        if broken and k == 0: continue
        g += f'<rect x="{x+k*42*s-24*s}" y="{y-14*s}" width="{48*s}" height="{28*s}" rx="{14*s}" {stroke(7*s)}/>'
    return g
def sun(x, y, s=1, rising=False):
    g = f'<circle cx="{x}" cy="{y}" r="{32*s}" fill="{INK}"/>'
    for k in range(12):
        a = math.radians(k*30)
        if rising and math.sin(a) > 0.1: continue
        g += f'<line x1="{x+44*s*math.cos(a):.1f}" y1="{y+44*s*math.sin(a):.1f}" x2="{x+62*s*math.cos(a):.1f}" y2="{y+62*s*math.sin(a):.1f}" stroke="{INK}" stroke-width="{6*s}" stroke-linecap="round"/>'
    if rising: g += f'<rect x="{x-80*s}" y="{y}" width="{160*s}" height="{40*s}" fill="{FAB}"/><line x1="{x-80*s}" y1="{y}" x2="{x+80*s}" y2="{y}" stroke="{INK}" stroke-width="{6*s}"/>'
    return g
def web(x, y, s=1):
    g = ''
    for k in range(8):
        a = math.radians(k*45); g += f'<line x1="{x}" y1="{y}" x2="{x+70*s*math.cos(a):.1f}" y2="{y+70*s*math.sin(a):.1f}" stroke="{INK}" stroke-width="{3*s}"/>'
    for r in (20, 40, 62):
        pts = ' '.join(f'{x+r*s*math.cos(math.radians(k*45)):.1f},{y+r*s*math.sin(math.radians(k*45)):.1f}' for k in range(9))
        g += f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="{3*s}"/>'
    return g
def figure(x, y, s=1, pose="stand"):
    # head center (x,y)
    r = 14*s; by = y+r; hy = by+55*s
    g = f'<circle cx="{x}" cy="{y}" r="{r}" {stroke(6)}/><line x1="{x}" y1="{by}" x2="{x}" y2="{hy}" {stroke(6)}/>'
    if pose == "stand":
        g += f'<polyline points="{x-28*s},{by+45*s} {x},{by+12*s} {x+28*s},{by+45*s}" {stroke(6)}/>'
    elif pose == "flex":
        g += f'<polyline points="{x-45*s},{by-15*s} {x-40*s},{by+12*s} {x},{by+12*s} {x+40*s},{by+12*s} {x+45*s},{by-15*s}" {stroke(6)}/>'
    elif pose == "sit":
        g += f'<polyline points="{x-20*s},{by+40*s} {x},{by+15*s} {x+20*s},{by+40*s}" {stroke(6)}/>'
        return g + f'<polyline points="{x},{hy} {x+40*s},{hy} {x+40*s},{hy+40*s}" {stroke(6)}/>'
    elif pose == "press":
        g += f'<polyline points="{x-40*s},{y-35*s} {x-30*s},{by+5*s} {x},{by+12*s} {x+30*s},{by+5*s} {x+40*s},{y-35*s}" {stroke(6)}/>' + barbell(x, y-40*s, 0.6*s)
    g += f'<polyline points="{x-18*s},{hy+52*s} {x},{hy} {x+18*s},{hy+52*s}" {stroke(6)}/>'
    return g
def figures2(x, y, s=1):
    return figure(x-40*s, y, s, "stand") + figure(x+40*s, y, s, "stand") + f'<line x1="{x-12*s}" y1="{y+42*s}" x2="{x+12*s}" y2="{y+42*s}" {stroke(6)}/>'
def checklist(x, y, s=1, items=()):
    g = ''
    for i, t in enumerate(items):
        yy = y+i*40*s
        g += f'<rect x="{x-120*s}" y="{yy-22*s}" width="{24*s}" height="{24*s}" {stroke(4)}/><path d="M{x-116*s} {yy-10*s} L{x-108*s} {yy-1*s} L{x-92*s} {yy-26*s}" {stroke(5)}/>'
        g += f'<text x="{x-84*s}" y="{yy}" font-size="{20*s}" fill="{INK}">{E(t)}</text>'
    return g
def none(x, y, s=1): return ''

ICONS = {k: v for k, v in globals().items() if callable(v) and k not in ("stroke", "E", "hoodie")}

# ---------- text helpers ----------
def fit(text, width, maxsize, bold=True, upper=True):
    k = 0.64 if (bold and upper) else (0.56 if bold else 0.5)
    return int(min(maxsize, width / max(1, len(text)*k)))
def textblock(lines, x, y, width, maxsize, gap=1.12):
    out = ''; yy = y
    for ln in lines:
        fs = fit(ln, width, maxsize)
        out += f'<text x="{x}" y="{yy+fs}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="{INK}" letter-spacing="1">{E(ln)}</text>'
        yy += fs*gap
    return out, yy
def sub(t, x, y, width, maxsize=15):
    if not t: return '', y
    fs = fit(t, width, maxsize, bold=False, upper=False)
    return f'<text x="{x}" y="{y+fs+4}" text-anchor="middle" font-size="{fs}" fill="{INK}">{E(t)}</text>', y+fs+8

def icon(name, x, y, s, args):
    return ICONS[name](x, y, s, **args)

def layout(d):
    lines, subl, ic, place = d["lines"], d.get("sub", ""), d.get("icon", "none"), d["place"]
    args = d.get("args", {})
    view = "back" if place in ("back", "hood") else "front"
    art = ''
    if place == "front":
        if ic != "none":
            art += icon(ic, 300, 262, d.get("s", 0.85)*0.82, args)
            ms = min(34, int(82/(len(lines)*1.12)) if len(lines) > 2 else 34)
            t, yy = textblock(lines, 300, 345, 290, ms)
        else:
            t, yy = textblock(lines, 300, 258, 290, min(46, int(160/(len(lines)*1.12))))
        art += t
        s_, _ = sub(subl, 300, yy, 300); art += s_
    elif place == "back":
        t, yy = textblock(lines, 300, 200, 300, 50); art += t
        s_, yy = sub(subl, 300, yy, 310, 16); art += s_
        if ic != "none": art += icon(ic, 300, max(yy+80, 420), d.get("s", 0.8), args)
    elif place == "hood":
        art += f'<text x="300" y="133" text-anchor="middle" font-size="{fit(d["hood"], 90, 13)}" font-weight="bold" fill="{FAB}">{E(d["hood"])}</text>'
        art = f'<path d="M246 122 Q300 100 354 122 L354 140 Q300 122 246 140 Z" fill="{INK}"/>' + art
        t, yy = textblock(lines, 300, 220, 300, 44); art += t
        s_, yy = sub(subl, 300, yy, 310, 16); art += s_
        if ic != "none": art += icon(ic, 300, max(yy+75, 430), d.get("s", 0.7), args)
    elif place == "chest":
        cx = 382
        if ic != "none": art += icon(ic, cx, 232, d.get("s", 0.4), args)
        t, yy = textblock(lines, cx, 262 if ic != "none" else 220, 120, 18); art += t
        s_, _ = sub(subl, cx, yy, 130, 10); art += s_
    elif place == "sleeve":
        txt = " ".join(lines)
        fs = fit(txt, 270, 17)
        art += f'<text transform="translate(138 205) rotate(105.6)" font-size="{fs}" font-weight="bold" fill="{INK}">{E(txt)}</text>'
        if subl:
            art += f'<text transform="translate(462 205) rotate(74.4)" font-size="{fit(subl, 270, 13, bold=False, upper=False)}" fill="{INK}">{E(subl)}</text>'
        if ic != "none": art += icon(ic, 300, 260, d.get("s", 0.45), args)
    elif place == "pocket":
        if ic != "none": art += icon(ic, 382, 240, d.get("s", 0.4), args)
        t, yy = textblock(lines, 300, 440, 200, 26); art += t
        s_, _ = sub(subl, 300, yy, 220, 12); art += s_
    return view, art

PLACE = {"front": "front center", "back": "back", "chest": "left chest", "sleeve": "sleeve", "pocket": "pocket + chest", "hood": "hood + back"}
def svg(num, d):
    view, art = layout(d)
    full = " ".join(d["lines"]).strip()
    title = full if len(full) <= 38 else full[:36].rsplit(" ", 1)[0] + "…"
    title = title[0] + title[1:].lower()
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 720" width="600" height="720" font-family="Arial, Helvetica, sans-serif">
<rect width="600" height="720" fill="#ffffff"/>
{hoodie(view)}
{art}
<text x="300" y="640" text-anchor="middle" font-size="17" font-weight="bold" fill="#222">{num:02d}. {E(title)} ({PLACE[d["place"]]})</text>
<text x="300" y="668" text-anchor="middle" font-size="13" fill="#555">{E(d["note"])}</text>
<text x="300" y="700" text-anchor="middle" font-size="11" fill="#999">Placement sketch only. Redraw in your own hand before use.</text>
</svg>'''
    name = f"{num:03d}-{d['slug']}.svg" if num >= 100 else f"{num:02d}-{d['slug']}.svg"
    open(os.path.join(OUT, name), "w").write(s)
    return name

if __name__ == "__main__":
    from designs_data import DESIGNS
    names = [svg(8+i, d) for i, d in enumerate(DESIGNS)]
    print(len(names), names[0], names[-1])

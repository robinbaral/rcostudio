# Pencil sketches of what Puzzle Studio does, in the style of the ProLog logo drafts:
# graph paper, wobbly dark outlines drawn twice, diagonal hatching. Abstract on purpose:
# what the tool handles, not how the system is set up.
# Usage: python3 crisscross-sketches.py out.svg [cols]   (4 columns for the page, 2 for phones)
import random, math, sys
random.seed(7)
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
W, H = 360 * COLS, 300 * (8 // COLS)
INK = "#3a3a3a"
out = []
def wob(pts, closed=False, j=1.1):
    s = ""
    for k in range(2):
        q = [(x + random.uniform(-j, j), y + random.uniform(-j, j)) for x, y in pts]
        if closed: q.append(q[0])
        s += f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x,y in q)}" fill="none" stroke="{INK}" stroke-width="{1.5 if k==0 else 1.0}" stroke-linejoin="round" stroke-linecap="round" opacity="{0.9 if k==0 else 0.6}"/>'
    return s
def seg(a, b, n=None):
    n = n or max(2, int(math.dist(a, b) / 10))
    return [(a[0] + (b[0]-a[0])*i/n, a[1] + (b[1]-a[1])*i/n) for i in range(n+1)]
def rrect(x, y, w, h, r=6, hatch=False, fill=None):
    pts = []
    corners = [(x+w-r, y+r, -90), (x+w-r, y+h-r, 0), (x+r, y+h-r, 90), (x+r, y+r, 180)]
    pts += seg((x+r, y), (x+w-r, y))
    for i, (cx, cy, a0) in enumerate(corners):
        pts += [(cx + r*math.cos(math.radians(a0+t*15)), cy + r*math.sin(math.radians(a0+t*15))) for t in range(7)]
        nxt = [((x+w, y+r), (x+w, y+h-r)), ((x+w-r, y+h), (x+r, y+h)), ((x, y+h-r), (x, y+r)), None][i]
        if nxt: pts += seg(*nxt)
    s = ""
    if hatch: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#hatch)"/>'
    if fill: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
    return s + wob(pts, closed=True)
def line(a, b): return wob(seg(a, b))
def circle(cx, cy, r, hatch=False):
    pts = [(cx + r*math.cos(t/24*2*math.pi), cy + r*math.sin(t/24*2*math.pi)) for t in range(24)]
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#hatch)"/>' if hatch else ""
    return s + wob(pts, closed=True)
def text(x, y, t, size=15, anchor="middle", w=600):
    return f'<text x="{x}" y="{y}" font-family="Bradley Hand, Marker Felt, Comic Sans MS, cursive" font-size="{size}" font-weight="{w}" fill="{INK}" text-anchor="{anchor}">{t}</text>'
def tile(x, y, s, ch="", hatch=False):
    return rrect(x, y, s, s, 4, hatch) + (text(x+s/2, y+s*0.7, ch, s*0.55) if ch else "")

cells = []
# 1 · Word list: word, clue, status dot
def words(ox, oy):
    s = rrect(ox, oy, 230, 200, 10)
    for i, (w, c) in enumerate([(70, 110), (54, 128), (82, 96), (60, 118), (74, 104)]):
        y = oy + 26 + i*34
        s += rrect(ox+16, y, w, 18, 9, hatch=True) + line((ox+w+30, y+9), (ox+w+30+c*0.9, y+9))
        s += circle(ox+212, y+9, 4, hatch=(i % 2 == 0))
    return s
# 2 · Grid generation
def grid(ox, oy):
    s = ""; n = 7; t = 27
    fill = {(1,1),(1,2),(1,3),(1,4),(1,5),(0,3),(2,3),(3,3),(4,3),(3,0),(3,1),(3,2),(5,1),(5,2),(5,3),(5,4),(3,5),(4,5),(5,5)}
    for r in range(n):
        for c in range(n):
            if (r, c) in fill: s += rrect(ox+c*(t+4), oy+r*(t+4), t, t, 4, hatch=True)
    return s + rrect(ox-10, oy-10, n*(t+4)+16, n*(t+4)+16, 10)
# 3 · Two spellings
def locales(ox, oy):
    s = ""
    for i, ch in enumerate("COLOUR"): s += tile(ox + i*36, oy+20, 30, ch, hatch=(ch=="U"))
    for i, ch in enumerate("COLOR"): s += tile(ox + 18 + i*36, oy+100, 30, ch)
    s += text(ox-30, oy+42, "GB", 14) + text(ox-30, oy+122, "US", 14)
    return s + line((ox+100, oy+62), (ox+100, oy+88)) + line((ox+94, oy+80), (ox+100, oy+90)) + line((ox+106, oy+80), (ox+100, oy+90))
# 4 · Audio with IPA
def audio(ox, oy):
    s = rrect(ox, oy+40, 34, 40, 6, hatch=True) + wob([(ox+34, oy+40), (ox+62, oy+18), (ox+62, oy+102), (ox+34, oy+80)])
    for i, h in enumerate([16, 34, 52, 26, 60, 40, 22, 46, 30, 14, 24, 10]):
        x = ox + 86 + i*11; s += line((x, oy+60-h/2), (x, oy+60+h/2))
    return s + text(ox+130, oy+150, "/təˈmɑːtəʊ/", 22, w=700)
# 5 · Flashcards
def flash(ox, oy):
    s = rrect(ox+30, oy, 170, 110, 10, hatch=True) + rrect(ox, oy+30, 170, 110, 10, fill="#f3f2ee")
    s += line((ox+30, oy+70), (ox+140, oy+70)) + line((ox+30, oy+92), (ox+110, oy+92))
    s += circle(ox+40, oy+170, 16) + wob([(ox+32, oy+170), (ox+38, oy+177), (ox+49, oy+163)])
    s += circle(ox+130, oy+170, 16) + line((ox+123, oy+163), (ox+137, oy+177)) + line((ox+137, oy+163), (ox+123, oy+177))
    return s
# 6 · Flags from players
def flags(ox, oy):
    s = rrect(ox, oy+70, 210, 70, 10) + rrect(ox+16, oy+92, 60, 26, 13, hatch=True) + line((ox+90, oy+105), (ox+190, oy+105))
    s += line((ox+150, oy), (ox+150, oy+66)) + wob([(ox+150, oy+2), (ox+196, oy+14), (ox+150, oy+30)], closed=True)
    s += f'<path d="M{ox+150},{oy+4} L{ox+194},{oy+15} L{ox+150},{oy+28} Z" fill="url(#hatch)"/>'
    return s
# 7 · Versions and backups
def versions(ox, oy):
    s = ""
    for i in range(3):
        y = oy + 110 - i*52
        s += wob([(ox, y+20), (ox+100, y), (ox+200, y+20), (ox+100, y+40)], closed=True)
        if i == 2: s += f'<path d="M{ox},{y+20} L{ox+100},{y} L{ox+200},{y+20} L{ox+100},{y+40} Z" fill="url(#hatch)"/>'
    for i, v in enumerate(["1.0", "1.1", "1.2"]): s += text(ox+226, oy+136 - i*52, v, 15, "start")
    return s
# 8 · Into the app
def push(ox, oy):
    s = rrect(ox, oy, 110, 200, 18) + rrect(ox+10, oy+14, 90, 172, 10)
    for r in range(4):
        for c in range(4):
            if (r+c) % 3 != 1: s += rrect(ox+20+c*19, oy+50+r*19, 15, 15, 3, hatch=(r==1))
    for i in range(4): s += rrect(ox+20+i*19, oy+150, 15, 15, 3)
    return s
fns = [words, grid, locales, audio, flash, flags, versions, push]
COLW = W / COLS
g = ""
for i, f in enumerate(fns):
    cx = (i % COLS) * COLW + COLW/2; cy = 150 + (i // COLS) * 300
    boxes = {words:(230,200), grid:(220,220), locales:(250,140), audio:(220,160), flash:(200,190), flags:(210,200), versions:(250,140), push:(110,200)}
    bw, bh = boxes[f]
    g += f(cx - bw/2 + (20 if f is locales else 0), cy - bh/2)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#dcdad4" stroke-width="1"/></pattern>
<pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" stroke="#6d6d6d" stroke-width="0.8" opacity="0.55"/></pattern>
<filter id="pencil"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="1.6"/></filter>
</defs>
<rect width="100%" height="100%" fill="#f2f1ee"/><rect width="100%" height="100%" fill="url(#grid)"/>
<g filter="url(#pencil)">{g}</g></svg>'''
open(sys.argv[1], "w").write(svg)

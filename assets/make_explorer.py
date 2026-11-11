"""Generates assets/explorer.svg: an XP-style Explorer window listing projects as folders.
Edit FOLDERS below and run:  python assets/make_explorer.py
"""
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

PATH = "C:\\Users\\Lucas\\Documents"
FOLDERS = [  # (name, type line, description)
    ("shelflife", "File Folder  ·  Python  ·  MIT License",
     "A local recommender: logs what you rate and how much you use it, then suggests what to try next."),
    ("Moonkey-Game", "File Folder  ·  C#  ·  Unity  ·  GPL-3.0",
     "Computer Graphics project at UNESP, themed on the UN goals for life on land, life below water and climate action."),
]

W = 900
X0, Y0 = 10, 10                     # window origin
TITLE_H, MENU_H, TOOL_H, ADDR_H, STATUS_H = 30, 22, 40, 28, 22
TILE_H = 78
CONTENT_H = max(196, 24 + TILE_H * len(FOLDERS))
H = Y0 + TITLE_H + MENU_H + TOOL_H + ADDR_H + CONTENT_H + STATUS_H + 14
PANE_W = 210
UI = "Tahoma, Verdana, 'Segoe UI', sans-serif"


def folder(x, y, s=1.0):
    """XP-style yellow folder, ~48px wide at s=1."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M2 6 H18 L22 10 H46 V40 H2 Z" fill="#e3ad3b" stroke="#b07d1c"/>'
            f'<path d="M0 15 H48 L44 42 H4 Z" fill="url(#fold)" stroke="#c08a1e"/>'
            f'<path d="M2 17 H45" stroke="#fff7d6" stroke-width="1.5" opacity=".8"/></g>')


def green_btn(cx, cy, direction, faded=False):
    arrow = "M5 0 H-4 M-1 -4 L-5 0 L-1 4" if direction == "left" else "M-5 0 H4 M1 -4 L5 0 L1 4"
    return (f'<g transform="translate({cx} {cy})" opacity="{0.45 if faded else 1}">'
            f'<circle r="12" fill="url(#go)" stroke="#2c7a2c"/>'
            f'<path d="{arrow}" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')


def task_box(x, y, w, title, items):
    h = 26 + 19 * len(items) + 8
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#d6dff7"/>',
           f'<path d="M{x} {y+24} V{y+4} Q{x} {y} {x+4} {y} H{x+w-4} Q{x+w} {y} {x+w} {y+4} V{y+24} Z" fill="url(#taskhdr)"/>',
           f'<text x="{x+10}" y="{y+16}" class="ui b" fill="#215dc6">{escape(title)}</text>',
           f'<circle cx="{x+w-14}" cy="{y+12}" r="8" fill="#fff" stroke="#a8b8e8"/>',
           f'<path d="M{x+w-18} {y+14} l4 -4 l4 4 M{x+w-18} {y+10} l4 -4 l4 4" stroke="#215dc6" stroke-width="1.4" fill="none" transform="translate(0 1)"/>']
    for i, (icon, label) in enumerate(items):
        ty = y + 42 + i * 19
        out.append(f'<text x="{x+10}" y="{ty}" class="ui">{icon}</text>'
                   f'<text x="{x+30}" y="{ty}" class="ui" fill="#215dc6">{escape(label)}</text>')
    return "".join(out), h


def render():
    yt = Y0 + TITLE_H
    ym = yt + MENU_H
    ya = ym + TOOL_H
    yc = ya + ADDR_H
    ys = yc + CONTENT_H
    R = X0 + W - 20  # window right edge

    p = []
    # frame + title bar
    p.append(f'<rect x="{X0}" y="{Y0}" width="{W-20}" height="{H-20}" rx="8" fill="#0831d9"/>')
    p.append(f'<path d="M{X0} {yt} V{Y0+8} Q{X0} {Y0} {X0+8} {Y0} H{R-8} Q{R} {Y0} {R} {Y0+8} V{yt} Z" fill="url(#titlebar)"/>')
    p.append(folder(X0 + 8, Y0 + 6, 0.38))
    p.append(f'<text x="{X0+32}" y="{Y0+20}" class="title">Documents</text>')
    p.append(f'''<g stroke="#fff" stroke-width="1.2">
    <rect x="{R-74}" y="{Y0+5}" width="21" height="21" rx="3" fill="url(#tb)"/>
    <rect x="{R-51}" y="{Y0+5}" width="21" height="21" rx="3" fill="url(#tb)"/>
    <rect x="{R-28}" y="{Y0+5}" width="21" height="21" rx="3" fill="url(#close)"/></g>
  <rect x="{R-69}" y="{Y0+18}" width="8" height="3" fill="#fff"/>
  <rect x="{R-46}" y="{Y0+10}" width="11" height="11" fill="none" stroke="#fff" stroke-width="2"/>
  <path d="M{R-23} {Y0+10} l11 11 M{R-12} {Y0+10} l-11 11" stroke="#fff" stroke-width="2.4"/>''')

    # menu bar, toolbar, address bar (beige chrome)
    p.append(f'<rect x="{X0+4}" y="{yt}" width="{W-28}" height="{MENU_H+TOOL_H+ADDR_H}" fill="#ece9d8"/>')
    p.append(f'<text x="{X0+12}" y="{yt+15}" class="ui" style="white-space:pre">File    Edit    View    Favorites    Tools    Help</text>')
    p.append(f'<rect x="{X0+4}" y="{ym}" width="{W-28}" height="1" fill="#d8d2bd"/><rect x="{X0+4}" y="{ym+1}" width="{W-28}" height="1" fill="#fff"/>')
    cy = ym + TOOL_H / 2
    p.append(green_btn(X0 + 28, cy, "left"))
    p.append(f'<text x="{X0+46}" y="{cy+4}" class="ui">Back</text><path d="M{X0+80} {cy-1} l3 3 l3 -3" fill="#000"/>')
    p.append(green_btn(X0 + 106, cy, "right", faded=True))
    p.append(f'<path d="M{X0+124} {cy-1} l3 3 l3 -3" fill="#000" opacity=".45"/>')
    p.append(folder(X0 + 142, cy - 10, 0.42))
    p.append(f'<path d="M{X0+152} {cy+6} V{cy-6} M{X0+147} {cy-1} L{X0+152} {cy-7} L{X0+157} {cy-1}" stroke="#2a8a2a" stroke-width="2.4" fill="none"/>')
    p.append(f'<rect x="{X0+176}" y="{ym+7}" width="1" height="{TOOL_H-14}" fill="#c5c2b2"/>')
    p.append(f'<circle cx="{X0+196}" cy="{cy-2}" r="6" fill="#dbe9ff" stroke="#3a6fc4" stroke-width="2"/>'
             f'<path d="M{X0+200} {cy+2} l6 6" stroke="#7a5a2a" stroke-width="3" stroke-linecap="round"/>')
    p.append(f'<text x="{X0+212}" y="{cy+4}" class="ui">Search</text>')
    p.append(folder(X0 + 262, cy - 10, 0.42))
    p.append(f'<text x="{X0+286}" y="{cy+4}" class="ui">Folders</text>')
    p.append(f'<rect x="{X0+336}" y="{ym+7}" width="1" height="{TOOL_H-14}" fill="#c5c2b2"/>')
    p.append("".join(f'<rect x="{X0+348 + (i%2)*7}" y="{cy-7 + (i//2)*7}" width="5" height="5" fill="#3a6fc4"/>' for i in range(4)))
    p.append(f'<path d="M{X0+366} {cy-1} l3 3 l3 -3" fill="#000"/>')
    p.append(f'<rect x="{X0+4}" y="{ya}" width="{W-28}" height="1" fill="#d8d2bd"/><rect x="{X0+4}" y="{ya+1}" width="{W-28}" height="1" fill="#fff"/>')
    p.append(f'<text x="{X0+12}" y="{ya+18}" class="ui" fill="#5a5a5a">Address</text>')
    p.append(f'<rect x="{X0+64}" y="{ya+4}" width="{W-160}" height="20" fill="#fff" stroke="#7f9db9"/>')
    p.append(folder(X0 + 69, ya + 6, 0.32))
    p.append(f'<text x="{X0+90}" y="{ya+18}" class="ui">{escape(PATH)}</text>')
    p.append(f'<rect x="{X0+W-117}" y="{ya+4}" width="18" height="20" fill="url(#hdr)" stroke="#7f9db9"/>'
             f'<path d="M{X0+W-112} {ya+12} l4 4 l4 -4" fill="#4d6185"/>')
    p.append(f'<circle cx="{X0+W-84}" cy="{ya+14}" r="9" fill="url(#go)" stroke="#2c7a2c"/>'
             f'<path d="M{X0+W-88} {ya+14} H{X0+W-80} M{X0+W-83} {ya+10} L{X0+W-79} {ya+14} L{X0+W-83} {ya+18}" stroke="#fff" stroke-width="2" fill="none"/>'
             f'<text x="{X0+W-70}" y="{ya+18}" class="ui">Go</text>')

    # left task pane
    p.append(f'<rect x="{X0+4}" y="{yc}" width="{PANE_W}" height="{CONTENT_H}" fill="url(#pane)"/>')
    box, h1 = task_box(X0 + 16, yc + 12, PANE_W - 24, "File and Folder Tasks",
                       [("📁", "Make a new folder"), ("🌐", "Publish this folder"), ("🤝", "Share this folder")])
    p.append(box)
    box, _ = task_box(X0 + 16, yc + 24 + h1, PANE_W - 24, "Other Places",
                      [("🖥️", "My Computer"), ("🌐", "My Network")])
    p.append(box)

    # main pane: tiles view
    mx = X0 + 4 + PANE_W
    p.append(f'<rect x="{mx}" y="{yc}" width="{R - 4 - mx}" height="{CONTENT_H}" fill="#fff"/>')
    for i, (name, kind, desc) in enumerate(FOLDERS):
        ty = yc + 16 + i * TILE_H
        p.append(folder(mx + 20, ty + 4, 1.0))
        tx = mx + 84
        p.append(f'<text x="{tx}" y="{ty+15}" class="ui b" fill="#000">{escape(name)}</text>')
        for j, line in enumerate(textwrap.wrap(desc, max(50, len(desc) // 2 + 8))):
            p.append(f'<text x="{tx}" y="{ty+33 + j*15}" class="ui">{escape(line)}</text>')
        p.append(f'<text x="{tx}" y="{ty+33 + 2*15}" class="ui" fill="#808080">{escape(kind)}</text>')

    # status bar
    p.append(f'<rect x="{X0+4}" y="{ys}" width="{W-28}" height="{STATUS_H}" fill="#ece9d8"/>'
             f'<rect x="{X0+4}" y="{ys}" width="{W-28}" height="1" fill="#c5c2b2"/>')
    p.append(f'<text x="{X0+12}" y="{ys+15}" class="ui">{len(FOLDERS)} objects</text>')
    p.append(f'<rect x="{R-170}" y="{ys+3}" width="1" height="{STATUS_H-6}" fill="#c5c2b2"/>')
    p.append(f'<text x="{R-160}" y="{ys+15}" class="ui">🖥️  My Computer</text>')

    body = "\n  ".join(p)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .ui {{ font-family: {UI}; font-size: 12px; }}
    .b {{ font-weight: bold; }}
    .title {{ font-family: 'Trebuchet MS', Tahoma, sans-serif; font-size: 14px; font-weight: bold; fill: #fff; }}
  </style>
  <defs>
    <linearGradient id="titlebar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0a5fe8"/><stop offset=".12" stop-color="#3d95ff"/><stop offset=".35" stop-color="#0b5fe6"/>
      <stop offset=".9" stop-color="#0052d9"/><stop offset="1" stop-color="#003fb0"/>
    </linearGradient>
    <linearGradient id="close" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e87a5a"/><stop offset="1" stop-color="#c2350f"/></linearGradient>
    <linearGradient id="tb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f93ff"/><stop offset="1" stop-color="#0a4fd0"/></linearGradient>
    <linearGradient id="go" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fd77a"/><stop offset="1" stop-color="#2a9a2a"/></linearGradient>
    <linearGradient id="fold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset="1" stop-color="#f3bf3f"/></linearGradient>
    <linearGradient id="hdr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdfdfd"/><stop offset="1" stop-color="#d9e4f8"/></linearGradient>
    <linearGradient id="pane" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ba2e7"/><stop offset="1" stop-color="#6375d6"/></linearGradient>
    <linearGradient id="taskhdr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c6d3f7"/></linearGradient>
  </defs>
  {body}
</svg>
'''


# The window is cut into horizontal strips (top, one per folder, bottom) so each folder
# can be its own link in the README. Every strip draws the full window and just crops it.
full = render()
head = f'width="{W}" height="{H}" viewBox="0 0 {W} {H}"'
yc = Y0 + TITLE_H + MENU_H + TOOL_H + ADDR_H
cuts = [0, yc + 10] + [yc + 10 + (i + 1) * TILE_H for i in range(len(FOLDERS))] + [H]
names = ["top"] + [n for n, _, _ in FOLDERS] + ["bottom"]
outdir = Path(__file__).with_name("explorer")
outdir.mkdir(exist_ok=True)
for old in outdir.glob("*.svg"):
    old.unlink()
for name, a, b in zip(names, cuts, cuts[1:]):
    svg = full.replace(head, f'width="{W}" height="{b-a}" viewBox="0 {a} {W} {b-a}"', 1)
    (outdir / f"{name}.svg").write_text(svg, encoding="utf-8")
print("wrote", len(names), "strips to", outdir)

# README snippet (paste between the Documents heading and the next section)
user = "Antonetti-Lucas"
for name in names:
    url = f"https://github.com/{user}/{name}" if name not in ("top", "bottom") else f"https://github.com/{user}?tab=repositories"
    print(f'<a href="{url}"><img align="left" width="100%" src="assets/explorer/{name}.svg" alt="{name}"/></a>')
print('<br clear="both"/>')

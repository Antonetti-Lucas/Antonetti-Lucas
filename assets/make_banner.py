"""Generates assets/banner.svg: an old-school XP-style command prompt window.
Edit INFO below and run:  python assets/make_banner.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

INFO = [  # (key, value) shown next to the logo
    ("OS", "Computer Science @ UNESP Bauru"),
    ("Shell", "Python, C#"),
    ("Interests", "AI, recommender systems, data"),
    ("Working on", "shelflife, a Python recommender"),
    ("Uptime", "on GitHub since 2023"),
]
LOGO = [
    "██╗      █████╗ ",
    "██║     ██╔══██╗",
    "██║     ███████║",
    "██║     ██╔══██║",
    "███████╗██║  ██║",
    "╚══════╝╚═╝  ╚═╝",
]
CONSOLE = ["#0c0c0c", "#c50f1f", "#13a10e", "#c19c00", "#0037da", "#881798", "#3a96dd", "#cccccc",
           "#767676", "#e74856", "#16c60c", "#f9f1a5", "#3b78ff", "#b4009e", "#61d6d6", "#f2f2f2"]

W, H = 900, 380
WX, WY, WW, WH = 40, 14, 820, 322         # window
MONO = "'Lucida Console', Consolas, ui-monospace, Menlo, monospace"
UI = "'Trebuchet MS', Tahoma, Verdana, sans-serif"


def t(x, y, s, cls="", begin=None, extra=""):
    anim = (f'<set attributeName="opacity" to="1" begin="{begin:.2f}s" fill="freeze"/>' if begin is not None else "")
    op = ' opacity="0"' if begin is not None else ""
    return f'<text x="{x}" y="{y}" class="{cls}"{op}{extra}>{escape(s)}{anim}</text>'


parts = []
cx, y = WX + 16, WY + 52
parts.append(t(cx, y, "Lucas Antonetti [Version 2026.11]", "dim"))
parts.append(t(cx, y + 18, "(C) Copyright 2023-2026 Lucas Antonetti. All rights reserved.", "dim"))

# typed command
py = y + 50
parts.append(t(cx, py, "C:\\Users\\Lucas>", "fg"))
cmd_x = cx + 15 * 8
parts.append(f'''<clipPath id="typed"><rect x="{cmd_x}" y="{py-14}" height="20" width="0">
    <animate attributeName="width" from="0" to="120" begin="0.4s" dur="0.9s" fill="freeze" calcMode="discrete"
      values="0;8;16;24;32;40;48;56;64;72;80;88;96" keyTimes="0;.08;.16;.24;.32;.4;.48;.56;.64;.72;.8;.88;1"/></rect></clipPath>
  <text x="{cmd_x}" y="{py}" class="fg" clip-path="url(#typed)">whoami /all</text>''')

# logo + info appear after the command "runs"
t0 = 1.6
ly = py + 30
CW, CH = 10, 17  # logo cell size; blocks become rects, box-drawing chars become thin "shadow" lines
SEG = {"═": ["l", "r"], "║": ["u", "d"], "╗": ["l", "d"], "╔": ["r", "d"], "╚": ["r", "u"], "╝": ["l", "u"]}
for i, row in enumerate(LOGO):
    x0, y0, g = cx + 8, ly - 13 + i * CH, []
    for j, ch in enumerate(row):
        x, yy = x0 + j * CW, y0
        mx, my = x + CW / 2, yy + CH / 2
        if ch == "█":
            g.append(f'<rect x="{x}" y="{yy}" width="{CW+0.5}" height="{CH+0.5}" fill="#3b78ff"/>')
        for s in SEG.get(ch, []):
            x1, y1, x2, y2 = {"l": (x, my, mx, my), "r": (mx, my, x + CW, my),
                              "u": (mx, yy, mx, my), "d": (mx, my, mx, yy + CH)}[s]
            g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1f4fb0" stroke-width="2"/>')
    parts.append(f'<g opacity="0">{"".join(g)}<set attributeName="opacity" to="1" begin="{t0 + i*0.06:.2f}s" fill="freeze"/></g>')
ix = cx + 210
parts.append(t(ix, ly, "lucas@ANTONETTI-PC", "user", t0 + 0.4))
parts.append(t(ix, ly + 19, "-" * 18, "dim", t0 + 0.45))
for i, (k, v) in enumerate(INFO):
    parts.append(f'<text x="{ix}" y="{ly + 38 + i*19}" opacity="0"><tspan class="key">{escape(k)}:</tspan>'
                 f'<tspan class="fg" x="{ix + 105}">{escape(v)}</tspan>'
                 f'<set attributeName="opacity" to="1" begin="{t0 + 0.55 + i*0.12:.2f}s" fill="freeze"/></text>')
by = ly + 38 + len(INFO) * 19 - 6
blocks = "".join(f'<rect x="{ix + (i % 8)*22}" y="{by + (i//8)*12}" width="22" height="12" fill="{c}"/>'
                 for i, c in enumerate(CONSOLE))
parts.append(f'<g opacity="0">{blocks}<set attributeName="opacity" to="1" begin="{t0+1.3:.2f}s" fill="freeze"/></g>')

# final prompt with blinking cursor
fy = WY + WH - 16
parts.append(t(cx, fy, "C:\\Users\\Lucas>", "fg", t0 + 1.5))
parts.append(f'<rect x="{cmd_x}" y="{fy-2}" width="9" height="3" fill="#cccccc" opacity="0" class="cursor">'
             f'<set attributeName="opacity" to="1" begin="{t0+1.5:.2f}s" fill="freeze"/></rect>')
console = "\n  ".join(parts)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font-family: {MONO}; font-size: 13px; white-space: pre; }}
    .fg {{ fill: #cccccc; }} .dim {{ fill: #8a8a8a; }} .key {{ fill: #61d6d6; font-weight: bold; }}
    .user {{ fill: #f9f1a5; font-weight: bold; }}
    .logo {{ fill: #3b78ff; font-size: 16px; }}
    .title {{ font-family: {UI}; font-size: 14px; font-weight: bold; fill: #fff; }}
    .ui {{ font-family: {UI}; fill: #fff; }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ visibility: hidden; }} }}
  </style>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2c6fd6"/><stop offset=".7" stop-color="#7fb6f2"/><stop offset="1" stop-color="#b9dbff"/>
    </linearGradient>
    <linearGradient id="hill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5fb83a"/><stop offset="1" stop-color="#2d7a1e"/>
    </linearGradient>
    <linearGradient id="titlebar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0a5fe8"/><stop offset=".12" stop-color="#3d95ff"/><stop offset=".35" stop-color="#0b5fe6"/>
      <stop offset=".9" stop-color="#0052d9"/><stop offset="1" stop-color="#003fb0"/>
    </linearGradient>
    <linearGradient id="taskbar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3a8af0"/><stop offset=".1" stop-color="#2463d8"/><stop offset="1" stop-color="#1c4fbf"/>
    </linearGradient>
    <linearGradient id="start" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5dbb57"/><stop offset=".5" stop-color="#3a9a32"/><stop offset="1" stop-color="#2e7d27"/>
    </linearGradient>
    <linearGradient id="close" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#e87a5a"/><stop offset="1" stop-color="#c2350f"/>
    </linearGradient>
    <linearGradient id="btn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4f93ff"/><stop offset="1" stop-color="#0a4fd0"/>
    </linearGradient>
    <clipPath id="screen"><rect width="{W}" height="{H}" rx="12"/></clipPath>
  </defs>

  <g clip-path="url(#screen)">
  <!-- wallpaper -->
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <ellipse cx="160" cy="70" rx="90" ry="18" fill="#fff" opacity=".35"/>
  <ellipse cx="720" cy="110" rx="120" ry="20" fill="#fff" opacity=".3"/>
  <path d="M0 300 C 200 210, 420 220, 600 270 S 860 250, 900 230 L 900 {H} L 0 {H} Z" fill="url(#hill)"/>

  <!-- window -->
  <rect x="{WX-1}" y="{WY+4}" width="{WW+2}" height="{WH}" rx="8" fill="#000" opacity=".25"/>
  <rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="8" fill="#0831d9"/>
  <path d="M{WX} {WY+30} V{WY+8} Q{WX} {WY} {WX+8} {WY} H{WX+WW-8} Q{WX+WW} {WY} {WX+WW} {WY+8} V{WY+30} Z" fill="url(#titlebar)"/>
  <rect x="{WX+8}" y="{WY+7}" width="17" height="15" rx="2" fill="#000" stroke="#c0c0c0" stroke-width="1"/>
  <text x="{WX+10}" y="{WY+19}" style="font-size:9px;fill:#c0c0c0">C:\\</text>
  <text x="{WX+32}" y="{WY+20}" class="title">C:\\WINDOWS\\system32\\cmd.exe</text>
  <g stroke="#fff" stroke-width="1.2">
    <rect x="{WX+WW-74}" y="{WY+5}" width="21" height="21" rx="3" fill="url(#btn)"/>
    <rect x="{WX+WW-51}" y="{WY+5}" width="21" height="21" rx="3" fill="url(#btn)"/>
    <rect x="{WX+WW-28}" y="{WY+5}" width="21" height="21" rx="3" fill="url(#close)"/>
  </g>
  <rect x="{WX+WW-69}" y="{WY+18}" width="8" height="3" fill="#fff"/>
  <rect x="{WX+WW-46}" y="{WY+10}" width="11" height="11" fill="none" stroke="#fff" stroke-width="2"/>
  <path d="M{WX+WW-23} {WY+10} l11 11 M{WX+WW-12} {WY+10} l-11 11" stroke="#fff" stroke-width="2.4"/>
  <rect x="{WX+4}" y="{WY+30}" width="{WW-8}" height="{WH-34}" fill="#0c0c0c"/>
  {console}

  <!-- taskbar -->
  <rect x="0" y="{H-34}" width="{W}" height="34" fill="url(#taskbar)"/>
  <path d="M0 {H-34} H96 Q112 {H-34} 112 {H-17} Q112 {H} 96 {H} H0 Z" fill="url(#start)"/>
  <circle cx="22" cy="{H-17}" r="8" fill="#fff" opacity=".9"/>
  <circle cx="22" cy="{H-17}" r="5" fill="#3a9a32"/>
  <text x="38" y="{H-11}" class="ui" style="font-size:18px;font-weight:bold;font-style:italic">start</text>
  <rect x="124" y="{H-30}" width="180" height="26" rx="3" fill="#1e52b7" stroke="#14408f"/>
  <rect x="132" y="{H-24}" width="14" height="13" rx="1" fill="#000" stroke="#c0c0c0"/>
  <text x="154" y="{H-12}" class="ui" style="font-size:12px">C:\\WINDOWS\\system32\\cmd...</text>
  <rect x="{W-110}" y="{H-34}" width="110" height="34" fill="#0f8ff0" opacity=".55"/>
  <rect x="{W-110}" y="{H-34}" width="1" height="34" fill="#0b5dcf"/>
  <text x="{W-55}" y="{H-12}" text-anchor="middle" class="ui" style="font-size:12px">BAURU, SP</text>
  </g>
</svg>
'''
out = Path(__file__).with_name("banner.svg")
out.write_text(svg, encoding="utf-8")
print("wrote", out)

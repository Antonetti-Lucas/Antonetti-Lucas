"""Draws your GitHub contribution calendar as an XP-style Disk Defragmenter window.

  "before" bar: every day of the last year, left to right
  "after"  bar: the same days "defragmented" (packed together by type), animated

Usage:
  GITHUB_TOKEN=... python scripts/defrag.py <github-user> dist/defrag.svg
  python scripts/defrag.py --sample dist/defrag.svg      # fake data, for previewing
Standard library only.
"""
import json
import os
import random
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""

# category: (colour, legend label)
CATS = {
    "best": ("#00b000", "Unmovable: top 5% busiest days"),
    "busy": ("#2050e0", "Contiguous: busy days"),
    "light": ("#e02020", "Fragmented: light days"),
    "free": ("#ffffff", "Free space: days off"),
}
ORDER = ["best", "busy", "light", "free"]


def fetch(login):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req))
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]


def sample():
    rnd, start = random.Random(7), date.today() - timedelta(days=364)
    return [((start + timedelta(i)).isoformat(),
             0 if rnd.random() < 0.55 else int(rnd.expovariate(0.25)) + 1) for i in range(365)]


def classify(days):
    counts = sorted(c for _, c in days if c > 0)
    if not counts:
        return ["free"] * len(days)
    med = counts[len(counts) // 2]
    top = counts[int(len(counts) * 0.95)] if len(counts) >= 20 else counts[-1]
    return ["free" if c == 0 else "best" if c >= top else "busy" if c > med else "light" for _, c in days]


def runs(cats):
    """Merge neighbouring days of the same category into (category, start, length)."""
    out = []
    for i, c in enumerate(cats):
        if out and out[-1][0] == c:
            out[-1][2] += 1
        else:
            out.append([c, i, 1])
    return out


def band(x, y, w, h, cats):
    n, parts = len(cats), []
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>')
    for c, s, ln in runs(cats):
        if c != "free":
            parts.append(f'<rect x="{x + s*w/n:.2f}" y="{y}" width="{ln*w/n + 0.3:.2f}" height="{h}" fill="{CATS[c][0]}"/>')
    # sunken XP border
    parts.append(f'<path d="M{x-1} {y+h} V{y-1} H{x+w}" fill="none" stroke="#808080"/>'
                 f'<path d="M{x-1} {y+h+1} H{x+w+1} V{y-1}" fill="none" stroke="#fff"/>')
    return "".join(parts)


def button(x, y, w, label, pressed=False):
    fill = "#e3e3db" if pressed else "url(#btn)"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="23" rx="3" fill="{fill}" stroke="#003c74"/>'
            f'<text x="{x + w/2}" y="{y+16}" text-anchor="middle" class="ui">{label}</text>')


def render(days, login):
    cats = classify(days)
    n = len(days)
    total = sum(c for _, c in days)
    active = sum(1 for c in cats if c != "free")
    frag = sum(1 for c in cats if c == "light")
    W, H, X, BW = 900, 330, 34, 832
    Y1, Y2, BH = 150, 206, 30
    packed = sorted(cats, key=ORDER.index)
    cols = [("Volume", 0), ("Session Status", 150), ("File System", 300), ("Capacity", 410),
            ("Free Space", 530), ("% Free Space", 660)]
    vals = [f"{login} (C:)", "Defragmented", "GIT", f"{total} commits",
            f"{n - active} days", f"{round(100*(n-active)/n)} %"]
    table = "".join(f'<text x="{X+6+dx}" y="{93}" class="ui">{escape(h)}</text>'
                    f'<text x="{X+6+dx}" y="{113}" class="ui">{escape(v)}</text>' for (h, dx), v in zip(cols, vals))
    legend = "".join(f'<rect x="{X + i*210}" y="279" width="11" height="11" fill="{CATS[k][0]}" stroke="#808080"/>'
                     f'<text x="{X + 16 + i*210}" y="289" class="ui">{escape(CATS[k][1])}</text>'
                     for i, k in enumerate(ORDER))
    period = f"{days[0][0]} to {days[-1][0]}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .ui {{ font-family: Tahoma, Verdana, 'Segoe UI', sans-serif; font-size: 12px; fill: #000; }}
    .title {{ font-family: 'Trebuchet MS', Tahoma, sans-serif; font-size: 14px; font-weight: bold; fill: #fff; }}
  </style>
  <defs>
    <linearGradient id="titlebar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0a5fe8"/><stop offset=".12" stop-color="#3d95ff"/><stop offset=".35" stop-color="#0b5fe6"/>
      <stop offset=".9" stop-color="#0052d9"/><stop offset="1" stop-color="#003fb0"/>
    </linearGradient>
    <linearGradient id="btn" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset=".85" stop-color="#ecebe6"/><stop offset="1" stop-color="#d6d0c5"/>
    </linearGradient>
    <linearGradient id="hdr" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fdfdfd"/><stop offset="1" stop-color="#e4e3dd"/>
    </linearGradient>
    <linearGradient id="close" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#e87a5a"/><stop offset="1" stop-color="#c2350f"/>
    </linearGradient>
    <linearGradient id="tb" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4f93ff"/><stop offset="1" stop-color="#0a4fd0"/>
    </linearGradient>
    <clipPath id="progress"><rect x="{X}" y="{Y2-2}" height="{BH+4}" width="0">
      <animate attributeName="width" values="0;{BW};{BW}" keyTimes="0;.75;1" dur="10s" repeatCount="indefinite"/>
    </rect></clipPath>
  </defs>

  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="8" fill="#0831d9"/>
  <path d="M10 40 V18 Q10 10 18 10 H{W-18} Q{W-10} 10 {W-10} 18 V40 Z" fill="url(#titlebar)"/>
  <g>{"".join(f'<rect x="{18 + (i%2)*8}" y="{17 + (i//2)*8}" width="7" height="7" fill="{c}"/>' for i, c in enumerate(["#e02020", "#2050e0", "#00b000", "#fff"]))}</g>
  <text x="42" y="31" class="title">Disk Defragmenter</text>
  <g stroke="#fff" stroke-width="1.2">
    <rect x="{W-84}" y="15" width="21" height="21" rx="3" fill="url(#tb)"/>
    <rect x="{W-61}" y="15" width="21" height="21" rx="3" fill="url(#tb)"/>
    <rect x="{W-38}" y="15" width="21" height="21" rx="3" fill="url(#close)"/>
  </g>
  <rect x="{W-79}" y="28" width="8" height="3" fill="#fff"/>
  <rect x="{W-56}" y="20" width="11" height="11" fill="none" stroke="#fff" stroke-width="2"/>
  <path d="M{W-33} 20 l11 11 M{W-22} 20 l-11 11" stroke="#fff" stroke-width="2.4"/>

  <rect x="14" y="40" width="{W-28}" height="{H-54}" fill="#ece9d8"/>
  <text x="{X-6}" y="58" class="ui" style="white-space:pre">File    Action    View    Help</text>
  <rect x="14" y="64" width="{W-28}" height="1" fill="#c5c2b2"/>

  <rect x="{X}" y="76" width="{BW}" height="44" fill="#fff" stroke="#7f9db9"/>
  <rect x="{X+1}" y="77" width="{BW-2}" height="22" fill="url(#hdr)"/>
  <rect x="{X+1}" y="99" width="{BW-2}" height="1" fill="#d6d2c2"/>
  {table}

  <text x="{X}" y="{Y1-8}" class="ui">Estimated disk usage before defragmentation:  <tspan fill="#555">({period})</tspan></text>
  {band(X, Y1, BW, BH, cats)}
  <text x="{X}" y="{Y2-8}" class="ui">Estimated disk usage after defragmentation:</text>
  <rect x="{X}" y="{Y2}" width="{BW}" height="{BH}" fill="#fff"/>
  <g clip-path="url(#progress)">{band(X, Y2, BW, BH, packed)}</g>
  <path d="M{X-1} {Y2+BH} V{Y2-1} H{X+BW}" fill="none" stroke="#808080"/>
  <path d="M{X-1} {Y2+BH+1} H{X+BW+1} V{Y2-1}" fill="none" stroke="#fff"/>

  {button(X, 246, 80, "Analyze")}{button(X+88, 246, 90, "Defragment", True)}{button(X+186, 246, 70, "Pause")}{button(X+264, 246, 70, "Stop")}{button(X+342, 246, 100, "View Report")}
  <text x="{X+BW}" y="262" text-anchor="end" class="ui">{active} active days · {frag} fragmented</text>
  {legend}
  <rect x="14" y="{H-30}" width="{W-28}" height="16" fill="#ece9d8" stroke="#c5c2b2"/>
  <text x="{X-6}" y="{H-18}" class="ui" style="font-size:11px">Defragmenting {escape(login)} (C:)... compacting {total} commits into {active} days.</text>
</svg>
'''


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--sample":
        days, login = sample(), "Lucas"
        args = args[1:]
    else:
        login, args = args[0], args[1:]
        days = fetch(login)
    out = Path(args[0] if args else "dist/defrag.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(days, login), encoding="utf-8")
    print("wrote", out)

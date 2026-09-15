#!/usr/bin/env python3
"""Generate the 3D isometric projects board.

Four floating cubes, one per real project, letter on the top face laid into
the iso plane. Static-safe: every element's resting state is complete.

Output: assets/projects.svg — stdlib only, no data fetch.
"""
from pathlib import Path

W, H = 1200, 460
BG = "#04100b"
GREEN = "#00ff9c"
CYAN = "#00d4ff"
AMBER = "#ffb454"
TXT = "#eafff4"
DIM = "#0f8f63"

PROJECTS = [
    {
        "glyph": "$",
        "name": "SellStack",
        "line": "multi-tenant SaaS — resellers run branded",
        "line2": "Telegram shops off one stack",
        "chips": "TypeScript · Node · Mongo · Expo",
        "status": "IN BUILD",
        "color": "#19ffa8",
        "status_color": AMBER,
    },
    {
        "glyph": "S",
        "name": "SubWala",
        "line": "the n8n fleet that started it —",
        "line2": "live Telegram subscription bots",
        "chips": "n8n · MongoDB · Telegram",
        "status": "LIVE",
        "color": CYAN,
        "status_color": GREEN,
    },
    {
        "glyph": "C",
        "name": "Cleo",
        "line": "personal AI assistant — calendar,",
        "line2": "mail, memory, tasks on tap",
        "chips": "n8n · GPT · Telegram",
        "status": "DAILY DRIVER",
        "color": "#0fd68a",
        "status_color": CYAN,
    },
    {
        "glyph": "W",
        "name": "WhatsApp AI",
        "line": "AI agents answering customers inside",
        "line2": "WhatsApp for real businesses",
        "chips": "GPT-4.1 mini · Baileys",
        "status": "LIVE",
        "color": AMBER,
        "status_color": GREEN,
    },
]


def shade(hexcolor, factor):
    r, g, b = (int(hexcolor[i : i + 2], 16) for i in (1, 3, 5))
    f = lambda v: max(0, min(255, int(v * factor)))
    return f"#{f(r):02x}{f(g):02x}{f(b):02x}"


def cube(cx, cy, s, color, glyph, idx):
    """Isometric cube with a glyph laid onto the top-face plane."""
    h = s * 0.5
    d = s * 0.95
    top = f"M{cx},{cy - h} L{cx + s},{cy} L{cx},{cy + h} L{cx - s},{cy} Z"
    left = f"M{cx - s},{cy} L{cx},{cy + h} L{cx},{cy + h + d} L{cx - s},{cy + d} Z"
    right = f"M{cx + s},{cy} L{cx},{cy + h} L{cx},{cy + h + d} L{cx + s},{cy + d} Z"
    # text on top-face plane: unit iso transform, then center it
    gs = s * 0.02
    glyph_tf = f"matrix({gs},{gs * 0.5},{-gs},{gs * 0.5},{cx},{cy})"
    return f"""<g class="cube c{idx}">
      <path d="{left}" fill="{shade(color, 0.38)}" stroke="{shade(color, 0.55)}" stroke-width="1"/>
      <path d="{right}" fill="{shade(color, 0.58)}" stroke="{shade(color, 0.75)}" stroke-width="1"/>
      <path d="{top}" fill="{shade(color, 1.15)}" stroke="{color}" stroke-width="1.6"/>
      <text transform="{glyph_tf}" font-size="28" fill="#04100b" text-anchor="middle" dominant-baseline="central" font-weight="700">{glyph}</text>
    </g>"""


def card(p, cx, idx):
    cy = 218
    s = 92
    return f"""<g class="board">
  {cube(cx, cy, s, p["color"], p["glyph"], idx)}
  <text x="{cx}" y="52" text-anchor="middle" font-size="26" fill="{TXT}" font-weight="700" letter-spacing="1">{p["name"]}</text>
  <text x="{cx}" y="78" text-anchor="middle" font-size="13" fill="{p["status_color"]}" letter-spacing="2">● {p["status"]}</text>
  <text x="{cx}" y="376" text-anchor="middle" font-size="14.5" fill="#9fd8bd">{p["line"]}</text>
  <text x="{cx}" y="396" text-anchor="middle" font-size="14.5" fill="#9fd8bd">{p["line2"]}</text>
  <text x="{cx}" y="422" text-anchor="middle" font-size="12.5" fill="{CYAN}" opacity="0.85">{p["chips"]}</text>
</g>"""


body = "\n  ".join(card(p, 170 + i * 287, i) for i, p in enumerate(PROJECTS))

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, 'Cascadia Mono', Menlo, Consolas, monospace">
  <defs>
    <radialGradient id="bg" cx="50%" cy="35%" r="100%">
      <stop offset="0%" stop-color="#0a2016"/>
      <stop offset="60%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#020806"/>
    </radialGradient>
  </defs>
  <style>
    .cube {{ animation: bob ease-in-out infinite; }}
    .c0 {{ animation-duration: 5.6s; }}
    .c1 {{ animation-duration: 6.9s; animation-delay: -2.4s; }}
    .c2 {{ animation-duration: 6.1s; animation-delay: -1.1s; }}
    .c3 {{ animation-duration: 5.0s; animation-delay: -3.3s; }}
    @keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-11px); }} }}
    .board text {{ opacity: 1; animation: fadeUp .8s ease both; }}
    .board:nth-of-type(1) text {{ animation-delay: .15s; }}
    .board:nth-of-type(2) text {{ animation-delay: .35s; }}
    .board:nth-of-type(3) text {{ animation-delay: .55s; }}
    .board:nth-of-type(4) text {{ animation-delay: .75s; }}
    @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="12" y="12" width="{W - 24}" height="{H - 24}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.22" stroke-width="1.5"/>

  {body}

  <text x="34" y="40" font-size="20" fill="{TXT}">the board</text>
  <text x="34" y="62" font-size="13" fill="{DIM}">what I actually ship — most of it lives in private repos and on live servers</text>
</svg>
"""

dest = Path(__file__).resolve().parent.parent / "assets" / "projects.svg"
dest.write_text(svg, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")

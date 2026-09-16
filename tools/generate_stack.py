#!/usr/bin/env python3
"""Generate the 3D language-stack graphic.

Four floating isometric layers — runtime, core, ship, ai — stacked in an
exploded view with a rising energy axis. Static-safe: every element's
resting state is complete.

Output: assets/stack.svg — stdlib only, no data fetch.
"""
from pathlib import Path

W, H = 1200, 560
BG = "#04100b"
GREEN = "#00ff9c"
CYAN = "#00d4ff"
TXT = "#eafff4"
DIM = "#0f8f63"
MUTED = "#9fd8bd"

CX = 430
S = 190
KAPPA = 0.16
DROP = 12
ANGLE = 9.09

LAYERS = [
    {"name": "runtime", "color": "#0f8f63", "cy": 430, "techs": "Linux VPS \u00b7 Docker \u00b7 MongoDB Atlas"},
    {"name": "core", "color": "#00c97b", "cy": 330, "techs": "TypeScript \u00b7 Node.js \u00b7 Express \u00b7 Python \u00b7 Zod"},
    {"name": "ship", "color": "#19ffa8", "cy": 230, "techs": "Telegraf \u00b7 React Native + Expo \u00b7 Baileys"},
    {"name": "ai", "color": CYAN, "cy": 130, "techs": "n8n \u00b7 GPT-4.1 mini"},
]


def shade(hexcolor, factor):
    r, g, b = (int(hexcolor[i : i + 2], 16) for i in (1, 3, 5))
    f = lambda v: max(0, min(255, int(v * factor)))
    return f"#{f(r):02x}{f(g):02x}{f(b):02x}"


def slab(cx, cy, s, kappa, drop, color):
    hh = s * kappa
    top = f"M{cx},{cy - hh} L{cx + s},{cy} L{cx},{cy + hh} L{cx - s},{cy} Z"
    left = f"M{cx - s},{cy} L{cx},{cy + hh} L{cx},{cy + hh + drop} L{cx - s},{cy + drop} Z"
    right = f"M{cx + s},{cy} L{cx},{cy + hh} L{cx},{cy + hh + drop} L{cx + s},{cy + drop} Z"
    return (
        f'<path d="{left}" fill="{shade(color, 0.32)}" stroke="{shade(color, 0.5)}" stroke-width="1"/>'
        f'<path d="{right}" fill="{shade(color, 0.52)}" stroke="{shade(color, 0.7)}" stroke-width="1"/>'
        f'<path d="{top}" fill="{shade(color, 1.1)}" stroke="{color}" stroke-width="1.5"/>'
    )


layer_groups = []
legend_rows = []
for i, layer in enumerate(LAYERS):
    cy = layer["cy"]
    layer_groups.append(
        f'<g class="layer L{i + 1}">'
        f'{slab(CX, cy, S, KAPPA, DROP, layer["color"])}'
        f'<text x="{CX}" y="{cy + 7}" font-size="21" fill="#04100b" text-anchor="middle" '
        f'font-weight="700" letter-spacing="3" transform="rotate({ANGLE} {CX} {cy})">{layer["name"]}</text>'
        f"</g>"
    )
    ly = cy + 5
    legend_rows.append(
        f'<line x1="628" y1="{cy}" x2="646" y2="{cy}" stroke="{layer["color"]}" stroke-opacity="0.5" stroke-width="1.2"/>'
        f'<path d="M656,{cy - 5} L661,{cy} L656,{cy + 5} L651,{cy} Z" fill="{layer["color"]}"/>'
        f'<text x="672" y="{ly}" font-size="15.5">'
        f'<tspan fill="{layer["color"]}" font-weight="700">{layer["name"]}</tspan>'
        f'<tspan fill="{MUTED}"> \u2014 {layer["techs"]}</tspan>'
        f"</text>"
    )

rising = []
for i, (dur, begin, color) in enumerate(
    [(3.6, -0.4, GREEN), (4.4, -1.8, CYAN), (3.1, -2.6, "#19ffa8")]
):
    rising.append(
        f'<circle r="2.4" fill="{color}">'
        f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="M430,500 L430,90"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" '
        f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f"</circle>"
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, 'Cascadia Mono', Menlo, Consolas, monospace">
  <defs>
    <radialGradient id="bg" cx="40%" cy="35%" r="100%">
      <stop offset="0%" stop-color="#0a2016"/>
      <stop offset="60%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#020806"/>
    </radialGradient>
  </defs>
  <style>
    .layer {{ animation: bob ease-in-out infinite; }}
    .L1 {{ animation-duration: 6.6s; }}
    .L2 {{ animation-duration: 5.8s; animation-delay: -1.9s; }}
    .L3 {{ animation-duration: 7.1s; animation-delay: -3.2s; }}
    .L4 {{ animation-duration: 5.3s; animation-delay: -0.8s; }}
    @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
    .axis {{ stroke-dasharray: 3 8; animation: rise 1.6s linear infinite; }}
    @keyframes rise {{ to {{ stroke-dashoffset: -11; }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="12" y="12" width="{W - 24}" height="{H - 24}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.22" stroke-width="1.5"/>

  <path class="axis" d="M430,505 L430,85" fill="none" stroke="{DIM}" stroke-width="1.2"/>

  {" ".join(layer_groups)}

  <g>{" ".join(legend_rows)}</g>

  <g>{" ".join(rising)}</g>

  <text x="34" y="40" font-size="20" fill="{TXT}">the stack</text>
  <text x="34" y="62" font-size="13" fill="{DIM}">four layers — everything else is a detail</text>
</svg>
"""

dest = Path(__file__).resolve().parent.parent / "assets" / "stack.svg"
dest.write_text(svg, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")

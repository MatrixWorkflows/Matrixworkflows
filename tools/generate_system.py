#!/usr/bin/env python3
"""Generate the animated 3D "system" diagram.

Two channel slabs on top, the four products floating in the middle, the
platform slab underneath — circuit-routed traffic lines carry moving pulses
between them. Static-safe: every element's resting state is complete.

Output: assets/system.svg — stdlib only, no data fetch.
"""
from pathlib import Path

W, H = 1200, 700
BG = "#04100b"
GREEN = "#00ff9c"
CYAN = "#00d4ff"
AMBER = "#ffb454"
TXT = "#eafff4"
DIM = "#0f8f63"
MUTED = "#9fd8bd"

CHANNELS = [
    {"label": "TELEGRAM", "cx": 420, "color": CYAN, "cls": "ch1"},
    {"label": "WHATSAPP", "cx": 780, "color": "#19ffa8", "cls": "ch2"},
]

PRODUCTS = [
    {"glyph": "$", "name": "SellStack", "line": "multi-tenant SaaS", "color": "#19ffa8", "cx": 210, "cls": "c1"},
    {"glyph": "S", "name": "SubWala", "line": "the n8n bot fleet", "color": CYAN, "cx": 470, "cls": "c2"},
    {"glyph": "C", "name": "Cleo", "line": "personal assistant", "color": "#0fd68a", "cx": 730, "cls": "c3"},
    {"glyph": "W", "name": "WhatsApp AI", "line": "agents in the inbox", "color": AMBER, "cx": 990, "cls": "c4"},
]

ROUTES = [
    "M420,239 V262 H210 V293",
    "M420,239 V272 H470 V293",
    "M420,239 V282 H730 V293",
    "M780,239 V272 H990 V293",
]

PLATFORM_CHIPS = [
    ("n8n workflows", -200),
    ("MongoDB Atlas", 0),
    ("Docker \u00b7 Hostinger VPS", 200),
]

CUBE_CY = 340
CUBE_S = 90
PLATFORM_CY = 575
PLATFORM_S = 460
PLATFORM_KAPPA = 0.18
CHANNEL_CY = 165


def shade(hexcolor, factor):
    r, g, b = (int(hexcolor[i : i + 2], 16) for i in (1, 3, 5))
    f = lambda v: max(0, min(255, int(v * factor)))
    return f"#{f(r):02x}{f(g):02x}{f(b):02x}"


def slab(cx, cy, s, kappa, drop, color):
    """Isometric slab: diamond top + two side faces."""
    hh = s * kappa
    top = f"M{cx},{cy - hh} L{cx + s},{cy} L{cx},{cy + hh} L{cx - s},{cy} Z"
    left = f"M{cx - s},{cy} L{cx},{cy + hh} L{cx},{cy + hh + drop} L{cx - s},{cy + drop} Z"
    right = f"M{cx + s},{cy} L{cx},{cy + hh} L{cx},{cy + hh + drop} L{cx + s},{cy + drop} Z"
    return (
        f'<path d="{left}" fill="{shade(color, 0.32)}" stroke="{shade(color, 0.5)}" stroke-width="1"/>'
        f'<path d="{right}" fill="{shade(color, 0.52)}" stroke="{shade(color, 0.7)}" stroke-width="1"/>'
        f'<path d="{top}" fill="{shade(color, 1.1)}" stroke="{color}" stroke-width="1.5"/>'
    )


def cube(cx, cy, s, color, glyph):
    """Isometric cube with a glyph laid onto the top-face plane."""
    h = s * 0.5
    d = s * 0.95
    top = f"M{cx},{cy - h} L{cx + s},{cy} L{cx},{cy + h} L{cx - s},{cy} Z"
    left = f"M{cx - s},{cy} L{cx},{cy + h} L{cx},{cy + h + d} L{cx - s},{cy + d} Z"
    right = f"M{cx + s},{cy} L{cx},{cy + h} L{cx},{cy + h + d} L{cx + s},{cy + d} Z"
    gs = s * 0.02
    glyph_tf = f"matrix({gs},{gs * 0.5},{-gs},{gs * 0.5},{cx},{cy})"
    return (
        f'<path d="{left}" fill="{shade(color, 0.38)}" stroke="{shade(color, 0.55)}" stroke-width="1"/>'
        f'<path d="{right}" fill="{shade(color, 0.58)}" stroke="{shade(color, 0.75)}" stroke-width="1"/>'
        f'<path d="{top}" fill="{shade(color, 1.15)}" stroke="{color}" stroke-width="1.6"/>'
        f'<text transform="{glyph_tf}" font-size="28" fill="#04100b" text-anchor="middle" dominant-baseline="central" font-weight="700">{glyph}</text>'
    )


channel_groups = []
for ch in CHANNELS:
    channel_groups.append(
        f'<g class="slab {ch["cls"]}">'
        f'{slab(ch["cx"], CHANNEL_CY, 150, 0.32, 26, ch["color"])}'
        f'<text x="{ch["cx"]}" y="{CHANNEL_CY + 6}" font-size="22" fill="#04100b" text-anchor="middle" '
        f'font-weight="700" letter-spacing="4" transform="rotate(17.74 {ch["cx"]} {CHANNEL_CY})">{ch["label"]}</text>'
        f"</g>"
    )

product_groups = []
for p in PRODUCTS:
    product_groups.append(
        f'<g class="cube {p["cls"]}">'
        f'{cube(p["cx"], CUBE_CY, CUBE_S, p["color"], p["glyph"])}'
        f'<text x="{p["cx"]}" y="496" text-anchor="middle" font-size="19" fill="{TXT}" font-weight="700">{p["name"]}</text>'
        f'<text x="{p["cx"]}" y="516" text-anchor="middle" font-size="13" fill="{MUTED}">{p["line"]}</text>'
        f"</g>"
    )

chips = []
for label, u in PLATFORM_CHIPS:
    x = 600 + u
    y = PLATFORM_CY + u * PLATFORM_KAPPA + 4
    chips.append(
        f'<text x="{x}" y="{y}" font-size="14" fill="{TXT}" text-anchor="middle" '
        f'transform="rotate(10.2 {x} {y})" opacity="0.92">{label}</text>'
    )

routes = [
    f'<path class="flow" d="{d}" fill="none" stroke="{DIM}" stroke-width="1.3"/>' for d in ROUTES
]

pulse_dots = []
for i, d in enumerate(ROUTES):
    color = (GREEN, CYAN, GREEN, AMBER)[i]
    dur = (3.1, 3.4, 2.9, 3.6)[i]
    begin = (-1.2, -2.1, -0.6, -1.8)[i]
    pulse_dots.append(
        f'<circle r="3" fill="{color}" opacity="0.95">'
        f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{d}"/>'
        f"</circle>"
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, 'Cascadia Mono', Menlo, Consolas, monospace">
  <defs>
    <radialGradient id="bg" cx="50%" cy="35%" r="100%">
      <stop offset="0%" stop-color="#0a2016"/>
      <stop offset="60%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#020806"/>
    </radialGradient>
  </defs>
  <style>
    .slab, .cube {{ animation: bob ease-in-out infinite; }}
    .ch1 {{ animation-duration: 6.2s; }}
    .ch2 {{ animation-duration: 5.4s; animation-delay: -2.2s; }}
    .c1 {{ animation-duration: 5.6s; }}
    .c2 {{ animation-duration: 6.9s; animation-delay: -2.4s; }}
    .c3 {{ animation-duration: 6.1s; animation-delay: -1.1s; }}
    .c4 {{ animation-duration: 5.0s; animation-delay: -3.3s; }}
    @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-9px); }} }}
    .flow {{ stroke-dasharray: 4 9; animation: flow 1.1s linear infinite; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -13; }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="12" y="12" width="{W - 24}" height="{H - 24}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.22" stroke-width="1.5"/>

  <g class="platform">{slab(600, PLATFORM_CY, PLATFORM_S, PLATFORM_KAPPA, 24, DIM)}</g>

  {" ".join(routes)}

  {" ".join(chips)}

  {" ".join(channel_groups)}

  {" ".join(product_groups)}

  <g>{" ".join(pulse_dots)}</g>

  <text x="34" y="40" font-size="20" fill="{TXT}">the system</text>
  <text x="34" y="62" font-size="13" fill="{DIM}">one message path from /start to renewal — all four products ride it</text>
</svg>
"""

dest = Path(__file__).resolve().parent.parent / "assets" / "system.svg"
dest.write_text(svg, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")

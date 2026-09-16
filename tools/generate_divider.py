#!/usr/bin/env python3
"""Generate the animated ember-divider equivalent: a data-bus divider.

One gradient bus line, end ticks, drifting pulses in brand colors.
Static-safe: without animation it still reads as a thin terminal rule.

Output: assets/divider.svg — stdlib only, no data fetch.
"""
from pathlib import Path

W, H = 1200, 48
GREEN = "#00ff9c"
CYAN = "#00d4ff"
AMBER = "#ffb454"
BG = "#04100b"
DIM = "#0f8f63"

PULSES = [
    {"color": GREEN, "dur": 5.4, "begin": 0, "path": "M40,24 L1160,24"},
    {"color": CYAN, "dur": 6.2, "begin": -2.1, "path": "M1160,24 L40,24"},
    {"color": AMBER, "dur": 7.8, "begin": -4.3, "path": "M40,24 L1160,24"},
]

pulses = []
for p in PULSES:
    pulses.append(
        f'<circle r="2.6" fill="{p["color"]}">'
        f'<animateMotion dur="{p["dur"]}s" begin="{p["begin"]}s" repeatCount="indefinite" path="{p["path"]}"/>'
        f"</circle>"
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, 'Cascadia Mono', Menlo, Consolas, monospace">
  <defs>
    <linearGradient id="bus" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{DIM}" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="{GREEN}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{DIM}" stop-opacity="0.15"/>
    </linearGradient>
  </defs>
  <style>
    @media (prefers-reduced-motion: reduce) {{
      circle {{ display: none; }}
    }}
  </style>

  <line x1="40" y1="24" x2="1160" y2="24" stroke="url(#bus)" stroke-width="1.4"/>
  <path d="M40,15 V33 M1160,15 V33" stroke="{DIM}" stroke-width="1.4"/>

  <path d="M240,21 L243,24 L240,27 L237,24 Z" fill="none" stroke="{DIM}" stroke-width="1"/>
  <path d="M960,21 L963,24 L960,27 L957,24 Z" fill="none" stroke="{DIM}" stroke-width="1"/>

  <path d="M600,14 L610,24 L600,34 L590,24 Z" fill="{BG}" stroke="{GREEN}" stroke-width="1.3"/>
  <circle cx="600" cy="24" r="2" fill="{GREEN}"/>

  {" ".join(pulses)}
</svg>
"""

dest = Path(__file__).resolve().parent.parent / "assets" / "divider.svg"
dest.write_text(svg, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")

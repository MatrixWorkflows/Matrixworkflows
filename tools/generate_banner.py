#!/usr/bin/env python3
"""Generate the animated matrix-theme profile banner.

Pure stdlib, deterministic (seeded) — same input, same banner.
Output: assets/banner.svg

Animations run on GitHub: the SVG is proxied by camo and rendered as an
<img>, where inline <style> CSS keyframes execute. Every element's static
state is its finished state, so if animations are stripped the banner still
renders complete.
"""
import random
from pathlib import Path

W, H = 1200, 400
GREEN = "#00ff9c"
GREEN_DIM = "#0f8f63"
CYAN = "#00d4ff"
BG = "#04100b"
SEED = 7

# matrix rain glyphs: katakana + digits + a few symbols
GLYPHS = (
    "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ01234567890123456789Z:=*+-<>"
)

random.seed(SEED)
out = []


def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def rain_columns(n=26):
    """Each column: one random 22-glyph string rendered twice stacked; the
    inner group animates translateY by exactly one copy's height per loop
    => seamless. Outer group holds the x offset (CSS transform on the inner
    would otherwise clobber it)."""
    cols = []
    line_h = 18
    period = 22 * line_h  # 396px = one copy
    for i in range(n):
        x = 14 + i * ((W - 28) / (n - 1)) + random.uniform(-4, 4)
        s = "".join(random.choice(GLYPHS) for _ in range(22))
        dur = random.uniform(5.5, 11.0)
        delay = random.uniform(-11.0, 0.0)  # negative => mid-fall at t=0
        opacity = random.uniform(0.14, 0.34)
        tspans = []
        for copy in range(2):
            for g in range(22):
                y = copy * period + g * line_h
                tspans.append(f'<tspan x="0" y="{y}">{esc(s[g])}</tspan>')
        cols.append(
            f'<g transform="translate({x:.1f},{-period})">'
            f'<g class="rain" style="animation-duration:{dur:.2f}s;'
            f'animation-delay:{delay:.2f}s;opacity:{opacity:.2f}">'
            f'<text class="glyph">{" ".join(tspans)}</text></g></g>'
        )
    return "\n    ".join(cols)


def iso_cube(cx, cy, s, cls):
    """Isometric cube: diamond top + two side faces."""
    h = s * 0.5
    d = s * 0.95  # side drop
    top = f"M{cx},{cy - h} L{cx + s},{cy} L{cx},{cy + h} L{cx - s},{cy} Z"
    left = f"M{cx - s},{cy} L{cx},{cy + h} L{cx},{cy + h + d} L{cx - s},{cy + d} Z"
    right = f"M{cx + s},{cy} L{cx},{cy + h} L{cx},{cy + h + d} L{cx + s},{cy + d} Z"
    return (
        f'<g class="cube {cls}">'
        f'<path class="face-l" d="{left}"/>'
        f'<path class="face-r" d="{right}"/>'
        f'<path class="face-t" d="{top}"/>'
        f"</g>"
    )


def corner_ticks():
    t = 18
    c = []
    for (x, y, dx, dy) in [
        (14, 14, 1, 1),
        (W - 14, 14, -1, 1),
        (14, H - 14, 1, -1),
        (W - 14, H - 14, -1, -1),
    ]:
        c.append(
            f'<path d="M{x + dx * t},{y} L{x},{y} L{x},{y + dy * t}" '
            f'fill="none" stroke="{GREEN}" stroke-width="2.5" opacity="0.9"/>'
        )
    return "\n    ".join(c)


NAME = "matrixworkflows"
NAME_X, NAME_Y = 84, 208
FONT = 46

# per-char reveal: base opacity 1, animation only hides before its delay.
# cursor is a trailing tspan -> flows after the text in ANY font, no metric math
chars = " ".join(
    f'<tspan class="ch" style="--d:{0.4 + i * 0.115:.2f}s">{esc(c)}</tspan>'
    for i, c in enumerate(NAME)
) + f' <tspan class="cursor" dx="7" font-size="{int(FONT * 0.9)}" style="animation-delay:{0.4 + len(NAME) * 0.115:.2f}s">|</tspan>'

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, 'Cascadia Mono', 'JetBrains Mono', Menlo, Consolas, monospace">
  <defs>
    <radialGradient id="bg" cx="35%" cy="40%" r="90%">
      <stop offset="0%" stop-color="#0a2016"/>
      <stop offset="55%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#020806"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="25%" stop-color="white"/>
      <stop offset="80%" stop-color="white"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{GREEN}" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <mask id="rainMask">
      <rect x="0" y="0" width="{W}" height="{H}" fill="url(#fade)"/>
    </mask>
  </defs>

  <style>
    .rain {{ animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translateY(0); }} to {{ transform: translateY(396px); }} }}
    .rain text {{ font-size: 15px; fill: {GREEN_DIM}; }}
    .ch {{ opacity: 1; animation: chIn 1ms linear var(--d) both; }}
    @keyframes chIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .cursor {{ opacity: 0; animation: blink 1.05s steps(1) infinite; }}
    @keyframes blink {{ 0%, 55% {{ opacity: 1; }} 56%, 100% {{ opacity: 0; }} }}
    .sub {{ opacity: 1; animation: subIn .9s ease 2.3s both; }}
    @keyframes subIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .tag {{ opacity: 1; animation: subIn .9s ease 2.7s both; }}
    .cube {{ animation: bob ease-in-out infinite; }}
    .c1 {{ animation-duration: 5.2s; }}
    .c2 {{ animation-duration: 6.8s; animation-delay: -2.1s; }}
    .c3 {{ animation-duration: 4.4s; animation-delay: -1.2s; }}
    @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-13px); }} }}
    .sweep {{ animation: sweepmove 8s linear infinite; }}
    @keyframes sweepmove {{ from {{ transform: translateY(-110px); }} to {{ transform: translateY({H + 110}px); }} }}
    .face-t {{ fill: #19ffa8; stroke: {GREEN}; stroke-width: 1.4; filter: drop-shadow(0 0 7px rgba(0,255,156,.55)); }}
    .face-l {{ fill: #0b9c62; stroke: #063; stroke-width: 1; }}
    .face-r {{ fill: #076b43; stroke: #052; stroke-width: 1; }}
    .name {{ fill: #eafff4; filter: drop-shadow(0 0 9px rgba(0,255,156,.5)); }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .sub, .tag {{ opacity: 1 !important; transform: none !important; }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <g mask="url(#rainMask)">
    {rain_columns()}
  </g>

  <!-- HUD frame -->
  <rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.28" stroke-width="1.5"/>
  {corner_ticks()}

  <!-- name + subtitle -->
  <text class="name" x="{NAME_X}" y="{NAME_Y}" font-size="{FONT}" letter-spacing="1">{chars}</text>
  <text class="sub" x="{NAME_X + 4}" y="{NAME_Y + 44}" font-size="21" fill="{CYAN}">bots that sell &#183; systems that run themselves</text>
  <text class="tag" x="{NAME_X + 4}" y="{NAME_Y + 76}" font-size="15" fill="{GREEN}" opacity="0.75">telegram &#183; saas &#183; ai agents &#183; automation</text>

  <!-- floating isometric cubes (right zone only, clear of the name) -->
  {iso_cube(995, 160, 50, "c1")}
  {iso_cube(1095, 258, 34, "c2")}
  {iso_cube(885, 285, 22, "c3")}

  <!-- footer -->
  <text x="28" y="{H - 28}" font-size="14" fill="{GREEN_DIM}">$ git push origin main --force-with-love</text>
  <text x="{W - 28}" y="{H - 28}" font-size="14" fill="{GREEN_DIM}" text-anchor="end">uptime: shipping daily &#9654;</text>

  <!-- scan sweep -->
  <rect class="sweep" x="0" y="0" width="{W}" height="110" fill="url(#sweep)"/>
</svg>
"""

dest = Path(__file__).resolve().parent.parent / "assets" / "banner.svg"
dest.write_text(svg, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size / 1024:.1f} KB)")

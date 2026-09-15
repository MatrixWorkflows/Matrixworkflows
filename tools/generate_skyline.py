#!/usr/bin/env python3
"""Generate the animated 3D isometric contribution skyline.

Every cube below is one real day from GitHub's GraphQL contribution
calendar. Bars rise with a staggered wave on load; peak days glow-pulse.

Usage:
  python tools/generate_skyline.py --user MatrixWorkflows            # needs GITHUB_TOKEN
  python tools/generate_skyline.py --demo                             # deterministic sample, watermarked

Output: assets/skyline.svg

stdlib only.
"""
import argparse
import datetime as dt
import json
import os
import random
import sys
import urllib.request
from pathlib import Path

GREEN = "#00ff9c"
CYAN = "#00d4ff"
BG = "#04100b"
DIM = "#0f8f63"
TXT = "#eafff4"

QUERY = """
query($user: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $user) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_days(user, token):
    to = dt.date.today()
    from_ = to - dt.timedelta(days=364)
    body = json.dumps(
        {
            "query": QUERY,
            "variables": {
                "user": user,
                "from": from_.isoformat() + "T00:00:00Z",
                "to": to.isoformat() + "T00:00:00Z",
            },
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return days, cal["totalContributions"]


def demo_days():
    random.seed(11)
    days = []
    today = dt.date.today()
    for i in range(365):
        d = today - dt.timedelta(days=364 - i)
        # sparse bursts so the demo skyline reads as plausible, not fake-busy
        burst = 6 if (i // 17) % 5 == 0 else 0
        c = random.choice([0, 0, 0, 1, 2, 3, 5 + burst]) if random.random() < 0.5 else 0
        days.append({"date": d.isoformat(), "contributionCount": c})
    return days, sum(d["contributionCount"] for d in days)


def shade(hexcolor, factor):
    r = int(hexcolor[1:3], 16)
    g = int(hexcolor[3:5], 16)
    b = int(hexcolor[5:7], 16)
    f = lambda v: max(0, min(255, int(v * factor)))
    return f"#{f(r):02x}{f(g):02x}{f(b):02x}"


def ramp(q):
    """color ramp by intensity q in [0,1] — matrix greens, GitHub-style tiers."""
    if q == 0:
        return "#0c2e22", None
    if q < 0.25:
        return "#0e5c3e", None
    if q < 0.55:
        return "#12a06c", None
    if q < 0.85:
        return "#19ffa8", None
    return "#8dffd2", "hot"  # peak tier glows


def render(days, total, demo=False):
    A, B = 10, 5  # iso half-width / half-height of one day cell
    MAXH, MINH = 150, 10
    OX, OY = 86, 240  # OY must clear the tallest early-week bar (MAXH + B + headroom)
    n_weeks = max((len(days) + 6) // 7, 53)
    counts = [d["contributionCount"] for d in days]
    peak = max(counts) if counts else 0
    active = sum(1 for c in counts if c)

    def ground(w, dcol):
        return OX + (w - dcol) * A, OY + (w + dcol) * B

    bars = []  # (depth, markup)
    for i, day in enumerate(days):
        w, dcol = divmod(i, 7)
        c = day["contributionCount"]
        gx, gy = ground(w, dcol)
        depth = w + dcol
        fill, hot = ramp(c / peak if peak else 0)
        if c == 0:
            # flat day-tile
            tile = (
                f"M{gx},{gy - B} L{gx + A},{gy} L{gx},{gy + B} L{gx - A},{gy} Z"
            )
            bars.append(
                (depth, w, dcol,
                 f'<path class="tile" d="{tile}" fill="{fill}"/>')
            )
            continue
        h = MINH + (c / peak) * (MAXH - MINH)
        top = f"M{gx},{gy - B - h} L{gx + A},{gy - h} L{gx},{gy + B - h} L{gx - A},{gy - h} Z"
        left = f"M{gx - A},{gy - h} L{gx},{gy + B - h} L{gx},{gy + B} L{gx - A},{gy} Z"
        right = f"M{gx + A},{gy - h} L{gx},{gy + B - h} L{gx},{gy + B} L{gx + A},{gy} Z"
        cls = "bar" + (" hot" if hot else "")
        delay = w * 0.028 + dcol * 0.012
        bars.append(
            (depth, w, dcol,
             f'<g class="{cls}" style="animation-delay:{delay:.3f}s">'
             f'<path class="fl" d="{left}" fill="{shade(fill, 0.42)}"/>'
             f'<path class="fr" d="{right}" fill="{shade(fill, 0.62)}"/>'
             f'<path class="ft" d="{top}" fill="{fill}"/></g>')
        )
    bars.sort(key=lambda t: (t[0], t[1], t[2]))
    body = "\n    ".join(b[3] for b in bars)

    first = days[0]["date"] if days else "?"
    last = days[-1]["date"] if days else "?"
    peak_day = days[counts.index(peak)]["date"] if peak else "—"
    W = OX + (n_weeks + 6) * A + 70
    H = OY + (n_weeks + 6) * B + 150
    demo_tag = (
        f'<text x="{W - 30:.0f}" y="{H - 36:.0f}" text-anchor="end" font-size="15" fill="#ffb454">DEMO DATA</text>'
        if demo
        else ""
    )
    stats = (
        f"{total} contributions · {active} active days · peak {peak} on {peak_day}"
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="ui-monospace, 'Cascadia Mono', Menlo, Consolas, monospace">
  <defs>
    <radialGradient id="bg" cx="30%" cy="25%" r="110%">
      <stop offset="0%" stop-color="#0a2016"/>
      <stop offset="60%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="#020806"/>
    </radialGradient>
    <linearGradient id="groundFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GREEN}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .bar {{ transform-box: fill-box; transform-origin: 50% 100%;
           animation: rise .9s cubic-bezier(.18,.7,.25,1) both; }}
    @keyframes rise {{ from {{ transform: scaleY(0.04); }} to {{ transform: scaleY(1); }} }}
    .hot .ft {{ animation: pulse 2.8s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ filter: none; }} 50% {{ filter: drop-shadow(0 0 9px rgba(141,255,210,.95)); }} }}
    .tile {{ animation: tileIn .01s linear both; }}
  </style>

  <rect width="{W:.0f}" height="{H:.0f}" fill="url(#bg)"/>
  <rect x="12" y="12" width="{W - 24:.0f}" height="{H - 24:.0f}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.22" stroke-width="1.5"/>

  <text x="34" y="46" font-size="21" fill="{TXT}">contribution skyline</text>
  <text x="34" y="68" font-size="13" fill="{DIM}">one cube = one real day · regenerated daily by GitHub Action</text>
  {demo_tag}

  <g>
    {body}
  </g>

  <rect x="34" y="{H - 96:.0f}" width="{W - 68:.0f}" height="2" fill="url(#groundFade)"/>
  <text x="34" y="{H - 60:.0f}" font-size="16" fill="{GREEN}">{stats}</text>
  <text x="34" y="{H - 36:.0f}" font-size="13" fill="{DIM}">window {first} → {last} · snapshot {dt.date.today().isoformat()} · github graphql, zero hand-editing</text>
</svg>
"""
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="MatrixWorkflows")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    if args.demo:
        days, total = demo_days()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN not set (or pass --demo)")
        days, total = fetch_days(args.user, token)

    dest = Path(__file__).resolve().parent.parent / "assets" / "skyline.svg"
    dest.write_text(render(days, total, demo=args.demo), encoding="utf-8")
    print(f"wrote {dest} ({dest.stat().st_size / 1024:.1f} KB) — total={total}")


if __name__ == "__main__":
    main()

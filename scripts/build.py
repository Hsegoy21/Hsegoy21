"""Draws the profile artwork into assets/.

    python scripts/build.py            # banner, footer and contribution range
    GITHUB_TOKEN=... python scripts/build.py

Stdlib only, so the GitHub Action needs no installs. Without a token the
contribution range is drawn from sample data.
"""
import datetime as dt
import json
import math
import os
import random
import urllib.request
from pathlib import Path

USER = "Hsegoy21"
NAME = "Yogesh Rayamajhi"
NAME_NE = "योगेश रायमाझी"
ROLES = ["Network &amp; security engineer", "Cybersecurity enthusiast", "Packets, ports &amp; protocols", "Based in Nepal"]

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
DEVANAGARI = "'Kohinoor Devanagari', 'Nirmala UI', 'Noto Sans Devanagari', sans-serif"

SKY = """
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0b1022"/>
    <stop offset=".55" stop-color="#23264a"/>
    <stop offset="1" stop-color="#7a3f52"/>
  </linearGradient>"""


def smooth(points):
    """Catmull-Rom spline through points, as an SVG path."""
    d = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(len(points) - 1):
        p0 = points[max(i - 1, 0)]
        p1, p2 = points[i], points[i + 1]
        p3 = points[min(i + 2, len(points) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def jagged(rng, width, base, amp, step, seed_peaks=()):
    """A sharp mountain silhouette; seed_peaks are (x, height) summits to force."""
    pts, x = [], -20
    while x <= width + 20:
        h = amp * (0.35 + 0.65 * rng.random())
        for px, ph in seed_peaks:
            h = max(h, ph - abs(x - px) * 1.1)
        pts.append((x, base - h))
        x += step * (0.6 + 0.8 * rng.random())
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{width + 20},{base + 200} L-20,{base + 200} Z"


def stars(rng, width, height, n):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, width), rng.uniform(0, height)
        r = rng.choice([0.6, 0.8, 1.1, 1.4])
        delay = rng.uniform(0, 4)
        out.append(f'<circle class="tw" cx="{x:.0f}" cy="{y:.0f}" r="{r}" style="animation-delay:{delay:.1f}s"/>')
    return "\n  ".join(out)


def fishtail(cx, base, h):
    """Machhapuchhre-style twin summit."""
    return (f"M{cx - 170},{base} L{cx - 40},{base - h * .72} L{cx - 14},{base - h} L{cx + 2},{base - h * .86} "
            f"L{cx + 22},{base - h * .97} L{cx + 60},{base - h * .7} L{cx + 190},{base} Z")


def banner():
    rng = random.Random(21)
    W, H = 1000, 320
    slot = 100 / len(ROLES)
    roles = "".join(
        f'<text class="role" style="animation-delay:{i * 3}s" x="60" y="214">{r}</text>' for i, r in enumerate(ROLES)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{NAME}">
<defs>{SKY}
  <radialGradient id="sun" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#ffd27a"/><stop offset=".45" stop-color="#f5a623" stop-opacity=".55"/>
    <stop offset="1" stop-color="#f5a623" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="snow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff4e0"/><stop offset=".35" stop-color="#c9cde6" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  .tw {{ fill:#fff; animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity:.25 }} 50% {{ opacity:1 }} }}
  .sun {{ animation: rise 6s ease-out both; }}
  @keyframes rise {{ from {{ transform: translateY(60px); opacity:0 }} to {{ transform:none; opacity:1 }} }}
  .name {{ font: 700 54px {FONT}; fill:#fff; letter-spacing:.5px; animation: up 1.2s ease-out both; }}
  .ne {{ font: 500 24px {DEVANAGARI}; fill:#f5a623; animation: up 1.2s .3s ease-out both; }}
  @keyframes up {{ from {{ transform: translateY(14px); opacity:0 }} to {{ transform:none; opacity:1 }} }}
  .role {{ font: 500 20px {FONT}; fill:#c9cde6; opacity:0; animation: role {len(ROLES) * 3}s infinite; }}
  @keyframes role {{ 0% {{ opacity:0; transform:translateY(8px) }} 3%,{slot - 3:.0f}% {{ opacity:1; transform:none }}
                     {slot:.0f}%,100% {{ opacity:0; transform:translateY(-8px) }} }}
  .flag {{ animation: wave 2.4s ease-in-out infinite; transform-origin: 0 0; }}
  @keyframes wave {{ 0%,100% {{ transform: skewY(0) }} 50% {{ transform: skewY(6deg) }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars(rng, W, 170, 70)}
  <circle class="sun" cx="745" cy="205" r="110" fill="url(#sun)"/>
  <path d="{jagged(rng, W, 268, 70, 34)}" fill="#3b3560" opacity=".9"/>
  <path d="{fishtail(745, 270, 165)}" fill="#4a4475"/>
  <path d="{fishtail(745, 270, 165)}" fill="url(#snow)"/>
  <path d="{jagged(rng, W, 292, 48, 26, [(520, 70), (930, 80)])}" fill="#2a2548"/>
  <path d="{jagged(rng, W, 312, 26, 18)}" fill="#171430"/>
  <g transform="translate(731,105)">
    <line x1="0" y1="0" x2="0" y2="-20" stroke="#e8e8f0" stroke-width="1.2"/>
    <g class="flag">
      <rect x="0" y="-20" width="5" height="4" fill="#3b82f6"/><rect x="5" y="-20" width="5" height="4" fill="#f8fafc"/>
      <rect x="10" y="-20" width="5" height="4" fill="#ef4444"/><rect x="15" y="-20" width="5" height="4" fill="#22c55e"/>
      <rect x="20" y="-20" width="5" height="4" fill="#facc15"/>
    </g>
  </g>
  <text class="name" x="58" y="132">{NAME}</text>
  <text class="ne" x="60" y="172">{NAME_NE}</text>
  {roles}
</g>
</svg>
"""


def footer():
    rng = random.Random(7)
    W, H = 1000, 110
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Mountain ridge">
<defs>{SKY}<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<style>.t {{ font: 500 15px {FONT}; fill:#c9cde6; }} .k {{ letter-spacing:3px; }} .ne {{ font-family: {DEVANAGARI}; fill:#f5a623; }}</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <path d="{jagged(rng, W, 96, 40, 30)}" fill="#3b3560"/>
  <path d="{jagged(rng, W, 110, 26, 20)}" fill="#171430"/>
  <text class="t" x="{W / 2}" y="40" text-anchor="middle"><tspan class="k">KEEP CLIMBING</tspan>  ·  <tspan class="ne">धन्यवाद</tspan></text>
</g>
</svg>
"""


def contributions():
    """Weekly contribution totals for the last year, oldest first."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        rng = random.Random(1)
        weeks = [(dt.date.today() - dt.timedelta(weeks=52 - i), int(max(0, rng.gauss(12, 9)))) for i in range(53)]
        return weeks, sum(c for _, c in weeks)
    query = """query($login:String!){ user(login:$login){ contributionsCollection{ contributionCalendar{
        totalContributions weeks{ firstDay contributionDays{ contributionCount } } } } } }"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [(dt.date.fromisoformat(w["firstDay"]), sum(d["contributionCount"] for d in w["contributionDays"]))
             for w in cal["weeks"]]
    return weeks, cal["totalContributions"]


BIKER = """<g transform="translate(0,-2)">
      <circle cx="-7" cy="-6" r="5.5" fill="none" stroke="#fff" stroke-width="1.6"/>
      <circle cx="7" cy="-6" r="5.5" fill="none" stroke="#fff" stroke-width="1.6"/>
      <path d="M-7,-6 L-1,-6 L4,-13 L-4,-13 Z M4,-13 L7,-6 M3,-15 L6,-15" fill="none" stroke="#f5a623" stroke-width="1.6" stroke-linejoin="round"/>
      <path d="M-2,-14 L1,-21 L4,-14" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
      <circle cx="2" cy="-24" r="2.8" fill="#f5a623"/>
    </g>"""


def commit_range(weeks, total):
    rng = random.Random(3)
    W, H, base, top = 1000, 280, 238, 92
    peak = max(c for _, c in weeks) or 1
    x0, x1 = 30, W - 30
    step = (x1 - x0) / (len(weeks) - 1)
    # Foothills keep the range looking like mountains in quiet weeks; commits rise above them.
    hills = [22 + 16 * math.sin(i * 0.55) + 10 * math.sin(i * 1.7 + 1) for i in range(len(weeks))]
    lift = (base - top) * (1 if peak >= 10 else 0.4 + 0.06 * peak)
    pts = [(x0 + i * step, base - hills[i] - math.sqrt(c / peak) * lift) for i, (_, c) in enumerate(weeks)]
    ridge = smooth(pts)
    fill = f"M0,{pts[0][1]:.1f} L{ridge[1:]} L{W},{pts[-1][1]:.1f} L{W},{H} L0,{H} Z"
    far = smooth([(x, base - 20 - (base - y) * 0.55 - rng.uniform(0, 30)) for x, y in pts[::2]] + [(x1, base - 30)])
    snowline = base - (base - top) * 0.62

    hi = max(range(len(weeks)), key=lambda i: weeks[i][1])
    hx, hy = pts[hi]
    hi_label = f"{weeks[hi][1]} in the week of {weeks[hi][0]:%d %b}"
    flag_anchor = "end" if hx > W * 0.7 else "start"
    flag_dx = -10 if flag_anchor == "end" else 10

    months, seen = [], set()
    for i, (d, _) in enumerate(weeks):
        if d.day <= 7 and d.month not in seen and 0 < i < len(weeks) - 1:
            seen.add(d.month)
            months.append(f'<text class="m" x="{pts[i][0]:.0f}" y="{H - 12}">{d:%b}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{total} contributions in the last year, drawn as a mountain range">
<defs>{SKY}
  <linearGradient id="rock" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5a4f8a"/><stop offset="1" stop-color="#1c1838"/>
  </linearGradient>
  <clipPath id="snowcap"><rect width="{W}" height="{snowline:.0f}"/></clipPath>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  .tw {{ fill:#fff; animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity:.25 }} 50% {{ opacity:1 }} }}
  .h {{ font: 700 22px {FONT}; fill:#fff; }}
  .s {{ font: 500 14px {FONT}; fill:#c9cde6; }}
  .n {{ font: 700 14px {FONT}; fill:#f5a623; }}
  .m {{ font: 500 11px {FONT}; fill:#8e92b8; text-anchor:middle; }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars(rng, W, 120, 45)}
  <path d="M0,{base - 40} L{far[1:]} L{W},{base - 30} L{W},{H} L0,{H} Z" fill="#2f2a55" opacity=".8"/>
  <path d="{fill}" fill="url(#rock)"/>
  <path d="{fill}" fill="#f4f1ff" opacity=".92" clip-path="url(#snowcap)"/>
  <path d="{ridge}" fill="none" stroke="#f5a623" stroke-width="1.2" opacity=".5"/>
  <g transform="translate({hx:.0f},{hy:.0f})">
    <line x1="0" y1="0" x2="0" y2="-22" stroke="#fff" stroke-width="1.4"/>
    <path d="M0,-22 L14,-18 L0,-14 Z" fill="#ef4444"/>
    <text class="n" x="{flag_dx}" y="-28" text-anchor="{flag_anchor}">▲ {hi_label}</text>
  </g>
  <g>
    {BIKER}
    <animateMotion dur="24s" repeatCount="indefinite" rotate="auto" path="{ridge}"/>
  </g>
  <text class="h" x="32" y="44">Commit Himalaya</text>
  <text class="s" x="32" y="68">{total:,} contributions in the last year · every peak is a week</text>
  {"".join(months)}
</g>
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "banner.svg").write_text(banner())
    (ASSETS / "footer.svg").write_text(footer())
    (ASSETS / "commit-himalaya.svg").write_text(commit_range(*contributions()))
    print("wrote", ", ".join(sorted(p.name for p in ASSETS.glob("*.svg"))))

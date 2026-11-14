#!/usr/bin/env python3
"""Draws the pictures of this profile: the header and the activity card, each in a dark and a light version.

    GITHUB_TOKEN=... python3 build.py            # all four files under assets/
    python3 build.py --hero-only                 # the header only (needs no token)

Standard library only. The activity card reads public data of the account through the GitHub
GraphQL API; the scheduled workflow in .github/workflows/refresh.yml runs it once a day.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

LOGIN = "gapilongo"
NAME = "Ahmed Ghazouani"
EYEBROW = "AI FOR SECURITY OPERATIONS"
TAGLINE = "I build AI that works the security alert queue, and shows its evidence."
OUT = Path(__file__).parent / "assets"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "bg": "#0b1016", "edge": "#1e2733", "grid": "#18202b", "ink": "#e8edf3", "muted": "#8793a2",
        "lane": "#243040", "dot": "#6f7d8f", "calm": "#2dd4bf", "hot": "#ffb224",
        "heat": ["#151c26", "#0f4a45", "#127169", "#17a094", "#2dd4bf"],
        "langs": ["#2dd4bf", "#ffb224", "#8793a2", "#4b5868", "#2a3442"],
    },
    "light": {
        "bg": "#ffffff", "edge": "#d5dbe3", "grid": "#edf0f4", "ink": "#16202b", "muted": "#5d6978",
        "lane": "#d5dbe3", "dot": "#8c98a8", "calm": "#0f8577", "hot": "#c26a00",
        "heat": ["#edf0f4", "#bdeee6", "#74d6c8", "#27b3a2", "#0f8577"],
        "langs": ["#0f8577", "#c26a00", "#5d6978", "#a3adba", "#d5dbe3"],
    },
}

W = 1000
LEFT, RIGHT = 56, 944


def frame(t: dict, height: int, body: str, css: str = "", label: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img" aria-label="{label}">
<title>{label}</title>
<style>
text{{font-family:{SANS};fill:{t['ink']}}}
.mono{{font-family:{MONO};letter-spacing:.08em}}
.muted{{fill:{t['muted']}}}
{css}
</style>
<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t['grid']}"/></pattern></defs>
<rect x=".5" y=".5" width="{W - 1}" height="{height - 1}" rx="16" fill="{t['bg']}" stroke="{t['edge']}"/>
<rect x="1" y="1" width="{W - 2}" height="{height - 2}" rx="16" fill="url(#grid)"/>
{body}
</svg>
"""


def hero(t: dict) -> str:
    """Alerts flow in from the left; at the gate most are closed, and the one that matters goes on to a person."""
    lanes = [244, 266, 288, 310, 332]
    gate, ring = 650, 920
    travel = gate - LEFT
    period = 7.0
    parts = []
    for i, y in enumerate(lanes):
        parts.append(f'<line x1="{LEFT}" y1="{y}" x2="{gate}" y2="{y}" stroke="{t["lane"]}" stroke-width="1.5" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{gate}" cy="{y}" r="3.5" fill="{t["bg"]}" stroke="{t["calm"]}" stroke-width="1.5"/>')
        count = 2 if i == 2 else 3
        for k in range(count):
            delay = -((k + (i * 0.37) % 1) * period / count)
            rest = int(travel * ((k + 0.5 + (i * 0.23) % 0.5) / (count + 0.5)))
            parts.append(
                f'<circle class="d" cx="{LEFT}" cy="{y}" r="4" fill="{t["dot"]}" transform="translate({rest} 0)" style="animation-delay:{delay:.2f}s"/>'
            )
    y = lanes[2]
    parts.append(f'<line x1="{gate}" y1="{y}" x2="{ring - 14}" y2="{y}" stroke="{t["hot"]}" stroke-width="1.5" stroke-linecap="round" opacity=".55"/>')
    parts.append(f'<circle class="ping" cx="{ring}" cy="{y}" r="10" fill="none" stroke="{t["hot"]}" stroke-width="1.5"/>')
    parts.append(f'<circle cx="{ring}" cy="{y}" r="10" fill="none" stroke="{t["hot"]}" stroke-width="1.5"/>')
    parts.append(f'<circle class="h" cx="{LEFT}" cy="{y}" r="5" fill="{t["hot"]}" transform="translate({ring - LEFT} 0)"/>')
    parts.append(f'<line x1="{gate}" y1="{lanes[0] - 14}" x2="{gate}" y2="{lanes[-1] + 14}" stroke="{t["calm"]}" stroke-width="1.5" stroke-linecap="round" opacity=".5"/>')
    body = f"""<text x="{LEFT}" y="78" class="mono muted" font-size="14">{EYEBROW}</text>
<text x="{LEFT}" y="146" font-size="62" font-weight="700" letter-spacing="-.02em">{NAME}</text>
<text x="{LEFT}" y="192" class="muted" font-size="24">{TAGLINE}</text>
{chr(10).join(parts)}
<text x="{LEFT}" y="372" class="mono muted" font-size="13">ALERTS IN</text>
<text x="{gate}" y="372" class="mono" font-size="13" text-anchor="middle" style="fill:{t['calm']}">CLOSED, WITH EVIDENCE</text>
<text x="{RIGHT}" y="372" class="mono" font-size="13" text-anchor="end" style="fill:{t['hot']}">TO A PERSON</text>"""
    css = f"""@keyframes flow{{0%{{transform:translateX(0);opacity:0}}7%{{opacity:1}}86%{{opacity:1}}100%{{transform:translateX({travel}px);opacity:0}}}}
@keyframes hot{{0%{{transform:translateX(0);opacity:0}}5%{{opacity:1}}88%{{transform:translateX({ring - LEFT}px);opacity:1}}100%{{transform:translateX({ring - LEFT}px);opacity:1}}}}
@keyframes ping{{0%,86%{{transform:scale(1);opacity:0}}88%{{transform:scale(1);opacity:.9}}100%{{transform:scale(2.1);opacity:0}}}}
.d{{animation:flow {period}s linear infinite}}
.h{{animation:hot {period * 1.2:.1f}s linear infinite}}
.ping{{transform-origin:{ring}px {y}px;animation:ping {period * 1.2:.1f}s linear infinite}}
@media (prefers-reduced-motion:reduce){{.d,.h,.ping{{animation:none}}.ping{{opacity:0}}}}"""
    return frame(t, 400, body, css, f"{NAME}. {TAGLINE}")


QUERY = """query($login:String!){user(login:$login){createdAt
 contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount}}}}
 repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){totalCount
  nodes{languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}}}"""


def fetch() -> dict:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("set GITHUB_TOKEN (or run with --hero-only)")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"Bearer {token}", "User-Agent": "profile-readme"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        payload = json.load(res)
    if payload.get("errors"):
        sys.exit(f"GitHub API: {payload['errors'][0].get('message')}")
    return payload["data"]["user"]


def languages(nodes: list) -> list:
    """Each repository counts once, split by its own language shares, so one large repository does not decide the bar."""
    share: dict = {}
    for repo in nodes:
        edges = repo["languages"]["edges"]
        total = sum(e["size"] for e in edges)
        for e in edges:
            if total:
                share[e["node"]["name"]] = share.get(e["node"]["name"], 0) + e["size"] / total
    whole = sum(share.values()) or 1
    ranked = sorted(share.items(), key=lambda kv: -kv[1])
    top = [(n, v / whole) for n, v in ranked[:4]]
    rest = 1 - sum(v for _, v in top)
    return top + ([("Other", rest)] if rest > 0.005 else [])


def activity(t: dict, user: dict) -> str:
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"][-53:]
    counts = sorted(d["contributionCount"] for w in weeks for d in w["contributionDays"] if d["contributionCount"])
    cuts = [counts[int(len(counts) * q)] for q in (0.25, 0.5, 0.75)] if counts else [1, 2, 3]

    def level(n: int) -> int:
        return 0 if n == 0 else 1 + sum(n > c for c in cuts)

    pitch, cell, top = (RIGHT - LEFT) / 53, 13.2, 150
    cells = []
    for x, week in enumerate(weeks):
        for yy, day in enumerate(week["contributionDays"]):
            cells.append(
                f'<rect x="{LEFT + x * pitch:.1f}" y="{top + yy * pitch:.1f}" width="{cell}" height="{cell}" rx="3" fill="{t["heat"][level(day["contributionCount"])]}"/>'
            )
    stats = [
        (f"{cal['totalContributions']:,}", "contributions in the last year"),
        (str(user["repositories"]["totalCount"]), "public repositories"),
        (f"{date.today().year - int(user['createdAt'][:4])} years", "on GitHub"),
    ]
    head = []
    for i, (number, label) in enumerate(stats):
        x = LEFT + i * 300
        head.append(f'<text x="{x}" y="84" font-size="44" font-weight="700" letter-spacing="-.02em">{number}</text>')
        head.append(f'<text x="{x}" y="112" class="muted" font-size="17">{label}</text>')
    bar_y = top + 7 * pitch + 22
    bar, legend, x = [], [], float(LEFT)
    langs = languages(user["repositories"]["nodes"])
    for i, (name, part) in enumerate(langs):
        width = (RIGHT - LEFT) * part
        bar.append(f'<rect x="{x:.1f}" y="{bar_y:.1f}" width="{max(width - 2, 1):.1f}" height="8" rx="4" fill="{t["langs"][i]}"/>')
        x += width
    lx = float(LEFT)
    for i, (name, part) in enumerate(langs):
        legend.append(f'<circle cx="{lx + 5:.1f}" cy="{bar_y + 31:.1f}" r="5" fill="{t["langs"][i]}"/>')
        text = f"{name} {round(part * 100)}%"
        legend.append(f'<text x="{lx + 17:.1f}" y="{bar_y + 36:.1f}" class="muted" font-size="15">{text}</text>')
        lx += 17 + len(text) * 8.6 + 26
    body = "\n".join(head + cells + bar + legend)
    height = int(bar_y + 62)
    return frame(t, height, body, "", f"{cal['totalContributions']} contributions in the last year, as of {date.today().isoformat()}")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(t))
    if "--hero-only" in sys.argv:
        return
    user = fetch()
    for name, t in THEMES.items():
        (OUT / f"activity-{name}.svg").write_text(activity(t, user))


if __name__ == "__main__":
    main()

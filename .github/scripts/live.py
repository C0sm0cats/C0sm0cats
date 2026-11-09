"""Regenerate the live profile panels in assets/live/:

- activity-{dark,light}.svg: latest commits and releases across the featured repos
- contrib-{dark,light}.svg:  contribution calendar for the last year

Run daily by .github/workflows/badges.yml.
"""
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

OWNER = "C0sm0cats"
REPOS = {"SnapTess": 0, "SmartGrid": 0, "GMAIL": 1, "GDRIVE": 1, "lethe": 2, "the-source": 2, "naorush": 3}
OUT = Path(__file__).resolve().parents[2] / "assets" / "live"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
FONT = "ui-monospace,SFMono-Regular,'JetBrains Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"

THEMES = {
    "dark": dict(bg0="#070b14", bg1="#0d1424", frame="#26324a", text="#e6edf7", muted="#8b98ad", bar="#0b1120",
                 acc=["#22d3ee", "#a78bfa", "#e879f9", "#34d399"], gold="#fbbf24",
                 levels=["#141c2e", "#0e4f63", "#0891b2", "#8b5cf6", "#e879f9"]),
    "light": dict(bg0="#f7f9fc", bg1="#eef2f9", frame="#c9d2e0", text="#0f172a", muted="#526077", bar="#e9eef6",
                  acc=["#0e7490", "#6d28d9", "#a21caf", "#047857"], gold="#b45309",
                  levels=["#e3e8f1", "#a5e4f0", "#22b8d6", "#8b5cf6", "#c026d3"]),
}


def request(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-live"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def api(path):
    return request(f"https://api.github.com{path}")


def when(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def write(name, svg):
    p = OUT / name
    if not p.exists() or p.read_text() != svg:
        p.write_text(svg)
        print("updated", name)


# --- activity feed ----------------------------------------------------------
def events():
    ev = []
    for repo, col in REPOS.items():
        for c in api(f"/repos/{OWNER}/{repo}/commits?per_page=3") or []:
            msg = c["commit"]["message"].splitlines()[0]
            ev.append(dict(t=when(c["commit"]["committer"]["date"]), kind="commit", repo=repo, col=col, text=msg))
        rel = api(f"/repos/{OWNER}/{repo}/releases/latest")
        if rel:
            ev.append(dict(t=when(rel["published_at"]), kind="release", repo=repo, col=col, text=f"released {rel['tag_name']}"))
    ev.sort(key=lambda e: e["t"], reverse=True)
    picked, per_repo = [], {}
    for e in ev:  # at most two lines per repo so one busy project does not fill the feed
        if per_repo.get(e["repo"], 0) < 2:
            picked.append(e)
            per_repo[e["repo"]] = per_repo.get(e["repo"], 0) + 1
    return picked[:7]


def clip(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


def activity_svg(th, ev, now):
    W, ROW, TOP = 900, 27, 96
    H = TOP + len(ev) * ROW + 40
    rows = []
    for i, e in enumerate(ev):
        y = TOP + i * ROW
        a = th["acc"][e["col"]]
        mark = (f'<polygon points="118,{y-11} 125,{y-1} 111,{y-1}" fill="{th["gold"]}"/>' if e["kind"] == "release"
                else f'<circle cx="118" cy="{y-5}" r="4" fill="none" stroke="{a}" stroke-width="2"/>')
        msg_col = th["gold"] if e["kind"] == "release" else th["text"]
        rows.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.9 + i * 0.22:.2f}s" dur=".25s" fill="freeze"/>'
            f'<text x="32" y="{y}" fill="{th["muted"]}">{e["t"].strftime("%d %b")}</text>{mark}'
            f'<text x="140" y="{y}" fill="{a}" font-weight="700">{escape(e["repo"])}</text>'
            f'<text x="272" y="{y}" fill="{msg_col}">{escape(clip(e["text"], 66))}</text></g>')
    cy = TOP + len(ev) * ROW + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Latest activity across C0sm0cats projects">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{th['bg0']}"/><stop offset="1" stop-color="{th['bg1']}"/></linearGradient>
    <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{th['acc'][0]}" stop-opacity="0"/><stop offset=".5" stop-color="{th['acc'][0]}" stop-opacity=".9"/><stop offset="1" stop-color="{th['acc'][0]}" stop-opacity="0"/></linearGradient>
    <clipPath id="cp"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#cp)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="36" fill="{th['bar']}"/>
    <rect x="-200" y="35" width="200" height="2" fill="url(#sh)"><animate attributeName="x" values="-200;{W}" dur="6s" repeatCount="indefinite"/></rect>
  </g>
  <rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="none" stroke="{th['frame']}" stroke-width="1.5"/>
  <circle cx="22" cy="18" r="5" fill="{th['acc'][2]}" opacity=".85"/><circle cx="40" cy="18" r="5" fill="{th['acc'][1]}" opacity=".85"/><circle cx="58" cy="18" r="5" fill="{th['acc'][0]}" opacity=".85"/>
  <g font-family="{FONT}" font-size="14">
    <text x="{W/2}" y="23" text-anchor="middle" fill="{th['muted']}" font-size="12.5">~/C0sm0cats — activity</text>
    <text x="{W-20}" y="23" text-anchor="end" fill="{th['muted']}" font-size="11.5">synced {now.strftime('%d %b %Y')}</text>
    <text x="32" y="66" fill="{th['acc'][3]}" font-weight="700">$</text>
    <text x="50" y="66" fill="{th['text']}">git log --all-projects --since=recent<animate attributeName="opacity" values="0;1" dur=".4s" fill="freeze"/></text>
    {"".join(rows)}
    <text x="32" y="{cy + 18}" fill="{th['acc'][3]}" font-weight="700">$</text>
    <rect x="50" y="{cy + 4}" width="9" height="18" rx="1.5" fill="{th['acc'][0]}"><animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>
  </g>
</svg>
'''


# --- contribution calendar ---------------------------------------------------
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def calendar():
    q = '{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionLevel}}}}}}' % OWNER
    r = request("https://api.github.com/graphql", json.dumps({"query": q}).encode())
    return r["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def contrib_svg(th, cal):
    C, G, X0, Y0 = 12, 3, 62, 58
    weeks = cal["weeks"]
    W = 900
    H = Y0 + 7 * (C + G) + 38
    cells, months, last_month = [], [], None
    for wi, wk in enumerate(weeks):
        x = X0 + wi * (C + G)
        for d in wk["contributionDays"]:
            lv = LEVEL[d["contributionLevel"]]
            y = Y0 + d["weekday"] * (C + G)
            cells.append(f'<rect x="{x}" y="{y}" width="{C}" height="{C}" rx="3" fill="{th["levels"][lv]}"/>')
        m = wk["contributionDays"][0]["date"][:7]
        if m != last_month:
            if last_month is not None and wi < len(weeks) - 2:
                months.append(f'<text x="{x}" y="{Y0 - 8}">{datetime.strptime(m, "%Y-%m").strftime("%b")}</text>')
            last_month = m
    gw = len(weeks) * (C + G)
    legend_x = X0 + len(weeks) * (C + G) - 5 * (C + G) - 70
    legend = "".join(f'<rect x="{legend_x + 34 + i * (C + G)}" y="{H - 27}" width="{C}" height="{C}" rx="3" fill="{c}"/>' for i, c in enumerate(th["levels"]))
    days = "".join(f'<text x="{X0 - 10}" y="{Y0 + i * (C + G) + 10}" text-anchor="end">{n}</text>' for i, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{cal['totalContributions']} contributions in the last year">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{th['bg0']}"/><stop offset="1" stop-color="{th['bg1']}"/></linearGradient>
    <linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{th['acc'][0]}" stop-opacity="0"/><stop offset=".5" stop-color="{th['acc'][0]}" stop-opacity=".35"/><stop offset="1" stop-color="{th['acc'][0]}" stop-opacity="0"/></linearGradient>
    <clipPath id="cp"><rect width="{W}" height="{H}" rx="14"/></clipPath>
    <clipPath id="grid"><rect x="{X0}" y="{Y0}" width="{gw}" height="{7 * (C + G)}"/></clipPath>
  </defs>
  <g clip-path="url(#cp)"><rect width="{W}" height="{H}" fill="url(#bg)"/></g>
  <rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="none" stroke="{th['frame']}" stroke-width="1.5"/>
  <g font-family="{FONT}">
    <text x="{X0}" y="28" font-size="15" font-weight="700" fill="{th['text']}">{cal['totalContributions']:,} contributions <tspan fill="{th['muted']}" font-weight="400">in the last year</tspan></text>
    <g font-size="11" fill="{th['muted']}">{"".join(months)}{days}
      <text x="{legend_x + 26}" y="{H - 17}" text-anchor="end">less</text><text x="{legend_x + 34 + 5 * (C + G) + 4}" y="{H - 17}">more</text></g>
  </g>
  {"".join(cells)}
  {legend}
  <g clip-path="url(#grid)"><rect x="{X0 - 120}" y="{Y0}" width="120" height="{7 * (C + G)}" fill="url(#scan)"><animate attributeName="x" values="{X0 - 120};{X0 + gw}" dur="5s" repeatCount="indefinite"/></rect></g>
</svg>
'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    ev, cal = events(), calendar()
    for t, th in THEMES.items():
        write(f"activity-{t}.svg", activity_svg(th, ev, now))
        write(f"contrib-{t}.svg", contrib_svg(th, cal))


if __name__ == "__main__":
    main()

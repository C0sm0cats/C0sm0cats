"""Regenerate the project badges in assets/badges/ (release + last update).

Run daily by .github/workflows/badges.yml. Badges are served from this repo
so they never depend on a third-party badge service through GitHub's image proxy.
"""
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

OWNER = "C0sm0cats"
REPOS = {  # repo -> value colour (readable with white text)
    "SnapTess": "#0e7490", "SmartGrid": "#0e7490",
    "GMAIL": "#6d28d9", "GDRIVE": "#6d28d9",
    "lethe": "#1d4ed8", "the-source": "#a21caf",
    "naorush": "#047857",
}
LABEL_BG = "#0d1424"
OUT = Path(__file__).resolve().parents[2] / "assets" / "badges"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-badges"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def ago(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    days = (now.date() - d.date()).days
    if days <= 0: return "today"
    if days == 1: return "yesterday"
    if days < 7: return f"{days} days ago"
    if days < 30: return f"{days // 7} week{'s' if days >= 14 else ''} ago"
    return d.strftime("%B").lower() if d.year == now.year else d.strftime("%b %Y").lower()


def width(text):  # approx Verdana 11px advance
    narrow, wide = set("fijlrt.,:;'|! "), set("mwMW")
    return sum(4 if c in narrow else 10 if c in wide else 7 for c in text)


def badge(label, value, color):
    lw, vw = width(label) + 12, width(value) + 12
    w = lw + vw
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{esc(label)}: {esc(value)}">
  <title>{esc(label)}: {esc(value)}</title>
  <rect width="{lw}" height="20" fill="{LABEL_BG}"/><rect x="{lw}" width="{vw}" height="20" fill="{color}"/>
  <g fill="#fff" font-family="Verdana,Geneva,'DejaVu Sans',sans-serif" font-size="11" text-rendering="geometricPrecision">
    <text x="6" y="14" textLength="{lw - 12}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>
    <text x="{lw + 6}" y="14" textLength="{vw - 12}" lengthAdjust="spacingAndGlyphs">{esc(value)}</text>
  </g>
</svg>
'''


def write(name, svg):
    p = OUT / name
    if not p.exists() or p.read_text() != svg:
        p.write_text(svg)
        print("updated", name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for repo, color in REPOS.items():
        rel = api(f"/repos/{OWNER}/{repo}/releases/latest")
        if rel:
            write(f"{repo}-release.svg", badge("release", rel["tag_name"], color))
        commits = api(f"/repos/{OWNER}/{repo}/commits?per_page=1")
        if commits:
            write(f"{repo}-updated.svg", badge("updated", ago(commits[0]["commit"]["committer"]["date"]), color))


if __name__ == "__main__":
    main()

"""Builds README.md from the project list (descriptions, colours, order).

Run through tools/build.sh from the repository root."""
GH = "https://github.com/C0sm0cats"
RAW = "https://raw.githubusercontent.com/C0sm0cats"
SH = "https://img.shields.io"
ST = "style=flat-square&labelColor=0d1424"
import hashlib

def v(path):
    """Content hash query so browsers refetch a changed asset."""
    return path + "?v=" + hashlib.sha1(open(path, "rb").read()).hexdigest()[:8]

COL = dict(cyan="0e7490", violet="6d28d9", magenta="a21caf", green="047857", blue="1d4ed8")

def badges(repo, color, release=True):
    c = COL[color]; b = []
    if release:
        b.append(f'<a href="{GH}/{repo}/releases/latest"><img src="{v(f'assets/badges/{repo}-release.svg')}" alt="Latest release"></a>')
    b.append(f'<a href="{GH}/{repo}/commits"><img src="{v(f'assets/badges/{repo}-updated.svg')}" alt="Last update"></a>')
    return " ".join(b)

def tags(*t): return " · ".join(f"<code>{x}</code>" for x in t)

def body(p):
    return (f'{badges(p["repo"], p["color"], p.get("release", True))}<br><br>'
            f'{p["desc"]}<br><br>{tags(*p["tags"])}' + (f'<br><br>{p["cta"]}' if p["cta"] else ''))

def image(p, width="100%"):
    return f'<a href="{p["href"]}"><img src="{RAW}/{p["repo"]}/main/{p["img"]}" alt="{p["alt"]}" width="{width}"></a>'

def title(p):
    k = p["repo"].lower()
    return (f'<a href="{GH}/{p["repo"]}"><picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="{v(f'assets/headers/{k}-dark.svg')}">'
            f'<img src="{v(f'assets/headers/{k}-light.svg')}" alt="{p["name"]}" width="100%"></picture></a>')

def pic(base, alt, width=None):
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{v(f'{base}-dark.svg')}">'
            f'<img src="{v(f'{base}-light.svg')}" alt="{alt}"{w}></picture>')

SECTIONS = {"Window management": "window", "Terminal tools for Google Workspace": "workspace", "AI coding agents": "ai",
            "Writing": "writing", "Game": "game", "Activity": "activity", "Stack": "stack"}

def heading(section):
    return f'{pic("assets/sections/" + SECTIONS[section], section, "100%")}\n\n'

def button(href, key, label, width):
    return f'<a href="{href}">{pic("assets/buttons/" + key, label, width)}</a>'

SIDE = {"n": 0}

def block(p):
    side = "left" if SIDE["n"] % 2 == 0 else "right"
    SIDE["n"] += 1
    img = (f'<a href="{p["href"]}"><img src="{RAW}/{p["repo"]}/main/{p["img"]}" alt="{p["alt"]}" '
           f'width="47%" align="{side}"></a>')
    k = p["repo"].lower()
    head = (f'<a href="{GH}/{p["repo"]}"><picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="{v(f'assets/headers/{k}-dark.svg')}">'
            f'<img src="{v(f'assets/headers/{k}-light.svg')}" alt="{p["name"]}" width="46%"></picture></a>')
    return f'<p>\n{img}\n{head}<br><br>\n{body(p)}\n</p>\n<br clear="all">\n'

def pair(section, a, b):
    return f"{heading(section)}{block(a)}\n{block(b)}"

def solo(section, p, image_left=True):
    return f"{heading(section)}{block(p)}"

def rel(repo): return ""

P = {
 "snap": dict(repo="SnapTess", name="SnapTess", icon="🐧", color="cyan", img="docs/snaptess-overview-blurred.png", alt="SnapTess tiling windows on GNOME", href=f"{GH}/SnapTess",
   desc="Automatic window tiling for <strong>GNOME 50–51 on Wayland</strong>. Grid &amp; split layouts, drag-to-snap, Layout Studio, linked tile resize, keyboard-driven focus and independent spaces per monitor.",
   tags=("GNOME Shell extension", "GJS", "Wayland"), cta=rel("SnapTess")),
 "smart": dict(repo="SmartGrid", name="SmartGrid", icon="🪟", color="cyan", img="docs/smartgrid-overview.png", alt="SmartGrid tiling windows on Windows 11", href=f"{GH}/SmartGrid",
   desc="Automatic tiling window manager for <strong>Windows 10/11</strong> — a FancyZones alternative. Layout studio, custom grids, snap &amp; swap, virtual desktops, global hotkeys.",
   tags=("Python", "Qt", "Win32"), cta=rel("SmartGrid")),
 "gmail": dict(repo="GMAIL", name="GMAIL", icon="📬", color="violet", img="docs/screenshot.svg", alt="GMAIL terminal UI", href=f"{GH}/GMAIL",
   desc="<strong>Gmail in your terminal.</strong> Browse and triage Inbox, Sent, Spam and Trash (archive, star, undo), and save emails as PDFs with their attachments.",
   tags=("Python", "TUI", "Gmail API", "Playwright"), cta=rel("GMAIL")),
 "gdrive": dict(repo="GDRIVE", name="GDRIVE", icon="📁", color="violet", img="docs/screenshot.svg", alt="GDRIVE terminal UI", href=f"{GH}/GDRIVE",
   desc="<strong>Google Drive in your terminal.</strong> Two-way sync of the folders you pick across My Drive, shared items and shared drives, preview every change on both sides, then sync safely: conflicts kept, deletions to the trash, Docs/Sheets/Slides export.",
   tags=("Python", "TUI", "Textual", "Drive API"), cta=rel("GDRIVE")),
 "lethe": dict(repo="lethe", name="lethe", icon="🤖", color="blue", img="docs/demo.svg", alt="lethe picker listing Claude Code and Codex sessions", href=f"{GH}/lethe",
   desc="<strong>Browse, resume and forget your Claude Code and Codex sessions</strong> from one terminal picker. Live preview, resume in the original directory, bulk cleanup with undo; running sessions are never touched. Scriptable with <code>--json</code>, <code>--dry-run</code> and cron.",
   tags=("Bash", "fzf", "Claude Code", "Codex"), cta=rel("lethe")),
 "source": dict(repo="the-source", name="The Source", icon="📖", color="magenta", release=False, img="assets/hero.svg", alt="The Source: a burst of coloured light strands radiating from a single origin", href="https://c0sm0cats.github.io/the-source/en/",
   desc="A bilingual (FR/EN) vision of <strong>consciousness, infinity and return</strong>, told one idea at a time, each with an interactive generative figure. Also as two illustrated books.",
   tags=("Generative art", "FR / EN"), cta=button("https://c0sm0cats.github.io/the-source/en/", "read-online", "Read online", 149) + " " + button("https://c0sm0cats.github.io/the-source/", "lire-en-francais", "Lire en français", 187)),
 "nao": dict(repo="naorush", name="NAO Rush", icon="🎮", color="green", release=False, img="docs/title.jpg", alt="NAO Rush title screen", href="https://c0sm0cats.github.io/naorush/",
   desc="A <strong>2D browser platformer</strong> set in Inetum's offices, Rick Dangerous / Prince of Persia style: cross five stages, convince the directors, get the raise envelope signed. No engine dependency, PC/tablet/mobile.",
   tags=("JavaScript", "WebGL2"), cta=button("https://c0sm0cats.github.io/naorush/", "play-now", "Play now", 125)),
}

out = f'''<a href="{GH}">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="C0sm0cats — DevOps engineer building open-source tiling window managers and terminal tools for Linux and Windows" width="100%">
  </picture>
</a>

{pair("Window management", P["snap"], P["smart"])}
{pair("Terminal tools for Google Workspace", P["gmail"], P["gdrive"])}
{solo("AI coding agents", P["lethe"], image_left=True)}
{solo("Writing", P["source"], image_left=False)}
{solo("Game", P["nao"], image_left=True)}
{heading("Activity")}{pic("assets/live/activity", "Latest commits and releases across my projects", "100%")}

{pic("assets/live/contrib", "Contribution calendar for the last year", "100%")}

{heading("Stack")}
<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img src="assets/stack-light.svg" alt="Linux · Windows · Docker · Python · JavaScript · Bash · Qt · GitHub Actions">
</picture></p>

<br>

<a href="{GH}?tab=repositories">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
    <img src="assets/footer-light.svg" alt="Thanks for stopping by — find something useful? A star helps others discover it." width="100%">
  </picture>
</a>
'''
open("README.md", "w").write(out)

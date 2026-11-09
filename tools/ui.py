"""Section titles and CTA buttons -> assets/sections/, assets/buttons/.

Run through tools/build.sh from the repository root."""
import sys
root = sys.argv[1]
FONT = "ui-monospace,SFMono-Regular,'JetBrains Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
TH = {
 "dark": dict(text="#e6edf7", muted="#8b98ad", bg0="#0b1120", bg1="#111a2e", frame="#26324a",
              acc=dict(cyan="#22d3ee", violet="#a78bfa", magenta="#e879f9", green="#34d399", blue="#60a5fa")),
 "light": dict(text="#0f172a", muted="#526077", bg0="#f7f9fc", bg1="#eef2f9", frame="#c9d2e0",
               acc=dict(cyan="#0e7490", violet="#6d28d9", magenta="#a21caf", green="#047857", blue="#1d4ed8")),
}
NEXT = dict(cyan="violet", violet="blue", magenta="violet", green="cyan", blue="cyan")
SECTIONS = [("window", "Window management", "cyan"), ("workspace", "Terminal tools for Google Workspace", "violet"),
            ("ai", "AI coding agents", "blue"), ("writing", "Writing", "magenta"), ("game", "Game", "green"),
            ("activity", "Activity", "cyan"), ("stack", "Stack", "violet")]

def fit(text, fs, room):
    w = len(text) * fs * .6
    return f' textLength="{room}" lengthAdjust="spacingAndGlyphs"' if w > room else ""

def section(th, title, col, uid):
    a, b = th["acc"][col], th["acc"][NEXT[col]]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 56" width="900" height="56" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="ln{uid}" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset=".45" stop-color="{b}" stop-opacity=".55"/><stop offset="1" stop-color="{b}" stop-opacity="0"/></linearGradient>
    <radialGradient id="dot{uid}"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>.m{{display:none}}@media (max-width:600px){{.d{{display:none}}.m{{display:inline}}}}</style>
  <g class="d"><polygon points="2,40 24,18 24,40" fill="{a}"/>
  <text x="36" y="38" font-family="{FONT}" font-size="25" font-weight="800" fill="{th['text']}">{title}</text></g>
  <g class="m"><polygon points="2,44 32,12 32,44" fill="{a}"/>
  <text x="46" y="44" font-family="{FONT}" font-size="44" font-weight="800" fill="{th['text']}"{fit(title, 44, 850)}>{title}</text></g>
  <rect x="0" y="50" width="900" height="2" rx="1" fill="url(#ln{uid})"/>
  <ellipse cx="0" cy="51" rx="40" ry="3.5" fill="url(#dot{uid})"><animate attributeName="cx" values="-40;940" dur="4.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0" keyTimes="0;.55;.8" dur="4.5s" repeatCount="indefinite"/></ellipse>
</svg>
'''

def icon(kind, c):
    if kind == "book":
        return f'<path d="M0 3 q7-3 12 0 v14 q-5-3-12 0 z M12 3 q5-3 12 0 v14 q-7-3-12 0" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
    if kind == "play":
        return f'<polygon points="4,1 21,10 4,19" fill="{c}"/>'
    if kind == "globe":
        return f'<circle cx="11" cy="10" r="9" fill="none" stroke="{c}" stroke-width="2"/><ellipse cx="11" cy="10" rx="4" ry="9" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M2 10 h18" stroke="{c}" stroke-width="1.6"/>'

BUTTONS = [("read-online", "Read online", "magenta", "book", True), ("lire-en-francais", "Lire en français", "magenta", "globe", False),
           ("play-now", "Play now", "green", "play", True)]

def button(th, label, col, kind, primary, uid):
    a = th["acc"][col]
    W = 64 + int(len(label) * 10.2) + 22
    fill = f'<rect x="1" y="1" width="{W-2}" height="44" rx="22" fill="{a}" fill-opacity="{".16" if primary else ".0"}"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 46" width="{W}" height="46" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="bg{uid}" x1="0" x2="1"><stop offset="0" stop-color="{th['bg0']}"/><stop offset="1" stop-color="{th['bg1']}"/></linearGradient>
    <linearGradient id="sh{uid}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <clipPath id="cp{uid}"><rect x="1" y="1" width="{W-2}" height="44" rx="22"/></clipPath>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="44" rx="22" fill="url(#bg{uid})"/>
  {fill}
  <g clip-path="url(#cp{uid})"><rect x="-80" y="0" width="60" height="46" fill="url(#sh{uid})" transform="skewX(-20)"><animate attributeName="x" values="-80;-80;{W+40}" keyTimes="0;.6;1" dur="4s" repeatCount="indefinite"/></rect></g>
  <rect x="1" y="1" width="{W-2}" height="44" rx="22" fill="none" stroke="{a}" stroke-width="{2 if primary else 1.5}" stroke-opacity="{1 if primary else .7}"/>
  <g transform="translate(22 13)">{icon(kind, a)}</g>
  <text x="56" y="29" font-family="{FONT}" font-size="16" font-weight="{800 if primary else 600}" fill="{a if primary else th['text']}">{label}</text>
</svg>
'''

for t, th in TH.items():
    for key, title, col in SECTIONS:
        open(f"{root}/sections/{key}-{t}.svg", "w").write(section(th, title, col, f"{key}{t[0]}"))
    for key, label, col, kind, primary in BUTTONS:
        open(f"{root}/buttons/{key}-{t}.svg", "w").write(button(th, label, col, kind, primary, f"{key[:4]}{t[0]}"))

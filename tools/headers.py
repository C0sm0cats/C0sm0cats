"""Per-project header banners -> assets/headers/<repo>-{dark,light}.svg.

Run through tools/build.sh from the repository root."""
import sys
out = sys.argv[1]
FONT = "ui-monospace,SFMono-Regular,'JetBrains Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
TH = {
 "dark": dict(bg0="#0b1120", bg1="#111a2e", frame="#26324a", text="#e6edf7", muted="#8b98ad",
              acc=dict(cyan="#22d3ee", violet="#a78bfa", magenta="#e879f9", green="#34d399", blue="#60a5fa"),
              acc2=dict(cyan="#a78bfa", violet="#60a5fa", magenta="#a78bfa", green="#22d3ee", blue="#22d3ee")),
 "light": dict(bg0="#f7f9fc", bg1="#eef2f9", frame="#c9d2e0", text="#0f172a", muted="#526077",
               acc=dict(cyan="#0e7490", violet="#6d28d9", magenta="#a21caf", green="#047857", blue="#1d4ed8"),
               acc2=dict(cyan="#6d28d9", violet="#1d4ed8", magenta="#6d28d9", green="#0e7490", blue="#0e7490")),
}
# icons drawn in a 40x40 box at (24,20)
def icon(kind, a, b):
    S = lambda c: f'fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"'
    s = S(a)
    if kind == "tiles-gnome":
        return f'<rect x="0" y="0" width="22" height="40" rx="4" {s}/><rect x="26" y="0" width="14" height="18" rx="4" {s}/><rect x="26" y="22" width="14" height="18" rx="4" stroke="{b}" fill="{b}" fill-opacity=".25" stroke-width="2.2"/>'
    if kind == "tiles-win":
        return f'<rect x="0" y="0" width="18" height="18" rx="3" {s}/><rect x="22" y="0" width="18" height="18" rx="3" {s}/><rect x="0" y="22" width="18" height="18" rx="3" {s}/><rect x="22" y="22" width="18" height="18" rx="3" stroke="{b}" fill="{b}" fill-opacity=".25" stroke-width="2.2"/>'
    if kind == "mail":
        return f'<rect x="0" y="6" width="40" height="28" rx="4" {s}/><path d="M2 9 L20 23 L38 9" {S(b)}/>'
    if kind == "folder":
        return f'<path d="M0 10 a3 3 0 0 1 3-3 h11 l4 5 h19 a3 3 0 0 1 3 3 v19 a3 3 0 0 1-3 3 h-34 a3 3 0 0 1-3-3 z" {s}/><path d="M14 24 h12 m-4 -4 l4 4 -4 4" {S(b)}/>'
    if kind == "term":
        return f'<rect x="0" y="2" width="40" height="36" rx="4" {s}/><path d="M8 14 l7 6 -7 6" {S(b)}/><path d="M19 27 h12" {s}/>'
    if kind == "burst":
        rays = "".join(f'<line x1="20" y1="20" x2="{20+18*__import__("math").cos(k*0.5236):.1f}" y2="{20+18*__import__("math").sin(k*0.5236):.1f}" stroke="{a if k%2 else b}" stroke-width="2" stroke-linecap="round"/>' for k in range(12))
        return rays + f'<circle cx="20" cy="20" r="4.5" fill="{a}"/>'
    if kind == "pad":
        return f'<rect x="0" y="8" width="40" height="24" rx="12" {s}/><path d="M10 16 v8 M6 20 h8" {S(b)}/><circle cx="28" cy="17" r="2.2" fill="{a}"/><circle cx="32" cy="23" r="2.2" fill="{b}"/>'

P = [
 ("snaptess", "SnapTess", "GNOME 50 · Wayland tiling", "cyan", "tiles-gnome"),
 ("smartgrid", "SmartGrid", "Windows 10/11 tiling", "cyan", "tiles-win"),
 ("gmail", "GMAIL", "Gmail in your terminal", "violet", "mail"),
 ("gdrive", "GDRIVE", "Google Drive sync TUI", "violet", "folder"),
 ("lethe", "lethe", "AI coding session picker", "blue", "term"),
 ("the-source", "The Source", "a vision of consciousness · FR / EN", "magenta", "burst"),
 ("naorush", "NAO Rush", "browser platformer", "green", "pad"),
]

def svg(th, name, sub, col, kind, uid):
    a, b = th["acc"][col], th["acc2"][col]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 76" width="400" height="76" role="img" aria-label="{name} — {sub}">
  <defs>
    <linearGradient id="bg{uid}" x1="0" x2="1"><stop offset="0" stop-color="{th['bg0']}"/><stop offset="1" stop-color="{th['bg1']}"/></linearGradient>
    <radialGradient id="gl{uid}" cx=".08" cy=".5" r=".35"><stop offset="0" stop-color="{a}" stop-opacity=".28"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
    <linearGradient id="nm{uid}" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-.4 0;.4 0;-.4 0" dur="7s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="sh{uid}" x1="0" x2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}" stop-opacity=".9"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
    <clipPath id="cp{uid}"><rect x="1" y="1" width="398" height="74" rx="11"/></clipPath>
  </defs>
  <g clip-path="url(#cp{uid})">
    <rect width="400" height="76" fill="url(#bg{uid})"/>
    <rect width="400" height="76" fill="url(#gl{uid})"/>
    <rect x="-120" y="73" width="120" height="3" fill="url(#sh{uid})"><animate attributeName="x" values="-120;400" dur="5s" repeatCount="indefinite"/></rect>
  </g>
  <rect x="1" y="1" width="398" height="74" rx="11" fill="none" stroke="{th['frame']}" stroke-width="1.5"/>
  <style>.m{{display:none}}@media (max-width:300px){{.d{{display:none}}.m{{display:inline}}}}</style>
  <g class="d">
  <g transform="translate(18 18)">{icon(kind, a, b)}</g>
  <g font-family="{FONT}">
    <text x="74" y="39" font-size="26" font-weight="800" fill="url(#nm{uid})">{name}</text>
    <text x="75" y="59" font-size="13" fill="{th['muted']}">{sub}</text>
  </g>
  <g fill="{th['muted']}" opacity=".7"><path d="M372 32 l7 6 -7 6" fill="none" stroke="{th['muted']}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><animate attributeName="opacity" values=".3;1;.3" dur="2.4s" repeatCount="indefinite"/></path></g>
  </g>
  <g class="m">
  <g transform="translate(14 10) scale(1.4)">{icon(kind, a, b)}</g>
  <text x="90" y="52" font-family="{FONT}" font-size="40" font-weight="800" fill="url(#nm{uid})"{' textLength="296" lengthAdjust="spacingAndGlyphs"' if len(name) * 24 > 296 else ''}>{name}</text>
  </g>
</svg>
'''
for slug, name, sub, col, kind in P:
    for t, th in TH.items():
        open(f"{out}/{slug}-{t}.svg", "w").write(svg(th, name, sub, col, kind, f"{slug[:3]}{t[0]}"))

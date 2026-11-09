"""Animated top banner -> assets/banner-{dark,light}.svg (desktop + mobile layout).

Run through tools/build.sh from the repository root."""
import sys
out = sys.argv[1]

THEMES = {
  "dark": dict(bg0="#070b14", bg1="#0d1424", grid="#1b2740", text="#e6edf7", muted="#8b98ad",
               c=["#22d3ee", "#a78bfa", "#e879f9", "#34d399"], frame="#26324a", star="#cfe8ff", tileop=".10", glow=".55"),
  "light": dict(bg0="#f7f9fc", bg1="#eef2f9", grid="#dfe5ef", text="#0f172a", muted="#526077",
                c=["#0e7490", "#6d28d9", "#a21caf", "#047857"], frame="#c9d2e0", star="#94a3b8", tileop=".10", glow=".25"),
}

FONT = "ui-monospace,SFMono-Regular,'JetBrains Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
PHRASES = [
  "tiling window managers for GNOME & Windows",
  "terminal tools for Gmail & Google Drive",
  "a session picker for AI coding agents",
  "generative art & a browser platformer",
]
CW, FS, TX, TY = 12.6, 21, 64, 214   # char width (textLength forced), font size, x, baseline
PROMPT = "$ "

# --- typing timeline -------------------------------------------------------
TYPE, DEL, HOLD, GAP = 0.055, 0.022, 1.8, 0.35
events = []  # (t, phrase_idx, chars)
t = 0.0
for i, p in enumerate(PHRASES):
    n = len(p)
    for k in range(n + 1):
        events.append((t + k * TYPE, i, k))
    t += n * TYPE + HOLD
    for k in range(n - 1, -1, -1):
        t += DEL
        events.append((t, i, k))
    t += GAP
TOTAL = round(t, 3)

def discrete(series):
    """series: list of (t, value) -> keyTimes/values for calcMode=discrete"""
    kt, vals = [], []
    last = None
    for tt, v in series:
        if v == last:
            continue
        kt.append(tt / TOTAL); vals.append(v); last = v
    if kt[0] != 0:
        kt.insert(0, 0); vals.insert(0, 0)
    return ";".join(f"{k:.5f}" for k in kt), ";".join(str(v) for v in vals)

px = TX + len(PROMPT) * CW

def typing_svg(th, tx=TX, ty=TY, cw=CW, fs=FS, uid=""):
    px = tx + len(PROMPT) * cw
    k = fs / FS
    parts = []
    for i, p in enumerate(PHRASES):
        series = [(0, 0)] + [(tt, round(n * cw, 1)) for tt, j, n in events if j == i]
        series.sort()
        kt, vals = discrete(series)
        parts.append(f'''<clipPath id="tc{uid}{i}"><rect x="{px}" y="{ty-24*k:.1f}" height="{34*k:.1f}" width="0">
      <animate attributeName="width" dur="{TOTAL}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/></rect></clipPath>
    <text x="{px}" y="{ty}" textLength="{len(p)*cw:.1f}" lengthAdjust="spacing" clip-path="url(#tc{uid}{i})" fill="{th['text']}">{p.replace('&','&amp;')}</text>''')
    cur = sorted([(tt, round(px + n * cw, 1)) for tt, j, n in events])
    kt, vals = discrete([(0, px)] + cur)
    vals = vals.split(";"); vals[0] = str(px); vals = ";".join(vals)
    parts.append(f'''<rect y="{ty-18*k:.1f}" width="{cw-2*k:.1f}" height="{22*k:.1f}" rx="1.5" fill="{th['c'][0]}">
      <animate attributeName="x" dur="{TOTAL}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>
      <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.5" values="1;0"/></rect>''')
    return "\n    ".join(parts)

# --- tiling monitor --------------------------------------------------------
X0, Y0, W, H, G = 772, 86, 368, 172, 8
def lay_master():
    mw = round((W - G) * .58); rw = W - mw - G; rh = (H - 2 * G) / 3
    return [(X0, Y0, mw, H)] + [(X0 + mw + G, Y0 + k * (rh + G), rw, rh) for k in range(3)]
def lay_grid():
    w = (W - G) / 2; h = (H - G) / 2
    return [(X0, Y0, w, h), (X0 + w + G, Y0, w, h), (X0, Y0 + h + G, w, h), (X0 + w + G, Y0 + h + G, w, h)]
def lay_cols():
    w = (W - 2 * G) / 3; h = (H - G) / 2
    return [(X0, Y0, w, H), (X0 + w + G, Y0, w, H), (X0 + 2 * (w + G), Y0, w, h), (X0 + 2 * (w + G), Y0 + h + G, w, h)]
def lay_swap():  # master on the right
    mw = round((W - G) * .58); lw = W - mw - G; lh = (H - 2 * G) / 3
    return [(X0 + lw + G, Y0, mw, H)] + [(X0, Y0 + k * (lh + G), lw, lh) for k in range(3)]

LAYS = [lay_master(), lay_grid(), lay_cols(), lay_swap()]
TD = 12
# hold / move per layout, cycle back to first
kts, spl = [], []
n = len(LAYS)
for i in range(n):
    a = i / n; b = a + (1 / n) * .82
    kts += [a, b]
kts.append(1)
seq = [L for L in LAYS for _ in (0, 1)] + [LAYS[0]]
splines = ";".join(["0 0 1 1", ".65 0 .25 1"] * n)
ktstr = ";".join(f"{k:.4f}" for k in kts)

def tiles_svg(th):
    out = []
    for ti in range(4):
        col = th["c"][ti]
        anims = []
        for ai, attr in enumerate(("x", "y", "width", "height")):
            vals = ";".join(f"{L[ti][ai]:.1f}" for L in seq)
            anims.append(f'<animate attributeName="{attr}" dur="{TD}s" repeatCount="indefinite" calcMode="spline" keyTimes="{ktstr}" keySplines="{splines}" values="{vals}"/>')
        x, y, w, h = LAYS[0][ti]
        a = "".join(anims)
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{col}" fill-opacity="{th["tileop"]}" stroke="{col}" stroke-width="1.6">{a}</rect>')
        # header bar inside each tile (same geometry, thin)
        hb = []
        for ai, attr in enumerate(("x", "y", "width")):
            vals = ";".join(f"{(L[ti][ai] + (0 if ai == 2 else 0)):.1f}" for L in seq)
            hb.append(f'<animate attributeName="{attr}" dur="{TD}s" repeatCount="indefinite" calcMode="spline" keyTimes="{ktstr}" keySplines="{splines}" values="{vals}"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="7" fill="{col}" fill-opacity=".35">{"".join(hb)}</rect>')
    return "\n    ".join(out)

STARS = [(520, 40, 1.2, 0), (600, 268, 1, 1.3), (690, 30, 1.4, 2.1), (1160, 40, 1.1, .7), (1180, 290, 1.3, 2.8),
         (40, 290, 1, 1.9), (470, 290, 1.2, .4), (420, 56, .9, 3.1), (735, 300, 1, 1.1), (1110, 300, .9, 2.4)]

def svg(name):
    th = THEMES[name]; c = th["c"]
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{th["star"]}"><animate attributeName="opacity" dur="3.6s" begin="{d}s" repeatCount="indefinite" values=".15;1;.15"/></circle>' for x, y, r, d in STARS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 330" width="1200" height="330" role="img" aria-label="C0sm0cats — DevOps engineer building tiling window managers, terminal tools and AI agent tooling">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{th['bg0']}"/><stop offset="1" stop-color="{th['bg1']}"/></linearGradient>
    <radialGradient id="g1" cx=".82" cy=".5" r=".45"><stop offset="0" stop-color="{c[1]}" stop-opacity=".22"/><stop offset="1" stop-color="{c[1]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx=".12" cy=".2" r=".5"><stop offset="0" stop-color="{c[0]}" stop-opacity=".16"/><stop offset="1" stop-color="{c[0]}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{th['grid']}" stroke-width="1"/></pattern>
    <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".55" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity=".6"/></linearGradient>
    <mask id="gm"><rect width="1200" height="330" fill="url(#fade)"/></mask>
    <linearGradient id="name" x1="0" x2="1" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="{c[0]}"/><stop offset=".5" stop-color="{c[1]}"/><stop offset="1" stop-color="{c[2]}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-.5 0;.5 0;-.5 0" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>
    <linearGradient id="scan" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{c[0]}" stop-opacity="0"/><stop offset=".5" stop-color="{c[0]}" stop-opacity=".18"/><stop offset="1" stop-color="{c[0]}" stop-opacity="0"/></linearGradient>
    <clipPath id="card"><rect width="1200" height="330" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
  <rect width="1200" height="330" fill="url(#bg)"/>
  <rect width="1200" height="330" fill="url(#grid)" mask="url(#gm)" opacity=".7"/>
  <rect width="1200" height="330" fill="url(#g1)"/>
  <rect width="1200" height="330" fill="url(#g2)"/>
  {stars}
  <rect x="0" y="-60" width="1200" height="60" fill="url(#scan)"><animate attributeName="y" values="-60;330" dur="7s" repeatCount="indefinite"/></rect>

  <style>.m{{display:none}}@media (max-width:600px){{.d{{display:none}}.m{{display:inline}}}}</style>
  <g class="m" font-family="{FONT}">
    <text x="62" y="96" font-size="30" letter-spacing="6" fill="{th['muted']}">DEVOPS ENGINEER</text>
    <text x="56" y="205" font-size="146" font-weight="800" fill="url(#name)" filter="url(#glow)" opacity="{th['glow']}">C0sm0cats</text>
    <text x="56" y="205" font-size="146" font-weight="800" fill="url(#name)">C0sm0cats</text>
    <g font-size="42">
    <text x="62" y="282" fill="{c[3]}" font-weight="700">{PROMPT.strip()}</text>
    {typing_svg(th, 62, 282, 25.2, 42, "m")}
    </g>
  </g>
  <g class="d" font-family="{FONT}">
    <text x="{TX}" y="76" font-size="14" letter-spacing="4" fill="{th['muted']}">DEVOPS ENGINEER · LINUX &amp; WINDOWS</text>
    <text x="{TX-2}" y="150" font-size="68" font-weight="800" fill="url(#name)" filter="url(#glow)" opacity="{th['glow']}">C0sm0cats</text>
    <text x="{TX-2}" y="150" font-size="68" font-weight="800" fill="url(#name)">C0sm0cats</text>
    <g font-size="{FS}">
    <text x="{TX}" y="{TY}" fill="{c[3]}" font-weight="700">{PROMPT.strip()}</text>
    {typing_svg(th)}
    </g>
    <text x="{TX}" y="276" font-size="13" fill="{th['muted']}">GNOME Shell · Wayland · Win32 · Python · TUI · Google APIs · AI coding agents</text>
  </g>

  <g class="d">
  <rect x="756" y="50" width="400" height="224" rx="14" fill="{th['bg0']}" fill-opacity=".55" stroke="{th['frame']}" stroke-width="1.5"/>
  <circle cx="776" cy="68" r="4.5" fill="{c[2]}" opacity=".8"/><circle cx="792" cy="68" r="4.5" fill="{c[1]}" opacity=".8"/><circle cx="808" cy="68" r="4.5" fill="{c[0]}" opacity=".8"/>
  <text x="1140" y="72" text-anchor="end" font-family="{FONT}" font-size="11" fill="{th['muted']}">layout: auto</text>
  <g>
    {tiles_svg(th)}
  </g>
  <rect x="756" y="50" width="400" height="224" rx="14" fill="none" stroke="{c[0]}" stroke-opacity=".35" stroke-width="1"><animate attributeName="stroke-opacity" values=".1;.5;.1" dur="4s" repeatCount="indefinite"/></rect>
  </g>
  </g>
</svg>
'''

for name in THEMES:
    open(f"{out}/banner-{name}.svg", "w").write(svg(name))
print("total typing loop", TOTAL)

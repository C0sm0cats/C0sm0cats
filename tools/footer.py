"""Animated footer banner -> assets/footer-{dark,light}.svg.

Run through tools/build.sh from the repository root."""
import sys, math
out=sys.argv[1]
FONT = "ui-monospace,SFMono-Regular,'JetBrains Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
TH = {
 "dark": dict(bg0="#070b14", bg1="#0d1424", grid="#1b2740", frame="#26324a", text="#e6edf7", muted="#8b98ad", star="#cfe8ff",
              c=["#22d3ee", "#a78bfa", "#e879f9", "#34d399"], gold="#fbbf24"),
 "light": dict(bg0="#f7f9fc", bg1="#eef2f9", grid="#dfe5ef", frame="#c9d2e0", text="#0f172a", muted="#526077", star="#94a3b8",
               c=["#0e7490", "#6d28d9", "#a21caf", "#047857"], gold="#b45309"),
}
def star(cx, cy, R, r):
    pts=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5; rr=R if k%2==0 else r
        pts.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return " ".join(pts)
DOTS=[(70,30,1.1,0),(150,96,1,1.2),(420,20,1.3,2),(640,104,1,.6),(760,24,1.2,2.6),(850,92,1,1.7),(870,30,.9,.3),(30,96,1,2.2)]
def svg(t):
    th=TH[t]; c=th["c"]
    dots="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{th["star"]}"><animate attributeName="opacity" dur="3.6s" begin="{d}s" repeatCount="indefinite" values=".15;1;.15"/></circle>' for x,y,r,d in DOTS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 120" width="900" height="120" role="img" aria-label="Thanks for stopping by — find something useful? A star helps others discover it.">
  <defs>
    <linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{th['bg1']}"/><stop offset="1" stop-color="{th['bg0']}"/></linearGradient>
    <radialGradient id="gl" cx=".5" cy=".5" r=".4"><stop offset="0" stop-color="{c[1]}" stop-opacity=".18"/><stop offset="1" stop-color="{c[1]}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{th['grid']}" stroke-width="1"/></pattern>
    <linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset=".5" stop-color="{c[1]}"/><stop offset="1" stop-color="{c[2]}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-.5 0;.5 0;-.5 0" dur="8s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{c[0]}" stop-opacity="0"/><stop offset=".5" stop-color="{c[0]}" stop-opacity=".9"/><stop offset="1" stop-color="{c[0]}" stop-opacity="0"/></linearGradient>
    <filter id="sg" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>
    <clipPath id="cp"><rect width="900" height="120" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#cp)">
    <rect width="900" height="120" fill="url(#bg)"/>
    <rect width="900" height="120" fill="url(#grid)" opacity=".5"/>
    <rect width="900" height="120" fill="url(#gl)"/>
    {dots}
    <rect x="-240" y="0" width="240" height="2" fill="url(#sh)"><animate attributeName="x" values="-240;900" dur="6s" repeatCount="indefinite"/></rect>
  </g>
  <rect x=".75" y=".75" width="898.5" height="118.5" rx="16" fill="none" stroke="{th['frame']}" stroke-width="1.5"/>
  <style>.m{{display:none}}@media (max-width:600px){{.d{{display:none}}.m{{display:inline}}}}</style>
  <g class="m">
    <polygon transform="translate(84 60)" points="{star(0,0,36,15)}" fill="{th['gold']}"/>
    <g font-family="{FONT}">
      <text x="140" y="62" font-size="50" font-weight="800" fill="url(#nm)" textLength="720" lengthAdjust="spacingAndGlyphs">Thanks for stopping by</text>
      <text x="142" y="100" font-size="28" fill="{th['muted']}">A star helps others discover it.</text>
    </g>
  </g>
  <g class="d">
  <g transform="translate(196 60)">
    <polygon points="{star(0,0,22,9)}" fill="{th['gold']}" filter="url(#sg)" opacity=".6"><animate attributeName="opacity" values=".2;.8;.2" dur="2.8s" repeatCount="indefinite"/></polygon>
    <polygon points="{star(0,0,20,8.5)}" fill="{th['gold']}">
      <animateTransform attributeName="transform" type="rotate" values="0;0;72;72" keyTimes="0;.7;.85;1" dur="5s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;.6 0 .3 1;0 0 1 1"/></polygon>
  </g>
  <g font-family="{FONT}">
    <text x="238" y="55" font-size="28" font-weight="800" fill="url(#nm)">Thanks for stopping by</text>
    <text x="239" y="82" font-size="15" fill="{th['muted']}">Find something useful? A star helps others discover it.</text>
  </g>
  </g>
</svg>
'''
for t in TH: open(f"{out}/footer-{t}.svg","w").write(svg(t))

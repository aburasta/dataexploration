#!/usr/bin/env python3
"""Render the agent architecture diagram (SVG -> PNG)."""
import cairosvg

W, H = 1500, 1820

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#0f1117"/>')

# defs: arrow marker
svg.append('''<defs>
<marker id="arr" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto">
  <path d="M0,0 L10,5 L0,10 z" fill="#7aa2f7"/>
</marker>
<marker id="arrg" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto">
  <path d="M0,0 L10,5 L0,10 z" fill="#9ece6a"/>
</marker>
</defs>''')

# title
svg.append(f'<text x="{W//2}" y="56" fill="#ffffff" font-size="34" font-weight="bold" text-anchor="middle">THE COUP-TO-DOCUMENTARY AGENT</text>')
svg.append(f'<text x="{W//2}" y="88" fill="#9aa5ce" font-size="17" text-anchor="middle">Pipeline built so far &#8212; raw coup data &#8594; research &#8594; script &#8594; footage-ready shot list</text>')

def node(x, y, w, h, title, lines, fill, stroke, badge=None, tcol="#ffffff"):
    svg.append(f'<rect x="{x}" y="{y}" rx="14" ry="14" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
    svg.append(f'<text x="{x+22}" y="{y+34}" fill="{tcol}" font-size="20" font-weight="bold">{esc(title)}</text>')
    yy = y + 60
    for ln in lines:
        svg.append(f'<text x="{x+22}" y="{yy}" fill="#c8d0f0" font-size="14.5">{esc(ln)}</text>')
        yy += 22
    if badge:
        bw = 116
        svg.append(f'<rect x="{x+w-bw-14}" y="{y+14}" rx="10" ry="10" width="{bw}" height="26" fill="{badge[1]}"/>')
        svg.append(f'<text x="{x+w-bw/2-14}" y="{y+32}" fill="#0f1117" font-size="13" font-weight="bold" text-anchor="middle">{esc(badge[0])}</text>')

def varrow(x, y1, y2, color="#7aa2f7", mk="arr", label=None):
    svg.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-4}" stroke="{color}" stroke-width="3" marker-end="url(#{mk})"/>')
    if label:
        svg.append(f'<text x="{x+14}" y="{(y1+y2)//2+5}" fill="#9aa5ce" font-size="13" font-style="italic">{esc(label)}</text>')

cx = 150           # left column x
colw = 760         # node width
done = ("BUILT", "#9ece6a")
prog = ("IN PROGRESS", "#e0af68")
pend = ("PENDING", "#7dcfff")

# ---- INPUT ----
node(cx, 110, colw, 70, "INPUT  —  user request", ["“African coups d’état — successful vs. unsuccessful”"], "#1b2335", "#3b4a6b")
varrow(cx+colw/2, 180, 230)

# ---- NODE 1 ----
node(cx, 230, colw, 96, "NODE 1  ·  Coup Dataset",
     ["Compile African coups 1950–present; classify by outcome.",
      "→ african_coups_1950_present.xlsx  (tabs: All / Successful / Unsuccessful)"],
     "#13261b", "#2f6d3f", badge=done)
varrow(cx+colw/2, 326, 360)

# ---- NODE 2 ----
node(cx, 360, colw, 96, "NODE 2  ·  Extract Unsuccessful",
     ["Pull the unsuccessful coups into their own sheet.",
      "→ african_coups_unsuccessful.xlsx"],
     "#13261b", "#2f6d3f", badge=done)
varrow(cx+colw/2, 456, 490, label="user picks: the 2004 Wonga Coup")

# ---- NODE 3 ----
node(cx, 490, colw, 150, "NODE 3  ·  Deep-Research Dossier",
     ["5 parallel research agents → cross-check → tag [FACT]/[ALLEGED]/[DISPUTED].",
      "Characters · oil/motive · colonial history · the plot · the failure.",
      "→ wonga_coup_dossier.md  +  .docx  (sourced bibliography)"],
     "#13261b", "#2f6d3f", badge=done)
varrow(cx+colw/2, 640, 674)

# ---- NODE 4 ----
node(cx, 674, colw, 168, "NODE 4  ·  Narration / Voiceover",
     ["Persona: showrunner + director + continuity + narration writer.",
      "Structure: COLD OPEN → context → continuation (loose, anti-cringe).",
      "Accuracy tags inherited. Measures runtime; segments into beats.",
      "→ wonga_coup_script.md + .docx   (~13:19, voice = placeholder)"],
     "#13261b", "#2f6d3f", badge=done)
varrow(cx+colw/2, 842, 876)

# ---- NODE 5 ----
node(cx, 876, colw, 196, "NODE 5  ·  Footage Sourcing + Timed Shot List",
     ["3 parallel footage agents: People · The Event · Country/Oil/History.",
      "Priority: REAL → public-domain/CC → licensable archive → stock.",
      "Compiler maps 193 beats (3–5s each) to one visual + link + licence.",
      "→ wonga_coup_shotlist.md + .docx",
      "   (timecodes, colour-coded asset types, rights flags)"],
     "#13261b", "#2f6d3f", badge=done)
varrow(cx+colw/2, 1072, 1106)

# ---- OUTPUT ----
node(cx, 1106, colw, 84, "OUTPUT  —  production-ready documentary package",
     ["Dossier  +  timed voiceover  +  shot list, committed & pushed to GitHub."],
     "#1b2335", "#3b4a6b")

# ---- NODE 6 (proposed) ----
svg.append(f'<line x1="{cx+colw/2}" y1="1190" x2="{cx+colw/2}" y2="1226" stroke="#565f89" stroke-width="3" stroke-dasharray="7 6" marker-end="url(#arr)"/>')
node(cx, 1226, colw, 74, "NODE 6  ·  Voice Re-tune (next)",
     ["Ingest user writing samples → style bible → re-voice script & shot list."],
     "#2a2030", "#6b4a6b", badge=pend)

# ====== RIGHT SIDE: cross-cutting capabilities & infra ======
rx = 1000
rw = 360
svg.append(f'<text x="{rx}" y="150" fill="#9aa5ce" font-size="16" font-weight="bold">CROSS-CUTTING</text>')

def side(y, title, lines, fill, stroke):
    h = 40 + 22*len(lines)
    svg.append(f'<rect x="{rx}" y="{y}" rx="12" width="{rw}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    svg.append(f'<text x="{rx+18}" y="{y+28}" fill="#ffffff" font-size="16" font-weight="bold">{esc(title)}</text>')
    yy=y+52
    for ln in lines:
        svg.append(f'<text x="{rx+18}" y="{yy}" fill="#c8d0f0" font-size="13">{esc(ln)}</text>'); yy+=22
    return y+h+24

y = 168
y = side(y, "Accuracy spine", ["[FACT] / [ALLEGED] / [DISPUTED]", "tags propagate node → node.", "Allegations never stated as fact."], "#241f12", "#6b5a2f")
y = side(y, "Multi-agent engine", ["Fan-out research agents (5 + 3),", "then a compiler agent merges", "results into the deliverable."], "#1a2230", "#3b5a7b")
y = side(y, "Doc rendering", ["md_to_docx.py  +  generators", "→ styled Word (.docx) output.", "Tables, headings, colour tags."], "#1a2230", "#3b5a7b")
y = side(y, "Footage rules", ["Real → CC → archive → stock.", "Links = map, not cleared rights.", "Gaps flagged (note, Calil)."], "#1a2230", "#3b5a7b")
y = side(y, "Version control", ["Every artifact committed &", "pushed to branch on GitHub.", "Reproducible generators."], "#1a2230", "#3b5a7b")
y = side(y, "Known limits", ["Sandbox blocks downloads;", "no live video pull / no Google", "Sheets — files import instead."], "#2a1a1a", "#6b3b3b")

# legend bottom
ly = 1340
svg.append(f'<text x="{rx}" y="{ly}" fill="#9aa5ce" font-size="14" font-weight="bold">STATUS</text>')
for i,(lab,col) in enumerate([("BUILT","#9ece6a"),("IN PROGRESS","#e0af68"),("PENDING","#7dcfff")]):
    yy=ly+24+i*30
    svg.append(f'<rect x="{rx}" y="{yy-14}" rx="7" width="20" height="20" fill="{col}"/>')
    svg.append(f'<text x="{rx+30}" y="{yy+2}" fill="#c8d0f0" font-size="14">{lab}</text>')

# footer
svg.append(f'<text x="{cx}" y="{H-30}" fill="#565f89" font-size="13">Case study threaded through: the 2004 Wonga Coup (Equatorial Guinea).  Each node consumes the previous node’s output.</text>')

svg.append('</svg>')
data = "\n".join(svg)
open("agent_architecture.svg","w").write(data)
cairosvg.svg2png(bytestring=data.encode(), write_to="agent_architecture.png", output_width=W*2, output_height=H*2)
print("wrote agent_architecture.svg / .png")

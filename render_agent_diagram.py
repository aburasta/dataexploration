#!/usr/bin/env python3
"""Render the CURRENT agent architecture diagram (SVG -> PNG)."""
import cairosvg

W, H = 1540, 1780

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">')
svg.append(f'<rect width="{W}" height="{H}" fill="#0f1117"/>')
svg.append('''<defs>
<marker id="arr" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7aa2f7"/></marker>
</defs>''')

svg.append(f'<text x="{W//2}" y="54" fill="#ffffff" font-size="33" font-weight="bold" text-anchor="middle">THE COUP-TO-DOCUMENTARY AGENT</text>')
svg.append(f'<text x="{W//2}" y="86" fill="#9aa5ce" font-size="16.5" text-anchor="middle">current state &#8226; starts from a chosen unsuccessful-coup row &#8594; research &#8594; script &#8594; footage shot list</text>')

def node(x, y, w, h, title, lines, fill, stroke, badge=None, accent=None):
    svg.append(f'<rect x="{x}" y="{y}" rx="14" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
    if accent:
        svg.append(f'<rect x="{x}" y="{y}" rx="14" width="8" height="{h}" fill="{accent}"/>')
    svg.append(f'<text x="{x+24}" y="{y+33}" fill="#ffffff" font-size="20" font-weight="bold">{esc(title)}</text>')
    yy = y + 59
    for ln in lines:
        svg.append(f'<text x="{x+24}" y="{yy}" fill="#c8d0f0" font-size="14.5">{esc(ln)}</text>'); yy += 22
    if badge:
        bw = 128
        svg.append(f'<rect x="{x+w-bw-14}" y="{y+13}" rx="10" width="{bw}" height="26" fill="{badge[1]}"/>')
        svg.append(f'<text x="{x+w-bw/2-14}" y="{y+31}" fill="#0f1117" font-size="12.5" font-weight="bold" text-anchor="middle">{esc(badge[0])}</text>')

def varrow(x, y1, y2, label=None):
    svg.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-4}" stroke="#7aa2f7" stroke-width="3" marker-end="url(#arr)"/>')
    if label:
        svg.append(f'<text x="{x+14}" y="{(y1+y2)//2+5}" fill="#9aa5ce" font-size="13" font-style="italic">{esc(label)}</text>')

cx, colw = 130, 800
done = ("BUILT", "#9ece6a"); active = ("ACTIVE", "#7dcfff"); pend = ("PENDING", "#e0af68")
green, gstroke = "#13261b", "#2f6d3f"
blue, bstroke = "#10212e", "#356a8f"

# Node 0
node(cx, 108, colw, 92, "NODE 0  ·  Row Selector",
     ["Pick a coup from african_coups_unsuccessful.xlsx:",
      "RANDOM on “generate a new one”, or a USER-SUPPLIED row."],
     blue, bstroke, badge=active)
varrow(cx+colw/2, 200, 234, label="the chosen coup")

# Node 1
node(cx, 234, colw, 116, "NODE 1  ·  Deep-Research Dossier",
     ["5 parallel research agents → cross-check → tag [FACT]/[ALLEGED]/[DISPUTED].",
      "Characters · founding history · resources/motive · the plot · the aftermath.",
      "→ <case>_dossier.md + .docx  (sourced bibliography)"],
     green, gstroke, badge=done)
varrow(cx+colw/2, 350, 384)

# Node 2
node(cx, 384, colw, 122, "NODE 2  ·  Narration / Voiceover  +  Timing",
     ["Showrunner+director+continuity+writer persona.",
      "COLD OPEN → context → continuation (loose, anti-cringe).",
      "Measures runtime; segments into ~3–5s beats with timecodes.",
      "→ <case>_script.md + .docx"],
     green, gstroke, badge=done)
varrow(cx+colw/2, 506, 540)

# Node 3 - the highlighted footage node
node(cx, 540, colw, 150, "NODE 3  ·  Footage Shot-List   (image + source per beat)",
     ["3 parallel footage agents: People · Event · Country/History.",
      "Under EACH beat: a prescribed IMAGE/VIDEO + DESCRIPTION + LINK + licence.",
      "Priority: REAL → public-domain/CC → licensable archive → stock.",
      "Trawls the web for sources (no downloads); flags gaps & graphic shots.",
      "→ <case>_shotlist.md + .docx  (colour-coded, timecoded)"],
     "#241a2e", "#7a4fa3", badge=done, accent="#c08be0")
varrow(cx+colw/2, 690, 724)

# Node 4
node(cx, 724, colw, 80, "NODE 4  ·  Voice Re-tune",
     ["Ingest user writing samples → style bible → re-voice script & shot list."],
     "#2a2415", "#6b5a2f", badge=pend)
varrow(cx+colw/2, 804, 838)

# Output
node(cx, 838, colw, 80, "OUTPUT  —  documentary package per coup",
     ["Dossier + timed voiceover + footage shot list — committed & pushed to GitHub."],
     "#1b2335", "#3b4a6b")

# Retired box
ry = 956
svg.append(f'<rect x="{cx}" y="{ry}" rx="12" width="{colw}" height="74" fill="#1a1a1f" stroke="#444" stroke-width="2" stroke-dasharray="7 6"/>')
svg.append(f'<text x="{cx+24}" y="{ry+30}" fill="#888" font-size="17" font-weight="bold">RETIRED  (data already generated)</text>')
svg.append(f'<text x="{cx+24}" y="{ry+55}" fill="#777" font-size="14" text-decoration="line-through">Coup Dataset → african_coups_1950_present.xlsx   ·   Extract Unsuccessful → african_coups_unsuccessful.xlsx</text>')

# Right column cross-cutting
rx, rw = 1000, 410
svg.append(f'<text x="{rx}" y="150" fill="#9aa5ce" font-size="16" font-weight="bold">CROSS-CUTTING</text>')
def side(y, title, lines, fill="#1a2230", stroke="#3b5a7b"):
    h = 38 + 21*len(lines)
    svg.append(f'<rect x="{rx}" y="{y}" rx="12" width="{rw}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    svg.append(f'<text x="{rx+18}" y="{y+27}" fill="#ffffff" font-size="15.5" font-weight="bold">{esc(title)}</text>')
    yy = y+50
    for ln in lines:
        svg.append(f'<text x="{rx+18}" y="{yy}" fill="#c8d0f0" font-size="13">{esc(ln)}</text>'); yy += 21
    return y+h+22
y = 168
y = side(y, "Accuracy spine", ["[FACT]/[ALLEGED]/[DISPUTED] tags", "propagate node → node;", "allegations never stated as fact."], "#241f12", "#6b5a2f")
y = side(y, "Multi-agent engine", ["Fan-out research/footage agents,", "then a compiler builds the doc."])
y = side(y, "Footage rules", ["Real → CC → archive → stock.", "Links = map to verify, not rights.", "Gaps & graphic shots flagged."])
y = side(y, "Doc rendering", ["md_to_docx.py + generators →", "styled, colour-tagged Word docs."])
y = side(y, "Version control", ["Every artifact committed &", "pushed to the GitHub branch."])
y = side(y, "Known limits", ["Sandbox blocks downloads / live", "video pull / Google Sheets;", "files import instead."], "#2a1a1a", "#6b3b3b")

# status legend
ly = y + 8
svg.append(f'<text x="{rx}" y="{ly}" fill="#9aa5ce" font-size="14" font-weight="bold">STATUS</text>')
for i,(lab,col) in enumerate([("BUILT","#9ece6a"),("ACTIVE","#7dcfff"),("PENDING","#e0af68")]):
    yy = ly+22+i*28
    svg.append(f'<rect x="{rx}" y="{yy-14}" rx="6" width="18" height="18" fill="{col}"/>')
    svg.append(f'<text x="{rx+28}" y="{yy+1}" fill="#c8d0f0" font-size="13.5">{lab}</text>')

# case studies footer
fy = 1110
svg.append(f'<text x="{cx}" y="{fy}" fill="#9aa5ce" font-size="15" font-weight="bold">CASE STUDIES RUN THROUGH THE PIPELINE</text>')
svg.append(f'<rect x="{cx}" y="{fy+16}" rx="10" width="385" height="58" fill="#13261b" stroke="#2f6d3f" stroke-width="2"/>')
svg.append(f'<text x="{cx+18}" y="{fy+40}" fill="#fff" font-size="15" font-weight="bold">Wonga Coup (Eq. Guinea, 2004)</text>')
svg.append(f'<text x="{cx+18}" y="{fy+62}" fill="#9ece6a" font-size="13">dossier + script + 193-beat shot list ✓</text>')
svg.append(f'<rect x="{cx+410}" y="{fy+16}" rx="10" width="385" height="58" fill="#13261b" stroke="#2f6d3f" stroke-width="2"/>')
svg.append(f'<text x="{cx+428}" y="{fy+40}" fill="#fff" font-size="15" font-weight="bold">Liberia 1985 (Quiwonkpa)</text>')
svg.append(f'<text x="{cx+428}" y="{fy+62}" fill="#9ece6a" font-size="13">dossier + script + 146-beat shot list ✓</text>')

svg.append(f'<text x="{cx}" y="{H-26}" fill="#565f89" font-size="13">Each node consumes the previous node’s output. Point Node 0 at any unsuccessful-coup row and Nodes 1–3 develop it into the final package.</text>')
svg.append('</svg>')
data = "\n".join(svg)
open("agent_architecture.svg","w").write(data)
cairosvg.svg2png(bytestring=data.encode(), write_to="agent_architecture.png", output_width=W*2, output_height=H*2)
print("wrote agent_architecture.svg / .png")

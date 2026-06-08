#!/usr/bin/env python3
"""Build the demo episode deliverables for:
Concept: Risk pooling  |  Animal: Vampire bat reciprocal blood sharing.
Outputs: EP07_shot-list.docx (Deliverable A) and EP07_prompt-pack.txt (Deliverable B)."""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------- fixed style + bibles ----------
STYLE_SUFFIX = (
    "Flat 2D vector illustration in a warm mid-century-modern explainer-animation style (in the spirit of Hey "
    "Duggee / modern motion-graphics). Bold simple geometric shapes with soft rounded corners. No outlines, forms "
    "defined by flat color blocks. Limited warm palette: ochre yellow (#E8A93C), warm cream (#F7EAD0), teal blue "
    "(#3C7C9A), deep navy (#21465A), coral red-orange (#EF5A2A), burnt orange (#CC6B2C), moss olive (#A7A24A). Flat "
    "soft ambient lighting, gentle minimal flat shadows. Subtle fine film-grain / paper texture over the whole frame. "
    "Simple dot eyes, minimal facial features. Cozy, friendly, clean, generous negative space. 16:9. No gradients, no "
    "3D, no realistic shading, no glossy highlights, no heavy black outlines, no clutter, no photorealism."
)
HOST = ("the teal-blue fox host (rounded chunky body, small charcoal dot eyes, a signature coral-orange knitted "
        "scarf)")
BAT = ("a friendly rounded vampire bat (deep-navy body, teal-blue wing membranes, tiny charcoal dot eyes, small "
       "rounded fangs)")
FIG = "a simple rounded teal humanoid figure with no detailed face"
SET = "the cozy mid-century living room (pendant lamp, monstera plant, window with stylized autumn trees)"

# ---------- the episode: (act, narration, scene_for_prompt, type, family) ----------
S = [
("HOOK", "What if one disaster could never wipe you out —",
 f"Close-up of {HOST} leaning toward camera, intrigued, eyebrows raised, inside {SET}. A single warm spotlight, cozy darker frame. The coral scarf is the focal accent.", "STILL", "HOST"),
("HOOK", "no matter how unlucky you got?",
 f"Same {HOST} in {SET}, tilting its head with a questioning expression, a small floating coral question-mark beside it. Only the question-mark is added.", "STILL", "HOST"),
("HOOK", "Most people are always one bad month away from losing everything.",
 f"Wide shot of one small lone {FIG} standing on a cream floor, a thin coral crack opening in the ground beneath it. Ochre background, generous negative space. The coral crack is the focal accent.", "STILL", "STAKE"),
("HOOK", "But a tiny creature solved this millions of years before we invented money.",
 f"Medium shot of {BAT} perched small on a large moss-olive jungle leaf, a single flat ochre coin lying nearby for contrast. The bat is the focal subject.", "STILL", "BATINTRO"),
("HOOK", "And once you see how it works,",
 f"Medium shot of {HOST} in {SET}, one paw raised with a knowing look. The coral scarf is the focal accent.", "STILL", "HOST"),
("HOOK", "you'll never look at insurance the same way again.",
 f"{HOST} in {SET} gesturing toward a floating coral shield icon (insurance). Only the shield icon is added.", "STILL", "HOST"),

("STAKES", "Here's the uncomfortable truth.",
 f"Medium shot of {HOST} in {SET} with a serious, leaning-in expression. Coral scarf focal.", "STILL", "HOST"),
("STAKES", "You can do everything right — save, work hard, plan —",
 f"A single {FIG} on an ochre field surrounded by three small teal icons: a coin, a tool, and a checklist. Calm, tidy composition.", "STILL", "STAKE"),
("STAKES", "and a single emergency can erase it all in a day.",
 f"The same {FIG} as the coin, tool and checklist icons crack and a sharp coral burst strikes through them, everything tipping. Only the coral burst and cracks are added. The coral burst is the focal accent.", "STILL", "STAKE"),
("STAKES", "Relying on luck is a losing game.",
 f"The same {FIG} standing alone beneath a large wobbling coral dice symbol of luck. The coral dice is the focal accent.", "STILL", "STAKE"),
("STAKES", "So how do you make yourself disaster-proof?",
 f"{HOST} in {SET}, palms turned up in a question, a small coral question-mark above. Coral focal.", "STILL", "HOST"),

("ANIMAL", "Meet the vampire bat.",
 f"Centered hero shot of {BAT} hanging upside down in a warm softly-lit hollow, friendly, looking at camera. The bat is the focal subject.", "STILL", "BAT"),
("ANIMAL", "It survives on one thing: blood.",
 f"{BAT} hanging in the warm hollow with a small glowing coral blood-droplet motif near its mouth. Only the coral droplet is added; it is the focal accent.", "STILL", "BAT"),
("ANIMAL", "And it lives on a knife's edge.",
 f"{BAT} balanced tensely on a thin branch edge above a soft dark drop, cautious posture. Moody cozy lighting.", "STILL", "BATEDGE"),
("ANIMAL", "A vampire bat must feed almost every single night.",
 f"{BAT} in the hollow beside a small coral crescent-moon and a coral droplet, indicating nightly feeding. Coral elements focal.", "STILL", "BAT"),
("ANIMAL", "Go just two nights without a meal, and it starves.",
 f"{BAT} in the hollow turning pale and greyish, weak posture, beside two small moon icons and a tiny hourglass. Only the bat greying and the icons change. Muted tones.", "STILL", "BAT"),
("ANIMAL", "But hunting is unreliable.",
 f"Wide shot of {BAT} flying across a dark moss-olive jungle night, searching. The bat is a small focal silhouette.", "STILL", "BATFLY"),
("ANIMAL", "On any night, a healthy bat may find nothing at all.",
 f"{BAT} landing on a bare leaf with nothing there, a small worried expression. Empty, quiet composition.", "STILL", "BATFLY"),

("PARALLEL", "So these bats made a deal.",
 f"Two of {BAT} hanging side by side in the warm hollow, turning to face each other. Both bats are the focal subjects.", "STILL", "SHARE"),
("PARALLEL", "A bat that feeds well throws up part of its meal",
 f"In the hollow, one well-fed {BAT} with a soft coral droplet glow at its belly leans toward a second, emptier bat. The coral glow is the focal accent.", "STILL", "SHARE"),
("PARALLEL", "to share with a roost-mate that came home empty.",
 f"In the hollow, the fed {BAT} passing a glowing coral droplet to the empty bat's mouth. The shared coral droplet is the focal point.", "STILL", "SHARE"),
("PARALLEL", "It gives away blood it didn't need",
 f"Close-up of the giving {BAT}, a small coral droplet leaving it, calm and generous posture. The coral droplet is focal.", "STILL", "SHARE"),
("PARALLEL", "to keep a hungry neighbor alive.",
 f"In the hollow, the receiving {BAT} brightening and regaining its deep-navy color, revived. Only the receiver brightening changes. Warm glow.", "STILL", "SHARE"),
("PARALLEL", "And here's the genius part: the bats remember.",
 f"{HOST} in {SET} tapping its head with a knowing smile, a small coral lightbulb icon beside it. The coral lightbulb is the focal accent.", "STILL", "HOST"),
("PARALLEL", "The ones you feed are the ones who feed you",
 f"A web of several of {BAT} in the hollow connected by thin coral lines showing who fed whom. The coral lines are the focal element.", "STILL", "NETWORK"),
("PARALLEL", "when your own luck runs out.",
 f"The same web of {BAT}, one coral line lighting up as a droplet travels back along it to a dim bat. Only the lit line and returning droplet change.", "STILL", "NETWORK"),
("PARALLEL", "Each bat pays a small price on its good nights",
 f"A single {BAT} dropping a small coral droplet into a shared glowing pool-jar in the hollow. The coral droplet and glowing pool are focal.", "STILL", "POOL"),
("PARALLEL", "to buy protection on its bad ones.",
 f"The same {BAT} drawing a coral droplet back out of the glowing shared pool on a bad night. Only the direction of the droplet changes.", "STILL", "POOL"),
("PARALLEL", "No single bat can survive its own bad luck alone.",
 f"One lone {BAT} facing a huge dark looming wave of bad luck, tiny and overwhelmed. The dark wave dominates; the small bat is focal.", "STILL", "CONTRAST"),
("PARALLEL", "But pooled across the colony, one bat's disaster",
 f"Many of {BAT} together raising a soft protective coral dome against the same dark wave. The coral dome is the focal element.", "STILL", "CONTRAST"),
("PARALLEL", "is covered by another bat's surplus.",
 f"Under the holding coral dome, one dim {BAT} is lifted by the warm surplus glow of the others around it. Only the lifted glowing bat changes.", "STILL", "CONTRAST"),
("PARALLEL", "That is insurance. Exactly.",
 f"A bold centered emblem: a coral shield formed out of many tiny bat shapes, clean and graphic, on a warm cream field. The coral shield is the focal subject.", "STILL", "BADGE"),
("PARALLEL", "The premium is the blood you give when you're full.",
 f"A {BAT} dropping a coral droplet marked with a small '+' into the glowing shared pool. The coral droplet is focal.", "STILL", "POOL"),
("PARALLEL", "The payout is the blood you get when you're empty.",
 f"A {BAT} receiving a coral droplet marked with a small payout arrow from the glowing shared pool. Only the arrow and direction change.", "STILL", "POOL"),
("PARALLEL", "The colony is the insurance company.",
 f"The whole warm hollow stylized as a cozy little 'company' of {BAT}, with a small coral sign above the entrance. The coral sign is the focal accent.", "STILL", "COLONYCO"),

("INSIGHT", "This is why insurance feels like a waste —",
 f"{HOST} in {SET} shrugging, a small coral question-mark over a wall calendar. Coral focal.", "STILL", "HOST"),
("INSIGHT", "until the day it doesn't.",
 f"{HOST} in {SET} watching a wall calendar rapidly flip through months while nothing happens, patient expression. Animate the calendar pages flipping.", "CLIP", "HOST"),
("INSIGHT", "Every month you pay, and nothing happens.",
 f"A {FIG} dropping a small coral coin into a slot, repeatedly, on an ochre field. Animate one coral coin dropping into the slot.", "CLIP", "PAY"),
("INSIGHT", "You're the well-fed bat, giving away blood you didn't need.",
 f"The same {FIG} shown with a faint overlay of {BAT}, giving away a small coral droplet it did not need. The coral droplet is focal.", "STILL", "PAY"),
("INSIGHT", "That feeling of waste is the product working.",
 f"On an ochre field, the small 'wasted' coral coin transforming into a glowing coral shield. Only the coin-to-shield change. The coral shield is focal.", "STILL", "PAY"),
("INSIGHT", "You're paying so that if disaster strikes, the colony catches you.",
 f"A coral disaster bolt striking down at a {FIG}, but a protective coral dome of figures catches it. The coral bolt and dome are focal.", "STILL", "CATCH"),

("BREAKDOWN", "But here's where the bats and your insurer part ways.",
 f"{HOST} in {SET}, one eyebrow raised in a 'but...' gesture, the background subtly split warm-left and cool-right. Coral scarf focal.", "STILL", "HOST"),
("BREAKDOWN", "The bats run on memory and friendship.",
 f"Warm scene of several of {BAT} linked by soft coral friendship lines in the cozy hollow. The coral lines are focal.", "STILL", "BREAK"),
("BREAKDOWN", "A company runs on cold math.",
 f"A cool, cleaner composition of a navy geometric grid and abacus on a pale field, precise and hard-edged. Minimal, colder mood.", "STILL", "BREAK"),
("BREAKDOWN", "It has priced you precisely to stay profitable.",
 f"The navy abacus calculating, setting a precise small coral figure (your price). Only the coral figure is added; it is focal.", "STILL", "BREAK"),
("BREAKDOWN", "And unlike a loyal roost-mate, it can deny your claim.",
 f"A cold geometric 'company' hand snapping shut a coral claim-folder. The coral folder is the focal accent.", "STILL", "BREAK"),
("BREAKDOWN", "So the bats teach you why pooling works.",
 f"{HOST} in {SET} nodding, holding a small warm {BAT} icon in one paw. The little bat is focal.", "STILL", "HOST"),
("BREAKDOWN", "But you're trusting a spreadsheet — not a friend.",
 f"{HOST} in {SET} holding up a flat navy spreadsheet grid in the other paw, comparing it to the bat. Only the spreadsheet is added.", "STILL", "HOST"),

("LESSON", "So the lesson is simple.",
 f"Medium shot of {HOST} in {SET}, confident, speaking directly to camera. Coral scarf focal.", "STILL", "HOST"),
("LESSON", "Don't try to survive every disaster alone.",
 f"A lone {FIG} straining under a huge dark load by itself on an ochre field. The strained lone figure is focal.", "STILL", "LESSON"),
("LESSON", "Pool the risks too big to carry by yourself.",
 f"The same huge load now lifted easily by many of {FIG} together. Only the added helping figures change. Light, balanced mood.", "STILL", "LESSON"),
("LESSON", "Pay the small price on your good days,",
 f"A {FIG} calmly placing a small coral coin into the glowing shared pool on a sunny ochre day. The coral coin is focal.", "STILL", "POOL"),
("LESSON", "so a single bad one can never end the game.",
 f"A single coral disaster bolt bouncing harmlessly off the group's protective coral dome. The coral bolt and dome are focal.", "STILL", "CATCH"),

("BUTTON", "A creature that drinks blood in the dark figured that out.",
 f"Intimate shot of {BAT} in the dark hollow with a single warm coral droplet glowing, a wise look to camera. The coral droplet is focal.", "STILL", "END"),
("BUTTON", "The question is — will you?",
 f"{HOST} in {SET} pointing gently at the viewer with a friendly, challenging smile. The coral scarf is the focal accent.", "STILL", "HOST"),
("BUTTON", "See you in the next one.",
 f"{HOST} in {SET} giving a small warm wave as the room softly dims. Cozy farewell mood.", "STILL", "HOST"),
]

WPS = 2.5  # 150 wpm


def mmss(t):
    return f"{int(t)//60:02d}:{int(round(t))%60:02d}"


# compute timings
rows = []
clock = 0.0
for i, (act, narr, scene, typ, fam) in enumerate(S, start=1):
    wc = len(narr.split())
    dur = max(2.0, wc / WPS)
    start, end = clock, clock + dur
    rows.append(dict(n=i, act=act, narr=narr, scene=scene, typ=typ, fam=fam,
                     wc=wc, start=start, end=end))
    clock = end
total = clock
total_words = sum(r["wc"] for r in rows)

# seeds per family (stable)
fams = []
for r in rows:
    if r["fam"] not in fams:
        fams.append(r["fam"])
seed_of = {f: 673346 + 137 * k for k, f in enumerate(fams)}

OUT = "/home/user/dataexploration/EP07_risk-pooling_vampire-bat"
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)
os.makedirs(os.path.join(OUT, "clips"), exist_ok=True)

# ============================ Deliverable A: shot-list.docx ============================
def shade(cell, hexv):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexv)
    tcPr.append(shd)

def sct(cell, text, bold=False, size=8.5, color=None):
    cell.text = ""; r = cell.paragraphs[0].add_run(text)
    r.bold = bold; r.font.size = Pt(size)
    if color: r.font.color.rgb = RGBColor.from_string(color)

doc = Document()
doc.styles["Normal"].font.name = "Calibri"; doc.styles["Normal"].font.size = Pt(10.5)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("EPISODE 07 — SHOT LIST"); r.bold = True; r.font.size = Pt(22)
r.font.color.rgb = RGBColor.from_string("1F4E5F")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Why insurance feels like a scam — until the day it saves you"); r.italic = True; r.font.size = Pt(12)
r.font.color.rgb = RGBColor.from_string("EF5A2A")

doc.add_heading("Episode meta", level=1)
for k, v in [
    ("Finance concept", "Risk pooling (individual catastrophic loss absorbed by the group's surplus)"),
    ("Animal match", "Vampire bat reciprocal blood sharing (quality 96%, web-verified)"),
    ("Target runtime", f"{mmss(total)} (pilot cut; extend to 10–15 min for full release)"),
    ("Word count", f"{total_words} words"),
    ("Narration pace", "150 wpm (2.5 words/sec)"),
    ("Shots / images", f"{len(rows)} (one image per shot; {sum(1 for r in rows if r['typ']=='CLIP')} clips)"),
    ("Primary model", "Seedream 4.5, 16:9 (Nano Banana Pro only for any text/diagram frames)"),
]:
    pp = doc.add_paragraph(); pp.add_run(f"{k}: ").bold = True; pp.add_run(v)

doc.add_heading("Clean narration script (read top to bottom)", level=1)
last_act = None
for r in rows:
    if r["act"] != last_act:
        doc.add_paragraph()
        last_act = r["act"]
    para = doc.paragraphs[-1]
    if para.runs and not para.text.endswith(" ") and para.text:
        para.add_run(" ")
    para.add_run(r["narr"] + " ").font.size = Pt(11)

doc.add_heading("Shot list", level=1)
tbl = doc.add_table(rows=1, cols=6); tbl.style = "Table Grid"
hd = tbl.rows[0].cells
for i, h in enumerate(["Shot", "Time", "Narration", "On-screen visual", "File", "Type"]):
    sct(hd[i], h, bold=True, size=8.5, color="FFFFFF"); shade(hd[i], "1F4E5F")
for r in rows:
    c = tbl.add_row().cells
    sct(c[0], f"{r['n']:03d}")
    sct(c[1], f"{mmss(r['start'])}-{mmss(r['end'])}")
    sct(c[2], r["narr"])
    short = r["scene"].split(",")[0].split(".")[0]
    sct(c[3], (short[:80] + "…") if len(short) > 80 else short)
    sct(c[4], f"shot_{r['n']:03d}.png" if r["typ"] == "STILL" else f"shot_{r['n']:03d}.mp4")
    sct(c[5], r["typ"])
widths = [0.4, 0.9, 2.3, 2.5, 0.8, 0.5]
for row in tbl.rows:
    for i, w in enumerate(widths):
        row.cells[i].width = Inches(w)

doc.save(os.path.join(OUT, "EP07_shot-list.docx"))

# ============================ Deliverable B: prompt-pack.txt ============================
lines = []
lines.append("HIGGSFIELD PROMPT PACK  —  EPISODE 07: Risk pooling / Vampire bat reciprocal blood sharing")
lines.append("Model: Seedream 4.5  |  Aspect: 16:9  |  Paste each SHOT prompt into the Higgsfield web app.")
lines.append("=" * 100)
lines.append("")
lines.append("=== CONSISTENCY HEADER  (keep these anchors identical for every image) ===")
lines.append("")
lines.append("RECURRING CHARACTERS (describe with these EXACT words whenever they appear):")
lines.append(f"  HOST  = {HOST}")
lines.append(f"  BAT   = {BAT}")
lines.append(f"  FIG   = {FIG}")
lines.append(f"  SET   = {SET}")
lines.append("")
lines.append("PALETTE (hex): ochre #E8A93C, cream #F7EAD0, teal #3C7C9A, navy #21465A, "
             "coral #EF5A2A, burnt orange #CC6B2C, moss olive #A7A24A.")
lines.append("")
lines.append("SETTINGS for every generation:")
lines.append("  - Model: Seedream 4.5  |  Aspect ratio: 16:9  |  quality: high for hero frames, basic otherwise")
lines.append("  - Reference image: attach your approved style key-frame (the fox test) so palette/grain carry over")
lines.append("  - Element: attach your saved 'host-fox' Element for every shot that includes the HOST")
lines.append("  - Seed: reuse the seed listed per shot (same seed within a shot-family keeps frames continuous)")
lines.append("  - Coral is the focal/spotlight color: reserve it for the one thing the viewer should look at")
lines.append("")
lines.append("STYLE BLOCK (appended to every prompt below):")
lines.append("  " + STYLE_SUFFIX)
lines.append("")
lines.append("=" * 100)
lines.append("PER-SHOT PROMPTS")
lines.append("=" * 100)
for r in rows:
    lines.append("")
    tag = f"=== SHOT {r['n']:03d}  |  {mmss(r['start'])}-{mmss(r['end'])}  |  family:{r['fam']}  seed:{seed_of[r['fam']]}  |  {r['typ']} ==="
    lines.append(tag)
    if r["typ"] == "CLIP":
        lines.append("[CLIP: generate this still first, then animate it with image-to-video, keeping the same style.]")
    lines.append(r["scene"] + " " + STYLE_SUFFIX)
lines.append("")
lines.append("=" * 100)
lines.append("END OF PROMPT PACK  —  " + f"{len(rows)} prompts, runtime {mmss(total)}.")

with open(os.path.join(OUT, "EP07_prompt-pack.txt"), "w") as f:
    f.write("\n".join(lines))

print("Wrote:")
print(" ", os.path.join(OUT, "EP07_shot-list.docx"))
print(" ", os.path.join(OUT, "EP07_prompt-pack.txt"))
print(f"Shots: {len(rows)} | words: {total_words} | runtime: {mmss(total)} | seed families: {len(fams)}")

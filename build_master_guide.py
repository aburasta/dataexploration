#!/usr/bin/env python3
"""Build the consolidated PROJECT MASTER GUIDE (.docx) for upload to Claude Projects.
Folds together: concept, assets, visual style, per-episode workflow, prompt pack,
Higgsfield operations (models/credits/consistency), procedure, and checklists."""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FULL_SUFFIX = (
    "Flat 2D vector illustration in a warm mid-century-modern explainer-animation style (in the spirit of Hey "
    "Duggee / modern motion-graphics). Bold simple geometric shapes with soft rounded corners. No outlines, forms "
    "defined by flat color blocks. Limited warm palette: ochre yellow (#E8A93C), warm cream (#F7EAD0), teal blue "
    "(#3C7C9A), deep navy (#21465A), coral red-orange (#EF5A2A), burnt orange (#CC6B2C), moss olive (#A7A24A). Flat "
    "soft ambient lighting, gentle minimal flat shadows. Subtle fine film-grain / paper texture over the whole "
    "frame. Simple dot eyes, minimal facial features. Cozy, friendly, clean, generous negative space. 16:9. No "
    "gradients, no 3D, no realistic shading, no glossy highlights, no heavy black outlines, no clutter, no photorealism."
)
COMPACT_SUFFIX = (
    "STYLE: flat 2D vector explainer-animation (Hey Duggee vibe); bold rounded geometric shapes, no outlines, flat "
    "color blocks; warm palette ochre #E8A93C, cream #F7EAD0, teal #3C7C9A, navy #21465A, coral #EF5A2A, burnt "
    "orange #CC6B2C, olive #A7A24A; flat soft lighting, minimal flat shadows, subtle film-grain; dot eyes, simple "
    "faces; cozy, clean, generous negative space; 16:9. No gradients/3D/realistic shading/gloss/black "
    "outlines/clutter/photorealism."
)


def shade(cell, hexv):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexv.lstrip("#"))
    tcPr.append(shd)


def sct(cell, text, bold=False, size=9, color=None):
    cell.text = ""; r = cell.paragraphs[0].add_run(text)
    r.bold = bold; r.font.size = Pt(size)
    if color: r.font.color.rgb = RGBColor.from_string(color.lstrip("#"))


def h1(t): return doc.add_heading(t, level=1)
def h2(t): return doc.add_heading(t, level=2)


def body(t, size=10.5, italic=False):
    p = doc.add_paragraph(); r = p.add_run(t); r.font.size = Pt(size); r.italic = italic
    return p


def bullet(t, size=10.5):
    p = doc.add_paragraph(style="List Bullet"); p.add_run(t).font.size = Pt(size); return p


def num(t, size=10.5):
    p = doc.add_paragraph(style="List Number"); p.add_run(t).font.size = Pt(size); return p


def box(label, text):
    if label:
        lp = doc.add_paragraph(); r = lp.add_run(label); r.bold = True
        r.font.size = Pt(9.5); r.font.color.rgb = RGBColor.from_string("1F4E5F")
    tbl = doc.add_table(rows=1, cols=1); tbl.style = "Table Grid"
    c = tbl.cell(0, 0); shade(c, "F2F4F0"); c.text = ""
    rr = c.paragraphs[0].add_run(text); rr.font.name = "Consolas"; rr.font.size = Pt(9)
    doc.add_paragraph()


def callout(text):
    tbl = doc.add_table(rows=1, cols=1); tbl.style = "Table Grid"
    c = tbl.cell(0, 0); shade(c, "FBEFD6"); c.text = ""
    r = c.paragraphs[0].add_run(text); r.bold = True; r.font.size = Pt(10)
    r.font.color.rgb = RGBColor.from_string("8A4B16"); doc.add_paragraph()


doc = Document()
doc.styles["Normal"].font.name = "Calibri"; doc.styles["Normal"].font.size = Pt(10.5)

# ---------------- TITLE ----------------
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("PROJECT MASTER GUIDE"); r.bold = True; r.font.size = Pt(28)
r.font.color.rgb = RGBColor.from_string("1F4E5F")
s = doc.add_paragraph(); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run("Finance × Animal Behavior — Animated YouTube Documentary Series")
r.font.size = Pt(13); r.font.color.rgb = RGBColor.from_string("EF5A2A")
s = doc.add_paragraph(); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run("The single, complete reference for the project. Upload to the Claude Projects section. "
              "When a spreadsheet row is named, follow this guide end-to-end.")
r.italic = True; r.font.size = Pt(10)
doc.add_paragraph()

# ---------------- 1. AT A GLANCE ----------------
h1("1. The Project at a Glance")
body("A YouTube documentary series that explains difficult finance concepts by paralleling them to specific animal "
     "behaviors. Each episode is built from ONE row of the file finance_animal_behavior_matches.xlsx.")
body("The pipeline for every episode:")
num("Pick a row (a finance concept + its animal-behavior match).")
num("Write the narration script (benefit-led hook + retention arc).")
num("Break it into a timed SHOT LIST — a new on-screen visual every 3–5 seconds.")
num("Produce a HIGGSFIELD PROMPT PACK — paste-ready prompts that generate every image in the fixed style.")
num("Generate the images (free in the Higgsfield web app on Seedream 4.5), name them to match the shots.")
num("Assemble in a video editor (add VO, captions, camera moves), then publish.")
callout("TWO THINGS NEVER CHANGE BETWEEN EPISODES: the VISUAL STYLE (Section 4) and the SCRIPT/HOOK FORMULA "
        "(Section 3). Only the content — the concept and the animal — changes. Consistency is the brand.")
bullet("Target runtime: 10–15 minutes (default ~12).  Cadence: a visual change every 3–5 seconds.")
bullet("A 10–15 min episode = ~150–300 shots/images.  Primary image model: Seedream 4.5.")

# ---------------- 2. ASSETS ----------------
h1("2. Project Assets & Inputs")
tbl = doc.add_table(rows=1, cols=2); tbl.style = "Table Grid"
for i, x in enumerate(["File", "What it is / how it's used"]):
    sct(tbl.rows[0].cells[i], x, bold=True, size=9, color="FFFFFF"); shade(tbl.rows[0].cells[i], "1F4E5F")
for f, d in [
    ("finance_animal_behavior_matches.xlsx", "THE INPUT. 100 granular finance concepts, each with 2 rated animal "
     "matches + script-ready behavior descriptions. One row = one episode. Default to the higher-rated match."),
    ("finance_concepts_for_animation.xlsx", "The source list of 100 granular finance concepts (reference)."),
    ("PROJECT_MASTER_GUIDE.docx", "THIS document — the complete project guide."),
    ("style reference image", "The approved cartoon look (flat mid-century explainer style) — see Section 4."),
    ("EP07_risk-pooling_vampire-bat/", "A complete worked demo episode (shot list + prompt pack) to copy as a template."),
]:
    c = tbl.add_row().cells
    sct(c[0], f, bold=True, size=9); sct(c[1], d, size=9)
tbl.rows[0].cells[0].width = Inches(2.6); tbl.rows[0].cells[1].width = Inches(4.0)
doc.add_paragraph()
body("Reading a row: use the Category, Granular Concept, and The Specific Finance Aspect to know exactly what to "
     "teach; use the chosen Animal Match's description as the factual basis. If a match is flagged below 75% or "
     "'debated', lean into the 'where the analogy breaks down' beat rather than overstating it.")

# ---------------- 3. CREATIVE PRINCIPLES ----------------
h1("3. Creative Principles — Script & Hook (fixed every episode)")
h2("3a. The Hook (first ~10–15 seconds)")
body("ALWAYS create suspense around the personal BENEFIT of knowing the lesson — framed as an intriguing question or "
     "'what if'. Do NOT open by naming the concept; open with the payoff and the mystery.")
box("HOOK EXAMPLES (benefit-led):",
    "Avoid herd behavior → \"How do the people who spot the next big thing always see it first? "
    "The answer is hiding in how one bird breaks from the flock...\"\n"
    "Risk pooling → \"What if one bad month could never wipe you out — no matter how unlucky you got?\"\n"
    "Compounding → \"What if one small, boring habit today decided whether you're rich in 20 years?\"")
h2("3b. Retention Arc (after the hook)")
for x in [
    "STAKES — make the viewer feel why getting this wrong hurts them.",
    "MEET THE ANIMAL — introduce the animal + behavior vividly (from the spreadsheet description).",
    "THE PARALLEL — map the behavior onto the finance aspect, one idea at a time.",
    "WHERE IT BREAKS DOWN — honestly note where the analogy stops (signature trust-builder).",
    "THE PAYOFF — deliver the practical lesson promised in the hook.",
    "BUTTON — a short memorable closing line + soft subscribe / next-episode nudge.",
]:
    bullet(x)
bullet("Throughout: short sentences, concrete imagery, a question every ~20–30 seconds, warm and clever — never lecture-y.")
h2("3c. Length & Pace")
bullet("Target 10–15 minutes (default ~12). Narration pace 150 wpm = 2.5 words/sec.")
bullet("At 150 wpm: 10 min ≈ 1,500 words, 12 min ≈ 1,800, 15 min ≈ 2,250.")

# ---------------- 4. VISUAL STYLE ----------------
h1("4. Visual Style — Applied to EVERY Episode")
callout("Mandatory and unchanging. Every image in every episode matches this. Append the style tag (Section 6 / "
        "Appendix) to every Higgsfield prompt.")
body("One sentence: warm, friendly, FLAT 2D vector illustration in a mid-century-modern 'explainer animation' style "
     "— bold simple shapes, a tight cozy palette, no harsh outlines, flat lighting, and a subtle grain texture.")
h2("4a. Core traits")
for x in [
    "FLAT color only — no gradients, no realistic shading, no 3D, no gloss.",
    "SHAPE-FIRST — circles, ovals, rounded rectangles; chunky, friendly, stable.",
    "OUTLINE-LESS — forms separated by color, not black ink lines.",
    "WARM LIMITED PALETTE (below); nothing neon.",
    "FLAT SOFT LIGHTING — gentle ambient; soft flat low-opacity shadows.",
    "GRAIN — a subtle film/paper texture over the whole frame.",
    "SIMPLE FACES — dot eyes, minimal mouths; emotion via eyebrows + posture.",
    "COZY & UNCLUTTERED — simple props, generous negative space.",
]:
    bullet(x)
h2("4b. Color palette (canonical hex)")
palette = [
    ("Ochre Yellow", "#E8A93C", "Backgrounds / large warm fields"),
    ("Warm Cream", "#F7EAD0", "Light backgrounds, negative space"),
    ("Teal Blue", "#3C7C9A", "Main character bodies, calm zones"),
    ("Deep Navy", "#21465A", "Depth, dark accents, grounding"),
    ("Coral Red-Orange", "#EF5A2A", "THE focal color — the key idea (sparingly)"),
    ("Burnt Orange", "#CC6B2C", "Plants, warm secondary accents"),
    ("Moss Olive", "#A7A24A", "Foliage, variety"),
    ("Off-White", "#FCF6EA", "Highlights, eye whites"),
    ("Charcoal", "#2C2A29", "Eyes / fine details only — never pure black"),
]
pt = doc.add_table(rows=1, cols=4); pt.style = "Table Grid"
for i, x in enumerate(["Swatch", "Name", "Hex", "Usage"]):
    sct(pt.rows[0].cells[i], x, bold=True, size=8.5, color="FFFFFF"); shade(pt.rows[0].cells[i], "1F4E5F")
for name, hexv, usage in palette:
    c = pt.add_row().cells
    shade(c[0], hexv); sct(c[0], "", size=8.5)
    sct(c[1], name, bold=True, size=8.5); sct(c[2], hexv, size=8.5); sct(c[3], usage, size=8.5)
for row in pt.rows:
    row.cells[0].width = Inches(0.5); row.cells[1].width = Inches(1.5)
    row.cells[2].width = Inches(0.9); row.cells[3].width = Inches(3.3)
doc.add_paragraph()
bullet("60/30/10: ~60% warm neutrals, ~30% blues, ~10% coral accent. Coral marks what to look at. No pure black/white.")
h2("4c. Characters")
bullet("HOST (recurring narrator): one fixed friendly animal guide — recommended a rounded teal fox with a signature "
       "coral scarf and dot eyes — in every episode. Lock ONE design and reuse it identically.")
bullet("ANIMAL OF THE WEEK: the spreadsheet animal, RE-TINTED into the palette (not natural photo colors), simplified.")
bullet("CROWDS / MARKETS / 'YOU': simple rounded humanoid figures in palette colors; the odd-one-out is coral.")
h2("4d. Finance motifs & composition")
bullet("Charts/coins/arrows drawn flat & chunky in palette (no realistic stock screenshots). Keep one icon vocabulary.")
bullet("16:9 every frame; one clear subject; keep bottom ~15% caption-safe; vary shot scale across a sequence.")

# ---------------- 5. DELIVERABLES + TIMING ----------------
h1("5. Per-Episode Deliverables")
body("For each row, produce THREE linked deliverables (Shot 001 ↔ Prompt 001 ↔ shot_001.png):")
num("DELIVERABLE A — SHOT LIST (Word doc): header meta + clean narration script + a table of timed shots "
    "(Shot #, timestamp, narration slice, one-line visual, file name, STILL/CLIP, prompt #).")
num("DELIVERABLE B — HIGGSFIELD PROMPT PACK (text): a consistency header + one paste-ready prompt per shot (Section 6).")
num("DELIVERABLE C — IMAGE FOLDER: the images, produced by running the Prompt Pack (free in the web app, or via API "
    "at credit cost), named shot_001.png … shot_0NN.png.")
h2("5a. Timing method (every shot = 3–5 seconds)")
num("Write the full clean narration script.")
num("Total duration = total_words ÷ 2.5 (seconds).")
num("Segment into shots of 3–5s each (~8–13 words = one short clause), one IMAGE per shot.")
num("Assign cumulative timestamps (shot length = its_words ÷ 2.5).")
callout("RESULT: a 10–15 min episode → ~150–300 shots/images. Use the key-frame + editor approach (Section 7) to hit "
        "the 3–5s cadence WITHOUT generating a separate image for literally every shot.")
h2("5b. File/folder naming")
box("FOLDER STRUCTURE:",
    "EP07_risk-pooling_vampire-bat/\n"
    "    EP07_shot-list.docx          <- Deliverable A\n"
    "    EP07_prompt-pack.txt         <- Deliverable B\n"
    "    images/  shot_001.png … shot_0NN.png   <- Deliverable C\n"
    "    clips/   shot_0XX.mp4        <- only if any CLIP shots")

# ---------------- 6. PROMPT PACK ----------------
h1("6. The Higgsfield Prompt Pack (Deliverable B)")
body("After the shot list, ALWAYS output the Prompt Pack: the exact prompts the user pastes into the Higgsfield web "
     "app to generate the episode's images consistently. Two parts:")
h2("6a. The Consistency Header (written once)")
bullet("STYLE BLOCK: the compact style tag (below), verbatim.")
bullet("CHARACTER BIBLE: thorough, word-for-word descriptions of every recurring character (Host, Animal of the "
       "Week, crowd figures). Reuse these EXACT words in every prompt featuring the character.")
bullet("WORLD/SET BIBLE: the recurring environment(s), described identically.")
bullet("PALETTE hex list + SETTINGS (Seedream 4.5, 16:9, attach style key-frame as reference + Host Element, one "
       "seed per shot-family).")
h2("6b. The per-shot prompts (one per image, numbered to the shot list)")
bullet("Each = Consistency Header content + [shot type] + [subject & action] + [setting] + [coral accent].")
bullet("RE-STATE recurring characters using the SAME wording as the Character Bible — never 'same as before' (that "
       "causes drift).")
bullet("Name the ONE thing that changes from the previous shot, so consecutive frames interconnect.")
bullet("State the seed + shot-family; be self-contained and paste-ready.")
bullet("STAY UNDER 3000 CHARACTERS (Higgsfield's per-prompt limit). Use the COMPACT style tag, not the full "
       "paragraph — each self-contained prompt should land ~600–1000 characters.")
callout("THOROUGHNESS RULE: every per-shot prompt carries a COMPLETE description of characters, palette, and style. "
        "Repeating it across all 150–300 prompts is exactly what keeps the separate images consistent.")
box("COMPACT STYLE TAG (append to every per-shot prompt):", COMPACT_SUFFIX)
box("EXAMPLE PER-SHOT PROMPT (~700 chars):",
    "Centered hero shot of rounded vampire bat (deep-navy body, teal wing membranes, tiny charcoal dot eyes, small "
    "fangs) hanging upside down in a warm softly-lit hollow, friendly, looking at camera. The bat is the focal "
    "subject. " + COMPACT_SUFFIX)

# ---------------- 7. HIGGSFIELD OPERATIONS ----------------
h1("7. Higgsfield Operations (models, consistency, credits)")
h2("7a. Models")
bullet("PRIMARY: Seedream 4.5 (id seedream_v4_5) — high quality, up to 4K, ~1 credit/image, in the paid plans' "
       "365-day unlimited set. Default for ALL images. quality 'high' for hero frames, 'basic' otherwise. 16:9.")
bullet("SECONDARY: Nano Banana Pro or GPT Image — ONLY for frames with on-image text/diagrams (better text). "
       "Cost more; use sparingly. (Better still: add text in the editor.)")
h2("7b. Web app vs API (this decides whether generation is FREE)")
bullet("Higgsfield WEB APP on a paid plan: Seedream is UNLIMITED (free) — generate the bulk here.")
bullet("Via API/automation (e.g., generating inside a chat): Seedream still bills ~1 credit/image even on a paid plan.")
bullet("FREE tier: ~10 credits/day, reloading daily; cannot sustain a full episode (use it for style tests only).")
h2("7c. Consistency tools (so frames flow like one animation)")
bullet("Save the HOST + recurring sets/props as ELEMENTS (for Seedream use Elements + reference images — NOT Soul).")
bullet("Keep one approved STYLE KEY-FRAME and attach it as a reference image to every generation.")
bullet("Reuse ONE SEED within a shot-family; change only ONE element per frame (shot families).")
bullet("Generate 2–4 variations per shot and keep the best — AI drifts slightly even with anchors.")
h2("7d. Clips")
bullet("Default to stills. Use a short (2–4s) clip ONLY where motion is essential (typing, a number ticking, a chart "
       "drawing, a coin flip). Generate the still first, then animate it.")
h2("7e. Plans & credits")
bullet("Seedream ≈ 1 credit/image; Nano Banana Pro ≈ 2.  Free reloads ~10/day (no rollover, basic models only).")
bullet("Plus ≈ $39/mo annual = 1,000 credits/mo (~2–4 episodes on credits alone).")
bullet("Ultra ≈ $99/mo annual = 3,000 credits/mo + best unlimited coverage + lowest cost/credit (recommended for "
       "daily output, generating the bulk free in the web app).")
bullet("Credits expire 90 days and don't roll over. Daily output on credits alone would need ~9,000–18,000/mo — so "
       "rely on web-app unlimited Seedream, not credits.")

# ---------------- 8. PROCEDURE ----------------
h1("8. Step-by-Step Procedure When a Row Is Called")
for x in [
    "Read the row: concept, specific aspect, chosen animal match (higher %), and flags.",
    "Write the benefit-led suspense HOOK (3a).",
    "Write the full clean narration script using the retention arc (3b) to target length (3c).",
    "Compute duration (words ÷ 2.5) and segment into 3–5s shots; assign timestamps (5a).",
    "Build the SHOT LIST (Deliverable A): narration slice, one-line visual, file name, type per shot.",
    "Group shots into shot families so consecutive images flow.",
    "Build the PROMPT PACK (Deliverable B, Section 6): consistency header + one paste-ready, under-3000-char prompt "
    "per shot, restating characters verbatim.",
    "Produce the IMAGES (Deliverable C) by running the pack — free in the web app on Seedream 4.5 (recommended), or "
    "via API at credit cost — 16:9, reusing the Host Element + style key-frame; Nano Banana Pro only for text frames.",
    "For CLIP shots, generate the still then animate it.",
    "Save all three deliverables per Section 5b naming, then run the checklists (Section 9).",
]:
    num(x)

# ---------------- 9. CHECKLISTS ----------------
h1("9. Quality Checklists")
h2("Script")
for c in ["Hook is benefit-led/suspenseful and doesn't just name the concept.",
          "Arc: stakes → animal → parallel → where-it-breaks-down → payoff → button.",
          "A question/open loop ~every 20–30s; reads naturally aloud; hits target runtime."]:
    doc.add_paragraph("☐  " + c, style="List Bullet")
h2("Shot list & timing")
for c in ["Every shot 3–5s; one image per shot; timestamps sum to total duration.",
          "Numbers match across shot list, prompt pack, and image files."]:
    doc.add_paragraph("☐  " + c, style="List Bullet")
h2("Prompt pack")
for c in ["Consistency header present (compact style tag + character/world bible + palette + settings).",
          "Every per-shot prompt restates characters VERBATIM and is under 3000 characters.",
          "Self-contained, paste-ready, numbered to match; seed/shot-family noted."]:
    doc.add_paragraph("☐  " + c, style="List Bullet")
h2("Images (each)")
for c in ["Flat colors only; palette only; coral on the one focal element.",
          "No black outlines/gradients/3D; subtle grain + soft flat shadows.",
          "Recurring characters identical to their canonical reference.",
          "16:9; clear subject; bottom 15% caption-safe; consecutive frames interconnect."]:
    doc.add_paragraph("☐  " + c, style="List Bullet")

# ---------------- APPENDIX ----------------
h1("Appendix — Copy-Paste Blocks")
box("FULL MASTER STYLE SUFFIX (for single hero images where length is not a constraint):", FULL_SUFFIX)
box("COMPACT STYLE TAG (for per-shot prompts — keeps each under 3000 chars):", COMPACT_SUFFIX)
box("NEGATIVE / AVOID:",
    "photorealism, 3D render, CGI, realistic textures, gradients, glossy/metallic highlights, ambient occlusion, "
    "drop shadows, lens flare, glow/bloom, heavy black outlines, comic linework, sketchy wobble, crosshatching, neon "
    "colors, dark/gritty mood, cluttered backgrounds, complex detailed faces, tiny illegible text, watermarks, extra "
    "limbs/fingers, natural photographic animal coloring.")

note = doc.add_paragraph()
r = note.add_run("End of master guide. Input: one row of finance_animal_behavior_matches.xlsx. Output: a shot-list "
                 ".docx, a Higgsfield prompt pack, and an image folder — fixed series style, visuals every 3–5 seconds.")
r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor.from_string("888888")

out = "/home/user/dataexploration/PROJECT_MASTER_GUIDE.docx"
doc.save(out)
print("Saved:", out)

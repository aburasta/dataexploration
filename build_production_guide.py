#!/usr/bin/env python3
"""Overall Production Guide (Word .docx) for the finance x animal-behavior
animated documentary series. Folds in the visual style module + the full
per-episode workflow. Designed to be uploaded to the Claude Projects section."""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def shade_cell(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))
    tcPr.append(shd)


def set_cell_text(cell, text, bold=False, size=9, color=None, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color.lstrip("#"))


def h1(doc, text):
    return doc.add_heading(text, level=1)


def h2(doc, text):
    return doc.add_heading(text, level=2)


def body(doc, text, size=10.5, italic=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.italic = italic
    return p


def bullet(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    p.add_run(text).font.size = Pt(size)
    return p


def numbered(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Number")
    p.add_run(text).font.size = Pt(size)
    return p


def box(doc, label, text):
    if label:
        lp = doc.add_paragraph()
        r = lp.add_run(label)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor.from_string("1F4E5F")
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    cell = tbl.cell(0, 0)
    shade_cell(cell, "F2F4F0")
    cell.text = ""
    run = cell.paragraphs[0].add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    doc.add_paragraph()


def callout(doc, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    cell = tbl.cell(0, 0)
    shade_cell(cell, "FBEFD6")
    cell.text = ""
    run = cell.paragraphs[0].add_run(text)
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string("8A4B16")
    doc.add_paragraph()


doc = Document()
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(10.5)

# ============================ TITLE ============================
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("PRODUCTION GUIDE"); r.bold = True; r.font.size = Pt(28)
r.font.color.rgb = RGBColor.from_string("1F4E5F")
s = doc.add_paragraph(); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run("Finance × Animal Behavior — Animated YouTube Documentary Series")
r.font.size = Pt(13); r.font.color.rgb = RGBColor.from_string("EF5A2A")
s2 = doc.add_paragraph(); s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s2.add_run("Master instructions for turning ONE row of the concept spreadsheet "
               "into a finished episode (shot list + image folder). Upload to the Claude Projects section.")
r.italic = True; r.font.size = Pt(10)
doc.add_paragraph()

# ============================ 0. MISSION ============================
h1(doc, "0. What This Project Does")
body(doc, "This is a YouTube documentary series that explains difficult finance concepts by paralleling them to "
          "specific animal behaviors. Each episode takes ONE row from the file "
          "“finance_animal_behavior_matches.xlsx” and turns it into a short, highly engaging animated explainer.")
body(doc, "When the user names or pastes a row (a finance concept + its animal-behavior match), Claude must produce "
          "the TWO deliverables defined in Part 3, following every rule in this guide. The visual style (Part 7) and "
          "the script/hook formula (Part 4) are FIXED and identical for every episode — only the content changes.")

callout(doc, "THE ONE RULE ABOVE ALL: Every single video uses the exact same visual style defined in Part 7. "
             "The style never changes from episode to episode. Consistency across episodes IS the brand.")

# ============================ 1. INPUT ============================
h1(doc, "1. The Input: One Spreadsheet Row")
body(doc, "Source file: finance_animal_behavior_matches.xlsx. Each row contains:")
bullet(doc, "Category, Granular Concept, and The Specific Finance Aspect — the precise idea to teach.")
bullet(doc, "Animal Match 1 & 2 (name + a script-ready behavior description + a quality %).")
bullet(doc, "Notes / verification flags.")
body(doc, "Default behavior: build the episode around the HIGHER-rated match. Use the second match only if it adds a "
          "distinct facet, or in the honesty beat (see Part 4). If a match is flagged below 75% or “debated,” lean "
          "into the “where the analogy breaks down” section rather than overstating it.")

# ============================ 2. OUTPUT OVERVIEW ============================
h1(doc, "2. The Output: Two Deliverables, Every Time")
body(doc, "For each row called, Claude produces exactly two things:")
numbered(doc, "DELIVERABLE A — THE SHOT LIST (a Word document). A reader-ready narration script broken into shots, "
              "each with a timestamp range and the exact image to be shown during that stretch of script. Visuals "
              "change every 3–5 seconds.")
numbered(doc, "DELIVERABLE B — THE IMAGE FOLDER. A folder containing every image referenced in the shot list, "
              "generated with Higgsfield’s best image model in the fixed series style, named to match the shots.")
body(doc, "The shot list and the folder are linked one-to-one: shot_001 in the document corresponds to shot_001.png "
          "in the folder. (See Part 9 for naming.)")

# ============================ 3. DELIVERABLE A SPEC ============================
h1(doc, "3. Deliverable A — The Shot List Document")
body(doc, "Structure of the document, top to bottom:")
numbered(doc, "Header block: Episode title, the finance concept, the animal match used, target runtime, total word "
              "count, and narration pace used (default 150 words/min).")
numbered(doc, "CLEAN NARRATION SCRIPT: the full voice-over written as continuous prose, ready to read aloud "
              "start to finish with no interruptions. This is what the narrator records.")
numbered(doc, "THE SHOT LIST TABLE: the same script broken into timed shots with image instructions (columns below).")
body(doc, "Shot list table columns:")
bullet(doc, "Shot # (e.g., 001).")
bullet(doc, "Timestamp (start–end, mm:ss–mm:ss).")
bullet(doc, "Narration for this shot (the exact words spoken during this stretch — ~8–13 words = 3–5 seconds).")
bullet(doc, "On-screen visual (one-line description of what the image shows).")
bullet(doc, "Image file (e.g., shot_001.png) — matches the folder.")
bullet(doc, "Type (STILL or CLIP — clip only where motion is essential, see Part 8).")
bullet(doc, "Higgsfield prompt (the full prompt used to generate this image, INCLUDING the Master Style Suffix).")

# ============================ 4. SCRIPT RULES ============================
h1(doc, "4. Script Rules (identical every episode)")

h2(doc, "4a. The Hook (first ~5–15 seconds) — the most important part")
body(doc, "The hook ALWAYS creates suspense around the personal BENEFIT of knowing the lesson. Frame it as an "
          "intriguing question (or a “what if”) that makes the viewer feel they’re about to gain an edge most people "
          "miss. Do NOT open by naming the concept; open with the payoff and the mystery.")
body(doc, "Formula: [Tease the benefit / the edge] → [pose a question or “what if” the viewer wants answered] → "
          "[promise the animal will reveal the answer]. Keep it punchy.")
box(doc, "HOOK EXAMPLES (benefit-led, suspenseful):",
    "Lesson = avoid herd behavior →\n"
    "  “How do the people who spot the next big thing always see it before everyone else? "
    "The answer is hiding in how a single bird breaks from the flock...”\n\n"
    "Lesson = risk pooling / insurance →\n"
    "  “What if one bad month could never wipe you out — no matter how unlucky you got? "
    "A tiny vampire bat has quietly solved this for millions of years.”\n\n"
    "Lesson = compounding →\n"
    "  “What if doing one small, boring thing today decided whether you’re rich in 20 years? "
    "A colony of bees shows exactly when the magic kicks in.”")

h2(doc, "4b. Retention Structure (after the hook)")
body(doc, "Arrange the body to hold attention as tightly as possible:")
numbered(doc, "HOOK — benefit + question (above).")
numbered(doc, "STAKES — quickly make the viewer feel why getting this wrong hurts them (loss aversion pulls attention).")
numbered(doc, "MEET THE ANIMAL — introduce the animal and its behavior vividly (use the spreadsheet description).")
numbered(doc, "THE PARALLEL — map the behavior onto the finance aspect, step by step, one idea at a time.")
numbered(doc, "THE TURN / “WHERE IT BREAKS DOWN” — honestly note where the analogy stops (this builds trust and "
              "teaches nuance; it is a signature of the series).")
numbered(doc, "THE PAYOFF — deliver the practical lesson promised in the hook: what the viewer should DO or notice.")
numbered(doc, "BUTTON — a short, memorable closing line (and a soft prompt to subscribe / next episode).")
body(doc, "Throughout: short sentences, concrete imagery, open loops (tease something resolved later), and a question "
          "every ~20–30 seconds to re-grab attention. Conversational, warm, smart — never lecture-y.")

h2(doc, "4c. Length & Pace")
bullet(doc, "Target runtime: 4–7 minutes (default ~5). State the chosen target in the header.")
bullet(doc, "Narration pace: 150 words/minute = 2.5 words/second (documentary-calm). Adjustable, but state it.")
bullet(doc, "At 150 wpm, a 5-minute episode ≈ 750 words.")

# ============================ 5. TIMING METHOD ============================
h1(doc, "5. Timing & Timestamp Method (every shot = 3–5 seconds)")
body(doc, "How Claude assigns timestamps and the per-shot image cadence:")
numbered(doc, "Write the full clean narration script first.")
numbered(doc, "Compute total duration: total_words ÷ 2.5 = seconds (at 150 wpm).")
numbered(doc, "Segment the script into SHOTS of 3–5 seconds each. At 2.5 words/sec that is roughly 8–13 words per "
              "shot — usually one short sentence or clause per shot.")
numbered(doc, "Assign each shot a cumulative timestamp range (shot 1: 00:00–00:04, shot 2: 00:04–00:09, etc.), "
              "computing each shot’s length as its_word_count ÷ 2.5.")
numbered(doc, "Every shot gets exactly ONE image (still or clip). This guarantees the on-screen visual changes "
              "every 3–5 seconds, as required.")
callout(doc, "RESULT: a 5-minute (~750-word) episode produces roughly 75–100 shots — i.e., 75–100 images in the "
             "folder. Plan generation accordingly.")
body(doc, "Round timestamps to whole seconds. Keep the sum of shot lengths equal to the total duration.")

# ============================ 6. SHOT LIST EXAMPLE ============================
h1(doc, "6. Worked Example — Shot List Excerpt")
body(doc, "Concept: Risk pooling. Animal: vampire bat reciprocal blood sharing (96%). The first ~25 seconds, to show "
          "the exact format Claude must produce (image prompts shown condensed; append the Master Style Suffix in full).")

ex = [
    ("001", "00:00–00:05", "What if one bad month could never wipe you out — no matter how unlucky you got?",
     "Host fox leaning in, curious, spotlight on face, cozy dark frame", "shot_001.png", "STILL"),
    ("002", "00:05–00:09", "Most people are just one emergency away from losing everything.",
     "A lone teal figure standing small; a thin coral crack opening in the ground beneath", "shot_002.png", "STILL"),
    ("003", "00:09–00:13", "But some never seem to get destroyed by a single disaster.",
     "Three rounded figures standing together, calm, a soft protective dome over them", "shot_003.png", "STILL"),
    ("004", "00:13–00:18", "Their secret was solved millions of years ago — by a tiny vampire bat.",
     "Cute navy-and-teal vampire bat hanging, friendly dot eyes, warm hollow", "shot_004.png", "STILL"),
    ("005", "00:18–00:23", "A vampire bat must drink within two days, or it dies.",
     "Same bat, a small clock/moon motif; one bat looking weak, slightly grey", "shot_005.png", "STILL"),
    ("006", "00:23–00:27", "And on any night, some of them fail to feed.",
     "Two bats: one with a coral droplet (fed), one empty and worried", "shot_006.png", "STILL"),
]
tbl = doc.add_table(rows=1, cols=6)
tbl.style = "Table Grid"
hdr = tbl.rows[0].cells
for i, h in enumerate(["Shot", "Timestamp", "Narration", "On-screen visual", "File", "Type"]):
    set_cell_text(hdr[i], h, bold=True, size=8.5, color="FFFFFF")
    shade_cell(hdr[i], "1F4E5F")
for shot, ts, narr, vis, f, typ in ex:
    c = tbl.add_row().cells
    set_cell_text(c[0], shot, size=8.5)
    set_cell_text(c[1], ts, size=8.5)
    set_cell_text(c[2], narr, size=8.5)
    set_cell_text(c[3], vis, size=8.5)
    set_cell_text(c[4], f, size=8.5)
    set_cell_text(c[5], typ, size=8.5)
for row in tbl.rows:
    row.cells[0].width = Inches(0.4)
    row.cells[1].width = Inches(0.9)
    row.cells[2].width = Inches(2.4)
    row.cells[3].width = Inches(2.4)
    row.cells[4].width = Inches(0.8)
    row.cells[5].width = Inches(0.5)
doc.add_paragraph()
body(doc, "Note how each shot is one short clause (~3–5s) with its own image, and the images interconnect (same bat, "
          "same hollow, one element changing) so the stills read as continuous animation. The full document would "
          "also include the clean narration script above this table.", italic=True)

# ============================ 7. VISUAL STYLE MODULE ============================
h1(doc, "7. Visual Style — Applied to EVERY Episode")
callout(doc, "This style is mandatory and unchanging. Every image in every episode must match it. Append the Master "
             "Style Suffix (Part 8) to every Higgsfield prompt.")

body(doc, "The look in one sentence: warm, friendly, FLAT 2D vector illustration in a mid-century-modern "
          "“explainer animation” style — bold simple shapes, a tight cozy palette, no harsh outlines, flat lighting, "
          "and a subtle grain texture (the Hey Duggee / modern motion-graphics family).")

h2(doc, "7a. Core Traits")
for tr in [
    "FLAT: flat color only — no gradients, no realistic shading, no 3D, no gloss.",
    "SHAPE-FIRST: built from circles, ovals, rounded rectangles with soft rounded corners. Chunky, friendly, stable.",
    "OUTLINE-LESS: forms separated by color, not black ink lines.",
    "WARM LIMITED PALETTE (below). Nothing neon.",
    "FLAT SOFT LIGHTING: gentle ambient light; shadows are soft flat shapes at low opacity, never dark.",
    "GRAIN: a fine film/paper texture over the whole frame, subtle.",
    "SIMPLE FACES: tiny dot eyes, minimal mouths; emotion via eyebrows and posture.",
    "COZY & UNCLUTTERED: simple props, generous negative space.",
]:
    bullet(doc, tr)

h2(doc, "7b. Color Palette (canonical hex values)")
palette = [
    ("Ochre Yellow", "#E8A93C", "Primary", "Backgrounds / large warm fields."),
    ("Warm Cream", "#F7EAD0", "Primary", "Light backgrounds, negative space."),
    ("Teal Blue", "#3C7C9A", "Secondary", "Main character bodies, calm zones."),
    ("Deep Navy", "#21465A", "Secondary", "Depth, dark accents, grounding."),
    ("Coral Red-Orange", "#EF5A2A", "Accent", "THE focal color — the key idea. Use sparingly."),
    ("Burnt Orange", "#CC6B2C", "Accent", "Plants, warm secondary accents."),
    ("Moss Olive", "#A7A24A", "Accent", "Foliage, variety."),
    ("Off-White", "#FCF6EA", "Neutral", "Highlights, eye whites."),
    ("Charcoal", "#2C2A29", "Neutral", "Eyes / fine details only — never pure black, never an outline."),
]
pt = doc.add_table(rows=1, cols=5); pt.style = "Table Grid"
hd = pt.rows[0].cells
for i, x in enumerate(["Swatch", "Name", "Hex", "Role", "Usage"]):
    set_cell_text(hd[i], x, bold=True, size=8.5, color="FFFFFF"); shade_cell(hd[i], "1F4E5F")
for name, hexv, role, usage in palette:
    c = pt.add_row().cells
    shade_cell(c[0], hexv); set_cell_text(c[0], "", size=8.5)
    set_cell_text(c[1], name, bold=True, size=8.5)
    set_cell_text(c[2], hexv, size=8.5)
    set_cell_text(c[3], role, size=8.5)
    set_cell_text(c[4], usage, size=8.5)
for row in pt.rows:
    row.cells[0].width = Inches(0.5)
    row.cells[1].width = Inches(1.3)
    row.cells[2].width = Inches(0.9)
    row.cells[3].width = Inches(0.9)
    row.cells[4].width = Inches(2.8)
doc.add_paragraph()
bullet(doc, "60/30/10: ~60% warm neutrals (ochre, cream), ~30% blues, ~10% coral accent. Coral marks what to look at.")
bullet(doc, "No pure black, no pure white — use Charcoal and Off-White.")

h2(doc, "7c. Characters")
bullet(doc, "THE HOST (recurring narrator): one fixed friendly animal guide (recommended: a rounded teal fox with a "
            "signature coral scarf and dot eyes) appearing in every episode. Lock ONE design and reuse it identically.")
bullet(doc, "ANIMAL OF THE WEEK: the spreadsheet animal, re-tinted into the palette (NOT natural photo colors), "
            "simplified into friendly geometric shapes.")
bullet(doc, "CROWDS / MARKETS / “YOU”: simple rounded humanoid silhouettes in palette colors; the odd-one-out is coral.")

h2(doc, "7d. Finance Motifs (in-style)")
bullet(doc, "Charts: chunky rounded bars/lines, key line in coral, minimal axes — never realistic stock screenshots.")
bullet(doc, "Money: flat ochre coins; stacks as rounded rectangles. Arrows: thick rounded; coral/burnt-orange for alarm.")
bullet(doc, "Keep one consistent icon vocabulary across all episodes (herd = identical shapes, growth = sprouting plant, etc.).")

h2(doc, "7e. Composition")
bullet(doc, "16:9 every frame. Highest available resolution.")
bullet(doc, "One clear subject, centered or on a thirds point, with breathing room.")
bullet(doc, "Keep the bottom ~15% clear (caption-safe). Vary shot scale (wide/medium/close) across a sequence.")

# ============================ 8. IMAGE GENERATION ============================
h1(doc, "8. Image Generation with Higgsfield")

h2(doc, "8a. Model & Settings")
bullet(doc, "Use Higgsfield’s BEST current image model — Nano Banana Pro (model id: nano_banana_pro). If unsure it is "
            "still the top model, run models_explore first and pick the highest-quality image model available.")
bullet(doc, "aspect_ratio: 16:9. Highest resolution offered. Generate one image per shot (use count to batch a scene).")
bullet(doc, "For motion shots, generate the STILL first, then animate it with image-to-video so the style is preserved.")

h2(doc, "8b. Consistency (so frames flow like one animation)")
bullet(doc, "Save the Host (and recurring props/sets) as a Higgsfield ELEMENT, or train a SOUL for the Host, and "
            "reference it in every prompt so the character is identical across all shots and all episodes.")
bullet(doc, "Keep one approved “style key frame” and pass it as a reference image so new frames inherit palette/grain/finish.")
bullet(doc, "Work in SHOT FAMILIES: within a beat, keep the same background, character, palette, and camera, and change "
            "only ONE thing per shot (a pose, a prop, the camera distance). Successive stills then read as motion.")
bullet(doc, "Describe recurring characters with the SAME wording every time.")

h2(doc, "8c. When to use a CLIP instead of a STILL")
body(doc, "Default to stills. Use a short (2–4s) video clip ONLY when motion is essential and cannot be faked by a "
          "few interconnected stills, e.g.: text being typed on screen, a number ticking up, a chart drawing itself, "
          "a coin flip, a fast chase, or a transformation. Mark these as CLIP in the shot list.")

h2(doc, "8d. The Master Prompt Formula")
body(doc, "Every image prompt = [SHOT type] + [SUBJECT described identically] + [single clear ACTION] + [SETTING] + "
          "[where the coral accent goes] + the Master Style Suffix appended verbatim.")
box(doc, "MASTER STYLE SUFFIX (append to EVERY image/video prompt):",
    "Flat 2D vector illustration in a warm mid-century-modern explainer-animation style (in the spirit of Hey "
    "Duggee / modern motion-graphics). Bold simple geometric shapes with soft rounded corners. No outlines — forms "
    "defined by flat color blocks. Limited warm palette: ochre yellow (#E8A93C), warm cream (#F7EAD0), teal blue "
    "(#3C7C9A), deep navy (#21465A), coral red-orange (#EF5A2A), burnt orange (#CC6B2C). Flat soft ambient lighting, "
    "gentle minimal flat shadows. Subtle fine film-grain / paper texture over the whole frame. Simple dot eyes, "
    "minimal facial features. Cozy, friendly, clean, generous negative space. 16:9. No gradients, no 3D, no realistic "
    "shading, no glossy highlights, no heavy black outlines, no clutter, no photorealism.")
box(doc, "NEGATIVE / AVOID:",
    "photorealism, 3D render, CGI, realistic textures, gradients, glossy/metallic highlights, ambient occlusion, "
    "drop shadows, lens flare, glow/bloom, heavy black outlines, comic linework, sketchy wobble, crosshatching, neon "
    "colors, dark/gritty mood, cluttered backgrounds, complex detailed faces, tiny illegible text, watermarks, extra "
    "limbs/fingers, natural photographic animal coloring.")

# ============================ 9. FILE OUTPUT ============================
h1(doc, "9. Output Files & Naming")
body(doc, "Produce this structure per episode (EP number + short concept slug):")
box(doc, "FOLDER STRUCTURE:",
    "EP07_risk-pooling_vampire-bat/\n"
    "    EP07_shot-list.docx          <- Deliverable A (clean script + shot table)\n"
    "    images/                      <- Deliverable B\n"
    "        shot_001.png\n"
    "        shot_002.png\n"
    "        shot_003.png\n"
    "        ...\n"
    "        shot_0NN.png\n"
    "    clips/                       <- only if any CLIP shots exist\n"
    "        shot_0XX.mp4")
bullet(doc, "Image filenames MUST match the shot list (shot_001.png ↔ Shot 001). Zero-pad to 3 digits.")
bullet(doc, "One image per shot. Clips go in /clips with the same shot number and are marked CLIP in the table.")

# ============================ 10. PROCEDURE ============================
h1(doc, "10. Step-by-Step Procedure When a Row Is Called")
for step in [
    "Read the row: note the concept, the specific finance aspect, the chosen animal match (higher %), and any flags.",
    "Write the HOOK using the benefit-led suspense formula (Part 4a).",
    "Write the full clean narration script using the retention structure (Part 4b), to the target length (Part 4c).",
    "Compute total duration (words ÷ 2.5) and segment into 3–5s shots (~8–13 words each); assign timestamps (Part 5).",
    "Build the shot list table: for each shot write the narration slice, a one-line visual, file name, type, and the "
    "full Higgsfield prompt (subject + action + setting + Master Style Suffix).",
    "Confirm interconnection: group shots into shot families so consecutive images flow (Part 8b).",
    "Generate every image on Higgsfield’s best model at 16:9, reusing the Host Element/Soul and style key frame.",
    "For any CLIP shots, generate the still then animate it.",
    "Save Deliverable A (shot-list.docx) and Deliverable B (images/ folder, + clips/ if needed) per Part 9 naming.",
    "Run the checklists (Part 11) before delivering.",
]:
    numbered(doc, step)

# ============================ 11. CHECKLISTS ============================
h1(doc, "11. Quality Checklists")
h2(doc, "Script")
for c in [
    "Hook is benefit-led and suspenseful (a question/what-if), and does NOT just name the concept.",
    "Body follows: stakes → animal → parallel → where-it-breaks-down → payoff → button.",
    "A question or open loop roughly every 20–30 seconds.",
    "Reads naturally aloud; short concrete sentences; matches target runtime.",
]:
    doc.add_paragraph("☐  " + c, style="List Bullet")
h2(doc, "Shot list & timing")
for c in [
    "Every shot is 3–5 seconds; one image per shot.",
    "Timestamps are cumulative and sum to total duration.",
    "Each shot has narration, visual, file name, type, and a full prompt with the Master Style Suffix.",
    "File names match the images folder exactly.",
]:
    doc.add_paragraph("☐  " + c, style="List Bullet")
h2(doc, "Images (every single one)")
for c in [
    "Flat colors only; palette only; coral reserved for the focal element.",
    "No black outlines, no gradients, no 3D; subtle grain and soft flat shadows present.",
    "Recurring characters identical to their canonical reference.",
    "16:9; clear subject; bottom 15% caption-safe; cozy on-brand mood.",
    "Consecutive images in a beat interconnect (read as animation).",
]:
    doc.add_paragraph("☐  " + c, style="List Bullet")

doc.add_paragraph()
note = doc.add_paragraph()
r = note.add_run("End of guide. Inputs: finance_animal_behavior_matches.xlsx. Outputs per row: one shot-list .docx "
                 "and one image folder, in the fixed series style, with visuals changing every 3–5 seconds.")
r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor.from_string("888888")

out = "/home/user/dataexploration/PRODUCTION_GUIDE.docx"
doc.save(out)
print("Saved:", out)

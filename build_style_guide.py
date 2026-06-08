#!/usr/bin/env python3
"""Generate the cartoon style guide (Word .docx) for the
finance x animal-behavior documentary series."""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ---------- helpers ----------
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
    p = doc.add_heading(text, level=1)
    return p


def h2(doc, text):
    return doc.add_heading(text, level=2)


def body(doc, text, size=10.5):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    return p


def bullet(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    run.font.size = Pt(size)
    return p


def numbered(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Number")
    run = p.add_run(text)
    run.font.size = Pt(size)
    return p


def prompt_box(doc, label, text):
    """A shaded, monospace-ish copy-paste block."""
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
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    doc.add_paragraph()


doc = Document()

# base font
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)

# ============================ TITLE ============================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("VISUAL STYLE GUIDE")
r.bold = True
r.font.size = Pt(26)
r.font.color.rgb = RGBColor.from_string("1F4E5F")

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Finance × Animal Behavior — Animated Documentary Series")
r.font.size = Pt(13)
r.font.color.rgb = RGBColor.from_string("EF5A2A")

sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run("The single source of truth for the look of every image and clip. "
                 "This is the art-direction module of the larger production guide.")
r.italic = True
r.font.size = Pt(10)

doc.add_paragraph()

# ============================ 0. HOW TO USE ============================
h1(doc, "0. How to Use This Guide")
body(doc, "This document defines the fixed visual language of the series so that hundreds of separately "
          "generated images stay perfectly on-brand and flow together as if hand-animated. Two audiences use it:")
bullet(doc, "A human (you) reviewing and approving images.")
bullet(doc, "An AI image/video model (Higgsfield) generating them. Every generation prompt MUST end with the "
            "Master Style Suffix in Section 13, and respect the Negative/Avoid list in Section 14.")
body(doc, "Golden rule: the STYLE never changes from video to video — only the CONTENT (which animal, which "
          "scene, which finance idea) changes. Consistency is the brand.")

# ============================ 1. NORTH STAR ============================
h1(doc, "1. The Look in One Sentence")
body(doc, "Warm, friendly, flat 2D vector illustration in a mid-century-modern “explainer animation” style "
          "— bold simple shapes, a tight cozy color palette, no harsh outlines, flat lighting, and a subtle "
          "grain texture — the same family as Hey Duggee, modern motion-graphics explainers, and warm "
          "children’s-book illustration.")
body(doc, "Emotional target: approachable, calm, clever, and a little cozy. Even when the topic is a market crash, "
          "the visuals stay warm and disarming — that contrast is part of the channel’s charm.")

# ============================ 2. REFERENCE BREAKDOWN ============================
h1(doc, "2. Reference Image — What Defines the Style")
body(doc, "The approved reference (cozy living room with two rounded characters) establishes these non-negotiable traits:")
bullet(doc, "FLAT: everything is flat color. No gradients, no realistic shading, no 3D, no glossy highlights.")
bullet(doc, "SHAPE-FIRST: characters and objects are built from clean geometric shapes (circles, ovals, rounded "
            "rectangles) with soft rounded corners. Chunky, stable, friendly.")
bullet(doc, "OUTLINE-LESS: forms are separated by color, not by black ink lines. At most, very subtle tonal interior "
            "detail — never a heavy comic outline.")
bullet(doc, "WARM LIMITED PALETTE: ochre yellow, cream, teal blue, deep navy, coral orange, burnt orange. Nothing neon.")
bullet(doc, "FLAT, SOFT LIGHTING: a single gentle ambient light; shadows are simple flat shapes at low opacity, never dark.")
bullet(doc, "GRAIN: a fine film/paper-grain texture sits over the whole frame, giving a soft printed warmth.")
bullet(doc, "COZY DETAILING: simple props (pendant lamp, monstera plant, armchair, window with autumn trees), generous "
            "negative space, nothing cluttered.")
bullet(doc, "SIMPLE FACES: tiny dot eyes and minimal mouths; emotion comes from eyebrows, posture, and gesture.")

# ============================ 3. COLOR PALETTE ============================
h1(doc, "3. Color Palette")
body(doc, "Use these colors and (sparingly) tints/shades of them. A tight palette is what makes every frame feel like "
          "the same show. Hex values are the canonical reference.")

palette = [
    ("Ochre Yellow", "#E8A93C", "Primary", "Dominant background / walls / large warm fields."),
    ("Warm Cream", "#F7EAD0", "Primary", "Light backgrounds, negative space, paper base."),
    ("Teal Blue", "#3C7C9A", "Secondary", "Main character bodies, cool objects, calm zones."),
    ("Deep Navy", "#21465A", "Secondary", "Depth, overalls, dark accents, grounding shadows."),
    ("Coral Red-Orange", "#EF5A2A", "Accent", "THE focal color. Hero element, the key idea, call-to-action. Use sparingly."),
    ("Burnt Orange", "#CC6B2C", "Accent", "Plants, secondary warm accents, autumn tones."),
    ("Moss Olive", "#A7A24A", "Accent", "Foliage, variety, occasional cool-warm bridge."),
    ("Off-White", "#FCF6EA", "Neutral", "Highlights, eye whites, small bright pops."),
    ("Charcoal", "#2C2A29", "Neutral", "Eyes and fine details ONLY — never pure black, never as an outline."),
]

tbl = doc.add_table(rows=1, cols=5)
tbl.style = "Table Grid"
hdr = tbl.rows[0].cells
for i, t in enumerate(["Swatch", "Name", "Hex", "Role", "Usage"]):
    set_cell_text(hdr[i], t, bold=True, size=9, color="FFFFFF")
    shade_cell(hdr[i], "1F4E5F")
for name, hexv, role, usage in palette:
    cells = tbl.add_row().cells
    shade_cell(cells[0], hexv)
    set_cell_text(cells[0], "", size=9)
    set_cell_text(cells[1], name, bold=True, size=9)
    set_cell_text(cells[2], hexv, size=9)
    set_cell_text(cells[3], role, size=9)
    set_cell_text(cells[4], usage, size=9)
# widths
for row in tbl.rows:
    row.cells[0].width = Inches(0.6)
    row.cells[1].width = Inches(1.3)
    row.cells[2].width = Inches(0.9)
    row.cells[3].width = Inches(0.9)
    row.cells[4].width = Inches(3.2)

doc.add_paragraph()
body(doc, "Palette rules:")
bullet(doc, "60 / 30 / 10: ~60% warm neutrals (ochre, cream), ~30% the blues, ~10% the orange accent. The coral is a "
            "spotlight — reserve it for whatever the viewer should look at.")
bullet(doc, "No pure black and no pure white. Use Charcoal and Off-White instead.")
bullet(doc, "Backgrounds stay muted; characters and the key idea carry the saturation.")

# ============================ 4. SHAPE & FORM ============================
h1(doc, "4. Shape & Form Language")
bullet(doc, "Build everything from circles, ovals, and rounded rectangles. Corners are always softened.")
bullet(doc, "Chunky and stable: thick limbs, solid bodies, low centers of gravity. Nothing thin or spiky.")
bullet(doc, "Geometric simplification: a tree is a few rounded blobs; a building is rounded rectangles; a cloud is "
            "overlapping circles.")
bullet(doc, "Symmetry and balance over realism. Proportions are playful, not anatomically correct.")

# ============================ 5. LINE & TEXTURE ============================
h1(doc, "5. Line, Outline & Texture")
bullet(doc, "Outlines: essentially none. Separate shapes with color contrast. If a detail line is unavoidable, make it "
            "a darker tint of the same fill, thin and soft — never black.")
bullet(doc, "Texture: a uniform fine film/paper grain over the entire frame at low opacity. It must be subtle — "
            "warmth, not noise.")
bullet(doc, "Edges: clean vector edges, slightly soft. No sketchy, hand-drawn wobble; no crosshatching.")

# ============================ 6. LIGHTING & SHADOW ============================
h1(doc, "6. Lighting & Shadow")
bullet(doc, "Flat ambient light, gentle direction from the upper-left.")
bullet(doc, "Shadows are simple flat shapes (an oval under a character, a soft block under furniture) at ~10–15% "
            "opacity in a warm tone — never dark or sharp.")
bullet(doc, "No cast-shadow realism, no ambient occlusion, no glow, no lens flare.")

# ============================ 7. CHARACTER SYSTEM ============================
h1(doc, "7. Character Design System")
body(doc, "There are three character types. All obey the same shape, palette, and face rules.")

h2(doc, "7a. The Host (recurring narrator)")
body(doc, "A single friendly animal guide who appears in every episode for brand continuity. Recommended: a warm, "
          "approachable mammal (e.g., a rounded fox or bear) rendered in the palette — teal or ochre body, coral "
          "scarf or accessory as a signature, simple dot eyes. Lock ONE design and reuse it everywhere.")
bullet(doc, "Keep a fixed turnaround: same proportions, same colors, same signature accessory in every shot.")
bullet(doc, "Expression range via eyebrows + posture: curious, surprised, thinking, reassuring.")

h2(doc, "7b. The “Animal of the Week”")
body(doc, "Each episode features the animal from the chosen spreadsheet row (vampire bat, gazelle, honeybee, locust, "
          "etc.). Render it in-style: simplified geometric form, flat palette colors (re-tint the real animal into the "
          "series palette rather than using natural photo colors), tiny dot eyes, friendly proportions.")

h2(doc, "7c. Abstract / Human Figures (markets, crowds, “you”)")
body(doc, "For crowds, traders, or the viewer stand-in, use simple rounded humanoid silhouettes in palette colors "
          "— no detailed faces. A crowd is a field of identical rounded shapes; the odd one out is coral.")

h2(doc, "7d. Faces & Expressions")
bullet(doc, "Eyes: small charcoal dots or short ovals. Optional tiny off-white catchlight.")
bullet(doc, "Mouths: minimal — a small line, oval, or curve. Often none.")
bullet(doc, "Eyebrows do the emotional heavy lifting. Cheeks (a soft coral oval) for warmth when needed.")

h2(doc, "7e. Character Consistency (critical)")
bullet(doc, "Save the Host (and any repeated prop) as a Higgsfield ELEMENT, or train a Soul, and reuse it in every "
            "prompt so the character stays identical across frames. (See Section 12.)")
bullet(doc, "Keep one canonical reference image of each character and pass it as a reference in new generations.")
bullet(doc, "Always describe the character the same way, word-for-word, in prompts.")

# ============================ 8. ENVIRONMENTS ============================
h1(doc, "8. Environments & Backgrounds")
bullet(doc, "Cozy, simplified, mid-century interiors and soft stylized nature (forests, savanna, ocean) — "
            "always reduced to a few clean shapes.")
bullet(doc, "Generous negative space. The background supports the subject; it never competes.")
bullet(doc, "Recurring set: a warm “study/living-room” where the Host explains things, reused for continuity "
            "(pendant lamp, plant, window, armchair as in the reference).")
bullet(doc, "Depth via flat layered shapes and slight color-value shifts, not perspective realism.")

# ============================ 9. FINANCE MOTIFS ============================
h1(doc, "9. Finance Motifs, Icons & Charts (in-style)")
body(doc, "Finance concepts must be drawn in the SAME flat style — no realistic screenshots or stock chart imagery.")
bullet(doc, "Charts: bold rounded line/bar charts in palette colors; the key line is coral. Chunky, friendly, minimal axes.")
bullet(doc, "Coins / money: simple flat ochre circles with a minimal symbol; stacks as rounded rectangles.")
bullet(doc, "Arrows / trends: thick rounded arrows; up = teal/positive, down = burnt orange/coral for alarm.")
bullet(doc, "Abstractions: a “herd” as identical rounded shapes; “risk” as a wobbling shape; "
            "“growth” as a sprouting rounded plant. Keep one icon vocabulary across the series.")

# ============================ 10. TYPOGRAPHY ============================
h1(doc, "10. On-Screen Text & Typography")
bullet(doc, "Font: a friendly geometric rounded sans-serif (e.g., a Poppins / Quicksand / Nunito feel). One family only.")
bullet(doc, "Use text sparingly: key term, a number, a punchy phrase. Charcoal or navy on light fields; off-white on dark.")
bullet(doc, "Numbers and key terms can pop in coral for emphasis.")
bullet(doc, "Generating clean text inside images is unreliable — PREFER adding titles/captions in your video editor. "
            "If text must be in the image, keep it to 1–3 large words and verify spelling.")

# ============================ 11. COMPOSITION ============================
h1(doc, "11. Composition & Framing")
bullet(doc, "Aspect ratio: 16:9 for every frame (YouTube). Generate at the highest available resolution.")
bullet(doc, "One clear subject per frame, centered or on a rule-of-thirds point, with breathing room.")
bullet(doc, "Caption-safe zone: keep important content out of the bottom ~15% (room for subtitles/lower-thirds).")
bullet(doc, "Vary shot scale across a sequence (wide establishing → medium → close detail) to keep energy up.")

# ============================ 12. HIGGSFIELD PRODUCTION ============================
h1(doc, "12. Higgsfield Production Settings")
bullet(doc, "Image model: use a high-quality image model (e.g., Nano Banana Pro) for stills; aspect_ratio 16:9.")
bullet(doc, "Consistency tools: create ELEMENTS for the Host and recurring props, or train a SOUL for the Host, and "
            "reference them in every prompt. This is the #1 lever for frames that flow together.")
bullet(doc, "Style anchoring: keep one approved “style key frame” and pass it as a reference image so new "
            "frames inherit palette, grain, and finish.")
bullet(doc, "Short clips: use image-to-video ONLY where motion is essential (typing, a number ticking up, a chart "
            "drawing itself, a coin flip). Generate the still first, then animate it so the style matches. Keep clips 2–4s.")
bullet(doc, "Batch by scene: generate 3–6 frames per scene from the same anchor so a beat reads as one continuous shot.")

# ============================ 13. MASTER PROMPT FORMULA ============================
h1(doc, "13. The Master Prompt Formula")
body(doc, "Every image prompt = [SHOT] + [SUBJECT & ACTION] + [SETTING] + [the Master Style Suffix]. "
          "Append the suffix verbatim to lock the look.")

prompt_box(doc, "PROMPT TEMPLATE:",
           "[Shot type, e.g. medium shot] of [character described identically each time] "
           "[doing a clear single action], [short setting description]. [Where the coral accent goes]. "
           "+ MASTER STYLE SUFFIX")

prompt_box(doc, "MASTER STYLE SUFFIX (paste at the end of EVERY image prompt):",
           "Flat 2D vector illustration in a warm mid-century-modern explainer-animation style (in the spirit of "
           "Hey Duggee / modern motion-graphics). Bold simple geometric shapes with soft rounded corners. No outlines "
           "— forms defined by flat color blocks. Limited warm palette: ochre yellow (#E8A93C), warm cream "
           "(#F7EAD0), teal blue (#3C7C9A), deep navy (#21465A), coral red-orange (#EF5A2A), burnt orange (#CC6B2C). "
           "Flat soft ambient lighting, gentle minimal flat shadows. Subtle fine film-grain / paper texture over the "
           "whole frame. Simple dot eyes, minimal facial features. Cozy, friendly, clean, generous negative space. "
           "16:9. No gradients, no 3D, no realistic shading, no glossy highlights, no heavy black outlines, no clutter, "
           "no photorealism.")

# ============================ 14. NEGATIVE / AVOID ============================
h1(doc, "14. Negative / Avoid List")
body(doc, "Steer away from (state these as things to avoid in prompts):")
avoid = ("photorealism, 3D render, CGI, realistic textures, gradients, glossy or metallic highlights, ambient "
         "occlusion, drop shadows, lens flare, glow/bloom, heavy black ink outlines, comic-book linework, sketchy "
         "hand-drawn wobble, crosshatching, neon or saturated electric colors, dark/gritty mood, cluttered busy "
         "backgrounds, complex detailed faces, tiny illegible text, watermarks, extra limbs or fingers, "
         "natural photographic animal coloring (re-tint animals into the palette instead).")
prompt_box(doc, "NEGATIVE PROMPT / AVOID:", avoid)

# ============================ 15. WORKED EXAMPLES ============================
h1(doc, "15. Worked Example Prompts")
body(doc, "Each below already follows the formula; append the Master Style Suffix when generating.")

prompt_box(doc, "A) The Host introducing the episode:",
           "Medium shot of the Host — a rounded friendly teal fox with small charcoal dot eyes and a signature "
           "coral scarf — standing in a cozy mid-century living room, one paw raised mid-explanation, warm and "
           "curious expression. Pendant lamp, monstera plant, and a window with stylized autumn trees behind. The "
           "coral scarf is the focal accent. + MASTER STYLE SUFFIX")

prompt_box(doc, "B) Animal-of-the-week (vampire bat, risk-pooling episode):",
           "Wide shot of three rounded, friendly vampire bats re-tinted in deep navy and teal hanging in a softly "
           "lit hollow, one bat gently sharing a glowing coral droplet with a hungry neighbor. Cozy, warm, simple "
           "geometric forms, tiny dot eyes. The shared droplet is the coral focal point. + MASTER STYLE SUFFIX")

prompt_box(doc, "C) Finance abstraction (herd behavior):",
           "Top-down medium shot of a tight crowd of identical rounded teal figures all facing the same way, with a "
           "single coral figure turning to look the opposite direction. Flat ochre background, generous negative "
           "space. The lone coral figure is the focal point. + MASTER STYLE SUFFIX")

prompt_box(doc, "D) Chart reveal (use as a short clip if it animates):",
           "Medium shot of a chunky rounded line chart on a warm cream panel, a single bold coral line rising and "
           "then dipping, minimal navy axes, no realistic UI. Clean and friendly. The coral line is the focal point. "
           "+ MASTER STYLE SUFFIX")

# ============================ 16. SEQUENCE / FLOW ============================
h1(doc, "16. Making Stills Flow Like Animation")
body(doc, "Because the video changes visuals every 3–4 seconds, design images in connected SETS, not as isolated "
          "pictures:")
bullet(doc, "Work in “shot families”: keep the same background, character, palette, and camera, and change "
            "only ONE thing per frame (a pose, a prop, the camera distance, one element entering). Successive frames "
            "then read as continuous motion.")
bullet(doc, "Use the same Host Element / reference image across the family so the character is pixel-consistent.")
bullet(doc, "Plan beats: one idea = one shot family of 3–6 frames. Cut between families at topic changes.")
bullet(doc, "Reserve a true short video clip for motion that stills can’t fake (typing, counting numbers, drawing "
            "arrows, flips, fast movement).")

# ============================ 17. CHECKLIST ============================
h1(doc, "17. Per-Image Quality Checklist")
for item in [
    "Flat colors only — no gradients or realistic shading?",
    "Palette colors only, with coral reserved for the one focal element?",
    "No black outlines; shapes read by color?",
    "Subtle grain present; soft flat shadows only?",
    "Recurring characters identical to their canonical reference?",
    "16:9, clear single subject, caption-safe bottom 15% kept clear?",
    "Cozy, friendly, uncluttered — on-brand mood?",
    "Any on-image text limited and spelled correctly (or left for the editor)?",
]:
    p = doc.add_paragraph(style="List Bullet")
    r = p.add_run("☐  " + item)
    r.font.size = Pt(10.5)

doc.add_paragraph()
note = doc.add_paragraph()
r = note.add_run("This is the visual-style module. It will be merged into the overall production guide "
                 "(script structure, hook formula, image-timestamp syncing) per your earlier instructions.")
r.italic = True
r.font.size = Pt(9.5)
r.font.color.rgb = RGBColor.from_string("888888")

out = "/home/user/dataexploration/style_guide.docx"
doc.save(out)
print("Saved:", out)

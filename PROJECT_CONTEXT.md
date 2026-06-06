# COUP DOCUMENTARY AGENT — PROJECT CONTEXT

> **Purpose of this document.** This is the master context/operating manual for an
> agent that turns a single African *coup d'état* into a documentary-ready package
> (research dossier → voiceover script → timed footage shot list). Upload it to a
> project so any session has the full goal, standards, reusable prompts, and file
> conventions needed to generate the package for **any other coup** consistently.

---

## 1. PROJECT GOAL

Build documentaries about African coups. For each chosen coup, the agent produces:
1. A **deep-research dossier** — cross-checked, source-tagged, documentary-grade.
2. A **voiceover script** — a story, in a fixed dramatic structure, in the creator's voice.
3. A **timed footage shot list** — every ~3–5 seconds, a prescribed image/video with a
   real source link and licensing note (the agent finds *sources*; it does not download).

The first two coups are done as worked examples (see §8). The system is general:
point it at any unsuccessful-coup row and it develops the full package.

---

## 2. THE PIPELINE AT A GLANCE

| # | Node | Input | Output |
|---|------|-------|--------|
| 0 | **Row Selector** | the unsuccessful-coups spreadsheet | one chosen coup (random or user-supplied row) |
| 1 | **Deep-Research Dossier** | the chosen coup | `<case>_dossier.md/.docx` |
| 2 | **Narration / Voiceover + Timing** | Node 1 dossier | `<case>_script.md/.docx` |
| 3 | **Footage Shot-List** (image + source per beat) | Node 2 script | `<case>_shotlist.md/.docx` |
| 4 | **Voice Re-tune** (pending writing samples) | a script + samples | re-voiced script/shot list |

**Retired** (data already generated, do not re-run): a "Coup Dataset" node and an
"Extract Unsuccessful" node. Their outputs already exist as spreadsheets (§3).

**Golden rule across all nodes — the accuracy spine:** every factual claim is tagged
`[FACT]` / `[ALLEGED]` / `[DISPUTED]`, and these tags **propagate** from the dossier into
the script and shot list. **Narration must never state an allegation as established fact.**

---

## 3. SOURCE DATA (already produced)

- `african_coups_1950_present.xlsx` — all African coups 1950–present, tabs **All /
  Successful / Unsuccessful** (142 events: 99 successful, 43 unsuccessful), classified by
  Powell & Thyne convention (successful = power held ≥ ~7 days).
- `african_coups_unsuccessful.xlsx` — the 43 **unsuccessful** coups only. **This is the
  menu Node 0 draws from.** Columns: #, Country, Date, Year, Outcome, Deposed/Target, Notes.

---

## 4. NODE SPECIFICATIONS (reusable prompts & rules)

### NODE 0 — Row Selector
Pick one row from `african_coups_unsuccessful.xlsx`. Either **random** (when the user says
"generate a new one") or a **user-supplied row**. Carry forward: country, date, the deposed
leader (target), and the coup leader. This identifies the event for Node 1.

### NODE 1 — Deep-Research Dossier
Run **5 parallel research agents**, one per angle, then synthesize and cross-check.
The five standard angles (adapt wording to the coup):
1. **Key characters** — the coup leader, the target/ruler, other principals; concise
   "what made them who they are" portraits + their fate.
2. **Founding / colonial / political history** — how the country and regime got here, and
   why it set the stage.
3. **Resources & geopolitics** — the economic prize and outside patrons (oil, minerals,
   rubber, Cold-War aid, etc.) — "what was at stake / why the regime survived or was a target."
4. **The plot** — who organized/funded it, the plan, the mechanics.
5. **How it failed + aftermath** — the collapse, the blunders, the consequences.

**Standing instructions for each research agent:**
- Prioritize **reputable sources** (BBC, NYT/WashPost archives, Reuters/AP, Britannica,
  Library of Congress, HRW, Amnesty, truth-commission reports, academic work, the
  definitive book if one exists). Avoid unreliable blogs.
- Give a **source URL** for every significant claim. **Do not fabricate URLs.**
- Clearly separate **[FACT]** from **[ALLEGED]/[DISPUTED]**; flag where sources conflict
  (especially death tolls, force sizes, atrocity claims).

**Synthesis (the dossier) — fixed section order:**
1. How to use (source list + tag legend + tonal note) · 2. The story in 90 seconds ·
3. Character dossier · 4. Founding/colonial history · 5. Resources/stakes · 6. The plot ·
7. How it went wrong · 8. Aftermath · 9. Timeline (table) · 10. Documentary angles ·
11. Verify-before-broadcast flags · 12. Selected bibliography.

### NODE 2 — Narration / Voiceover + Timing
**Persona:** one creative intelligence wearing four hats — **showrunner/screenwriter,
documentary director, continuity/story editor, narration writer** — applying the best
principles of each.

**Structure (apply loosely, never force, never cringe):**
1. **COLD OPEN** on a single dramatic moment (or a tight run of related dramatic beats)
   that opens a question. Drop the viewer into heat, end on a hook.
2. **PULL BACK TO CONTEXT** — who/where/why, the history that loaded the gun.
3. **CONTINUE THE STORY FORWARD** through escalation → climax → consequence, with
   callbacks that pay off the cold open.

**Anti-cringe guardrails:** no trailer-voice clichés ("little did they know…"); drama
earned from real facts; use the "and/but/therefore" causal test; adapt the shape if the
story genuinely doesn't fit. **Match tone to the material** — e.g. the Wonga Coup is wry
dark comedy; Liberia 1985 is a straight tragedy. Don't force one register onto the other.

**Voice matching (Node 4 input):** when the creator's **writing samples** are supplied,
build a style bible (register, rhythm, humour *type* and *density*, tics, what they avoid)
and write in *their* voice, not generic doc-voice. Until then, use a sensible default and
label it as a placeholder.

**Accuracy:** dramatize event *order*, never invent events/quotes; respect the dossier tags
(attribute allegations: "prosecutors said…", "by his own account…").

**Output:** segmented script (COLD OPEN / ACT headers), spoken-word lines, light
`[VISUAL: …]` cues, a **runtime estimate at ~140 wpm**, and word counts.

### NODE 3 — Footage Shot-List (image + source per beat)
**Fan-out:** 3 footage-research agents by cluster — **People · The Event & Aftermath ·
Country/History/Context (+ generic stock B-roll)**. Each trawls the web for real
images/videos with **description + link + licensing**, returning a visual asset library
keyed by subject. (Agent finds *sources*; it does **not** download — see §9.)

**Footage priority order (strict):**
**(a) real related images/footage of the actual subject → (b) public-domain / Creative
Commons (Wikimedia, government) → (c) licensable news archive (Getty, AP Archive, Reuters,
AFP, British Pathé) → (d) generic stock (free Pexels/Pixabay first) as a last resort.**

**Compiler step:** segment the script into **~3–5-second beats** (≈8–12 spoken words each),
assign **running timecodes** (≈140 wpm), and under each beat place **one prescribed visual**:
- a one-line **description**, a **real link**, an **asset-type tag**
  (`REAL` / `CC` / `ARCHIVE` / `STOCK` / `DOC`), and a short **licensing note**.
- **Flag gaps** (subjects with no/rare imagery) and **graphic** material for editorial care.
- State plainly: links are a **vetted starting map for a picture researcher, NOT cleared
  rights**; most event footage must be licensed; links may rot; the agent can't watch clips.

### NODE 4 — Voice Re-tune (pending)
On receiving the creator's **writing samples**, rebuild the style bible and re-voice the
script (the shot list regenerates from the new wording automatically).

---

## 5. CROSS-CUTTING STANDARDS

- **Accuracy tags** `[FACT]/[ALLEGED]/[DISPUTED]` everywhere; allegations always attributed.
- **Output formats:** Markdown (source of truth) + **Word `.docx`** via `md_to_docx.py`
  (styled headings, tables, colour-coded tags). Shot lists are colour-coded by asset type.
- **Footage:** real → CC → archive → stock; sources only, no downloads; gaps & graphic flagged.
- **Version control:** every artifact is committed and pushed to the GitHub branch; the
  generator scripts make each deliverable reproducible.
- **Runtime math:** ~140 words/min; one visual per ~3–5s ⇒ ≈12–16 visual beats per minute.

---

## 6. DELIVERABLE SET & FILE NAMING (per coup)

For a coup with case slug `<case>` (e.g. `wonga_coup`, `liberia_1985`):
- `<case>_dossier.md` / `.docx`
- `<case>_script.md` / `.docx`
- `<case>_shotlist.md` / `.docx`
- a generator script where useful (e.g. `generate_shotlist_<case>.py`)

Shared tooling: `md_to_docx.py` (markdown→Word), `render_agent_diagram.py` (the pipeline
diagram), `agent/PIPELINE.md` and `agent/narration_node.md` (the living specs).

---

## 7. HOW TO RUN A NEW COUP (kick-off you can paste)

> "Generate the next coup. Pick a random row from `african_coups_unsuccessful.xlsx`
> (or use this row: COUNTRY / DATE / TARGET / LEADER). Run the full pipeline per the
> project context: (1) deep-research dossier via 5 parallel agents with `[FACT]/[ALLEGED]/
> [DISPUTED]` tags and a sourced bibliography; (2) a mid-length (~10–20 min) voiceover
> script using the cold-open → context → continuation structure, tone matched to the
> material; (3) a timed shot list with one sourced image/video under each ~3–5s beat,
> prioritizing real → CC → archive → stock. Deliver all three as Word docs, commit and push."

If writing samples are attached, add: "and re-voice the script to my style bible."

---

## 8. WHAT'S BEEN PRODUCED SO FAR

**A) Wonga Coup — Equatorial Guinea, 2004** (Simon Mann's failed mercenary plot vs. Obiang).
- Dossier, ~13-min script (wry dark-comedy register), **193-beat** timed shot list. Complete.

**B) Liberia 1985 — the Quiwonkpa coup** (Thomas Quiwonkpa vs. Samuel Doe).
- Dossier, ~10.5-min script (straight tragedy register), **146-beat** timed shot list. Complete.

Both followed the identical node sequence and standards, demonstrating the system is
coup-agnostic. (Note: for Liberia, the footage sub-agents hit a session limit, so the
asset library was assembled directly from reputable sources and the dossier's citations —
flagged for verification.)

---

## 9. CONSTRAINTS & KNOWN LIMITS (be honest about these)

- **No downloads / no live video pull.** The execution sandbox blocks most external network
  access, and almost all archive footage is copyrighted. The agent therefore **finds and
  links sources** (to license or to use where free); it does not fetch video. For the
  creator's own machine: `yt-dlp` downloads YouTube, but only use **own/CC/public-domain/
  licensed** material — YouTube's ToS and copyright otherwise apply.
- **No Google Sheets/Drive** connection — spreadsheets are delivered as `.xlsx` that import
  into Google Sheets (File → Import → Upload).
- **Links are a starting map, not cleared rights.** Verify each at source; many 1980s–2000s
  event clips are AFP/Reuters/AP/Getty and must be licensed; links can rot; the agent can't
  watch the footage. Some subjects are genuinely scarce (flag as gaps).
- **Voice is a placeholder** until the creator's writing samples are provided (Node 4).

---

## 10. REPO FILE INVENTORY (current)

- **Data:** `african_coups_1950_present.xlsx`, `african_coups_unsuccessful.xlsx`,
  `generate_african_coups.py`
- **Specs:** `agent/PIPELINE.md`, `agent/narration_node.md`
- **Wonga Coup:** `wonga_coup_dossier.*`, `wonga_coup_script.*`, `wonga_coup_shotlist.*`,
  `generate_shotlist.py`
- **Liberia 1985:** `liberia_1985_dossier.*`, `liberia_1985_script.*`,
  `liberia_1985_shotlist.*`, `generate_shotlist_liberia.py`
- **Tooling/diagram:** `md_to_docx.py`, `render_agent_diagram.py`, `agent_architecture.png/.svg`
- **This file:** `PROJECT_CONTEXT.md`

---

## 11. OPEN ITEMS / NEXT STEPS

- **Supply writing samples** → triggers Node 4 (re-voice both existing scripts + all future ones).
- Optionally re-run the Liberia footage agents to upgrade its asset library with verified links.
- Optional add-ons: clickable hyperlinks in the Word docs, PDF exports, an episode/shot-list
  outline, or a Node 5 "production package" (per-coup folder bundling all deliverables).

*Tags legend — [FACT]: established · [ALLEGED]: claimed/denied · [DISPUTED]: sources conflict.*

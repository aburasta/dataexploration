# THE AGENT — PIPELINE MAP

Turns a single **unsuccessful-coup row** into a documentary-ready package.
The dataset-generation nodes are **retired** (the spreadsheets already exist);
the agent now begins by selecting a row to develop.

| # | Node | Input | Output | Status |
|---|------|-------|--------|--------|
| 0 | **Row Selector** | `african_coups_unsuccessful.xlsx` | One chosen coup — **random** on "generate a new one," or a **user-supplied row** | 🟢 active |
| 1 | **Deep Research Dossier** | The chosen coup | Cross-checked, source-tagged research dossier | 🟢 built |
| 2 | **Narration / Voiceover** | Node 1 dossier | Documentary VO script (story format) **+ timed shot list** | 🟢 built |
| 3 | **Footage Sourcing** | Node 2 script | Per-beat image/video suggestions + links + licensing, compiled into the Word doc | 🟢 built |
| 4 | **Voice Re-tune** | A script + user writing samples | Script re-voiced to the user's style bible | 🟡 pending samples |

**Retired (data already generated):**
- ~~Coup Dataset~~ → `african_coups_1950_present.xlsx`
- ~~Extract Unsuccessful~~ → `african_coups_unsuccessful.xlsx`

Design rule across the pipeline: **accuracy tags propagate.** The `[FACT]` /
`[ALLEGED]` / `[DISPUTED]` distinctions from Node 1 must survive into Nodes 2–3 —
narration may never state an allegation as established fact.

**Per-run outputs** are named by case, e.g. `wonga_coup_*` (first run) and
`quiwonkpa_coup_*` / `liberia_1985_*` (this run).

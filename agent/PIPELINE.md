# THE AGENT — PIPELINE MAP

This documents the agent's processing nodes for turning raw coup data into
documentary-ready narration. Each node consumes the output of the previous one.

| # | Node | Input | Output | Status |
|---|------|-------|--------|--------|
| 1 | **Coup Dataset** | "African coups 1950–present" | Spreadsheet split into Successful / Unsuccessful | ✅ built (`african_coups_1950_present.xlsx`) |
| 2 | **Extract Unsuccessful** | Node 1 | Standalone unsuccessful-coups spreadsheet | ✅ built (`african_coups_unsuccessful.xlsx`) |
| 3 | **Deep Research Dossier** | A chosen coup | Cross-checked, source-tagged research dossier | ✅ built (`wonga_coup_dossier.*`) |
| 4 | **Narration / Voiceover** | A dossier (Node 3) | Documentary VO script in story format | 🟡 spec ready — needs writing samples (`narration_node.md`) |
| 5 | **Footage Sourcing** *(proposed)* | A dossier / script | Footage links + licensing map | ⬜ proposed |

Design rule across the pipeline: **accuracy tags propagate.** The `[FACT]` /
`[ALLEGED]` / `[DISPUTED]` distinctions from Node 3 must survive into Node 4 —
narration may never state an allegation as established fact.

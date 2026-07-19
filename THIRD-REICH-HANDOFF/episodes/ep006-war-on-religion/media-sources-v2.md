# ep006 — Media Sources v2 (fresh re-source + video expansion, 2026-07-18)

Re-sources ep006's media from scratch (the handoff shipped without the files). **v1 = the existing
`media-plan.md`**, which already identifies a specific source for all 59 tags after a round-2 quality
pass — this sheet is the consolidated, actionable **download manifest** (tag → source → rights →
credit → status) plus the **video expansion** the user asked for. Scene→file mapping is per
`spec-rendered.json` (76 scenes, files `1.jpg`–`59.jpg` + callback splits `60–64` + `11.mp4` +
`51.mp4`).

**Status:** `✓id` = specific source identified (Bundesarchiv Bild # or named Commons file) ·
`◇check` = subject known, exact file/clip to confirm at download · `reuse` = same-person/place, no
distinct image exists (kept ≤ plan's ~12%).
**Rights:** `PD-US` · `NARA` · `BArch` (CC-BY-SA — **must credit**) · `EDIT` (editorial/fair-use) ·
`CC-photo` (modern CC photo of a place — credit photographer).

House rules: real archival only, no AI · **camps = sober gate/exterior stills only, never graphic** ·
never fabricate a portrait (cover with context) · insignia incidental, never hero of frame.

---

## A. Video — expansion (2 → ~8–10)

Genre reality (per v1): church-official subject matter has little newsreel, so video maximizes at the
**footage-rich beats only** — rallies, book-burning, SA, radio, Potsdam, Anschluss. Prefer **NARA /
US-gov PD**; `catalog.archives.gov` holds ~1,293 seized German newsreel reels (unambiguously PD).
`*` = PD in US; add BArch credit where the underlying shot is German-archive origin.

| Tag(s) | Clip | Content | Source | Rights | Status |
|---|---|---|---|---|---|
| 51 | `51.mp4` **KEEP original** | May 10 1933 Berlin book-burning (the exact clip from the finished render — user confirmed it was well done) | [Sandler Film Library — same archive.org item as v1](https://archive.org/details/IA_35000454_1); re-fetch identical footage, keep spec trim `startTrim 0.3` / `playbackRate 2.0062` | see note | keep |
| 11 | `11.mp4` **re-source** | Reichsparteitag parade / mass salute | [Sandler — Nazi rallies](https://archive.org/details/IA_35000454_1) · [Universal Newsreels](https://archive.org/details/universal_newsreels) | PD-US* | ✓id |
| 21 | `vid-sa` **NEW** | SA marching / SA as auxiliary police 1933 | *The Nazi Plan* / NARA seized newsreel ([catalog.archives.gov](https://catalog.archives.gov/id/100520)) | PD-US* | ◇check |
| 22 | `vid-radio` **NEW** | Hitler at the radio microphone, 1933 | Universal Newsreels / NARA | PD-US* | ◇check |
| 17 | `vid-potsdam` **NEW** | Tag von Potsdam 1933 / Hitler sworn in, torchlight | [Universal Newsreels](https://archive.org/details/universal_newsreels) → "Potsdam 1933" | PD-US* | ◇check |
| 1/20 | `vid-dc-rally` **NEW** *(if exists)* | Deutsche Christen / church-politics rally 1933 | *The Nazi Plan* church segment | PD-US* | ◇check |
| 58 | `vid-anschluss` **NEW** | Anschluss, Heldenplatz Vienna 1938 | [Universal Newsreels](https://archive.org/details/universal_newsreels) | PD-US* | ◇check |
| 59 | `vid-retreat` **NEW** | German army retreat, WWII (non-graphic) | [United News 1945](https://archive.org/details/ARC-39067) / NARA | NARA/PD | ✓id |
| 5/11 | `vid-sportpalast` **NEW** *(if exists)* | Sportpalast / big-hall rally interior | Sandler / Universal | PD-US* | ◇check |

**Camps (35/41/42) stay stills on purpose.** Liberation footage is PD (NARA Signal Corps; [LOC
confirms free reuse](https://www.loc.gov/item/2019606950/)) but graphic — **not used**, per the
sensitivity rule. Sober gate/exterior stills only.

**Rights caution (from v1):** "on archive.org ≠ free." A *Triumph of the Will* excerpt was CC-BY-NC-ND
and rejected for a monetized upload — keep that discipline; confirm each clip's license before publish.
The kept `51.mp4` came from the Sandler collection with an unstated license in v1 — it stays in the
cut as the user requested; still worth confirming its license before publish if monetization matters.

---

## B. Stills — re-source manifest (all ~64, sources from v1 round-2 final state)

| Tag | Subject | Source (identified in v1) | Rights | Status |
|---|---|---|---|---|
| 1 | Deutsche Christen "Kirchenwahl" propaganda, Berlin | Bundesarchiv | BArch | ✓id |
| 2 | Krause's printed Sportpalast speech — title page (no portrait exists) | Commons "Rede von Krause" | PD/EDIT | ✓id |
| 3 | Torah scroll | Bodleian MS heb. a. 4 | PD | ✓id |
| 4 | Berlin Luthertag (Deutsche Christen) 1933 | Bundesarchiv | BArch | ✓id |
| 5 | Deutsche Christen / Bekennende Kirche emblem | Commons | EDIT | ◇check |
| 6 | Ludwig Müller, Reich Bishop | **BArch Bild 183-H30223** | BArch | ✓id |
| 7 | Völkischer Beobachter front page, 31 Jan 1933 | Commons | PD-US | ◇check |
| 8 | Germans reading newspaper on the street | period photo | PD | ◇check |
| 9 | Hitler cabinet group, Jan 1933 | Bundesarchiv | BArch | ✓id |
| 10 | Alfred Rosenberg portrait | Bundesarchiv | BArch | ✓id |
| 11 | Reichsparteitag Nürnberg 1933 parade | Commons (PD) | PD-US | ✓id |
| 12 | Adolf Hitler portrait | Bundesarchiv | BArch | ✓id |
| 13 | NSDAP 25-point program, page 1 (1920) | Commons | PD-US | ✓id |
| 14 | NSDAP 25-point program, page 2 | Commons | PD-US | ✓id |
| 15 | Ludwigskirche baroque church exterior | Commons | CC-photo | ◇check |
| 16 | Hofbräuhaus München exterior | Commons | CC-photo | ◇check |
| 17 | Tag von Potsdam, Hitler & Hindenburg | **BArch 183-S38324** | BArch | ✓id |
| 18 | Wittenberg Schlosskirche interior (panoramic) | Commons | CC-photo | ✓id |
| 19 | Neue Reichskanzlei exterior | Bundesarchiv | BArch | ✓id |
| 20 | Hitler + church leader at Nuremberg, 1934 | Bundesarchiv | BArch | ✓id |
| 21 | SA als Hilfspolizei, Berlin 1933 | Bundesarchiv | BArch | ✓id |
| 22 | Hitler at radio microphone, Feb 1933 | Bundesarchiv | BArch | ✓id |
| 23 | Wittenberg Thesentür (Luther door) | Commons | CC-photo | ✓id |
| 24 | Hitler at the Berghof, 1936 | Bundesarchiv | BArch | ✓id |
| 25 | Hitler 1936 portrait | Bundesarchiv | BArch | ✓id |
| 26 | "Hitler's officers" group (incl. Kerrl, Himmler) | Commons | ◇ | ◇check |
| 27 | Hitler seated at a table (period) | Commons | ◇ | ◇check |
| 28 | Catholic clergy + Nazi officials, salute together | Bundesarchiv | BArch | ✓id |
| 29 | Niemöller, signed 1917 U-boat portrait | Commons "Martin Niemöller Marineoffizier" | PD-US | ✓id |
| 30 | Niemöller "From U-Boat to Pulpit" title page 1936 | Internet Archive cover service | PD/EDIT | ✓id |
| 31 | Niemöller (kept-preaching beat) | reuse of 29 | PD-US | reuse |
| 32 | Deutsche Christen / Bekennende Kirche emblem | Commons | EDIT | ◇check |
| 33 | Confessing Church membership document | Commons | ◇ | ◇check |
| 34 | SA / security-force photo | reuse of 21 (BArch) | BArch | reuse |
| 35 | Sachsenhausen camp gate (respectful exterior) | Commons | CC-photo | ✓id |
| 36 | German church congregation/interior | reuse of 18 (Wittenberg) | CC-photo | reuse |
| 37 | Illuminated medieval Bible manuscript page | Commons | PD | ◇check |
| 38 | Arrest/security beat | reuse of 21/34 | BArch | reuse |
| 39 | Volksgerichtshof (People's Court) session | Bundesarchiv | BArch | ✓id |
| 40 | Gestapo outside courthouse | reuse of 39 | BArch | reuse |
| 41 | Sachsenhausen (2nd mention) | reuse of 35 | CC-photo | reuse |
| 42 | Dachau camp gate (respectful exterior) | Commons | CC-photo | ✓id |
| 43 | Hans Kerrl portrait, 1938 | Commons (PD) | PD | ✓id |
| 44 | "room of churchmen" | reuse of 28 (clergy+salute) | BArch | reuse |
| 45 | German crucifixion sculpture group (Dülmen) | Commons | CC-photo | ✓id |
| 46 | Kabinett von Papen cabinet photo | Bundesarchiv | BArch | ✓id |
| 47 | Martin Bormann portrait | **BArch Bild 183-R14128A** | BArch | ✓id |
| 48 | Bormann's signed circular, 3 Jan 1941 (Schrifterlass) | Commons | PD-US | ✓id |
| 49 | Rosenberg, *Der Mythus des 20. Jahrhunderts* (cover) | Commons | PD/EDIT | ✓id |
| 50 | Church altar, bare (Crostwight, Norfolk) | Commons | CC-photo | ◇check |
| 51 | *(now clip `51.mp4` — book-burning)*; still fallback = Bible manuscript (37) | — | — | ✓id |
| 52 | Münster St.-Paulus-Dom altar (real German cathedral) | Commons | CC-photo | ✓id |
| 53 | Mein Kampf dust jacket | Commons (PD) | PD-US | ✓id |
| 54 | swastika-vs-cross (symbolic; plan never enacted) | reuse of 20 (Hitler+church leader) | BArch | reuse |
| 55 | Berlin street scene, 1933 | Bundesarchiv | BArch | ✓id |
| 56 | Berlin furniture-exhibition living room, 1930s | Bundesarchiv | BArch | ✓id |
| 57 | Reichsautobahn construction site | Bundesarchiv/Commons | BArch | ✓id |
| 58 | Anschluss, Heldenplatz speech, Vienna 1938 | Bundesarchiv/Commons | BArch | ✓id |
| 59 | Eastern Front, troops retreating | Bundesarchiv | BArch | ✓id |
| 60–64 | callback splits (German Christians faction / Old Testament / stripped NT / disown / Article 24 text) | variants of tags 1, 3, 4, 6, 13/14 | mixed | ◇check |

---

## C. Fix list (weak matches flagged in v1 — attempt one distinct pass, keep only if nothing better)
- **45** crucifix → already German (Dülmen) ✓ · **57** → real construction site ✓ (both round-2 fixes).
- **26/27** ("Hitler's officers" / "seated at table") — loosely sourced; try for a dated, on-topic
  Bundesarchiv alternative.
- **7 legitimate reuses** (31, 34, 38, 40, 41, 44, 54) — same-person/place, no distinct image; keep.
- **50/52** altars are English/German generic — fine as Christian iconography, not event-accurate.

## D. No-fabrication cases (kept honest)
- **Krause (2)** — no portrait exists → his speech's printed title page.
- **Rosenberg's 30-point draft (49)** — no scan exists → his actual book *Der Mythus* instead.
- **swastika-replacing-cross (54)** — never enacted → symbolic pairing (Hitler + church leader), captioned as such.

## E. Required BArch credits (CC-BY-SA)
Collect "Bundesarchiv, Bild …" credits for every BArch asset (most of the set). Confirmed Bild #s so
far: `183-H30223` (Müller), `183-S38324` (Potsdam), `183-R14128A` (Bormann) — plus all rows marked
`BArch` above, whose exact Bild #s get recorded at download.

## F. Prep / verification
- Stills cap 1920px; clips crop to clean 1920×1080 + `playbackRate` via bundled `ffmpeg` directly
  (never `npx remotion ffmpeg`). Land in `reich-engine/public/media/war-on-religion/`.
- Verify each clip: one frame → clean 16:9, correct subject, **no atrocity/graphic content**.
- Cross-check against `spec-rendered.json` so all 76 scene slots resolve; keep reuse ≤ ~12%.

## G. Open items before download
- `◇check` rows: confirm exact file/clip + individual rights (esp. modern `CC-photo` place shots →
  record photographer for attribution).
- New clips (`vid-sa/radio/potsdam/dc-rally/anschluss/sportpalast`): pull the specific sub-clip;
  confirm PD/BArch and no graphic content.
- Callback splits **60–64**: confirm which exact variant image each uses.

# HANDOFF — "Hitler / Eva Braun love-life" documentary visual remake

## Goal
Rebuild the **visuals** of an existing 9:32 YouTube video (poor retention) while keeping the
**original voiceover** untouched. Output 1920×1080/30fps, public-domain archival footage cut
to the narration. Remotion project at `remotion-africa/`.

## Branch / repo
`aburasta/dataexploration`, branch `claude/remotion-map-motion-graphic-r61a2a`.
Original uploaded video: `/root/.claude/uploads/51536a94-*/548aa492-The_Woman_Who_Travelled_to_Berlin_To_Die_With_Hitler_*.mp4`.

## Hard requirements (latest)
1. **Every beat = a unique cut; NO repeated frames.** Different non-overlapping cuts of the
   same source film are OK; the same segment twice is not.
2. **Tightest context fit** to what's said at each timecode.
3. **Stills ONLY to introduce a named person**, appearing exactly when the name is spoken and
   dropping as soon as the intro ends (never parked early).
4. **No graphic content** (no corpses/atrocity) — frame-check every clip.
5. **Monetizable licenses only** (Public Domain / CC0). Reject CC BY-NC-ND, modern
   documentaries, YouTube re-uploads, watermarked archive footage (Pathé/Chronos). Log all in
   `public/broll/CREDITS.md`.
6. Professional **cross-dissolves** (no cut-to-black), Ken-Burns push, vignette, name-cards.

## Environment gotchas
- Use Remotion's bundled ffmpeg: `node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg`.
  MINIMAL build — NO `gblur`/`eq`/`unsharp`/`hstack`/`fps` filters or `mpeg4`. Use `libx264`,
  `scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080`, `-r 30` (not fps
  filter), `overlay=x=..:y=..` (named).
- HuggingFace/Whisper egress BLOCKED. Transcription via **pocketsphinx** →
  `scratchpad/words_full.json` (rough; garbled in the Eva-era stretch). `pip install pocketsphinx pillow`.
- **Wikimedia blocks large downloads** (2256-byte error pages). **Archive.org reliable**
  (`curl -sSL`, `_512kb.mp4` derivatives seek fine).
- 30 MB chat-file limit → deliver in ~2.4-min parts; full 9:32 master too big to send.
- Render ≈ 8–9 min per 2.4-min part. Run in background (`nohup` chain writing a
  `/tmp/*.done` marker + a blocking `until [ -f marker ]` waiter). A `nohup ... &` wrapper's
  "completed" is NOT the render finishing — poll the marker.

## Built (committed)
- `src/Root.tsx` registers `ReelOpen` (approved 60s) and `ReelFull` (full, 17160 frames).
- `src/ReelFull.tsx` — reads `src/beatsFull.json`; `@remotion/transitions` `TransitionSeries`
  + `fade()` (XF=11; each sequence padded by XF so cuts land on beat times, VO stays synced);
  `Clip` = OffthreadVideo for `.mp4` / `Img` for `.jpg`, Ken-Burns 1.06→1.14, vignette;
  `NameCard`; single `<Audio staticFile('vo/voiceover.wav')>`.
- `src/ReelOpen.tsx` — the approved Part 1 beat list (source of truth for 0–143s).
- `public/vo/voiceover.wav` (gitignored, large), `public/broll/*` clips + `CREDITS.md`.
- `.gitignore` excludes `public/vo/*.wav`, `out/*.mp4`.

## Delivery state
- **Part 1 (0:00–2:23) APPROVED** (`--frames=0-4289`) — 27 distinct clips, no repeats.
- Parts 2–4 first version rejected (repetition/static). **Reworking now** to unique-frames +
  precisely-timed stills.

## Person-still windows (place still here, drop after)
Geli tease **35.5–40.5s** · Geli intro **214–226s** · Stempfle **312.5–321s** ·
Geli death **367–378s** · Hindenburg **406–414s** · Hoffmann **427–432s** · Eva **432–440s**.

## Narrative timeline (approx.)
0–11 bunker/1945 secret marriage · 11–42 Eva tease → Geli ("love died 1930") · 42–60 thesis
"occult practices of the Nazis" → love · 60–92 young Hitler/Vienna · 92–138 WWI · 138–160
early flings · 160–206 Obersalzberg 1928 · 206–248 Geli (the "one true love") · 248–293
control/gossip · 293–333 letter → Stempfle → Night of Long Knives · 333–360 leaves for
Hamburg · 360–393 Geli's death (non-graphic) · 393–424 grief/Hindenburg · 424–442 Eva at
Hoffmann's studio · 442–545 Eva era/Berghof/WWII · 545–572 outro.

## Source films (in `scratchpad/broll_src/`, NOT committed — re-download in a new container)
- `BERLINSINFONIEEINERGROSSSTADT_201806` — Berlin: Symphony of a Great City (1927), PD →
  1920s city/society.
- `111-m-59-r3` — Battle of the Somme (NARA, PD) → WWI. CASUALTIES at ~30s & ~560s — AVOID;
  clean at 70/108/158/208/258/318/378/428.
- `neva-braun-home-movies-part-3-1` — Eva Braun Home Movies Part 3 (PD/NARA, ~10min) — BEST
  Berghof/Eva variety (alps, dogs, guests, skating, Hitler, children, lake).
- `color-material-from-hans-baur-hitler-mussolini-vinnytsia_202405` — Hans Baur color (CC0).
- `1944-03-20_Blast_Berlin_By_Daylight` (PD) → night air-raid/bombers/flak (body-free).
- Universal Newsreels (PD): `1933-03-16_Hitlerites_Parade_In_Rain` (parade/standards/crowd),
  `1941-12-24_Big_News_of_1941` (tank/factory), `1945-05-08_Germany_Gives_Up` (surrender).
- REJECTED: `1945-03-29_Reds_Roll_On_In_Germany` (corpses); a CC BY-NC-ND "Hitler addresses
  SA/SS 1934" clip; British Pathé & Chronos (watermarks).
- `hitler_eva_home.webm` (0–200s partial) — Part 1's Eva cuts.

## Clip pool committed in `public/broll/` (~47 video + 7 stills + 29 new bh_*)
Part 1: `airraid_bombers/flak/smoke`, `eva_berghof/close/group/terrace/mountains`,
`hitler_child`, `parade_troops/standards/crowd`,
`city_countryside/train/aerial/street_dawn/facade/residential/shops/greengrocer/tram/workers/industry/park/labor/market/men_talk/crowd_walk/cars/traffic/bridge/crowd_b`,
`wwi_soldiers/column/transport/countryside/trench/village/muddy/ruins`,
`war_factory/tank/ruins/surrender`, `eva_men/walk/scene`.
Stills: `geli_raubal`, `still_stempfle/_hindenburg/_hoffmann/_eva_portrait/_hitler_young/_hitler_wwi`.
**NEW (this session): `bh_01..bh_29`** = distinct Berghof/Eva cuts from Eva Home Movies Part 3
(6s each at 18,40,58,80,100,120,140,160,180,200,218,240,258,280,300,320,340,360,380,400,418,
440,458,480,500,520,540,560,580). Use these for the Eva/Berghof sections (2–4).
CAUTION: some old `hitler_eva_home` cuts overlap (`eva_men`88–94 vs `eva_terrace`84–94;
`eva_scene`128–134 vs `eva_group`125–134) — don't use overlapping pairs together.

## REMAINING WORK (approved "rework v2")
1. Finish the unique library: still to cut — `bc_01..04` (Baur color, ss 60/220/430/640);
   **~18 new Berlin-1927 cuts** at NEW timestamps disjoint from existing `city_*`
   (e.g. 742,860,952,1002,1102,1252,1302,1452,1502,1652,1702,1902,2102,2302,2602,2902,3002,3102);
   **~5 WWII** (Big News 1941 @90/150/330, Germany Gives Up @15/90 — frame-check bodies);
   **~3 airraid** (Blast Berlin @12/30/52); **~2 parade** (Hitlerites @2/20). Frame-check
   war/WWI for casualties.
2. Write `gen_beats3.py`: assign a UNIQUE cut file per beat (assert none used twice across all
   106); keep Part 1 explicit (mirror `ReelOpen` beats); insert person STILLS as their own
   short beats at the exact windows above (5–8s + name card); map each section to its context
   pool (Eva/Berghof→`bh_*`/`bc_*`; society/politics→`city_*`; WWI→`wwi_*` Part 1 only;
   ceremony/purge→`parade_*`; war→`war_*`/`airraid_*`). Regenerate `src/beatsFull.json`.
3. Render sections 2–4 (background): `npx remotion render ReelFull out/rework_p2.mp4
   --frames=4290-8579 --crf=20`; then 8580-12869→p3, 12870-17159→p4. Part1 = rework_p1
   (`--frames=0-4289`).
4. Frame-scan each part (contact sheets) — no bodies; correct topic; stills within windows.
5. Concatenate all 4 (ffmpeg concat demuxer) into full master; compress each part <30MB
   (`libx264 -b:v 1.5M -maxrate 1.7M -c:a aac 128k -movflags +faststart`); deliver parts 2–4
   previews; keep full master in `out/` (gitignored).
6. Commit clips + `beatsFull.json` + `CREDITS.md`; push.

## Verification
`beatsFull.json`: each cut file used ≤1×; stills only in name windows, ≤8s. No casualty/
watermark/title-card frames. Audio = unmodified VO; total 9:32; 1080p/30fps.

## Scratchpad scripts (ephemeral, /tmp): `contact.py` (Pillow contact sheets, .mp4 only),
`cutlib.py` (batch cutter), `gen_beats2.py` (superseded), `psx_timing.py`, `words_full.json`.

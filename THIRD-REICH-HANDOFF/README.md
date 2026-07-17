# Third Reich Documentary Series — Handoff Package

This folder is everything needed to **keep producing** this YouTube documentary series on a
new device. It deliberately contains **no finished videos and no sourced episode media/audio**
(images, video clips, narration recordings) — those stay behind on the old machine. This is the
reusable tooling, process knowledge, and reference material: give it to Claude on the new device
and it can pick this series up cold.

## What this series is

A YouTube documentary channel covering the Third Reich, built almost entirely from **William L.
Shirer's "The Rise and Fall of the Third Reich"** as the primary source (the full book text is
included at `reference/source-text-full-book.txt`, 56,000+ lines). Episodes are either single-
chapter EVENT angles or cross-book FACET/ARC/RELATIONSHIP/INSTITUTION angles pulled from a
backlog (`reference/character-angle-pool.md`). Videos are strictly non-political/educational in
framing — every script and every YouTube description carries an explicit disclaimer to that
effect; this is a hard house rule, not boilerplate.

## Folder structure

```
THIRD-REICH-HANDOFF/
├── README.md                    <- this file
├── memory/                      <- the standing process/pipeline knowledge (READ THIS FIRST)
├── reich-engine/                <- the Remotion rendering engine (code only)
├── reference/                   <- source book text, topic backlog, research reports
├── metadata/                    <- packaged YouTube titles/descriptions/tags/chapters, per episode
└── episodes/                    <- past episode scripts + media/render plans (text only)
```

## Start here: `memory/feedback_bracket_tag_media_assembly.md`

This is the single most important file in this package — it's the accumulated, tested,
standing pipeline for turning a finalized script into a rendered video, written from real
production experience (not theory). It covers, in order:

1. The end-to-end workflow: script → bracket-tag → media-plan → source media → user sign-off →
   TTS narration → assemble/render in `reich-engine`.
2. How to bracket-tag a script yourself (the `(N)…(N)` / `(TAG)…(TAG)` span system).
3. Where to source real archival media (Wikimedia Commons, Internet Archive, rights caveats —
   what's actually public-domain vs. what looks it) and how to avoid rate-limiting/wrong-image
   mistakes that have happened before.
4. Sound design conventions (see also `reference/sound-design-guide.md`).
5. Visual style rules: no on-screen text except the end card and quote/diary-entry typewriter
   overlays; letterboxing for off-ratio images; cap image dimensions at 1920px (oversized images
   have crashed the render before); vary transitions purposefully (`cut` vs `xfade` vs
   `dip-to-black`).
6. **Render environment gotchas** — this pipeline was mostly built/tested on a very RAM-
   constrained machine (~4GB total). Read this section closely if the new device has similarly
   tight RAM: `--concurrency=1` is required, `chrome-headless-shell`/`node` processes leak memory
   over a long render, `TaskStop` doesn't cascade-kill child processes on Windows (always
   explicitly `Stop-Process` them before retrying), and frame-range batching (render in chunks,
   concatenate with the bundled ffmpeg) is a valid fallback if full-length renders keep failing —
   though the user's stated preference is a single full render by default. **If the new device has
   normal amounts of RAM, most of this section won't apply — but read it anyway, since the
   underlying render mechanics (playbackRate, aspectRatio letterboxing, transition rules) aren't
   RAM-specific.**

The other two files in `memory/` are packaging research, both worth reading before writing any
YouTube title/description/tags:
- `research_third_reich_packaging_playbook.md` — real competitive analysis of top WW2/Third
  Reich YouTube channels: what titles, descriptions, and thumbnails actually work in this niche.
- `master_plan_youtube_algorithm_optimization.md` — cross-series (not Third-Reich-specific)
  guidance on hooks, retention, and metadata optimization.

## `reich-engine/` — the rendering tool

A Remotion (React-based video rendering) project. **Before doing anything else on the new
device:**
```
cd reich-engine
npm install
```
This pulls in `node_modules` (deliberately excluded from this package — it's large and fully
reinstallable) including the bundled ffmpeg binary the pipeline depends on directly:
`node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe`. **Always call that binary
directly for any ffmpeg work** — `npx remotion ffmpeg` has a broken argument passthrough that
silently mis-parses some flags (this is called out explicitly in the memory file too).

Key source files:
- `src/Documentary.jsx` — the main composition. Scene timeline + audio timeline (per-scene
  `audio` field owns that clip for its own duration plus any following audio-less scenes; a
  `spec.narration` global track is also supported for episodes recorded as one continuous take
  rather than per-scene clips — see `episodes/ep003-hitler-love-life/render-spec-v3-notes.md`
  for why/when that was used).
- `src/KenBurnsImage.jsx`, `src/ClipScene.jsx` — still-image and video-clip scene renderers.
- `src/Transitions.jsx` — xfade / dip-to-black / cut.
- `src/config.js` — motion presets, transition timings, and `DEFAULT_SPEC` (reads
  `src/active-episode.json` via a static import — **this file is a hard build dependency, the
  project won't bundle without it.** The copy included here is a bare placeholder (one outro
  scene, no real content), not a real episode — the render pipeline overwrites it per episode.
  Build a fresh one for whatever episode comes next, following the conventions in the memory file
  and the past episodes' `spec-rendered.json`/`spec-in-progress.json` files under `episodes/` as
  worked examples of the real JSON shape.
- `src/Hemicycle.jsx` — a reusable data-viz scene type (parliament dot-chart), opt-in per episode.
- `src/LikeSubscribeCard.jsx` — the standard end card, reused on every episode.
- `render-batches.sh` — the frame-range batching driver script (fallback for render instability;
  see the memory file for when to actually use this vs. a single full render).

Render command (once a spec is built into `src/active-episode.json`):
```
npx remotion render src/index.jsx Documentary "<output-path>.mp4" --concurrency=1
```

## `reference/` — material for writing new episodes

- `source-text-full-book.txt` — the full Shirer book text. Grep this for names/dates/quotes when
  researching a new episode; pull real surrounding passages, not just keyword hits.
- `character-angle-pool.md` — the backlog of episode angles (topic, type, status). Check this
  first when picking what to make next.
- `chapter-by-chapter-hidden-gems-report.md` and `full-chapter-synthesis-exhaustive.md` — research
  reports mapping the book's chapters to potential episode material.
- `episode-queue.md` — an older, now-retired topic-selection file. Superseded by
  `character-angle-pool.md` as of 2026-07-08 — kept for historical reference only, don't use it
  for topic selection.
- `sound-design-guide.md` — maps script-moment types (cold opens, quote reveals, revelations,
  montages, epilogues) to sound treatments.
- `scripts/nazis-war-on-religion-old-testament.md` — an example of a standalone user-written
  script (as opposed to one generated via the angle-pool → rough → final flow).
- `archive-index/channel-index.json` — index of previously-analyzed reference channels/sources.

## `metadata/` — finished YouTube packages

One file per already-packaged episode (title options, full description, tags, hashtags,
chapters, target-audience profile). Useful as format examples for packaging future episodes, and
directly usable if the corresponding video/thumbnail assets are brought over separately.

## `episodes/` — past episode scripts and plans (text only)

Each subfolder is one episode's script + media/render planning docs, **with all audio, thumbnail
images, and render logs stripped out** (those are the "video" assets this package intentionally
excludes). What's kept:
- `script-rough.md` / `script-final.md` (or equivalent) — the actual narration text. Read a couple
  of these to internalize the house voice/structure before writing a new one.
- `media-plan.md` (and versioned variants) — how each script span was mapped to a real sourced
  image/clip. Useful as a worked example of the bracket-tag → media-plan process.
- `spec-rendered.json` / `spec-in-progress.json` — the actual Remotion scene spec used to render
  (or, for `special-legal-coup-1919-1933`, still being built for) that episode. Good concrete
  examples of the JSON shape `src/active-episode.json` needs to take.
- `creative-vision.md` (where present) — a paragraph-by-paragraph creative-treatment planning doc,
  per the pre-tagging planning convention described in the memory file.

**Status as of this handoff (2026-07-17):**
- `ep003-hitler-love-life` — fully scripted, sourced, rendered, and packaged (finished video not
  included here).
- `ep006-war-on-religion` — same, fully finished and packaged.
- `special-legal-coup-1919-1933` — script finalized, media plan built, spec in progress
  (`spec-in-progress.json`); this one was mid-production when this handoff was made — probably
  the best candidate to resume first.
- `special-hitler-mussolini-1922-1945`, `special-hitler-name-schicklgruber`,
  `special-reichstag-fire-1933` — rough scripts only, not yet developed further.

## What's deliberately NOT in this package

- Any rendered `.mp4` — the finished videos aren't needed to make new ones.
- Sourced episode images/video clips (`Third Reich/Media/`, `reich-engine/public/media/`) — large,
  per-episode, and not reusable across new episodes.
- Narration/music audio files (`reich-engine/public/audio/`, episode `audio/` subfolders) —
  same reasoning.
- `reich-engine/node_modules` and `reich-engine/out/` — reinstallable/regenerable, not source.
- `src/active-episode.json` — transient working state, not a stable asset.

If you need any of the above later, they remain on the original device until explicitly deleted.

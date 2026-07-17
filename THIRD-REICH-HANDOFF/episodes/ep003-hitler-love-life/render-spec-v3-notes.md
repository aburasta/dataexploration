# ep003 — Render spec v3 (2026-07-15)

Continues from `media-plan-v2.md`. Picking up where the prior session left off: media was
already fully sourced (all 41 numbered images + `new-*`/`keep-a*` replacements + 4 cropped
`-clean.mp4` clips, confirmed present in `reich-engine/public/media/love-life/`), and a fresh
**single continuous narration take** (`narration-full.mp3`, 9:35.63, re-recorded from
`script-final-no-brackets.md`) had just been generated minutes before this session started —
found in both the episode folder and `reich-engine/public/audio/love-life/`.

## Deviation from the v2 plan's "Stage B" (flagging honestly)

`media-plan-v2.md`'s stated next step was: generate **18 discrete per-paragraph clips**
(P01–P18) via Epidemic Sound, matching this project's standing per-span-audio convention (see
the `feedback_bracket_tag_media_assembly` memory — one audio file per narration span, zero
forced-alignment guessing). That didn't happen — instead a single continuous take exists.

Rather than discard the completed narration and re-record 18 separate clips (extra time/cost,
and no confirmation the same voice/take would reproduce), `Documentary.jsx` was extended with a
new optional `spec.narration` field: a full-length `<Audio>` track played once from t=0,
alongside the existing looped `spec.music` bed. This sidesteps the per-scene `audio`-ownership
mechanism entirely — no scene in this episode's spec sets `audio`.

**Consequence:** scene cut points are *not* measured from real per-clip durations (the method
the standing rule exists to guarantee). They're estimated from each paragraph's share of total
word count (1,751 words / 575.63s = ~0.329s/word), which assumes roughly steady narration pace.
Actual silence-gap detection (`ffmpeg silencedetect`) was tried first but rejected — at
reasonable thresholds it flagged 100+ sentence-level pauses, not just the 17 paragraph
boundaries, so it couldn't reliably distinguish "end of paragraph" from "end of sentence."
Word-count proportional timing is a coarser but safer estimate. **Visual cuts may drift by a
second or two from the actual narration content especially in longer paragraphs — this is the
one real risk in this build and worth a spot-check against the rendered video**, particularly
paragraph 2 (longest at 173 words / ~57s, holds two long single-image beats around the occult
flash-montage) and the two Ken-Burns-only paragraphs with 3-way splits (P08, P11).

## Beat map used (durations = word-count-proportional split of each paragraph's estimated span)

Same image/clip assignments as `media-plan-v2.md`'s Scene map (P01–P18), just re-timed:
- P01 (10.19+10.19s): img1 → img2
- P02 (56.87s): img4 (27.43s) → occult flash montage 5.jpg–9.jpg (1.5s each, fixed, not
  rescaled — a deliberate fast-cut effect) → img4 again (21.94s)
- P03 (22.03s): new-meldemannstrasse → keep-a11
- P04 (31.23s): `ic-clean.mp4` (14.2s, playbackRate 0.34) → keep-a13 (17.04s)
- P05 (51.94s): keep-a17 → img20 → new-winifred-wagner
- P06–P07: 2 beats each, even split
- P08 (51.31s): img22 → img23 → img24, even 3-way split
- P09 (37.89s): img26 (dip-to-black in, pivot #1) → img14 (2nd reuse)
- P10 (41.32s): keep-a30 → img27
- P11 (23.40s): img29 → `h-and-h-clean.mp4` (7.8s, playbackRate 0.56, cut in/out) → 30.jpg
- P12: img31 → img32
- P13 (24.28s): img38 → `eva-clean.mp4` (8.67s, playbackRate 1.44, cut in/out) → keep-a20
- P14: img33.webp → img17
- P15: new-haus-wachenfeld → img36
- P16 (26.96s): `holiday-clean.mp4` alone, full paragraph (dip-to-black in, pivot #2,
  playbackRate 0.27 — deliberately slow-motion for the wedding ceremony)
- P17 (27.94s): img39 (dip-to-black in, pivot #3) → img40
- P18 (7.22s): img41, closing hold
- Outro: `LikeSubscribeCard`, 5s, dip-to-black in (no VO — P18's spoken line already carries
  the subscribe CTA; this is just the animated card's visual beat)

44 scenes total, 580.64s (~9:41) final runtime. All aspect ratios re-measured directly via
`ffprobe`/VP8-header parsing (not reused from the v2 manifest) since the image set could have
changed; `-clean` clip variants (already cropped to clean 1920x1080 + trimmed past the credit
cards, from the 2026-07-13 crop-fix pass) used throughout instead of the original uncropped
files — no crop filter needed in `ClipScene` anymore, just `playbackRate`.

## What's still open

- **Spot-check the render** against the script for beat/narration sync, especially the
  paragraphs flagged above. If a cut visibly lands mid-sentence, the fix is a targeted manual
  nudge to that one paragraph's split (not a full re-time).
- If this drift proves unacceptable, the clean fix is regenerating true per-paragraph audio
  (P01–P18) via Epidemic Sound as v2 originally specified, then reverting to the
  per-scene-`audio`-ownership model — `spec.narration` stays available as a fallback path for
  future episodes where only a continuous take exists, but per-span audio remains the preferred
  default per standing project convention.
- `active-episode.json` now points at this episode (`love-life`); ep006's previously-active spec
  was backed up to `episodes/ep006-war-on-religion/spec-rendered.json` before being overwritten.

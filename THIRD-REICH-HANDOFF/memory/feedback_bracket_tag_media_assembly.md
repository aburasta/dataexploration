---
name: feedback-bracket-tag-media-assembly
description: Standard end-to-end pipeline for turning a user-finalized Third Reich script into a rendered documentary video via reich-engine
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c2a81fc7-cfe7-41f6-82b2-fa6341dbbcfc
---

Standard media-assembly workflow for Third Reich episodes, established on ep003
(hitler-love-life), 2026-07-10, superseding the earlier manual scene-curation approach.

**Standing pipeline, confirmed 2026-07-10 on ep006 (war-on-religion):** once the user hands
Claude a *finalized* script (whether via the normal angle-pool → `script-rough.md` →
user-edited `script-final.md` flow, or a standalone script the user wrote/pasted directly into
`Third Reich/scripts/`), the routine — without needing to be re-explained — is: (1) copy it
verbatim into the episode folder and bracket-tag it (Claude does the tagging now, not just the
user — see below), (2) write a tag-indexed `media-plan.md`, (3) source real media per tag and
drop it in `Third Reich/Media/<slug>/`, (4) get the user's visual sign-off on the tag↔media
correspondence, (5) generate per-span TTS narration, (6) assemble and render in `reich-engine`
with the standard Like & Subscribe end card. Do not ask the user to re-describe this sequence —
it's the default for every future episode unless they say otherwise.

**Claude now does the tagging itself.** Originally the user hand-placed every bracket tag; on
ep006 Claude read the finalized narration cold and inserted the `(N)…(N)` spans itself —
splitting on natural clause/sentence boundaries, deciding still-vs-callback per tag, and
deliberately reusing an earlier tag number when the same visual subject recurs later in the
script (thesis statement, "he was not wrong, he was just early" full-circle beats, etc.) — same
non-nesting FSM as before. This worked well and is now the default; don't wait for the user to
tag it unless they say they're doing it themselves.

**Automated media sourcing (new capability, proven on ep006, all 59 tags).** When the
`claude-in-chrome` MCP is connected, use it for live Google Images/YouTube search as originally
planned. **When it isn't** (happened for the entire ep006 batch — extension never connected),
fall back to: WebSearch for the subject (append "wikimedia commons" or "Bundesarchiv" to the
query) → identify the exact Commons filename → download with `curl -L`, e.g.
`https://commons.wikimedia.org/wiki/Special:FilePath/<exact_filename>?width=1200`. This
public-domain/CC-BY-SA tier (Bundesarchiv via Commons, plus NARA/LOC-equivalent) is the same
sourcing tier ep003 used manually, so it's a legitimate substitute, not a downgrade.
- **Wikimedia rate-limits aggressively and inconsistently** (HTTP 429 "Too many requests",
  `noc@wikimedia.org` in the error body) — it's a bursty leaky-bucket, not a clean per-N-seconds
  throttle: some requests succeed seconds apart while others fail repeatedly for no visible
  reason even with 20-25s gaps. Always append `?width=1200` (thumbnail, not full-res — the error
  message itself suggests this) and space requests out; when a specific file keeps 429ing after
  several genuine attempts, stop fighting it and substitute the closest already-downloaded file
  rather than burning more time — flag the substitution honestly in `media-plan.md` rather than
  silently forcing a weak match.
- URL-encode filenames with `%20`/`%2C` etc., not raw spaces/commas/umlauts — a raw non-ASCII
  character (e.g. `ö`) in the URL produces a "Bad title" error that looks like the file doesn't
  exist when it actually does.
- **Always visually verify every downloaded image before calling a tag done** — on ep006, three
  search results that looked right by filename/caption turned out wrong on inspection: a
  wax-museum diorama mistaken for a real historical photo, a modern American church mistaken for
  a period German one, and a modern Filipino church mistaken for a European one. Catching these
  requires actually opening the image (Read tool), not just trusting the search result's title.

**Script markup:** the user places a matched open/close tag around each sentence/clause in
`script-rough.md`/`script-final.md` — numbers like `(1)…(1)` for still images (mapping to
`N.jpg`/`.jpeg`/`.webp`/`.png` in the episode's media folder), or short mnemonic tags like
`(IC)…(IC)`, `(Eva)…(Eva)` for video clips (mapping to `<tag>.mp4`). This forms a clean,
non-overlapping partition of the whole script — the FSM is: walk tag tokens in order, the
first occurrence of a value opens a span, the next occurrence of that same value closes it,
the next token always opens a new span (spans never truly nest even when tags look adjacent
like `(6) (7)`). A tag value can legitimately repeat later in the script for a deliberate
thematic image callback (seen with `(11)` reused for an "outcast" beat) — treat that as
intentional, not a parsing bug. Untagged trailing text (e.g. a closing subscribe CTA) holds
on the last visual rather than erroring.

**Voice note generation — per-span TTS, not one continuous pass.** Generate one edge-tts clip
per span (not a single call over the whole script): this gives an exact, unambiguous duration
per span with zero forced-alignment guessing. Concatenate the per-span clips in order (via the
actual `ffmpeg.exe` binary bundled inside
`reich-engine/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe` — **do not** use
`npx remotion ffmpeg`, its argument passthrough is broken and silently mis-parses `-f concat`
flags; call the bundled binary directly instead) to produce the single deliverable "voice
note" file, with brackets stripped from the spoken text. The same per-span clips double as
each Remotion scene's per-scene audio, so the video and the standalone voice note are
frame-identical by construction.

**Image scenes:** `durationSec` = that span's measured audio length; `KenBurnsImage` already
sizes its pan/zoom to fill whatever duration it's given, no engine change needed.

**Video clip scenes — stretch/compress via playbackRate, not short hard-cut inserts.**
`reich-engine/src/ClipScene.jsx` was extended with a `playbackRate` prop passed straight
through to `OffthreadVideo`. Compute `playbackRate = sourceSecondsUsed / durationSec` (probe
native clip length with `npx remotion ffprobe`, or the bundled `ffmpeg.exe` directly — this one
works fine unlike the ffmpeg wrapper). This is a real behavior change from the prior approach
(short ~5s hard-cut inserts): bracket-tagged clip spans run the clip's own full/extended length
slowed or sped to exactly fill the sentence, which can mean deliberate slow-motion (rates as
low as ~0.19x tested fine) rather than a quick cutaway. Before picking a `startTrim` in-point,
extract a preview frame (`ffmpeg -ss <t> -frames:v 1`) to confirm it isn't sitting on a static
thumbnail/play-button frame from a screen-recorded source clip — a real issue seen on this
project's raw clips.

**No on-screen text, with two deliberate exceptions:** the documentary body stays completely
text-free (no captions/lower-thirds anywhere) except for these two carved-out cases:
1. The animated end card — `reich-engine/src/LikeSubscribeCard.jsx`, a `type: "outro"` scene —
   with a like icon, "LIKE & SUBSCRIBE" text, and a pulsing subscribe bell, that fades the whole
   card to black over its final ~1.1s (needed because Remotion's `dip-to-black` transition only
   handles the fade-IN at scene start; the last scene has no next scene to provide the fade-out
   half, so a self-fading final scene is required for the video to end on black rather than cut
   abruptly). Reuse it for every future episode's closer rather than re-litigating the rule.
2. **Quote/diary-entry typewriter overlays (added 2026-07-14, special-legal-coup-1919-1933
   session).** For most quotes in the script — and *always* for actual diary-entry quotes — show
   the quote's actual words typed out on screen in a typewriter/typing-reveal animation, paired
   with an image of the person the quote is from occupying only part of the frame (not full
   bleed). Vary the composition every time rather than reusing one layout: sometimes the portrait
   takes half the screen with the quote beside it, sometimes the portrait is styled like a small
   printed photograph tucked in a corner of an otherwise black/dark background with the quote
   typed out across the rest of the frame. Sometimes (not always — vary it) add a subtle
   typewriter clack sound effect synced to the reveal. This is a second, separate exception to the
   no-text rule — don't fold it into or confuse it with the end-card exception above.
   - **Comic speech-bubble variant** (added on paragraph 10 of the same session, for a shouted
     quote — Hitler's "The National Revolution has begun!" at the Bürgerbräukeller): when a
     strong image exists of the speaker mid-speech/shouting, this variant skips the split-frame
     treatment — use the full image, darken a portion of it, and place a comic-style speech
     bubble (white background, tail pointing near the speaker's head/mouth) with the quote typed
     inside it. Reserve this for genuinely dramatic/shouted lines where a fiery speech-photo
     exists; it's one more option in the varying rotation, not a replacement for the
     half-screen/corner-photo defaults above.

**Sound design is now a first-class creative pass, not just "one ambient bed" (escalated
2026-07-14, special-legal-coup-1919-1933 session).** The user wants sound design that actively
tunes to the beats and content of the script — not a single flat music bed under the whole
episode. Standing approach: maintain a `Third Reich/sound-design-guide.md` reference (researched
from real documentary sound-design practice) mapping script-moment types to a sound treatment,
e.g. cold-open hooks get a tension drone/room-tone under them, quote-reveal beats (see typewriter
overlay exception above) get a typewriter clack, revelations/turning points get a stinger or a
dip to near-silence rather than more music, montages of escalating events get building
percussion/tempo increases, transitions get a soft riser/whoosh, epilogue/reflection beats get
the music thin out or drop to silence. Vary the specific choice each episode/scene for freshness —
don't reuse the identical cue in the identical spot every time — but the *category* of treatment
per moment-type is the standing rule and shouldn't be skipped. Source real sound-effect/music
files ahead of the Remotion build (not invented placeholders) so they're ready to drop into the
spec. The Higgsfield-style MCP's `generate_audio` is TTS-only and explicitly cannot produce
music/SFX — don't try prompting it for a music bed or sound effect. Source a free ambient/tension
track instead (Incompetech/Kevin MacLeod tracks download cleanly via direct URLs like
`https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Track%20Name>.mp3`; Pixabay's own
sound-effects/music library requires no attribution and is a good source for typewriter clacks,
stingers, and tension drones specifically, though the site itself is JS-walled and doesn't work
via WebFetch — download links still resolve via `curl -L` once the exact file URL is known).
Kevin MacLeod tracks are CC-BY — flag the required
attribution line to the user for the YouTube description.

**Real video-clip sourcing (established 2026-07-15, special-legal-coup-1919-1933): footage from
outside an episode's exact narration date range is fine if a short usable portion fits the
context** — the user explicitly said generic public-gathering/Nazi-official footage from other
years is acceptable, not just frame-exact matches. What matters is the *rights*, not the date:
- **Reject anything in Internet Archive's "fringe" or "deemphasize" collections outright**, even
  when it looks like the perfect clip and nothing else turns up — check `archive.org/metadata/<id>`
  for the `collection` field before getting attached to a candidate. These tags mean IA itself
  flagged the uploader as unreliable/extremist-adjacent; no rights statement is trustworthy there.
- **NARA's and USHMM's own official catalogs are not automatically clear either** — both surfaced
  excellent-looking candidates (a Nuremberg-trial exhibit reel; Steven Spielberg Film Archive rally
  footage) that turned out copyright-restricted (news-agency-owned, e.g. Fox) or on-site-viewing-
  only with no downloadable file. Always open the specific item page and read its actual rights/
  access statement — being *in* NARA or USHMM's catalog is not itself a usable-for-YouTube signal,
  same lesson as the earlier Internet Archive "on archive.org isn't PD" finding.
- **Confirmed-clean sources found and worth returning to first:** Frank Capra's "Why We Fight"
  series (e.g. `PreludeToWar` on IA) — definite public domain as US War Department productions,
  and despite being framed around WWII they splice in substantial genuine 1920s-30s German/Italian/
  Japanese newsreel footage as context (rally crowds, marching soldiers, propaganda banners,
  labeled official portrait cards) — scrub through at ~2-3 minute intervals with ffmpeg frame
  grabs to find usable stretches, since relevant and irrelevant countries/eras are interleaved
  unpredictably rather than blocked together. The **FedFlix / "United States Government Films"**
  collection on IA (items sometimes prefixed `mt-mtt-` from Movietone-sourced but US-government-
  cleared reels) is reliably clean — confirm via the item's collection tags. **Universal Newsreels**
  (identifiers prefixed `un-un-` or `200-un-`) are also a legitimate PD source, but check the
  identifier suffix carefully: a single `-sN` (e.g. `-s7`) is **one story excerpt only**, not the
  full reel — only a range suffix (`-s1-7`, `-s1_8`) or a title with its own dedicated identifier
  (found via search, not guessed) is the complete multi-story newsreel. Guessing sequential
  identifiers (`-s2`, `-s3`) to find a specific story rarely works; search by the story's own
  keywords instead (e.g. "Hitlerites Parade In Rain" surfaced its own identifier directly).
- **Workprint/reference copies sometimes have a burned-in timecode overlay** in one corner — real
  and usable, but lower priority than clean footage; mention this quality difference to the user
  rather than silently treating both tiers as equivalent.
- Cut short clips (5-12s) with the bundled `ffmpeg.exe` (`-ss <start> -i <src> -t <dur> -c:v libx264
  -crf 20 -an`) rather than using the full source file — matches how `ClipScene.jsx`'s
  `playbackRate` stretches a clip to fill its assigned span, and keeps per-tag files small.

**Round 2 refinements, confirmed 2026-07-12 on ep006 after user feedback on the first cut.** The
first ep006 render had three real quality problems the user flagged directly — these are now
standing rules, not one-off fixes:

- **Repetition budget: aim under ~10-15%, not the ~32% the first pass produced.** Root cause was
  giving up after a single WebSearch query per tag. Fixed by using a tiered fallback, only
  reusing an existing image after actually trying ≥2 tiers: (1) the subject's Wikipedia infobox
  image (fastest, usually best-known portrait), (2) Wikimedia Commons' *own* search
  (`commons.wikimedia.org/w/index.php?search=...&title=Special:Search&fulltext=1&ns6=1`), not a
  generic web search — Commons' own search surfaces its 430,000+ Bundesarchiv holdings far better
  than WebSearch summaries do, (3) Deutsche Digitale Bibliothek / Library of Congress / USHMM
  collections as a second opinion. Internet Archive's book-cover service
  (`https://archive.org/services/img/<item-identifier>`) is a good source for a book's real title
  page when no portrait/cover art exists. Report the final reuse count to the user honestly
  either way — some reuse is legitimate (same person shown again with no other photo available,
  same place referenced twice in one sentence) and should be labeled as such, not hidden.
- **Off-ratio images were getting harshly cropped.** `KenBurnsImage.jsx` now checks a precomputed
  `aspectRatio` field (width/height, computed by the spec-build script via `ffprobe`) against a
  1.5–2.1 band around 16:9: inside the band, plain `objectFit: cover` (the existing Ken Burns
  push/pull sells the small crop as intentional); outside it (portraits, extreme panoramas), a
  blurred/darkened full-bleed `cover` backdrop plays behind a full, uncropped `contain` copy on
  top — nothing is ever lost. Also cap every sourced image at max 1920px on its long edge
  (`ffmpeg -vf "scale='min(1920,iw)':'min(1920,ih)':force_original_aspect_ratio=decrease"`) — a
  50-megapixel (10000×5000) Commons panorama caused an actual `EncodingError: source image cannot
  be decoded` browser crash mid-render on this machine's tight RAM, not just a cosmetic issue.
- **Real video clips, sourced from Internet Archive, not just Commons.** Commons has almost no
  motion footage. `archive.org` direct-download pattern:
  `https://archive.org/download/<item-identifier>/<filename>`. **Rights vary per item — "on
  archive.org" is not itself a usable-for-monetized-YouTube signal.** A "Triumph of the Will"
  excerpt found this way was explicitly CC BY-NC-ND (non-commercial, no-derivatives) and was
  correctly *not* used. The Prelinger/Sandler Film Library stock-footage collection generally
  curates public-domain ephemeral material and is a reasonable source, but still flag per-item
  rights uncertainty to the user rather than asserting clear PD. Preview every candidate clip with
  extracted frames (`ffmpeg -ss <t> -frames:v 1`) before committing — one clip's book-burning
  footage turned out to be an exact, much stronger match for a specific script beat (Bible
  publishing ban) than the generic atmosphere role it was first pulled for.
- **Vary transitions with purpose, not just "xfade + occasional dip-to-black."** Reserve `cut`
  (hard cut, already defined in `Transitions.jsx`) for two specific situations: (a) a scene that's
  a same-image continuation of the immediately preceding one (e.g. a cold-open sentence split into
  two shorter spans for pacing — a crossfade-to-itself is pointless, a cut keeps it snappy), and
  (b) a scene whose narration is a standalone direct quotation — a hard cut lands a quote harder
  than a soft dissolve. Keep `dip-to-black` reserved for genuine act/chapter breaks and heavy
  beats as before. This reads as deliberate editing rather than either monotonous or gimmicky.
- **Denser cuts in the first ~30-45s specifically.** Split the cold-open's longer spans into two
  shorter ones at a natural clause break, reusing the *same* already-sourced image for both
  halves with different `motion` values — this doubles cut frequency for the hook without
  requiring new distinct images or creating the disliked kind of repetition (adjacent quick cuts
  on one establishing shot read as intentional pacing, not laziness).

**Render environment is the real bottleneck on this machine (~4GB total RAM) — expect instability
and plan for it, don't just retry blindly:**
- `--concurrency=1` is required; even then, `chrome-headless-shell`/`node` processes leak memory
  over a long render and the failure mode is inconsistent: sometimes a clean crash
  (`EncodingError`, browser crash + failed retry), sometimes a silent death-spiral where the ETA
  climbs from minutes to 90+ hours without erroring, sometimes it recovers on its own. Frame
  rendering (`Rendered N/15098`) reaching 100% does **not** mean the job succeeded — a separate,
  recurring bug in the final audio-mux step
  (`ffmpeg ... remotion-audio-mixing\0.wav: No such file or directory`, exit code
  4294967294) has failed after 100% frame completion on two separate full attempts. This looks
  like an intermittent Windows temp-directory race, not a memory issue — **a plain retry of the
  exact same render command is a legitimate fix**, not just hopeful repetition, because frame
  rendering itself has proven reliable once it completes.
- `TaskStop` does **not** cascade-kill child `chrome-headless-shell`/`node` processes on Windows —
  always follow it with an explicit process kill
  (`Get-Process -Name "chrome-headless-shell","node" | Stop-Process -Force`) before starting a
  new render attempt, or the old attempt's orphans silently compete with the new one for the same
  tight RAM. **Never kill plain `chrome.exe`** (as opposed to `chrome-headless-shell.exe`) while a
  render is active — it can be a page/session the render itself depends on, and killing it caused
  an active render to fail outright (`Protocol error: Session closed`) rather than just freeing
  memory.
- Splitting a render into frame-range batches (`--frames=0-999`, etc., each getting a fresh
  browser process) is a real, valid mitigation for the memory-leak degradation curve and was
  about to be used successfully — but the user's explicit preference, given a choice, was a
  **single full render, not batches**, even knowing it's less RAM-safe. Default to a single
  full-length render; only propose batching if a full attempt has already failed multiple times
  and the user hasn't said otherwise.
- Do not add Windows Defender exclusions or otherwise weaken security controls to work around
  render instability, even under a broad "optimize however you need to" instruction — that
  specific class of fix needs the user to name it explicitly, and the auto-mode permission
  classifier will correctly block it otherwise.

**Pre-tagging creative-vision planning sessions (established 2026-07-14, special-legal-coup-1919-1933
episode).** Before bracket-tagging/media-plan, the user likes to walk the finalized script
paragraph-by-paragraph with Claude and state a creative vision per paragraph (specific shots,
special treatment, unusual pacing, etc.), logged into a `creative-vision.md` file in the episode
folder. **Default visual treatment when the user doesn't add anything extra for a paragraph:**
literal, relevant historic photos/videos depicting the paragraph's actual described events —
being lenient on exactness is fine and expected. If the precise incident has no surviving
photo/footage, a piece of period-accurate media reasonably standing in for it (the same
person/place/type of event, or something that's been used as a substitute in other WW2/Third
Reich documentaries in that same context) is an acceptable default, not a downgrade to flag. Only
deviate from this literal-substitute-imagery default when the user explicitly adds a creative
layer for that specific paragraph (metaphor, stylization, a specific unusual shot, etc.) — absent
that, assume the plain/literal default across the whole script, not just the paragraph it was
first stated on.

**Fast-paced cutting is now a standing requirement for this series, not just a nice-to-have
(stated 2026-07-14 during the special-legal-coup-1919-1933 creative-vision session).** Subdivide
each paragraph into beats — one beat per distinct important idea/sub-event within the paragraph —
and give each beat its own image/clip rather than holding one image across a whole paragraph.
`durationSec` for each beat = that beat's own measured TTS length (already how the engine works
per-span), so shorter beats naturally produce faster on-screen cuts. This is a deliberate
escalation of the pacing guidance already in this file (denser cuts in the first 30-45s) into a
whole-episode default: bracket-tag at beat/clause granularity throughout, not just in the cold
open.

**Data-viz motion graphics are an occasional, opt-in scene type — build a throwaway prototype
first, don't wire straight into the real episode.** Confirmed on special-legal-coup-1919-1933:
when a paragraph's content is more naturally a chart than a photo (an election result, a vote
tally), the user may ask for a custom Remotion graphic. Workflow that worked: add a new scene
component (e.g. `reich-engine/src/Hemicycle.jsx`), wire it into `Documentary.jsx`'s `SceneBody`
dispatch via a new `scene.type`, add a standalone preview `<Composition>` in `Root.jsx` with
hardcoded `defaultProps` (no real episode spec needed), render stills at a few frames plus a
short mp4 with `npx remotion still`/`render --concurrency=1`, and get an explicit go/no-go before
it's ever used in a real spec. If the user says no (happened for a paragraph-15 "shadow-state
departments" hub-and-spoke diagram idea), **delete the component and its Root.jsx/Documentary.jsx
wiring outright** rather than leaving dead code — don't keep a rejected prototype around "just in
case." `reich-engine/src/Hemicycle.jsx` is now a confirmed, reusable `scene.type: "hemicycle"` —
a classic parliament dot-chart (concentric semicircular rows, contiguous left-to-right color
blocks) that takes a `segments: [{count, color, label?}]` prop and works for three different
data shapes without code changes: seats (small `count` vs. total), vote-share (percentages
summing to 100), and yes/no tallies. Text-off by default (`showLabels` opt-in) to respect the
no-on-screen-text default.

See [[project_war_logistics_visual_pipeline]] for the sibling Seedream-based pipeline on a
different series; this reich-engine method is specific to Third Reich's archival-photo-and-clip
format.

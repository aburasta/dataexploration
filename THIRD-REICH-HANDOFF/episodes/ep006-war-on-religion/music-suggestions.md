# ep006 — Music & SFX suggestions (for you to download & drop in)

Mapped to the moment-types in `reference/sound-design-guide.md`. The render spec (`spec-rendered.json`)
currently loads a single looped bed via `spec.music = "music-bed.mp3"`; pick **one primary bed**
below, then optionally add the per-moment cues/SFX if you later want a layered mix. Put audio in
`reich-engine/public/media/war-on-religion/` (or wherever the spec's `mediaDir` resolves).

**Two clean, licence-safe sources** (per the guide):
- **Kevin MacLeod / Incompetech** — CC-BY (one attribution line in the YouTube description). Direct
  download pattern: `https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Track%20Name>.mp3`
- **Pixabay Music/SFX** — no attribution required. Site is JS-walled; search the track name, then download.

## Primary music bed (choose one) — somber, sustained, never fights the voice
| Track | Source | Why |
|---|---|---|
| **Long Note Four** | Incompetech (K. MacLeod) | Near-static sustained drone — ideal low bed under narration |
| **Echoes of Time v2** | Incompetech | Slow, grave, documentary-standard for this era |
| **Dark Times** | Incompetech | Ominous minimal pulse; good for the church-takeover build |
| "cinematic documentary / dark ambient" | Pixabay (search) | If you prefer no-attribution |

Recommended: **Long Note Four** as the bed (ducks invisibly under VO), with **Echoes of Time v2**
swapped in for the darker middle act if you want variation.

## Per-moment cues (optional layered mix)
| Moment (scenes) | Treatment (guide) | Suggested cue |
|---|---|---|
| Cold open — Sportpalast / Krause (1–14) | low tension drone, no melody | **Long Note One/Two**, or Pixabay "tension drone" |
| Rising tension — absorption / Reich Church (17–29) | tempo/percussion build | **Ossuary 5 – Rest**, **Clash Defiant**, or **Hitman** |
| Revelation / dip-to-black pivots (scenes 1, 22, 36, 51, 61, 66, 69) | stinger OR hard dip to silence | **Impact Prelude** stinger, or let the dip breathe in silence |
| Heavy / sober — Niemöller arrest, camps, murdered signer (35–42) | sparse, often no score | drop bed to **room tone / near-silence** |
| Epilogue / reflection — "he was just early", "little resistance" (65–76) | thin out, single sustained note | **Elegy** or **Meditation Impromptu**, fading to one held note |

## SFX (Pixabay — no attribution), used sparingly per the guide
- **Radio static / tuning** → scene 22 (Hitler's radio broadcast) and the "Nazi press" beats.
- **Fire crackle** → under the book-burning clip (scene 62 / `51.mp4`).
- **Typewriter clack** → document beats *if* you add type-on overlays (Article 24, the 25-point
  program, Rosenberg's 30 points, Bormann's circular). Guide says use *sometimes*, not every quote.
- **Soft paper rustle / page-turn** → the numbers/document beats.
- **Old newsreel hiss / projector clatter** → very low under the two archival clips to marry them to the stills.

## Attribution line (if you use any Kevin MacLeod track)
`Music: "<Track Name>" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0`

> I can pull the Incompetech tracks straight into the media folder once you confirm the bed; Pixabay
> ones I'd need the exact track URL from you (the site blocks scripted browsing).

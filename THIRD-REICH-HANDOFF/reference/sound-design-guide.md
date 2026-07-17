# Third Reich Series — Sound Design Guide

Reference for tuning sound design to script beats/content across every episode, not just a flat
music bed. Established 2026-07-14 during the special-legal-coup-1919-1933 creative-vision
session. Vary the *specific* cue used each time; the *category* mapping below is the standing
rule and should not be skipped.

## Principles (from documentary sound-design practice)
- Narration is always king: dialogue/narration sits at ~100%, music and SFX duck under it —
  never fight the voice for attention.
- Music/SFX exist to steer emotion and signal a change in tone, not to fill silence reflexively.
  Silence itself is a legitimate, powerful tool at heavy or reflective moments.
- Archival-style SFX (typewriter clacks, radio static, old newsreel hiss, film-projector clatter)
  ground a scene in its era — use them at moments that reference documents, broadcasts, or film.
- Tension is built with low drones, subtle room tone, and slow harmonic movement; release is a
  stinger, a hard cut to silence, or a resolving chord — not just "turn the volume down."

## Moment-type → treatment map
| Moment type | Treatment |
|---|---|
| Cold open / hook | Low tension drone or moody room tone under the narration, no melody yet — held back so the eventual reveal has somewhere to go |
| Quote reveal (typewriter overlay) | Typewriter clack SFX synced to the type-on animation — used *sometimes*, not every single quote, per the overlay rule |
| Diary-entry quote specifically | Slightly more intimate/close mix, optionally a soft paper-rustle or pen-scratch under the typewriter clacks |
| Rising tension / escalating events (montage) | Percussion or tempo builds — each beat's cut lands a little faster/harder than the last |
| Revelation / turning point | Stinger hit, or a hard dip to near-silence for a beat before the next line — reserve for the moments that actually deserve it |
| Betrayal / violence / heavy material | Sober, sparse — often just narration and room tone, no score at all (matches the sensitivity rule already in the master guide) |
| Transition between acts/timelines | Soft riser or whoosh under the dip-to-black transition |
| Epilogue / reflection / closing thought | Score thins out, instrumentation drops, ending on near-silence or a single sustained note rather than a full band |
| Numbers/statistics/legal-document beats | Understated — a soft page-turn or paper SFX, no music intrusion |

## Sourcing
- **Pixabay** (`pixabay.com/sound-effects` and `/music`) — no attribution required, good for
  typewriter clacks, tension drones, stingers, risers. Site itself is JS-walled (WebFetch won't
  render it), but once the exact asset URL is known, direct download works.
- **Incompetech / Kevin MacLeod** — `https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Track%20Name>.mp3`
  downloads cleanly. CC-BY — attribution line required in the YouTube description.
- **Epidemic Sound** — already connected via MCP for the Debt Psychology/Forbidden Philosopher
  voiceover pipelines; also has a documentary SFX library if a subscription-backed source is
  preferred over ad-hoc downloads.

## Per-episode workflow
1. After bracket-tagging, pass over the tag list and mark each span's moment-type from the table
   above.
2. Source or reuse 1 cue per moment-type actually present in the episode (don't over-fetch —
   most episodes will reuse the same handful of cues across many beats of the same type).
3. Note the chosen files + their placement in the episode's `media-plan.md` so the Remotion spec
   step has everything it needs.

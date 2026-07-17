# ep003 — Media Cut v2 (redo plan, 2026-07-13)

Supersedes `media-cut-v1.json`/`media-cut-v1-notes.md`. Script text (`script-final.md`) is
unchanged — this only rebuilds narration audio grouping and the visual cut.

## What's fixing what

- **Pauses** → narration re-recorded as **18 continuous clips (P01–P18)**, one per paragraph,
  instead of 47 tiny per-bracket-tag clips. Bracket tags below mark *where the visual cuts*,
  not where the audio is spliced.
- **Orientation** → every image's real aspect ratio measured (see manifest below); the engine's
  existing letterbox path (blur backdrop + full "contain" image) now gets accurate data, so nothing
  is cropped/stretched wrong. Most of this episode's images are portrait/document shots outside the
  1.5–2.1 "cover" band, so letterboxing will be the norm here, not the exception — that's expected
  and correct.
- **Pacing** → no beat held past ~6–8s. Long idle stretches (old S10 Vienna 25s, S27–33 ~20–25s)
  broken into 2–3 shorter beats each via the engine's audio-ownership mechanism (one narration
  clip "owns" itself + every following silent scene).
- **Transitions** → `xfade` (true crossfade) is the default. `dip-to-black` cut from 7 uses down to
  **3**, reserved for the biggest pivots only: into Geli's death (P09), and into the wedding/bunker
  close (P16). `cut` used for punch on the occult montage and clip in/out.
- **Occult montage** → `5.jpg`–`9.jpg` (already-sourced real book covers: *The Nazis and the
  Occult*, *The Nazi Occult*, *Gods & Beasts*) flashed at ~1.5s each under P02's occult sentence.
- **Video clips** → all 4 kept, pillarbox-cropped and (for `h-and-h.mp4`) trimmed to clear a
  bottom-edge subtitle sliver and (for `holiday.mp4`) trimmed past an opening credit card. Verified
  by pulling real frames and measuring pixel data — see Clip crop spec below.
- **Known-issue cleanup**: `img3` dropped (was reused 3x); `img35` (ambiguous "signing" photo)
  swapped for `img36` (bunker room); `img34` (unverified SS officer) moved to the Emil Maurice
  mention per the old notes' own suggestion, framed generically (no on-screen ID claim since the
  narration doesn't name him there); Strasser/Winifred Wagner/Vienna/cemetery beats now use the
  new `new-*`/`keep-a*` photos sourced today instead of generic stand-ins.
- **Unresolved, unchanged from v1**: no real Ciano/Sigrid von Lappus photo exists; P14 still uses
  suggestive portraits (`img33`, `img17`) for that rumor, same judgment call as before.

## Aspect-ratio manifest (key non-obvious ones; full set measured for all 50 images)

Portrait/off-ratio images (will letterbox, i.e. show full-bleed blurred backdrop + full image) —
this is most of the set: `1.jpg` 0.72, `3.jpg`(unused) 0.72, `4.jpg` 1.05, `5–9.jpg` (occult books)
0.65–0.74, `14/16/22/23/24/26/30.jpg` 0.64–0.77, `new-strasser.jpg` 0.59, `new-winifred-wagner.jpg`
0.86, `new-haus-wachenfeld.jpg` 1.455. Near-16:9 "cover"-band images (fill frame normally):
`keep-a11/13/17/20/30.jpg` all exactly 1920x1080 (1.778); `new-meldemannstrasse.jpg` 1.69;
`12/15/18/19/25/27/33.webp/34/36.jpg` 1.5–1.9.

## Clip crop spec (measured via pixel scan of extracted frames, verified with test-crop renders)

| Clip | Source | Fix | ffmpeg filter |
|---|---|---|---|
| `eva.mp4` | 2262x1080, black pillarbox both sides (content x:215–2035) | crop out pillarbox | `crop=1820:1080:215:0,scale=1920:1080` |
| `h-and-h.mp4` | 2690x1080, pillarbox + subtitle sliver at very bottom edge | crop pillarbox + drop bottom 80px | `crop=1778:1000:308:0,scale=1920:1080` |
| `holiday.mp4` | 2106x1080, pillarbox + opening credit card ("A film written by...") in first ~1.5s | crop pillarbox + `startTrim: 1.6` to skip the card | `crop=1889:1062:192:9,scale=1920:1080` |
| `ic.mp4` | 1742x1080, no pillarbox, just narrower than 16:9 | crop height | `crop=1742:980:0:50,scale=1920:1080` |

All 4 verified visually via extracted test-crop frames — clean full-bleed 16:9, no black bars, no
caption/UI remnants.

## Scene map (P01–P18 = the 18 continuous narration clips; sub-beats share each clip's audio)

- **P01** — bunker wedding cold open. `img1` (marriage certificate) 6s xfade → `img2` (bunker
  ruins) 6s xfade.
- **P02** — "great love was Geli" + occult digression + thesis. `img4` (Geli/Hitler) 5s xfade →
  **occult montage**: `5.jpg`→`6.jpg`→`7.jpg`→`8.jpg`→`9.jpg`, ~1.5s each, `cut` between each for
  a fast flash-montage feel (~7.5s total) → back to `img4` 4s xfade for the closing thesis line.
- **P03** — Vienna years. `new-meldemannstrasse.jpg` (Männerheim building) 5s xfade → `keep-a11.jpg`
  (men's home interior) 6s xfade.
- **P04** — WWI / Iron Cross (`IC` tag). `ic.mp4` (cropped) full clip xfade in → `keep-a13.jpg`
  (WWI soldiers group) 6s xfade.
- **P05** — post-prison fame, early women, no marriage. `keep-a17.jpg` (Hitler at prison window)
  5s xfade → `img20` (early circle) 5s xfade → `new-winifred-wagner.jpg` 4s xfade (lands on the
  Wagner mention specifically).
- **P06** — Geli arrives, "only true love." `img14` (Geli portrait) 6s xfade → `img19` (Munich
  apartment) 6s xfade.
- **P07** — party gossip, tyranny, Emil Maurice suspicion. `img20` 5s xfade → `img34` (placed here
  per old notes' own suggestion, generic framing, no on-screen ID claim) 5s xfade.
- **P08** — Stempfle letter and killing. `img22` (old letter) 5s xfade → `img23` (Stempfle) 5s
  xfade → `img24` (forest) 5s xfade.
- **P09** — Geli's death. **dip-to-black in** (pivot #1) → `img26` (apartment) 6s xfade → `img14`
  (Geli's face, 2nd of 2 allowed reuses) 6s.
- **P10** — grief, grave visit, vegetarian vow. `keep-a30.jpg` (Vienna cemetery) 6s xfade →
  `img27` (Geli photo spread) 6s xfade.
- **P11** — Hindenburg meeting. `img29` (handshake) 5s xfade → `h-and-h.mp4` (cropped) full clip
  cut in/out → `img30` (Hitler w/ field marshal) 5s xfade.
- **P12** — Eva introduced at Hoffmann's shop. `img31` (shop) 5s xfade → `img32` (Eva at shop) 5s
  xfade.
- **P13** — Eva's strange life (swim/ski/wait). `img38` (Eva+Hitler+dogs) 4s xfade → `eva.mp4`
  (cropped) full clip cut in/out → `keep-a20.jpg` (Hitler+Eva reclining) 5s xfade.
- **P14** — Ciano/Sigrid rumor (unresolved, suggestive per v1). `img33` (Berghof couple, color)
  5s xfade → `img17` 5s xfade.
- **P15** — April 1945, Eva returns to die with him, "he married her." `new-haus-wachenfeld.jpg`
  (Hitler alone, private) 5s xfade → `img36` (bunker room, replacing ambiguous `img35`) 5s xfade.
- **P16** — the wedding ceremony (`Holiday` tag). **dip-to-black in** (pivot #2) → `holiday.mp4`
  (cropped, `startTrim: 1.6`) full clip.
- **P17** — suicide, "married less than forty hours" + closing reflection. **dip-to-black in**
  (pivot #3) → `img39` (bunker exterior) 5s xfade → `img40` (crowd, `slow-pull` motion to reveal
  scale) 6s xfade.
- **P18** — closing line + subscribe CTA. `img41` 6s hold, gentle xfade out.

Total: ~18 narration clips, ~45 visual beats, target runtime roughly similar to the original
11.6 min but with more cuts (faster feel) and 3 dip-to-blacks instead of 7.

## Next step

If this map looks right, Stage B generates the 18 narration clips via Epidemic Sound and Stage C
builds the render spec from this table.

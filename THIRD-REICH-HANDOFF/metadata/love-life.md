# Package: ep003 — Hitler's Love Life

- **Slug:** `love-life`
- **Series:** Third Reich (documentary) — RELATIONSHIP angle (dual-POV: Hitler's succession of women, centered on Geli Raubal, landing on Eva Braun and the bunker)
- **Render:** `Third Reich/renders/ep003-hitler-love-life.mp4` (runtime 9:40, 17,419 frames @ 30fps, ~580.64s)
- **Spec:** `reich-engine/src/active-episode.json` (currently active — 44 scenes, GLOBAL `narration` + `music` tracks, no per-scene audio)
- **Beat/paragraph map:** `Third Reich/episodes/ep003-hitler-love-life/render-spec-v3-notes.md`
- **Script:** `Third Reich/episodes/ep003-hitler-love-life/script-final-no-brackets.md`
- **Metadata (this file):** `Third Reich/metadata/love-life.md`
- **Thumbnail (fallback, exists):** `Third Reich/episodes/ep003-hitler-love-life/thumbnail.jpg`

> Note on timestamp derivation: this episode does not use the per-scene-audio model. Chapter starts
> were derived by summing cumulative `durationSec` across the 44 scenes in `active-episode.json` and
> cross-referencing the P01–P18 paragraph→scene mapping documented in `render-spec-v3-notes.md`. Because
> scene cuts here are word-count-proportional estimates (not measured per-clip durations), timestamps
> may drift ±1–2s in the longer paragraphs; they're snapped to the topic-sentence scene of each act.

---

## Who this is for

History viewers who know the WW2 headlines but have never followed the private, document-grounded
story of the women in Hitler's life. It targets people searching for "Geli Raubal," "Hitler and Eva
Braun," "who did Hitler love," "Geli Raubal death," or the bunker wedding — plus the broader
documentary audience drawn to a lesser-known, source-based angle that treats intimacy as a window into
character rather than as tabloid material. The viewer wants the real chronology and the real sourcing,
not sensationalism.

---

## Title — 3 options + recommended

1. **Hitler's Love Life: The Niece He Called His Only Love**  *(~53 chars — RECOMMENDED)*
2. Hitler's Only Love Was His Niece — Geli Raubal's Story  *(~54 chars)*
3. Hitler's Women: Geli Raubal, Eva Braun, and a Suicide  *(~53 chars)*

**Recommended: Option 1.** It front-loads the primary keyword ("Hitler's Love Life") in the first ~40
characters, uses the niche's proven colon-split dual-hook shape, and the payoff is literally grounded
in the video — Hitler told his inner circle the one true love of his life was his niece Geli Raubal,
dead since 1931. It stays analytical (no shock words, no innuendo), consistent with the channel's
non-political, document-driven tone. Option 2 is the strongest alternative if you want the em-dash
comparative "overturn an assumption" framing; Option 3 leads with named entities for search but is the
most tabloid-leaning of the three, so it's the fallback rather than the pick.

---

## Description — full copy-paste block

```
Hitler's love life was hidden even from his closest followers — and the one woman he called the only love of his life was his own niece, dead since 1931. This is the full story, from Vienna to the bunker.

In the early hours of April 29th, 1945, forty feet beneath a burning Berlin, Adolf Hitler married for the first time. Almost no one in his inner circle even knew Eva Braun existed. Yet for years he had told those closest to him that his one true passion was not the woman he was marrying — it was Geli Raubal, his half-sister's daughter, who had been dead for fourteen years.

This episode traces that succession of relationships as a window into the man. The paralysing shyness of his down-and-out Vienna years and the war that changed nothing; the early romances after prison — Jenny Haug, Erna Hanfstaengl, even Winifred Wagner — that went nowhere because parole, he said, left "no question of marriage"; the intense, controlling affair with twenty-year-old Geli in his nine-room Munich apartment; a compromising 1929 letter and the ex-priest Bernhard Stempfle, who knew too much and turned up dead in the Night of the Long Knives; Geli's death by gunshot in September 1931 — investigated and ruled a suicide, though Munich gossip long whispered otherwise, with no evidence ever surfacing; and finally Eva Braun, the photographer's assistant kept out of sight for twelve years, who traveled into a surrounded Berlin against his wishes to die beside him less than forty hours after the wedding.

WHO THIS IS FOR: viewers who know the WW2 headlines but have never followed the private, document-grounded story of the women in Hitler's life — and what his failure at ordinary intimacy reveals about him.

CHAPTERS
0:00 A Secret Wedding Under Berlin
0:20 The Woman He Truly Loved
1:17 Vienna and the War: A Man Alone
2:10 Fame, Parole, and First Romances
3:02 Geli Raubal, the Niece He Loved
4:20 The Compromising Letter
5:12 September 1931: Geli's Death
5:49 The Only Woman He Ever Loved
6:54 Eva Braun, the Hidden Mistress
8:05 Return to Berlin and the Wedding
9:00 What His Love Life Reveals

This is a STRICTLY NON-POLITICAL, educational history channel. Nothing here endorses or promotes any ideology, party, or regime — the material is presented for historical, documentary, and educational purposes only, and condemns the crimes of the period without reservation.

Sourcing: built on the standard published histories of Nazi Germany — principally William L. Shirer's "The Rise and Fall of the Third Reich" and the early biography by Konrad Heiden — alongside contemporary accounts (Count Ciano's diaries and the recollections of Hitler's own staff, including his chauffeur Erich Kempka). Geli Raubal's death is presented exactly as the state investigation ruled it, with the later murder rumors flagged as unproven. Where no photograph of a moment survives, we use an accurate contextual image rather than invent one. [FILL IN: add any specific page/edition citations you want credited]

New episodes cover the twists behind the major figures of the Third Reich you probably haven't heard before. If this was worth your time, subscribe and hit the bell — and share it with someone who'd find it as surprising as you did.

▶ WATCH NEXT: [FILL IN: paste link to the most related episode — e.g. ep006 "The Nazis' War on Religion"]

#ThirdReich #Hitler #WW2History #NaziGermany #History
```

---

## Tags — clean copy-paste line (8)

```
Hitler love life, Geli Raubal, Eva Braun, Hitler and Eva Braun, Geli Raubal death, Hitler bunker wedding, Third Reich documentary, WW2 history
```

---

## Hashtags (5, most important first — first one shows above the title)

1. #ThirdReich
2. #Hitler
3. #WW2History
4. #NaziGermany
5. #History

---

## YouTube chapters — copy-paste (derived from the render spec's scene list)

```
0:00 A Secret Wedding Under Berlin
0:20 The Woman He Truly Loved
1:17 Vienna and the War: A Man Alone
2:10 Fame, Parole, and First Romances
3:02 Geli Raubal, the Niece He Loved
4:20 The Compromising Letter
5:12 September 1931: Geli's Death
5:49 The Only Woman He Ever Loved
6:54 Eva Braun, the Hidden Mistress
8:05 Return to Berlin and the Wedding
9:00 What His Love Life Reveals
```

**How these were derived:** cumulative `durationSec` from `active-episode.json`, aligned to the P01–P18
paragraph→scene map in `render-spec-v3-notes.md`, then grouped at the episode's real narrative act
transitions (corroborated by the engine's `dip-to-black` pivots at ~5:12, ~6:31, ~6:54 and ~8:33).
Chapter starts snap to the topic-sentence scene of each act so each chapter opens on the line that
introduces its subject. Total runtime ~9:40.

| # | Start | Paragraph(s) | Scenes | Narrative beat |
|---|---|---|---|---|
| 1 | 0:00 | P01 | n1–n2 | The secret bunker wedding, 29 April 1945 |
| 2 | 0:20 | P02 | n3–n9 | Thesis: the love he truly claimed was dead since 1931 (occult flash-montage beat) |
| 3 | 1:17 | P03–P04 | n10–n13 | Vienna men's-home shyness + the war years; no ordinary intimacy |
| 4 | 2:10 | P05 | n14–n16 | Fame after prison; Jenny Haug, Erna Hanfstaengl, Winifred Wagner; "no question of marriage" |
| 5 | 3:02 | P06–P07 | n17–n20 | Geli Raubal arrives; the only deep affair; jealousy and control (Emil Maurice) |
| 6 | 4:20 | P08 | n21–n23 | The 1929 letter, Father Stempfle, and his death in the Night of the Long Knives |
| 7 | 5:12 | P09 | n24–n25 | 17 Sept 1931: "No." — Geli found shot dead; ruled suicide; the murder rumors |
| 8 | 5:49 | P10–P11 | n26–n30 | "The only woman he ever loved"; grief, the vegetarian vow; the failed Hindenburg meeting |
| 9 | 6:54 | P12–P14 | n31–n37 | Eva Braun enters; the hidden twelve-year mistress; Kempka; the Sigrid von Lappus rumor |
| 10 | 8:05 | P15–P16 | n38–n40 | Eva returns to surrounded Berlin; the "ceremony out of a nightmare" and the deaths |
| 11 | 9:00 | P17–P18 | n41–n43 | What his love life reveals + closing subscribe line |

---

## Thumbnails

**Image generation was NOT attempted this run** — the workspace is out of image-generation credits
(per the task). No `generate_image` calls were made. Per the Third Reich packaging research, this niche
should use a single strong, ideally colorized, **real archival photograph depicting the literal
subject**, with little to no baked-in text anyway — so no generation is required to ship a good
thumbnail; the right image is one of the episode's already-sourced stills.

Three A/B directions (all from the episode's existing sourced media — no generation needed):

- **A — FALLBACK, ALREADY ON DISK.** `Third Reich/episodes/ep003-hitler-love-life/thumbnail.jpg` — a
  1920x1080 archival photo of Hitler and Eva Braun in deck chairs (sourced from `keep-a20.jpg`,
  scene n35). A colorization pass was attempted and **failed on credits**, so this stays as the B&W
  fallback A option. Colorize it whenever credits return; it depicts the literal "love life" subject
  and reads clearly at phone size.
- **B — Geli Raubal portrait (RECOMMENDED once available).** A clean portrait crop from the episode's
  Geli section stills (e.g. `22.jpg` / `23.jpg` / `20.jpg`, scenes n15/n19/n21–22). This is the
  strongest curiosity-gap match for the recommended title ("the niece he called his only love") —
  most viewers won't recognize her, which is exactly the World-History-channel "person next to the
  famous person" hook. Colorize; no text or a single accent word.
- **C — The bunker wedding.** The Hitler–Eva marriage document / registrar moment, or a still lifted
  from the wedding footage (`holiday-clean.mp4`, scene n40), or the closing pair `39.jpg`/`40.jpg`
  (scenes n41–42). Visualizes the opening hook (married 40 feet under a burning Berlin, dead within
  two days). Strongest for a "secret wedding" title angle.

Keep all three text-light per the niche research (documentary audiences read heavy overlays as
AI/amateur). If any text is used at all, hold it to a single accent word and keep the thumbnail angle
matched to whichever title you ship.

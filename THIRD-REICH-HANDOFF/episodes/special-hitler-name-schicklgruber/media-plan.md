# special — "Heil Schicklgruber?" (The Name) — MEDIA PLAN

Beat-indexed per the house standard (ep003/ep006): fast-cut, one distinct image or clip per
beat, real historical media only — **no AI art**. This document is the *plan* written before the
sourcing/download pass; the **Status** column shows what I have already verified exists (with the
exact Wikimedia Commons filename) versus what still needs a live sourcing pass.

> ⚠️ **Script provenance — please confirm.** I built these beats from the committed
> `script-rough.md`, **not** from a transcript of the audio. You mentioned you may have edited the
> script after it was written, and I could not transcribe the audio to check: this environment's
> network policy blocks every speech-to-text model host (HuggingFace, Azure, alphacephei all
> return 403/000), and the only fully-offline engine available (pocketsphinx) was far too
> inaccurate to trust — it rendered "Schicklgruber" as "she called group up" and hallucinated
> whole sentences. The recognizable words it *did* catch in the first 40 s (Nuremberg rallies,
> raised arms, mandatory greeting, replacing "hello" on the telephone, Heil Schicklgruber) match
> `script-rough.md`, so the audio broadly follows this script — but if you changed specific lines,
> tell me which beats are affected (or paste the final text / enable HuggingFace so I can Whisper
> it) and I'll re-cut those beats.

## Sourcing rules (same as ep003/ep006)
- **Real historical images/footage only, no AI art.** Public-domain / CC-BY-SA tier: Bundesarchiv
  via Wikimedia Commons, NARA/LOC/USHMM equivalents, Internet Archive PD newsreels.
- **Never fabricate a portrait for a person with no known photo.** Several central figures here —
  **Maria Anna Schicklgruber, Johann Georg Hiedler (the wandering miller), Johann von Nepomuk
  Hüttler** — died in the 1840s–50s, before photography reached the rural Waldviertel. **No
  portrait of any of them exists.** Those beats get an honest period-accurate stand-in (the
  village, the register, a genre "miller/old peasant" image) and are flagged as such below — the
  same rule ep006 used for figures like Reinhold Krause.
- **No death/atrocity imagery.** The one dark-history beat (the Czech "erased from the map"
  footnote, beat 51) uses a sober occupation-of-Prague photo — troops/castle only, no suffering.
- **Nazi insignia incidental, never the hero of the frame.**
- **Deliberate visual callbacks are intentional, not repetition padding:** the opening Nuremberg
  rally (beats 1–2) is reused at the close (beat 54) to land Shirer's full-circle "Heil
  Schicklgruber at Nuremberg?" question; Alois's and Shirer's portraits recur where the narration
  returns to them.

## Creative treatments (house on-screen-text exceptions apply)
- **Beat 4 — "Heil Schicklgruber!" (shouted):** comic **speech-bubble variant** — hold the
  Nuremberg salute crowd, darken part of the frame, place a white comic speech bubble with the
  tail near the podium reading *"Heil Schicklgruber!"* This is the exact case the house style
  carves out for shouted lines. It also visually *is* the episode's thesis, so it earns the
  treatment. (Reprised, optional, at beat 54.)
- **Quote typewriter overlays** for the three direct Shirer/Kubizek quotations (beats 36, 46, 52),
  each paired with a partial-frame portrait, composition varied per the house rule (half-frame /
  corner-photo / etc.).
- **Beat 25 / 46 — the name variants** (Hiedler / Hüttler / Hitler; "Schicklgruber → Hitler"):
  candidate for a short typewriter/strike-through motion treatment rather than a literal photo.
- **Beat 13 / 50 — optional data-viz:** the "shifting names on the paternal side" tangle and the
  Czech-blood family line could be a small hand-drawn-style family-tree motion graphic instead of
  a document photo. Marked opt-in below; I'd prototype it for a go/no-go before wiring it in, per
  house rule — say if you want that.

## Video clips wanted (PD newsreel tier — Internet Archive "Why We Fight" / Universal Newsreels)
| For beats | Clip | Rights note |
|---|---|---|
| 1–2, 43, 54 | Nuremberg rally: sea of raised arms, Hitler at the podium, crowd salute | Source from Frank Capra *Why We Fight* (US War Dept, PD) or Universal Newsreels; verify per-item, preview frames before committing |
| 51 | German troops enter Prague / Hitler at Prague Castle, March 1939 | PD newsreel; sober occupation footage only, no atrocity |
| 2, 22 (opt) | Hitler mid-speech, fiery gesture | PD newsreel, atmosphere |

---

## Beat table

Status legend: **✅ VERIFIED** = exact Commons file confirmed to exist this session · **🔎 TODO** =
needs live sourcing pass · **⚠️ NO PHOTO** = subject has no surviving portrait, stand-in proposed.

| # | Narration anchor | Subject to depict | Recommended source / query | Status |
|---|---|---|---|---|
| 1 | "Picture the Nuremberg rallies. Hundreds of thousands of raised arms" | Sea of raised arms at a Nuremberg rally (wide) | Bundesarchiv Nuremberg rally, `Category:Nuremberg Rallies` on Commons; **clip** preferred | 🔎 TODO (category confirmed) |
| 2 | "one word thundering across the stadium… 'Heil Hitler!'" | Hitler at the Zeppelinfeld podium, crowd beyond | Bundesarchiv Reichsparteitag; **clip** preferred | 🔎 TODO |
| 3 | "mandatory greeting of an entire nation… replacing 'hello' on the telephone" | Ordinary Germans giving the salute in daily life | Bundesarchiv everyday-salute street photo | 🔎 TODO |
| 4 | "Now try the same scene… 'Heil Schicklgruber!' … almost comic" | **Speech-bubble treatment** over the beat-1 crowd | reuse beat 1 image + comic bubble | reuse |
| 5 | "a real question historians have actually asked" | Shirer's *Rise and Fall of the Third Reich* book / historian's desk | Internet Archive book-cover service | 🔎 TODO |
| 6 | "his own father legally carried that exact name" | **Alois Hitler** portrait (customs uniform) | `File:Alois Hitler.jpeg` (Commons, PD) | ✅ VERIFIED |
| 7 | "one bizarre decision, made by an old man, thirteen years before Adolf Hitler was even born" | Old parish register / notary document (foreshadow) | period Austrian register close-up | 🔎 TODO |
| 8 | "The story starts in the Waldviertel… peasant villages in Lower Austria" | Waldviertel rolling landscape | Commons `Category:Waldviertel` (GuentherZ CC-BY) | 🔎 TODO (category confirmed) |
| 9 | "wedged between the Danube and the borders of Bohemia and Moravia" | Period map of Lower Austria / Waldviertel | old map, Commons | 🔎 TODO |
| 10 | "Shirer, who passed through it himself on trips to Prague" | **William L. Shirer** portrait | `File:` in `Category:William L. Shirer` — "Shirer at Compiègne 1940" | ✅ VERIFIED (category) |
| 11 | "the main currents of Austrian life had simply passed by. Intermarriage… illegitimacy" | Old rural Austrian village / peasants, period | Commons period Waldviertel village photo | 🔎 TODO |
| 12 | "Adolf Hitler's family, on both sides, came from exactly this soil" | Strones / Döllersheim old village view | Commons Döllersheim historic | 🔎 TODO |
| 13 | "the paternal side… a mess of shifting names, shifting addresses" | **opt-in family-tree motion graphic**, else period handwritten register | prototype graphic / Commons | 🔎 TODO (opt-in) |
| 14 | "On June 7th, 1837… Maria Anna Schicklgruber gave birth to a son in Strones" | Village of Strones / period peasant mother-and-infant | **⚠️ NO PHOTO of Maria Anna** — use Strones/Döllersheim + honest caption | ⚠️ NO PHOTO |
| 15 | "She named him Alois. She did not name a father on the record." | **Döllersheim baptismal register** — blank father column / "illegitimate" | Commons / matricula-online.eu register scan | 🔎 TODO (record documented) |
| 16 | "a wandering miller named Johann Georg Hiedler" | Period Austrian miller / watermill | **⚠️ NO PHOTO of Hiedler** — genre mill image, flagged | ⚠️ NO PHOTO |
| 17 | "wouldn't actually marry Maria until five years later, in 1842" | Period Austrian village church / marriage register | Commons | 🔎 TODO |
| 18 | "he didn't bother to legitimize his own son… Alois Schicklgruber" | Register held on the name "Schicklgruber" | reuse beat 15 register | reuse |
| 19 | "In 1847, Maria Anna died." | Waldviertel cemetery / period gravestone | Commons Döllersheim graveyard | 🔎 TODO |
| 20 | "the probable father… simply disappeared… For thirty." | Empty road through the Waldviertel (vanishing) | reuse beat 8 landscape, different motion | reuse |
| 21 | "joins the Austrian border police… the customs service" | **Alois** in customs/uniform | reuse `File:Alois Hitler.jpeg` (uniform) | ✅ VERIFIED (reuse) |
| 22 | "marries — not once, but eventually three times" | Period Austrian wedding portrait | Commons genre | 🔎 TODO |
| 23 | "For thirty-nine years, this is simply who he is." | Alois portrait held | reuse beat 6 | reuse |
| 24 | "Then, in 1876, the old miller resurfaces… in the town of Weitra" | **Weitra** town, period view | Commons `Category:Weitra` | 🔎 TODO |
| 25 | "now spelling his own name not Hiedler but Hitler" | The name variants — **typewriter/strike treatment** | motion treatment | 🔎 TODO (treatment) |
| 26 | "walks into a notary's office with three witnesses and formally swears he is the father" | 19th-c Austrian notary / legal act, period | Commons genre document/office | 🔎 TODO |
| 27 | "Why now?… a man in his mid-eighties" | Anonymous elderly Austrian man, period | **⚠️ stand-in** (no Hiedler photo), flagged | ⚠️ NO PHOTO |
| 28 | "Shirer is honest that the record doesn't say for certain" | Shirer / his book | reuse beat 10 or beat 5 | reuse |
| 29 | "biographer Konrad Heiden heard… the real motive… money" | **Konrad Heiden** portrait, else his book *Der Fuehrer* cover | Commons `Category:Konrad Heiden` (portrait uncertain) / IA book cover | 🔎 TODO (⚠️ portrait may not exist — book-cover fallback) |
| 30 | "An inheritance… claiming paternity was the key that unlocked it." | Period coins / Austrian farmhouse (inheritance) | Commons genre | 🔎 TODO |
| 31 | "forwarded to the parish priest at Döllersheim… kept the baptismal register" | **Döllersheim church** (Friedenskirche) | Commons Döllersheim church (GuentherZ CC-BY) | 🔎 TODO (confirmed exists) |
| 32 | "November 23rd, 1876… almost administrative in how small it looks on the page" | Baptismal register book, close-up | Commons / matricula scan | 🔎 TODO |
| 33 | "crossed out 'Alois Schicklgruber'… wrote 'Alois Hitler'" | **The altered register entry** (hero image) | matricula-online.eu Döllersheim register; else period register close-up | 🔎 TODO (⚠️ exact altered entry may be hard to license — flag) |
| 34 | "A signature, a notary, a single stroke of a priest's pen" | Extreme close-up: pen nib on old ledger | Commons genre | 🔎 TODO |
| 35 | "a thirty-nine-year-old man's legal identity changed forever" | Register held on "Alois Hitler" | reuse beat 33 | reuse |
| 36 | *Quote:* "Adolf's father was legally known as Alois Hitler, and the name passed on naturally to his son." | **Shirer quote — typewriter overlay** + Shirer portrait | reuse beat 10 + typewriter | reuse+treatment |
| 37 | "marry his third wife, a young cousin named Klara Pölzl" | **Klara Pölzl** portrait | `File:Klara Hitler.jpg` (Commons, PD Mark) | ✅ VERIFIED |
| 38 | "April 20th, 1889… Braunau am Inn… They named him Adolf." | **Braunau am Inn birth house** | `File:Hitlers Geburtshaus Braunau am Inn.jpg` (c.1934, PD) | ✅ VERIFIED |
| 39 | "born Adolf Hitler only because an eighty-four-year-old miller had walked into a notary's office… everything to do with an inheritance" | Register/notary callback + Braunau | reuse beats 33 + 38 | reuse |
| 40 | "The story didn't stay buried. In the 1930s… journalists in Vienna went digging through the parish archives" | 1930s Vienna / newspaper press / Hitler's rise | Commons Bundesarchiv 1930s | 🔎 TODO |
| 41 | "found the whole tangled history — the illegitimacy, the vanished miller, the late legitimization" | Parish archive / stacked old registers | reuse register imagery | reuse |
| 42 | "Some tried to brand him publicly as 'Adolf Schicklgruber'… It never really stuck." | Real "Schicklgruber" Allied/anti-Nazi leaflet or cartoon | Commons / IA WWII propaganda ("Schicklgruber") | 🔎 TODO |
| 43 | "already built an entire mythology, an entire mass movement, around the name" | Nuremberg rally / Hitler myth | reuse beats 1–2 | reuse |
| 44 | "Hitler himself understood exactly what had been at stake" | Young Hitler, Linz/Vienna era portrait | Commons `Category:Adolf Hitler in the 1900s` | 🔎 TODO |
| 45 | "his only real boyhood friend, August Kubizek, later recorded…" | **August Kubizek** 1907 photo | `File:` in Kubizek Commons (1907 portrait) | ✅ VERIFIED (Commons has 1907 photo) |
| 46 | *Quote:* "'Schicklgruber' uncouth… 'Hiedler' too soft… 'Hitler' sounded nice and was easy to remember" | **Kubizek quote — typewriter overlay** + young Hitler + name variants | reuse beat 44 + typewriter | reuse+treatment |
| 47 | "a name is a kind of branding — his own had come within one old man's whim of being unusable" | Young Hitler held | reuse beat 44 | reuse |
| 48 | "the uncle who actually raised young Alois… Johann von Nepomuk Hüttler" | The name / period document | **⚠️ NO PHOTO of Hüttler** — document stand-in | ⚠️ NO PHOTO |
| 49 | "Saint John of Nepomuk was the national saint of the Czech people" | **Statue of St. John of Nepomuk, Charles Bridge, Prague** | `File:Saint John of Nepomuk statue Charles Bridge Prague.JPG` | ✅ VERIFIED |
| 50 | "a hint of Czech blood somewhere in the family line" | Bohemia/Moravia map or Czech landscape | Commons period map | 🔎 TODO (opt-in tie to beat 13 tree) |
| 51 | "undying contempt… for Czechs, whose nation he would ultimately erase from the map" | **German troops enter Prague / Hitler at Prague Castle, March 1939** (sober) | Commons Bundesarchiv occupation of Prague; **clip** option | 🔎 TODO (documented; no atrocity) |
| 52 | *Quote:* "There are many weird twists of fate… none more odd than this one which took place thirteen years before his birth." | **Shirer quote — typewriter overlay** + Shirer portrait / book | reuse beat 10 / 5 + typewriter | reuse+treatment |
| 53 | "Had the old miller never walked into that notary's office… All of it, under the name Adolf Schicklgruber." | Notary/register callback + rally | reuse beats 33 + 1 | reuse |
| 54 | "Whether several hundred thousand voices could ever have roared that name back at him… at Nuremberg" | **Full-circle Nuremberg callback** (opt. speech-bubble reprise) | reuse beats 1–2 | reuse |
| 55 | "But it's the one Shirer himself couldn't resist asking." | Shirer portrait, final hold | reuse beat 10 | reuse |

## Sourcing risks flagged now (before the download pass)
- **Beats 14, 16, 27, 48 — no surviving portraits.** Maria Anna Schicklgruber, Johann Georg
  Hiedler, and Johann von Nepomuk Hüttler predate rural-Austrian photography; there is nothing to
  find and I will not fabricate one. Stand-ins (the village, a period mill, the register, an
  anonymous period elderly man) will be captioned honestly, exactly as ep006 handled Krause.
- **Beat 33 — the altered register entry** is the episode's single most important "document" image.
  The event is well documented (priest struck "Schicklgruber," entered "Hitler," 23 Nov 1876) and
  the Döllersheim registers are digitized at matricula-online.eu, but a cleanly reusable,
  rights-clear image of *that exact altered page* may not surface — fallback is a faithful period
  register close-up, flagged as representative rather than the literal page.
- **Beat 29 — Konrad Heiden portrait** may not exist on Commons; the strong fallback is the real
  cover of his 1944 biography *Der Fuehrer* via the Internet Archive book-cover service.
- **Döllersheim irony worth a caption (beats 31–33, 51):** the ancestral village and this very
  register's parish were **razed on Hitler's own orders in 1938** to create the Allentsteig
  Wehrmacht training ground — historians link the timing to burying these ancestry rumors. Strong
  optional caption/callback if you want to lean into it; the church survives as a "church of peace."
- **Video rights:** every newsreel clip is "verify per item, not PD by default" — I'll open each
  Internet Archive item's rights statement and preview frames before committing, per the standing
  rule (no fringe/deemphasize collections, confirm PD source).

## Next steps
1. **You review** this beat↔media mapping — adjust any pick, tell me which beats (if any) the
   script edits changed, and approve the creative treatments (speech-bubble beat 4, the two
   opt-in motion graphics).
2. On approval I run the sourcing/download pass into `Media/hitler-name/`, visually verify every
   file, and report the final source list + any substitutions honestly.
3. Then bracket-tag the finalized script, build per-span TTS timing against the existing audio,
   and render in `reich-engine` with the standard Like & Subscribe end card.

# Bible Quiz Video — Page Design System & Google Flow Prompt Pack

Reference video: `https://youtu.be/H37HaHwC8fk`
"The ULTIMATE Bible Quiz — 50 Questions, 3 Rounds (Easy → Hard)" (8:51)

---

## 1. The design system at a glance

The video runs on a **two-world** visual system that alternates on a strict beat:

| World | Used for | Feel |
|---|---|---|
| **Cream world** — warm off-white `#FAF7EE`, black ink line art, ornamental corner frame | Question pages, milestone interstitials, outro | Storybook / illuminated-manuscript / children's Bible primer |
| **Teal world** — flat matte teal `#3B8A88`, pale mint card, no texture | Intro, round transitions, answer reveals | Flat modern quiz-app UI, punchy and clean |

The rhythm is: cream question page (7s timer) → hard cut → teal answer card (2s) → hard cut → next cream question page. Every 6 questions a cream milestone card breaks the loop. That cut between warm/ornamental and cool/flat is the single most important stylistic signature — copy that and you've copied the video.

### Master palette

| Role | Hex |
|---|---|
| Teal background | `#3B8A88` |
| Pale mint card / badge | `#E6F7F5` – `#E2F8F6` |
| Dark forest slate text (on teal) | `#1E3834` / `#112A27` |
| Warm cream canvas | `#FAF7EE` |
| Warm eggshell (outro) | `#FDF8EE` |
| Ink black (line art + body text) | `#1B232A` |
| Royal blue accent (answer badges) | `#2649B2` |
| Ochre / amber accent | `#D97706` |
| Royal navy (outro headings) | `#20366B` |
| YouTube red (CTA) | `#E53E3E` |

### Typography

- **Everything functional is a geometric sans-serif** (Poppins / Montserrat / Inter family look), bold to black weight, centred.
- Small labels are **UPPERCASE with wide letter-spacing** (`SOLO MODE`, `QUESTION 7 OF 50`, `12 OF 50`).
- Question text and answer reveals are **bold title/sentence case**, large scale.
- **Only the outro switches to serif** — bold serif headline plus an italic serif subtitle. That serif is the "we're done, breathe" signal.
- No text outlines, no neon glow, no heavy drop shadows on type. Shadows only on cards, and they're soft (`0 4px 12px rgba(0,0,0,0.08)`).

### The four rotating illustration themes

Question pages and milestone cards share the same frame artwork, cycling through four themes so 50 questions don't feel repetitive:

- **A — Scroll & Quill:** dark navy corner blocks with gold filigree stars, a rolled parchment scroll top-left, a white quill pen with a navy ink pot bottom-right.
- **B — Tablets & Crown:** deep purple-blue archway across the header, two stone tablets in the top corners, a gold royal crown, sparkling gold stars.
- **C — Dove & Olive:** black corner brackets with golden floral leaves, a flying white dove carrying an olive branch top-right, a soft mint-green landscape bar along the bottom.
- **D — Shepherd & Flock:** retro-70s horizontal sunset stripes in terracotta / amber / pale yellow, a hanging shepherd's lantern on a wooden post, silhouetted grazing sheep on a green hill.

### On-screen chrome

- **Top-left:** question counter pill — `QUESTION 7 OF 50`, dark bold uppercase on a light pill.
- **Top-right:** circular dark timer with a radial pie fill that drains green → red over 7 seconds, big numeral in the middle.
- **Answers:** 2×2 grid of white rounded rectangles (`border-radius: 12px`), each with a circular A/B/C/D letter badge on the left in royal blue or amber.
- **Milestones:** a single bottom-centre progress pill — `6 OF 50`, `12 OF 50` …

### Motion

Deliberately minimal. Static locked-off framing, hard cuts between pages, occasional crossfade on the teal slides. The **only** animated element is the radial countdown timer. Nothing slides, bounces, or parallaxes.

---

## 2. How to use these prompts in Google Flow

Flow (Veo) **cannot reliably render long or exact text.** Words come out warped, misspelled, or gibberish. So:

1. Use the **"plate" prompts (B-series)** to generate the *empty decorated frame* — background, corner ornaments, illustrations, blank card shapes. No text in the prompt at all.
2. Bring that plate into Canva / Figma / After Effects / CapCut and **overlay the real question text, answer options, counter pill and timer** as actual type layers. This also means one plate serves all 50 questions.
3. Use the **"full page" prompts (A-series)** only when you want a look-and-feel reference or a thumbnail — expect the text to be nonsense.
4. In Flow, set **16:9**, and keep `Ingredients` empty unless you're locking style across shots — if you are, generate Theme A first and feed it as a reference image so B/C/D inherit the same line weight and palette.

Every prompt ends with the same anti-motion clause, because Veo's instinct is to add camera drift and you want a dead-still page.

---

## 3. The prompts

### A1 — Intro / "How to Play" screen (teal world)

```
A flat 2D graphic design title card, 16:9. Solid matte teal background, hex #3B8A88, completely
flat with no texture, no gradient, no grain. Centred composition with generous 12% margins. In the
upper third, a small flat vector line-art analog clock icon in dark forest green #1E3834. Below it,
a bold geometric sans-serif headline in dark forest slate #1E3834, and beneath that two short lines
of lighter regular-weight sans-serif body text, all centre-aligned in a tight vertical stack. Above
the headline, a tiny uppercase label with wide letter spacing. Minimal editorial vector design,
clean quiz-app aesthetic, high contrast, no photographic elements, no drop shadows.
Static locked-off camera, absolutely no camera movement, no zoom, no pan, no parallax,
the image holds perfectly still.
```

### A2 — Round transition slide (teal world)

```
A flat 2D graphic design slide, 16:9. Solid matte teal background, hex #3B8A88, perfectly flat and
untextured. Dead centre of frame sits a single wide rounded-rectangle pill card in pale mint
#E2F8F6, 24px corner radius, no border, sitting flat with no shadow. Inside the pill, short bold
geometric sans-serif text in deep ink teal #112A27, centred. A small uppercase wide-tracked label
floats above the pill in the same dark teal. Nothing else in frame. Extreme minimalism, flat vector,
modern quiz-show interstitial, generous negative space.
Static locked-off camera, absolutely no camera movement, no zoom, no pan, the image holds
perfectly still.
```

### A3 — Answer reveal card (teal world)

```
A flat 2D graphic design reveal card, 16:9. Solid matte teal background, hex #3B8A88, flat and
untextured. Centred in the frame, one large rounded-rectangle card in soft pale mint #E6F7F5,
16px corner radius, no stroke, with a very subtle elevation shadow. Inside the card, a short bold
heavy-weight geometric sans-serif word in deep ink teal #112A27, large scale, centred. Directly
beneath the card, a smaller semi-bold line of text in slate teal #1E3D38. Punchy minimalist vector
card design, lots of breathing room, no ornament, no icons, no photographic texture.
Static locked-off camera, absolutely no camera movement, the image holds perfectly still.
```

### B1 — Question page PLATE, Theme A: Scroll & Quill (cream world)

```
An empty 2D flat-vector page design template, 16:9, warm cream off-white canvas hex #FAF7EE.
The page is enclosed by a decorative double black stroke border frame with ornamental flourishes at
each corner. The four corners are filled with dark navy blocks decorated with gold filigree and
small gold stars. A rolled parchment scroll illustration sits in the top-left corner and a white
quill pen with a navy ink pot sits in the bottom-right corner, both drawn as clean flat vector
storybook line art with solid fills and no shading. The centre of the page is left completely
EMPTY cream space — no text, no letters, no words, no writing anywhere in the image.
Modern children's Bible storybook illustration style, crisp black ink outlines, warm limited
palette of cream, navy, gold and black, educational quiz layout, print-poster clean.
Static locked-off camera, absolutely no camera movement, no zoom, no pan, the image holds
perfectly still.
```

### B2 — Question page PLATE, Theme B: Tablets & Crown

```
An empty 2D flat-vector page design template, 16:9, warm cream off-white canvas hex #FAF7EE,
enclosed by a decorative double black stroke border with ornate corner flourishes. Across the top
of the page runs a deep purple-blue archway band. Two grey stone tablets of the Ten Commandments
sit in the top corners, and a gold royal crown with sparkling gold stars sits centred in the arch.
The lower two thirds of the page are left completely EMPTY cream space — no text, no letters,
no words, no writing anywhere in the image. Flat 2D vector illustration with solid fills and clean
black outlines, modern children's Bible storybook style, palette of cream, deep purple-blue, gold
and ink black.
Static locked-off camera, absolutely no camera movement, no zoom, no pan, the image holds
perfectly still.
```

### B3 — Question page PLATE, Theme C: Dove & Olive

```
An empty 2D flat-vector page design template, 16:9, warm cream off-white canvas hex #FAF7EE.
Black L-shaped corner brackets decorated with golden floral leaves sit at all four corners. A white
dove in flight carrying a green olive branch is illustrated in the top-right area. A soft mint-green
rolling landscape bar runs along the very bottom edge of the page. The centre of the page is left
completely EMPTY cream space — no text, no letters, no words, no writing anywhere in the image.
Flat 2D vector storybook illustration, clean black ink outlines, solid colour fills, no gradients,
peaceful warm palette of cream, mint green, gold and black.
Static locked-off camera, absolutely no camera movement, no zoom, no pan, the image holds
perfectly still.
```

### B4 — Question page PLATE, Theme D: Shepherd & Flock

```
An empty 2D flat-vector page design template, 16:9. Background is a retro 1970s horizontal striped
sunset in bands of terracotta, burnt amber and pale yellow, flat with no gradient blending, enclosed
by a decorative double black stroke border frame with ornamental corners. On the left, a hanging
shepherd's lantern on a wooden post. Along the bottom, a green rolling hill with silhouetted
grazing sheep. The centre of the page is left completely EMPTY flat cream space #FAF7EE for content
— no text, no letters, no words, no writing anywhere in the image. Retro flat vector poster
illustration, thick clean outlines, warm nostalgic palette, children's Bible storybook aesthetic.
Static locked-off camera, absolutely no camera movement, no zoom, no pan, the image holds
perfectly still.
```

### A4 — Full question page with card slots (look-and-feel reference)

```
A flat 2D vector quiz page design, 16:9, warm cream canvas hex #FAF7EE inside a decorative double
black stroke border with ornamental corner flourishes and small gold star details. Top-left: a
small light rounded pill badge. Top-right: a circular dark navy countdown timer dial with a radial
pie-slice fill draining from green to red and a large numeral in the centre. Upper centre: one wide
white rounded card with a very soft drop shadow, 12px corner radius. Below it, a 2x2 grid of four
identical white rounded rectangle cards with 12px corner radius and a thin light grey border, each
card with a solid circular letter badge on its left edge — two badges royal blue #2649B2, two badges
amber #D97706. Cards are blank inside. Clean educational quiz UI, flat vector, generous even
spacing, storybook Bible illustration framing.
Static locked-off camera, absolutely no camera movement, the image holds perfectly still.
```

### A5 — Milestone / encouragement interstitial

```
A flat 2D vector page design, 16:9, warm cream canvas hex #FAF7EE inside a decorative double black
stroke ornamental border with gold filigree corners and a small Bible-themed illustration in the
upper corners. Dead centre of the page, one single large white rounded card with a soft subtle drop
shadow and 16px corner radius, taking up the middle third of the frame, containing two short lines
of bold dark geometric sans-serif text, centred. At the bottom centre, a small solid amber #D97706
pill badge with short bold uppercase white text. Playful gamified checkpoint screen, flat vector,
warm cream and gold palette, clean and uncluttered.
Static locked-off camera, absolutely no camera movement, the image holds perfectly still.
```

### A6 — Outro / subscribe CTA (serif world)

```
A flat 2D graphic outro card, 16:9. Solid warm eggshell cream background hex #FDF8EE, flat with no
texture. Centred composition. A bold serif headline in classic royal navy #20366B in the upper
middle, with a smaller italic serif subtitle line beneath it in muted navy #28437D. Below the text,
a centred rounded rectangle button in bright red #E53E3E with a white triangular play icon, and
beside it a small floating white circular badge containing a blue thumbs-up icon with a soft drop
shadow. Friendly modern editorial print aesthetic, warm and calm, flat vector, no photographic
elements, generous white space.
Static locked-off camera, absolutely no camera movement, the image holds perfectly still.
```

---

## 4. Assembly notes

- **One plate per theme, reused.** Generate B1–B4 once each at high quality, then drive all 50 questions off those four plates with text layers on top. Rotate themes every ~12 questions or every round.
- **Timer is the only animation.** Build it as a 7-second radial wipe (green → amber → red) in your editor; don't ask Flow for it.
- **Cut, don't transition.** Hard cuts between question and answer. Save crossfades for the teal round-transition slides only.
- **Hold times from the reference:** question 7s, answer reveal ~2s, milestone ~2s, round transition ~1–2s, intro ~10s, outro ~5s.
- **Consistency trick:** generate Theme A first, then attach it as an `Ingredients` reference image when generating B/C/D so line weight, stroke thickness and colour temperature stay identical across all four.

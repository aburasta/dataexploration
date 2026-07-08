# Police-Camera True Crime — Subcategory Taxonomy & Virality Report

*Built 2026-07-08 for a rankings-format YouTube Shorts channel in the Dr Insanity / EWU niche.*

## What's in this folder

| File | What it is |
|---|---|
| `data/moment_bank.csv` | **The "memory"**: 171 verified videos (title + URL + case notes), organized by family → subcategory. Every URL was located via web search — nothing needs to be watched to know what it contains. |
| `taxonomy.json` | 56 subcategories in 10 families, each with regex keyword rules for auto-classifying any video title in this niche. |
| `scripts/classify.py` | Multi-label classifier: point it at any catalog CSV with a `title` column and it applies the taxonomy. Ready for the day full per-video stats become available (VidIQ credits or a local yt-dlp crawl). |

## Method & constraints (honest version)

- The session environment blocks direct YouTube access and VidIQ tool calls were unavailable, so this catalog was built via **web search sweeps** (~31 queries across all taxonomy families) plus channel-level VidIQ data collected earlier in the session.
- **Virality rankings below are therefore tiered judgments, not per-video view math.** They're grounded in: (a) measured channel momentum (e.g. Dr Insanity: 161M views in May–Jul 2026, the fastest in the niche), (b) which formats the fastest-growing channels are built on, and (c) how many competing compilation/ranking videos already exist per subcategory (proof of demand).
- Upgrade path: run `yt-dlp --flat-playlist -J` on the 13 channel URLs from any normal machine, drop the JSON in `data/raw/`, and `classify.py` turns it into a fully quantified catalog.

## The 13 reference channels

EXPLORE WITH US, Dr Insanity, EWU Bodycam, EWU Crime Storytime, Police Insider, Criminally Listed, Stranger Stories, Ape Huncho, Cop Watch, JustThoughtLounge, Law&Crime BodyCam, The Hidden Files, Vigilant Detective.
Momentum signal (views gained May 8–Jul 8 2026): Dr Insanity 161M · EWU Bodycam 95M · EXPLORE WITH US 52M · EWU Crime Storytime 38M · Police Insider 24M · Law&Crime BodyCam 14M · The Hidden Files 7.7M · Stranger Stories 7.3M · JustThoughtLounge 7.3M · Vigilant Detective 7.1M.

## Virality tiers for a *rankings Shorts* channel

### S-Tier — build the channel on these

1. **"The moment they realized they were caught"** (interrogation: lies_unraveling + psychopath_calm + confession_moment). The single strongest format in the niche — it's what Dr Insanity's 161M/2mo is built on. Perfect for Shorts: the realization is a 5–15 second facial-expression payoff. Ranking angles: "5 killers realizing it's over", "criminals' faces when the detective drops the evidence".
2. **Caught-by-DNA / cold case solved decades later** (dna_catch + cold_case_solved). Your instinct was right — this has a built-in ranking axis (*years until caught*: 7 → 24 → 41 → 57), historic anchors (Colin Pitchfork = first ever, Golden State Killer = biggest ever), and constant news refresh. Highly advertiser-safe for a crime format.
3. **Instant karma / messed with the wrong person** (instant_karma + entitled_meltdown). The most Shorts-native arc in existence: setup → arrogance → payoff in under 30 seconds. Endless supply, low gore, high comment-bait ("do you know who I am?" → judge).
4. **Chases with dramatic endings** (pit_maneuver + chase_crash_ending + stolen_vehicle). Pure visual adrenaline, works muted, huge existing compilation demand (multiple "Top 10 PIT" series). Rank by speed, by ending, by audacity (guy steals the police car itself).
5. **Sentencing & judge moments** (sentencing_reaction + judge_moments). Courtroom footage is cheap to license-clear (public record), faces are the content, and "smirk gets wiped off" is a proven loop. Judge Boyd alone is a recurring viral character.

### A-Tier — heavy rotation

6. **Dark discovery cliffhangers** (trunk_discovery + welfare_check + house_of_horrors). Massive curiosity-gap hooks ("police thought it was shoplifting… then they opened the trunk"). Mind the graphic-content line: tease, never show.
7. **Courtroom outbursts & victim confrontations** (courtroom_outburst + victim_confronts). Nassar-dad-level moments are legendary; rank by chaos level.
8. **Fake cops caught by real cops** (fake_cop). Small but *reliably* viral irony engine — "fake cop pulls over the sheriff" is a perfect Short on its own.
9. **Teen/young suspects in interrogation** (young_suspect). The "(He Didn't)" title formula is the niche's most copied for a reason. Slightly higher sensitivity — keep it factual.
10. **K9 takedowns & escape attempts** (k9_takedown + escape_attempt). Visual, fast, satisfying; A&E already proves escape attempts work as Shorts.

### B-Tier — freshness fillers (keep the channel non-repetitive)

11. **Sovereign citizens** (sovereign_citizen) — reliable but saturated; use the twist endings (hidden cocaine, window smash).
12. **DUI stops** (dui_stop) — infinite supply, moderate ceiling; best when stacked with entitlement ("my son is a cop!").
13. **Dumb criminals / funny arrests** (dumb_criminal) — comedy diversifies the emotional palette of the channel.
14. **Killer's own 911 call** (killer_calls_911 + chilling_911) — audio-first; great with waveform + transcript captions.
15. **Kid-hero 911 calls & hero cop rescues** (kid_hero_call + hero_rescue) — the wholesome counterweight; algorithm loves the emotional whiplash and it's maximally advertiser-safe.
16. **Digital-evidence catches** (digital_evidence) — "his Google searches convicted him" (Walshe, Bliefnick) is a strong list format; refreshes with every big trial.
17. **Corrupt cops arrested** (killer_cop) — strong justice-porn appeal; verify case outcomes before publishing claims.

### C-Tier — use sparingly / risk-flagged

18. **Shootouts & officer-down** (shootout, officer_down) — high views but graphic; demonetization and age-restriction risk on Shorts. Use news-style framing if at all.
19. **Online predator stings** (online_predator) — popular but brand-unsafe territory and platform-policy sensitive.
20. **Standoffs/hostage, smell-complaint discoveries** — slower arcs that need more than 60 seconds to land.

## First 20 Shorts (concrete, sourced from moment_bank.csv)

1. 5 Killers Who Were Caught by DNA — Decades Later *(rank by years: 7 → 24 → 41 → 42 → 57)*
2. The First Person Ever Caught by DNA *(Colin Pitchfork single-story)*
3. 5 Moments Killers Realized It Was Over *(psychopath_calm rows)*
4. 3 Suspects Whose Lies Fell Apart in Seconds *(lies_unraveling rows)*
5. Top 5 PIT Maneuvers That Ended Chases Instantly
6. He Stole a POLICE CAR — 3 Dumbest Getaways *(stolen_vehicle rows)*
7. 5 "Do You Know Who I Am?" Meltdowns That Ended in Handcuffs
8. Fake Cop Pulls Over a Real Sheriff — 3 Impersonators Caught in the Act
9. 5 Judges Who Wiped the Smirk Off a Defendant's Face
10. Killers Collapsing at Sentencing — Ranked by Reaction
11. Police Thought It Was Shoplifting… 3 Trunk Discoveries That Changed Everything
12. 4 Welfare Checks That Uncovered the Unthinkable *(tease, don't show)*
13. 5 Courtroom Attacks — When Families Snapped *(Nassar dad as #1)*
14. 3 Killers Whose Google Searches Convicted Them *(Walshe, Gregor, Bliefnick)*
15. Teen Killers Who Thought They Got Away With It *(young_suspect rows)*
16. 5 Craziest K9 Takedowns on Bodycam
17. 3 Inmates Who Almost Escaped the Courtroom
18. The Killer Who Called 911 On Himself — 3 Self-Confessions
19. 4 Kids Who Saved Their Parents With One 911 Call *(wholesome pivot)*
20. Sovereign Citizen Says "Am I Being Detained?" — 5 Times It Ended Badly

## Production notes for the Shorts format

- **Rankings need a countdown visual** (5→1) with a numeric overlay; end #1 with the strongest facial-reaction payoff to maximize rewatch loops.
- **Fair use posture**: this niche runs on transformative commentary — add narration, on-screen analysis, and cut footage tightly. The moment_bank notes column tells you the case name so you can source original agency-released footage (bodycam/court footage is largely public record) rather than re-clipping other creators' edits.
- **Title formulas that dominate the niche**: "The Moment X Realized Y", "X Thinks He Got Away With Murder (He Didn't)", "Cops Thought X… Then Y".
- Sensitive subcategories (young_suspect, online_predator, officer_down): factual tone, no mockery, blur minors — this is both an ethics line and a monetization line.

## Coverage status

40 of 56 taxonomy subcategories currently have verified example URLs in the moment bank. The 16 not yet populated (e.g. foot_chase, motorcycle getaway singles, lawyer_moments, verdict_moment, taser_moment, standoff_hostage, scammer_fraudster, celebrity_arrest, serial-killer-specific singles) have classifier rules ready — extend the bank with the same web-search method, or auto-fill once per-video data is available.

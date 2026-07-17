# reich-engine

Remotion assembler for the Third Reich documentary series: archival video clips
+ still images (Ken Burns) + animated map graphics, narrated per scene, joined
with documentary-grade transitions. Ported the Ken Burns / crossfade patterns
from `forbidden-engine`, tuned calmer for archival documentary footage
(monotonic pan/zoom instead of an oscillating cycle).

## Render

```
npm install
npm run render                 # renders src/active-episode.json -> out.mp4 (or pass an output path)
npm run render -- "C:/path/to/output.mp4"
```

Convention (same as `forbidden-engine`): the assembly stage **overwrites
`src/active-episode.json`** with the real episode spec before each render.
To render a one-off spec without touching that file, use Remotion's built-in
props override instead:

```
npx remotion render src/index.jsx Documentary out.mp4 --props=src/some-other-spec.json
```

## Media layout

```
public/
  media/<mediaDir>/   still images (.jpg/.png/.svg), video clips (.mp4), map JSON files
  audio/<mediaDir>/   per-scene narration mp3s, optional music bed
```

`mediaDir` comes from the spec's `mediaDir` field (falls back to `slug`). In
production this is `Media/<episode-slug>/` from the Third Reich project,
copied or symlinked into `reich-engine/public/media/<mediaDir>/` before render
(and `audio/<mediaDir>/` similarly from the episode's `audio/` folder).

## Episode spec (`active-episode.json`)

```jsonc
{
  "title": "ep001 — ...",
  "slug": "blomberg-fritsch-scandal",
  "mediaDir": "ep001",
  "music": false,                 // or a filename in audio/<mediaDir>/
  "scenes": [
    { "n": 1, "type": "image", "src": "01.jpg", "durationSec": 12.5, "audio": "scene-01.mp3", "motion": "slow-push", "transition": "xfade" },
    { "n": 2, "type": "clip",  "src": "02.mp4", "startTrim": 3.0, "durationSec": 9.0, "audio": "scene-02.mp3", "transition": "cut" },
    { "n": 3, "type": "map",   "src": "03-map.json", "durationSec": 14, "audio": "scene-03.mp3", "transition": "dip-to-black" }
  ]
}
```

- `type`: `"image"` (KenBurnsImage), `"clip"` (ClipScene, video), `"map"` (MapRoute, animated map).
- `durationSec` is authoritative — the assembly stage measures each scene's
  narration mp3 and writes the matching `durationSec` before render.
- `audio` is optional per scene — omit it (or the whole spec has none) for a
  silent scene/test render. **Or**, omit it on a scene that immediately
  follows one that *does* set `audio`: that scene's narration clip keeps
  playing underneath it (and under any further audio-less scenes right
  after it), so one narrated span can be subdivided into extra visual beats
  — more images/clips cut in — without re-cutting or re-timing the
  narration. The audio file and its start time never move; only how many
  silent visual scenes ride underneath it changes.
- `transition` describes how the scene **enters**: `"xfade"` (default, 12-frame
  crossfade — use within a sequence/act), `"dip-to-black"` (20-frame fade
  through black — use between chapters/acts), `"cut"` (no transition).

### Image scenes — `motion` presets (KenBurnsImage / config.js `IMAGE_MOTIONS`)
`slow-push` (default), `slow-pull`, `pan-left`, `pan-right`, `settle`. All are
monotonic across the scene (not a repeating cycle) and capped around 1.15x
zoom, plus a faint idle float — tuned for archival stills, not a Ken-Burns
cliché.

### Clip scenes
`startTrim` (seconds into the source file), `durationSec` (how long to show),
`playbackRate` (optional, default 1 — stretches/compresses the clip via
Remotion's native `OffthreadVideo` playbackRate to exactly fill `durationSec`;
compute as `sourceSecondsUsed / durationSec`, e.g. 0.5 plays at half speed to
stretch a short clip across a long narrated span). Always muted (narration
carries the audio track); a barely-there 1.0→1.04 zoom keeps static shots alive
independent of playbackRate.

### Map scenes
`src` points at a JSON file (in the same `media/<mediaDir>/` folder) shaped:
```jsonc
{
  "mapImage": "map-bg.jpg",              // background image, 1920x1080-ish, covers the frame
  "routes": [
    { "points": [[x,y],[x,y],...],       // pixel coords in 1920x1080 space over mapImage
      "color": "#e63946", "strokeWidth": 6,
      "label": "Ribbentrop → Moscow",
      "startSec": 1, "durSec": 5 }        // when, over the scene, the route draws on
  ],
  "markers": [
    { "x": 960, "y": 400, "label": "Berlin", "appearSec": 0.5, "color": "#f4a300" }
  ]
}
```
Routes draw on with an animated leading arrowhead; markers pulse and fade in
their label at `appearSec`. The map background gets the same subtle Ken Burns
drift as image scenes.

## Verification

`npm run render:test` renders the `TestClip` fixture composition (a synthetic
3s moving-shape clip) to `public/media/test/testclip.mp4` — this stands in for
a real downloaded archival clip so the engine can be exercised end-to-end
before any production media exists. `src/test-spec.json` is a 3-scene spec
(image + clip + map, one of each transition type) used for the engine's own
verification render — copy it over `active-episode.json` and run `npm run
render` to reproduce.

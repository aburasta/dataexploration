# Accra → Kampala — Remotion flight motion graphic

A sharp, cinematic map animation: an aeroplane flies from **Accra, Ghana** to
**Kampala, Uganda** across a fully-in-view map of the African continent.

![preview](out/accra-to-kampala.mp4)

## What's in the shot

- **Accurate map** — real country geometry (Natural Earth via GeoJSON) projected
  with a `d3-geo` Mercator projection fitted to the continent, so borders are
  geographically correct, not hand-drawn.
- **Staggered draw-in** of all 50 mainland countries, with **Ghana** and
  **Uganda** highlighted in amber as origin/destination.
- **Animated flight arc** — a glowing gold→cyan route that draws itself as the
  plane travels, with a faint dotted "full route" underneath.
- **Plane** that follows the arc and banks to the path tangent.
- **City markers** with pulsing rings, connector labels (city + country) and an
  arrival shockwave when the plane lands.
- **Design extras** — animated title block, a stats panel (distance 3,684 km,
  bearing ENE · 098°, ~4h 55m), starfield backdrop, subtle graticule grid and a
  cinematic vignette.

## Second composition — `TroopAdvance` (Paris → Alsace-Lorraine)

A light, warm WWI/WWII-style operations map. A single **cluster** — a 2D tank
leading a block of marching boot-prints — advances *as a group* from Paris to
the Alsace-Lorraine objective on the German border. The group **moves**; it does
not leave an ever-extending trail (only a faint static dashed route + arrow
shows the plan). France sits highlighted among its neighbours for context; the
objective zone is a dashed coral area, and a flag plants on arrival.

- Map: `d3-geo` conic-conformal projection of France (+ neighbours), overseas
  territories clipped out.
- Files: `src/geoFrance.ts` (map + route math), `src/TroopAdvance.tsx` (scene).

```bash
npm run render -- TroopAdvance out/paris-to-alsace.mp4   # or use Studio
```

## Specs

- Both: 1920 × 1080, 30 fps (Accra→Kampala 420 frames ~14 s; TroopAdvance 400 frames ~13 s)

## Use it

```bash
npm install
npm start      # open Remotion Studio to preview / tweak
npm run render # renders to out/accra-to-kampala.mp4
```

## Where to change things

| Want to change… | File |
| --- | --- |
| Cities, coordinates, projection, arc math | `src/geo.ts` |
| Colours, timeline, layout, overlays | `src/AccraToKampala.tsx` |
| Duration / fps / dimensions | `src/Root.tsx` |
| Country geometry | `src/data/africa.json` |

Swapping the route is as easy as editing the `CITIES` coordinates in
`src/geo.ts`; everything (arc, markers, highlights) keys off them.

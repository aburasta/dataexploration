import { geoMercator, geoPath, geoGraticule10, geoInterpolate } from "d3-geo";
import type { GeoPermissibleObjects } from "d3-geo";
import africaRaw from "./data/africa.json";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const africa = africaRaw as any;

export const VIDEO_WIDTH = 1920;
export const VIDEO_HEIGHT = 1080;

// ---- 3D tabletop tilt --------------------------------------------------
// The map SVG is tilted with CSS `perspective(P) rotateX(TILT)` about its
// centre. `project3d` replicates that exact transform in JS so the upright
// pin overlay can be positioned to land on the tilted surface.
export const TILT_DEG = 52;
export const PERSPECTIVE = 1500;

export function project3d(
  x: number,
  y: number,
): { x: number; y: number; scale: number } {
  const cx = VIDEO_WIDTH / 2;
  const cy = VIDEO_HEIGHT / 2;
  const a = (TILT_DEG * Math.PI) / 180;
  const u = x - cx;
  const v = y - cy;
  const yr = v * Math.cos(a); // rotateX: y' = y·cos
  const zr = v * Math.sin(a); // rotateX: z' = y·sin (bottom comes forward)
  const scale = PERSPECTIVE / (PERSPECTIVE - zr);
  return { x: cx + u * scale, y: cy + yr * scale, scale };
}

// Box the continent is fitted into (leaves room for titles / labels).
const FIT: [[number, number], [number, number]] = [
  [220, 120],
  [1700, 1010],
];

export const projection = geoMercator().fitExtent(FIT, africa);
export const pathGen = geoPath(projection);

export type LonLat = [number, number];

export const CITIES = {
  accra: {
    name: "ACCRA",
    country: "GHANA",
    lonlat: [-0.187, 5.6037] as LonLat,
  },
  kampala: {
    name: "KAMPALA",
    country: "UGANDA",
    lonlat: [32.5825, 0.3476] as LonLat,
  },
};

export const project = (ll: LonLat): [number, number] => {
  const p = projection(ll);
  return p ? [p[0], p[1]] : [0, 0];
};

export const ACCRA_XY = project(CITIES.accra.lonlat);
export const KAMPALA_XY = project(CITIES.kampala.lonlat);

// Country outlines as SVG path strings (one per feature) so we can stagger them.
export const COUNTRY_PATHS: { id: string; d: string }[] = africa.features
  .map((f: GeoPermissibleObjects & { id: string }) => ({
    id: (f as unknown as { id: string }).id,
    d: pathGen(f) ?? "",
  }))
  .filter((c: { d: string }) => c.d.length > 0);

// Continent silhouette (merged) for the drop shadow / glow base.
export const CONTINENT_PATH = pathGen(africa) ?? "";

// Graticule (lat/long grid) for a cartographic feel.
export const GRATICULE_PATH = pathGen(geograticuleClipped()) ?? "";

function geograticuleClipped() {
  // Restrict the grid roughly to the African bounding box so lines don't
  // sprawl across the whole world.
  return geoGraticule10();
}

/**
 * A stylised flight arc between two projected points: a quadratic Bézier that
 * bows away from the continent's interior so it reads as an air route rather
 * than a straight ruler line. Also exposes helpers to place / orient a plane.
 */
export function buildArc(a: [number, number], b: [number, number]) {
  const mx = (a[0] + b[0]) / 2;
  const my = (a[1] + b[1]) / 2;
  const dx = b[0] - a[0];
  const dy = b[1] - a[1];
  const dist = Math.hypot(dx, dy);
  // Perpendicular offset (bow upward / outward). Scale with distance.
  const bow = dist * 0.28;
  // Normal pointing "up" on screen (negative y) biased.
  let nx = -dy / dist;
  let ny = dx / dist;
  if (ny > 0) {
    nx = -nx;
    ny = -ny;
  }
  const cx = mx + nx * bow;
  const cy = my + ny * bow;
  return { a, b, control: [cx, cy] as [number, number], dist };
}

export function bezierPoint(
  arc: ReturnType<typeof buildArc>,
  t: number,
): [number, number] {
  const { a, b, control } = arc;
  const mt = 1 - t;
  const x = mt * mt * a[0] + 2 * mt * t * control[0] + t * t * b[0];
  const y = mt * mt * a[1] + 2 * mt * t * control[1] + t * t * b[1];
  return [x, y];
}

export function bezierAngle(
  arc: ReturnType<typeof buildArc>,
  t: number,
): number {
  const { a, b, control } = arc;
  // Derivative of quadratic Bézier.
  const dx =
    2 * (1 - t) * (control[0] - a[0]) + 2 * t * (b[0] - control[0]);
  const dy =
    2 * (1 - t) * (control[1] - a[1]) + 2 * t * (b[1] - control[1]);
  return (Math.atan2(dy, dx) * 180) / Math.PI;
}

export function bezierPathD(arc: ReturnType<typeof buildArc>): string {
  return `M ${arc.a[0]} ${arc.a[1]} Q ${arc.control[0]} ${arc.control[1]} ${arc.b[0]} ${arc.b[1]}`;
}

// Great-circle midpoints (unused in render but handy for accurate routes).
export const greatCircle = (a: LonLat, b: LonLat, n = 64): [number, number][] => {
  const interp = geoInterpolate(a, b);
  return Array.from({ length: n + 1 }, (_, i) => project(interp(i / n) as LonLat));
};

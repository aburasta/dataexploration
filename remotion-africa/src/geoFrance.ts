import { geoConicConformal, geoPath } from "d3-geo";
import type { GeoPermissibleObjects } from "d3-geo";
import franceRaw from "./data/france.json";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const fc = franceRaw as any;

export const FR_WIDTH = 1920;
export const FR_HEIGHT = 1080;

// France-centred conic conformal projection, fitted to metropolitan France.
const FRANCE = fc.features.find((f: { id: string }) => f.id === "FRA");
const NEIGHBOURS = fc.features.filter((f: { id: string }) => f.id !== "FRA");

const FIT: [[number, number], [number, number]] = [
  [560, 210],
  [1470, 940],
];

export const projection = geoConicConformal()
  .parallels([44, 49])
  .rotate([-3, 0])
  .fitExtent(FIT, FRANCE);

export const pathGen = geoPath(projection);

export type LonLat = [number, number];
export const project = (ll: LonLat): [number, number] => {
  const p = projection(ll);
  return p ? [p[0], p[1]] : [0, 0];
};

export const FRANCE_PATH = pathGen(FRANCE) ?? "";
export const NEIGHBOUR_PATHS: { id: string; d: string }[] = NEIGHBOURS.map(
  (f: GeoPermissibleObjects & { id: string }) => ({
    id: (f as unknown as { id: string }).id,
    d: pathGen(f) ?? "",
  }),
).filter((c: { d: string }) => c.d.length > 0);

// Approximate outline of Alsace-Lorraine (1871–1918 Reichsland), lon/lat.
const ALSACE_LORRAINE_LL: LonLat[] = [
  [5.62, 49.46],
  [6.9, 49.2],
  [8.1, 49.0],
  [8.2, 48.5],
  [7.6, 47.95],
  [7.35, 47.45],
  [6.45, 47.85],
  [5.9, 48.65],
  [5.62, 49.46],
];
export const ALSACE_PATH =
  "M " +
  ALSACE_LORRAINE_LL.map((ll) => project(ll).join(" ")).join(" L ") +
  " Z";

// Key points
export const PARIS: LonLat = [2.3522, 48.8566];
export const STRASBOURG: LonLat = [7.7521, 48.5734];
export const AL_LABEL: LonLat = [6.9, 48.9];

export const PARIS_XY = project(PARIS);
export const DEST_XY = project([7.1, 48.7]); // inside the region
export const AL_LABEL_XY = project(AL_LABEL);

// Gentle marching route (quadratic Bézier) between two projected points.
export function buildRoute(a: [number, number], b: [number, number]) {
  const mx = (a[0] + b[0]) / 2;
  const my = (a[1] + b[1]) / 2;
  const dx = b[0] - a[0];
  const dy = b[1] - a[1];
  const dist = Math.hypot(dx, dy) || 1;
  const bow = dist * 0.12;
  let nx = -dy / dist;
  let ny = dx / dist;
  if (ny > 0) {
    nx = -nx;
    ny = -ny;
  }
  return {
    a,
    b,
    control: [mx + nx * bow, my + ny * bow] as [number, number],
    dist,
  };
}
export function routePoint(
  r: ReturnType<typeof buildRoute>,
  t: number,
): [number, number] {
  const mt = 1 - t;
  return [
    mt * mt * r.a[0] + 2 * mt * t * r.control[0] + t * t * r.b[0],
    mt * mt * r.a[1] + 2 * mt * t * r.control[1] + t * t * r.b[1],
  ];
}
export function routeAngle(
  r: ReturnType<typeof buildRoute>,
  t: number,
): number {
  const dx = 2 * (1 - t) * (r.control[0] - r.a[0]) + 2 * t * (r.b[0] - r.control[0]);
  const dy = 2 * (1 - t) * (r.control[1] - r.a[1]) + 2 * t * (r.b[1] - r.control[1]);
  return (Math.atan2(dy, dx) * 180) / Math.PI;
}
export function routePathD(r: ReturnType<typeof buildRoute>): string {
  return `M ${r.a[0]} ${r.a[1]} Q ${r.control[0]} ${r.control[1]} ${r.b[0]} ${r.b[1]}`;
}

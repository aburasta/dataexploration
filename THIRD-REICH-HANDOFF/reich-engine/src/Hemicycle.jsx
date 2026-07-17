import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { SANS } from "./config";

// ── Parliament hemicycle dot chart ────────────────────────────────────────────
// Reusable data-viz scene: lays `total` dots out in concentric semicircular
// rows (classic "parliament diagram" layout) and colors them in contiguous
// left-to-right blocks per `segments`. Works for three modes just by shaping
// `segments` differently at the spec level:
//   - seats:      [{count: 12, color: "#c0392b", label: "NSDAP"}, {count: 488, color: "#4a4a4a"}]
//   - vote-share: [{count: 37, color:"#c0392b"}, {count: 53, color:"#4a6fa5"}, {count: 10, color:"#4a4a4a"}]
//   - yes/no:     [{count: 441, color:"#4a6fa5", label:"Ja"}, {count: 84, color:"#c0392b", label:"Nein"}]
// Deliberately text-free by default (no labels rendered) to match the
// no-on-screen-text rule — pass `showLabels` only if the user wants an
// exception for this graphic specifically.

function computeLayout(total, innerR, outerR, rowGap) {
  const rows = Math.max(1, Math.round((outerR - innerR) / rowGap) + 1);
  const radii =
    rows === 1
      ? [outerR]
      : Array.from({ length: rows }, (_, i) => innerR + i * ((outerR - innerR) / (rows - 1)));

  const sumR = radii.reduce((a, r) => a + r, 0);
  const counts = radii.map((r) => Math.max(1, Math.round((r / sumR) * total)));

  // Reconcile rounding so counts sum exactly to `total` (adjust outer rows first).
  let diff = total - counts.reduce((a, b) => a + b, 0);
  let guard = 0;
  while (diff !== 0 && guard < 10000) {
    const idx = diff > 0 ? counts.length - 1 : counts.findIndex((c) => c > 1);
    if (idx < 0) break;
    counts[idx] += diff > 0 ? 1 : -1;
    diff += diff > 0 ? -1 : 1;
    guard++;
  }

  const points = [];
  radii.forEach((r, i) => {
    const n = counts[i];
    for (let j = 0; j < n; j++) {
      const t = n === 1 ? 0.5 : j / (n - 1);
      const angle = Math.PI - t * Math.PI; // sweep left (π) → right (0), over the top
      points.push({ x: Math.cos(angle) * r, y: -Math.sin(angle) * r, angle });
    }
  });

  // Left-to-right reading order for contiguous color-block assignment.
  points.sort((a, b) => a.x - b.x);
  return points;
}

export function Hemicycle({ scene = {}, durationInFrames }) {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const total = scene.total || (scene.segments || []).reduce((a, s) => a + s.count, 0) || 1;
  const innerR = scene.innerR || 110;
  const outerR = scene.outerR || 460;
  const rowGap = scene.rowGap || 42;

  const points = computeLayout(total, innerR, outerR, rowGap);

  // Assign each point a color from the contiguous segment blocks.
  const segments = scene.segments && scene.segments.length ? scene.segments : [{ count: total, color: "#c0392b" }];
  const colored = [];
  let cursor = 0;
  segments.forEach((seg) => {
    for (let k = 0; k < seg.count && cursor < points.length; k++, cursor++) {
      colored.push({ ...points[cursor], color: seg.color, label: seg.label });
    }
  });

  const dotR = Math.max(3, Math.min(9, (outerR - innerR) / 14));
  const cx = width / 2;
  const cy = height * 0.72; // baseline near the lower third, arc opens upward

  // Sweeping reveal: dots pop in left→right in step with their x position,
  // not a flat fade — this reads as a deliberate "count filling in," which
  // suits an election-result beat better than everything appearing at once.
  const sweepFrames = Math.min(durationInFrames * 0.6, 46);
  const minX = Math.min(...points.map((p) => p.x));
  const maxX = Math.max(...points.map((p) => p.x));
  const spanX = Math.max(1, maxX - minX);

  return (
    <AbsoluteFill style={{ background: "#0c0c0c" }}>
      <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} style={{ position: "absolute", inset: 0 }}>
        {colored.map((p, i) => {
          const xt = (p.x - minX) / spanX;
          const startFrame = xt * sweepFrames * 0.7;
          const scale = interpolate(frame, [startFrame, startFrame + 10], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.out(Easing.back(1.5)),
          });
          return (
            <circle
              key={i}
              cx={cx + p.x}
              cy={cy + p.y}
              r={dotR * scale}
              fill={p.color}
            />
          );
        })}
      </svg>
      {scene.showLabels ? (
        <div
          style={{
            position: "absolute",
            bottom: 60,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            gap: 48,
            opacity: interpolate(frame, [sweepFrames, sweepFrames + 20], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          {segments.map((seg, i) =>
            seg.label ? (
              <div key={i} style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: seg.color }}>
                {seg.label}: {seg.count}
              </div>
            ) : null
          )}
        </div>
      ) : null}
    </AbsoluteFill>
  );
}

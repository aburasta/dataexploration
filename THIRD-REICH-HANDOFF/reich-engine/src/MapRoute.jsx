import { useEffect, useState } from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender, cancelRender } from "remotion";
import { imageMotion } from "./config";

const VB_W = 1920;
const VB_H = 1080;

function dist(a, b) {
  return Math.hypot(b[0] - a[0], b[1] - a[1]);
}

// Cumulative arc-length table for a polyline: [{ atLen, point, segLen, dir }]
function buildArcTable(points) {
  let acc = 0;
  const table = [{ atLen: 0, point: points[0] }];
  for (let i = 1; i < points.length; i++) {
    const segLen = dist(points[i - 1], points[i]);
    acc += segLen;
    table.push({ atLen: acc, point: points[i], segLen });
  }
  return { table, total: acc };
}

// Point (and heading angle in degrees) at a given arc-length along the polyline.
function pointAtLength(points, table, len) {
  if (len <= 0) return { pt: points[0], angle: 0 };
  const last = table[table.length - 1];
  if (len >= last.atLen) {
    const a = points[points.length - 2] || points[0];
    const b = points[points.length - 1];
    const angle = (Math.atan2(b[1] - a[1], b[0] - a[0]) * 180) / Math.PI;
    return { pt: b, angle };
  }
  for (let i = 1; i < table.length; i++) {
    if (len <= table[i].atLen) {
      const a = table[i - 1];
      const b = table[i];
      const segLen = b.segLen || 1;
      const t = (len - a.atLen) / segLen;
      const pt = [a.point[0] + (b.point[0] - a.point[0]) * t, a.point[1] + (b.point[1] - a.point[1]) * t];
      const angle = (Math.atan2(b.point[1] - a.point[1], b.point[0] - a.point[0]) * 180) / Math.PI;
      return { pt, angle };
    }
  }
  return { pt: points[points.length - 1], angle: 0 };
}

function easeInOut(t) {
  return t * t * (3 - 2 * t);
}

function Route({ route, secondsElapsed }) {
  const points = route.points;
  if (!points || points.length < 2) return null;
  const { table, total } = buildArcTable(points);
  const startSec = route.startSec || 0;
  const durSec = route.durSec || 4;
  const rawT = Math.min(1, Math.max(0, (secondsElapsed - startSec) / durSec));
  const t = easeInOut(rawT);
  const drawnLen = total * t;

  const d = "M " + points.map((p) => `${p[0]},${p[1]}`).join(" L ");
  const dashOffset = total - drawnLen;
  const { pt: tip, angle } = pointAtLength(points, table, drawnLen);
  const showArrow = rawT > 0.02 && rawT < 1;

  return (
    <>
      <path
        d={d}
        stroke={route.color || "#e63946"}
        strokeWidth={route.strokeWidth || 6}
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={total}
        strokeDashoffset={dashOffset}
      />
      {showArrow ? (
        <polygon
          points="0,-11 24,0 0,11"
          fill={route.color || "#e63946"}
          transform={`translate(${tip[0]}, ${tip[1]}) rotate(${angle})`}
        />
      ) : null}
      {route.label ? (
        <text
          x={points[points.length - 1][0] + 18}
          y={points[points.length - 1][1] - 18}
          fill="#f4f1ea"
          fontSize={26}
          fontFamily="'Inter', 'Segoe UI', Arial, sans-serif"
          fontWeight={600}
          opacity={rawT > 0.15 ? Math.min(1, (rawT - 0.15) / 0.2) : 0}
          style={{ textShadow: "0 2px 6px rgba(0,0,0,0.8)" }}
        >
          {route.label}
        </text>
      ) : null}
    </>
  );
}

function Marker({ marker, secondsElapsed, fps }) {
  const appearSec = marker.appearSec || 0;
  const sinceAppear = secondsElapsed - appearSec;
  if (sinceAppear < 0) return null;
  const fadeIn = Math.min(1, sinceAppear / 0.5);
  const pulse = 1 + Math.sin(sinceAppear * fps * 0.05) * 0.08;

  return (
    <g opacity={fadeIn}>
      <circle cx={marker.x} cy={marker.y} r={9 * pulse} fill={marker.color || "#f4a300"} stroke="#1a1a1a" strokeWidth={2} />
      {marker.label ? (
        <text
          x={marker.x + 16}
          y={marker.y + 8}
          fill="#f4f1ea"
          fontSize={28}
          fontFamily="'Inter', 'Segoe UI', Arial, sans-serif"
          fontWeight={700}
          style={{ textShadow: "0 2px 6px rgba(0,0,0,0.85)" }}
        >
          {marker.label}
        </text>
      ) : null}
    </g>
  );
}

// ── Animated map scene ────────────────────────────────────────────────────────
// scene.src points at a JSON file (in the episode's media dir) shaped like:
// { mapImage, routes: [{points,color,strokeWidth,label,startSec,durSec}], markers: [{x,y,label,appearSec}] }
// Coordinates are pixels in 1920x1080 space over the map image. The JSON is
// fetched at render time (standard Remotion delayRender/continueRender pattern)
// since the filename isn't known until the episode spec is loaded.
export function MapRoute({ scene = {}, mediaDir, durationInFrames }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const secondsElapsed = frame / fps;
  const [mapSpec, setMapSpec] = useState(null);

  useEffect(() => {
    if (!scene.src) return;
    const handle = delayRender(`loading map spec ${scene.src}`);
    fetch(staticFile(`media/${mediaDir}/${scene.src}`))
      .then((res) => res.json())
      .then((json) => {
        setMapSpec(json);
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scene.src, mediaDir]);

  if (!mapSpec) {
    return (
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", background: "#111" }}>
        <div style={{ color: "#889", fontSize: 34, fontFamily: "sans-serif" }}>
          [ missing map spec: {scene.src || `scene ${scene.n}`} ]
        </div>
      </AbsoluteFill>
    );
  }

  const bgSrc = mapSpec.mapImage ? staticFile(`media/${mediaDir}/${mapSpec.mapImage}`) : null;
  const { transform } = imageMotion(frame, "slow-push", durationInFrames);

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#0c0c0c" }}>
      {bgSrc ? (
        <AbsoluteFill style={{ transform, transformOrigin: "center center" }}>
          <Img src={bgSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </AbsoluteFill>
      ) : null}
      <svg
        viewBox={`0 0 ${VB_W} ${VB_H}`}
        width="100%"
        height="100%"
        style={{ position: "absolute", top: 0, left: 0 }}
      >
        {(mapSpec.routes || []).map((route, i) => (
          <Route key={i} route={route} secondsElapsed={secondsElapsed} />
        ))}
        {(mapSpec.markers || []).map((marker, i) => (
          <Marker key={i} marker={marker} secondsElapsed={secondsElapsed} fps={fps} />
        ))}
      </svg>
    </AbsoluteFill>
  );
}

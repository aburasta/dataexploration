import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";
import {
  FR_WIDTH,
  FR_HEIGHT,
  FRANCE_PATH,
  NEIGHBOUR_PATHS,
  ALSACE_PATH,
  PARIS_XY,
  DEST_XY,
  AL_LABEL_XY,
  buildRoute,
  routePoint,
  routeAngle,
  routePathD,
} from "./geoFrance";

// --- Light warm palette (matches the Africa piece) ------------------------
const CORAL = "#d9694a"; // objective / advancing force
const TEAL = "#1f9e8f"; // origin
const INK = "#3a4551";
const SUBINK = "#8a97a3";
const LAND = "#f4eee2"; // France
const LAND_N = "#eae3d5"; // neighbours
const EDGE = "#d3c4ac";
const OLIVE = "#8f8a5f"; // tank body
const OLIVE_DK = "#6b6642"; // tank tracks
const BOOT = "#7c6a57"; // footprints

const ROUTE = buildRoute(PARIS_XY, DEST_XY);
const ROUTE_D = routePathD(ROUTE);

const DEPART = 110;
const ARRIVE = 320;

const ease = (from: number, to: number, f: number, a: number, b: number) =>
  interpolate(f, [a, b], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });

// ---------------------------------------------------------------------------
export const TroopAdvance: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const t = interpolate(frame, [DEPART, ARRIVE], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.5, 0, 0.5, 1),
  });
  const marching = frame >= DEPART - 4;
  const pos = routePoint(ROUTE, t);
  const ang = routeAngle(ROUTE, t);

  const arrival = spring({
    frame: frame - ARRIVE,
    fps,
    config: { damping: 13, mass: 0.8 },
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#eef3f4" }}>
      <Backdrop />

      <svg
        width={FR_WIDTH}
        height={FR_HEIGHT}
        viewBox={`0 0 ${FR_WIDTH} ${FR_HEIGHT}`}
        style={{ position: "absolute", inset: 0 }}
      >
        <Defs />

        {/* Neighbours (context) */}
        <g opacity={ease(0, 1, frame, 8, 46)}>
          {NEIGHBOUR_PATHS.map((c) => (
            <path key={c.id} d={c.d} fill={LAND_N} stroke={EDGE} strokeWidth={0.9} strokeLinejoin="round" />
          ))}
        </g>

        {/* France */}
        <path
          d={FRANCE_PATH}
          fill={LAND}
          stroke="#c3b193"
          strokeWidth={1.6}
          strokeLinejoin="round"
          opacity={ease(0, 1, frame, 14, 54)}
        />

        {/* Alsace-Lorraine objective zone */}
        <g opacity={ease(0, 1, frame, 60, 92)}>
          <path
            d={ALSACE_PATH}
            fill="url(#objFill)"
            stroke={CORAL}
            strokeWidth={2}
            strokeDasharray="7 5"
            strokeLinejoin="round"
          />
        </g>

        {/* Planned route (static dashed line + arrowhead) */}
        <RouteLine frame={frame} />

        {/* Origin marker: Paris */}
        <CityDot xy={PARIS_XY} label="PARIS" appear={70} frame={frame} fps={fps} side="left" accent={TEAL} />

        {/* Objective label */}
        <ObjectiveLabel xy={AL_LABEL_XY} appear={84} frame={frame} arrival={arrival} />

        {/* The advancing group — a single cluster that MOVES (no trail) */}
        {marching && <Squad x={pos[0]} y={pos[1]} angle={ang} frame={frame} t={t} />}
      </svg>

      <TitleBlock frame={frame} />
      <OpsChip frame={frame} arrival={arrival} />
      <Vignette />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Defs: React.FC = () => (
  <defs>
    <radialGradient id="objFill" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stopColor="#f0b89c" stopOpacity="0.85" />
      <stop offset="100%" stopColor="#eec3ac" stopOpacity="0.45" />
    </radialGradient>
    <filter id="softSh" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="3" stdDeviation="3" floodColor="#7a6a55" floodOpacity="0.35" />
    </filter>
  </defs>
);

// ---------------------------------------------------------------------------
const RouteLine: React.FC<{ frame: number }> = ({ frame }) => {
  const op = ease(0, 0.6, frame, 92, 120);
  const [ax, ay] = ROUTE.b;
  const a = routeAngle(ROUTE, 1) * (Math.PI / 180);
  // arrowhead at destination
  const s = 16;
  const p1 = [ax - s * Math.cos(a - 0.5), ay - s * Math.sin(a - 0.5)];
  const p2 = [ax - s * Math.cos(a + 0.5), ay - s * Math.sin(a + 0.5)];
  return (
    <g opacity={op}>
      <path d={ROUTE_D} fill="none" stroke={CORAL} strokeWidth={2.4} strokeDasharray="2 10" strokeLinecap="round" />
      <path d={`M ${ax} ${ay} L ${p1[0]} ${p1[1]} M ${ax} ${ay} L ${p2[0]} ${p2[1]}`} stroke={CORAL} strokeWidth={2.4} strokeLinecap="round" fill="none" />
    </g>
  );
};

// ---------------------------------------------------------------------------
// A footprint = ball + heel (points "up" / forward in local space)
const Footprint: React.FC<{ x: number; y: number; rot: number; op: number }> = ({ x, y, rot, op }) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={op}>
    <ellipse cx={0} cy={-4} rx={4.6} ry={6.4} fill={BOOT} />
    <ellipse cx={0} cy={7} rx={3.6} ry={4.4} fill={BOOT} />
  </g>
);

// formation offsets in local space (forward = up / -y). Behind the tank (+y).
const FEET: { x: number; y: number; rot: number; phase: number; foot: number }[] = [
  { x: -24, y: 40, rot: -6, phase: 0.0, foot: 0 },
  { x: -8, y: 52, rot: 5, phase: 0.5, foot: 1 },
  { x: 10, y: 40, rot: -4, phase: 0.2, foot: 0 },
  { x: 26, y: 54, rot: 7, phase: 0.7, foot: 1 },
  { x: -26, y: 74, rot: -5, phase: 0.9, foot: 0 },
  { x: -8, y: 86, rot: 4, phase: 0.35, foot: 1 },
  { x: 10, y: 74, rot: -6, phase: 0.6, foot: 0 },
  { x: 26, y: 88, rot: 6, phase: 0.15, foot: 1 },
  { x: -16, y: 104, rot: -4, phase: 0.8, foot: 0 },
  { x: 16, y: 106, rot: 5, phase: 0.45, foot: 1 },
];

const Tank: React.FC = () => (
  <g filter="url(#softSh)">
    {/* tracks */}
    <rect x={-24} y={-26} width={11} height={52} rx={4} fill={OLIVE_DK} />
    <rect x={13} y={-26} width={11} height={52} rx={4} fill={OLIVE_DK} />
    {/* track treads */}
    {Array.from({ length: 7 }, (_, i) => (
      <React.Fragment key={i}>
        <rect x={-24} y={-24 + i * 7.2} width={11} height={2} fill="#4f4a30" opacity={0.6} />
        <rect x={13} y={-24 + i * 7.2} width={11} height={2} fill="#4f4a30" opacity={0.6} />
      </React.Fragment>
    ))}
    {/* hull */}
    <rect x={-14} y={-24} width={28} height={48} rx={6} fill={OLIVE} stroke="#726d47" strokeWidth={1.5} />
    {/* turret */}
    <circle cx={0} cy={-2} r={12} fill="#9a945f" stroke="#726d47" strokeWidth={1.5} />
    {/* barrel (points forward / up) */}
    <rect x={-3} y={-40} width={6} height={34} rx={2.5} fill="#847e52" stroke="#6b6642" strokeWidth={1} />
    {/* hatch */}
    <circle cx={0} cy={-2} r={4.5} fill="#726d47" />
  </g>
);

const Squad: React.FC<{ x: number; y: number; angle: number; frame: number; t: number }> = ({ x, y, angle, frame, t }) => {
  const appear = ease(0, 1, frame, DEPART - 4, DEPART + 12);
  const bob = Math.sin(frame * 0.5) * 1.6;
  const scale = 1.15;
  return (
    <g transform={`translate(${x} ${y})`} opacity={appear}>
      {/* rotate whole cluster to travel heading (icons drawn pointing up) */}
      <g transform={`rotate(${angle + 90}) translate(0 ${bob}) scale(${scale})`}>
        {FEET.map((f, i) => {
          const march = 0.55 + 0.45 * (0.5 + 0.5 * Math.sin(frame * 0.55 + f.phase * Math.PI * 2));
          return <Footprint key={i} x={f.x} y={f.y} rot={f.rot} op={march} />;
        })}
        <Tank />
      </g>
    </g>
  );
};

// ---------------------------------------------------------------------------
const CityDot: React.FC<{
  xy: [number, number];
  label: string;
  appear: number;
  frame: number;
  fps: number;
  side: "left" | "right";
  accent: string;
}> = ({ xy, label, appear, frame, fps, side, accent }) => {
  const s = spring({ frame: frame - appear, fps, config: { damping: 13, mass: 0.6 } });
  const op = ease(0, 1, frame, appear, appear + 16);
  const [x, y] = xy;
  const dir = side === "left" ? -1 : 1;
  const anchor = side === "left" ? "end" : "start";
  const pulseT = ((frame - appear) % 55) / 55;
  const pr = interpolate(pulseT, [0, 1], [6, 22]);
  const po = interpolate(pulseT, [0, 1], [0.5, 0]);
  return (
    <g opacity={op}>
      <circle cx={x} cy={y} r={pr} fill="none" stroke={accent} strokeWidth={1.6} opacity={po} />
      <line x1={x} y1={y} x2={x + dir * 16} y2={y - 26} stroke={accent} strokeWidth={1.3} opacity={0.7} />
      <text
        x={x + dir * 22}
        y={y - 30}
        fill={INK}
        stroke="#fff"
        strokeWidth={4}
        paintOrder="stroke"
        fontSize={28}
        fontWeight={800}
        fontFamily="Arial, sans-serif"
        letterSpacing={2}
        textAnchor={anchor}
      >
        {label}
      </text>
      <circle cx={x} cy={y} r={7 * s} fill={accent} />
      <circle cx={x} cy={y} r={3 * s} fill="#fff" />
    </g>
  );
};

const ObjectiveLabel: React.FC<{ xy: [number, number]; appear: number; frame: number; arrival: number }> = ({ xy, appear, frame, arrival }) => {
  const op = ease(0, 1, frame, appear, appear + 20);
  const [x, y] = xy;
  const flag = arrival; // 0..1 plant animation
  return (
    <g opacity={op}>
      <text
        x={x}
        y={y - 46}
        fill={CORAL}
        stroke="#fff"
        strokeWidth={4.5}
        paintOrder="stroke"
        fontSize={26}
        fontWeight={800}
        fontFamily="Arial, sans-serif"
        letterSpacing={1.5}
        textAnchor="middle"
      >
        ALSACE-LORRAINE
      </text>
      <text
        x={x}
        y={y - 24}
        fill={SUBINK}
        stroke="#fff"
        strokeWidth={3}
        paintOrder="stroke"
        fontSize={14}
        fontWeight={700}
        fontFamily="Arial, sans-serif"
        letterSpacing={5}
        textAnchor="middle"
      >
        OBJECTIVE
      </text>

      {/* flag plants on arrival */}
      {flag > 0.01 && (
        <g transform={`translate(${x} ${y})`} opacity={Math.min(1, flag * 1.5)}>
          <line x1={0} y1={6} x2={0} y2={-30 * Math.min(1, flag)} stroke={INK} strokeWidth={2.4} />
          <path d={`M 0 ${-30 * Math.min(1, flag)} l ${22 * Math.min(1, flag)} 6 l ${-22 * Math.min(1, flag)} 6 Z`} fill={CORAL} />
        </g>
      )}
    </g>
  );
};

// ---------------------------------------------------------------------------
const Backdrop: React.FC = () => (
  <AbsoluteFill
    style={{
      background: "radial-gradient(130% 110% at 50% 28%, #f9fbfb 0%, #e9eff1 55%, #dde6e9 100%)",
    }}
  />
);

const TitleBlock: React.FC<{ frame: number }> = ({ frame }) => {
  const op = ease(0, 1, frame, 6, 34);
  const y = ease(20, 0, frame, 6, 40);
  const lineW = ease(0, 320, frame, 20, 60);
  return (
    <div style={{ position: "absolute", top: 66, left: 92, opacity: op, transform: `translateY(${y}px)`, fontFamily: "Arial, sans-serif" }}>
      <div style={{ color: CORAL, fontSize: 20, letterSpacing: 7, fontWeight: 700 }}>TROOP ADVANCE · WESTERN FRONT</div>
      <div style={{ color: INK, fontSize: 58, fontWeight: 800, letterSpacing: 1, marginTop: 6, lineHeight: 1.05 }}>
        Paris <span style={{ color: CORAL }}>→</span> Alsace-Lorraine
      </div>
      <div style={{ height: 3, width: lineW, background: `linear-gradient(90deg, ${TEAL}, ${CORAL})`, marginTop: 14, borderRadius: 2 }} />
    </div>
  );
};

const OpsChip: React.FC<{ frame: number; arrival: number }> = ({ frame, arrival }) => {
  const op = ease(0, 1, frame, 110, 146);
  const emph = 1 + 0.05 * arrival;
  return (
    <div
      style={{
        position: "absolute",
        bottom: 74,
        left: 92,
        opacity: op,
        transform: `scale(${emph})`,
        transformOrigin: "left bottom",
        display: "flex",
        gap: 38,
        fontFamily: "Arial, sans-serif",
        padding: "18px 30px",
        borderRadius: 14,
        background: "rgba(255,255,255,0.74)",
        border: "1px solid rgba(180,165,140,0.5)",
        boxShadow: "0 12px 30px rgba(120,110,90,0.18)",
      }}
    >
      <Stat label="DISTANCE" value="397 km" accent={CORAL} />
      <Stat label="AXIS" value="E · 093°" accent={TEAL} />
      <Stat label="FORCE" value="Armour + Inf." accent={INK} />
    </div>
  );
};

const Stat: React.FC<{ label: string; value: string; accent: string }> = ({ label, value, accent }) => (
  <div>
    <div style={{ color: SUBINK, fontSize: 14, letterSpacing: 3, fontWeight: 700 }}>{label}</div>
    <div style={{ color: accent, fontSize: 26, fontWeight: 800, marginTop: 4 }}>{value}</div>
  </div>
);

const Vignette: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", boxShadow: "inset 0 0 260px 60px rgba(90,80,60,0.10)" }} />
);

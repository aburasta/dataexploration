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
  VIDEO_WIDTH,
  VIDEO_HEIGHT,
  COUNTRY_PATHS,
  CONTINENT_PATH,
  GRATICULE_PATH,
  CITIES,
  ACCRA_XY,
  KAMPALA_XY,
  buildArc,
  bezierPoint,
  bezierAngle,
  bezierPathD,
  project3d,
  TILT_DEG,
  PERSPECTIVE,
} from "./geo";

// --- Light "Google-Maps-ish" / warm nude palette --------------------------
const CORAL = "#e2734a"; // origin accent
const TEAL = "#1f9e8f"; // destination accent
const INK = "#3a4551"; // primary text
const SUBINK = "#8a97a3"; // secondary text
const LAND = "#f6f1e7"; // country top face
const LAND_EDGE = "#d8c9b2"; // country borders
const WALL_TOP = "#e7dbc6"; // slab side (near top)
const WALL_LO = "#b6a88e"; // slab side (deep)
const HI_TOP = "#f3c6a6"; // highlighted country fill
const HI_EDGE = "#d98a5d";

const HIGHLIGHT = new Set(["GHA", "UGA"]);

const ARC = buildArc(ACCRA_XY, KAMPALA_XY);
const ARC_D = bezierPathD(ARC);

const DEPART = 118;
const ARRIVE = 322;
const EXTRUDE = 15; // slab thickness in map-plane px

const CENTER_TRANSFORM = `perspective(${PERSPECTIVE}px) rotateX(${TILT_DEG}deg)`;

const ease = (from: number, to: number, f: number, a: number, b: number) =>
  interpolate(f, [a, b], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });

// ---------------------------------------------------------------------------
export const AccraToKampala: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Whole-scene entrance (applied to tilted map + pin overlay together so
  // they stay perfectly aligned).
  const introOp = ease(0, 1, frame, 6, 40);
  const introRise = ease(46, 0, frame, 6, 60);
  const introScale = ease(0.94, 1, frame, 6, 90);
  const drift = Math.sin(frame / 110) * 2;

  const t = interpolate(frame, [DEPART, ARRIVE], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.45, 0, 0.25, 1),
  });
  const planePos = bezierPoint(ARC, t);
  const planeAngle = bezierAngle(ARC, t);
  const flying = frame >= DEPART && frame <= ARRIVE + 6;

  const arrivalPulse = spring({
    frame: frame - ARRIVE,
    fps,
    config: { damping: 12, mass: 0.7 },
  });

  // Frame the tilted slab a touch lower & smaller so it sits nicely.
  const FRAME_Y = 46;
  const FRAME_S = 0.9;

  return (
    <AbsoluteFill style={{ backgroundColor: "#eef3f4" }}>
      <Backdrop />

      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: introOp,
          transform: `translateY(${FRAME_Y + introRise + drift}px) scale(${FRAME_S * introScale})`,
          transformOrigin: "center center",
        }}
      >
        {/* Tilted 3D map surface */}
        <svg
          width={VIDEO_WIDTH}
          height={VIDEO_HEIGHT}
          viewBox={`0 0 ${VIDEO_WIDTH} ${VIDEO_HEIGHT}`}
          style={{
            position: "absolute",
            inset: 0,
            transform: CENTER_TRANSFORM,
            transformOrigin: "center center",
            overflow: "visible",
          }}
        >
          <Defs />

          {/* Contact shadow on the ground */}
          <path
            d={CONTINENT_PATH}
            fill="#98867a"
            opacity={0.28}
            transform="translate(26 46)"
            filter="url(#groundBlur)"
          />

          {/* Extruded slab side walls */}
          <g>
            {Array.from({ length: EXTRUDE }, (_, k) => {
              const i = EXTRUDE - k; // deep -> shallow
              const f = i / EXTRUDE;
              const col = mix(WALL_TOP, WALL_LO, f);
              return (
                <path
                  key={i}
                  d={CONTINENT_PATH}
                  transform={`translate(0 ${i})`}
                  fill={col}
                />
              );
            })}
          </g>

          {/* Top face base */}
          <path d={CONTINENT_PATH} fill={LAND} />

          {/* Graticule */}
          <path
            d={GRATICULE_PATH}
            fill="none"
            stroke="#9fb2bd"
            strokeWidth={0.6}
            opacity={ease(0, 0.22, frame, 24, 70)}
            clipPath="url(#continentClip)"
          />

          {/* Countries */}
          <g>
            {COUNTRY_PATHS.map((c, i) => {
              const start = 14 + i * 1.0;
              const op = ease(0, 1, frame, start, start + 24);
              const hi = HIGHLIGHT.has(c.id);
              return (
                <path
                  key={c.id}
                  d={c.d}
                  fill={hi ? HI_TOP : LAND}
                  stroke={hi ? HI_EDGE : LAND_EDGE}
                  strokeWidth={hi ? 1.4 : 0.8}
                  strokeLinejoin="round"
                  opacity={op}
                />
              );
            })}
          </g>

          {/* Top rim */}
          <path
            d={CONTINENT_PATH}
            fill="none"
            stroke="#c9b596"
            strokeWidth={1.6}
            opacity={ease(0, 0.9, frame, 40, 90)}
            strokeLinejoin="round"
          />

          {/* Flight arc + plane live on the tilted surface */}
          <FlightArc t={t} frame={frame} />
          {flying && (
            <Plane
              x={planePos[0]}
              y={planePos[1]}
              angle={planeAngle}
              opacity={
                ease(0, 1, frame, DEPART, DEPART + 10) *
                ease(1, 0, frame, ARRIVE - 2, ARRIVE + 6)
              }
            />
          )}
        </svg>

        {/* Upright pin overlay (not tilted) */}
        <svg
          width={VIDEO_WIDTH}
          height={VIDEO_HEIGHT}
          viewBox={`0 0 ${VIDEO_WIDTH} ${VIDEO_HEIGHT}`}
          style={{ position: "absolute", inset: 0, overflow: "visible" }}
        >
          <Pin
            xy={ACCRA_XY}
            label={CITIES.accra.name}
            sub={CITIES.accra.country}
            appear={78}
            frame={frame}
            fps={fps}
            side="left"
            accent={CORAL}
            active={frame < DEPART + 20}
          />
          <Pin
            xy={KAMPALA_XY}
            label={CITIES.kampala.name}
            sub={CITIES.kampala.country}
            appear={96}
            frame={frame}
            fps={fps}
            side="right"
            accent={TEAL}
            active={frame >= ARRIVE - 4}
            arrivalPulse={arrivalPulse}
          />
        </svg>
      </div>

      <TitleBlock frame={frame} />
      <DistanceChip frame={frame} arrivalPulse={arrivalPulse} />
      <Vignette />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Defs: React.FC = () => (
  <defs>
    <linearGradient id="arcGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stopColor={CORAL} />
      <stop offset="55%" stopColor="#e0a15c" />
      <stop offset="100%" stopColor={TEAL} />
    </linearGradient>
    <clipPath id="continentClip">
      <path d={CONTINENT_PATH} />
    </clipPath>
    <filter id="groundBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="16" />
    </filter>
    <filter id="arcGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" />
    </filter>
    <filter id="planeShadow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="3" />
    </filter>
  </defs>
);

// ---------------------------------------------------------------------------
const FlightArc: React.FC<{ t: number; frame: number }> = ({ t, frame }) => {
  const ref = React.useRef<SVGPathElement>(null);
  const [len, setLen] = React.useState(1600);
  React.useEffect(() => {
    if (ref.current) setLen(ref.current.getTotalLength());
  }, []);

  const appear = ease(0, 1, frame, DEPART - 6, DEPART + 8);
  const drawn = len * t;

  return (
    <g opacity={appear}>
      <path
        d={ARC_D}
        fill="none"
        stroke={CORAL}
        strokeWidth={1.6}
        strokeDasharray="1 9"
        strokeLinecap="round"
        opacity={0.4}
      />
      <path
        d={ARC_D}
        fill="none"
        stroke="url(#arcGrad)"
        strokeWidth={7}
        strokeLinecap="round"
        strokeDasharray={`${drawn} ${len}`}
        opacity={0.35}
        filter="url(#arcGlow)"
      />
      <path
        ref={ref}
        d={ARC_D}
        fill="none"
        stroke="url(#arcGrad)"
        strokeWidth={3.2}
        strokeLinecap="round"
        strokeDasharray={`${drawn} ${len}`}
      />
    </g>
  );
};

// ---------------------------------------------------------------------------
const PLANE_PATH =
  "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z";

const Plane: React.FC<{ x: number; y: number; angle: number; opacity: number }> = ({
  x,
  y,
  angle,
  opacity,
}) => {
  const scale = 1.9;
  return (
    <g opacity={opacity}>
      {/* shadow on the surface */}
      <g transform={`translate(${x + 5} ${y + 8}) rotate(${angle + 90})`}>
        <g transform={`scale(${scale}) translate(-12 -12)`}>
          <path d={PLANE_PATH} fill="#7d6a5a" opacity={0.35} filter="url(#planeShadow)" />
        </g>
      </g>
      <g transform={`translate(${x} ${y}) rotate(${angle + 90})`}>
        <g transform={`scale(${scale}) translate(-12 -12)`}>
          <path d={PLANE_PATH} fill={INK} />
          <path
            d={PLANE_PATH}
            fill="none"
            stroke="#ffffff"
            strokeWidth={0.7}
            opacity={0.6}
          />
        </g>
      </g>
    </g>
  );
};

// ---------------------------------------------------------------------------
const Pin: React.FC<{
  xy: [number, number];
  label: string;
  sub: string;
  appear: number;
  frame: number;
  fps: number;
  side: "left" | "right";
  accent: string;
  active: boolean;
  arrivalPulse?: number;
}> = ({ xy, label, sub, appear, frame, fps, side, accent, active, arrivalPulse }) => {
  const s = spring({ frame: frame - appear, fps, config: { damping: 13, mass: 0.6 } });
  const op = ease(0, 1, frame, appear, appear + 16);

  const base = project3d(xy[0], xy[1]);
  const bx = base.x;
  const by = base.y;
  const headY = by - 58 * s; // pin stands up
  const dir = side === "left" ? -1 : 1;
  const anchor = side === "left" ? "end" : "start";
  const lx = bx + dir * 14;

  // flattened ground ring (sits on the tilted surface)
  const pulseT = ((frame - appear) % 55) / 55;
  const pulseR = interpolate(pulseT, [0, 1], [7, 30]);
  const pulseO = interpolate(pulseT, [0, 1], [0.5, 0]) * (active ? 1 : 0.3);

  const arrR = arrivalPulse ? interpolate(arrivalPulse, [0, 1], [8, 64]) : 0;
  const arrO = arrivalPulse ? interpolate(arrivalPulse, [0, 1], [0.55, 0]) : 0;

  return (
    <g opacity={op}>
      {arrivalPulse ? (
        <ellipse cx={bx} cy={by} rx={arrR} ry={arrR * 0.34} fill="none" stroke={accent} strokeWidth={2} opacity={arrO} />
      ) : null}
      <ellipse cx={bx} cy={by} rx={pulseR} ry={pulseR * 0.34} fill="none" stroke={accent} strokeWidth={1.6} opacity={pulseO} />
      <ellipse cx={bx} cy={by} rx={7} ry={2.6} fill={accent} opacity={0.55} />

      {/* pin stick */}
      <line x1={bx} y1={by} x2={bx} y2={headY} stroke={accent} strokeWidth={2.4} />
      {/* head */}
      <circle cx={bx} cy={headY} r={10 * s} fill={accent} />
      <circle cx={bx} cy={headY} r={4.2 * s} fill="#ffffff" />

      {/* label */}
      <text
        x={lx + dir * 6}
        y={headY - 12}
        fill={INK}
        stroke="#ffffff"
        strokeWidth={4}
        paintOrder="stroke"
        fontSize={30}
        fontWeight={800}
        fontFamily="Arial, sans-serif"
        letterSpacing={2}
        textAnchor={anchor}
      >
        {label}
      </text>
      <text
        x={lx + dir * 6}
        y={headY + 10}
        fill={accent}
        stroke="#ffffff"
        strokeWidth={3.5}
        paintOrder="stroke"
        fontSize={15}
        fontWeight={700}
        fontFamily="Arial, sans-serif"
        letterSpacing={4}
        textAnchor={anchor}
      >
        {sub}
      </text>
    </g>
  );
};

// ---------------------------------------------------------------------------
const Backdrop: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(130% 110% at 50% 30%, #f7fbfc 0%, #e7eef1 55%, #dbe4e8 100%)",
    }}
  />
);

// ---------------------------------------------------------------------------
const TitleBlock: React.FC<{ frame: number }> = ({ frame }) => {
  const op = ease(0, 1, frame, 6, 34);
  const y = ease(20, 0, frame, 6, 40);
  const lineW = ease(0, 300, frame, 20, 60);
  return (
    <div
      style={{
        position: "absolute",
        top: 70,
        left: 96,
        opacity: op,
        transform: `translateY(${y}px)`,
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div style={{ color: CORAL, fontSize: 20, letterSpacing: 8, fontWeight: 700 }}>
        FLIGHT ROUTE · WEST → EAST AFRICA
      </div>
      <div
        style={{
          color: INK,
          fontSize: 62,
          fontWeight: 800,
          letterSpacing: 2,
          marginTop: 6,
          lineHeight: 1.05,
        }}
      >
        Accra <span style={{ color: TEAL }}>→</span> Kampala
      </div>
      <div
        style={{
          height: 3,
          width: lineW,
          background: `linear-gradient(90deg, ${CORAL}, ${TEAL})`,
          marginTop: 14,
          borderRadius: 2,
        }}
      />
    </div>
  );
};

const DistanceChip: React.FC<{ frame: number; arrivalPulse: number }> = ({ frame, arrivalPulse }) => {
  const op = ease(0, 1, frame, 118, 150);
  const emph = 1 + 0.06 * arrivalPulse;
  return (
    <div
      style={{
        position: "absolute",
        bottom: 76,
        left: 96,
        opacity: op,
        transform: `scale(${emph})`,
        transformOrigin: "left bottom",
        display: "flex",
        gap: 40,
        fontFamily: "Arial, sans-serif",
        padding: "18px 30px",
        borderRadius: 14,
        background: "rgba(255,255,255,0.72)",
        border: "1px solid rgba(180,165,140,0.5)",
        boxShadow: "0 12px 30px rgba(120,110,90,0.18)",
        backdropFilter: "blur(4px)",
      }}
    >
      <Stat label="DISTANCE" value="3,684 km" accent={CORAL} />
      <Stat label="BEARING" value="ENE · 098°" accent={TEAL} />
      <Stat label="FLIGHT TIME" value="~4h 55m" accent={INK} />
    </div>
  );
};

const Stat: React.FC<{ label: string; value: string; accent: string }> = ({ label, value, accent }) => (
  <div>
    <div style={{ color: SUBINK, fontSize: 14, letterSpacing: 3, fontWeight: 700 }}>{label}</div>
    <div style={{ color: accent, fontSize: 28, fontWeight: 800, marginTop: 4 }}>{value}</div>
  </div>
);

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      boxShadow: "inset 0 0 260px 60px rgba(90,80,60,0.10)",
    }}
  />
);

// ---------------------------------------------------------------------------
// tiny hex colour lerp
function mix(a: string, b: string, t: number): string {
  const pa = hex(a);
  const pb = hex(b);
  const r = Math.round(pa[0] + (pb[0] - pa[0]) * t);
  const g = Math.round(pa[1] + (pb[1] - pa[1]) * t);
  const bl = Math.round(pa[2] + (pb[2] - pa[2]) * t);
  return `rgb(${r},${g},${bl})`;
}
function hex(h: string): [number, number, number] {
  const s = h.replace("#", "");
  return [
    parseInt(s.slice(0, 2), 16),
    parseInt(s.slice(2, 4), 16),
    parseInt(s.slice(4, 6), 16),
  ];
}

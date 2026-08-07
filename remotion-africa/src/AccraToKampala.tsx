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
} from "./geo";

const GOLD = "#FFB65C";
const CYAN = "#4FD8C7";
const INK0 = "#050912";
const INK1 = "#0a1428";

const HIGHLIGHT = new Set(["GHA", "UGA"]);

const ARC = buildArc(ACCRA_XY, KAMPALA_XY);
const ARC_D = bezierPathD(ARC);

// Departure / arrival timing (frames @30fps)
const DEPART = 118;
const ARRIVE = 322;

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

  // Overall cinematic breathing of the map group.
  const introScale = ease(0.965, 1, frame, 8, 120);
  const drift = Math.sin(frame / 90) * 3;

  // Plane progress 0..1 with ease-in-out.
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

  return (
    <AbsoluteFill style={{ backgroundColor: INK0 }}>
      <Backdrop frame={frame} />

      <svg
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
        viewBox={`0 0 ${VIDEO_WIDTH} ${VIDEO_HEIGHT}`}
        style={{ position: "absolute", inset: 0 }}
      >
        <Defs />

        <g
          transform={`translate(${VIDEO_WIDTH / 2} ${VIDEO_HEIGHT / 2}) scale(${introScale}) translate(${-VIDEO_WIDTH / 2} ${-VIDEO_HEIGHT / 2 + drift})`}
        >
          {/* Continent glow / shadow base */}
          <path
            d={CONTINENT_PATH}
            fill="url(#seaGlow)"
            opacity={ease(0, 1, frame, 8, 60)}
            filter="url(#softGlow)"
          />

          {/* Graticule grid */}
          <path
            d={GRATICULE_PATH}
            fill="none"
            stroke={CYAN}
            strokeWidth={0.6}
            opacity={ease(0, 0.12, frame, 24, 70)}
            clipPath="url(#continentClip)"
          />

          {/* Countries (staggered draw-in) */}
          <g>
            {COUNTRY_PATHS.map((c, i) => {
              const start = 14 + i * 1.05;
              const op = ease(0, 1, frame, start, start + 26);
              const rise = ease(16, 0, frame, start, start + 34);
              const hi = HIGHLIGHT.has(c.id);
              return (
                <g key={c.id} transform={`translate(0 ${rise})`} opacity={op}>
                  <path
                    d={c.d}
                    fill={hi ? "url(#hiFill)" : "url(#landFill)"}
                    stroke={hi ? GOLD : "#356aa8"}
                    strokeWidth={hi ? 1.4 : 0.75}
                    strokeLinejoin="round"
                  />
                </g>
              );
            })}
          </g>

          {/* Crisp continent rim */}
          <path
            d={CONTINENT_PATH}
            fill="none"
            stroke="url(#rimStroke)"
            strokeWidth={1.6}
            opacity={ease(0, 0.9, frame, 40, 90)}
            strokeLinejoin="round"
          />

          {/* Flight arc trail */}
          <FlightArc t={t} frame={frame} />

          {/* City markers */}
          <CityMarker
            xy={ACCRA_XY}
            label={CITIES.accra.name}
            sub={CITIES.accra.country}
            appear={78}
            frame={frame}
            fps={fps}
            side="left"
            accent={GOLD}
            active={frame < DEPART + 20}
          />
          <CityMarker
            xy={KAMPALA_XY}
            label={CITIES.kampala.name}
            sub={CITIES.kampala.country}
            appear={96}
            frame={frame}
            fps={fps}
            side="right"
            accent={CYAN}
            active={frame >= ARRIVE - 4}
            arrivalPulse={arrivalPulse}
          />

          {/* Plane */}
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
        </g>
      </svg>

      {/* Foreground UI overlays (not affected by map scale) */}
      <TitleBlock frame={frame} />
      <DistanceChip frame={frame} arrivalPulse={arrivalPulse} />
      <Vignette />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Defs: React.FC = () => (
  <defs>
    <linearGradient id="landFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#173257" />
      <stop offset="100%" stopColor="#0e2038" />
    </linearGradient>
    <linearGradient id="hiFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#7a4f1e" />
      <stop offset="100%" stopColor="#3a2a12" />
    </linearGradient>
    <radialGradient id="seaGlow" cx="45%" cy="45%" r="60%">
      <stop offset="0%" stopColor="#12406b" stopOpacity="0.9" />
      <stop offset="100%" stopColor="#0a1a30" stopOpacity="0" />
    </radialGradient>
    <linearGradient id="rimStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stopColor="#5fa8e6" />
      <stop offset="100%" stopColor="#4FD8C7" />
    </linearGradient>
    <linearGradient id="arcGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stopColor="#FFB65C" />
      <stop offset="55%" stopColor="#F2C879" />
      <stop offset="100%" stopColor="#4FD8C7" />
    </linearGradient>
    <clipPath id="continentClip">
      <path d={CONTINENT_PATH} />
    </clipPath>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="14" />
    </filter>
    <filter id="arcGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" />
    </filter>
    <filter id="planeGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="4" />
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
      {/* faint full route (dotted) */}
      <path
        d={ARC_D}
        fill="none"
        stroke={CYAN}
        strokeWidth={1.4}
        strokeDasharray="1 9"
        strokeLinecap="round"
        opacity={0.35}
      />
      {/* glow underlay of drawn portion */}
      <path
        d={ARC_D}
        fill="none"
        stroke="url(#arcGrad)"
        strokeWidth={7}
        strokeLinecap="round"
        strokeDasharray={`${drawn} ${len}`}
        opacity={0.5}
        filter="url(#arcGlow)"
      />
      {/* crisp drawn portion */}
      <path
        ref={ref}
        d={ARC_D}
        fill="none"
        stroke="url(#arcGrad)"
        strokeWidth={3}
        strokeLinecap="round"
        strokeDasharray={`${drawn} ${len}`}
      />
    </g>
  );
};

// ---------------------------------------------------------------------------
const CityMarker: React.FC<{
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
  const [x, y] = xy;

  // continuous soft pulse ring
  const pulseT = ((frame - appear) % 55) / 55;
  const pulseR = interpolate(pulseT, [0, 1], [6, 26]);
  const pulseO = interpolate(pulseT, [0, 1], [0.55, 0]) * (active ? 1 : 0.35);

  const dir = side === "left" ? -1 : 1;
  const anchor = side === "left" ? "end" : "start";
  const tx = x + dir * 22;

  const arrivalR = arrivalPulse ? interpolate(arrivalPulse, [0, 1], [8, 60]) : 0;
  const arrivalO = arrivalPulse ? interpolate(arrivalPulse, [0, 1], [0.6, 0]) : 0;

  return (
    <g opacity={op}>
      {/* connector line */}
      <line
        x1={x}
        y1={y}
        x2={tx}
        y2={y - 30}
        stroke={accent}
        strokeWidth={1.2}
        opacity={0.7}
      />
      <line
        x1={tx}
        y1={y - 30}
        x2={tx + dir * 150}
        y2={y - 30}
        stroke={accent}
        strokeWidth={1.2}
        opacity={0.7}
      />
      {/* label */}
      <text
        x={tx + dir * 8}
        y={y - 36}
        fill="#ffffff"
        fontSize={30}
        fontWeight={700}
        fontFamily="Arial, sans-serif"
        letterSpacing={3}
        textAnchor={anchor}
      >
        {label}
      </text>
      <text
        x={tx + dir * 8}
        y={y - 14}
        fill={accent}
        fontSize={16}
        fontWeight={600}
        fontFamily="Arial, sans-serif"
        letterSpacing={5}
        textAnchor={anchor}
      >
        {sub}
      </text>

      {/* arrival shockwave */}
      {arrivalPulse ? (
        <circle cx={x} cy={y} r={arrivalR} fill="none" stroke={accent} strokeWidth={2} opacity={arrivalO} />
      ) : null}
      {/* pulse ring */}
      <circle cx={x} cy={y} r={pulseR} fill="none" stroke={accent} strokeWidth={1.6} opacity={pulseO} />
      {/* dot */}
      <circle cx={x} cy={y} r={7 * s} fill={accent} />
      <circle cx={x} cy={y} r={3.2 * s} fill="#ffffff" />
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
  // icon nose points "up" (-90°); add 90 to align with travel direction.
  const scale = 1.9;
  return (
    <g transform={`translate(${x} ${y})`} opacity={opacity}>
      <g transform={`rotate(${angle + 90})`}>
        <g transform={`scale(${scale}) translate(-12 -12)`}>
          <path d={PLANE_PATH} fill={GOLD} filter="url(#planeGlow)" />
          <path d={PLANE_PATH} fill="#fff7ea" />
        </g>
      </g>
      <circle r={4} fill="#fff" opacity={0.9} />
    </g>
  );
};

// ---------------------------------------------------------------------------
const Backdrop: React.FC<{ frame: number }> = ({ frame }) => {
  const glow = 0.5 + 0.12 * Math.sin(frame / 60);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 100% at 50% 35%, ${INK1} 0%, ${INK0} 62%)`,
      }}
    >
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 35% at 30% 40%, rgba(30,90,140,${glow * 0.5}) 0%, transparent 70%)`,
        }}
      />
      <StarField />
    </AbsoluteFill>
  );
};

const StarField: React.FC = () => {
  const dots = React.useMemo(
    () =>
      Array.from({ length: 90 }, (_, i) => {
        const r = seeded(i);
        return {
          x: seeded(i * 3.1) * VIDEO_WIDTH,
          y: seeded(i * 7.7) * VIDEO_HEIGHT,
          s: 0.5 + r * 1.4,
          o: 0.08 + r * 0.22,
        };
      }),
    [],
  );
  return (
    <svg width={VIDEO_WIDTH} height={VIDEO_HEIGHT} style={{ position: "absolute" }}>
      {dots.map((d, i) => (
        <circle key={i} cx={d.x} cy={d.y} r={d.s} fill="#8fb7d6" opacity={d.o} />
      ))}
    </svg>
  );
};

const seeded = (n: number) => {
  const x = Math.sin(n * 999.13) * 43758.5453;
  return x - Math.floor(x);
};

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
      <div style={{ color: GOLD, fontSize: 20, letterSpacing: 8, fontWeight: 600 }}>
        FLIGHT ROUTE · WEST → EAST AFRICA
      </div>
      <div
        style={{
          color: "#fff",
          fontSize: 62,
          fontWeight: 800,
          letterSpacing: 2,
          marginTop: 6,
          lineHeight: 1.05,
        }}
      >
        Accra <span style={{ color: CYAN }}>→</span> Kampala
      </div>
      <div style={{ height: 3, width: lineW, background: `linear-gradient(90deg, ${GOLD}, ${CYAN})`, marginTop: 14, borderRadius: 2 }} />
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
        background: "rgba(10,20,40,0.55)",
        border: "1px solid rgba(90,150,210,0.35)",
        backdropFilter: "blur(4px)",
      }}
    >
      <Stat label="DISTANCE" value="3,684 km" accent={GOLD} />
      <Stat label="BEARING" value="ENE · 098°" accent={CYAN} />
      <Stat label="FLIGHT TIME" value="~4h 55m" accent="#ffffff" />
    </div>
  );
};

const Stat: React.FC<{ label: string; value: string; accent: string }> = ({ label, value, accent }) => (
  <div>
    <div style={{ color: "#9fb6cf", fontSize: 14, letterSpacing: 3, fontWeight: 600 }}>{label}</div>
    <div style={{ color: accent, fontSize: 28, fontWeight: 800, marginTop: 4 }}>{value}</div>
  </div>
);

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      boxShadow: "inset 0 0 320px 80px rgba(0,0,0,0.55)",
    }}
  />
);

import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  Easing,
  delayRender,
  continueRender,
} from "remotion";
import { STROKES, I_DOT, STROKE_STARTS, WORD_CENTER } from "./handwriting";

// --- warm palette ----------------------------------------------------------
const PAPER = "#f3ead6";
const INK = "#4a3524"; // warm sepia
const INK_CORE = "#2f2113";
const INK_BLEED = "#6b5033";

// writing-space -> screen transform
const SCALE = 1.5;
const OX = 960 - SCALE * WORD_CENTER.x;
const OY = 540 - SCALE * WORD_CENTER.y;
const toScreen = (p: { x: number; y: number }) => ({
  x: OX + SCALE * p.x,
  y: OY + SCALE * p.y,
});

// timeline (30fps)
const WRITE_START = 46;
const WRITE_END = 250;
const DOT_AT = 256;
const HAND_IN_START = 20;
const HAND_OUT_START = 262;
const HAND_OUT_END = 292;

const GAP = 46; // local travel length inserted between strokes (pen lift)
const SAMPLES = 200;

const ease = (from: number, to: number, f: number, a: number, b: number) =>
  interpolate(f, [a, b], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });

const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

// ---------------------------------------------------------------------------
export const PrinceInk: React.FC = () => {
  const frame = useCurrentFrame();

  const refs = React.useRef<(SVGPathElement | null)[]>([]);
  const [handle] = React.useState(() => delayRender("measure-strokes"));
  const [lens, setLens] = React.useState<number[]>(() => STROKES.map(() => 200));
  const [samples, setSamples] = React.useState<{ x: number; y: number }[][]>(
    () => STROKES.map(() => []),
  );

  React.useEffect(() => {
    const nextLens: number[] = [];
    const nextSamples: { x: number; y: number }[][] = [];
    STROKES.forEach((_, i) => {
      const el = refs.current[i];
      if (!el) {
        nextLens.push(200);
        nextSamples.push([]);
        return;
      }
      const L = el.getTotalLength();
      nextLens.push(L);
      const pts: { x: number; y: number }[] = [];
      for (let s = 0; s < SAMPLES; s++) {
        const pt = el.getPointAtLength((L * s) / (SAMPLES - 1));
        pts.push({ x: pt.x, y: pt.y });
      }
      nextSamples.push(pts);
    });
    setLens(nextLens);
    setSamples(nextSamples);
    continueRender(handle);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const sampleAt = (stroke: number, t: number) => {
    const arr = samples[stroke];
    if (!arr || arr.length === 0) return STROKE_STARTS[stroke];
    return arr[Math.round(clamp01(t) * (arr.length - 1))];
  };

  // ---- cumulative offsets across strokes + gaps -------------------------
  const n = STROKES.length;
  const off: number[] = [];
  let acc = 0;
  for (let i = 0; i < n; i++) {
    off.push(acc);
    acc += lens[i] + (i < n - 1 ? GAP : 0);
  }
  const total = acc;

  const g = clamp01((frame - WRITE_START) / (WRITE_END - WRITE_START));
  const drawn = g * total;

  const progress = lens.map((L, i) => clamp01((drawn - off[i]) / L));

  // ---- nib position + pen lift ------------------------------------------
  let nibLocal = STROKE_STARTS[0];
  let lift = 0;

  if (frame < WRITE_START) {
    nibLocal = STROKE_STARTS[0];
    lift = interpolate(frame, [HAND_IN_START, WRITE_START], [46, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= WRITE_END) {
    // travel to the i-dot / settle
    const a = sampleAt(n - 1, 1);
    const tt = ease(0, 1, frame, WRITE_END, DOT_AT);
    nibLocal = { x: a.x + (I_DOT.x - a.x) * tt, y: a.y + (I_DOT.y - a.y) * tt };
    lift = interpolate(frame, [WRITE_END, DOT_AT - 3, DOT_AT], [10, 20, 3], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else {
    let placed = false;
    for (let i = 0; i < n; i++) {
      const segStart = off[i];
      const segEnd = off[i] + lens[i];
      if (drawn <= segEnd) {
        nibLocal = sampleAt(i, (drawn - segStart) / lens[i]);
        placed = true;
        break;
      }
      const gapEnd = segEnd + GAP;
      if (i < n - 1 && drawn < gapEnd) {
        const gt = clamp01((drawn - segEnd) / GAP);
        const a = sampleAt(i, 1);
        const b = sampleAt(i + 1, 0);
        nibLocal = { x: a.x + (b.x - a.x) * gt, y: a.y + (b.y - a.y) * gt };
        lift = Math.sin(gt * Math.PI) * 24;
        placed = true;
        break;
      }
    }
    if (!placed) nibLocal = sampleAt(n - 1, 1);
  }

  const nib = toScreen(nibLocal);

  // hand entrance / exit (screen space, from bottom-right)
  const enter = interpolate(frame, [HAND_IN_START - 12, WRITE_START], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });
  const exit = interpolate(frame, [HAND_OUT_START, HAND_OUT_END], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.5, 0, 0.5, 1),
  });
  const handOff = (enter + exit) * 620;
  const handVisible = frame > HAND_IN_START - 14;
  const sway = Math.sin(frame / 16) * 1.1;

  // i-dot appearance
  const dotOp = ease(0, 1, frame, DOT_AT, DOT_AT + 4);
  const dotR = interpolate(frame, [DOT_AT, DOT_AT + 6], [2, 6.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.3, 1.5, 0.5, 1),
  });

  const paperIn = ease(0.985, 1, frame, 0, 24);
  const inkSettle = ease(0, 1, frame, WRITE_END, WRITE_END + 40);

  return (
    <AbsoluteFill style={{ backgroundColor: "#e7dfd2" }}>
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(120% 100% at 50% 40%, #efe7d9 0%, #e2d7c4 60%, #d3c6ae 100%)",
        }}
      />

      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0 }}>
        <Defs />

        {/* paper sheet */}
        <g transform={`translate(960 540) scale(${paperIn}) translate(-960 -540)`}>
          <rect x={150} y={96} width={1620} height={888} rx={10} fill="#c9bda6" opacity={0.5} filter="url(#sheetShadow)" />
          <rect x={150} y={96} width={1620} height={888} rx={10} fill={PAPER} />
          <rect x={150} y={96} width={1620} height={888} rx={10} fill={PAPER} filter="url(#crumple)" />
          <rect x={150} y={96} width={1620} height={888} rx={10} fill="#000" opacity={0.5} filter="url(#grain)" />
          <rect x={150} y={96} width={1620} height={888} rx={10} fill="none" stroke="#d8ccb2" strokeWidth={2} />
        </g>

        {/* ink word (local writing space) */}
        <g transform={`translate(${OX} ${OY}) scale(${SCALE})`}>
          {/* settle shadow */}
          <g opacity={inkSettle * 0.45} filter="url(#inkShadow)">
            {STROKES.map((st, i) => (
              <path
                key={`sh-${st.id}`}
                d={st.d}
                fill="none"
                stroke="#000"
                strokeWidth={5}
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeDasharray={`${lens[i] * progress[i]} ${lens[i]}`}
              />
            ))}
          </g>

          {STROKES.map((st, i) => {
            const dash = `${lens[i] * progress[i]} ${lens[i]}`;
            return (
              <g key={st.id} opacity={progress[i] > 0 ? 1 : 0}>
                <path d={st.d} fill="none" stroke={INK_BLEED} strokeWidth={7.5} strokeLinecap="round" strokeLinejoin="round" opacity={0.3} filter="url(#bleed)" strokeDasharray={dash} />
                <path ref={(el) => (refs.current[i] = el)} d={st.d} fill="none" stroke={INK} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
                <path d={st.d} fill="none" stroke={INK_CORE} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" opacity={0.55} strokeDasharray={dash} />
              </g>
            );
          })}

          {/* i-dot */}
          <circle cx={I_DOT.x} cy={I_DOT.y} r={dotR} fill={INK} opacity={dotOp} />
        </g>

        {/* hand + pen (screen space) */}
        {handVisible && (
          <g transform={`translate(${nib.x + handOff} ${nib.y + handOff * 0.55 - lift}) rotate(${sway})`}>
            <HandPen />
          </g>
        )}
      </svg>

      <Vignette />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Defs: React.FC = () => (
  <defs>
    <filter id="crumple" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.010 0.014" numOctaves={3} seed={11} result="noise" />
      <feDiffuseLighting in="noise" surfaceScale="2.4" diffuseConstant="1" lightingColor="#ffffff" result="light">
        <feDistantLight azimuth={235} elevation={62} />
      </feDiffuseLighting>
      <feComposite in="light" in2="SourceGraphic" operator="arithmetic" k1={1} k2={0} k3={0} k4={0} />
    </filter>
    <filter id="grain" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={4} result="n" />
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.6 0" />
    </filter>
    <filter id="sheetShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="22" floodColor="#5c4a30" floodOpacity="0.35" />
    </filter>
    <filter id="bleed" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.2" />
    </filter>
    <filter id="inkShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" />
    </filter>
  </defs>
);

// ---------------------------------------------------------------------------
// Stylised 2D hand holding a fountain pen; nib tip at local (0,0).
const HandPen: React.FC = () => (
  <g>
    <line x1={22} y1={-14} x2={224} y2={-176} stroke="#7c5a38" strokeWidth={30} strokeLinecap="round" />
    <line x1={26} y1={-20} x2={210} y2={-168} stroke="#9a744a" strokeWidth={8} strokeLinecap="round" opacity={0.7} />
    <line x1={16} y1={-10} x2={44} y2={-32} stroke="#c8c8cf" strokeWidth={30} strokeLinecap="butt" />
    <path d="M0,0 L22,-12 L34,-30 L14,-22 Z" fill="#b9b9c2" stroke="#8a8a93" strokeWidth={1.2} />
    <line x1={5} y1={-4} x2={24} y2={-19} stroke="#6f6f79" strokeWidth={1.4} />

    <path d="M96,-150 C150,-186 196,-150 190,-104 C186,-74 150,-58 120,-70 C96,-80 78,-124 96,-150 Z" fill="#dcb187" stroke="#c1946a" strokeWidth={2} />
    <g stroke="#c1946a" strokeWidth={2}>
      <rect x={70} y={-118} width={64} height={20} rx={10} fill="#e2ba90" transform="rotate(-38 102 -108)" />
      <rect x={78} y={-100} width={60} height={19} rx={9.5} fill="#dcb488" transform="rotate(-38 108 -90)" />
      <rect x={86} y={-83} width={54} height={18} rx={9} fill="#d6ad80" transform="rotate(-38 113 -74)" />
    </g>
    <rect x={64} y={-96} width={48} height={18} rx={9} fill="#e2ba90" stroke="#c1946a" strokeWidth={2} transform="rotate(-64 88 -87)" />
    <path d="M150,-210 C210,-244 268,-206 250,-152 C242,-130 206,-120 176,-140 C154,-154 138,-190 150,-210 Z" fill="#8a9a8e" stroke="#6f8073" strokeWidth={2} />
  </g>
);

// ---------------------------------------------------------------------------
const Vignette: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", boxShadow: "inset 0 0 300px 80px rgba(70,55,35,0.18)" }} />
);

import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  interpolate,
  Easing,
} from "remotion";

// Beat sheet for the opening 60s, cut to the Whisper word timings.
// type: "video" (public/broll/<src>.mp4) or "still" (Ken-Burns image).
type Beat = {
  from: number; // start frame (30fps)
  dur: number; // frames
  src: string;
  kind: "video" | "still";
  name?: string; // lower-third name card
  sub?: string;
};

const B: Beat[] = [
  { from: 0, dur: 162, src: "broll/reds_ruins.mp4", kind: "video" },
  { from: 162, dur: 164, src: "broll/reds_combat.mp4", kind: "video" },
  { from: 326, dur: 199, src: "broll/eva_berghof.mp4", kind: "video", name: "EVA BRAUN", sub: "Berghof · home movies" },
  { from: 525, dur: 159, src: "broll/eva_terrace.mp4", kind: "video" },
  { from: 684, dur: 177, src: "broll/eva_group.mp4", kind: "video" },
  { from: 861, dur: 234, src: "broll/eva_close.mp4", kind: "video" },
  { from: 1095, dur: 165, src: "broll/geli_raubal.jpg", kind: "still", name: "GELI RAUBAL", sub: "1908 – 1931" },
  { from: 1260, dur: 195, src: "broll/parade_troops.mp4", kind: "video" },
  { from: 1455, dur: 180, src: "broll/reds_town.mp4", kind: "video" },
  { from: 1635, dur: 165, src: "broll/eva_berghof.mp4", kind: "video" },
];

const DUR = 1800; // 60s @30fps

// ---------------------------------------------------------------------------
const Clip: React.FC<{ beat: Beat }> = ({ beat }) => {
  const f = useCurrentFrame();
  // gentle cinematic push (Ken Burns) across the whole beat
  const scale = interpolate(f, [0, beat.dur], [1.06, 1.14], {
    extrapolateRight: "clamp",
    easing: Easing.linear,
  });
  const fadeIn = interpolate(f, [0, 8], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", opacity: fadeIn }}>
      <AbsoluteFill style={{ transform: `scale(${scale})` }}>
        {beat.kind === "video" ? (
          <OffthreadVideo
            src={staticFile(beat.src)}
            muted
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <Img
            src={staticFile(beat.src)}
            style={{ width: "100%", height: "100%", objectFit: "cover", filter: "grayscale(0.1)" }}
          />
        )}
      </AbsoluteFill>

      {/* subtle film vignette + tone */}
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          boxShadow: "inset 0 0 320px 90px rgba(0,0,0,0.55)",
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.28) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 62%, rgba(0,0,0,0.5) 100%)",
        }}
      />

      {beat.name ? <NameCard name={beat.name} sub={beat.sub} dur={beat.dur} /> : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const NameCard: React.FC<{ name: string; sub?: string; dur: number }> = ({ name, sub, dur }) => {
  const f = useCurrentFrame();
  const inO = interpolate(f, [8, 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const outO = interpolate(f, [dur - 26, dur - 12], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const op = Math.min(inO, outO);
  const x = interpolate(f, [8, 22], [-24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const barW = interpolate(f, [10, 30], [0, 8], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div
      style={{
        position: "absolute",
        left: 96,
        bottom: 96,
        opacity: op,
        transform: `translateX(${x}px)`,
        display: "flex",
        alignItems: "stretch",
        gap: 18,
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div style={{ width: barW, background: "#e0b13c", borderRadius: 2 }} />
      <div>
        <div style={{ color: "#fff", fontSize: 44, fontWeight: 800, letterSpacing: 2, textShadow: "0 2px 14px rgba(0,0,0,0.7)" }}>
          {name}
        </div>
        {sub ? (
          <div style={{ color: "#e7d9b6", fontSize: 22, fontWeight: 600, letterSpacing: 4, marginTop: 4, textShadow: "0 2px 10px rgba(0,0,0,0.7)" }}>
            {sub}
          </div>
        ) : null}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
export const ReelOpen: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {B.map((beat, i) => (
        <Sequence key={i} from={beat.from} durationInFrames={beat.dur}>
          <Clip beat={beat} />
        </Sequence>
      ))}
      <Audio src={staticFile("vo/voiceover.wav")} />
    </AbsoluteFill>
  );
};

export { DUR as REEL_OPEN_DURATION };

import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Img,
  staticFile,
  useCurrentFrame,
  interpolate,
  Easing,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import beats from "./beatsFull.json";

type Beat = { from: number; dur: number; src: string; name?: string; sub?: string };
const B = beats as Beat[];

// Cross-dissolve length between clips (frames). Overlaps adjacent clips so there
// is never a cut to black. Sequences are padded by XF so each cut still lands on
// its original beat time -> the voiceover stays in sync.
const XF = 11;

const isStill = (src: string) =>
  src.toLowerCase().endsWith(".jpg") || src.toLowerCase().endsWith(".png");

// ---------------------------------------------------------------------------
const Clip: React.FC<{ beat: Beat }> = ({ beat }) => {
  const f = useCurrentFrame();
  // gentle cinematic push (Ken Burns) — no fade-from-black; the transition blends.
  const scale = interpolate(f, [0, beat.dur + XF], [1.06, 1.14], {
    extrapolateRight: "clamp",
    easing: Easing.linear,
  });
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${scale})` }}>
        {isStill(beat.src) ? (
          <Img
            src={staticFile(beat.src)}
            style={{ width: "100%", height: "100%", objectFit: "cover", filter: "grayscale(0.05)" }}
          />
        ) : (
          <OffthreadVideo
            src={staticFile(beat.src)}
            muted
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        )}
      </AbsoluteFill>

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
  const inO = interpolate(f, [XF + 4, XF + 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const outO = interpolate(f, [dur - 26, dur - 12], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const op = Math.min(inO, outO);
  const x = interpolate(f, [XF + 4, XF + 18], [-24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const barW = interpolate(f, [XF + 6, XF + 26], [0, 8], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
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
export const ReelFull: React.FC = () => {
  const last = B.length - 1;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TransitionSeries>
        {B.flatMap((beat, i) => {
          // pad every clip (except the last) by XF so the dissolve overlaps the
          // next clip while each cut still starts at beat.from.
          const seqDur = i < last ? beat.dur + XF : beat.dur;
          const nodes = [
            <TransitionSeries.Sequence key={`s${i}`} durationInFrames={seqDur}>
              <Clip beat={beat} />
            </TransitionSeries.Sequence>,
          ];
          if (i < last) {
            nodes.push(
              <TransitionSeries.Transition
                key={`t${i}`}
                timing={linearTiming({ durationInFrames: XF })}
                presentation={fade()}
              />,
            );
          }
          return nodes;
        })}
      </TransitionSeries>
      <Audio src={staticFile("vo/voiceover.wav")} />
    </AbsoluteFill>
  );
};

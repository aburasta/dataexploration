import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { DUR } from "./config";

// Crossfade in/out at the edges of a scene — for cuts within a sequence/act.
export function XFade({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const f = Math.min(DUR.xfade, Math.floor(durationInFrames / 2));
  const opacity = interpolate(
    frame,
    [0, f, durationInFrames - f, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
}

// Dip to black — fades through solid black at the scene boundary, for moving
// between chapters/acts. Only applies the "in" half at the scene's start; the
// "out" half is handled by the NEXT scene's own dip-to-black-in, so scenes
// don't need to know about their neighbor.
export function DipToBlack({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const half = Math.min(DUR.dipToBlack, Math.floor(durationInFrames / 2));
  const contentOpacity = interpolate(frame, [0, half], [0, 1], { extrapolateRight: "clamp" });
  const blackOpacity = interpolate(
    frame,
    [0, half, durationInFrames - half, durationInFrames],
    [1, 0, 0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: contentOpacity }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ background: "#000", opacity: blackOpacity }} />
    </AbsoluteFill>
  );
}

// No-op wrapper for a hard cut.
export function Cut({ children }) {
  return <AbsoluteFill>{children}</AbsoluteFill>;
}

export function wrapTransition(kind, durationInFrames, children) {
  if (kind === "dip-to-black") return <DipToBlack durationInFrames={durationInFrames}>{children}</DipToBlack>;
  if (kind === "cut") return <Cut>{children}</Cut>;
  return <XFade durationInFrames={durationInFrames}>{children}</XFade>; // default: xfade
}

import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { DUR } from "./config";

// Crossfade in/out at the edges of a scene — for cuts within a sequence/act.
export function XFade({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const d = durationInFrames;
  const f = Math.min(DUR.xfade, Math.floor(d / 2));
  // For a scene long enough to hold a plateau, fade in→hold→out. For a scene
  // too short (d <= 2f) the in/out points would collide (non-strict range,
  // which Remotion rejects), so collapse to a triangular in→out instead.
  let range, out;
  if (f >= 1 && d - f > f) {
    range = [0, f, d - f, d];
    out = [0, 1, 1, 0];
  } else if (d >= 2) {
    range = [0, Math.max(1, Math.floor(d / 2)), d];
    out = [0, 1, 0];
  } else {
    range = [0, 1];
    out = [1, 1];
  }
  const opacity = interpolate(frame, range, out, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
}

// Dip to black — fades through solid black at the scene boundary, for moving
// between chapters/acts. Only applies the "in" half at the scene's start; the
// "out" half is handled by the NEXT scene's own dip-to-black-in, so scenes
// don't need to know about their neighbor.
export function DipToBlack({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const d = durationInFrames;
  const half = Math.max(1, Math.min(DUR.dipToBlack, Math.floor(d / 2)));
  const contentOpacity = interpolate(frame, [0, half], [0, 1], { extrapolateRight: "clamp" });
  // Same short-scene guard as XFade: avoid a colliding (non-strict) range.
  let range, out;
  if (d - half > half) {
    range = [0, half, d - half, d];
    out = [1, 0, 0, 1];
  } else if (d >= 2) {
    range = [0, Math.max(1, Math.floor(d / 2)), d];
    out = [1, 0, 1];
  } else {
    range = [0, 1];
    out = [0, 0];
  }
  const blackOpacity = interpolate(frame, range, out, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
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

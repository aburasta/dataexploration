import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { DUR } from "./config";

// All fade-family transitions are ENTRY-ONLY. Scene A stays at full opacity
// through its tail; scene B fades in on top during the overlap zone driven by
// Documentary.jsx's OVERLAP_FRAMES. That produces a real crossfade instead of
// fade-to-black + fade-in-from-black caused by non-overlapping Sequences.
function FadeCore({ durationInFrames, fadeFrames, children }) {
  const frame = useCurrentFrame();
  const f = Math.min(fadeFrames, Math.floor(durationInFrames / 2));
  const opacity = interpolate(frame, [0, f], [0, 1], { extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
}
export const XFade = (p) => <FadeCore fadeFrames={DUR.xfade} {...p} />;
export const FadeSlow = (p) => <FadeCore fadeFrames={24} {...p} />;
export const FadeFast = (p) => <FadeCore fadeFrames={6} {...p} />;

// Dip-to-black — kept for backward-compat only; new specs must not use it.
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

// Flash-white — quick warm-white punctuation at act pivots. Entry-only: the
// content fades in from white during the first ~8 frames. No overlap with the
// previous scene (this transition IS the boundary).
export function FlashWhite({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const f = Math.min(8, Math.floor(durationInFrames / 2));
  const contentOpacity = interpolate(frame, [0, f], [0, 1], { extrapolateRight: "clamp" });
  const whiteOpacity = interpolate(frame, [0, f], [1, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: contentOpacity }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ background: "#f5f2ea", opacity: whiteOpacity }} />
    </AbsoluteFill>
  );
}

// Zoom-blur — entry-only soft push+blur ramp, distinct feel from a plain fade.
export function ZoomBlur({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const f = Math.min(10, Math.floor(durationInFrames / 2));
  const opacity = interpolate(frame, [0, f], [0, 1], { extrapolateRight: "clamp" });
  const blur = interpolate(frame, [0, f], [8, 0], { extrapolateRight: "clamp" });
  const scale = interpolate(frame, [0, f], [1.04, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity, filter: `blur(${blur}px)`, transform: `scale(${scale})` }}>
      {children}
    </AbsoluteFill>
  );
}

export function Cut({ children }) {
  return <AbsoluteFill>{children}</AbsoluteFill>;
}

export function wrapTransition(kind, durationInFrames, children) {
  const props = { durationInFrames, children };
  switch (kind) {
    case "cut":         return <Cut>{children}</Cut>;
    case "fade-slow":   return <FadeSlow {...props} />;
    case "fade-fast":   return <FadeFast {...props} />;
    case "flash-white": return <FlashWhite {...props} />;
    case "zoom-blur":   return <ZoomBlur {...props} />;
    case "dip-to-black":return <DipToBlack {...props} />; // legacy, avoid
    case "xfade":
    default:            return <XFade {...props} />;
  }
}

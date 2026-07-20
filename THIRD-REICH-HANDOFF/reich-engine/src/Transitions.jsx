import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { DUR } from "./config";

// Parameterised crossfade — length varied per scene for rhythm.
function FadeCore({ durationInFrames, fadeFrames, children }) {
  const frame = useCurrentFrame();
  const f = Math.min(fadeFrames, Math.floor(durationInFrames / 2));
  const opacity = interpolate(
    frame,
    [0, f, durationInFrames - f, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
}
export const XFade = (p) => <FadeCore fadeFrames={DUR.xfade} {...p} />;
export const FadeSlow = (p) => <FadeCore fadeFrames={24} {...p} />;
export const FadeFast = (p) => <FadeCore fadeFrames={6} {...p} />;

// Dip-to-black — kept for backward-compat if any leftover spec still references
// it, but no new spec should use it (per creative direction).
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

// Flash-white — quick bright punctuation at act pivots. Replaces dip-to-black
// where the script wants a beat without going dark.
export function FlashWhite({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const half = Math.min(8, Math.floor(durationInFrames / 2));
  const contentOpacity = interpolate(frame, [0, half], [0, 1], { extrapolateRight: "clamp" });
  const whiteOpacity = interpolate(
    frame,
    [0, half, durationInFrames - half, durationInFrames],
    [0.9, 0, 0, 0.9],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: contentOpacity }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ background: "#f5f2ea", opacity: whiteOpacity }} />
    </AbsoluteFill>
  );
}

// Zoom-blur — a soft push+blur ramp on entry/exit; distinct from a plain fade.
export function ZoomBlur({ durationInFrames, children }) {
  const frame = useCurrentFrame();
  const f = Math.min(10, Math.floor(durationInFrames / 2));
  const opacity = interpolate(frame, [0, f, durationInFrames - f, durationInFrames],
    [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const blurIn = interpolate(frame, [0, f], [8, 0], { extrapolateRight: "clamp" });
  const blurOut = interpolate(frame, [durationInFrames - f, durationInFrames], [0, 8], { extrapolateLeft: "clamp" });
  const blur = frame < durationInFrames - f ? blurIn : blurOut;
  const scaleIn = interpolate(frame, [0, f], [1.04, 1], { extrapolateRight: "clamp" });
  const scaleOut = interpolate(frame, [durationInFrames - f, durationInFrames], [1, 1.04], { extrapolateLeft: "clamp" });
  const scale = frame < durationInFrames - f ? scaleIn : scaleOut;
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
    case "dip-to-black":return <DipToBlack {...props} />; // legacy, avoid in new specs
    case "xfade":
    default:            return <XFade {...props} />;
  }
}

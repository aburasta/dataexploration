import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { SANS } from "./config";

// ── Closing end-card ──────────────────────────────────────────────────────────
// The only scene in the whole documentary allowed on-screen text/graphics —
// every archival scene stays clean, but the final beat is a deliberate
// like-and-subscribe prompt. Solid black backdrop throughout so the whole
// thing self-fades to black at the very end (no next scene to hand off to).
const THUMB_PATH =
  "M2 21h4V9H2v12zm19.83-11.14c.11-.25.17-.52.17-.8V8c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L12.17 1 6.59 6.59C6.22 6.95 6 7.45 6 8v11c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.04c.09-.23.14-.47.14-.71v-1.86l-.17-.31z";
const BELL_PATH =
  "M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z";

export function LikeSubscribeCard({ durationInFrames }) {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const tailFade = Math.round(fps * 1.1);
  const fadeOutStart = durationInFrames - tailFade;
  const masterOpacity = interpolate(frame, [fadeOutStart, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Thumbs-up: pop in with a small overshoot, then a slow idle bob.
  const thumbIn = interpolate(frame, [4, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(1.8)),
  });
  const thumbBob = Math.sin((frame / 40) * Math.PI * 2) * 4;

  // Headline text: fade + rise in just after the thumb.
  const textIn = interpolate(frame, [16, 34], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const textY = interpolate(frame, [16, 34], [16, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // Bell: appears after the text, then rings (rotates) periodically.
  const bellIn = interpolate(frame, [30, 46], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(1.6)),
  });
  const ringCycle = 65;
  const ringPhase = frame % ringCycle;
  const ringT = ringPhase < 14 ? ringPhase / 14 : 0;
  const bellRotate = Math.sin(ringT * Math.PI * 6) * 14 * (1 - ringT);

  // Subtle pulsing glow ring behind the subscribe button.
  const pulse = 1 + Math.sin((frame / 30) * Math.PI * 2) * 0.06;

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill
        style={{
          opacity: masterOpacity,
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          gap: 28,
        }}
      >
        <div
          style={{
            transform: `scale(${thumbIn}) translateY(${thumbBob}px)`,
            opacity: thumbIn,
          }}
        >
          <svg width={150} height={150} viewBox="0 0 24 24" fill="#f2f2f2">
            <path d={THUMB_PATH} />
          </svg>
        </div>

        <div
          style={{
            opacity: textIn,
            transform: `translateY(${textY}px)`,
            fontFamily: SANS,
            fontWeight: 800,
            fontSize: 64,
            letterSpacing: 2,
            color: "#f2f2f2",
            textAlign: "center",
          }}
        >
          LIKE &amp; SUBSCRIBE
        </div>

        <div
          style={{
            opacity: bellIn,
            transform: `scale(${bellIn})`,
            display: "flex",
            alignItems: "center",
            gap: 14,
            marginTop: 6,
          }}
        >
          <div
            style={{
              position: "relative",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: 74,
              height: 74,
              borderRadius: "50%",
              background: "#c0392b",
              transform: `scale(${pulse})`,
            }}
          >
            <svg
              width={38}
              height={38}
              viewBox="0 0 24 24"
              fill="#f2f2f2"
              style={{ transform: `rotate(${bellRotate}deg)`, transformOrigin: "50% 10%" }}
            >
              <path d={BELL_PATH} />
            </svg>
          </div>
          <div
            style={{
              fontFamily: SANS,
              fontWeight: 600,
              fontSize: 30,
              color: "#c9c9c9",
            }}
          >
            for more hidden history
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
}

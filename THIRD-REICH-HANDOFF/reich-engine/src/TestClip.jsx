import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

// Synthetic 3s test clip (solid background + a moving shape) used purely as
// fixture input for ClipScene's verification render — stands in for a real
// downloaded archival clip so the engine can be tested end-to-end without
// needing production footage yet.
export function TestClip() {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 90], [40, 560]);
  return (
    <AbsoluteFill style={{ background: "#2b3a4a" }}>
      <div
        style={{
          position: "absolute",
          top: 140,
          left: x,
          width: 80,
          height: 80,
          borderRadius: 12,
          background: "#e6b800",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: 20,
          left: 20,
          color: "#fff",
          fontFamily: "sans-serif",
          fontSize: 22,
        }}
      >
        TEST CLIP — frame {frame}
      </div>
    </AbsoluteFill>
  );
}

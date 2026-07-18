import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { imageMotion } from "./config";

// ── Still image with documentary Ken Burns motion ────────────────────────────
// A monotonic pan/zoom across the whole scene (see config.imageMotion) plus a
// faint idle float, so archival photographs never sit perfectly still.
export function KenBurnsImage({ scene = {}, mediaDir, durationInFrames }) {
  const frame = useCurrentFrame();
  const src = scene.src ? staticFile(`media/${mediaDir}/${scene.src}`) : null;

  const { transform, opacity } = imageMotion(frame, scene.motion, durationInFrames);

  if (!src) {
    return (
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", background: "#111" }}>
        <div style={{ color: "#889", fontSize: 34, fontFamily: "sans-serif" }}>
          [ missing image: {scene.src || `scene ${scene.n}`} ]
        </div>
      </AbsoluteFill>
    );
  }

  // Every still is scaled to fill the 16:9 frame (cover / center-crop) — no
  // letterboxing, ever. Off-ratio sources are resized to fit and the Ken Burns
  // push/pull sells the crop as intentional framing.
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#000" }}>
      <AbsoluteFill
        style={{
          transform,
          opacity,
          transformOrigin: "center center",
        }}
      >
        <Img
          src={src}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
}

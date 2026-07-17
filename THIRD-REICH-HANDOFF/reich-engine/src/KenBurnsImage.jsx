import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { imageMotion } from "./config";

// A source within this band of 16:9 (1.778) gets the plain full-bleed `cover`
// treatment — the crop is small and the Ken Burns push/pull sells it as
// intentional framing. Outside the band (portraits, extreme panoramas) cover
// would discard too much of the actual photo, so those get a letterbox instead.
const COVER_MIN_RATIO = 1.5; // e.g. 3:2
const COVER_MAX_RATIO = 2.1; // e.g. ~21:9

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

  // aspectRatio is precomputed by the assembly stage (build_spec_*.py) and
  // written into active-episode.json alongside durationSec — probing natural
  // image size at render time is async/unreliable under headless Chrome.
  const ratio = scene.aspectRatio;
  const isOffRatio = typeof ratio === "number" && (ratio < COVER_MIN_RATIO || ratio > COVER_MAX_RATIO);

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#000" }}>
      <AbsoluteFill
        style={{
          transform,
          opacity,
          transformOrigin: "center center",
        }}
      >
        {isOffRatio ? (
          <>
            {/* Blurred, darkened full-bleed backdrop so the frame is never empty. */}
            <Img
              src={src}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "blur(40px) brightness(0.45)",
                transform: "scale(1.15)", // hide blur edge artifacts
              }}
            />
            {/* Full, uncropped image on top — nothing lost. */}
            <Img
              src={src}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                objectFit: "contain",
              }}
            />
          </>
        ) : (
          <Img
            src={src}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
}

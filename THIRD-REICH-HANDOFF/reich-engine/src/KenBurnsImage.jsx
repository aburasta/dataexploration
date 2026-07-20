import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { imageMotion } from "./config";

// Images within this band of 16:9 (1.778) get a plain full-bleed `cover` — the
// crop is small and the Ken Burns push/pull sells it as intentional framing.
// Outside the band (portraits, squares, extreme panoramas) `cover` would chop
// off the actual subject, so those show the WHOLE image (contain) over a soft
// blurred backdrop that fills the 16:9 frame — no black bars, nothing lost.
const COVER_MIN_RATIO = 1.6; // ~3:2 and wider crops cleanly
const COVER_MAX_RATIO = 2.0; // up to ~2:1

// ── Still image with documentary Ken Burns motion ────────────────────────────
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

  // aspectRatio (width/height) is precomputed by spec_gen.py and written into
  // active-episode.json. If it's absent we default to the blurred-fill path,
  // which is always safe (a true 16:9 image fills it edge-to-edge anyway).
  const ratio = scene.aspectRatio;
  const useCover = typeof ratio === "number" && ratio >= COVER_MIN_RATIO && ratio <= COVER_MAX_RATIO;

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#000" }}>
      <AbsoluteFill style={{ transform, opacity, transformOrigin: "center center" }}>
        {useCover ? (
          <Img src={src} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : (
          <>
            {/* Blurred, darkened full-bleed backdrop so the 16:9 frame is never empty. */}
            <Img
              src={src}
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "blur(38px) brightness(0.4)",
                transform: "scale(1.18)", // hide blur edge artifacts
              }}
            />
            {/* The full, uncropped image on top — nothing lost. */}
            <Img
              src={src}
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                objectFit: "contain",
              }}
            />
          </>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
}

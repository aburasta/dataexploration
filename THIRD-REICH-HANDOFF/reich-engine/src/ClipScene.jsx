import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { clipMotion } from "./config";

// ── Archival video clip ───────────────────────────────────────────────────────
// Muted (narration carries the audio track); startTrim seeks into the source
// file; playbackRate stretches/compresses the clip to exactly fill durationSec
// (computed by the assembly stage from source length vs. target span length);
// a barely-there zoom keeps locked-off archival shots from feeling frozen.
export function ClipScene({ scene = {}, mediaDir, durationInFrames }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const src = scene.src ? staticFile(`media/${mediaDir}/${scene.src}`) : null;
  const startFrom = Math.round((scene.startTrim || 0) * fps);

  const { transform } = clipMotion(frame, durationInFrames);

  if (!src) {
    return (
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", background: "#111" }}>
        <div style={{ color: "#889", fontSize: 34, fontFamily: "sans-serif" }}>
          [ missing clip: {scene.src || `scene ${scene.n}`} ]
        </div>
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#000" }}>
      <AbsoluteFill style={{ transform, transformOrigin: "center center" }}>
        <OffthreadVideo
          src={src}
          muted
          startFrom={startFrom}
          playbackRate={scene.playbackRate || 1}
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

import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { FPS, DEFAULT_SPEC } from "./config";
import { KenBurnsImage } from "./KenBurnsImage";
import { ClipScene } from "./ClipScene";
import { MapRoute } from "./MapRoute";
import { LikeSubscribeCard } from "./LikeSubscribeCard";
import { Hemicycle } from "./Hemicycle";
import { wrapTransition } from "./Transitions";

// Overlap frames per transition kind. Scene B starts this many frames BEFORE
// scene A ends, so the two Sequences are simultaneously live during the fade —
// scene A at full opacity, scene B fading in on top → a real crossfade instead
// of a fade-to-black + fade-in-from-black caused by non-overlapping Sequences.
// `cut` and `flash-white` do not overlap (they're their own kind of boundary).
const OVERLAP_FRAMES = {
  xfade: 12,
  "fade-slow": 24,
  "fade-fast": 6,
  "zoom-blur": 10,
  "flash-white": 0,
  cut: 0,
  "dip-to-black": 0, // legacy, avoid
};

function SceneBody({ scene, mediaDir, durationInFrames }) {
  if (scene.type === "clip") return <ClipScene scene={scene} mediaDir={mediaDir} durationInFrames={durationInFrames} />;
  if (scene.type === "map") return <MapRoute scene={scene} mediaDir={mediaDir} durationInFrames={durationInFrames} />;
  if (scene.type === "outro") return <LikeSubscribeCard durationInFrames={durationInFrames} />;
  if (scene.type === "hemicycle") return <Hemicycle scene={scene} durationInFrames={durationInFrames} />;
  return <KenBurnsImage scene={scene} mediaDir={mediaDir} durationInFrames={durationInFrames} />;
}

export function Documentary(props) {
  const spec = props && props.scenes ? props : DEFAULT_SPEC;
  const mediaDir = spec.mediaDir || spec.slug || "";
  const scenes = spec.scenes || [];

  // Visual timeline. `at` tracks the *nominal* start of each scene (as if there
  // were no overlap); the actual Sequence `from` is `at - overlap`, and each
  // Sequence's duration is extended by `overlap` frames so the extra head frames
  // are the crossfade zone. Net timeline length matches sum(durationSec).
  let at = 0;
  const starts = [];
  const visualItems = [];
  scenes.forEach((scene, i) => {
    const dur = Math.round((scene.durationSec || 6) * FPS);
    const overlap = i > 0 ? (OVERLAP_FRAMES[scene.transition] || 0) : 0;
    const from = Math.max(0, at - overlap);
    const spanDur = dur + overlap;
    starts.push(from);
    const body = <SceneBody scene={scene} mediaDir={mediaDir} durationInFrames={spanDur} />;
    const wrapped = wrapTransition(scene.transition, spanDur, body);
    visualItems.push({ from, dur: spanDur, key: `scene-${scene.n ?? i}`, node: wrapped });
    at += dur;
  });

  // Audio timeline — a scene that sets `audio` owns that narration clip for
  // its own duration *plus* every immediately-following scene that has no
  // `audio` of its own. Unchanged from the original engine (used only when a
  // spec uses per-scene audio instead of a global spec.narration track).
  const audioItems = [];
  scenes.forEach((scene, i) => {
    if (!scene.audio) return;
    let span = Math.round((scene.durationSec || 6) * FPS);
    for (let j = i + 1; j < scenes.length && !scenes[j].audio; j++) {
      span += Math.round((scenes[j].durationSec || 6) * FPS);
    }
    audioItems.push({ from: starts[i], dur: span, key: `audio-${scene.n ?? i}`, src: scene.audio });
  });

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {spec.music ? <Audio src={staticFile(`audio/${mediaDir}/${spec.music}`)} volume={0.08} loop /> : null}
      {spec.narration ? <Audio src={staticFile(`audio/${mediaDir}/${spec.narration}`)} /> : null}
      {visualItems.map((it) => (
        <Sequence key={it.key} from={it.from} durationInFrames={it.dur}>
          {it.node}
        </Sequence>
      ))}
      {audioItems.map((it) => (
        <Sequence key={it.key} from={it.from} durationInFrames={it.dur}>
          <Audio src={staticFile(`audio/${mediaDir}/${it.src}`)} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
}

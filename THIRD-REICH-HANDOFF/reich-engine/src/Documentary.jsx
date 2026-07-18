import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { FPS, DEFAULT_SPEC } from "./config";
import { KenBurnsImage } from "./KenBurnsImage";
import { ClipScene } from "./ClipScene";
import { MapRoute } from "./MapRoute";
import { LikeSubscribeCard } from "./LikeSubscribeCard";
import { Hemicycle } from "./Hemicycle";
import { wrapTransition } from "./Transitions";

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

  // Visual timeline — unchanged: one Sequence per scene, each with its own
  // transition. `starts[i]` is scene i's frame offset, reused below.
  let at = 0;
  const starts = [];
  const visualItems = [];
  scenes.forEach((scene, i) => {
    const dur = Math.round((scene.durationSec || 6) * FPS);
    starts.push(at);
    const body = <SceneBody scene={scene} mediaDir={mediaDir} durationInFrames={dur} />;
    const wrapped = wrapTransition(scene.transition, dur, body);
    visualItems.push({ from: at, dur, key: `scene-${scene.n ?? i}`, node: wrapped });
    at += dur;
  });

  // Audio timeline — a scene that sets `audio` owns that narration clip for
  // its own duration *plus* every immediately-following scene that has no
  // `audio` of its own. This lets one narrated span be subdivided into extra
  // silent visual beats (more images/clips cut in) without re-cutting or
  // re-timing the narration at all — the audio file and its start time never
  // move; only how many visual scenes play underneath it can change.
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
      {spec.music ? <Audio src={staticFile(`audio/${mediaDir}/${spec.music}`)} volume={spec.musicVolume ?? 0.08} loop /> : null}
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

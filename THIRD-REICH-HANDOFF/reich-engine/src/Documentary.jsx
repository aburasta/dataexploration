import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { FPS, DEFAULT_SPEC } from "./config";
import { KenBurnsImage } from "./KenBurnsImage";
import { ClipScene } from "./ClipScene";
import { MapRoute } from "./MapRoute";
import { LikeSubscribeCard } from "./LikeSubscribeCard";
import { Hemicycle } from "./Hemicycle";
import { wrapTransition, TransitionIn } from "./Transitions";

// Default entrance length (frames) per transition kind for the overlapping
// timeline. `cut` is instantaneous; slides run a touch longer than dissolves.
const TIN_DEFAULT = { crossfade: 15, "slide-left": 20, "slide-right": 20, cut: 0, xfade: 15 };

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

  // Visual timeline — OVERLAPPING. `starts[i]` stays the narration-aligned
  // offset (cumulative durationSec), so audio timing is unaffected. Each scene's
  // Sequence, however, begins `tin` frames EARLY (from = start - tin) and runs
  // its entrance (crossfade / slide) over that overlap, on top of the previous
  // scene which never fades out — so the frame is never black between scenes.
  // Scene ends stay put, so total duration and narration sync are unchanged.
  let at = 0;
  const starts = [];
  const visualItems = [];
  scenes.forEach((scene, i) => {
    const dur = Math.round((scene.durationSec || 6) * FPS);
    const start = at;
    starts.push(start);
    const kind = scene.transition || "crossfade";
    const tinReq = scene.tin != null ? scene.tin : (TIN_DEFAULT[kind] ?? 15);
    const tin = i === 0 ? 0 : Math.max(0, Math.min(tinReq, dur - 1));
    const from = Math.max(0, start - tin);
    const total = start + dur - from;
    const body = <SceneBody scene={scene} mediaDir={mediaDir} durationInFrames={total} />;
    visualItems.push({ from, dur: total, tin, kind, key: `scene-${scene.n ?? i}`, node: body });
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
      {spec.music ? <Audio src={staticFile(`audio/${mediaDir}/${spec.music}`)} volume={0.08} loop /> : null}
      {spec.narration ? <Audio src={staticFile(`audio/${mediaDir}/${spec.narration}`)} /> : null}
      {visualItems.map((it) => (
        <Sequence key={it.key} from={it.from} durationInFrames={it.dur}>
          <TransitionIn kind={it.kind} tin={it.tin}>{it.node}</TransitionIn>
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

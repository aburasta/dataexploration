import { Composition } from "remotion";
import { Documentary } from "./Documentary";
import { TestClip } from "./TestClip";
import { Hemicycle } from "./Hemicycle";
import { WIDTH, HEIGHT, FPS, computeDuration, DEFAULT_SPEC } from "./config";

export function RemotionRoot() {
  return (
    <>
      <Composition
        id="Documentary"
        component={Documentary}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        defaultProps={DEFAULT_SPEC}
        calculateMetadata={({ props }) => {
          const spec = props && props.scenes ? props : DEFAULT_SPEC;
          return { durationInFrames: computeDuration(spec) };
        }}
      />
      {/* Test-fixture composition: renders a tiny synthetic clip used as ClipScene
          input for the engine's own verification render (see README). */}
      <Composition
        id="TestClip"
        component={TestClip}
        fps={FPS}
        width={640}
        height={360}
        durationInFrames={90}
      />
      {/* Prototype preview: special-legal-coup-1919-1933 — 1928 election (12/491 seats) */}
      <Composition
        id="HemicyclePreview1928"
        component={Hemicycle}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        durationInFrames={120}
        defaultProps={{
          scene: {
            segments: [
              { count: 12, color: "#c0392b", label: "NSDAP" },
              { count: 479, color: "#4a4a4a" },
            ],
          },
          durationInFrames: 120,
        }}
      />
      {/* Prototype preview: Sept 1930 election (107/491 seats) */}
      <Composition
        id="HemicyclePreview1930"
        component={Hemicycle}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        durationInFrames={120}
        defaultProps={{
          scene: {
            segments: [
              { count: 107, color: "#c0392b", label: "NSDAP" },
              { count: 384, color: "#4a4a4a" },
            ],
          },
          durationInFrames: 120,
        }}
      />
      {/* Prototype preview: 1932 presidential runoff, vote-share mode */}
      <Composition
        id="HemicyclePreviewRunoff1932"
        component={Hemicycle}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        durationInFrames={120}
        defaultProps={{
          scene: {
            total: 100,
            segments: [
              { count: 37, color: "#c0392b", label: "Hitler" },
              { count: 53, color: "#4a6fa5", label: "Hindenburg" },
              { count: 10, color: "#4a4a4a", label: "Other" },
            ],
          },
          durationInFrames: 120,
        }}
      />
    </>
  );
}

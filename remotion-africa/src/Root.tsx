import { Composition } from "remotion";
import { AccraToKampala } from "./AccraToKampala";
import { TroopAdvance } from "./TroopAdvance";
import { PrinceInk } from "./PrinceInk";
import { ReelOpen } from "./ReelOpen";
import { ReelFull } from "./ReelFull";
import { VIDEO_WIDTH, VIDEO_HEIGHT } from "./geo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AccraToKampala"
        component={AccraToKampala}
        durationInFrames={420}
        fps={30}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
      <Composition
        id="TroopAdvance"
        component={TroopAdvance}
        durationInFrames={400}
        fps={30}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
      <Composition
        id="PrinceInk"
        component={PrinceInk}
        durationInFrames={300}
        fps={30}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
      <Composition
        id="ReelOpen"
        component={ReelOpen}
        durationInFrames={1800}
        fps={30}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
      <Composition
        id="ReelFull"
        component={ReelFull}
        durationInFrames={17160}
        fps={30}
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
      />
    </>
  );
};

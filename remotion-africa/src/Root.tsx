import { Composition } from "remotion";
import { AccraToKampala } from "./AccraToKampala";
import { VIDEO_WIDTH, VIDEO_HEIGHT } from "./geo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="AccraToKampala"
      component={AccraToKampala}
      durationInFrames={420}
      fps={30}
      width={VIDEO_WIDTH}
      height={VIDEO_HEIGHT}
    />
  );
};

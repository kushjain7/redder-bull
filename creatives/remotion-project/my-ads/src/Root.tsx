import "./index.css";
import { Composition } from "remotion";

// ── Starter Templates ────────────────────────────────────────────────────────
import { ReelTemplate } from "./templates/ReelTemplate";
import { FeedTemplate } from "./templates/FeedTemplate";

// ── Add your brief compositions below ────────────────────────────────────────
// import { AdBrief001Reel } from "./AdBrief001Reel";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ── STARTER TEMPLATES (reference — duplicate and customize) ── */}
      <Composition
        id="ReelTemplate"
        component={ReelTemplate}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="FeedTemplate"
        component={FeedTemplate}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1080}
      />

      {/* ── YOUR BRIEF COMPOSITIONS GO HERE ──
      <Composition
        id="AdBrief001Reel"
        component={AdBrief001Reel}
        durationInFrames={450}   // 15s × 30fps
        fps={30}
        width={1080}
        height={1920}
      />
      */}
    </>
  );
};

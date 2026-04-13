/**
 * Root.tsx — Remotion Composition Registry
 * Leonardo (Creative Engine) adds new compositions here for each brief.
 *
 * INSTRUCTIONS FOR LEONARDO:
 * 1. Create a new file: src/AdBrief[N][Format].tsx (copy from src/templates/)
 * 2. Import it below
 * 3. Add a <Composition> entry with correct dimensions and duration
 * 4. Run: npx remotion studio (to preview)
 * 5. Run: npx remotion render [id] --output ../../rendered/brief-[N].mp4
 */

import "./index.css";
import { Composition } from "remotion";

// ── Starter Templates (for reference / testing) ──────────────────────────────
import { ReelTemplate } from "./templates/ReelTemplate";
import { FeedTemplate } from "./templates/FeedTemplate";

// ── Brief Compositions (Leonardo adds these as briefs come in) ───────────────
// import { AdBrief001Reel } from "./AdBrief001Reel";
// import { AdBrief002Feed } from "./AdBrief002Feed";
// import { AdBrief003Story } from "./AdBrief003Story";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ── Starter Templates (preview & reference) ── */}
      <Composition
        id="ReelTemplate"
        component={ReelTemplate}
        durationInFrames={450}  // 15s × 30fps
        fps={30}
        width={1080}
        height={1920}           // 9:16
      />

      <Composition
        id="FeedTemplate"
        component={FeedTemplate}
        durationInFrames={1}    // Static image — render 1 frame
        fps={30}
        width={1080}
        height={1080}           // 1:1
      />

      {/*
       * ── Brief Compositions (Leonardo uncomments as briefs come in) ──
       *
       * <Composition
       *   id="AdBrief001Reel"
       *   component={AdBrief001Reel}
       *   durationInFrames={450}   // 15s
       *   fps={30}
       *   width={1080}
       *   height={1920}
       * />
       *
       * <Composition
       *   id="AdBrief002Feed"
       *   component={AdBrief002Feed}
       *   durationInFrames={1}     // static
       *   fps={30}
       *   width={1080}
       *   height={1080}
       * />
       *
       * <Composition
       *   id="AdBrief003Story"
       *   component={AdBrief003Story}
       *   durationInFrames={450}
       *   fps={30}
       *   width={1080}
       *   height={1920}
       * />
       */}
    </>
  );
};

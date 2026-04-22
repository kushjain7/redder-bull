import "./index.css";
import { Composition } from "remotion";

// ── Starter Templates (always committed — product-free) ───────────────────────
import { ReelTemplate } from "./templates/ReelTemplate";
import { FeedTemplate } from "./templates/FeedTemplate";

// ── Campaign Compositions ─────────────────────────────────────────────────────
// Product-specific compositions live in `src/campaigns/` (gitignored).
// To add a new campaign:
//   1. Create src/campaigns/AdBrief[NNN][Format].tsx
//   2. Import it below and register a <Composition> block
//   3. src/campaigns/ is in .gitignore — only your machine ever sees it
//
// Example (uncomment and fill in real values):
//
// import { AdBrief001Reel } from "./campaigns/AdBrief001Reel";
// <Composition
//   id="AdBrief001Reel"
//   component={AdBrief001Reel}
//   durationInFrames={900}     // match composition fps × duration
//   fps={30}                   // MUST match source video fps (see skills/video-laws.md)
//   width={1080}
//   height={1920}
// />

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ── STARTER TEMPLATES (reference — duplicate into campaigns/ and customize) ── */}
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
    </>
  );
};

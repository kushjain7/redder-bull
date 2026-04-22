import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

// ── Font preloads — called once so Remotion bundles them ──────────────────────
import { loadFont as loadSpaceGrotesk } from "@remotion/google-fonts/SpaceGrotesk";
import { loadFont as loadJetBrainsMono } from "@remotion/google-fonts/JetBrainsMono";
import { loadFont as loadFraunces } from "@remotion/google-fonts/Fraunces";

loadSpaceGrotesk();
loadJetBrainsMono();
loadFraunces();

registerRoot(RemotionRoot);

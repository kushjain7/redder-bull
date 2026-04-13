import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
// Font preloads — called once so Remotion bundles them
import { loadFont as loadSpaceGrotesk } from "@remotion/google-fonts/SpaceGrotesk";
import { loadFont as loadJetBrainsMono } from "@remotion/google-fonts/JetBrainsMono";

loadSpaceGrotesk();
loadJetBrainsMono();

registerRoot(RemotionRoot);

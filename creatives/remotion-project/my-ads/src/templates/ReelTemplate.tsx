/**
 * ReelTemplate.tsx — Leonardo (Creative Engine)
 *
 * Instagram/Facebook Reel template: 9:16 (1080×1920), 30fps
 * Safe zones: 150px top, 170px bottom
 *
 * HOW TO USE:
 * 1. Copy this file and rename it: AdBrief001Reel.tsx
 * 2. Replace all "REPLACE:" comments with content from the creative brief
 * 3. Register the composition in Root.tsx
 * 4. Render: npx remotion render AdBrief001Reel --output ../../../rendered/brief-001.mp4
 */

import React from "react";
import {
  AbsoluteFill,
  spring,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { loadFont as loadSpaceGrotesk } from "@remotion/google-fonts/SpaceGrotesk";

// Load fonts here so they are only bundled when this composition is active.
loadSpaceGrotesk();

// ─── Brand Config (fill from state/product-context.md) ──────────────────────
const BRAND = {
  background: "#1A1A2E",    // REPLACE: brand background color
  primary: "#FF6B35",       // REPLACE: brand primary / CTA color
  textLight: "#FFFFFF",
  textDark: "#1A1A2E",
  // font: loaded separately if using Google Fonts
};

// ─── Ad Copy (fill from creative brief) ─────────────────────────────────────
const COPY = {
  hook: "Your Hook Here",               // REPLACE: exact hook text from brief (first 3s)
  body: "Your main message here.",      // REPLACE: body copy from brief script
  cta: "Start Now →",                   // REPLACE: CTA text from brief
};

// ─── Timeline (frames at 30fps) ─────────────────────────────────────────────
const T = {
  hookEnd: 90,          // 3 seconds — end of hook phase
  bodyStart: 100,       // when main content begins
  bodyEnd: 360,         // when main content ends
  ctaStart: 360,        // when CTA appears
};

export const ReelTemplate: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Hook animations
  const hookOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  const hookScale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 130 },
  });

  // Body animations
  const bodyOpacity = interpolate(frame, [T.bodyStart, T.bodyStart + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // CTA animations
  const ctaOpacity = interpolate(frame, [T.ctaStart, T.ctaStart + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ctaScale = spring({
    frame: Math.max(0, frame - T.ctaStart),
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  const showHook = frame <= T.hookEnd;
  const showBody = frame > T.bodyStart && frame <= T.bodyEnd;
  const showCta = frame > T.ctaStart;

  return (
    <AbsoluteFill style={{ backgroundColor: BRAND.background }}>
      {/*
       * SAFE ZONE: All content must stay within:
       *   top: 150px (platform status bar)
       *   bottom: 170px (like/comment/share buttons)
       *   left/right: 40px
       */}
      <div
        style={{
          position: "absolute",
          top: 150,
          bottom: 170,
          left: 40,
          right: 40,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 40,
        }}
      >
        {/* ── HOOK (frames 0 → hookEnd) ── */}
        {showHook && (
          <div
            style={{
              opacity: hookOpacity,
              transform: `scale(${hookScale})`,
              fontSize: 72,        // min 56px for headlines
              fontWeight: 900,
              color: BRAND.textLight,
              textAlign: "center",
              lineHeight: 1.2,
              padding: "0 20px",
            }}
          >
            {COPY.hook}
          </div>
        )}

        {/* ── BODY CONTENT (frames bodyStart → bodyEnd) ── */}
        {showBody && (
          <div
            style={{
              opacity: bodyOpacity,
              textAlign: "center",
              padding: "0 20px",
            }}
          >
            <p
              style={{
                fontSize: 40,       // min 36px for body
                color: BRAND.textLight,
                lineHeight: 1.6,
                margin: 0,
              }}
            >
              {COPY.body}
            </p>
          </div>
        )}

        {/* ── CTA (frames ctaStart → end) ── */}
        {showCta && (
          <div
            style={{
              opacity: ctaOpacity,
              transform: `scale(${ctaScale})`,
              backgroundColor: BRAND.primary,
              paddingTop: 24,
              paddingBottom: 24,
              paddingLeft: 56,
              paddingRight: 56,
              borderRadius: 14,
              fontSize: 48,       // min 40px for CTA
              fontWeight: 700,
              color: BRAND.textLight,
              textAlign: "center",
            }}
          >
            {COPY.cta}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

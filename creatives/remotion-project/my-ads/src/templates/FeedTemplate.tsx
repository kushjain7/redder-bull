/**
 * FeedTemplate.tsx — Leonardo (Creative Engine)
 *
 * Instagram/Facebook Feed static ad: 1:1 (1080×1080)
 * Safe zones: 60px top/bottom, 40px sides
 *
 * HOW TO USE:
 * 1. Copy this file and rename it: AdBrief002Feed.tsx
 * 2. Replace all "REPLACE:" comments with content from the creative brief
 * 3. Register in Root.tsx (durationInFrames: 1 for static render)
 * 4. Render still: npx remotion still AdBrief002Feed --frame 0 --output ../../../rendered/brief-002.png
 */

import React from "react";
import { AbsoluteFill } from "remotion";
import { loadFont as loadSpaceGrotesk } from "@remotion/google-fonts/SpaceGrotesk";

// Load fonts here so they are only bundled when this composition is active.
loadSpaceGrotesk();
// import { Img, staticFile } from "remotion"; // Uncomment when adding product images

// ─── Brand Config (fill from state/product-context.md) ──────────────────────
const BRAND = {
  background: "#FFFFFF",    // REPLACE: brand background color
  primary: "#FF6B35",       // REPLACE: brand primary / CTA color
  headline: "#1A1A2E",      // REPLACE: headline text color
  textLight: "#FFFFFF",
  textMuted: "#666666",
};

// ─── Ad Copy (fill from creative brief) ─────────────────────────────────────
const COPY = {
  headline: "Your Headline Here",       // REPLACE: from brief — min 56px
  subtext: "Supporting message here.",  // REPLACE: from brief — min 36px
  cta: "Shop Now",                       // REPLACE: CTA text from brief
};

export const FeedTemplate: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: BRAND.background }}>
      {/*
       * SAFE ZONE: All content must stay within:
       *   top: 60px, bottom: 60px, left: 40px, right: 40px
       */}
      <div
        style={{
          position: "absolute",
          top: 60,
          bottom: 60,
          left: 40,
          right: 40,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          alignItems: "flex-start",
        }}
      >
        {/* ── HEADLINE ── */}
        <div
          style={{
            fontSize: 64,       // min 56px for headlines
            fontWeight: 900,
            color: BRAND.headline,
            lineHeight: 1.2,
            maxWidth: "85%",
          }}
        >
          {COPY.headline}
        </div>

        {/* ── PRODUCT IMAGE AREA ── */}
        <div
          style={{
            flex: 1,
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "30px 0",
          }}
        >
          {/*
           * REPLACE: Add product image here.
           * Place image in: creatives/remotion-project/my-ads/public/product.png
           * Then use: <Img src={staticFile("product.png")} style={{ maxHeight: 400 }} />
           */}
          <div
            style={{
              width: "100%",
              height: 400,
              backgroundColor: "#F0F0F0",
              borderRadius: 16,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: BRAND.textMuted,
              fontSize: 32,
            }}
          >
            {/* REPLACE: <Img src={staticFile("product.png")} style={{ maxHeight: 400, borderRadius: 16 }} /> */}
            Product Image Here
          </div>
        </div>

        {/* ── SUBTEXT + CTA ROW ── */}
        <div
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 20,
          }}
        >
          {/* Subtext */}
          <p
            style={{
              fontSize: 36,       // min 36px for body
              color: BRAND.textMuted,
              margin: 0,
              flex: 1,
              lineHeight: 1.4,
            }}
          >
            {COPY.subtext}
          </p>

          {/* CTA Button */}
          <div
            style={{
              backgroundColor: BRAND.primary,
              paddingTop: 20,
              paddingBottom: 20,
              paddingLeft: 40,
              paddingRight: 40,
              borderRadius: 12,
              fontSize: 40,       // min 40px for CTA
              fontWeight: 700,
              color: BRAND.textLight,
              whiteSpace: "nowrap",
              flexShrink: 0,
            }}
          >
            {COPY.cta}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

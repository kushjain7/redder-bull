# Design Laws — Universal Rules for All Ad Creatives

> **Authority:** Single source of truth for layout, typography, safe zones, and contrast.
> **Supersedes** any conflicting values in `skills/remotion/SKILL.md` or `skills/orchestrator/SKILL.md`.
> **Read by:** Leonardo (before writing any component), Zimmer (during visual QC).

---

## D1 — Safe Zones (Instagram Reels 9:16 · 1080×1920)

These are the ONLY authoritative values. Do not use values from any other file.

```
Frame: 1080 × 1920 px

SAFE_T = 180       // Top: platform status bar + account name
SAFE_B = 380       // Bottom: Instagram caption, like/comment/share/audio bar
SAFE_R = 110       // Right: Instagram vertical button column (follow, heart, comment, share)
SAFE_L = 0         // Left: no platform UI (safe to use full left edge)
```

**Safe content area:**
- Width: `1080 - 0 - 110 = 970px`
- Height: `1920 - 180 - 380 = 1360px`
- Top-left of safe area: `(0, 180)`
- Bottom-right of safe area: `(970, 1540)`

**In code:**
```tsx
const SAFE_T = 180;
const SAFE_B = 380;
const SAFE_R = 110;
const SAFE_CONTENT_HEIGHT = 1920 - SAFE_T - SAFE_B; // 1360
```

**Rule:** No text, no CTA, no logo, no important visual element may fall inside the top `SAFE_T` pixels or the bottom `SAFE_B` pixels. Always position critical elements with:
```tsx
bottom: SAFE_B + 20   // 20px breathing room above the platform bar
top: SAFE_T + 20      // 20px breathing room below the platform bar
```

---

## D2 — Safe Zones (Instagram Feed 1:1 · 1080×1080)

```
SAFE_T = 60   // Top
SAFE_B = 60   // Bottom
SAFE_L = 40   // Left
SAFE_R = 40   // Right
```

---

## D3 — Typography Minimums (9:16 Reels)

These are **floor values** — never go below them.

| Element | Min Size | Font | Notes |
|---|---|---|---|
| Hook / hero headline | **64px** | Space Grotesk Bold | First 3 seconds — max impact |
| Graphic overlay headline | **62px** | Space Grotesk SemiBold | Readable at arm's length |
| Caption (phrase-level) | **48px** | Space Grotesk SemiBold | Bottom bar captions |
| Body / supporting text | **36px** | Space Grotesk Regular | Secondary info |
| Label / badge / chip | **28px** | Space Grotesk Medium | Tags, counters |
| End-card CTA | **52px** | Space Grotesk Bold | Must be readable in <0.5s |
| Logo / wordmark lockup | **72px** wide | — | As measured horizontally |

**WCAG AA minimum contrast:** 4.5:1 text-to-background. Verify with `scripts/qc/contrast.py`.

---

## D4 — Caption Layer Rules (UGC / talking-head / VO formats)

Captions are phrase-level (not word-by-word karaoke):

1. **Sync:** Each phrase appears at the moment the speaker starts saying it. Never more than 0.5s early or late.
2. **Duration:** Each phrase stays visible until 0.2s after the speaker finishes it (or the next phrase starts, whichever is sooner).
3. **Size:** 48px minimum (D3).
4. **Contrast:** Always use a dark pill background `rgba(0,0,0,0.65)` with 12px horizontal padding and 6px vertical padding, OR a 3px stroke in the brand's darkest color. A UGC creator wearing dark clothing + a bright white wall will have both dark and bright regions simultaneously — the pill is mandatory.
5. **Position:** `bottom: SAFE_B + 20` (never lower). Center-aligned horizontally.
6. **Max width:** 80% of frame width (`0.8 × 1080 = 864px`). Wrap to a second line rather than overflow.

---

## D5 — Graphic Overlay Rules (call-outs, stats, price reveals)

Graphic overlays are distinct from captions — they are **designed elements** with their own visual treatment.

1. **Minimum size:** 62px (D3).
2. **Backing required** when video background is mixed (e.g., dark clothing + white wall): add a brand-color pill, card, or semi-transparent backdrop. Never float text over a busy, mixed background without a backing element.
3. **Position:** At or above vertical center of the safe content area. Never compete with captions at the bottom. Suggested range: `SAFE_T + 80` to `1920/2` (px from top).
4. **Animation:** spring entry (damping 14, stiffness 160) — snappy, not floaty. Duration: enter in 12 frames, exit in 8 frames.
5. **Stay time:** On-screen for at least 1.2s before exiting (long enough to read at a glance).

---

## D6 — Phone / Device Insert Rules

When a phone mockup or device frame is shown as an insert element:

1. **Minimum width:** 540px (50% of the 1080px frame).
2. **Bezel color:** Match brand or use neutral dark (#1A1A1A). Never pure white — it bleeds into white walls in UGC.
3. **Position:** Center of frame or slightly left/right of center. Never cut off by `SAFE_R`.
4. **Verification:** After render, run `scripts/qc/find_insert.py` to confirm bbox ≥540px wide.

---

## D7 — End-Card Rules

Every video creative must end with an end-card:

1. **Duration:** 1.5s minimum.
2. **Content:** Logo/brand mark + CTA text + optional URL.
3. **Background:** Solid brand color or strong gradient — NOT a frozen video frame.
4. **Logo size:** ≥72px wide (D3).
5. **CTA text:** ≥52px (D3).
6. **All text in safe zone:** No element within `SAFE_T`, `SAFE_B`, or `SAFE_R`.

---

## Quick Reference

| Constant | Value | Description |
|---|---|---|
| `SAFE_T` | 180 | Top safe zone — 9:16 Reels |
| `SAFE_B` | 380 | Bottom safe zone — 9:16 Reels |
| `SAFE_R` | 110 | Right safe zone — 9:16 Reels |
| Min caption size | 48px | Phrase captions, pill background mandatory |
| Min overlay size | 62px | Graphic call-outs, backing mandatory on mixed BG |
| Min hook size | 64px | Hero headline, first 3 seconds |
| Min phone insert width | 540px | Device mockup inserts |
| Min logo width | 72px | End-card / watermark |
| WCAG contrast | 4.5:1 | All text elements |

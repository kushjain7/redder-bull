# Remotion Project — Ad Creative Production

## Setup (Run Once)

```bash
cd creatives/remotion-project
npx create-video@latest my-ads --template hello-world
cd my-ads
npm install
npx remotion studio
# Should open browser at localhost:3000 — Ctrl+C to stop
```

## Project Structure (after setup)

```
my-ads/
├── src/
│   ├── Root.tsx              ← Register all compositions here
│   ├── index.ts              ← Entry point
│   ├── AdBrief001Reel.tsx    ← Brief 001 video (created by Creative Engine)
│   ├── AdBrief002Feed.tsx    ← Brief 002 static (created by Creative Engine)
│   └── templates/
│       └── README.md         ← Ad format specifications
├── public/
│   └── logo.png              ← Copy brand logo here
└── package.json
```

## Render Commands

```bash
cd creatives/remotion-project/my-ads

# Render video:
npx remotion render AdBrief001Reel --output ../../rendered/brief-001.mp4

# Render static image:
npx remotion still AdBrief002Feed --frame 0 --output ../../rendered/brief-002.png

# Preview in browser:
npx remotion studio
```

## Ad Format Quick Reference

| Format | Dimensions | Duration | Command Flag |
|---|---|---|---|
| Instagram Reel | 1080×1920 | 15–30s | `--width 1080 --height 1920` |
| Instagram Story | 1080×1920 | ≤15s | `--width 1080 --height 1920` |
| Instagram Feed | 1080×1080 | N/A (static) | `--width 1080 --height 1080` |
| Facebook Feed | 1080×1080 | 15–60s | `--width 1080 --height 1080` |

## Safe Zones

- **9:16 (Reels/Stories):** Content must stay between y=150 and y=1750 (top 150px, bottom 170px reserved)
- **1:1 (Feed):** 60px top/bottom, 40px sides

## Font Notes

- English: Inter, Arial, or any Google Font via `@remotion/google-fonts`
- Hindi/Hinglish: **Noto Sans Devanagari** — mandatory

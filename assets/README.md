# Assets Library

All production assets for Redder Bull creatives live here. Two types:

```
assets/
├── static/          ← Permanent, reusable across all campaigns and cycles
│   ├── sfx/
│   │   ├── transitions/   ← Whooshes, swipes, sweeps — used between scenes
│   │   ├── impacts/       ← Punches, thuds, drums — used on key text/elements
│   │   ├── risers/        ← Build-ups, rises, tension builders — used before reveals
│   │   ├── ambience/      ← Background room tone, city hum, tech hum
│   │   └── ui/            ← Typing, clicks, notifications, pop
│   ├── brand/         ← Logo files, brand color swatches, brand reference images
│   ├── fonts/         ← Any custom/licensed fonts (Space Grotesk + JetBrains Mono are via npm)
│   └── overlays/      ← Reusable visual overlays: grain, vignette, light leaks
│
└── dynamic/         ← Campaign-specific assets — one subfolder per cycle/brief
    ├── cycle-001/
    │   ├── brief-001/
    │   │   ├── stock-video/   ← Stock footage for this brief
    │   │   ├── stock-images/  ← Product photos, lifestyle images
    │   │   ├── music/         ← Background music track for this creative
    │   │   └── ASSET-REQUEST.md  ← What Tanmay asked for; what's been provided
    │   └── ...
    └── cycle-002/
        └── ...
```

## Rules

- **Static assets** are committed to git (keep files small — no raw video in static/).
- **Dynamic assets** are NOT committed to git (see `.gitignore`) — they're too large and campaign-specific.
- When Tanmay writes a brief and lists required assets, Zimmer creates the correct `dynamic/cycle-N/brief-N/` folder and writes an `ASSET-REQUEST.md`.
- You (the human) drop your files into the correct subfolder.
- Leonardo checks `assets/static/sfx/` for standard sounds before generating them.

## SFX Naming Convention

All static SFX follow this pattern: `[category]-[descriptor]-[variant].mp3`

Examples:
- `transitions/whoosh-fast-01.mp3`
- `transitions/whoosh-soft-01.mp3`
- `impacts/thud-low-01.mp3`
- `impacts/punch-mid-01.mp3`
- `risers/riser-cinematic-01.mp3`
- `risers/riser-electronic-01.mp3`
- `ui/typing-fast-01.mp3`
- `ui/pop-soft-01.mp3`

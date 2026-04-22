# Assets Library

All production assets for Redder Bull creatives live here. Three types:

```
assets/
├── static/                  ← Permanent, reusable across all campaigns
│   ├── sfx/
│   │   ├── transitions/       ← Whooshes, swipes, sweeps
│   │   ├── impacts/           ← Punches, thuds, drums
│   │   ├── risers/            ← Build-ups, rises, tension builders
│   │   ├── ambience/          ← Room tone, city hum, tech hum
│   │   └── ui/                ← Typing, clicks, notifications, pop
│   ├── brand/               ← Logo files, color swatches, reference images
│   ├── fonts/               ← Custom/licensed fonts
│   └── overlays/            ← Grain, vignette, light leaks
│
└── dynamic/                 ← Campaign-specific, filed by creative category (gitignored)
    ├── brand-assets/        ← Product UI screenshots, logo, homepage reference
    │                          (no asset-request needed — use freely for screen-recording
    │                           and brand-color briefs). Exact path set in product-context.md.
    └── {category}/{subcategory}/{YYYY-MM}/{YYYY-Www}/brief-{NNN}/
        ├── stock-video/       ← Stock footage for this brief
        ├── stock-images/      ← Product photos, lifestyle images
        ├── music/             ← Background music track
        └── ASSET-REQUEST.md   ← What Tanmay asked for; what's been provided
```

## Rules

- **Static assets** are committed to git (keep files small — no raw video in static/).
- **Dynamic assets** are NOT committed (see `.gitignore`) — they're too large and campaign-specific.
- Place product-specific brand files (UI screenshots, logo) under `assets/dynamic/brand-assets/`. This folder is gitignored.
- When Tanmay writes a brief and lists required assets, Zimmer creates the correct `dynamic/{category}/{subcategory}/{YYYY-MM}/{YYYY-Www}/brief-{NNN}/` subtree and writes an `ASSET-REQUEST.md` inside it.
- You (the human) drop your files into the correct subfolder.
- Leonardo checks `assets/static/sfx/` for standard sounds before generating them.
- Leonardo checks `assets/dynamic/brand-assets/` for product UI, logo, and brand-look reference before asking for new screenshots.

## Category-Sorted Dynamic Paths

Every campaign asset is filed under the same taxonomy as briefs and rendered creatives (see `creatives/CATEGORIES.md`):

```
assets/dynamic/ugc/confessional/{YYYY-MM}/{YYYY-Www}/brief-{NNN}/
assets/dynamic/screen-recording/chat-demo/{YYYY-MM}/{YYYY-Www}/brief-{NNN}/
assets/dynamic/static-visual/quote-card/{YYYY-MM}/{YYYY-Www}/brief-{NNN}/
```

This mirrors `briefs/` and `creatives/rendered/` so a single `grep` or `find` by category/subcategory retrieves the brief, the asset pack, the render, and the review doc together.

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

## Product Brand Assets — Quick Index

Place your product's brand assets in `assets/dynamic/brand-assets/`. Document them in `state/product-context.md` so every agent knows the file names without guessing.

Typical files to add:
- **Logo** — transparent PNG, min 512×512px. Use for end-cards, watermarks, brand cameos.
- **UI screenshots** — key product screens useful for screen-recording briefs.
- **Homepage screenshot** — useful for brand-color extraction and first-impression frames.
- **Brand color reference** — document hex values in `state/product-context.md`, not here.

The `assets/dynamic/` folder is gitignored — add your files there and they stay local.

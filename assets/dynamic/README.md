# Dynamic Assets

Campaign-specific assets live here. One folder per cycle, one subfolder per brief.

**This folder is NOT committed to git** (too large, too campaign-specific).

## How it works

1. Tanmay writes a brief and includes an **Asset Request** section
2. Zimmer creates `cycle-N/brief-N/ASSET-REQUEST.md` listing exactly what's needed
3. You drop your files into the correct subfolder
4. Zimmer confirms receipt in `state/outputs/current.md` and unblocks Leonardo

## Folder structure (created automatically by Zimmer)

```
dynamic/
└── cycle-001/
    ├── brief-001/
    │   ├── stock-video/        ← e.g. product demo clip, lifestyle footage
    │   ├── stock-images/       ← e.g. product photo, hero image
    │   ├── music/              ← background music track (MP3)
    │   └── ASSET-REQUEST.md    ← what was asked, what was provided, status
    ├── brief-002/
    │   └── ...
    └── brief-003/
        └── ...
```

## ASSET-REQUEST.md template

Zimmer writes this file. You fill in the "PROVIDED" column.

```markdown
# Asset Request — Cycle [N] / Brief [N]
**Requested by:** Tanmay | **Reviewed by:** Zimmer | **Date:** [DATE]

| Asset | Description | Format | Status | File placed at |
|---|---|---|---|---|
| Product logo | Transparent background, min 512×512px | PNG | ⏳ Needed | — |
| Hero product photo | White background | JPG/PNG | ⏳ Needed | — |
| Background music | [mood/genre from brief] | MP3 | ⏳ Needed | — |

Drop files into this folder's subfolders and update the Status column.
```

# Avatar Library

This folder contains the reusable character image library for UGC video generation via Higgsfield.

---

## Purpose

These images are the "seed" images uploaded to Higgsfield's image-to-video API. The first chunk of every UGC clip uses one of these images; subsequent chunks use the last frame of the previous clip (for character consistency).

---

## File Naming Convention

```
{gender}_{age-band}_{vibe}_{index}.jpg
```

| Segment | Valid values |
|---|---|
| `gender` | `female`, `male`, `neutral` |
| `age-band` | `18-24`, `25-30`, `30-35`, `35-45` |
| `vibe` | `casual`, `aspirational`, `professional`, `energetic`, `relatable`, `tech-savvy` |
| `index` | Two-digit integer: `01`, `02`, ... |

**Examples:**
- `female_25-30_casual_01.jpg`
- `male_30-35_professional_02.jpg`
- `female_18-24_energetic_01.jpg`

---

## Image Requirements

For best results with Higgsfield's image-to-video models:

| Property | Requirement |
|---|---|
| Aspect ratio | **9:16 portrait** (1080×1920 or proportional) |
| Resolution | Minimum 512×910px; prefer 1080×1920 |
| Format | JPEG or PNG |
| Subject | Single person, clearly visible face, direct or slight off-axis gaze |
| Background | Clean, solid, or subtly blurred |
| Expression | Neutral to mild positive — avoid strong emotion (model adds the emotion) |
| Lighting | Even, front-lit or soft side-lit — avoid harsh shadows |
| Clothing | Context-appropriate to the `vibe` tag (casual = everyday clothes, professional = clean top/blazer) |

---

## Metadata

Every avatar MUST have a corresponding entry in `_metadata.json`. The pick-avatar script reads this file.

---

## Who adds avatars?

The human operator (you) adds avatar images to this folder. Drop the image in, follow the naming convention, and add an entry to `_metadata.json`.

Leonardo will select avatars using `scripts/higgsfield/pick-avatar.py` based on brief tags.

---

## Committed vs. gitignored

This folder is **committed** to the repo. Avatars here are generic, reusable across all products. Never commit product-specific photos (e.g., a real person's headshot associated with a brand) — those go in `assets/dynamic/`.

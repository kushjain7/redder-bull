# Creative Category Taxonomy

> **Owner:** Zimmer (Orchestrator)
> **Single source of truth.** Every brief, render, review doc, and dynamic asset folder is filed against this taxonomy.

All creative output — both the thinking (briefs, reviews) and the finished work (renders, assets) — is organized as:

```
{category}/{subcategory}/{YYYY-MM}/{YYYY-Www}/
```

- **Category (L1)** — the broad production format. Fixed list below. Adding a new L1 category requires a deliberate decision (update this file + Zimmer's SKILL.md).
- **Subcategory (L2)** — the specific creative pattern inside the category. Grows organically. When Tanmay proposes a new subcategory in a brief, Zimmer adds it here.
- **Month** — `YYYY-MM` of the brief's write date (e.g. `2026-04`).
- **Week** — ISO week of the brief's write date (e.g. `2026-W17`, the week starting Monday 20 April 2026).

---

## Level-1 Categories (fixed)

| Slug | Category | What it is | Typical format |
|---|---|---|---|
| `ugc` | **UGC** | Creator/user-generated feel. Vertical selfie-mode, amateur lighting, first-person voice. Feels like a friend, not an ad. | Reel 9:16 video |
| `screen-recording` | **Screen-Recording** | POV of the product being used — phone or laptop screen is the main character. Chat demos, onboarding walkthroughs, feature discovery. | Reel 9:16 / Story 9:16 |
| `talking-head` | **Talking-Head** | A single person addressing camera. Creator, founder, expert, educator. Polished but conversational. | Reel 9:16 / Feed 1:1 video |
| `motion-graphics` | **Motion-Graphics** | Fully code-rendered. Kinetic typography, animated charts, terminal/dev aesthetic, pure-graphic storytelling. | Reel 9:16 / Feed 1:1 / Square 1:1 |
| `lifestyle-cinematic` | **Lifestyle / Cinematic** | Polished b-roll, aspirational storytelling, mood-first. Brand film energy. | Reel 9:16 / Landscape 16:9 |
| `static-visual` | **Static-Visual** | Single-frame image. Quote card, screenshot mockup, meme poster, testimonial card. | Feed 1:1 / Portrait 4:5 / Story 9:16 |
| `carousel` | **Carousel** | Multi-slide feed post. Educational threads, before/after, listicles. | Feed 1:1 × N slides |
| `meme-cultural` | **Meme / Cultural-Reference** | Trend-jacking. Remixes of viral formats, cultural references, pop-music edits. Fast-turnaround, low-polish is a feature. | Reel 9:16 |
| `podcast-clip` | **Podcast-Clip** | Two-person conversational format. Interview cuts, founder-interviewer style. | Reel 9:16 with captions |
| `compilation` | **Compilation** | Sequence of moments. Before/after, listicle montage, multi-user testimonial reel. | Reel 9:16 / Feed 1:1 |

---

## Level-2 Subcategories (grows over time)

Below are the seed subcategories. Tanmay may propose new ones in any brief; Zimmer appends the new L2 here during Stage 3 review before the brief is moved downstream.

### UGC
- `confessional` — looking-at-camera, vulnerable, first-person ("I was skeptical, but…")
- `reaction` — user reacts to their own chart / product output on screen
- `day-in-the-life` — product slotted into real daily routine
- `friend-recommendation` — casual "you need to try this" energy
- `duet-style` — responds to a popular creator/claim
- `transition-reveal` — simple before/after transition with a hook

### Screen-Recording
- `chat-demo` — live typing a question, watching the product answer
- `onboarding-flow` — walkthrough of signup/setup
- `feature-discovery` — spotlight one specific feature
- `similar-personalities-scroll` — scroll through match/comparison cards (product-specific viral angle)
- `daily-brief-scroll` — showing a Daily Brief / Weekly Outlook or similar periodic content

### Talking-Head
- `expert-explainer` — credibility-led, educator framing
- `founder-pov` — founder explaining the "why" behind the product
- `myth-buster` — debunking a category-wide lie
- `interview-cut` — sliced from a longer conversation

### Motion-Graphics
- `kinetic-typography` — animated text, editorial pacing
- `terminal-style` — code/IDE aesthetic
- `chart-animated-reveal` — data visualisation / chart rendered with motion
- `data-visual` — stats/numbers-led

### Lifestyle-Cinematic
- `brand-film` — 30-60s mood piece
- `product-in-world` — cinematic b-roll of the product being used

### Static-Visual
- `quote-card` — pull-quote / insight card with brand treatment
- `product-screenshot` — single clean screenshot mock with one-line headline
- `meme-poster` — meme format taken to print/feed
- `testimonial-card` — one verbatim review + face (or anonymized)
- `similar-personalities-card` — comparison/match card (e.g. "Your result matches {name}")

### Carousel
- `educational-thread` — 6–10 slide explainer
- `before-after` — transformation narrative
- `listicle` — "5 things…"
- `case-study` — one user journey across slides

### Meme-Cultural
- `trend-remix` — repurposing a trending Reel template
- `pop-culture-ref` — Bollywood / cricket / political moment tie-in (safe ones only)

### Podcast-Clip
- `2-person-conversation` — split-screen talking-heads with captions

### Compilation
- `before-after-reel` — multi-user transformation
- `multi-user-testimonial` — 3–5 users back-to-back

---

## Adding a New Subcategory

1. Tanmay writes the L2 slug in the brief's `Category` field (e.g. `screen-recording/new-subcategory`).
2. Zimmer reviews; if approved, appends it to this file under the correct L1 section.
3. Zimmer creates `briefs/{L1}/{new-L2}/{YYYY-MM}/{YYYY-Www}/` and mirrored folders under `creatives/rendered/`, `creatives/review/`, and `assets/dynamic/`.
4. Zimmer commits the updated CATEGORIES.md as part of the same stage.

## Folder Commands (Zimmer reference)

Before Stage 2 briefs move downstream, Zimmer creates the full subtree:

```bash
# Inputs: CATEGORY, SUBCATEGORY, BRIEF_ID
MONTH=$(date +%Y-%m)                     # e.g. 2026-04
WEEK=$(date +%G-W%V)                     # ISO: 2026-W17

PATH_PREFIX="$CATEGORY/$SUBCATEGORY/$MONTH/$WEEK"

mkdir -p "briefs/$PATH_PREFIX"
mkdir -p "creatives/rendered/$PATH_PREFIX"
mkdir -p "creatives/review/$PATH_PREFIX"
mkdir -p "assets/dynamic/$PATH_PREFIX/brief-$BRIEF_ID/stock-video"
mkdir -p "assets/dynamic/$PATH_PREFIX/brief-$BRIEF_ID/stock-images"
mkdir -p "assets/dynamic/$PATH_PREFIX/brief-$BRIEF_ID/music"
```

The brief itself lands at:
`briefs/{category}/{subcategory}/{YYYY-MM}/{YYYY-Www}/creative-brief-{NNN}.md`

The render lands at:
`creatives/rendered/{category}/{subcategory}/{YYYY-MM}/{YYYY-Www}/brief-{NNN}-v{N}.mp4` (or `.png`, `.jpg`)

The review doc lands at:
`creatives/review/{category}/{subcategory}/{YYYY-MM}/{YYYY-Www}/brief-{NNN}-review.md`

## Brief Numbering

Brief IDs are **globally sequential** (001, 002, 003, …) — they never restart per category. The folder path tells you the category; the ID tells you the global order. Cross-references between research, briefs, and campaigns stay clean.

## ISO Week Helper

Get the current ISO week at any time:
```bash
date +%G-W%V   # → e.g. 2026-W17
date +%Y-%m    # → e.g. 2026-04
```

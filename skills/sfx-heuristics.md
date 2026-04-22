# SFX Heuristics — Leonardo's Beat-to-Sound Mapping

> **Read by:** Leonardo before every video composition.
> **Purpose:** Leonardo infers which SFX files to use based on the brief's *beat types*.
> Tanmay never needs to specify filenames — only intent. This file bridges intent → file.

---

## The Core Principle

Every beat in a creative has an **emotional job**. The SFX must serve that job, not perform it loudly. The question is always: "Does this sound add energy, or does it just make noise?"

---

## Beat → SFX Mapping Table

| Beat type (Tanmay writes this) | SFX file | Volume | Timing | Notes |
|---|---|---|---|---|
| Caption / text punch-in | `ui/pop-soft-01.mp3` | 0.25 | Frame text enters | Subtle — don't overdo on every caption |
| Spring element entry (card, badge, chip) | `ui/pop-soft-01.mp3` | 0.30 | Frame element enters | 1 pop per element group, not per item |
| Scene / cut transition | `transitions/whoosh-fast-01.mp3` | 0.40 | 10 frames before cut | Only mid-video — not on opening or closing |
| Gentle / soft transition | `transitions/whoosh-soft-01.mp3` | 0.35 | 10 frames before cut | Slower pacing, emotional moments |
| Exit / outro sweep | `transitions/swoosh-down-01.mp3` | 0.35 | 8 frames before end card | |
| Swipe / slide reveal | `transitions/swipe-right-01.mp3` | 0.38 | Frame reveal starts | For horizontal slide-in animations |
| Impact / number reveal | `impacts/thud-low-01.mp3` | 0.30 | Frame element fully enters | Low freq — warm, not harsh |
| Key stat / hero moment | `impacts/snare-accent-01.mp3` | 0.45 | On the beat | Max 2–3 per video |
| CTA / product reveal | `impacts/punch-mid-01.mp3` | 0.48 | Frame CTA appears | |
| Hard impact / big reveal | `impacts/impact-hard-01.mp3` | 0.45 | Frame reveal starts | Sparingly — max 1 per video |
| Small pop / UI click | `impacts/pop-soft-01.mp3` | 0.30 | Frame element appears | |
| Boss / power entry | `risers/bass-swell-01.mp3` | 0.28 | 2s before the moment | Builds tension before reveal |
| Big tension / product drop | `risers/riser-cinematic-01.mp3` | 0.28 | 2–3s before moment | |
| Quick tension cut | `risers/riser-short-01.mp3` | 0.30 | 1s before moment | |
| Electronic build | `risers/riser-electronic-01.mp3` | 0.28 | 1.5s before moment | |
| Terminal / code typing | `ui/typing-fast-01.mp3` | 0.25 | Loop while typing visible | Loop = true; trim or loop to match |
| Typewriter / slow reveal | `ui/typing-slow-01.mp3` | 0.22 | Loop while typing | |
| Notification / success | `ui/notification-01.mp3` | 0.35 | Frame notification appears | |
| UI click / button press | `ui/click-ui-01.mp3` | 0.30 | Frame click happens | |
| Tech scene ambience | `ambience/tech-hum-01.mp3` | 0.10 | Loop through tech scenes | Very quiet — just warmth |
| Urban / lifestyle ambience | `ambience/city-ambience-01.mp3` | 0.12 | Loop through city scenes | |

---

## UGC Override Rules

**When the creative is in the `ugc` category (any subcategory), apply all of these:**

1. **NO background music** — the character's voice and natural room tone ARE the audio. BGM feels inauthentic in UGC; it signals "this is an ad" and kills trust.
2. **Max 1 SFX accent per 8 seconds** of video.
3. **Allowed SFX in UGC:** phone notification reveals, pop-soft for text overlays, and a single whoosh-soft for scene cuts if there are more than 2 sources stitched together.
4. **No risers, no bass-swells, no cinematic builds** — these betray the "genuine" framing.
5. **No typing SFX** unless the character is literally typing on screen.

---

## Density Guidelines by Format

| Format | BGM | SFX density | Notes |
|---|---|---|---|
| Motion-graphics | Yes (0.2–0.3 vol) | Moderate–heavy (5–10) | Every element entry can have a sound |
| Screen-recording | Optional (0.15–0.2) | Minimal–moderate (2–5) | Don't let SFX fight the product UI sounds |
| Talking-head | Optional (0.15–0.2) | Minimal (2–4) | Speaker clarity is priority |
| UGC (any) | **Never** | **1 per 8s maximum** | See UGC Override above |
| Static-visual | N/A | N/A | No audio layer |
| Carousel | N/A | N/A | No audio layer |

---

## SFX Quality Gate

Before submitting to Zimmer, verify each SFX layer:

- [ ] No harsh high-frequency sounds (avoid impact files above ~6kHz played loud)
- [ ] No clipping — all SFX peaks below -3 dBFS
- [ ] SFX do not overlap in a way that creates muddiness (leave at least 4 frames gap between same-category sounds)
- [ ] Typing SFX loops cleanly — no audible click at loop point
- [ ] BGM fades out over last 2–3 seconds (not cut abruptly)
- [ ] In UGC: confirm zero BGM, max 1 SFX per 8s

---

## File Locations

All files are in `assets/static/sfx/`. Copy to `creatives/remotion-project/my-ads/public/` before use.

```
transitions/  whoosh-fast-01.mp3  whoosh-soft-01.mp3  swoosh-down-01.mp3  swipe-right-01.mp3
impacts/      thud-low-01.mp3     punch-mid-01.mp3    impact-hard-01.mp3  snare-accent-01.mp3  pop-soft-01.mp3
risers/       riser-cinematic-01.mp3  riser-electronic-01.mp3  riser-short-01.mp3  bass-swell-01.mp3
ambience/     tech-hum-01.mp3     city-ambience-01.mp3
ui/           typing-fast-01.mp3  typing-slow-01.mp3  notification-01.mp3  click-ui-01.mp3
```

**Need a sound not on this list?** Add it to `assets/static/sfx/` with the correct category prefix and document it above before using it.

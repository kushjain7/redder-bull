# SFX Sound Catalog
> **Owner:** Leonardo (Creative Engine)  
> **Last updated:** 2026-04-22  
> **Curator:** Zimmer  
>
> This is the single source of truth for all SFX assets. Before placing any SFX in a Remotion composition, read this file. All files are in `assets/static/sfx/`. The active production copies (used in render) live in `creatives/remotion-project/my-ads/public/sfx/` — updated by Zimmer when selections change.

---

## How to Use This File

When Leonardo needs a sound:
1. Find the **Use Case** that matches the moment in the creative.
2. Check the **Active Production File** — that's already in `public/sfx/` and ready to use.
3. If you want to try a different variant from the **Also Good** list, copy it to `public/sfx/` with the correct name and re-render.
4. For typing sounds, always use `loop={true}` on the `<Audio>` component — see typing section.

---

## Active Production Slots

These 8 filenames are what the composition references. They live in `public/sfx/`.

| `public/sfx/` name | Source file | Dur | Use case | Why this one |
|---|---|---|---|---|
| `pop-soft-01.mp3` | `floraphonic-bloop-1-184019.mp3` | 0.63s | Text/element first-appear, subtle transition accent | Clean, light, not harsh. Works at low volume (0.3–0.4) |
| `whoosh-soft-01.mp3` | `mixkit-cinematic-transition-wind-swoosh-1468.wav` | 1.32s | Standard scene transition, soft scene exit | Wind-cinematic feel — elegant, not aggressive |
| `whoosh-fast-01.mp3` | `mixkit-fast-transitions-swoosh-3115.wav` | 0.57s | Quick cut transitions, data-to-data scene change | Shortest, punchiest — use when visual cuts are fast |
| `swoosh-down-01.mp3` | `mixkit-fast-whoosh-transition-1490.wav` | 1.76s | Before brand moment, before CTA, "closing" transitions | Slightly longer — has a directional falling feel |
| `thud-low-01.mp3` | `universfield-ground-impact-352053.mp3` | 1.44s | Cards appearing, data reveal moments, proof points | Ground impact — satisfying weight, not a meme boom |
| `punch-mid-01.mp3` | `mixkit-soft-quick-punch-2151.wav` | 0.48s | Element entry accents, small pops for list items | Short, punchy, doesn't overpower — safe at 0.3 vol |
| `notification-01.mp3` | `universfield-new-notification-040-493469.mp3` | 1.07s | Completion moments: sending, underline done, checkmarks | Clean app-style ding, reads as "success" |
| `typing-fast-01.mp3` | `dragon-studio-typing-keyboard-asmr-356116.mp3` (trimmed 3s) | 3.0s | Keyboard typing animation. Use with `loop={true}` | ASMR-quality, real keyboard, loopable, not mechanical |

---

## Full Sound Library

### WHOOSHES & TRANSITIONS

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `mixkit-fast-transitions-swoosh-3115.wav` | 0.57s | Very short, sharp cut | Quick cuts between scenes in fast-paced Reels |
| `mixkit-arrow-whoosh-1491.wav` | 1.10s | Clean, directional | Standard scene transitions |
| `mixkit-fast-swipe-zoom-2627.wav` | 1.06s | Mobile swipe feel | Story swipe, app navigation demo |
| `mixkit-cinematic-transition-wind-swoosh-1468.wav` | 1.32s | Wind-like, elegant | ★ **Production: whoosh-soft** — premium scene transitions |
| `mixkit-cinematic-whoosh-fast-transition-1492.wav` | 1.33s | Cinematic, fast | Energetic scene changes |
| `mixkit-cinematic-wind-swoosh-1471.wav` | 1.45s | Slightly longer wind | Slower cinematic pacing |
| `mixkit-flying-fast-swoosh-1469.wav` | 1.63s | High-energy, "flying" feel | Fast-paced hook transitions |
| `mixkit-fast-whoosh-transition-1490.wav` | 1.76s | Directional, falling | ★ **Production: swoosh-down** — closing/brand transitions |
| `mixkit-air-in-a-hit-2161.wav` | 1.28s | Air hit + impact combo | Before a thud or impact sound |
| `mixkit-air-woosh-1489.wav` | 2.32s | Long, atmospheric | Long transitions, before big reveals |
| `mixkit-vacuum-swoosh-transition-1465.wav` | 2.26s | "Sucking" downward | Dramatic reveals, villain-to-hero moments |
| `mixkit-short-fire-whoosh-1345.wav` | 3.19s | Fire-like, dramatic | Very dramatic moments — use sparingly |
| `mixkit-cinematic-whoosh-deep-impact-1143.mp3` | 4.08s | Whoosh + deep impact at end | Before the biggest moment in a creative |

---

### IMPACTS, THUDS & PUNCHES

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `mixkit-soft-quick-punch-2151.wav` | 0.48s | Short, punchy | ★ **Production: punch-mid** — element entries, small accents |
| `freesound_community-loud-thud-45719.mp3` | 0.44s | Short, hard thud | Very quick impact accents |
| `virtual_vibes-cinematic-thud-fx-379991.mp3` | 1.10s | Cinematic, medium | Card appears, result reveals |
| `universfield-punch-03-352040.mp3` | 1.42s | Punchy, mid-sized | Bold element entries |
| `universfield-ground-impact-352053.mp3` | 1.44s | Ground impact, satisfying | ★ **Production: thud-low** — data cards appearing, proof moments |
| `universfield-impact-cinematic-boom-352465.mp3` | 2.09s | Cinematic boom, medium | Big data reveals, hero stat moments |
| `universfield-cinematic-impact-hit-352702.mp3` | 3.05s | Big cinematic hit with tail | Very dramatic reveals — has 2s reverb tail |
| `dragon-studio-cinematic-boom-405463.mp3` | 3.02s | Full cinematic boom | Scene-opening impact (Scene1, big hooks) |
| `dragon-studio-suspenseful-boom-451863.mp3` | 3.02s | Suspense + slow boom | Before tension-building moments |
| `u_60prvfn0xb-thud-sound-effect-319090.mp3` | 3.08s | Heavy, reverb thud | Landing after a riser, big reveal punctuation |
| `universfield-powerful-cinematic-hit-454852.mp3` | 3.13s | Most powerful of the set | Reserved for the ONE moment that must land hardest |
| `mixkit-big-cinematic-impact-788.mp3` | 7.94s | Huge impact + very long tail | Only for endings or dramatic pauses — tail runs 6s |

---

### POPS & BLOOPS

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `floraphonic-bloop-1-184019.mp3` | 0.63s | Light, digital bloop | ★ **Production: pop-soft** — text first-appear, UI element pop |
| `floraphonic-bloop-2-186531.mp3` | 0.63s | Slightly brighter bloop | Variant of bloop-1, alternate for variety |
| `floraphonic-bloop-3-186532.mp3` | 1.04s | Bloop with slight sustain | Card appears with a little "ding" tail |
| `floraphonic-bloop-4-186533.mp3` | 1.04s | Warmer bloop | Element appearing in emotional moments |
| `universfield-bubble-pop-06-351337.mp3` | 1.06s | Soft bubble pop | Light, airy element reveals |
| `soundreality-pop-sound-423716.mp3` | 1.78s | Pop with resonance tail | When you want the pop to "breathe" |
| `soundreality-pop-423717.mp3` | 1.97s | Pop with longer sustain | Longer emphasis on a reveal |
| `virtual_vibes-pop-tap-click-fx-383733.mp3` | 2.14s | Pop + tap combined | Multi-element moment (button + visual) |

---

### CLICKS, TAPS & UI

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `lucadialessandro-tap-notification-180637.mp3` | 0.16s | Very short single tap | Individual character/keystroke accent |
| `existentialtaco-confirm-tap-394001.mp3` | 1.10s | Confirm tap, satisfying | Button press, send action, selection confirms |
| `universfield-computer-mouse-click-351398.mp3` | 1.06s | Clean mouse click | Clicking through UI in screen-recording ads |
| `universfield-computer-mouse-click-02-383961.mp3` | 1.06s | Slight click variant | Alternate click for variety |
| `soundreality-sound-of-mouse-click-4-478760.mp3` | 1.20s | Mouse click with slight tail | Deliberate click moments |
| `universfield-button-124476.mp3` | 1.78s | UI button with sustain | CTA button press, important decisions |

---

### NOTIFICATIONS & CONFIRMATIONS

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `universfield-new-notification-040-493469.mp3` | 1.07s | Clean app notification | ★ **Production: notification** — completion, success, checkmark |
| `universfield-new-notification-09-352705.mp3` | 1.15s | Slightly different tone | Alternate notification for variety |

---

### RISERS & ENERGY BUILDS

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `u_1pruylktlg-riser-4-130953.mp3` | 1.15s | Short subtle riser (quiet, -10.5dB) | Background energy build — use at vol 0.6–0.8 |
| `creatorshome-sharp-riser-327342.mp3` | 1.88s | Sharp, energetic riser | Before a product reveal or stat moment |
| `u_1pruylktlg-riser-3-130954.mp3` | 2.32s | Longer subtle riser (-10.4dB) | Slow build before a key message |
| `creatorshome-long-riser-336262.mp3` | 2.88s | Long, full riser | Full build before the biggest moment in a creative |

> ⚠️ `u_1pruylktlg` files are quiet (-10.4 to -10.5 dB max). Set volume to 0.7–0.9 or they won't be audible.

---

### PAGE TURNS

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `creatorshome-turn-a-page-336933.mp3` | 1.03s | Crisp page turn | Before/after comparison scenes ("here's what the old way looked like") |
| `49053354-page-turn-305789.mp3` | 1.23s | Slightly softer page turn | Switching between two chat examples, "flip to reveal" |

---

### TYPING

| Filename | Dur | Character | Best Use |
|---|---|---|---|
| `ncprime-keyboard-typing-one-short-1-292590.mp3` | 0.63s | Single short keystroke burst | Loop for brief typing animations (use `loop={true}`) |
| `dragon-studio-typing-keyboard-asmr-356116.mp3` | 8.10s | Long ASMR typing, continuous | ★ **Production: typing-fast** (trimmed to 3s) — for 1.5–3s typing animations |
| `sarthakraj_308-typing-on-laptop-keyboard-308455.mp3` | 27.74s | Real laptop keyboard, full session | If a creative has 5–20s of typing visible — trim to exact duration |

---

## Typing Sound Rule (Leonardo must follow)

**Problem:** A typing SFX that doesn't match the animation duration causes latency and sync issues.

**Rule:**
1. Calculate the typing animation duration in frames → convert to seconds.
2. If animation ≤ 3s: use `typing-fast-01.mp3` with `loop={true}` on `<Audio>`. Remotion will stop it at the Sequence boundary.
3. If animation is 3–8s: use `dragon-studio-typing-keyboard-asmr-356116.mp3` directly — trim to duration + 0.5s fade-out using ffmpeg before copying to `public/sfx/`.
4. If animation > 8s: use `sarthakraj_308-typing-on-laptop-keyboard-308455.mp3` — trim to duration + 0.5s fade.
5. ALWAYS wrap the typing `<Audio>` in a `<Sequence>` that starts exactly when typing starts and ends exactly when typing ends.

**Code pattern (correct):**
```tsx
// Typing from global frame 159 to 224 (65 frames = 2.17s)
<Sequence from={159} durationInFrames={65}>
  <Audio src={staticFile("sfx/typing-fast-01.mp3")} volume={0.25} loop />
</Sequence>
```

**`loop={true}` ensures:** if the typing file (e.g. 0.63s) is shorter than the animation, it loops seamlessly. If the file is longer (e.g. 3s for a 2.17s animation), `loop` has no effect — Remotion cuts at the Sequence boundary.

---

## Removed / Red-Listed Sounds

These files were deleted from the library. Do not re-download.

| File | Why removed |
|---|---|
| `bithuh-vine-boom-392646.mp3` | Vine boom — internet meme sound. Comedic/ironic, destroys premium feel |
| `freesound_community-windows-error-sound-effect-35894.mp3` | Windows OS error sound — wrong feel entirely |
| `universfield-error-010-206498.mp3` | UI error sound — wrong context for a premium product |
| `soundshelfstudio-ui-error-pop-515668.mp3` | Error pop — wrong |
| `mixkit-intro-news-sound-1151.wav` | News channel jingle — wrong context entirely |
| `dragon-studio-camera-shutter-effect-390310.mp3` | DSLR shutter — not relevant to app/UI context |
| `kauasilbershlachparodes-shutter-click-3-494029.mp3` | Camera shutter — not relevant |
| `universfield-impact-cinematic-boom-352465 (1).mp3` | Exact duplicate — removed |

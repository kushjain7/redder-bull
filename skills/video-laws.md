# Video Laws — Universal Rules for All Video Creatives

> **Authority:** These laws override any conflicting instruction in any other SKILL.md.
> **Read by:** Leonardo (before every composition), Zimmer (during QC).
> **Every agent** must cross-reference this file before touching video.

These laws were written from first principles after the Brief 002 production failure, where five separate "shaking" root causes were chased across six render iterations. They are not opinions — each law maps to a specific failure mode documented in the post-mortem.

---

## V1 — fps MUST match source

**Law:** The Remotion composition `fps` MUST equal the fps of the source video clips.

**Why:** If a 24fps clip is played in a 30fps composition, Remotion must interpolate 6 extra frames per second via 24→30 pulldown. This introduces judder that reads as "shaking" in the final render.

**How to check:**
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate \
  -of default=noprint_wrappers=1 <video.mp4>
# Output: r_frame_rate=24/1  → use fps={24} in <Composition>
```

**Rule for mixed-fps projects:** If you have a mix of 24fps and 30fps clips, convert all clips to a single fps BEFORE compositing — not inside Remotion. Use `ffmpeg -r 30 -i input.mp4 output.mp4` to up-convert (or down-convert) in a preprocessing step, and document the conversion. Do NOT rely on Remotion to handle it.

**Applies to:** Every composition containing video clips.

---

## V2 — Use `<OffthreadVideo>` for production renders

**Law:** All production renders MUST use Remotion's `<OffthreadVideo>` component, not `<Video>`.

**Why:** `<Video>` is backed by the HTML5 `<video>` element. During Remotion's frame-by-frame renderer, the HTML5 player uses `currentTime` seeks that accumulate error. On a 40-second composition, this drift manifests as visible frame jitter — the "shaking" on every v1-v4 of Brief 002.

`<OffthreadVideo>` asks FFmpeg to extract the exact source frame for each composition frame. There is no seek drift, no frame interpolation, no HTML5 involvement in render mode.

**Usage:**
```tsx
import { OffthreadVideo, staticFile, Sequence } from "remotion";

<Sequence from={startFrame} durationInFrames={durationFrames}>
  <OffthreadVideo
    src={staticFile("clip.mp4")}
    style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover" }}
  />
</Sequence>
```

**Exception:** `<Video>` is acceptable in Remotion Studio for live preview only (not render). Switch to `<OffthreadVideo>` before any `npx remotion render` call.

---

## V3 — No mid-clip cuts on AI-chained footage

**Law:** AI video tools (Higgsfield, Runway, Pika, Sora, Kling) that chain clips for consistency encode the **last frame of clip N as the first frame of clip N+1**. Cutting a clip before its natural end breaks this visual bridge and creates a visible jump cut.

**What you CAN do:**
- Trim dead air from the **tail** of a clip (silencedetect the audio, shorten `Sequence.durationInFrames`).
- Trim a brief "warm-up" from the **head** of clip 1 only (the first clip has no preceding visual chain to protect).

**What you CANNOT do:**
- Cut a clip mid-action to save time budget.
- Remove frames from the middle of any clip.
- Use `startFrom` on `<OffthreadVideo>` to skip the beginning of clips 2-N (this breaks chain continuity).

**How to trim tail dead air:**
1. Run `ffmpeg -i clip.mp4 -af silencedetect=-35dB:d=0.3 -f null - 2>&1`
2. Find the last `silence_start` timestamp → convert to frames: `frame = floor(timestamp × fps)`
3. Set `durationInFrames={frame}` on that clip's `<Sequence>`.

---

## V4 — No deshake on AI-generated UGC footage

**Law:** NEVER run `ffmpeg deshake` (or any stabilization filter) on AI-generated UGC footage (Higgsfield, Pika, Runway, Kling).

**Why:** These tools simulate **deliberate natural camera motion** — the slight wobble that makes UGC feel authentic. The `deshake` filter interprets this motion as error and tries to cancel it, which:
1. Introduces its own artificial oscillation at a different frequency.
2. Changes the pixel format (e.g., yuv420p → yuv444p), causing color shift artefacts.
3. Makes the footage look more unstable, not less — the opposite of the goal.

**When deshake IS appropriate:** Real-world footage shot handheld in uncontrolled conditions (e.g., actual user testimonials, street video). Not AI footage.

**Root cause of v1/v2 failure:** A previous rule in `skills/orchestrator/SKILL.md` said "ALWAYS deshake AI footage." That rule was wrong and has been deleted. **V4 supersedes it.**

---

## V5 — Audio structure goes first

**Law:** Decide the audio level hierarchy BEFORE locking the picture edit. Export and review audio first; adjust video timing to match, not the reverse.

**Why:** Retroactively fixing audio levels after picture lock forces multiple re-renders and changes the edit rhythm.

**Workflow:**
1. Identify all audio layers the creative will have: BGM (if any), VO (if any), SFX.
2. Set level targets:
   - BGM: -20 to -23 LUFS integrated (background, not competing with VO)
   - VO / character speech: -14 LUFS integrated (foreground)
   - SFX: peak -6 to -3 dBFS (impactful, not clipping)
3. Verify with `ffmpeg ebur128` before export: `ffmpeg -i video.mp4 -filter:a ebur128=peak=true -f null - 2>&1 | tail -20`
4. UGC format: NO BGM by default. Character audio IS the primary audio. SFX accent max 1 per 8s.

---

## Quick Reference

| Law | One-line rule |
|---|---|
| V1 | Composition fps = source fps. Always. |
| V2 | `<OffthreadVideo>` for all production renders. Never `<Video>`. |
| V3 | Only trim AI clip tails (dead air). Never cut mid-clip or head of clips 2+. |
| V4 | No deshake on AI UGC. Ever. |
| V5 | Decide audio structure first. Verify with ebur128 before export. |

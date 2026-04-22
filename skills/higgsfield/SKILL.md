# Higgsfield — UGC Video Generation Playbook

> **Who reads this:** Leonardo (Creative Engine) whenever a brief is tagged `category: ugc`.
>
> **What it covers:** How to automatically generate UGC talking-head clips from a creative brief using the Higgsfield API + Python SDK, and hand the clips to the Remotion pipeline.

---

## 1. What is Higgsfield?

Higgsfield is an AI video and image generation platform. For UGC ads, the relevant capability is **image-to-video**: you supply a character photograph and a motion/speech prompt, and Higgsfield animates the character speaking to camera.

**Key constraints:**
| Constraint | Value |
|---|---|
| Max video duration per request | **8 seconds** (hard limit; target 6.5–7.5s to leave breathing room) |
| Character consistency across chunks | Via **last-frame chaining** (see Section 5) |
| API base URL | `https://platform.higgsfield.ai` |
| Python SDK | `higgsfield-client` (`pip3 install higgsfield-client`) |
| Credentials | `HF_API_KEY` + `HF_API_SECRET` from `scripts/higgsfield/higgsfield.local.env` |

**Recommended UGC models (image-to-video):**
| Use case | Model ID |
|---|---|
| Talking-head, conversational, natural | `kling-video/v2.1/pro/image-to-video` |
| Cinematic / high-fidelity portrait | `bytedance/seedance/v1/pro/image-to-video` |
| Fast/cheap iteration | `higgsfield-ai/dop/preview` |

Start with `kling-video/v2.1/pro/image-to-video` for UGC. Switch to seedance if quality is insufficient.

---

## 2. Pre-flight Checklist

Before starting any generation:

```bash
bash scripts/higgsfield/verify-session.sh
```

All three checks must pass (API credentials ✓, SDK installed ✓, Playwright profile ✓).
If any fail, follow the instructions in the verify output.

---

## 3. Script Chunking

### Why chunk?

Higgsfield caps videos at 8 seconds. A 30-second UGC ad script must be split into 4–6 chunks. Poor cut points cause jarring transitions; good cut points feel invisible.

### Use the chunker script

```bash
# Reads <script.txt>, writes ugc-chunks.json next to the brief
python3 scripts/higgsfield/chunk-script.py \
  --script "briefs/ugc/confessional/2026-04/2026-W17/ugc-script.txt" \
  --brief-id "003" \
  --avatar "assets/static/avatars/female_25-30_casual_01.jpg" \
  --template "kling-video/v2.1/pro/image-to-video" \
  --output "briefs/ugc/confessional/2026-04/2026-W17/ugc-chunks.json"
```

The output JSON looks like:
```json
{
  "brief_id": "003",
  "avatar_path": "assets/static/avatars/female_25-30_casual_01.jpg",
  "template": "kling-video/v2.1/pro/image-to-video",
  "aspect": "9:16",
  "chunks": [
    {
      "index": 1,
      "text": "Yaar, mujhe pehle se hi pata tha ki yeh app legit hai.",
      "est_seconds": 4.2,
      "seed_image": "assets/static/avatars/female_25-30_casual_01.jpg"
    },
    {
      "index": 2,
      "text": "Lekin meri friend ne try kiya aur uska result dekha toh main shocked reh gayi.",
      "est_seconds": 5.8,
      "seed_image": "creatives/remotion-project/my-ads/public/campaigns/003/ugc/chunk-01-last.jpg"
    }
  ]
}
```

### Manual chunking rules (if you chunk by hand)

**Cut priority order (highest to lowest):**
1. Paragraph break / double newline
2. Full stop (`.`) or question mark (`?`) or exclamation mark (`!`)
3. Em-dash (`—`) or semicolon (`;`)
4. Comma (`,`)

**Never cut:**
- Mid-clause (subject–verb must stay together)
- Mid-number or mid-unit (`₹5,000` must not be split)
- Mid-bracketed expression
- Mid-Hindi compound verb (`kar rahi thi` stays together)

**Speaking rate:** 2.4 words/second for conversational Hindi-English. Adjust per character in the brief.
**Budget:** Target 6.5–7.5s per chunk. 8.0s is the hard ceiling.

---

## 4. Avatar Selection

Avatars live in `assets/static/avatars/`. Use `pick-avatar.py` to find the best match:

```bash
python3 scripts/higgsfield/pick-avatar.py \
  --gender female \
  --age-band "25-30" \
  --vibe confessional
```

Returns the file path for the best-matching avatar, e.g.:
```
assets/static/avatars/female_25-30_casual_01.jpg
```

If no avatars are available yet, **STOP** and notify Zimmer. Never generate a placeholder face.

---

## 5. Generation Runbook (Primary Path — Python SDK)

### Step 1: Load credentials

```python
import os, json
from pathlib import Path

env_path = Path("scripts/higgsfield/higgsfield.local.env")
for line in env_path.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())
```

### Step 2: Upload avatar image

```python
import higgsfield_client

avatar_url = higgsfield_client.upload_file("assets/static/avatars/female_25-30_casual_01.jpg")
```

The upload returns a CDN URL valid for the current session. Use this URL for chunk 1's `seed_image`.

### Step 3: Generate chunk N

```python
result = higgsfield_client.subscribe(
    "kling-video/v2.1/pro/image-to-video",
    arguments={
        "image_url": seed_url,       # avatar URL for chunk 1; last-frame URL for chunk N+1
        "prompt": chunk["text"],     # plain conversational script text
        "duration": 5,               # request ~5s; actual clip may be 6–8s
        "aspect_ratio": "9:16",
    }
)
video_url = result["video"]["url"]
```

### Step 4: Download and store

```python
import requests

out_dir = Path(f"creatives/remotion-project/my-ads/public/campaigns/{brief_id}/ugc")
out_dir.mkdir(parents=True, exist_ok=True)
chunk_path = out_dir / f"chunk-{chunk['index']:02d}.mp4"

with requests.get(video_url, stream=True) as r:
    r.raise_for_status()
    with open(chunk_path, "wb") as f:
        for block in r.iter_content(chunk_size=8192):
            f.write(block)
```

### Step 5: Extract last frame for chaining

```bash
ffmpeg -sseof -0.04 -i chunk-01.mp4 -frames:v 1 chunk-01-last.jpg -y
```

Upload this image for chunk 2's `seed_image`:
```python
next_seed_url = higgsfield_client.upload_file(str(out_dir / f"chunk-{chunk['index']:02d}-last.jpg"))
```

**Repeat steps 3–5 for every chunk.** Always wait for each chunk to complete before starting the next so the last-frame chain stays intact.

### Step 6: Sanity check

After all chunks are downloaded, verify:
```bash
for f in chunk-*.mp4; do
  ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f"
done
```

Each clip should be 5–8 seconds. If any is < 1s or > 9s, mark it failed and regenerate that chunk.

### Step 7: Emit report

The runner script (`scripts/higgsfield/run-brief.sh`) emits `ugc-chunks-report.json` automatically. Verify there are no `"status": "failed"` entries before handing off to Remotion.

---

## 6. Using the Runner Script

For a fully automated end-to-end run:

```bash
# Ensure chunker has produced ugc-chunks.json first
bash scripts/higgsfield/run-brief.sh \
  --chunks "briefs/ugc/confessional/2026-04/2026-W17/ugc-chunks.json"
```

The script:
1. Loads credentials
2. Uploads the avatar image
3. Iterates over chunks: generate → download → extract last frame → upload for next chunk
4. Writes `ugc-chunks-report.json` to the same directory as `ugc-chunks.json`
5. Exits non-zero if any chunk failed

---

## 7. Prompt Writing Rules

These rules apply to every chunk's `text` field:

| Rule | Detail |
|---|---|
| Plain speech only | Write exactly what the character should say. No stage directions, no brackets, no asterisks. |
| One emotion per chunk | Don't oscillate emotions mid-chunk. |
| Tonal marker at the start | If the chunk is surprised: start with "Yaar..." or "Sach mein?". If authoritative: start with a declarative statement. |
| No filler words in written form | "uhh", "umm" etc. cause model artifacts — omit them. |
| Avoid long compound sentences | Break at 15–20 words max per chunk. |
| Hindi-English mix is fine | Match the brief's tone. Don't force pure Hindi or pure English. |
| No emoji or special characters | These are spoken literally by the TTS inside Higgsfield. |

---

## 8. Playwright MCP — Secondary Path

Use the Playwright MCP when you need to:
- Browse the Higgsfield model gallery at https://cloud.higgsfield.ai/explore
- Inspect available templates and style presets
- Troubleshoot UI-only features not yet in the API

To call via Playwright MCP in Cursor:
```
CallMcpTool server="playwright" toolName="browser_navigate" arguments={"url":"https://higgsfield.ai"}
```

**Do NOT use Playwright for video generation.** The API / Python SDK is the authoritative generation path.

---

## 9. Failure Modes and Retries

| Failure | Symptom | Fix |
|---|---|---|
| `nsfw` status | API returns `status: "nsfw"` | Reword the prompt; remove metaphors that could be flagged |
| `failed` status | API returns `status: "failed"` | Retry up to 2 times; if persistent, try a different model |
| Character drift | Chunk N+1 looks different from chunk N | Ensure `seed_image` = last frame of chunk N, not the original avatar |
| Credit exhaustion | 402 or error mentioning credits | Notify Zimmer; do not proceed |
| Rate limit | 429 | Back off 30s and retry |
| Clip is silent | No audio in output | Kling/Seedance animate but do NOT add TTS by default — audio is added in Remotion via captions |

> **Note on audio:** Higgsfield image-to-video models produce **silent videos** — they animate the character's mouth/expression based on the motion prompt, but do not add TTS audio. The character appears to be speaking but the audio is silent. Voice-over audio, captions, and SFX are all added in the Remotion composition stage.

---

## 10. Folder Conventions

| Path | Contents |
|---|---|
| `assets/static/avatars/` | Committed avatar library (generic, no product-specific photos) |
| `briefs/.../ugc-chunks.json` | Per-brief chunk manifest (gitignored) |
| `briefs/.../ugc-chunks-report.json` | Per-brief generation report (gitignored) |
| `creatives/remotion-project/my-ads/public/campaigns/{brief_id}/ugc/` | Downloaded MP4 clips + last-frame JPGs (gitignored via `public/campaigns/`) |
| `scripts/higgsfield/higgsfield.local.env` | API credentials (gitignored, never committed) |
| `.playwright-profile/` | Persistent Chrome profile (gitignored) |

---

## 11. Handoff to Remotion

After all chunks are downloaded and verified:
1. Note the exact file paths: `public/campaigns/{brief_id}/ugc/chunk-01.mp4` ... `chunk-NN.mp4`
2. Run `ffprobe` on each to get the exact duration in frames
3. Build the Remotion composition — see `skills/remotion/SKILL.md` Section "Source Footage: AI-Generated UGC via Higgsfield"
4. Apply all laws from `skills/video-laws.md` (OffthreadVideo, match FPS, no mid-clip cuts, no deshake)

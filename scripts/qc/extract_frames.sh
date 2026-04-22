#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# extract_frames.sh  —  Pull QC frames and spectrogram from a rendered video
#
# Usage:  bash scripts/qc/extract_frames.sh <video.mp4> [output_dir] [qc_json]
#
# Outputs (all in <output_dir>/frames/):
#   scene_cut_<N>_<timestamp>.png   — frame at each detected scene cut
#   safe_zone_<N>_<timestamp>.png   — bottom-380px crop of each scene cut frame
#   silence_<N>_<timestamp>.png     — frame at each silence event (from qc.json)
#   thumb_<N>.png                   — 1 frame every 5 seconds (visual scan)
#   spectrogram.png                 — full-video audio spectrogram
#
# Zimmer MUST use the Read tool to open at least:
#   - 3 scene_cut frames
#   - 2 safe_zone crops
#   - spectrogram.png
# before approving any render.
#
# Requires: ffmpeg (with libfreetype for spectrogram)
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

VIDEO="${1:-}"
OUT_DIR="${2:-scripts/qc}"
QC_JSON="${3:-$OUT_DIR/qc.json}"

if [[ -z "$VIDEO" ]]; then
  echo "Usage: bash scripts/qc/extract_frames.sh <video.mp4> [output_dir] [qc_json]"
  exit 1
fi
if [[ ! -f "$VIDEO" ]]; then
  echo "ERROR: File not found: $VIDEO"
  exit 1
fi

FRAMES_DIR="$OUT_DIR/frames"
mkdir -p "$FRAMES_DIR"

echo "🎞  Extracting QC frames from: $VIDEO"
echo "   Output → $FRAMES_DIR"
echo ""

# ── 1. Get scene cut timestamps from qc.json (or run scene detect) ────────────
if [[ -f "$QC_JSON" ]]; then
  echo "  [1] Reading scene cuts from $QC_JSON..."
  SCENE_TS=$(python3 -c "
import json, sys
with open('$QC_JSON') as f:
    d = json.load(f)
ts = d.get('checks',{}).get('scene_cuts',{}).get('timestamps_seconds',[])
print(' '.join(str(t) for t in ts))
" || echo "")
else
  echo "  [1] No qc.json found — running scene detect inline..."
  SCENE_TS=$(ffmpeg -i "$VIDEO" -vf "select=gt(scene\,0.4),showinfo" -f null - 2>&1 \
    | grep pts_time | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | tr '\n' ' ' || echo "")
fi

if [[ -z "$SCENE_TS" ]]; then
  echo "  [1] No scene cuts detected — adding frames at 0s, 5s, 10s as fallback."
  SCENE_TS="0 5 10"
fi

echo "  Scene cut timestamps: $SCENE_TS"
echo ""

# ── 2. Extract scene cut frames + safe-zone crops ─────────────────────────────
echo "  [2] Extracting scene cut frames..."
IDX=1
for TS in $SCENE_TS; do
  FRAME_FILE="$FRAMES_DIR/scene_cut_${IDX}_${TS}s.png"
  SZ_FILE="$FRAMES_DIR/safe_zone_${IDX}_${TS}s.png"

  # Full frame at scene cut
  ffmpeg -ss "$TS" -i "$VIDEO" -frames:v 1 -q:v 2 "$FRAME_FILE" -y 2>/dev/null \
    && echo "    ✓ scene_cut_${IDX}_${TS}s.png" \
    || echo "    ✗ failed: scene_cut_${IDX} at ${TS}s"

  # Bottom-380px crop (safe-zone check area)
  # For 1080x1920: crop=1080:380:0:1540  (x=0, y=1920-380=1540, w=1080, h=380)
  if [[ -f "$FRAME_FILE" ]]; then
    FRAME_H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height \
      -of default=noprint_wrappers=1:nokey=1 "$VIDEO" 2>/dev/null || echo "1920")
    CROP_Y=$((FRAME_H - 380))
    ffmpeg -i "$FRAME_FILE" -vf "crop=iw:380:0:${CROP_Y}" "$SZ_FILE" -y 2>/dev/null \
      && echo "    ✓ safe_zone_${IDX}_${TS}s.png (bottom 380px)" \
      || echo "    ✗ failed: safe_zone_${IDX}"
  fi

  IDX=$((IDX + 1))
done
echo ""

# ── 3. Frames at silence events (from qc.json) ────────────────────────────────
if [[ -f "$QC_JSON" ]]; then
  echo "  [3] Extracting frames at silence events..."
  SILENCE_TS=$(python3 -c "
import json
with open('$QC_JSON') as f:
    d = json.load(f)
events = d.get('checks',{}).get('silence_events',{}).get('events',[])
ts = [e.get('start', e.get('end', 0)) for e in events[:5]]  # max 5
print(' '.join(str(t) for t in ts))
" || echo "")

  IDX=1
  for TS in $SILENCE_TS; do
    SIL_FILE="$FRAMES_DIR/silence_${IDX}_${TS}s.png"
    ffmpeg -ss "$TS" -i "$VIDEO" -frames:v 1 -q:v 2 "$SIL_FILE" -y 2>/dev/null \
      && echo "    ✓ silence_${IDX}_${TS}s.png" \
      || echo "    ✗ failed: silence_${IDX} at ${TS}s"
    IDX=$((IDX + 1))
  done
  echo ""
fi

# ── 4. Thumbnail strip — 1 frame every 5 seconds ─────────────────────────────
echo "  [4] Extracting thumbnail strip (1 per 5s)..."
ffmpeg -i "$VIDEO" -vf "fps=1/5" "$FRAMES_DIR/thumb_%03d.png" -y 2>/dev/null \
  && echo "    ✓ thumb_XXX.png series extracted" \
  || echo "    ✗ thumbnail extraction failed"
echo ""

# ── 5. Audio spectrogram ──────────────────────────────────────────────────────
echo "  [5] Generating audio spectrogram..."
SPEC_FILE="$OUT_DIR/spectrogram.png"
ffmpeg -i "$VIDEO" \
  -lavfi "showspectrumpic=s=1920x384:legend=1:color=intensity" \
  "$SPEC_FILE" -y 2>/dev/null \
  && echo "    ✓ spectrogram.png" \
  || echo "    ✗ spectrogram failed (ffmpeg may need --enable-libfreetype)"
echo ""

# ── Summary ───────────────────────────────────────────────────────────────────
echo "✅ Frame extraction complete."
echo ""
echo "Zimmer — MANDATORY review steps:"
echo "  1. Use the Read tool to open at least 3 scene_cut frames."
echo "  2. Use the Read tool to open at least 2 safe_zone crops."
echo "     Look for ANY text below the safe zone line."
echo "  3. Use the Read tool to open spectrogram.png."
echo "     Look for silence gaps and audio level consistency."
echo ""
echo "  Files are in: $FRAMES_DIR"
echo ""

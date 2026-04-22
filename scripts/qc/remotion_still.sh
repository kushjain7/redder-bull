#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# remotion_still.sh  —  Deterministic overlay frame extraction via Remotion
#
# Usage:  bash scripts/qc/remotion_still.sh <CompositionId> <frame> [output_dir]
#
# Examples:
#   bash scripts/qc/remotion_still.sh AdBrief002Reel 0       # first frame
#   bash scripts/qc/remotion_still.sh AdBrief002Reel 192     # frame 192 (8s @ 24fps)
#   bash scripts/qc/remotion_still.sh AdBrief002Reel 745     # start of scene 5
#
# What it does:
#   Renders a single exact frame from a Remotion composition using
#   `npx remotion still`. Unlike extracting from an mp4 (which involves
#   re-decoding), this gives you the frame exactly as Remotion computes it —
#   including all overlays, captions, and graphics.
#
# Output:
#   <output_dir>/still_<CompositionId>_frame<N>.png
#
# Use case:
#   - Verify caption text position at a known timestamp
#   - Check safe zone compliance on text overlays independent of video
#   - Feed to safe_zone.py / contrast.py for objective checks
#
# Requires: Node.js, npx, Remotion project set up in
#           creatives/remotion-project/my-ads/
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

COMPOSITION="${1:-}"
FRAME="${2:-0}"
OUT_DIR="${3:-scripts/qc}"
REMOTION_DIR="creatives/remotion-project/my-ads"

if [[ -z "$COMPOSITION" ]]; then
  echo "Usage: bash scripts/qc/remotion_still.sh <CompositionId> <frame> [output_dir]"
  echo ""
  echo "Available compositions (from Root.tsx):"
  grep 'id=' "$REMOTION_DIR/src/Root.tsx" 2>/dev/null | grep -o '"[A-Za-z0-9]*"' | tr -d '"' || echo "  (could not read Root.tsx)"
  exit 1
fi

mkdir -p "$OUT_DIR"

OUTPUT_FILE="$OUT_DIR/still_${COMPOSITION}_frame${FRAME}.png"

echo "🎬 Rendering still: $COMPOSITION frame $FRAME"
echo "   Output → $OUTPUT_FILE"
echo ""

cd "$REMOTION_DIR"

# npx remotion still [compositionId] [output] [--frame=N]
npx remotion still \
  --composition="$COMPOSITION" \
  --output="../../../../$OUTPUT_FILE" \
  --frame="$FRAME" \
  2>&1

cd - > /dev/null

if [[ -f "$OUTPUT_FILE" ]]; then
  echo ""
  echo "✅ Still rendered: $OUTPUT_FILE"
  echo ""
  echo "Next steps:"
  echo "  1. Use the Read tool to open $OUTPUT_FILE"
  echo "  2. Optionally run safe_zone check:"
  echo "     python3 scripts/qc/safe_zone.py $OUTPUT_FILE scripts/qc/safe_zone_still.json"
  echo "  3. Optionally run contrast check:"
  echo "     python3 scripts/qc/contrast.py $OUTPUT_FILE scripts/qc/contrast_still.json"
else
  echo ""
  echo "❌ ERROR: Still was not produced. Check Remotion error above."
  exit 1
fi

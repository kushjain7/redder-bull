#!/usr/bin/env bash
# =============================================================================
# run-brief.sh
# Thin shell wrapper around run-brief.py.
# Verifies the session, then delegates to the Python runner.
#
# Usage:
#   bash scripts/higgsfield/run-brief.sh \
#       --chunks path/to/ugc-chunks.json
#
#   # Dry run (prints plan without calling API)
#   bash scripts/higgsfield/run-brief.sh \
#       --chunks path/to/ugc-chunks.json --dry-run
#
#   # Resume from chunk 3 (if earlier chunks already downloaded)
#   bash scripts/higgsfield/run-brief.sh \
#       --chunks path/to/ugc-chunks.json --start-from 3
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Pre-flight ────────────────────────────────────────────────────────────────
echo "→ Verifying Higgsfield session..."
bash "$SCRIPT_DIR/verify-session.sh" || {
  echo "Pre-flight failed — fix errors above before running."
  exit 1
}
echo ""

# ── Delegate to Python runner ─────────────────────────────────────────────────
python3 "$SCRIPT_DIR/run-brief.py" "$@"

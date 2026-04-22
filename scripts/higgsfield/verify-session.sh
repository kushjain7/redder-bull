#!/usr/bin/env bash
# =============================================================================
# verify-session.sh
# Verifies that:
#   1. Higgsfield API credentials are set and working (Python SDK ping)
#   2. Playwright profile exists (browser session is available for UI tasks)
# Run this before any generation job to catch auth failures early.
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$SCRIPT_DIR/higgsfield.local.env"
PROFILE_DIR="$REPO_ROOT/.playwright-profile"
EXIT_CODE=0

echo "=== Higgsfield Session Verification ==="

# ── Load credentials ─────────────────────────────────────────────────────────
if [ -f "$ENV_FILE" ]; then
  # Parse env file safely (avoids xargs issues with large environments)
  while IFS='=' read -r key val; do
    # Skip comments and blank lines
    [[ "$key" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$key" ]] && continue
    # Strip leading/trailing whitespace from key
    key="${key// /}"
    export "$key=$val"
  done < <(grep -v '^[[:space:]]*#' "$ENV_FILE" | grep '=')
fi

# ── 1. API credentials check ─────────────────────────────────────────────────
echo ""
echo "→ Checking Higgsfield API credentials..."

if [ -z "${HF_API_KEY:-}" ] || [ "${HF_API_KEY}" = "your_api_key_here" ]; then
  echo "  ✗ HF_API_KEY is not set. Fill in scripts/higgsfield/higgsfield.local.env"
  EXIT_CODE=1
elif [ -z "${HF_API_SECRET:-}" ] || [ "${HF_API_SECRET}" = "your_api_secret_here" ]; then
  echo "  ✗ HF_API_SECRET is not set. Fill in scripts/higgsfield/higgsfield.local.env"
  EXIT_CODE=1
else
  # Quick API ping — list a single queued request (will return empty list, proves auth works)
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Key ${HF_API_KEY}:${HF_API_SECRET}" \
    "https://platform.higgsfield.ai/requests/00000000-0000-0000-0000-000000000000/status" \
    2>/dev/null || echo "000")

  if [ "$HTTP_STATUS" = "401" ] || [ "$HTTP_STATUS" = "403" ]; then
    echo "  ✗ API auth failed (HTTP $HTTP_STATUS). Check your key/secret."
    EXIT_CODE=1
  elif [ "$HTTP_STATUS" = "000" ]; then
    echo "  ✗ Could not reach platform.higgsfield.ai. Check network."
    EXIT_CODE=1
  else
    echo "  ✓ API credentials valid (HTTP $HTTP_STATUS)"
  fi
fi

# ── 2. Python SDK check ──────────────────────────────────────────────────────
echo ""
echo "→ Checking higgsfield-client SDK..."

VENV_PATH="$REPO_ROOT/.venv-hf"

if python3 -c "import higgsfield_client" 2>/dev/null; then
  SDK_VER=$(python3 -c "import importlib.metadata; print(importlib.metadata.version('higgsfield-client'))" 2>/dev/null || echo "unknown")
  echo "  ✓ higgsfield-client installed system-wide (version: $SDK_VER)"
elif PYTHONPATH="$VENV_PATH" python3 -c "import higgsfield_client" 2>/dev/null; then
  echo "  ✓ higgsfield-client found in .venv-hf (local install)"
else
  echo "  ✗ higgsfield-client not found."
  echo "    Option A: pip3 install --user higgsfield-client"
  echo "    Option B: pip3 install --target .venv-hf higgsfield-client  (already done in sandbox)"
  EXIT_CODE=1
fi

# ── 3. Playwright profile check (optional — only needed for UI browsing) ─────
echo ""
echo "→ Checking Playwright profile (optional)..."

if [ -d "$PROFILE_DIR" ]; then
  echo "  ✓ Profile directory exists: $PROFILE_DIR"
else
  echo "  ℹ Profile directory missing (not required for API generation)."
  echo "    Run setup-playwright.sh if you need Higgsfield UI/browser access."
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
  echo "✓ All checks passed. Ready to generate."
else
  echo "✗ Some checks failed — fix the above before running generation."
fi
exit "$EXIT_CODE"

#!/usr/bin/env bash
# =============================================================================
# setup-playwright.sh
# One-time setup for Higgsfield integration:
#   1. Installs @playwright/mcp globally (for UI browsing / model discovery)
#   2. Installs higgsfield-client Python SDK (primary generation pathway)
#   3. Creates a persistent Chrome profile directory at .playwright-profile/
#   4. Registers the Playwright MCP server in ~/.cursor/mcp.json
#   5. Launches a headed browser for one-time Higgsfield login
# =============================================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROFILE_DIR="$REPO_ROOT/.playwright-profile"
MCP_CONFIG="$HOME/.cursor/mcp.json"

echo "=== Higgsfield Integration Setup ==="

# ── 1. Playwright MCP ────────────────────────────────────────────────────────
echo ""
echo "→ Installing @playwright/mcp globally..."
npm install -g @playwright/mcp

echo "→ Installing Playwright browsers..."
npx playwright install chromium

# ── 2. Python SDK ────────────────────────────────────────────────────────────
echo ""
echo "→ Installing higgsfield-client Python SDK..."
pip3 install --quiet higgsfield-client requests

# ── 3. Persistent profile dir ────────────────────────────────────────────────
echo ""
echo "→ Creating persistent Chrome profile at: $PROFILE_DIR"
mkdir -p "$PROFILE_DIR"

# ── 4. Register MCP in Cursor ────────────────────────────────────────────────
echo ""
echo "→ Registering Playwright MCP in $MCP_CONFIG ..."

if [ ! -f "$MCP_CONFIG" ]; then
  echo '{"mcpServers":{}}' > "$MCP_CONFIG"
fi

# Use Python for safe JSON merge
python3 - <<PYEOF
import json, pathlib, sys

cfg_path = pathlib.Path("$MCP_CONFIG")
cfg = json.loads(cfg_path.read_text())
cfg.setdefault("mcpServers", {})

cfg["mcpServers"]["playwright"] = {
    "command": "npx",
    "args": [
        "@playwright/mcp",
        "--browser", "chromium",
        "--user-data-dir", "$PROFILE_DIR",
        "--headless", "false"
    ]
}

cfg_path.write_text(json.dumps(cfg, indent=2))
print("  Playwright MCP registered.")
PYEOF

# ── 5. Initial login (headed) ────────────────────────────────────────────────
echo ""
echo "→ Launching headed browser for one-time Higgsfield login..."
echo "  1. Log in at https://higgsfield.ai"
echo "  2. Go to https://cloud.higgsfield.ai  → copy your API key & secret"
echo "  3. Close the browser when done."
echo ""

npx playwright open \
  --browser chromium \
  --user-data-dir "$PROFILE_DIR" \
  "https://higgsfield.ai/login" || true

echo ""
echo "→ Creating credential template..."
ENV_FILE="$SCRIPT_DIR/higgsfield.local.env"
if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<'ENVEOF'
# Higgsfield API credentials — get them from https://cloud.higgsfield.ai
# This file is gitignored. Never commit it.
HF_API_KEY=your_api_key_here
HF_API_SECRET=your_api_secret_here
ENVEOF
  echo "  Created $ENV_FILE — fill in your API key & secret."
else
  echo "  $ENV_FILE already exists — skipping."
fi

echo ""
echo "✓ Setup complete."
echo ""
echo "Next steps:"
echo "  1. Fill in scripts/higgsfield/higgsfield.local.env with your API key"
echo "  2. Run: bash scripts/higgsfield/verify-session.sh"
echo "  3. Restart Cursor so the Playwright MCP is loaded"

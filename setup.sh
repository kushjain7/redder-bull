#!/bin/bash

# ============================================================
# Marketing Agency Automation — Setup Script
# Agents: Zimmer (Orchestrator) | Tanmay (Strategist)
#         Leonardo (Creative Engine) | Mark (Media Buyer)
# ============================================================

set -e  # Exit on first error

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BOLD='\033[1m'

print_header() {
  echo ""
  echo -e "${BLUE}${BOLD}============================================================${NC}"
  echo -e "${BLUE}${BOLD}  Marketing Agency Setup — $1${NC}"
  echo -e "${BLUE}${BOLD}============================================================${NC}"
  echo ""
}

print_step() {
  echo -e "${YELLOW}▶ $1${NC}"
}

print_ok() {
  echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
  echo -e "${RED}✗ $1${NC}"
}

print_info() {
  echo -e "  ${BLUE}→${NC} $1"
}

# ── 0. Welcome ─────────────────────────────────────────────
print_header "Starting Setup"
echo "This script will:"
echo "  1. Check Node.js (v18+ required)"
echo "  2. Set up Remotion project (Leonardo's workspace)"
echo "  3. Configure Pipeboard MCP for Meta Ads (Mark's tool)"
echo "  4. Optionally install Claude Code skills"
echo ""
echo "Estimated time: 5–15 minutes"
echo ""
read -p "Press Enter to begin..."

# ── 1. Node.js Check ───────────────────────────────────────
print_header "Step 1/4: Node.js Check"

if ! command -v node &>/dev/null; then
  print_error "Node.js is not installed."
  print_info "Install from: https://nodejs.org (choose LTS version)"
  print_info "Then re-run this script."
  exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  print_error "Node.js v$NODE_VERSION found. Version 18+ is required."
  print_info "Update from: https://nodejs.org"
  exit 1
fi

print_ok "Node.js $(node --version) — OK"

if ! command -v npm &>/dev/null; then
  print_error "npm is not installed. It usually comes with Node.js."
  exit 1
fi

print_ok "npm $(npm --version) — OK"

# ── 2. Remotion Setup (Leonardo's workspace) ───────────────
print_header "Step 2/4: Remotion Setup (Leonardo — Creative Engine)"

REMOTION_DIR="creatives/remotion-project"
ADS_DIR="$REMOTION_DIR/my-ads"

if [ -f "$ADS_DIR/package.json" ]; then
  print_ok "Remotion project already exists at $ADS_DIR"
else
  print_step "Creating Remotion project..."
  print_info "This runs: npx create-video@latest my-ads --template hello-world"
  echo ""

  cd "$REMOTION_DIR"
  npx create-video@latest my-ads --blank --yes 2>&1 | tail -20
  cd ../..

  print_ok "Remotion project created at $ADS_DIR"
fi

print_step "Installing npm dependencies..."
cd "$ADS_DIR"
npm install --silent
print_ok "Dependencies installed"
cd ../../..

# Copy starter templates and Root.tsx into the Remotion project
print_step "Adding Leonardo's starter templates..."
mkdir -p "$ADS_DIR/src/templates"

# Copy templates if they exist in the repo (they'll be in src/templates/)
if [ -d "$ADS_DIR/src/templates" ]; then
  print_ok "Template directory exists at $ADS_DIR/src/templates/"
else
  mkdir -p "$ADS_DIR/src/templates"
  print_ok "Template directory created."
fi

# Create a .gitkeep in rendered/ so it's tracked by git
touch creatives/rendered/.gitkeep

print_ok "Leonardo's workspace is ready."
print_info "To preview: cd $ADS_DIR && npx remotion studio"
print_info "To render:  cd $ADS_DIR && npx remotion render [CompositionName] --output ../../rendered/[output].mp4"

# ── 3. Pipeboard MCP (Mark's tool) ─────────────────────────
print_header "Step 3/4: Pipeboard MCP Setup (Mark — Media Buyer)"

echo "Mark needs the Pipeboard MCP to connect to Meta Ads."
echo ""
echo "  Pipeboard Free: \$0/month, 30 executions/week"
echo "  Pipeboard Pro:  \$29.90/month, 500 executions/week"
echo ""
print_info "Step a: Go to https://pipeboard.co and create a free account"
print_info "Step b: Connect your Meta (Facebook) Ads account via OAuth"
print_info "Step c: Get your API token from https://pipeboard.co/api-tokens"
echo ""

read -p "Have you created a Pipeboard account? (y/n): " HAS_PIPEBOARD

if [ "$HAS_PIPEBOARD" = "y" ] || [ "$HAS_PIPEBOARD" = "Y" ]; then
  print_step "Adding Pipeboard MCP to Claude Code..."

  if command -v claude &>/dev/null; then
    claude mcp add --transport http pipeboard-meta-ads https://meta-ads.mcp.pipeboard.co 2>/dev/null && \
      print_ok "Pipeboard MCP added successfully." || \
      print_error "Could not add MCP automatically. Run manually: claude mcp add --transport http pipeboard-meta-ads https://meta-ads.mcp.pipeboard.co"

    echo ""
    print_info "To authenticate: Open Claude Code, type /mcp, and follow the Pipeboard auth flow."
  else
    echo ""
    print_error "Claude Code CLI not found in PATH."
    print_info "Manually run this command after installing Claude Code:"
    echo ""
    echo "  claude mcp add --transport http pipeboard-meta-ads https://meta-ads.mcp.pipeboard.co"
    echo ""
  fi
else
  echo ""
  print_info "Skipping Pipeboard setup. You can set it up later by running:"
  echo ""
  echo "  claude mcp add --transport http pipeboard-meta-ads https://meta-ads.mcp.pipeboard.co"
  echo ""
  print_info "Mark will not be able to create or monitor campaigns until Pipeboard is connected."
fi

# ── 4. Optional Skills Install ─────────────────────────────
print_header "Step 4/4: Optional Claude Code Skills"

echo "These are additional Claude Code skills that enhance Tanmay's research,"
echo "Mark's ad auditing, and Leonardo's creative production."
echo ""
echo "They require an internet connection and git."
echo ""

read -p "Install optional Claude Code skills? (y/n): " INSTALL_SKILLS

if [ "$INSTALL_SKILLS" = "y" ] || [ "$INSTALL_SKILLS" = "Y" ]; then
  print_step "Installing skills..."

  # Marketing fundamentals
  if command -v git &>/dev/null; then
    print_info "Marketing frameworks (Corey Haines)..."
    git clone --quiet https://github.com/coreyhaines31/marketingskills.git /tmp/mktg-skills 2>/dev/null && \
      cp -r /tmp/mktg-skills/skills/* skills/marketing/ 2>/dev/null || true
    rm -rf /tmp/mktg-skills

    print_info "Ad auditing skills (AgriciDaniel)..."
    git clone --quiet https://github.com/AgriciDaniel/claude-ads.git /tmp/claude-ads 2>/dev/null && \
      (cp -r /tmp/claude-ads/skills/* skills/ads/ 2>/dev/null || cp -r /tmp/claude-ads/* skills/ads/ 2>/dev/null) || true
    rm -rf /tmp/claude-ads

    print_ok "Optional skills installed."
  else
    print_error "git not found — skipping skills install. Install git and re-run."
  fi
else
  print_info "Skipping optional skills. The built-in SKILL.md files are sufficient to start."
fi

# ── 5. Final Status ────────────────────────────────────────
print_header "Setup Complete"

echo -e "${GREEN}${BOLD}Your marketing agency is ready.${NC}"
echo ""
echo "────────────────────────────────────"
echo "  The Team:"
echo "  • Zimmer  — Orchestrator (Agency Director)"
echo "  • Tanmay  — Strategist (Research + Briefs)"
echo "  • Leonardo — Creative Engine (Remotion)"
echo "  • Mark    — Media Buyer (Meta Ads)"
echo "────────────────────────────────────"
echo ""
echo -e "${YELLOW}${BOLD}NEXT STEPS:${NC}"
echo ""
echo "  1. Fill your product context:"
echo "     Open state/product-context.md in your text editor"
echo "     Fill ALL 7 sections thoroughly — this drives everything."
echo ""
echo "  2. Open Claude Code:"
echo "     $ claude"
echo ""
echo "  3. Type this to start Cycle 1:"
echo ""
echo '     Read CLAUDE.md, state/product-context.md, and skills/orchestrator/SKILL.md.'
echo '     You are Zimmer, the Orchestrator. Initialize Cycle 1, Stage 1.'
echo '     Invoke Tanmay for competitor and market research.'
echo ""
echo "  4. Morning command (while campaigns run):"
echo '     You are Zimmer. Give me the current status. Then invoke Mark to pull performance data.'
echo ""
echo "  Need help? Read OPERATIONS.md for the full step-by-step guide."
echo ""

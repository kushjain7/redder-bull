#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# push-framework.sh  —  Safe publish of generic framework changes to GitHub
#
# Usage:  bash scripts/push-framework.sh
#
# What it does:
#   1. Checks for product-tainted paths that must never reach the public repo.
#   2. Shows a diff summary of what WILL be committed.
#   3. Prompts for a commit message.
#   4. Runs: git add -A && git commit -m "…" && git push origin main
#
# Rules:
#   - Run this ONLY when you explicitly want to push to GitHub.
#   - Without running this script, nothing ever reaches the remote —
#     even if agents modified framework files.
#   - Never run this with uncommitted state files, research, or brief dates.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

RED='\033[0;31m'
YEL='\033[1;33m'
GRN='\033[0;32m'
BLU='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLU}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLU}║     Redder Bull — Framework Push Guard           ║${NC}"
echo -e "${BLU}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# ── Step 1: Taint check ───────────────────────────────────────────────────────
# These patterns must never appear in staged/untracked files heading to GitHub.
TAINT_PATTERNS=(
  "state/system-log"
  "state/current-cycle"
  "state/product-context"
  "state/outputs/current"
  "state/orchestrator-notes"
  "state/approvals/pending-approval"
  "research/competitor-analysis"
  "research/winning-hooks"
  "research/audience-insights"
  "src/campaigns/"
  "public/b00"
  "public/bgm"
  "public/iktara"
  "iktara general assets"
  "iktara_"
  "forsee.life"
  "briefs/ugc/confessional/20"
  "briefs/screen-recording/.*20"
  "creatives/review/.*/20"
)

echo -e "🔍 Scanning for product-tainted paths..."
TAINTED=0

# Check git status output (staged + untracked)
STATUS=$(git status --porcelain 2>/dev/null || true)

for pattern in "${TAINT_PATTERNS[@]}"; do
  if echo "$STATUS" | grep -qE "$pattern"; then
    echo -e "  ${RED}✗ BLOCKED:${NC} Found path matching '${pattern}'"
    TAINTED=1
  fi
done

if [[ $TAINTED -eq 1 ]]; then
  echo ""
  echo -e "${RED}╔══════════════════════════════════════════════════╗${NC}"
  echo -e "${RED}║  PUSH ABORTED — product-tainted files detected   ║${NC}"
  echo -e "${RED}║  Review your .gitignore or git-add selections.   ║${NC}"
  echo -e "${RED}╚══════════════════════════════════════════════════╝${NC}"
  echo ""
  echo "  Tip: Run 'git status' to see exactly what would be committed."
  echo "  Tip: The offending files should be in .gitignore already."
  echo "       If they're tracked, run: git rm --cached <file>"
  exit 1
fi

echo -e "  ${GRN}✓ No product-tainted paths found.${NC}"
echo ""

# ── Step 2: Show what will be committed ───────────────────────────────────────
echo -e "📦 Changes to be committed:"
echo ""
git diff --stat HEAD 2>/dev/null || git status --short
echo ""

CHANGED=$(git status --porcelain | wc -l | tr -d ' ')
if [[ "$CHANGED" -eq 0 ]]; then
  echo -e "${YEL}Nothing to commit. Working tree is clean.${NC}"
  exit 0
fi

# ── Step 3: Confirm ────────────────────────────────────────────────────────────
echo -e "${YEL}Review the diff above carefully.${NC}"
echo ""
read -rp "Commit message (or Ctrl+C to abort): " COMMIT_MSG

if [[ -z "$COMMIT_MSG" ]]; then
  echo -e "${RED}Empty commit message. Aborting.${NC}"
  exit 1
fi

# ── Step 4: Commit + push ─────────────────────────────────────────────────────
echo ""
echo -e "🚀 Committing and pushing..."
git add -A
git commit -m "$COMMIT_MSG"
git push origin main

echo ""
echo -e "${GRN}✓ Framework update pushed to origin/main.${NC}"
echo ""

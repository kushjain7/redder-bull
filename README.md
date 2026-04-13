# Marketing Agency Automation System

An automated, 4-agent marketing agency for the **Indian market** — built on Claude Code, Remotion, and Pipeboard (Meta Ads MCP). Designed to run on a bare-minimum budget of **~₹16,700/mo** (~$200) including ad spend.

> **This is a reusable template.** Clone this repo for a new product, fill `state/product-context.md`, run `setup.sh`, and start your first cycle.

---

## The Team

| Agent | Name | What They Do |
|---|---|---|
| Orchestrator | **Zimmer** | Agency Director — coordinates, reviews all output, manages state, reports to you |
| Strategist | **Tanmay** | Market research, competitor analysis, creative brief writing |
| Creative Engine | **Leonardo** | Remotion video & image ad production |
| Media Buyer | **Mark** | Meta Ads campaign creation, launch, and daily monitoring |

---

## How It Works

All 4 agents communicate exclusively through **files** — no external databases, no complex infrastructure. Everything lives in this repo.

```
You (Human Operator)
        │
        ▼
   Zimmer (Orchestrator)
   ├── → Tanmay (Strategist) → research/ + briefs/
   ├── → Leonardo (Creative Engine) → creatives/rendered/
   └── → Mark (Media Buyer) → campaigns/ + Meta Ads
```

Each marketing cycle has **10 stages**:

```
Research → Brief → Review → Create → Review → APPROVE → Deploy → Monitor → Analyze → Iterate
 Tanmay    Tanmay   Zimmer  Leonardo   Zimmer   [YOU]     Mark      Mark     Zimmer    Zimmer
```

Stage 6 (Approve) is **mandatory human sign-off** — Mark cannot spend a single rupee without your explicit written approval.

---

## Quickstart

### Prerequisites
- Node.js v18+
- Claude Code (Claude Pro, $20/mo)
- Meta Business Manager account + ad account
- Pipeboard account (free at https://pipeboard.co)

### 1. Clone this template
```bash
git clone https://github.com/YOUR_USERNAME/marketing-agency.git my-product-agency
cd my-product-agency
```

### 2. Run setup
```bash
chmod +x setup.sh
./setup.sh
```

The setup script:
- Verifies Node.js v18+
- Initializes the Remotion project (Leonardo's workspace)
- Adds Pipeboard MCP to Claude Code (Mark's Meta Ads connection)
- Optionally installs additional Claude Code skills

### 3. Fill your product context
Open `state/product-context.md` and fill all 7 sections:
- Product basics (name, URL, price in INR, differentiator)
- Target audience (age, city tiers, languages, pain points)
- Competitive landscape (3–5 competitors with URLs)
- Brand voice & creative guidelines (tone, colors, do's/don'ts)
- Campaign goals (objective, CPA target, daily budget in INR)
- Past performance (if any)
- Assets available (images, videos, testimonials)

### 4. Start Claude Code and kick off Cycle 1
```bash
claude
```

Type:
```
Read CLAUDE.md, state/product-context.md, and skills/orchestrator/SKILL.md.
You are Zimmer, the Orchestrator. Initialize Cycle 1, Stage 1.
Invoke Tanmay for competitor and market research.
```

---

## Project Structure

```
marketing-agency/
├── CLAUDE.md                    ← Shared instructions (all agents read this)
├── OPERATIONS.md                ← Full human-facing operations guide
├── setup.sh                     ← One-command bootstrap script
│
├── state/
│   ├── product-context.md       ← Fill this first (human fills)
│   ├── system-log.md            ← Zimmer's running log
│   ├── orchestrator-notes.md    ← Zimmer's cycle analyses
│   ├── current-cycle.md         ← Current cycle number + stage checklist
│   └── approvals/
│       └── pending-approval.md  ← Human approval gate (required before any ad spend)
│
├── research/                    ← Tanmay's outputs
│   ├── competitor-analysis.md
│   ├── winning-hooks.md
│   ├── audience-insights.md
│   └── ad-library-data/        ← Drop competitor ad exports here
│
├── briefs/                      ← Tanmay → Leonardo
│   ├── creative-brief-001.md   ← Video (Reels 9:16)
│   ├── creative-brief-002.md   ← Static/Carousel
│   └── creative-brief-003.md
│
├── creatives/
│   ├── remotion-project/       ← Leonardo's Remotion codebase
│   ├── rendered/               ← Output MP4s and PNGs (gitignored)
│   └── review/creative-summary.md ← Leonardo's render report + Zimmer's review
│
├── campaigns/
│   ├── campaign-plan-001.md    ← Mark's campaign structure (reviewed before launch)
│   ├── live-campaigns.md       ← Active campaign IDs and status
│   └── performance/
│       ├── daily-report.md     ← Mark's daily metrics
│       └── optimization-notes.md ← Mark's insights for Tanmay next cycle
│
└── skills/
    ├── orchestrator/SKILL.md   ← Zimmer's identity and rules
    ├── marketing/SKILL.md      ← Tanmay's research and brief writing
    ├── remotion/SKILL.md       ← Leonardo's technical specs and templates
    └── ads/SKILL.md            ← Mark's campaign creation and monitoring
```

---

## Daily Commands (Quick Reference)

| What You Want | Type in Claude Code |
|---|---|
| Check status | `You are Zimmer. Give me the current status of everything.` |
| Start research | `You are Zimmer. Start Cycle [N], trigger Tanmay for research.` |
| Write briefs | `You are Tanmay. Write creative briefs based on the latest research.` |
| Review briefs | `You are Zimmer. Review the briefs in briefs/ for quality and completeness.` |
| Make creatives | `You are Leonardo. Produce creatives from the approved briefs. Read skills/remotion/SKILL.md.` |
| Review creatives | `You are Zimmer. Review the creatives in creatives/rendered/ against the briefs.` |
| Launch campaigns | `You are Mark. Create campaigns based on the approved plan. Check approvals first.` |
| Check performance | `You are Mark. Pull performance data and write the daily report.` |
| End-of-cycle analysis | `You are Zimmer. Analyze this cycle's performance and prepare for the next cycle.` |

**Resuming a session:**
```
Read CLAUDE.md, state/system-log.md, and state/current-cycle.md.
You are Zimmer, the Orchestrator. Resume from where we left off.
```

---

## Budget

| Item | Monthly Cost |
|---|---|
| Claude Pro | $20 (~₹1,700) |
| Pipeboard Free | $0 |
| Remotion (≤3 users) | $0 |
| Meta ad spend (min) | ₹500/day (~₹15,000/mo) |
| **All-in minimum** | **~₹16,700/mo (~$200)** |

---

## Using This Template for Multiple Products

Each product gets its own clone of this repo:

```bash
git clone https://github.com/YOUR_USERNAME/marketing-agency.git product-a-agency
git clone https://github.com/YOUR_USERNAME/marketing-agency.git product-b-agency
```

No cross-product contamination — each clone has its own `state/`, `research/`, `briefs/`, `creatives/`, and `campaigns/` directories. The agents (Zimmer, Tanmay, Leonardo, Mark) work only on what's in their own folder.

---

## Troubleshooting

See `OPERATIONS.md` for full troubleshooting guide.

**Most common issues:**
- Remotion preview: `cd creatives/remotion-project/my-ads && npx remotion studio`
- Pipeboard not connecting: `claude mcp list` → re-add if missing → restart Claude Code
- Research too generic: add more detail to `state/product-context.md` (specific competitor URLs, real customer quotes)
- Claude forgetting context: start every session with the resume command above

---

*Version 2.0 — Generic template. Indian market focus. Bare-minimum budget.*
*Agents: Zimmer (Orchestrator) | Tanmay (Strategist) | Leonardo (Creative Engine) | Mark (Media Buyer)*

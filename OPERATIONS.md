# Marketing Agency — Operations Guide

## The Team

| Agent | Name | Role |
|---|---|---|
| Orchestrator | **Zimmer** | Agency Director — coordinates, reviews, manages state, reports to you |
| Strategist | **Tanmay** | Research, competitor analysis, creative briefs |
| Creative Engine | **Leonardo** | Remotion video & image ad production |
| Media Buyer | **Mark** | Meta Ads campaign creation, launch & daily monitoring |

---

## First-Time Setup (30–60 minutes)

### Step 1: Run the setup script
```bash
cd marketing-agency
chmod +x setup.sh
./setup.sh
```

This script:
- Checks Node.js is installed (v18+ required)
- Initializes the Remotion project inside `creatives/remotion-project/my-ads/`
- Installs npm dependencies
- Guides you through Pipeboard MCP connection
- Optionally installs external Claude Code skills

### Step 2: Fill your product context
Open `state/product-context.md` in any text editor and fill all 7 sections.
**This is the most critical step. The quality of every agent's output depends on this.**

### Step 3: Open Claude Code
```bash
claude
```

Type:
> Read CLAUDE.md, state/system-log.md, and skills/orchestrator/SKILL.md.
> You are Zimmer, the Orchestrator. Initialize Cycle 1, Stage 1.
> Invoke Tanmay for competitor and market research.

---

## Daily Morning Routine (5 minutes, while campaigns are running)

```
You are Zimmer. Read state/system-log.md and state/current-cycle.md. Give me the current status.
Then invoke Mark to pull last 24 hours of performance data from Meta Ads.
```

---

## The 10-Stage Cycle — Complete Playbook

### Stage 1: RESEARCH — Tanmay

**Trigger:**
```
You are Zimmer. Start Cycle [N], Stage 1.
Invoke Tanmay. Task: Competitor and market research for the Indian market.
Read skills/marketing/SKILL.md for research instructions.
```

**Tanmay will:**
- Search Meta Ad Library for each competitor (Country = India, Status = Active)
- Analyze hook patterns, ad formats, CTAs
- Research TG pain points on Indian forums/social media

**Output files:**
- `research/competitor-analysis.md`
- `research/winning-hooks.md`
- `research/audience-insights.md`

---

### Stage 2: BRIEF — Tanmay

**Trigger:**
```
You are Tanmay. Write creative briefs based on the research in research/.
Read skills/marketing/SKILL.md for the brief template and quality checklist.
Write at least 3 briefs: briefs/creative-brief-001.md, 002.md, 003.md.
Brief 001 must be a video Reel (9:16). Brief 002 must be static or carousel.
```

**Output:** 3+ complete brief files in `briefs/`

---

### Stage 3: REVIEW-1 — Zimmer

**Trigger:**
```
You are Zimmer. Review the briefs in briefs/ against the quality checklist in skills/orchestrator/SKILL.md.
For each brief assess: hook specificity, script completeness, visual direction clarity, targeting alignment.
Advance to Stage 4 or return to Tanmay with specific revision feedback.
```

**If briefs pass:** Advance to Stage 4
**If briefs fail:** Return to Tanmay with line-by-line revision notes (not vague)

---

### Stage 4: CREATE — Leonardo

**Trigger:**
```
You are Leonardo. Produce creatives for the approved briefs in briefs/.
Read skills/remotion/SKILL.md for all technical specifications.
Work inside creatives/remotion-project/my-ads/.
Render all outputs to creatives/rendered/.
Write a summary to creatives/review/creative-summary.md.
```

**Leonardo's mandatory specs:**
- Correct dimensions per format (1080×1920 for 9:16, 1080×1080 for 1:1)
- Safe zones (150px top, 170px bottom for 9:16)
- Font sizes (headlines 56px+, body 36px+, labels 28px+)
- Hook in frames 0–90 (first 3 seconds at 30fps)
- Noto Sans Devanagari for any Hindi/Hinglish text

---

### Stage 5: REVIEW-2 — Zimmer

**Trigger:**
```
You are Zimmer. Review the creatives in creatives/rendered/ against the briefs they were based on.
Check the creative summary in creatives/review/creative-summary.md.
Use the review checklist in skills/orchestrator/SKILL.md.
If creatives pass, prepare the approval request for the human. If they fail, return to Leonardo with specific visual feedback.
```

---

### Stage 6: APPROVE — Human (MANDATORY)

**Zimmer will tell you:** "Creatives are ready for your review and approval."

**You do:**
1. View all files in `creatives/rendered/`
2. Read the briefs they're based on in `briefs/`
3. Decide daily budget and campaign duration

**Then write to `state/approvals/pending-approval.md`:**
```markdown
## APPROVAL — [YYYY-MM-DD]

**Approved by:** [Your name]
**Date:** [YYYY-MM-DD]
**Budget approved:** ₹[X]/day
**Duration:** [X days] before next review

**Campaigns approved:**
- Brief 001: brief-001.mp4 — Instagram Reels
- Brief 002: brief-002.png — Instagram/Facebook Feed
- Brief 003: brief-003.mp4 — Instagram Stories

**Notes for Mark:** [Any restrictions or special instructions]
```

**Then type:**
```
You are Zimmer. I've written my approval in state/approvals/pending-approval.md.
Confirm it's complete and advance to Stage 7. Invoke Mark to create campaigns.
```

---

### Stage 7: DEPLOY — Mark

**Trigger (Zimmer sends this to Mark):**
```
You are Mark. Read state/approvals/pending-approval.md first.
Confirm approval exists with today's date. If confirmed:
1. Write the campaign plan to campaigns/campaign-plan-001.md
2. Show Zimmer for review
3. After Zimmer confirms, execute via Pipeboard MCP
```

**Mark will:**
- Write campaign plan (Campaign → Ad Set → Ad structure)
- Get Zimmer's sign-off
- Create campaigns on Meta via Pipeboard MCP
- Update `campaigns/live-campaigns.md` with campaign/ad set IDs

---

### Stage 8: MONITOR — Mark (Daily)

**Run every morning:**
```
You are Mark. Pull yesterday's performance data from Meta Ads via Pipeboard MCP.
Write the daily report to campaigns/performance/daily-report.md.
Write optimization notes to campaigns/performance/optimization-notes.md.
Flag anything urgent to Zimmer.
```

**Monitoring period:** Minimum 48–72 hours before making major decisions.

---

### Stage 9: ANALYZE — Zimmer

Run after 3–7 days of campaign data:
```
You are Zimmer. We've completed Cycle [N].
Read all performance data in campaigns/performance/.
Read the original research in research/ and briefs in briefs/.
Write a complete cycle analysis to state/orchestrator-notes.md.
Include: what worked, what didn't, what Tanmay/Leonardo/Mark should do differently next cycle.
```

---

### Stage 10: ITERATE — Zimmer

```
You are Zimmer. Based on the analysis in state/orchestrator-notes.md, initialize Cycle [N+1].
Update state/current-cycle.md.
Brief Tanmay on what to focus on differently in the next cycle's research.
```

---

## Troubleshooting

### "Claude keeps forgetting context"
Normal — Claude Code has no memory between sessions. Start every session with:
```
Read CLAUDE.md, state/system-log.md, and state/current-cycle.md.
You are Zimmer, the Orchestrator. Resume from where we left off.
```

### "Remotion creatives look bad"
- Check font sizes: headlines min 56px, body min 36px, labels min 28px
- Check safe zones: 150px top, 170px bottom for 9:16 (Reels/Stories)
- Tell Leonardo specifically what looks wrong — never vague feedback
- Preview live: `cd creatives/remotion-project/my-ads && npx remotion studio`

### "Pipeboard MCP isn't connecting"
```bash
claude mcp list
# If pipeboard-meta-ads is missing:
claude mcp add --transport http pipeboard-meta-ads https://meta-ads.mcp.pipeboard.co
# Restart: exit → claude
# Type /mcp inside Claude Code to authenticate
```

### "Tanmay's research is too generic"
Add more detail to `state/product-context.md`:
- Specific competitor URLs (not just brand names)
- Real customer quotes or testimonials
- Exact cities/regions you're targeting
- Specific pain points in Indian consumer language

### "Running out of Claude Pro quota"
- Don't re-read CLAUDE.md every message — once per session only
- Use specific agent prompts, not open-ended questions
- Batch: review all briefs in one pass, not one at a time
- Schedule heavy tasks (research, creative production) in separate sessions

---

## Budget Reference

| Item | Monthly Cost (USD) | Monthly Cost (INR) | Notes |
|---|---|---|---|
| Claude Pro | $20/mo | ~₹1,700 | Required |
| Pipeboard Free | $0 | ₹0 | 30 executions/week |
| Remotion | $0 | ₹0 | Free for ≤3 users |
| Meta ad spend (min) | ~$180/mo | ~₹15,000/mo | ₹500/day × 30 |
| **Total minimum** | **~$200/mo** | **~₹16,700/mo** | |

### Upgrade Path (after 2 successful cycles)
| Upgrade | Cost | Why |
|---|---|---|
| Pipeboard Pro | +$29.90/mo | 500 executions/week |
| Apify Starter | +$49/mo | Automated competitor scraping |
| AWS Lambda (Remotion) | +$5–15/mo | Faster cloud video rendering |
| Claude Max | +$80/mo | 5× usage for heavy automation |

---

## Success Milestones

**After Cycle 1 (Week 1–2):**
- Product context filled and thorough
- Tanmay's competitor research complete
- 3+ creative briefs written by Tanmay
- 2–3 creatives rendered by Leonardo
- 1 campaign live via Mark, ₹500–1,000/day
- Baseline CPA established

**After Cycle 3 (Week 5–6):**
- 2 full cycles of learnings informing the next
- Leonardo's creative quality improved based on Mark's performance data
- Winning hooks and formats identified
- CPA trending downward

**After Cycle 5+ (Week 9+):**
- Full cycle runs in 2–3 hours of active operator time
- Clear playbook for what works for this product/TG
- Ready to scale budget or add Google Ads via Pipeboard

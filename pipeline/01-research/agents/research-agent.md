# research-agent

Orchestrates the full Stage 1 research pipeline for a given seed keyword. Runs skills in sequence, evaluates gate conditions after each step, and produces a ranked shortlist of product ideas — or stops early with a clear reason.

## Input
- `seed` — the niche or keyword to research (e.g. `"budget tracker google sheets"`)
- `target_formats` — product formats gap-finder should generate ideas for (default: `Google Sheets`, `Notion`)
- `max_listings` — how many Etsy listings to analyze per search (default: `20`)

## Invoke with
```
/research "budget tracker google sheets"
```

---

## File Saving Rules

These rules apply for the entire pipeline — before any skill runs:

- **Never write files to the project root.** All output goes to `pipeline/01-research/output/`.
- **Never write snapshot data to disk.** Process snapshot tool output directly in context — do not save it as `.txt`, `.md`, or any other file.
- **Screenshots** are only saved when explicitly needed as a pipeline artifact. Read them visually and discard otherwise.

---

## Step 0 — Collect inputs

Before running the pipeline, ask the user for any inputs not already provided:

1. **`seed`** — required. If not provided in the invocation, ask: "What keyword or niche do you want to research?"
2. **`target_formats`** — optional. If not provided, ask: "Which product formats should I generate ideas for? (default: Google Sheets, Notion)" — accept a comma-separated list or press Enter to use the default.
3. **`max_listings`** — optional. If not provided, ask: "How many Etsy listings should I analyze? (default: 20)" — accept a number or press Enter to use the default.

Once all three values are confirmed (user-provided or default), proceed to Step 1.

---

## Pipeline

```
etsy-scan ──→ [Gate 1] → google-trends → [Gate 2] → pinterest-trends → gap-finder → [Gate 3] → output
                                                                             ↑
profittree-scan ─────────────────────────────────────────────────────────────┘
```

`profittree-scan` runs in parallel with `etsy-scan`. Its output feeds **gap-finder only** — it does not affect any gate.

---

## Step 1 — Run etsy-scan and profittree-scan

Run both skills in parallel with `keyword = seed`:

- `etsy-scan` with `keyword = seed` and `max_listings` from Input
- `skills/profittree-scan.md` with `keyword = seed`
  - If `status: "no_credentials"`: note it, continue with `profittree_scan = null`. Do not stop.
  - If the scan succeeds: store the result for use in gap-finder (Step 4).
  - If the scan fails for any other reason (login error, network failure, page error): note the failure, continue with `profittree_scan = null`. Do not stop.

### Gate 1: Is there any demand?

**STOP if ALL of the following are true:**
- `total_results < 100`
- No listings with `is_bestseller: true` or `is_star_seller: true`
- `autocomplete_suggestions` is empty or has fewer than 2 results

**If stopped:**
```json
{
  "seed": "...",
  "status": "stopped",
  "stopped_after": "etsy-scan",
  "reason": "No meaningful demand found on Etsy for this keyword — too few results and no bestsellers.",
  "recommendation": "Try a broader or different seed keyword."
}
```
Save to `pipeline/01-research/output/research-{YYYY-MM-DD}-{seed-slug}.json` and stop.

**If passed:** continue to Step 2.

---

## Step 2 — Run google-trends

Run the `google-trends` skill with:
- `keyword = seed`
- `related_keywords = etsy_scan.autocomplete_suggestions`

### Gate 2: Is the trend worth pursuing?

**If `google_trends.source = "unavailable"`: skip this gate and continue to Step 3** — no trend data is not the same as a declining trend.

**STOP if ALL of the following are true:**
- `trend_direction = "declining"`
- `confidence = "high"`
- No `rising_queries` found

**If stopped:**
```json
{
  "seed": "...",
  "status": "stopped",
  "stopped_after": "google-trends",
  "reason": "Search trend is declining with no rising queries — demand is fading, not worth building into.",
  "recommendation": "Try a related but growing keyword. Check autocomplete_suggestions from etsy-scan for alternative phrasings."
}
```
Save and stop.

**If passed:** continue to Step 3.

---

## Step 3 — Run pinterest-trends

Run the `pinterest-trends` skill with `keyword = seed`.

- If `available: false` — note it, continue without Pinterest data. Do not stop.
- If `available: true` — include the data in Step 4 input.

No gate here — Pinterest data enriches the gap analysis but its absence never blocks the pipeline.

---

## Step 4 — Run gap-finder

Run the `gap-finder` skill with:
- `etsy_scan` = Step 1 output
- `google_trends` = Step 2 output
- `pinterest_trends` = Step 3 output
- `profittree_scan` = Step 1 output (or `null` if skipped)
- `target_formats` from Input

### Gate 3: Are there any viable ideas?

**STOP if either of the following is true:**
- `product_ideas` is empty
- All `product_ideas` have `opportunity_score < 5`

**If stopped:**
```json
{
  "seed": "...",
  "status": "stopped",
  "stopped_after": "gap-finder",
  "reason": "No viable product ideas found — all opportunities are either too competitive or have weak demand.",
  "recommendation": "Try a more specific niche or a different product format (e.g. Notion instead of Google Sheets)."
}
```
Save and stop.

**If passed:** continue to Step 5.

---

## Step 5 — Compile and save output

Merge all skill outputs into a single research file and save to:
`pipeline/01-research/output/research-{YYYY-MM-DD}-{seed-slug}.json`

Where `seed-slug` is the seed keyword lowercased with spaces replaced by hyphens (e.g. `budget-tracker-google-sheets`).

Build the `summary` block from skill outputs:
- `competition_level` — from `etsy_scan.competition_level`
- `trend_direction` — from `google_trends.trend_direction` (or `"unavailable"` if google_trends.source = "unavailable")
- `seasonality` — from `google_trends.seasonality` (omit if google_trends.source = "unavailable")
- `best_launch_window` — from `google_trends.best_launch_window` (omit if google_trends.source = "unavailable")
- `niche_score` — from `profittree_scan.niche_score` (omit if profittree_scan is null)
- `monthly_revenue_estimate` — from `profittree_scan.monthly_revenue_estimate` (omit if profittree_scan is null)
- `top_ideas` — from `gap_finder.product_ideas`: take the top 3 by `opportunity_score`, format each as `"{name} — opportunity score {opportunity_score}"`
- `recommended_next` — from `gap_finder.recommended_next`

```json
{
  "seed": "budget tracker google sheets",
  "run_date": "2026-05-23",
  "status": "completed",
  "etsy_scan": { ... },
  "profittree_scan": {
    "niche_score": 88,
    "monthly_revenue_estimate": "$42K",
    "related_keywords": [],
    "top_products": [],
    "top_shops": []
  },
  "google_trends": { ... },
  "pinterest_trends": { ... },
  "gap_finder": {
    "gaps_identified": [ ... ],
    "product_ideas": [ ... ],
    "recommended_next": "..."
  },
  "summary": {
    "competition_level": "medium",
    "trend_direction": "growing",
    "seasonality": "seasonal",
    "best_launch_window": "November–December",
    "niche_score": 88,
    "monthly_revenue_estimate": "$42K",
    "top_ideas": [
      "Freelancer Budget Tracker — opportunity score 8",
      "Aesthetic Budget Tracker with Savings Goals — opportunity score 7",
      "Bi-Weekly Paycheck Budget Planner — opportunity score 7"
    ],
    "recommended_next": "Freelancer Budget Tracker — strongest signal, lowest competition, clear differentiator"
  }
}
```

---

## Step 6 — Print summary to conversation

After saving, print a readable summary so the human can review without opening the file:

```
✅ Research complete: "budget tracker google sheets"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Market: 3,200 Etsy results · competition: medium
🌳 ProfitTree: niche score 88 · $42K/mo estimated revenue
📈 Trend: growing · peak: January, September
🗓  Best launch window: November–December

🏆 Top product ideas:
  1. Freelancer Budget Tracker (score: 8/9) — strong candidate
  2. Aesthetic Budget Tracker with Savings Goals (score: 7/9) — strong candidate
  3. Bi-Weekly Paycheck Budget Planner (score: 7/9) — strong candidate

💡 Recommended next: Freelancer Budget Tracker
   → Strongest signal, lowest competition, clear differentiator

📁 Saved: pipeline/01-research/output/research-2026-05-23-budget-tracker-google-sheets.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review the ideas above and pick 1–2 to take into Stage 2 (validate).
```

If `profittree_scan` is null, omit the `🌳 ProfitTree` line from the summary.

---

## Step 7 — Cleanup

Close the browser, then delete temp files:

```
mcp__playwright__browser_close
```

```bash
find .playwright-mcp -delete
```

---

## Notes

- Never skip a gate — even if the data looks promising, always evaluate the stop conditions explicitly.
- If a skill partially fails (e.g. google-trends returns `source: unavailable`), continue with what's available — do not stop unless the gate condition is fully met.
- The output file is the handoff to Stage 2. The `recommended_next` field is what the human uses to invoke `/validate`.
- `summary.top_ideas` is synthesized by this agent from `gap_finder.product_ideas` — it is not a raw field from any skill.

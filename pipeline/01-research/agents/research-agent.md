# research-agent

Orchestrates the full Stage 1 research pipeline for a given seed keyword. Runs skills in sequence, evaluates gate conditions after each step, and produces a ranked shortlist of product ideas — or stops early with a clear reason.

## Input
- `seed` — the niche or keyword to research (e.g. `"budget tracker google sheets"`)

## Invoke with
```
/research "budget tracker google sheets"
```

---

## Pipeline

```
etsy-scan → [Gate 1] → google-trends → [Gate 2] → pinterest-trends → gap-finder → [Gate 3] → output
```

---

## Step 1 — Run etsy-scan

Run the `etsy-scan` skill with `keyword = seed`.

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
- `confidence = "low"`
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
- `top_ideas` — from `gap_finder.product_ideas`: take the top 3 by `opportunity_score`, format each as `"{name} — opportunity score {opportunity_score}"`
- `recommended_next` — from `gap_finder.recommended_next`

```json
{
  "seed": "budget tracker google sheets",
  "run_date": "2026-05-23",
  "status": "completed",
  "etsy_scan": { ... },
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

---

## Step 7 — Cleanup

```bash
find .playwright-mcp -type f -delete
```

---

## Notes

- Never skip a gate — even if the data looks promising, always evaluate the stop conditions explicitly.
- If a skill partially fails (e.g. google-trends returns `source: unavailable`), continue with what's available — do not stop unless the gate condition is fully met.
- The output file is the handoff to Stage 2. The `recommended_next` field is what the human uses to invoke `/validate`.
- `summary.top_ideas` is synthesized by this agent from `gap_finder.product_ideas` — it is not a raw field from any skill.

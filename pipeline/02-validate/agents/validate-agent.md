# validate-agent

Orchestrates the full Stage 02 validation pipeline. Can validate a single product idea or all ideas from a 01-research output file. Reads the 01-research output, runs targeted Etsy search, mines competitor reviews, and checks pricing. Outputs a go/no-go recommendation for human decision.

## Input
- `product_idea` — optional. If provided, validate only that idea. If omitted, validate all ideas in `gap_finder.product_ideas[]` from the research file, in ranked order.
- `research_file` — optional. Path to the 01-research output JSON. If not provided, scan `pipeline/01-research/output/` for the most recent file.

## Invoke with
```
/validate "Minimal ADHD Notion Planner — The 5-Feature System"
/validate "pipeline/01-research/output/research-2026-05-24-adhd-planner-notion-template.json"
/validate
```

If the argument ends in `.json` or starts with `pipeline/`, treat it as `research_file`. Otherwise treat it as `product_idea`.

---

## File Saving Rules

- **Never write files to the project root.** All output goes to `pipeline/02-validate/output/`.
- **Never write snapshot data to disk.** Process snapshot tool output directly in context.
- **Screenshots** are only saved when explicitly needed as a pipeline artifact.

---

## Step 0 — Load research context

Find and read the relevant 01-research output file:

1. If `research_file` was provided: read it directly.
2. If `product_idea` was provided but no `research_file`: list files in `pipeline/01-research/output/`, read the most recent one that contains the `product_idea` name in `gap_finder.product_ideas[].name` or `gap_finder.recommended_next`.
3. If neither was provided: list files in `pipeline/01-research/output/`, read the most recent one.
4. If no file found: ask the user to specify which research file to use.

**Determine run scope:**
- If `product_idea` was provided → run Steps 1–5 once for that idea, then Step 6.
- If `product_idea` was omitted → run Steps 1–5 for each idea in `gap_finder.product_ideas[]` in ranked order, then Step 6 once at the end.

Extract the following and hold in context for the entire run. The first block is constant across all ideas; the second block is re-derived per idea in batch mode:

**Constant across all ideas (load once):**

| Variable | Source in research file |
|---|---|
| `seed` | `seed` |
| `research_top_listings` | `etsy_scan.top_listings` |
| `research_price_median` | `etsy_scan.price_median` |
| `research_competition_level` | `etsy_scan.competition_level` |
| `research_trend_direction` | `google_trends.trend_direction` |
| `research_gaps` | `gap_finder.gaps_identified` |
| `dominant_competitor_review_threshold` | median of `etsy_scan.top_listings[].reviews` — a competitor is "dominant" if it has Star Seller status AND reviews ≥ this value |
| `max_reviews_per_listing` | 20 (enough to identify repeating patterns; diminishing returns beyond this) |
| `max_listings_per_query` | 10 |
| `min_reviews_to_mine` | same as `dominant_competitor_review_threshold` |

**Re-derived per idea (before each iteration):**

| Variable | Source |
|---|---|
| `product_idea_data` | matching entry in `gap_finder.product_ideas[]` for the current idea |
| `positioning` | 1–2 word tag from `product_idea_data.differentiator` — take the most distinctive adjective or audience word (e.g. "minimalist", "student", "shame-free", "gamified") |

---

## Pipeline

```
etsy-deep-dive ──┬→ price-check ─┐
                 └→ review-miner ─┴→ go/no-go → output
```

`price-check` and `review-miner` both depend on `etsy-deep-dive` output — run etsy-deep-dive first. Then run price-check and review-miner in parallel.

---

## Step 1 — Run etsy-deep-dive

Run `etsy-deep-dive` with:
- `product_idea` — from input
- `seed_keyword` — `seed` from research context
- `research_top_listings` — from research context
- `research_competition_level` — from research context
- `max_listings` — `max_listings_per_query` from research context

If `etsy-deep-dive` returns blocked: note it, continue with remaining skills using `research_top_listings` as fallback data.

---

## Step 2 — Run price-check and review-miner in parallel

**price-check** with:
- `research_etsy_scan` — full `etsy_scan` block from research context
- `deep_dive_results` — Step 1 output
- `product_idea` — from input
- `positioning` — from research context

**review-miner** with:
- `product_idea` — from input
- `listings_to_mine` — direct competitors from `etsy-deep-dive.direct_competitors` if any found; otherwise `research_top_listings[0..1]` (top 2 by listing order)
- `min_reviews_to_mine` — from research context
- `max_reviews_per_listing` — from research context

---

## Step 3 — Evaluate go/no-go

Apply the gate conditions using values derived from research — not hard-coded thresholds:

**NO-GO if ANY of the following:**
- A direct competitor from `etsy-deep-dive` is dominant (Star Seller AND reviews ≥ `dominant_competitor_review_threshold`) AND matches the product idea's core differentiator exactly
- `research_trend_direction` = `"declining"` AND `price-check` shows the majority of listings are in the budget band (race-to-bottom signal)
- `review-miner` found no unmet needs — all reviews are generic positives with no complaints or missing-feature mentions

**GO if ALL of the following:**
- No dominant direct competitor for the specific angle (or existing competitors have clear weaknesses in reviews)
- `review-miner.unmet_needs` contains at least one need the proposed product directly addresses
- `price-check.recommendations.launch_price` ≥ `research_price_median` — the median is a more meaningful floor than the outlier minimum; going below it signals low quality

**Borderline (human judgment needed):** everything else — present the evidence clearly and let the human decide.

---

## Step 4 — Save output

Save to:
`pipeline/02-validate/output/validate-{YYYY-MM-DD}-{product-idea-slug}.json`

Where `product-idea-slug` is the product idea lowercased with spaces/special chars replaced by hyphens.

```json
{
  "product_idea": "Minimal ADHD Notion Planner — The 5-Feature System",
  "seed": "ADHD planner notion template",
  "research_ref": "pipeline/01-research/output/research-2026-05-24-adhd-planner-notion-template.json",
  "run_date": "2026-05-24",
  "status": "completed",
  "etsy_deep_dive": { ... },
  "review_miner": { ... },
  "price_check": { ... },
  "decision": {
    "verdict": "go",
    "confidence": "high",
    "go_signals": [ ... ],
    "risk_flags": [ ... ],
    "recommended_title_keyword": "...",
    "recommended_launch_price": "{price_check.recommendations.launch_price}",
    "recommended_target_price": "{price_check.recommendations.target_price}"
  }
}
```

---

## Step 5 — Print summary and prompt for decision

Print a readable summary so the human can make a go/no-go call. Replace all placeholder values with real data from this run:

````
```
✅ Validation complete: "{product_idea}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Direct competitors found: {count} ({note})
📊 Specific angle search results: {total_results} ({interpretation})
💬 Review insights ({N} reviews across {M} listings):
   ✅ Buyers praise: {top_praised}
   ❌ Buyers complain: {top_complained}
   💡 Unmet need confirmed: "{key buyer_voice_phrase}"

💰 Pricing:
   Market center: {market_center}
   Launch price: {launch_price} ({discount}% off {display_original_price})
   Target price: {target_price} after first reviews

🏷  Recommended title keyword: "{recommended_title_keyword}"

{verdict emoji} Verdict: {GO / NO-GO / BORDERLINE}
   → {primary reason}

📁 Saved: pipeline/02-validate/output/validate-{date}-{slug}.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{if GO}  Proceed to Stage 03?
  /poc "{product_idea}"
{if NO-GO}  Consider these alternatives from research:
  /validate "{next highest-ranked idea from gap_finder.product_ideas[] not yet validated}"
```
````

---

## Step 6 — Cleanup

Close the browser, then delete temp files:

```
mcp__playwright__browser_close
```

```bash
find .playwright-mcp -delete
```

---

## Notes

- The validate agent does not re-run Google Trends or Pinterest — those signals are already in the research file.
- All thresholds used in go/no-go gate are derived from the research data, not hard-coded — this keeps the gate calibrated to each niche's actual market size.
- The `decision.recommended_title_keyword` flows directly into Stage 06 marketing — the etsy-listing skill uses it to build the listing title.

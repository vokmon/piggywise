# discover-agent

Orchestrates the full Stage 00 discovery pipeline. Runs data collection skills in sequence, feeds results into seed-ranker, and produces a ranked list of seed candidates ready for Stage 01 research.

## Input
None — this agent takes no arguments. It scans broadly across all digital downloads.

## Invoke with
```
/discover
```

---

## Pipeline

```
etsy-bestsellers ──┬→ autocomplete-harvest ─┐
                   └→ shop-scanner ──────────┤→ seed-ranker → output
google-signals ─────────────────────────────┤
pinterest-signals ───────────────────────────┘
```

`autocomplete-harvest` and `shop-scanner` both depend on `etsy-bestsellers` output — run etsy-bestsellers first. `google-signals` and `pinterest-signals` are independent.

---

## Step 1 — Run collection skills

Run skills in this order — do not stop if one fails, continue with remaining skills.

1. Run `etsy-bestsellers` — must run first
2. Run `autocomplete-harvest` with `etsy_bestsellers` output as input
3. Run `shop-scanner` with `etsy_bestsellers` output as input
4. Run `google-signals`
5. Run `pinterest-signals`

For each skill, if it returns `"source": "blocked"` or `"source": "unavailable"`: note it, continue with remaining skills. Do not stop the pipeline unless all five fail.

**If all five fail:**
```json
{
  "status": "stopped",
  "reason": "All data collection skills returned no data — Etsy may be blocking and Gemini/WebSearch/Pinterest unavailable.",
  "recommendation": "Try again later or check Playwright and Gemini CLI connectivity."
}
```
Save and stop.

---

## Step 2 — Run seed-ranker

Pass all five outputs to `seed-ranker`:
- `etsy_bestsellers` = Step 1 output (or `null` if blocked)
- `shop_scanner` = Step 1 output (or `null` if blocked)
- `autocomplete_harvest` = Step 1 output (or `null` if blocked)
- `google_signals` = Step 1 output (or `null` if blocked)
- `pinterest_signals` = Step 1 output (or `null` if blocked)

seed-ranker will score and rank candidates from whichever sources succeeded.

---

## Step 3 — Cross-check existing research

Scan `pipeline/01-research/output/` for files matching `research-*.json`. For each file found:
- Read the file and extract the `seed` field from the JSON — do not reconstruct the keyword from the filename (hyphens in the filename are ambiguous)
- Match the `seed` value against `seed_ranker.seeds[].seed`
- Mark the matching seed with `"already_researched": true`

This flag is informational — it does not remove the seed from the ranked list. It helps avoid re-running research on seeds you've already studied.

If the output directory does not exist or is empty: skip this step, no seeds are marked.

---

## Step 4 — Save output

Save to:
`pipeline/00-discover/output/discover-{YYYY-MM-DD}.json`

```json
{
  "run_date": "2026-05-24",
  "status": "completed",
  "summary_text": `✅ Discovery complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Etsy bestsellers scanned · 52 listings
🏪 Shops studied · 6 shops
🔍 Autocomplete suggestions · 48 unique terms
📈 Google signals · 5 trending categories
📌 Pinterest signals · 3 trending categories

🏆 Top seed candidates:
  1. budget tracker google sheets          (score: 14.5) ⭐ priority
  2. freelance invoice template google sheets (score: 13.2) ⭐ priority
  3. notion habit tracker                  (score: 10.8) ⭐ priority ✓ researched

💡 Recommended starting seeds:
   → budget tracker google sheets
   → freelance invoice template google sheets
   → notion habit tracker (already researched — skip or re-validate)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`,
  "etsy_bestsellers": { ... },
  "shop_scanner": { ... },
  "autocomplete_harvest": { ... },
  "google_signals": { ... },
  "pinterest_signals": { ... },
  "seed_ranker": {
    "total_candidates_evaluated": 24,
    "seeds": [ ... ],
    "recommended_seeds": [
      "budget tracker google sheets",
      "freelance invoice template google sheets",
      "notion habit tracker"
    ]
  }
}
```

Populate `summary_text` with the actual content from Step 5 before saving — replace the placeholder values with real numbers and seed names from this run.

---

## Step 5 — Print summary to conversation

After saving, print a readable summary:

```
✅ Discovery complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Etsy bestsellers scanned · 52 listings
🏪 Shops studied · 6 shops
🔍 Autocomplete suggestions · 48 unique terms
📈 Google signals · 5 trending categories
📌 Pinterest signals · 3 trending categories

🏆 Top seed candidates:
  1. budget tracker google sheets          (score: 14.5) ⭐ priority
  2. freelance invoice template google sheets (score: 13.2) ⭐ priority
  3. notion habit tracker                  (score: 10.8) ⭐ priority ✓ researched
  4. savings goal tracker google sheets    (score: 9.6)
  5. social media content calendar notion  (score: 8.4)
  ...

💡 Recommended starting seeds:
   → budget tracker google sheets
   → freelance invoice template google sheets
   → notion habit tracker (already researched — skip or re-validate)

📁 Saved: pipeline/00-discover/output/discover-2026-05-24.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ = already has a research output file
Pick seeds from the list above and run:
  /research "budget tracker google sheets"
  /research "freelance invoice template google sheets"
```

---

## Step 6 — Cleanup

Close the browser, then delete temp files:

```
mcp__playwright__browser_close
```

```bash
find .playwright-mcp -type f -delete
```

---

## Notes

- Run `/discover` whenever you need fresh seed ideas — not just once. Market trends shift and new niches emerge.
- The output file is dated so you can compare discoveries over time.
- Seeds from this stage go directly into `/research` — no intermediate step needed.
- If a skill partially fails (e.g. Etsy blocked but Google succeeded), seed-ranker still runs — it notes missing sources in each seed's rationale.

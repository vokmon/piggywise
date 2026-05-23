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
google-signals ────────────────────────────┘
```

`autocomplete-harvest` and `shop-scanner` both depend on `etsy-bestsellers` output — run etsy-bestsellers first. `google-signals` is independent.

---

## Step 1 — Run collection skills

Run skills in this order — do not stop if one fails, continue with remaining skills.

1. Run `etsy-bestsellers` — must run first
2. Run `autocomplete-harvest` with `etsy_bestsellers` output as input
3. Run `shop-scanner` with `etsy_bestsellers` output as input
4. Run `google-signals`

For each skill, if it returns `"source": "blocked"` or `"source": "unavailable"`: note it, continue with remaining skills. Do not stop the pipeline unless all four fail.

**If all four fail:**
```json
{
  "status": "stopped",
  "reason": "All data collection skills returned no data — Etsy may be blocking and Gemini/WebSearch unavailable.",
  "recommendation": "Try again later or check Playwright and Gemini CLI connectivity."
}
```
Save and stop.

---

## Step 2 — Run seed-ranker

Pass all four outputs to `seed-ranker`:
- `etsy_bestsellers` = Step 1 output (or `null` if blocked)
- `shop_scanner` = Step 1 output (or `null` if blocked)
- `autocomplete_harvest` = Step 1 output (or `null` if blocked)
- `google_signals` = Step 1 output (or `null` if blocked)

seed-ranker will score and rank candidates from whichever sources succeeded.

---

## Step 3 — Save output

Save to:
`pipeline/00-discover/output/discover-{YYYY-MM-DD}.json`

```json
{
  "run_date": "2026-05-23",
  "status": "completed",
  "etsy_bestsellers": { ... },
  "shop_scanner": { ... },
  "autocomplete_harvest": { ... },
  "google_signals": { ... },
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

---

## Step 4 — Print summary to conversation

After saving, print a readable summary:

```
✅ Discovery complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Etsy bestsellers scanned · 52 listings
🏪 Shops studied · 6 shops
🔍 Autocomplete suggestions · 48 unique terms
📈 Google signals · 5 trending categories

🏆 Top seed candidates:
  1. budget tracker google sheets          (score: 13.2) ⭐ priority
  2. freelance invoice template google sheets (score: 12.0) ⭐ priority
  3. notion habit tracker                  (score: 10.8) ⭐ priority
  4. savings goal tracker google sheets    (score: 9.6)
  5. social media content calendar notion  (score: 8.4)
  ...

💡 Recommended starting seeds:
   → budget tracker google sheets
   → freelance invoice template google sheets
   → notion habit tracker

📁 Saved: pipeline/00-discover/output/discover-2026-05-23.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pick 3–5 seeds from the list above and run:
  /research "budget tracker google sheets"
  /research "freelance invoice template google sheets"
```

---

## Step 5 — Cleanup

```bash
find .playwright-mcp -type f -delete
```

---

## Notes

- Run `/discover` whenever you need fresh seed ideas — not just once. Market trends shift and new niches emerge.
- The output file is dated so you can compare discoveries over time.
- Seeds from this stage go directly into `/research` — no intermediate step needed.
- If a skill partially fails (e.g. Etsy blocked but Google succeeded), seed-ranker still runs — it notes missing sources in each seed's rationale.

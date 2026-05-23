# seed-ranker

Synthesize outputs from etsy-bestsellers, shop-scanner, autocomplete-harvest, and google-signals into a single ranked list of seed candidates. This skill reasons over collected data only — it does not browse or call external tools.

## Input
- `etsy_bestsellers` — output from etsy-bestsellers skill
- `shop_scanner` — output from shop-scanner skill
- `autocomplete_harvest` — output from autocomplete-harvest skill
- `google_signals` — output from google-signals skill

---

## Steps

### 1. Collect and deduplicate all raw candidates

Pool `raw_seed_candidates` from all four inputs:
- `etsy_bestsellers.raw_seed_candidates`
- `shop_scanner.raw_seed_candidates`
- `autocomplete_harvest.raw_seed_candidates`
- `google_signals.raw_seed_candidates`

Deduplicate by normalizing to lowercase and merging near-duplicates (e.g. "budget tracker google sheets" and "google sheets budget tracker" → keep the more natural phrasing).

Aim for 20–30 unique candidates before scoring.

### 2. Score each candidate

Rate each seed across four dimensions (1–3 scale):

| Dimension | 1 | 2 | 3 |
|---|---|---|---|
| **Etsy demand** | Not seen in bestsellers or shops | Appeared in autocomplete or 1 shop | Bestseller pattern or 2+ shops |
| **Google momentum** | `direction: declining` in google-signals, or not found | `direction: stable` | `direction: growing` or emerging |
| **Competition fit** | Saturated (high Etsy volume, many bestsellers) | Medium (beatable) | Low (clear gap visible) |
| **Format fit** | Poor fit for Google Sheets / Notion / digital template | Moderate fit | Natural fit — buyers clearly want a digital file |

`seed_score` = Etsy demand + Google momentum + Competition fit + Format fit (base max 12, before autocomplete multiplier)

### 3. Apply multiplier for autocomplete presence

If a candidate appeared directly in Etsy autocomplete: multiply score × 1.2 (round to 1 decimal).
Autocomplete = buyers are actively typing this exact phrase — highest intent signal.

### 4. Rank and filter

- Keep top 15 candidates by score
- Remove any with `seed_score < 5` — too weak to research
- Flag top 3 with `"priority": true`

**When an input is null or blocked:** score that dimension as 1 (worst case) — do not skip the seed entirely. Note the missing source in `rationale`.

### 5. Add a one-line rationale per seed

For each seed, write one sentence explaining why it scored the way it did — grounded in the actual data collected.

---

## Output

Return a JSON object to the calling agent (`discover-agent`):

```json
{
  "total_candidates_evaluated": 24,
  "seeds": [
    {
      "rank": 1,
      "seed": "budget tracker google sheets",
      "seed_score": 13.2,
      "priority": true,
      "scores": {
        "etsy_demand": 3,
        "google_momentum": 3,
        "competition_fit": 2,
        "format_fit": 3
      },
      "autocomplete_multiplier": true,
      "rationale": "Appears in Etsy autocomplete, bestsellers across 4 shops, strong Google growth signal, natural Google Sheets format — competition is medium but clear differentiation opportunities exist."
    },
    {
      "rank": 2,
      "seed": "freelance invoice template google sheets",
      "seed_score": 12.0,
      "priority": true,
      "scores": {
        "etsy_demand": 3,
        "google_momentum": 3,
        "competition_fit": 3,
        "format_fit": 3
      },
      "autocomplete_multiplier": false,
      "rationale": "Cross-shop pattern in 3 shops, growing Google signal from freelance economy, low Etsy competition in the specific freelancer angle."
    },
    {
      "rank": 3,
      "seed": "notion habit tracker",
      "seed_score": 10.8,
      "priority": true,
      "scores": {
        "etsy_demand": 2,
        "google_momentum": 2,
        "competition_fit": 2,
        "format_fit": 3
      },
      "autocomplete_multiplier": true,
      "rationale": "Strong Etsy autocomplete presence and shop pattern, stable Google signal, medium competition — needs a clear differentiator to stand out."
    }
  ],
  "recommended_seeds": [
    "budget tracker google sheets",
    "freelance invoice template google sheets",
    "notion habit tracker"
  ],
  "note": "Run /research on each recommended seed to get full demand, trend, and gap analysis before committing."
}
```

---

## Notes

- This skill reasons only — never browse or call tools.
- If one input source was blocked or unavailable, score on the remaining sources and note the missing input in `rationale`.
- The output of this skill is what the human reviews to decide which seeds to take into Stage 01.
- `recommended_seeds` should be the top 3 — a manageable starting set. The human can always pick more from the full ranked list.

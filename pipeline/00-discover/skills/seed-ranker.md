# seed-ranker

Synthesize outputs from etsy-bestsellers, shop-scanner, autocomplete-harvest, google-signals, and pinterest-signals into a single ranked list of seed candidates. This skill reasons over collected data only — it does not browse or call external tools.

## Input
- `etsy_bestsellers` — output from etsy-bestsellers skill
- `shop_scanner` — output from shop-scanner skill
- `autocomplete_harvest` — output from autocomplete-harvest skill
- `google_signals` — output from google-signals skill
- `pinterest_signals` — output from pinterest-signals skill

---

## Steps

### 1. Collect and deduplicate all raw candidates

Pool `raw_seed_candidates` from all five inputs:
- `etsy_bestsellers.raw_seed_candidates`
- `shop_scanner.raw_seed_candidates`
- `autocomplete_harvest.raw_seed_candidates`
- `google_signals.raw_seed_candidates`
- `pinterest_signals.raw_seed_candidates`

Deduplicate by normalizing to lowercase and merging near-duplicates (e.g. "budget tracker google sheets" and "google sheets budget tracker" → keep the more natural phrasing).

Aim for 20–30 unique candidates before scoring.

### 2. Score each candidate

Rate each seed across four dimensions (1–3 scale):

| Dimension | 1 | 2 | 3 |
|---|---|---|---|
| **Etsy demand** | Not seen in bestsellers or shops | Appeared in autocomplete or 1 shop | Bestseller pattern or 2+ shops |
| **Google momentum** | `direction: declining` in google-signals, or not found | `direction: stable` | `direction: growing` or emerging |
| **Competition fit** | Saturated (high Etsy volume, many bestsellers) | Medium (beatable) | Low (clear gap visible) |
| **Format fit** | Poor fit for any digital template format | Moderate fit | Natural fit — buyers clearly want a digital file |

`seed_score` = Etsy demand + Google momentum + Competition fit + Format fit (base max 12, before autocomplete multiplier)

### 3. Apply multipliers

**Autocomplete multiplier (×1.2):** if the candidate appeared directly in Etsy autocomplete suggestions.
Autocomplete = buyers are actively typing this exact phrase — highest intent signal.

**Pinterest multiplier (×1.1):** if the candidate's keyword or topic appears in `pinterest_signals.trending_categories` where `direction: "growing"`.
Pinterest = early demand signal before Etsy search volume catches up.

Multipliers stack: autocomplete × Pinterest = ×1.2 × ×1.1 = ×1.32. Round final score to 1 decimal.

### 4. Rank and filter

- Keep top 15 candidates by score
- Remove any with `seed_score < 5` — too weak to research
- Flag top 3 with `"priority": true`

**When an input is null or blocked:** score that dimension as 1 (worst case) — do not skip the seed entirely. Note the missing source in `rationale`. If `pinterest_signals` is null or unavailable, treat `pinterest_multiplier` as false for all seeds.

**When an input has `source: "partial"`:** use the data as-is but note the limited coverage in each seed's `rationale` (e.g. "shop-scanner data is partial — fewer than 3 shops reachable").

### 5. Add a one-line rationale per seed

For each seed, write one sentence explaining why it scored the way it did — grounded in the actual data collected.

---

## Output

Return a JSON object to the calling agent:

```json
{
  "total_candidates_evaluated": 24,
  "seeds": [
    {
      "rank": 1,
      "seed": "budget tracker google sheets",
      "seed_score": 14.5,
      "priority": true,
      "scores": {
        "etsy_demand": 3,
        "google_momentum": 3,
        "competition_fit": 2,
        "format_fit": 3
      },
      "autocomplete_multiplier": true,
      "pinterest_multiplier": true,
      "rationale": "Appears in Etsy autocomplete, bestsellers across 4 shops, strong Google growth signal, growing Pinterest category — competition is medium but clear differentiation opportunities exist."
    },
    {
      "rank": 2,
      "seed": "freelance invoice template google sheets",
      "seed_score": 13.2,
      "priority": true,
      "scores": {
        "etsy_demand": 3,
        "google_momentum": 3,
        "competition_fit": 3,
        "format_fit": 3
      },
      "autocomplete_multiplier": false,
      "pinterest_multiplier": true,
      "rationale": "Cross-shop pattern in 3 shops, growing Google signal from freelance economy, growing Pinterest category, low Etsy competition in the specific freelancer angle."
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
      "pinterest_multiplier": false,
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
- If one input source was blocked or unavailable, score on the remaining sources and note the missing input in `rationale`. Missing `pinterest_signals` sets all `pinterest_multiplier` to false.
- The output of this skill is what the human reviews to decide which seeds to take into Stage 01.
- `recommended_seeds` should be the top 3 — a manageable starting set. The human can always pick more from the full ranked list.

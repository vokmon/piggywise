# pinterest-signals

Identify broad trending categories on Pinterest Trends. Pinterest data typically leads Etsy by 3–6 months — useful for spotting what's coming before it appears in Etsy search volume.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.
Follows `skills/pinterest-lookup.md` for Pinterest authentication.

## Input
- `pinterest_terms` — list of terms to search on Pinterest Trends

## Steps

### 1. Login

Run `skills/pinterest-lookup.md`. If it returns `{ "logged_in": false }`: proceed to Step 3 (WebSearch fallback).

### 2. Get trend data via Playwright

For each term in `pinterest_terms`, navigate directly to:
```
https://trends.pinterest.com/detail/?country=US&terms={url-encoded-term}
```

Take a **screenshot** to read the trend chart. Extract:
- `direction` — shape of the solid line: rising = `growing`, flat = `stable`, falling = `declining`
- `peak_season` — x-axis label at the highest point (e.g. `"January–February"`)

Then take a **snapshot** to extract the related trend chips shown below the chart. Record all visible chip text as `related_topics`.

If a term returns 404 or no chart data: note it and continue to the next term.

If all terms return no data: proceed to Step 3.

### 3. Fallback — WebSearch

Use the current year (from today's date) in place of `{current_year}` when running these queries:

For each term in `pinterest_terms`, run:
1. `Pinterest trending "{term}" {current_year}`
2. `"{term}" Pinterest saves interest trend rising`

Also run one broad query:
3. `what is trending on Pinterest for digital downloads {current_year}`

Synthesize results to identify trending categories and directions. Note `"source": "web_search"`.

If WebSearch returns no useful data: return `{ "source": "unavailable", "raw_seed_candidates": [] }` and stop.

### 4. Classify categories

Group findings into broad categories. For each:
- `direction`: `growing` / `stable` / `declining`
- `signal_strength`: `strong` / `moderate` / `weak`
- `peak_season`: time of year with highest activity
- `notes`: one sentence on why
- `examples`: 2–3 specific keyword examples from the trend

Set top-level `confidence`:
- `high` — Playwright data for most terms with clear directions
- `medium` — Some terms returned Playwright data, or WebSearch fallback used
- `low` — Fewer than half the terms returned meaningful data

---

## Output

Return a JSON object to the calling agent:

```json
{
  "source": "playwright",
  "confidence": "high",
  "trending_categories": [
    {
      "category": "personal finance trackers",
      "examples": ["budget tracker google sheets", "savings challenge tracker", "paycheck budget planner"],
      "direction": "growing",
      "peak_season": "January–February",
      "signal_strength": "strong",
      "notes": "Strong January spike — aligns with New Year financial resolutions"
    },
    {
      "category": "aesthetic notion templates",
      "examples": ["notion dashboard aesthetic", "notion student planner dark mode"],
      "direction": "stable",
      "peak_season": "August–September",
      "signal_strength": "moderate",
      "notes": "Back-to-school drives seasonal interest; stable year-round baseline"
    }
  ],
  "raw_seed_candidates": [
    "budget tracker google sheets",
    "savings challenge tracker",
    "notion dashboard aesthetic",
    "paycheck budget planner"
  ]
}
```

### `source` values
| Value | Meaning |
|---|---|
| `playwright` | Scraped Pinterest Trends directly |
| `web_search` | Synthesized from WebSearch — lower confidence |
| `unavailable` | Both methods failed |

---

## Notes

- Pinterest leads Etsy by 3–6 months. A growing Pinterest category with low Etsy competition is the strongest early-mover signal in the discover pipeline.
- `raw_seed_candidates` should come from `growing` categories only — do not include stable or declining.
- Include `declining` categories in output so seed-ranker can deprioritise matching seeds.

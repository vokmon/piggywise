# pinterest-signals

Identify broad trending categories on Pinterest Trends. Pinterest data typically leads Etsy by 3–6 months — useful for spotting what's coming before it appears in Etsy search volume.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input
- `pinterest_terms` — list of terms to search on Pinterest Trends

## Steps

### 1. Search Pinterest Trends for broad categories

Navigate to `https://trends.pinterest.com/`.

**If a login wall appears:**
1. Check for credentials:
   ```bash
   echo $PINTEREST_EMAIL
   echo $PINTEREST_PASSWORD
   ```
2. If both are set: navigate to `https://www.pinterest.com/login/`, enter the credentials and log in. Then return to `https://trends.pinterest.com/`.
3. If credentials are not set: proceed to Step 2 (WebSearch fallback).

**Once on Pinterest Trends**, search for each term in the `pinterest_terms` list in sequence.

For each search, take a **screenshot** to read the trend chart (direction and peak season). Then take a **snapshot** to extract related topics from the sidebar if present.

Record for each:
- `direction` — growing / stable / declining (from chart shape)
- `peak_season` — time of year with highest activity
- `related_topics` — any adjacent trends listed in the sidebar

If Pinterest Trends shows no data for a term: note it and continue to the next.

If the page is blocked or unavailable for all terms: proceed to Step 2.

### 2. Fallback — WebSearch

Use the current year (from today's date) in place of `{current_year}` when running these queries:

For each term in `pinterest_terms`, run:
1. `Pinterest trending "{term}" {current_year}`
2. `"{term}" Pinterest saves interest trend rising`

Also run one broad query:
3. `what is trending on Pinterest for digital downloads {current_year}`

Synthesize results to identify trending categories and directions. Note `"source": "web_search"`.

If WebSearch returns no useful data: return `{ "source": "unavailable", "raw_seed_candidates": [] }` and stop — the calling agent will continue without Pinterest signals.

### 3. Classify categories

Group findings into broad categories. For each:
- `direction`: `growing` / `stable` / `declining`
- `signal_strength`: `strong` / `moderate` / `weak`
- `peak_season`: time of year with highest activity
- `notes`: one sentence on why
- `examples`: 2–3 specific keyword examples from the trend

Set top-level `confidence`:
- `high` — All terms returned Playwright data with clear directions
- `medium` — Some terms returned data, or WebSearch fallback used
- `low` — Fewer than half the terms returned data, or data was vague

---

## Output

Return a JSON object to the calling agent:

```json
{
  "source": "playwright",
  "confidence": "medium",
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
    },
    {
      "category": "digital planners",
      "examples": ["digital planner goodnotes", "digital planner ipad"],
      "direction": "growing",
      "peak_season": "December–January",
      "signal_strength": "moderate",
      "notes": "Rising interest in app-based planning tools"
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

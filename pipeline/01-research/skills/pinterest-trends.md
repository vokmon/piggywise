# pinterest-trends

Check Pinterest Trends for a keyword to identify early demand signals and adjacent interests. Pinterest trends typically lead Etsy by 3–6 months — useful for spotting what's coming before it gets saturated on Etsy.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.
Follows `skills/pinterest-lookup.md` for Pinterest authentication.

## Input
- `keyword` — keyword to research (e.g. `"budget tracker google sheets"`)

---

## Steps

### 1. Login

Run `skills/pinterest-lookup.md`. If it returns `{ "logged_in": false }`: proceed to Step 3 (WebSearch fallback).

### 2. Get trend data via Playwright

Navigate directly to:
```
https://trends.pinterest.com/detail/?country=US&terms={url-encoded-keyword}
```

Take a **screenshot** to read the trend chart. Extract:
- `trend_direction` — shape of the solid line: rising = `growing`, flat = `stable`, falling = `declining`
- `peak_season` — x-axis label at the highest point (e.g. `"January–February"`)

Then take a **snapshot** to extract the related trend chips shown below the chart. Record all visible chip text as `related_interests`.

If the page returns 404 or shows no chart data: proceed to Step 3.

### 3. Fallback — WebSearch

Use the current year (from today's date) in place of `{current_year}` when running these queries:

1. `Pinterest trending "{keyword}" {current_year}`
2. `Pinterest search trend "{keyword}" growing declining {current_year}`
3. `"{keyword}" Pinterest saves interest trend {current_year}`

Synthesize results to extract `trend_direction`, `peak_season`, and `related_interests`. Note `"source": "web_search"`.

If WebSearch returns no useful data: return `{ "available": false, "source": "unavailable" }` and stop.

---

## Output

**If data available (Playwright):**
```json
{
  "keyword": "budget tracker google sheets",
  "available": true,
  "source": "playwright",
  "trend_direction": "growing",
  "peak_season": "January–February",
  "related_interests": [
    "savings challenge",
    "money saving aesthetic",
    "personal finance"
  ],
  "early_signal_note": "Rising on Pinterest since Oct — likely to peak on Etsy Jan–Feb"
}
```

**If data available (WebSearch fallback):**
```json
{
  "keyword": "budget tracker google sheets",
  "available": true,
  "source": "web_search",
  "trend_direction": "growing",
  "peak_season": "January–February",
  "related_interests": [
    "personal finance",
    "savings tracker"
  ],
  "early_signal_note": "Growing Pinterest interest based on web search synthesis — lower confidence"
}
```

**If no data:**
```json
{
  "keyword": "budget tracker google sheets",
  "available": false,
  "source": "unavailable",
  "note": "No Pinterest Trends data for this keyword — rely on Google Trends only"
}
```

---

## Notes

- Pinterest leads Etsy by 3–6 months. A growing Pinterest trend + medium Etsy competition = strong early opportunity.
- `related_interests` are worth passing to `gap-finder` as adjacent niche ideas even when the main keyword has low Etsy competition.
- Always run this skill. If no Pinterest data exists for the niche, the skill returns `available: false` and the pipeline continues without Pinterest data.

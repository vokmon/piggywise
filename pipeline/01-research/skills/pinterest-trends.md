# pinterest-trends

Check Pinterest Trends for a keyword to identify early demand signals and adjacent interests. Pinterest trends typically lead Etsy by 3–6 months — useful for spotting what's coming before it gets saturated on Etsy.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input
- `keyword` — keyword to research (e.g. `"budget tracker google sheets"`)

---

## Steps

### 1. Search Pinterest Trends

Navigate to `https://trends.pinterest.com/`.

**If a login wall appears:**
1. Check for credentials:
   ```bash
   echo $PINTEREST_EMAIL
   echo $PINTEREST_PASSWORD
   ```
2. If both are set: navigate to `https://www.pinterest.com/login/`, enter the credentials and log in. Then return to `https://trends.pinterest.com/` and search for the keyword.
3. If credentials are not set: proceed to Step 2 (WebSearch fallback).

**Once on Pinterest Trends**, search for the keyword.

Take a **screenshot** to read the trend chart — extract the curve shape (up / flat / down) and identify the spike season from the x-axis. Then take a **snapshot** to extract related interests from the sidebar list if present.

Extract:
- `trend_direction` — growing / stable / declining (read from chart shape)
- `peak_season` — time of year when saves/searches spike (read from chart x-axis)
- `related_interests` — Pinterest's suggested related topics (signals adjacent demand worth exploring)

If Pinterest Trends shows no data for the keyword, or the page is unavailable: proceed to Step 2.

### 2. Fallback — WebSearch

Use the current year (from today's date) in place of `{current_year}` when running these queries:

1. `Pinterest trending "{keyword}" {current_year}`
2. `Pinterest search trend "{keyword}" growing declining {current_year}`
3. `"{keyword}" Pinterest saves interest trend {current_year}`

Synthesize results to extract trend direction, peak season, and related interests. Note `"source": "web_search"`.

If WebSearch returns no useful data: return `{ "available": false, "source": "unavailable" }` and stop — the calling agent will continue without Pinterest data.

---

## Output

Return a JSON object to the calling agent:

**If data available (Playwright):**
```json
{
  "keyword": "budget tracker google sheets",
  "available": true,
  "source": "playwright",
  "trend_direction": "growing",
  "peak_season": "January–February",
  "related_interests": [
    "personal finance",
    "savings challenge",
    "financial planner"
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
- Always run this skill. If no Pinterest data exists for the niche (e.g. highly technical tools), the skill returns `available: false` and the pipeline continues without Pinterest data.

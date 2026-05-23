# pinterest-trends

Check Pinterest Trends for a keyword to identify early demand signals and adjacent interests. Pinterest trends typically lead Etsy by 3–6 months — useful for spotting what's coming before it gets saturated on Etsy.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input
- `keyword` — same keyword used in etsy-scan (e.g. `"budget tracker google sheets"`)

---

## Steps

### 1. Search Pinterest Trends
Navigate to `https://trends.pinterest.com/` and search for the keyword.

Take a **screenshot** to read the trend chart — extract the curve shape (up / flat / down) and identify the spike season from the x-axis. Then take a **snapshot** to extract related interests from the sidebar list if present.

Extract:
- `trend_direction` — growing / stable / declining (read from chart shape)
- `peak_season` — time of year when saves/searches spike (read from chart x-axis)
- `related_interests` — Pinterest's suggested related topics (signals adjacent demand worth exploring)

### 2. Check data availability
Pinterest Trends does not cover every niche. If no meaningful data is found:
- Set `available: false`
- Note it and return — do not guess or fill with assumptions

---

## Output

Return a JSON object to the calling agent (`research-agent`):

**If data available:**
```json
{
  "keyword": "budget tracker google sheets",
  "available": true,
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

**If no data:**
```json
{
  "keyword": "budget tracker google sheets",
  "available": false,
  "note": "No Pinterest Trends data for this keyword — rely on Google Trends only"
}
```

---

## Notes

- Pinterest leads Etsy by 3–6 months. A growing Pinterest trend + medium Etsy competition = strong early opportunity.
- `related_interests` are worth passing to `gap-finder` as adjacent niche ideas even when the main keyword has low Etsy competition.
- Always run this skill. If no Pinterest data exists for the niche (e.g. highly technical tools), the skill returns `available: false` and the pipeline continues without Pinterest data.

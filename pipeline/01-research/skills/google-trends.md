# google-trends

Check search trend momentum, seasonality, and keyword variants for a topic. Uses Gemini CLI as primary (Google Search grounding), with Playwright and WebSearch as fallbacks.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input
- `keyword` — same keyword used in etsy-scan (e.g. `"budget tracker google sheets"`)
- `related_keywords` — autocomplete suggestions from etsy-scan output

---

## Steps

### 1. Try Gemini CLI (primary)

Run via Bash:

```bash
gemini -p "Using Google Search, research the search trend for '{keyword}' worldwide over the last 12 months. Tell me: (1) is interest growing, flat, or declining? (2) which months have the highest search interest? (3) what is the current interest level on a scale of 0–100, and what is the approximate average level over the last 12 months? (4) what are the top rising related searches marked as Breakout or fast-growing? (5) what are the consistently high-volume related searches? Be specific and data-driven."
```

**Evaluate the response — does it contain ALL of the following?**
- A clear direction (growing / flat / declining)
- Specific month names for peak interest
- At least 2 rising queries with context
- At least 2 top queries

→ If yes: use the output, skip to Step 4
→ If no (vague, generic, or "I don't have real-time data"): proceed to Step 2

### 2. Fallback — Playwright on Google Trends

Navigate to:
`https://trends.google.com/trends/explore?q={keyword}&date=today%2012-m`

Take a **screenshot** to read the interest-over-time chart — extract the curve shape (up / flat / down) and identify spike months from the x-axis labels. Then take a **snapshot** to extract the **Related queries** section — copy all "Rising" and "Top" queries listed.

If the page fails to load: proceed to Step 3.

### 3. Fallback — WebSearch

Use the WebSearch tool with these queries in sequence:
1. `"{keyword}" search trend last 12 months`
2. `"{keyword}" google trends rising searches`
3. `best time of year to sell "{keyword}"`

Synthesize the results to extract trend direction, peak months, and related queries. Note `"source": "web_search"` in the output to flag lower confidence.

### 4. Keyword comparison

Using whichever source succeeded above, run a comparison of the top 3 terms from the `related_keywords` input against the main keyword:

- **If Gemini**: run a second prompt:
```bash
gemini -p "Using Google Search, compare worldwide search interest for these keywords over the last 12 months: '{kw1}', '{kw2}', '{kw3}', '{keyword}'. Which has the highest and most consistent interest? Which is best to use as an Etsy product title keyword? Be brief."
```

- **If Playwright**: navigate to the comparison URL:
`https://trends.google.com/trends/explore?q={kw1},{kw2},{kw3},{keyword}&date=today%2012-m`

- **If WebSearch**: ask which keyword variant has the most search results and articles.

### 5. Classify seasonality
Based on collected data:
- `evergreen` — consistent interest year-round, no major dips
- `seasonal` — clear spikes with notable off-season dips
- `emerging` — upward trend, rising queries, not yet saturated

Set `best_launch_window` as a human-readable string: 1–2 months before the peak month (e.g. `"November–December (ahead of January peak)"`).

---

## Output

Return a JSON object to the calling agent (`research-agent`):

```json
{
  "keyword": "budget tracker google sheets",
  "source": "gemini",
  "confidence": "high",
  "trend_direction": "growing",
  "current_score": 72,
  "avg_score": 58,
  "peak_months": ["January", "September"],
  "rising_queries": [
    "aesthetic budget tracker google sheets",
    "zero-based budget template google sheets"
  ],
  "top_queries": [
    "google sheets budget template",
    "monthly budget planner google sheets"
  ],
  "keyword_comparison": {
    "winner": "monthly budget tracker google sheets",
    "reason": "Highest consistent score across 12 months, strong Jan peak"
  },
  "seasonality": "seasonal",
  "best_launch_window": "November–December (ahead of January peak)"
}
```

### `source` values
| Value | Meaning |
|---|---|
| `gemini` | Gemini CLI with Search grounding — highest confidence |
| `playwright` | Scraped Google Trends UI directly |
| `web_search` | Synthesized from WebSearch results — lower confidence |
| `unavailable` | All three methods failed — no trend data |

### `confidence` values
| Value | Meaning |
|---|---|
| `high` | Specific data with months, scores, and queries |
| `medium` | Partial data — direction and months but no scores |
| `low` | Vague or inferred — direction only |

---

## Notes

- Always attempt Gemini first — it's the fastest and requires no browser.
- Do not fabricate scores — if a number is unavailable, omit the field rather than guessing.
- If all three methods fail, set `"source": "unavailable"` and return — the research-agent will proceed without trend data rather than block the pipeline.

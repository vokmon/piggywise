# autocomplete-harvest

Collect Etsy search autocomplete suggestions to reveal exactly what buyers are typing. Etsy autocomplete reflects real search behaviour — every suggestion is a query real buyers have entered.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

Uses two types of terms: fixed format anchors (always run) + dynamic topic terms derived from etsy-bestsellers output (adaptive — follows what buyers are already engaging with, not assumptions).

## Input
- `etsy_bestsellers` — output from etsy-bestsellers skill (provides dynamic topic terms)

---

## Steps

### 1. Build the query list

**Fixed format anchors** — always run these, no matter what:
- `google sheets`
- `notion template`
- `digital download`
- `spreadsheet template`

**Dynamic topic terms** — derived from `etsy_bestsellers` output:
- Take the top 5 keys from `etsy_bestsellers.topic_themes` (by count)
- Take the top 3 keys from `etsy_bestsellers.product_types` (by count)
- Replace underscores with spaces in each key before using as a search term (e.g. `google_sheets` → `google sheets`, `notion_template` → `notion template`)
- Skip the `other` key
- Skip any dynamic term that duplicates a fixed anchor after transformation (e.g. `google_sheets` → `google sheets` is already a fixed anchor — skip it)
- Use the remaining terms as additional autocomplete queries

Example: if etsy-bestsellers found `topic_themes: { finance: 18, productivity: 12, business: 9, health: 7 }` and `product_types: { tracker: 8, planner: 11 }`, the dynamic terms become:
`finance`, `productivity`, `business`, `health`, `planner`, `tracker`

If `etsy_bestsellers` is null or blocked: use only the fixed anchors.

Final query list = 4 fixed anchors + up to 8 dynamic terms = up to 12 queries total.

### 2. Trigger autocomplete for each term

For each term in the query list, navigate to:
`https://www.etsy.com/search?q={term}&explicit=1`

Take a snapshot immediately after the page loads — autocomplete suggestions appear in the search bar dropdown before results render.

Extract all suggestions shown (typically 6–10 per term).

If suggestions are not visible in the snapshot: try clicking the search bar element and taking a second snapshot. If still nothing: skip this term and continue.

### 3. Deduplicate and clean

- Deduplicate across all terms
- Remove suggestions that are clearly physical products (e.g. "planner notebook spiral bound", "printable wall art")
- Remove non-English suggestions
- Merge near-duplicates — keep the more specific phrasing (e.g. "google sheets budget tracker" beats "budget tracker")
- Lowercase all suggestions

### 4. Group by dominant keyword

Organize surviving suggestions into groups based on what the buyer is looking for — not the format:
- `finance` — budget, expense, savings, income, invoice
- `productivity` — habit, schedule, to-do, goal, task
- `business` — client, project, freelance, social media, content
- `health` — meal, fitness, wellness, symptom
- `personal` — wedding, travel, home, reading
- `format_only` — suggestions that are just format terms with no topic (e.g. "notion template", "google sheets template")

---

## Output

Return a JSON object to the calling agent (`discover-agent`):

```json
{
  "terms_queried": 10,
  "anchors_used": ["google sheets", "notion template", "digital download", "spreadsheet template"],
  "dynamic_terms_used": ["finance", "productivity", "business", "health", "planner", "tracker"],
  "total_suggestions_collected": 74,
  "deduplicated_count": 51,
  "by_group": {
    "finance": [
      "budget tracker google sheets",
      "expense tracker google sheets",
      "savings goal tracker notion",
      "invoice template google sheets freelancer",
      "income tracker self employed"
    ],
    "productivity": [
      "habit tracker notion template",
      "daily planner google sheets",
      "goal tracker spreadsheet"
    ],
    "business": [
      "client tracker google sheets",
      "social media content calendar notion",
      "freelance project tracker spreadsheet"
    ],
    "health": [
      "meal planner google sheets",
      "symptom tracker google sheets"
    ],
    "personal": [
      "wedding budget tracker google sheets",
      "reading tracker notion"
    ],
    "format_only": [
      "google sheets template bundle",
      "notion template aesthetic"
    ]
  },
  "raw_seed_candidates": [
    "budget tracker google sheets",
    "invoice template google sheets freelancer",
    "habit tracker notion template",
    "client tracker google sheets",
    "social media content calendar notion"
  ]
}
```

---

## Notes

- `raw_seed_candidates` should be the most specific and actionable suggestions — exclude vague format-only terms like "notion template" or "digital download".
- Dynamic terms make this skill adaptive: if Etsy bestsellers show fitness content rising, the autocomplete harvest will pick up fitness-related queries automatically.
- If Etsy blocks across all terms: return `{ "source": "blocked", "raw_seed_candidates": [] }` — discover-agent continues with data from other skills.

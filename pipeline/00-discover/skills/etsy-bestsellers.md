# etsy-bestsellers

Scrape Etsy search results to extract bestselling digital product types, themes, and categories. Uses Etsy's own filter chips as the discovery guide — these are dynamically generated from real buyer behaviour, not our assumptions.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Steps

### 1. Start with a broad search

Navigate to `https://www.etsy.com`, type `digital download` in the search box and press Enter.

Take a **snapshot** to extract the filter chips — they appear in the DOM. Then take a **screenshot** to extract listing tiles — tiles render via JavaScript and may not appear in the accessibility tree.

Extract:

- From snapshot: the **filter chips** shown below the search bar — these are Etsy's signal of what buyers actually filter by (e.g. `Planner`, `Tracker`, `Business`, `Calendar`, `Habit Tracking`). Collect all visible chips.
- From screenshot: up to 20 listings: title, price, star rating, review count, badges (`Bestseller`, `Star Seller`, `Popular now`), shop name.

If Etsy blocks or shows a captcha: note `"source": "blocked"` and stop — do not continue.

### 2. Expand using Etsy's filter chips

From the filter chips collected in Step 1, pick the top 4–5 that suggest a product category (skip chips like `Ships from TH`, `Under THB 1,500`, `Customizable` — these are attributes, not categories).

For each selected chip, navigate to `https://www.etsy.com`, type `digital download {chip}` in the search box and press Enter.

Take a screenshot and extract up to 20 listings per chip using the same fields.

### 3. Demand recency check

For the top 10 listings by review count across all searches, click through to the listing page. Take a **snapshot** to extract DOM-accessible fields. If `in_carts` is not visible in the snapshot, take a **screenshot** to locate it visually.

Check:

- `last_review_date` — date of the most recent visible review
- `listing_published` — "Listed on..." or "Last updated..." on the listing page
- `in_carts` — "X people have this in their carts" if shown

Classify each:

- `active` — last review within 3 months
- `slowing` — last review 3–6 months ago
- `stale` — last review more than 6 months ago

A stale listing with high reviews means that specific product is losing momentum — but check other listings in the same category before concluding the category is dead. If other listings in the same category are `active`, the category is healthy and the aging product is an opening for a fresher competitor.

Prioritise `active` listings when identifying `raw_seed_candidates`.

### 4. Extract patterns

From all collected listings, identify:

**Product types** — group titles by format keyword:

- `google_sheets` / `spreadsheet` / `excel`
- `notion_template` / `notion_dashboard`
- `planner` / `journal` / `worksheet`
- `tracker` / `log` / `dashboard`
- `resume` / `cv` / `portfolio`
- `bundle` / `kit` / `pack`
- `other`

**Topic themes** — group by subject matter:

- `finance` (budget, savings, expense, income)
- `business` (invoice, client tracker, project management)
- `health` (habit tracker, meal plan, fitness)
- `productivity` (to-do, schedule, calendar, goal setting)
- `creative` (social media, content calendar, editorial)
- `personal` (wedding, travel, home)
- `other`

**Price bands** (use relative labels — prices shown in local currency):

- `low` / `mid` / `high` / `premium` — judge relative to the range of prices seen across all listings collected

---

## Output

Return a JSON object to the calling agent:

```json
{
  "source": "playwright",
  "chips_found": [
    "Planner",
    "Tracker",
    "Business",
    "Calendar",
    "Habit Tracking",
    "Savings"
  ],
  "chips_used_for_expansion": ["Planner", "Tracker", "Business", "Calendar"],
  "listings_collected": 98,
  "product_types": {
    "google_sheets": 22,
    "notion_template": 14,
    "planner": 18,
    "tracker": 16,
    "bundle": 10,
    "other": 18
  },
  "topic_themes": {
    "finance": 24,
    "productivity": 18,
    "business": 14,
    "health": 12,
    "creative": 8,
    "personal": 6,
    "other": 16
  },
  "price_bands": {
    "low": 10,
    "mid": 38,
    "high": 32,
    "premium": 18
  },
  "top_listings": [
    {
      "title": "Monthly Budget Tracker Google Sheets Template",
      "price": 7.99,
      "reviews": 1840,
      "star_rating": 4.9,
      "is_bestseller": true,
      "is_star_seller": true,
      "is_popular_now": false,
      "in_carts": 12,
      "last_review_date": "2026-04-12",
      "listing_published": "2023-06-15",
      "demand_recency": "active",
      "shop": "FinanceWithGrace"
    }
  ],
  "raw_seed_candidates": [
    "budget tracker google sheets",
    "notion habit tracker",
    "freelance invoice template",
    "social media content calendar"
  ]
}
```

---

## Notes

- `raw_seed_candidates` are drawn from the most frequent title patterns among `active` listings only.
- If all chip expansions are blocked, return what was collected in Step 1 only and set `"source": "partial"` — partial data is still useful. seed-ranker will weight it accordingly.

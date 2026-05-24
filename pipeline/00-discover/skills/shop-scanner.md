# shop-scanner

Study top-performing Etsy shops in the digital templates / spreadsheets niche. Goal: learn what successful sellers have figured out — what product types they focus on, which listings get the most traction, and what price points work.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input

- `etsy_bestsellers` — output from etsy-bestsellers skill (provides top product types to search)

---

## Steps

### 1. Find top shops

If `etsy_bestsellers` is null or blocked: return `{ "source": "blocked", "raw_seed_candidates": [] }` — there are no product types to search from.

Take the top 3 product types from `etsy_bestsellers.product_types` (by count), excluding the `other` key. Replace underscores with spaces in the key before using it in the URL (e.g. `google_sheets` → `google sheets`):
`https://www.etsy.com/search?q={product_type}&explicit=1&sort_order=most_relevant`

Take a **screenshot** per search — listing tiles may not appear in the accessibility tree.

From the listings returned, collect unique shop names. Target shops that appear 2+ times or have Star Seller / Bestseller badges.

Aim for 5–8 unique shops to study.

### 2. Visit each shop

For each shop, navigate to their shop page:
`https://www.etsy.com/shop/{shop-name}`

Extract:

- Total shop sales count
- Number of listings
- Shop join date (shown as "Member since..." on the shop page) — used to calculate velocity
- Shop-level star rating (visible on shop page)
- Top 3–5 listings (by position or Star Seller / bestseller badge): title, price, review count, star rating, last review date, `in_carts` count if shown (click through to listing — take a **snapshot** first; if `in_carts` is not visible, take a **screenshot**)
- Any visible niche focus (e.g. "finance templates", "Notion dashboards")

Classify `demand_recency` for each listing based on `last_review_date`:

- `active` — last review within 3 months
- `slowing` — last review 3–6 months ago
- `stale` — last review more than 6 months ago

If a shop page is blocked or unavailable: note it and move to the next — do not retry.

**Calculate monthly sales velocity** for each shop:
`velocity = total_sales ÷ months_since_joining`

Classify each shop:

- `growing` — high velocity (> 200 sales/month) regardless of total sales
- `established` — moderate velocity (50–200 sales/month), steady performer
- `legacy` — low velocity (< 50 sales/month) but high total sales — accumulated over years, not a current trend signal

### 3. Identify patterns

From all shops studied, extract:

- Which product types appear most in top listings
- Which topics (finance, productivity, business, etc.) dominate
- Price range of their bestsellers
- Any product sub-niches that appear in multiple shops (signal of proven demand)

When building `raw_seed_candidates`: include patterns from `growing` and `established` shops. Include patterns from `legacy` shops only if they also appear in at least one `growing`/`established` shop.

---

## Output

Return a JSON object to the calling agent:

```json
{
  "source": "playwright",
  "shops_studied": 6,
  "shops": [
    {
      "name": "FinanceWithGrace",
      "total_sales": 12400,
      "listing_count": 34,
      "joined": "2023-03",
      "months_active": 26,
      "monthly_sales_velocity": 477,
      "velocity_signal": "growing",
      "top_listings": [
        {
          "title": "Monthly Budget Tracker Google Sheets",
          "price": 7.99,
          "reviews": 1840,
          "star_rating": 4.9,
          "in_carts": 14,
          "last_review_date": "2026-04-20",
          "demand_recency": "active"
        },
        {
          "title": "Savings Goal Tracker Google Sheets",
          "price": 5.99,
          "reviews": 920,
          "star_rating": 4.8,
          "in_carts": 3,
          "last_review_date": "2026-03-15",
          "demand_recency": "active"
        }
      ],
      "shop_star_rating": 4.9,
      "niche_focus": "personal finance spreadsheets"
    }
  ],
  "cross_shop_patterns": [
    "budget trackers appear in 5 of 6 shops studied",
    "notion habit trackers appear in 3 shops",
    "freelance invoice templates appear in 3 shops"
  ],
  "raw_seed_candidates": [
    "budget tracker google sheets",
    "savings goal tracker",
    "notion habit tracker",
    "freelance invoice template google sheets"
  ]
}
```

---

## Notes

- Do not study more than 8 shops — diminishing returns beyond that at the discover stage.
- If fewer than 3 shops were reachable, set `"source": "partial"` in the output — seed-ranker will weight this input accordingly.
- `cross_shop_patterns` are the most valuable output: if multiple successful shops sell the same product type, that's a proven category worth researching.
- When flagging cross-shop patterns, note whether they appear in `growing`/`established` shops — patterns seen only in `legacy` shops may reflect past demand, not current.
- `raw_seed_candidates` feed directly into `seed-ranker`.

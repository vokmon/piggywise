# etsy-scan

Scan Etsy search results for a keyword to extract demand signals, pricing patterns, competition level, and buyer language. Uses Playwright to browse Etsy directly.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input

- `keyword` — search term to scan (e.g. `"budget tracker google sheets"`)
- `max_listings` — how many top listings to analyze

---

## Steps

### 1. Capture autocomplete suggestions

Navigate to `https://www.etsy.com`, click the search box, type `{keyword}` slowly (character by character), and take a **snapshot before pressing Enter** — autocomplete suggestions appear in the search bar dropdown while typing. These are real buyer search terms — record all of them. After recording, press Enter to submit.

If suggestions are not visible in the snapshot: take a second snapshot with the search box focused. If still nothing: skip autocomplete and continue to Step 2.

If Etsy blocks with a bot/CAPTCHA screen, note it and continue to step 2 anyway — partial data is still useful.

### 2. Scrape search results page

Take a **screenshot** of the search results page — listing tiles may not appear in the accessibility tree. Extract for each visible listing (up to `max_listings`):

- `title` — full listing title
- `price` — current price (use sale price if active)
- `original_price` — original price if on sale (to infer discount strategy)
- `reviews` — review count
- `star_rating` — rating score (e.g. 4.9) — visible on listing tile
- `is_bestseller` — true if Bestseller badge is present
- `is_star_seller` — true if Star Seller badge is present
- `shop_name` — seller shop name
- `listing_url` — full URL

Also record:

- `total_results` — the "X results" count shown at top of page (competition signal)

### 3. Deep-dive top 3

Prioritise listings flagged `is_star_seller: true` first, then `is_bestseller: true`. If neither exists: pick the top 3 by review count. Pick up to 3 total. Navigate to each listing page. Take a **snapshot** to extract DOM-accessible metadata. If `favorites_count` or `in_carts` are not visible in the snapshot, take a **screenshot** to locate them visually.

Extract:

- `tags` — all 13 tags (found in page source or visible tag chips)
- `description_opening` — first 2 sentences of the description (buyer language + SEO keywords)
- `whats_included` — bullet list of what's included in the product
- `favorites_count` — number of people who favorited the listing
- `in_carts` — "X people have this in their carts" if shown — real-time buyer intent signal
- `shop_total_sales` — total sales shown on the shop profile section
- `shop_star_rating` — shop-level star rating visible on the listing page
- `last_review_date` — date of the most recent visible review
- `listing_published` — when the listing was first published or last updated (shown as "Listed on..." or "Last updated..." on the listing page)

**Calculate review velocity:**
`review_velocity = reviews ÷ months_since_published` (estimated months since `listing_published`)

Classify demand recency:

- `active` — last review within 3 months
- `slowing` — last review 3–6 months ago
- `stale` — last review more than 6 months ago

Use `demand_recency` at the listing level to spot aging products. Use `demand_recency_summary` across the 3 deep-dives to judge whether the category itself is healthy:

- `demand_recency_summary: hot` with one `stale` listing → the dominant product is aging but the category is still active. A fresher product has room to take its place.
- `demand_recency_summary: declining` → the whole category may be fading. Flag it — google-trends will confirm.

### 4. Infer signals

From the collected data, calculate:

- `price_min`, `price_max`, `price_median` — pricing range across all listings
- `bestseller_ratio` — % of top listings with Bestseller badge (high = competitive but proven)
- `star_seller_ratio` — % of top listings with Star Seller badge (better current health signal)
- `top_tags` — most frequently appearing tags across the 3 deep-dives
- `competition_level` — based on `total_results`:
  - `< 500` → low
  - `500–5000` → medium
  - `> 5000` → high
- `demand_recency_summary` — based on deep-dive listings:
  - `hot` — 2+ of top 3 listings are `active`
  - `declining` — 2+ of top 3 listings are `stale`
  - `mixed` — everything else (e.g. all slowing, or one active + one stale)

---

## Output

Return a JSON object in this structure — do not save to file, return it to the calling agent to merge into the final output. `top_listings` contains the up to 3 deep-dived listings from Step 3 with full field data. `bestseller_ratio` and `star_seller_ratio` are computed across all listings scanned in Step 2. `demand_recency_summary` is computed from the 3 deep-dived listings in Step 3.

```json
{
  "keyword": "budget tracker google sheets",
  "total_results": 3200,
  "competition_level": "medium",
  "price_min": 3.5,
  "price_max": 18.0,
  "price_median": 9.0,
  "bestseller_ratio": 0.35,
  "star_seller_ratio": 0.25,
  "demand_recency_summary": "hot",
  "autocomplete_suggestions": [
    "budget tracker google sheets template",
    "budget tracker google sheets free",
    "monthly budget tracker google sheets"
  ],
  "top_tags": [
    "budget template",
    "google sheets budget",
    "monthly budget planner",
    "expense tracker",
    "personal finance"
  ],
  "top_listings": [
    {
      "title": "Monthly Budget Tracker Google Sheets Template, Personal Finance Planner, Expense Tracker, Paycheck Budget",
      "price": 8.5,
      "original_price": 12.0,
      "reviews": 1842,
      "star_rating": 4.9,
      "is_bestseller": true,
      "is_star_seller": true,
      "shop_name": "ExampleShop",
      "listing_url": "https://www.etsy.com/listing/...",
      "tags": ["budget template", "google sheets", "monthly budget"],
      "description_opening": "Take control of your finances with this easy-to-use budget tracker. No accounting experience needed — just input your income and expenses.",
      "whats_included": [
        "1 Google Sheets template",
        "Setup guide",
        "Video walkthrough"
      ],
      "favorites_count": 4200,
      "in_carts": 8,
      "shop_total_sales": 28000,
      "shop_star_rating": 4.9,
      "last_review_date": "2026-04-18",
      "listing_published": "2023-09-01",
      "review_velocity": 57.6,
      "demand_recency": "active"
    }
  ]
}
```

---

## Notes

- Star Seller requires strong performance in the last 3 months; Bestseller is based on lifetime sales. Prioritise Star Seller for current demand signal.

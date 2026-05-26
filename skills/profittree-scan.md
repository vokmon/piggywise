# profittree-scan

Login to ProfitTree and search Product Finder for a keyword to extract niche-level market signals: niche score, monthly revenue, related keywords, top products, and top competing shops.

## What ProfitTree Product Finder provides

ProfitTree (https://profittree.io) is an Etsy product research tool. Product Finder searches all Etsy listings for a keyword and aggregates:

- **Niche Score** (0–100) — composite demand/opportunity signal. ≥ 80 is strong; ≥ 90 is high-demand.
- **Monthly Revenue** — estimated total monthly revenue across all Etsy listings for the keyword
- **Top Related Keywords** — 5 buyer-driven adjacent search terms (may vary between sessions)
- **Products table** — listings ranked by monthly sales. Default visible columns: Product, Price, Mo. Sales, Mo. Revenue, Total Revenue. Additional columns available via the Columns button: Demand, Views, Tags, Listing Age, Conv. Rate, Visibility Score, Avg. Rating, Total Reviews, Favorites, Shop Total Sales, Shop Age. Free tier: full metrics for top ~4 products; all remaining rows show product name + "View on Etsy" link only (metrics blurred).
- **Shops tab** — top competing shops with Total Revenue, Mo. Revenue, Total Sales, Mo. Sales
- **"View on Etsy" links** — every product row (blurred or not) links to the live Etsy listing — use to study competitor descriptions, tags, reviews, and pricing strategy
- **Pagination** — 25 results per page; total result count shown (e.g. "6,982 results")

---

## Input

- `keyword` — search term to research (e.g. `"notion planner"`)

---

## Steps

### 1. Login

Read `PROFIT_TREE_EMAIL` and `PROFIT_TREE_PASSWORD` from `.env`.

- If either is not set: return `{ "status": "no_credentials" }` and stop. Tell the caller to set both vars in `.env` before continuing.
- If both are set: navigate to `https://app.profittree.io`.
  - If already logged in (app loads directly, no redirect): proceed to Step 2.
  - If redirected to `https://login.profittree.io/u/login`: fill in email, fill in password, click the "Continue" button (not "Continue with Google"). Wait for redirect back to `https://app.profittree.io`.

### 2. Search

Navigate to `https://app.profittree.io/product-finder`.

Type `keyword` into the search input and press Enter. Wait until the results page loads and the Niche Score is visible before continuing.

### 3. Extract niche summary

Take a **screenshot** to capture the full results view.

Extract:
- `niche_score` — integer (e.g. `96`)
- `monthly_revenue_estimate` — string as displayed (e.g. `"$59K"`)
- `related_keywords` — all 5 chip labels under "Top Related Keywords"
- `total_results` — the result count from the pagination area (e.g. `6982`)

### 4. Extract Products tab

The Products tab is active by default. Take a **full-page screenshot** — blurred metric cells are not reliably captured in snapshots.

Extract from visible rows:
- **Top products (full data)** — the top ~4 rows where metrics are visible: `name`, `price`, `monthly_sales`, `monthly_revenue`, `total_revenue`
- **All product names** — product name for every visible row on the page (all 25 rows show names even when metrics are blurred)

### 5. Extract Shops tab

Click the **Shops** tab button (next to the Products tab).

Take a **screenshot**.

Extract all visible shop rows:
- `name`, `total_revenue`, `monthly_revenue`, `total_sales`, `monthly_sales`

### 6. (Optional) Study competitor listings

For any product of interest, click its **"View on Etsy"** link (accessible on all rows, including blurred ones). Study the live Etsy listing for: full title, description, tags, pricing strategy, what's included, reviews, and buyer language. Use this when you need to understand a specific competitor in depth.

---

## Output

Return a JSON object to the caller. Do not save to file.

```json
{
  "keyword": "notion planner",
  "status": "ok",
  "niche_score": 96,
  "monthly_revenue_estimate": "$59K",
  "total_results": 6982,
  "related_keywords": [
    "expense tracker",
    "content calendar",
    "budget tracker",
    "finance tracker",
    "second brain"
  ],
  "top_products": [
    {
      "name": "200+ Notion Templates Bundle | Life Planner, Finance, Productivity (PLR & MRR Rights)",
      "price": "$5.65",
      "monthly_sales": 67,
      "monthly_revenue": "$378.55",
      "total_revenue": "$1,553.75"
    },
    {
      "name": "Notion Wedding Planner Template | Not Teach Heavy, Actually Functional and Simple",
      "price": "$33.00",
      "monthly_sales": 60,
      "monthly_revenue": "$1,980.00",
      "total_revenue": "$2,706.00"
    }
  ],
  "all_product_names": [
    "200+ Notion Templates Bundle...",
    "Notion Wedding Planner...",
    "2026 Notion Life Planner...",
    "Notion Life & Business Planner...",
    "Notion Business and Social...",
    "2026 Life Planner - Notion..."
  ],
  "top_shops": [
    {
      "name": "Digicarft",
      "total_revenue": "$1,301,683.50",
      "monthly_revenue": "$26,498.05",
      "total_sales": 127034,
      "monthly_sales": 2580
    },
    {
      "name": "PandArtistDesigns",
      "total_revenue": "$322,206.91",
      "monthly_revenue": "$14,657.63",
      "total_sales": 54340,
      "monthly_sales": 2470
    }
  ],
  "free_tier_note": "Full metrics visible for top ~4 products only. All product names and 'View on Etsy' links accessible on all rows."
}
```

If credentials are missing:

```json
{ "status": "no_credentials" }
```

---

## Notes

- Env var names use underscores: `PROFIT_TREE_EMAIL` and `PROFIT_TREE_PASSWORD` (not `PROFITTREE_EMAIL`).
- ProfitTree uses Auth0. Email and password are on the same form; one "Continue" button submits both. Never use "Continue with Google".
- If already logged in (session still active), the app loads directly — treat this as a successful login.
- `niche_score` and `monthly_revenue_estimate` are niche-level aggregates, not per-product figures.
- `related_keywords` may vary slightly between sessions — they reflect recent buyer search behaviour.
- `top_shops` reveals the biggest revenue earners in this niche — cross-reference on Etsy to study their catalogue.
- For deeper per-listing research (tags, description, reviews), use the "View on Etsy" links and follow up with `pipeline/01-research/skills/etsy-scan.md`.

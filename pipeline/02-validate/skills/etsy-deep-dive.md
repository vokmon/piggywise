# etsy-deep-dive

Search Etsy for the specific product idea (not the broad seed) to confirm whether a direct competitor already fills the gap, and to identify the exact title keyword buyers use when searching for this specific angle.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input

- `product_idea` — the specific product concept to validate (e.g. `"minimal ADHD notion planner"`)
- `seed_keyword` — the original seed from 01-research (`seed`)
- `research_top_listings` — `etsy_scan.top_listings` array from 01-research
- `research_competition_level` — `etsy_scan.competition_level` from 01-research (`"low"`, `"medium"`, or `"high"`)
- `max_listings` — how many listings to extract per search query (passed from validate-agent)

---

## Steps

### 1. Build search queries

Derive 2 targeted search queries from `product_idea`:
- One using the core differentiator angle (e.g. `"minimalist ADHD notion template"`)
- One using buyer language (e.g. `"simple ADHD notion planner"`)

These should be more specific than `seed_keyword` — you're looking for direct competitors to the idea, not the broad category.

### 2. Search Etsy for each query

For each query, navigate to `https://www.etsy.com`, type `{query}` in the search box and press Enter. Take a **screenshot** to read the results. For each query record:
- `total_results` — the X results count shown
- `listings` — up to `max_listings` listings: title, price, reviews, star_rating, is_bestseller, is_star_seller, shop_name

**Interpreting total_results relative to research context:**

Use `research_competition_level` to set expectations:

| research_competition_level | Specific angle total_results | Interpretation |
|---|---|---|
| `high` | < 10% of seed results | Gap confirmed — the specific angle is uncrowded within a large category |
| `medium` | < 20% of seed results | Gap likely — room to enter with differentiation |
| `low` | Any results | Note that even the seed is uncrowded; specific angle adds further clarity |

The seed's result count is in `etsy_scan.total_results` — use that as the baseline for comparison, not an absolute number. If the value is a string like `"1,000+"` or `"1000+"`, parse out the numeric part (e.g. `1000`) before dividing. Treat `"1,000+"` as `1000` for the comparison — it's a lower bound, so the gap estimate is conservative.

### 3. Identify direct competitors

A listing is a **direct competitor** if it matches the product idea's core differentiator — not just the seed category. For example:
- Seed: "ADHD planner notion template" — many results
- Idea: "minimalist ADHD notion template" — a direct competitor must be explicitly minimalist/simple, not just another all-in-one

Check against `research_top_listings` first — if a top listing from research already matches the specific angle, it is a direct competitor.

A direct competitor is **dominant** if it has: Star Seller status AND reviews ≥ the median review count of `research_top_listings`. Dominant competitors block the gap.

Flag any direct competitors found. If none: note as gap confirmed.

### 4. Check autocomplete for the specific angle

Navigate to `https://www.etsy.com`, click the search box, type `{main keywords from product_idea}` slowly (character by character), and take a **snapshot before pressing Enter** to capture autocomplete suggestions. Record any suggestions — these are real buyer search terms and confirm search demand for the specific angle.

### 5. Identify the best title keyword

From the autocomplete suggestions and search query results, recommend the single best keyword to lead the Etsy listing title with. This should be:
- The most specific term that still has search volume
- What buyers type when they want THIS product (not just the broad seed)

---

## Output

```json
{
  "product_idea": "minimal ADHD notion planner",
  "seed_keyword": "ADHD planner notion template",
  "search_queries_used": [
    "minimalist ADHD notion template",
    "simple ADHD notion planner"
  ],
  "query_results": [
    {
      "query": "minimalist ADHD notion template",
      "total_results": 43,
      "total_results_vs_seed": "4% of seed (1000+) — low competition for this angle",
      "listings": [
        {
          "title": "...",
          "price": 12.00,
          "reviews": 8,
          "star_rating": 5.0,
          "is_bestseller": false,
          "is_star_seller": false,
          "shop_name": "..."
        }
      ]
    }
  ],
  "direct_competitors": [],
  "gap_confirmed": true,
  "autocomplete_suggestions": [
    "minimalist notion template ADHD",
    "simple ADHD planner notion"
  ],
  "recommended_title_keyword": "Minimalist ADHD Notion Planner",
  "competition_note": "No dominant direct competitor for the minimalist/low-stimulation angle. Closest existing products are all feature-heavy all-in-one systems from research_top_listings."
}
```

---

## Notes

- Do not compare against the seed category — only against the specific product angle.
- If a dominant direct competitor exists: flag it clearly, note its review count and Star Seller status, and describe what would still differentiate the proposed product.
- Prices from Etsy are shown in THB. Pass raw prices as-is.

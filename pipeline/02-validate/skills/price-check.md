# price-check

Analyze pricing across top listings for the seed category and the specific product angle. Recommend a launch price and a target long-term price based on competition, positioning, and market sweet spot.

This skill reasons over collected data — it does not browse the web. All pricing data comes from 01-research etsy_scan and 02-validate etsy-deep-dive outputs.

## Input

- `research_etsy_scan` — full `etsy_scan` output from 01-research, including `price_min`, `price_max`, `price_median`, and `top_listings[].price`
- `deep_dive_results` — `query_results` from etsy-deep-dive, including any listings found for the specific angle
- `product_idea` — the specific product concept
- `positioning` — 1–2 word tag derived from `product_idea_data.differentiator` (e.g. `"minimalist"`, `"student"`, `"shame-free"`)

---

## Steps

### 1. Map the price landscape

Group all listings into price bands (using sale prices where available):

| Band | Range | What it signals |
|---|---|---|
| Budget | < $5 | Loss-leader or low-trust signal — avoid |
| Entry | $5–$10 | Accessible, volume-oriented |
| Mid | $10–$18 | Standard range for digital templates |
| Premium | $18–$30 | Feature-rich or established seller premium |
| High | > $30 | Niche authority or bundle pricing |

Count listings per band across both `research_etsy_scan.top_listings` and all listings in `deep_dive_results.query_results[].listings`. The band with the most listings is the **market center**.

### 2. Find the conversion sweet spot

The sweet spot is where price and buyer trust intersect — look for listings that have the highest review count within each band. High reviews = proven willingness to pay at that price.

Cross-reference `is_star_seller` and `is_bestseller` flags:
- Star Seller listings at mid–premium = buyers trust and pay more for quality
- Non-Star Seller listings clustering at budget = price pressure, not real market preference

The sweet spot is the price band where: (a) Star Seller or Bestseller listings concentrate, AND (b) review counts are highest relative to the band.

### 3. Factor in positioning

Adjust the target price relative to the sweet spot center:

| Positioning | Adjustment | Reason |
|---|---|---|
| Minimalist / fewer features | −15% | Scope is intentionally narrower; price reflects that honestly |
| Student-focused | −10% | Students have tighter budgets — matching their expectations reduces friction |
| Niche / specialist angle | +15% | Unique solution commands a premium; buyers searching for it will pay |
| All-in-one / comprehensive | At sweet spot | Competes directly on features |
| New shop (no reviews yet) | −20% launch only | Compensates for trust deficit until first reviews accumulate |

Apply only the most relevant adjustment. Do not stack multiple adjustments.

### 4. Recommend pricing strategy

Produce three price points:

- **Launch price** — where to list initially to earn first reviews quickly. Apply the "New shop" adjustment (−20%) to the target price, then round to a clean .99 price point. The new shop discount is separate from — not stacked on — the positioning adjustment already baked into the target price. Must be ≥ `research_etsy_scan.price_median` — do not go below the market median.
- **Target price** — where to settle once the listing has enough reviews to establish trust. Derive from sweet spot center adjusted for positioning.
- **Display original price** — the "crossed out" price shown during sale. Must be a price you genuinely sell at first (even briefly) before running the sale — Etsy's policy requires this. Set as the target price or higher.

---

## Output

```json
{
  "product_idea": "minimal ADHD notion planner",
  "price_landscape": {
    "budget": { "range": "< $5", "count": 2 },
    "entry": { "range": "$5–$10", "count": 4 },
    "mid": { "range": "$10–$18", "count": 8 },
    "premium": { "range": "$18–$30", "count": 5 },
    "high": { "range": "> $30", "count": 1 }
  },
  "market_center": "mid ($10–$18)",
  "sweet_spot_evidence": "8 of 20 listings in mid band; top Star Seller sells at ~$15 with highest review count",
  "positioning": "minimalist",
  "positioning_adjustment": "-15% vs sweet spot center",
  "recommendations": {
    "launch_price": 9.99,
    "target_price": 13.99,
    "display_original_price": 13.99,
    "launch_note": "List at $13.99 first (display original). Then run a sale at $9.99 to drive early purchases."
  },
  "pricing_rationale": "Sweet spot center is ~$14. Minimalist positioning warrants -15% → ~$12 target, rounded to $13.99. Launch at $9.99 sale compensates for zero reviews. Floor is research price_median ($X) — well above."
}
```

---

## Notes

- Never recommend a launch price below `research_etsy_scan.price_median` — going below the market median signals low quality.
- The `display_original_price` must be a price you genuinely sell at before running the sale. List at that price first, even for one day.
- If `deep_dive_results` has fewer than 3 comparable listings for the specific angle: rely primarily on the broad category sweet spot from `research_etsy_scan`, note the uncertainty in `pricing_rationale`.

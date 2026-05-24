# review-miner

Read reviews from the 2–3 closest existing products to the proposed idea. Extract buyer language, unmet needs, complaints, and praise — this becomes the raw material for listing copy and product decisions.

Follows `skills/playwright.md` for screenshot vs snapshot usage, block handling, and cleanup.

## Input

- `product_idea` — the specific product concept being validated
- `listings_to_mine` — array of `{ listing_url, shop_name }` objects. Priority order:
  1. Direct competitors from `etsy-deep-dive.direct_competitors` (if any found)
  2. Fall back to `etsy_scan.top_listings[].listing_url` from 01-research
  Use 2–3 listings total.
- `min_reviews_to_mine` — minimum reviews a listing must have to be worth mining (passed from validate-agent). Skip listings below this threshold and move to the next in the priority list.
- `max_reviews_per_listing` — how many reviews to read per listing (passed from validate-agent).

---

## Steps

### 1. For each listing, navigate to the listing page

Navigate to each URL in `listings_to_mine` in priority order.

Take a **screenshot** of the visible reviews section.

### 2. Read reviews

Scroll through the reviews section and collect up to `max_reviews_per_listing` reviews. For each review record:
- `text` — the review text
- `rating` — star rating (1–5)
- `date` — review date

If a listing has fewer than `min_reviews_to_mine` reviews: skip it, move to the next listing.

### 3. Classify each review

For each review, classify the primary theme:

| Theme | Description |
|---|---|
| `praise_ease` | Buyer praises how easy/simple the template is |
| `praise_design` | Buyer praises visual design or layout |
| `praise_features` | Buyer praises specific features |
| `complaint_complexity` | Buyer found it too complex or overwhelming |
| `complaint_missing` | Buyer wishes it had something it doesn't |
| `complaint_setup` | Buyer had trouble setting it up |
| `praise_value` | Buyer mentions good value for price |
| `neutral` | Generic positive ("great product", "as described") |

### 4. Extract buyer language

Pull exact phrases that reveal how buyers describe what they need. Look specifically for:
- **Pain language** — what problem were they trying to solve? ("I've tried so many planners and this is the first one that...")
- **Outcome language** — what result did they get? ("finally I can...", "I actually use this every day")
- **Comparison language** — how do they compare to alternatives? ("unlike other planners...", "simpler than...")
- **Missing features** — what do they wish it had?

### 5. Synthesize

From all reviews collected across all listings:
- `top_praised` — up to 3 things buyers most consistently praise
- `top_complained` — up to 3 things buyers most consistently complain about or wish were different
- `unmet_needs` — specific features or angles mentioned as missing
- `buyer_voice_phrases` — exact verbatim phrases from reviews that best capture buyer sentiment (collect as many as found; quality over quantity)

---

## Output

```json
{
  "listings_mined": [
    {
      "listing_url": "https://www.etsy.com/listing/1509598332/",
      "shop_name": "TheSeekerSociety",
      "source": "research_top_listings",
      "reviews_read": 18,
      "themes": {
        "praise_ease": 4,
        "praise_features": 7,
        "complaint_complexity": 4,
        "complaint_setup": 2,
        "neutral": 1
      }
    }
  ],
  "top_praised": [
    "Color-coded layout makes navigation easy",
    "Covers every area of life in one place",
    "YouTube tutorial makes setup less intimidating"
  ],
  "top_complained": [
    "Takes time to learn — steep learning curve for Notion beginners",
    "Too many pages — overwhelming to start",
    "Some sections never get used"
  ],
  "unmet_needs": [
    "A simpler version for beginners",
    "Better mobile experience",
    "Quick-start mode with just the essentials"
  ],
  "buyer_voice_phrases": [
    "I've tried so many planners and always abandoned them after a week",
    "once you get the hang of it, it's everything you need",
    "finally something designed for how my ADHD brain actually works",
    "I wish there was a simpler version to start with",
    "the color coding is a game changer for me"
  ]
}
```

---

## Notes

- Prioritize reviews that mention the specific angle being validated. For "minimalist ADHD notion planner", weight reviews mentioning complexity/simplicity more heavily.
- Complaint reviews are more valuable than praise reviews — they reveal unmet needs directly.
- `buyer_voice_phrases` must be near-verbatim quotes, not paraphrases. These exact phrases go into listing copy.
- If all reviews are generic ("great product, fast delivery") with no specific feedback: note it — it means the product has low emotional resonance, which is itself a signal.

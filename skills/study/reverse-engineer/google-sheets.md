# reverse-engineer/google-sheets

Deep-dive study of each Google Sheets competitor using the Etsy listing page. Extracts buyer sentiment, stated features, visible tab structure from preview images, and visual style. Formula internals cannot be accessed without opening the spreadsheet — structure is inferred from listing descriptions and preview images only.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `competitor_urls` — array of Etsy listing URLs to study
- `max_competitors` — study only the first N URLs

---

## Steps (repeat for each URL, up to `max_competitors`)

### 1. Navigate to the listing page

Navigate to the listing URL. Take a **screenshot** of the full listing (preview images visible).

### 2. Read the listing

- Title and price
- Description — extract stated features, tab/sheet names, what the seller claims it does
- Tags (visible at bottom of listing)
- Preview images — describe each image: what tabs are visible, what data is shown, what formulas or features are visible in the screenshot

### 3. Read reviews

Scroll to reviews section. Take a **screenshot**. Read up to 20 reviews. For each review note:
- Rating (1–5)
- What the buyer praised (if positive)
- What the buyer complained about or wished was different (if negative or mixed)

### 4. Record findings

- `title`, `price`
- `key_features` — features described or visible in preview images
- `structure` — tab names visible in screenshots or mentioned in the listing description. Mark as `"inferred"` — these come from visual/text clues, not from opening the spreadsheet.
- `buyer_complaints` — exact pain language from reviews
- `buyer_wishes` — things buyers asked for that aren't there
- `visual_style` — `palette` (hex codes if visible), `font`, `style_notes`

---

## Output

```json
{
  "competitors": [
    {
      "url": "https://www.etsy.com/listing/...",
      "title": "Freelancer Budget Tracker Google Sheets Template",
      "price": "$18.00",
      "key_features": [
        "Income and expense tracking",
        "Monthly summary dashboard",
        "Category breakdown pie chart"
      ],
      "structure": {
        "tabs": ["Instructions", "Income", "Expenses", "Dashboard"],
        "source": "inferred",
        "notes": "Tab names visible in listing preview image 2. Seller description mentions 'Dashboard tab with automatic charts'."
      },
      "buyer_complaints": [
        "No instructions — had to figure it out myself",
        "Formulas broke when I deleted a row",
        "Doesn't work on mobile"
      ],
      "buyer_wishes": [
        "Annual summary view",
        "Dark theme option",
        "Category chart"
      ],
      "visual_style": {
        "palette": ["#2D6A4F", "#F0F4EF", "#FFFFFF"],
        "font": "Arial",
        "style_notes": "Clean, minimal. Green accent on header row. No icons or illustrations."
      }
    }
  ]
}
```

---

## Notes

- Formula internals are not available — Google Sheets templates cannot be opened or copied via automation. Structure and formula clues are inferred from listing descriptions and preview images only.
- If a listing has fewer than 5 reviews: note it and skip `buyer_complaints` / `buyer_wishes` rather than inferring.
- If blocked on Etsy (captcha/bot screen): note `"source": "blocked"`, skip this URL, continue to next.
- `structure.source` is always `"inferred"` — treat tab names as indicative, not confirmed.

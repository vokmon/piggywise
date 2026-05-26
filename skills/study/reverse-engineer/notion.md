# reverse-engineer/notion

Two-source study for each Notion competitor: (1) Etsy listing page for buyer sentiment and surface visuals; (2) a free equivalent from Notion template galleries for actual structure and database internals. Follows `skills/playwright.md` for screenshot/snapshot rules and cleanup.

## Input

- `competitor_urls` — array of Etsy listing URLs to study
- `max_competitors` — study only the first N URLs
- `keyword` — used to find free equivalents when Etsy listing doesn't suggest one

---

## Steps

### 0. Log in to Notion

Run `skills/notion-login.md`. If `logged_in: false`: stop and ask the human to set `NOTION_EMAIL` and `NOTION_PASSWORD` in `.env` before continuing.

Repeat the following for each URL, up to `max_competitors`:

### Source 1 — Etsy listing page

1. Navigate to the listing URL. Take a **screenshot** of the full listing (preview images visible).

2. Read the listing:
   - Title and price
   - Description — extract stated features, page/database names, what the seller claims it does
   - Tags (visible at bottom of listing)
   - Preview images — describe the visual style: palette, cover style, icon style, layout

3. Scroll to reviews section. Take a **screenshot**. Read up to 20 reviews. For each review note:
   - Rating (1–5)
   - What the buyer praised (if positive)
   - What the buyer complained about or wished was different (if negative or mixed)

4. Record Source 1 findings:
   - `title`, `price`
   - `key_features` — features described or visible in preview images
   - `buyer_complaints` — exact pain language from reviews
   - `buyer_wishes` — things buyers asked for that aren't there
   - `visual_style` — `palette` (hex codes if visible), cover/icon style, `style_notes`

### Source 2 — Free equivalent template

5. Search for the closest free Notion equivalent to this competitor's product. Search in this order, stopping when you find a suitable match:
   - Notion official gallery: `https://www.notion.so/templates` (search by keyword or browse category)
   - NotionPages.com: search `site:notionpages.com {keyword}`
   - Pinterest: search `{keyword} notion template free`

6. Take a **screenshot** of the template gallery page showing the candidate.

7. Copy the template into the Notion workspace using Playwright:
   - Navigate to the template URL (notion.site or notion.so/templates)
   - Take a **screenshot** to confirm the page loaded
   - Click "Start with this template" (or "Duplicate" / "Get template")
   - Wait for the page to open in the workspace (~3s)
   - Take a **screenshot** of the new workspace page and note its URL/ID

8. **Study the copy** using `mcp__claude_ai_Notion__notion-fetch` on the copied page — do not modify:
   - List all top-level pages and databases
   - For each database: list properties (name, type) and any views (table, board, calendar, gallery, list)
   - Identify formula properties: what they calculate, which fields they depend on
   - Identify rollups: source database, property rolled up, aggregation used
   - Describe relations: which databases are linked and how
   - Note any linked databases, filtered views, or cross-page references

9. Record Source 2 findings:
   - `structure` — list of pages/databases with types
   - `logic_notes` — plain-language summary of formulas, rollups, and relations
   - `key_formulas` — formula properties and rollups (name, property type, depends_on, logic)
   - `free_equivalent_urls` — URLs where this free template was found

10. **Trash the copy** using `mcp__claude_ai_Notion__notion-update-data-source` with `in_trash: true` and the page ID noted in Step 7. Confirm it is removed before continuing.

---

## Output

```json
{
  "competitors": [
    {
      "url": "https://www.etsy.com/listing/...",
      "title": "Notion Life Planner — All-in-One Dashboard",
      "price": "$22.00",
      "key_features": [
        "Habit tracker with streak counting",
        "Goal tracker with progress bars",
        "Daily journal with mood tagging"
      ],
      "structure": [
        "Home",
        "Goals (database)",
        "Habits (database)",
        "Journal (database)",
        "Tasks (database)"
      ],
      "logic_notes": "Habits database uses a formula property to calculate current streak from checkbox history. Goals database uses rollup from Tasks to show completion percentage. No relations between Habits and Goals.",
      "key_formulas": [
        {
          "name": "Streak",
          "location": "Habits database — formula property",
          "depends_on": "Done (checkbox)",
          "logic": "Counts consecutive days where Done is checked — breaks on first unchecked day"
        },
        {
          "name": "Progress",
          "location": "Goals database — rollup property",
          "depends_on": "Tasks relation",
          "logic": "Percent of related Tasks where Status = Done"
        }
      ],
      "buyer_complaints": [
        "Takes forever to set up",
        "Too many databases — overwhelming",
        "Streak formula doesn't work correctly"
      ],
      "buyer_wishes": [
        "Mobile-friendly layout",
        "Simpler version for beginners",
        "Video walkthrough"
      ],
      "visual_style": {
        "palette": ["#F5E6D3", "#8B6914", "#FFFFFF"],
        "font": "Default Notion",
        "style_notes": "Warm beige tones. Custom icons. Aesthetic header images on each page."
      },
      "free_equivalent_urls": [
        "https://www.notion.so/templates/...",
        "https://notionpages.com/..."
      ]
    }
  ]
}
```

---

## Notes

- If a listing has fewer than 5 reviews, note it — skip buyer_complaints and buyer_wishes rather than inferring.
- Notion formulas can be complex — record the intent and dependencies, not the full formula syntax.
- If copying a template via "Start with this template" requires a paid Notion plan and fails: note `"free_equivalent_urls"` found but `"structure": null`, `"logic_notes": "template requires paid plan — could not copy"`.
- If blocked on Etsy (captcha/bot screen): note `"source": "blocked"`, skip this URL, continue to next.
- If no free equivalent can be found after checking all sources: record `"free_equivalent_urls": []` and set `"structure": null`, `"logic_notes": "no free equivalent found"`.
- Always trash study copies before moving to the next competitor.

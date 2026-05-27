# reverse-engineer/canva

Two-source study for each Canva competitor: (1) Etsy listing page for buyer sentiment and surface visuals; (2) a free equivalent from the Canva template gallery for actual page/frame structure and layout patterns. Follows `skills/playwright.md` for screenshot/snapshot rules and cleanup.

No logic or formulas — Canva products are purely visual. Focus on page structure, visual hierarchy, layout patterns, and design language.

## Input

- `competitor_urls` — array of Etsy listing URLs to study
- `max_competitors` — study only the first N URLs
- `keyword` — used to find free equivalents

---

## Steps

### 0. Log in to Canva

Run `skills/canva-login.md`. If `logged_in: false`: stop and ask the human to set `CANVA_EMAIL` and `CANVA_PASSWORD` in `.env` before continuing.

Repeat the following for each URL, up to `max_competitors`:

### Source 1 — Etsy listing page

1. Navigate to the listing URL. Take a **screenshot** of the full listing (all preview images visible).

2. Read the listing:
   - Title and price
   - Description — extract stated features, number of pages/slides/frames, stated dimensions, file formats included
   - Tags (visible at bottom of listing)
   - Preview images — describe the visual style: palette, typography, layout structure, overall aesthetic, mood

3. Scroll to reviews section. Take a **screenshot**. Read up to 20 reviews. For each review note:
   - Rating (1–5)
   - What the buyer praised (if positive)
   - What the buyer complained about or wished was different (if negative or mixed)

4. Record Source 1 findings:
   - `title`, `price`
   - `key_features` — features described or visible in preview images (page count, formats, customisability)
   - `buyer_complaints` — exact pain language from reviews
   - `buyer_wishes` — things buyers asked for that aren't there
   - `visual_style` — `palette` (hex codes if visible), typography, layout style, `style_notes`

### Source 2 — Free equivalent template

5. Search for the closest free Canva equivalent to this competitor's product. Search in this order, stopping when you find a suitable match:
   - Canva template gallery: `https://www.canva.com/templates/` (search by keyword)
   - Pinterest: search `{keyword} canva template free` — only follow links that resolve to an actual Canva template URL

6. Take a **screenshot** of the template gallery page showing the candidate.

7. Copy the template into the Canva workspace using `mcp__canva__create-design-from-candidate` with the template URL.

8. **Study the copy** using `mcp__canva__get-design-pages` to list all pages, then `mcp__canva__get-design-content` for each page — do not edit:
   - Count the total number of pages/slides/frames
   - List each page/frame by name or purpose (e.g. "Cover", "About Me", "Portfolio Grid", "Contact")
   - For each page: describe the layout structure (e.g. "full-bleed image left, text right"), element types (text blocks, icons, shapes, photos), and colour usage
   - Note the overall visual rhythm: how pages relate to each other, whether there's a consistent grid or spacing system

9. Record Source 2 findings:
   - `structure` — list of page/frame names with brief purpose description
   - `logic_notes` — visual layout patterns and design system notes (no formulas — use this field for layout logic like grid systems, spacing patterns)
   - `free_equivalent_urls` — URLs where this free template was found

10. **Delete the copy** from the Canva workspace using Canva MCP. Confirm it is gone before continuing.

---

## Output

```json
{
  "competitors": [
    {
      "url": "https://www.etsy.com/listing/...",
      "title": "Canva Media Kit Template — Influencer Press Kit",
      "price": "$14.00",
      "key_features": [
        "10-page Canva template",
        "Fully customisable",
        "A4 and Letter size",
        "Includes PNG and PDF export instructions"
      ],
      "structure": [
        "Cover — name, tagline, hero photo",
        "About Me — bio and headshot",
        "Audience Stats — 3-column metrics layout",
        "Platforms — icon grid with follower counts",
        "Past Collaborations — logo grid",
        "Rates — pricing table",
        "Contact — social handles and email"
      ],
      "logic_notes": "Consistent two-column grid throughout. Cover breaks the grid with full-bleed. Text blocks always left-aligned. Brand colour used as accent on headings only.",
      "key_formulas": [],
      "buyer_complaints": [
        "Hard to change the fonts — not obvious how",
        "Photos don't fit the placeholders well",
        "No instructions included"
      ],
      "buyer_wishes": [
        "Dark version",
        "More page layout options",
        "Tutorial video"
      ],
      "visual_style": {
        "palette": ["#F9F5F0", "#C8A96E", "#1A1A1A"],
        "font": "Playfair Display (headings) + Lato (body)",
        "style_notes": "Luxury editorial feel. Warm neutrals. Heavy white space. Thin decorative lines as dividers."
      },
      "free_equivalent_urls": [
        "https://www.canva.com/templates/..."
      ]
    }
  ]
}
```

---

## Notes

- `key_formulas` is always an empty array for Canva products — no logic to extract.
- `logic_notes` for Canva describes visual layout logic (grid, spacing, hierarchy), not formulas.
- If a listing has fewer than 5 reviews: note it — skip buyer_complaints and buyer_wishes rather than inferring.
- If the free equivalent is behind a Canva Pro paywall: note in `logic_notes` and describe what is visible from the preview.
- If blocked on Etsy (captcha/bot screen): note `"source": "blocked"`, skip this URL, continue to next.
- If no free equivalent found after checking all sources: record `"free_equivalent_urls": []` and set `"structure": null`, `"logic_notes": "no free equivalent found"`.
- Always delete study copies before moving to the next competitor.

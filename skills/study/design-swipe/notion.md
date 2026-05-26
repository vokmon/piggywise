# design-swipe/notion

Collect visual inspiration beyond the direct competitors already studied in reverse-engineer. Focus on surface aesthetics: colour palette, cover image style, icon usage, page layout, typography choices. This feeds the `visual_inspiration` field in poc-brief and informs the `style` synthesis.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `keyword` — the validated keyword (used as search seed)
- `style_signals` — preliminary style observations from reverse-engineer (optional — used to focus or contrast the search)

---

## Steps

### 1. Search visual inspiration sources

Search these sources. Collect 6–10 strong visual references across all sources:

1. **Pinterest** — search `{keyword} notion template` and `{keyword} notion dashboard`
   Also try aesthetic directions: `{keyword} notion aesthetic`, `notion dashboard design inspiration`

2. **Etsy** — navigate to `https://www.etsy.com`, type `{keyword} notion template` in the search box and press Enter.
   Browse listing preview images for visual style — palette, cover style, icon choices, layout. Do not open listings for reviews; this is visual reference only.

3. **Notion official gallery** — `https://www.notion.so/templates`
   Browse for visually distinctive templates — focus on layout, cover style, and colour usage, not just feature match.

For each reference: take a **screenshot** of the preview. Do not copy any templates into the workspace at this stage.

### 2. Analyse visual patterns

Across all collected references, identify:

- **Dominant palettes** — what colour combinations appear most? Warm neutrals, dark mode, pastel, bold?
- **Cover image style** — gradient, solid colour, illustration, photography, none?
- **Icon usage** — emoji icons, custom icons, no icons?
- **Page structure patterns** — gallery view vs list view on databases, callout boxes, dividers, toggle sections
- **Typography** — default Notion fonts vs custom web fonts, heading weight and size patterns
- **Differentiating visuals** — what makes one Notion template look premium vs a basic template?

### 3. Record inspiration

Select the 3–5 most useful visual references (most instructive for our planned product).

---

## Output

```json
{
  "visual_inspiration": {
    "pinterest_boards": [
      "https://pinterest.com/pin/...",
      "https://pinterest.com/pin/..."
    ],
    "etsy_listings": ["https://www.etsy.com/listing/..."],
    "other_references": [
      "https://www.notion.so/templates/...",
      "https://notionpages.com/..."
    ],
    "style_notes": "Pinterest shows strong demand for warm beige/brown aesthetic ('notion aesthetic' searches). Official gallery templates trending toward dark headers with light page backgrounds. Emoji icons dominant — custom icon sets used only in premium paid templates. Best layouts use callout boxes as visual anchors for key metrics. Gallery view on databases consistently looks more polished than table view in lifestyle products."
  }
}
```

---

## Notes

- Do not copy any templates into the workspace — screenshots and visual observation only.
- `style_notes` should be actionable: specific observations the synthesis step can use to form palette/cover/icon decisions.
- If `style_signals` from reverse-engineer suggest a specific direction: use the search to either confirm or find a contrasting direction worth noting.
- If any source is blocked or returns irrelevant results: skip it, note it, continue with remaining sources.

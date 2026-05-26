# design-swipe/google-sheets

Collect visual inspiration beyond the direct competitors already studied in reverse-engineer. Focus on surface aesthetics: palette, typography, layout style, icon usage. This feeds the `visual_inspiration` field in poc-brief and informs the `style` synthesis.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `keyword` — the validated keyword (used as search seed)
- `style_signals` — preliminary style observations from reverse-engineer (optional — used to focus or contrast the search)

---

## Steps

### 1. Search visual inspiration sources

Search these sources. Collect 6–10 strong visual references across all sources:

1. **Pinterest** — search `{keyword} google sheets template` and `{keyword} spreadsheet design`
   Also try broader visual directions: `{keyword} dashboard design`, `{keyword} tracker aesthetic`

2. **Etsy** — navigate to `https://www.etsy.com`, type `{keyword} spreadsheet template` in the search box and press Enter.
   Browse listing preview images for visual style — palette, header design, layout density. Do not open listings for reviews; this is visual reference only.

3. **Vertex42** — `https://vertex42.com/ExcelTemplates/` — browse for interesting visual styles. Screenshots of listing/preview pages only — do not download any templates.

4. **Smartsheet templates** — `https://www.smartsheet.com/free-spreadsheet-templates` — browse for visual ideas. Screenshots of listing/preview pages only — do not open any templates.

For each reference: take a **screenshot**. Do not open or copy any templates.

### 2. Analyse visual patterns

Across all collected references, identify:
- **Dominant palettes** — what colour combinations appear most? Any clear aesthetic directions (dark/minimal, light/clean, colourful/bold)?
- **Typography patterns** — default Sheets fonts vs custom, header styles, weight usage
- **Layout conventions** — how do the best-looking sheets use whitespace, row height, column width, frozen rows?
- **Icon / illustration usage** — are icons used? Where? What style?
- **Differentiating visuals** — what design choices make one sheet look premium vs generic?

### 3. Record inspiration

Select the 3–5 most useful visual references (not necessarily the prettiest — the most instructive for our planned product).

---

## Output

```json
{
  "visual_inspiration": {
    "pinterest_boards": [
      "https://pinterest.com/pin/...",
      "https://pinterest.com/pin/..."
    ],
    "etsy_listings": [
      "https://www.etsy.com/listing/..."
    ],
    "other_references": [
      "https://vertex42.com/...",
      "https://www.smartsheet.com/..."
    ],
    "style_notes": "Strong Pinterest signal toward dark-mode dashboards with teal accents. Etsy listings and Vertex42 confirm light themes dominate the free tier — dark mode is a differentiator. Typography is almost universally default Google Sheets fonts; using a clean sans-serif (e.g. Inter) would stand out. Best layouts use frozen header rows with bold background colour and generous row height (28–32px)."
  }
}
```

---

## Notes

- Do not open or copy any templates — screenshots and visual observation only.
- `style_notes` should be actionable: specific observations the synthesis step can use to form palette/font/layout decisions.
- If `style_signals` from reverse-engineer suggest a specific direction: use the search to either confirm or find a contrasting direction worth noting.
- If any source is blocked or returns irrelevant results: skip it, note it, continue with remaining sources.

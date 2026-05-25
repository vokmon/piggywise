# design-swipe/canva

Collect visual inspiration beyond the direct competitors already studied in reverse-engineer. Focus on surface aesthetics: colour palette, typography pairing, layout structure, visual hierarchy, mood. This feeds the `visual_inspiration` field in poc-brief and informs the `style` synthesis.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `keyword` — the validated keyword (used as search seed)
- `style_signals` — preliminary style observations from reverse-engineer (optional — used to focus or contrast the search)

---

## Steps

### 1. Search visual inspiration sources

Search these sources. Collect 6–10 strong visual references across all sources:

1. **Pinterest** — search `{keyword} canva template` and `{keyword} design`
   Also try mood/aesthetic directions: `{keyword} minimal design`, `{keyword} luxury branding`, `{keyword} editorial layout`

2. **Etsy** — search `{keyword} canva template`
   Browse listing preview images for visual style — palette, typography, layout density. Do not open listings for reviews; this is visual reference only.

3. **Canva template gallery** — `https://www.canva.com/templates/`
   Browse for visually distinctive examples — focus on layout, typographic hierarchy, and colour palette, not just feature match.

4. **Behance** — search `{keyword} design` or browse `https://www.behance.net/`
   Look for polished work in the same category — for layout inspiration.

5. **Dribbble** — search `{keyword}` at `https://dribbble.com/`
   Focus on typography and colour palette trends.

For each reference: take a **screenshot**. Do not copy or open any templates at this stage.

### 2. Analyse visual patterns

Across all collected references, identify:
- **Dominant palettes** — what colour combinations appear most? Any clear trends (dark/luxury, light/minimal, bold/colourful)?
- **Typography pairing** — what font combinations are most common? Serif headings with sans body? All-sans? Display fonts?
- **Layout patterns** — full-bleed images, whitespace usage, grid vs organic layout, use of borders and dividers
- **Mood/aesthetic direction** — what overall feeling do the best-looking examples convey?
- **Differentiating visuals** — what design choices separate premium templates from generic ones in this category?

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
    "etsy_listings": [
      "https://www.etsy.com/listing/..."
    ],
    "other_references": [
      "https://www.canva.com/templates/...",
      "https://www.behance.net/gallery/...",
      "https://dribbble.com/shots/..."
    ],
    "style_notes": "Pinterest and Behance both point toward luxury editorial aesthetic for this category: warm neutrals (cream, tan, terracotta), Serif display heading + clean sans body, heavy whitespace. Dribbble shows bold dark-mode versions gaining traction. Canva gallery dominated by generic pastel templates — clean opportunity to stand out with a more editorial look. Key differentiator across premium examples: consistent typographic hierarchy (3 clear levels) and generous margins."
  }
}
```

---

## Notes

- Do not copy any templates — screenshots and visual observation only.
- `style_notes` should be actionable: specific observations the synthesis step can use to form palette/font/layout decisions.
- If `style_signals` from reverse-engineer suggest a specific direction: use the search to either confirm or find a contrasting direction worth noting.
- Behance and Dribbble are for layout/typography inspiration — the actual scaffold will come from Canva gallery (handled in template-hunt).
- If any source is blocked or returns irrelevant results: skip it, note it, continue with remaining sources.

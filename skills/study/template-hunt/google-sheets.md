# template-hunt/google-sheets

Gather structural and visual inspiration for the Google Sheets product from Etsy listings and Pinterest. There is no scaffold to copy — Google Sheets templates cannot be duplicated via automation. The output informs what tabs, formulas, and layouts to build from scratch in the build step.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `feature_spec` — always `null` at call time (synthesis happens after this skill runs); evaluation is done against the keyword and competitor structures from the reverse-engineer step instead
- `max_templates` — maximum number of inspiration references to collect
- `keyword` — the validated keyword (used as search seed)

---

## Steps

### 1. Search for inspiration

Search these sources in order. Collect up to `max_templates` references across all sources:

1. **Etsy** — navigate to `https://www.etsy.com`, type `{keyword} spreadsheet` in the search box and press Enter. If results are thin, repeat with `{keyword} google sheets template`.
   Browse listing pages and preview images. Look at what tabs/sections are shown in listing photos, what features are highlighted in descriptions.

2. **Pinterest** — search `{keyword} google sheets template` or `{keyword} spreadsheet layout`
   Collect screenshots of spreadsheet layouts, tab structures, and dashboard designs.

For each reference found: take a **screenshot** of the listing or pin page.

### 2. Extract structure and design notes

For each reference, note:
- **Tab names** — what tabs/sheets are visible in screenshots or described in listings?
- **Key formulas/features** — any mentioned formulas, dashboards, charts, or automations?
- **Visual style** — colour palette, header style, layout density
- **Price and format** — what are competitors charging and what do they deliver?

### 3. Summarise findings

Compile the collected references into a structural summary:
- Most common tab names across references
- Most common features and formulas
- Visual patterns worth adopting (colour schemes, header styles)
- Any differentiation opportunities (features competitors lack)

---

## Output

```json
{
  "inspirations": [
    {
      "url": "https://www.etsy.com/listing/...",
      "source": "etsy",
      "title": "Budget Tracker Spreadsheet Template",
      "notes": "Shows 5 tabs: Dashboard, Income, Expenses, Savings Goals, Reports. Dashboard has pie charts. Listed at $7. Headers use teal colour scheme."
    },
    {
      "url": "https://www.pinterest.com/pin/...",
      "source": "pinterest",
      "title": "Monthly Budget Google Sheets",
      "notes": "Screenshot shows Income and Expenses side-by-side on Dashboard tab. Category dropdowns visible. Clean white/green palette."
    }
  ],
  "structure_summary": {
    "common_tabs": ["Dashboard", "Income", "Expenses", "Savings Goals"],
    "common_features": ["category dropdowns", "monthly summary", "charts/graphs", "year-to-date totals"],
    "visual_patterns": ["light palette with one accent colour", "frozen header row", "conditional formatting on balance cells"],
    "differentiation_opportunities": ["automated savings rate calculation", "debt payoff tracker tab"]
  },
  "scaffold_url": null,
  "scaffold_source": null
}
```

---

## Notes

- There is no scaffold to copy — `scaffold_url` is always `null` for Google Sheets products. The build step generates the XLSX from scratch using Python/openpyxl.
- The `structure_summary` is the primary output — it feeds directly into synthesis and the build step.
- Collect enough references to identify structural patterns, not to find one perfect match.
- If a source returns no useful results: skip it and note it, continue to next source.

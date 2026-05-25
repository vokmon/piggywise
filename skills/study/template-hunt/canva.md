# template-hunt/canva

Study free Canva template galleries to harvest structural and design patterns for the POC. Study up to `max_templates` candidates. Extract the best pattern(s) from each. Build fresh from these patterns — do not copy any single template wholesale.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `feature_spec` — always `null` at call time (synthesis happens after this skill runs); pattern extraction is done against the keyword and competitor structures from the reverse-engineer step instead
- `max_templates` — maximum number of candidates to study
- `keyword` — the validated keyword (used as search seed)

---

## Steps

### 0. Log in to Canva

Run `skills/canva-login.md`. If `logged_in: false`: stop and ask the human to set `CANVA_EMAIL` and `CANVA_PASSWORD` in `.env` before continuing.

### 1. Search for candidates

Search these sources in order. Collect up to `max_templates` candidates across all sources:

1. **Canva template gallery** — `https://www.canva.com/templates/`
   Search for `{keyword}` and filter to free templates. Skip any Canva Pro-only templates.

2. **Pinterest** — search `{keyword} canva template free`
   Only collect candidates that resolve to an actual Canva template URL.

For each candidate found: take a **screenshot** of the listing/preview page.

### 2. Study each candidate

For each candidate, browse the preview (do NOT copy). Extract:

- **Page/frame structure** — how many pages, what is the purpose of each?
- **Layout patterns** — grid structure, section organisation, content hierarchy
- **Typography choices** — font pairings, heading size, visual weight
- **Colour usage** — palette structure, background/accent/text colour roles
- **Visual elements** — icon style, imagery, decorative elements
- **UX patterns** — how does the buyer navigate or use this template?
- **Specific patterns worth borrowing** — the 1–2 things this template does better than others

Take a **screenshot** of each template's most distinctive page.

### 3. Compile pattern library

Across all studied candidates, compile a `pattern_library[]`: one entry per candidate with the specific pattern(s) worth borrowing. Also write a `structure_summary` identifying the most common structural patterns and any differentiation opportunities.

Do NOT select a single "best" template to copy. The build step assembles patterns from multiple sources into a fresh design.

---

## Output

```json
{
  "pattern_library": [
    {
      "url": "https://www.canva.com/templates/...",
      "source": "canva-gallery",
      "title": "Kids Budget Tracker Printable",
      "patterns_to_borrow": [
        "Progress bar layout for savings goal tracking",
        "Colour-coded category icons (one per spending category)"
      ],
      "notes": "Strong visual hierarchy on the dashboard page. Typography too bold for our target age range — ignore font choices."
    },
    {
      "url": "https://www.canva.com/templates/...",
      "source": "pinterest",
      "title": "Weekly Planner Printable",
      "patterns_to_borrow": [
        "7-column day grid with consistent row heights — clean and readable at A4 size"
      ],
      "notes": "Found via Pinterest, resolves to a free Canva template. Layout pattern is reusable; colour and font choices are not."
    }
  ],
  "structure_summary": {
    "common_pages": ["Cover", "Instructions", "Main Tracker", "Summary/Totals"],
    "common_features": ["Category labels", "Date fields", "Progress indicators"],
    "visual_patterns": ["Pastel palettes dominant in kids/family templates", "Bold headers with light body text", "Icon-per-category convention"],
    "differentiation_opportunities": ["No template studied included a parent co-use mode", "Most use portrait A4 — landscape could differentiate"]
  }
}
```

---

## Notes

- Do NOT copy any template — study only (preview and screenshots).
- Study all `max_templates` candidates before compiling.
- Skip any template that requires a Canva Pro plan.
- `patterns_to_borrow` must be specific and actionable — not "nice design" but "progress bar layout for goal tracking on page 2".
- If a source is blocked or returns no useful results: skip it and note it, continue to next source.

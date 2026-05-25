# test-plan

Generate `test-plan.json` for the built product. Covers 6 test categories. Called by build-agent after the product is built and formula-spec is written.

---

## Input

- `product_type` — string identifying the product type
- `formula_spec_path` — path to `products/{slug}/docs/formula-spec.md` (Sheets/Notion only; null for Canva)
- `style_guide_path` — path to `products/{slug}/docs/style-guide.json`
- `differentiation` — array of differentiation items from poc-brief
- `gaps` — array of filled gaps from poc-brief
- `buyer_flow` — step-by-step buyer usage flow from poc-brief
- `structure` — actual built structure from poc-brief (tabs/pages/frames)

---

## Test categories

_To add a new product type: add `applies_to` values and extend the relevant category notes below._

Write one test object per test case. Each test has:
- `id` — unique identifier (e.g. `logic_01`, `style_02`)
- `category` — one of the 6 categories below
- `description` — what is being tested
- `steps` — ordered list of actions to perform
- `expected` — what a passing result looks like
- `applies_to` — `all` | `google-sheets` | `notion` | `sheets-notion` (skip test if product_type doesn't match)

---

### Category 1: Logic
**Applies to:** `google-sheets` and `notion` only. Skip for Canva.

Source: `formula_spec_path` — one test per formula or data flow listed in formula-spec.

For each formula/rollup/relation in formula-spec:
- Test that it returns the correct value with known sample data.
- Test that data flows between tabs/databases update correctly (e.g. Income tab change reflects on Dashboard).

### Category 2: Edge cases
**Applies to:** `google-sheets` and `notion` only. Skip for Canva.

Source: `formula_spec_path` — test the formulas under boundary conditions.

Standard edge cases to cover:
- All input cells empty — formulas should return 0 or blank, not an error.
- Zero values entered — no division-by-zero errors.
- Negative values entered (if allowed) — handled correctly or blocked by validation.
- Maximum realistic values (e.g. 999999 in a currency field) — no overflow or display issues.

### Category 3: Style
**Applies to:** all product types.

Source: `style_guide_path` — verify the built product matches the confirmed style.

Tests to write:
- Palette: primary background colour, accent colour, and text colour match `style-guide.json` values.
- Font: heading font and body font match `style-guide.json` values.
- Layout: layout style (e.g. frozen rows, consistent row heights, margins) matches `style-guide.json`.
- Consistency: spot-check 3 different tabs/pages/frames to confirm style is applied consistently across the product.

### Category 4: Buyer flow
**Applies to:** all product types.

Source: `buyer_flow` — one test per step in the buyer flow.

For each step in `buyer_flow`:
- Verify the buyer can complete that step using only what is visible in the product (no external guidance needed for basic usage).
- Verify the Instructions tab/page covers that step clearly.

### Category 5: Differentiation
**Applies to:** all product types.

Source: `differentiation` — one test per item.

For each item in `differentiation[]`:
- Write a test that confirms the item is present and works as described.
- Be specific: if differentiation says "clear Instructions tab — top complaint across competitors", the test should verify the Instructions tab exists, is the first tab, and contains the relevant setup steps.

### Category 6: Gaps filled
**Applies to:** all product types.

Source: `gaps` — one test per filled gap.

For each item in `gaps[]`:
- Write a test that confirms the gap has been filled in the built product.
- Same specificity requirement as Category 5.

---

## Output

Write to `products/{slug}/docs/test-plan.json`:

```json
{
  "product_slug": "{slug}",
  "product_type": "google-sheets",
  "generated_from": {
    "formula_spec": "products/{slug}/docs/formula-spec.md",
    "style_guide": "products/{slug}/docs/style-guide.json",
    "differentiation_count": 3,
    "gaps_count": 2,
    "buyer_flow_steps": 4
  },
  "tests": [
    {
      "id": "logic_01",
      "category": "logic",
      "applies_to": "sheets-notion",
      "description": "Total Income formula returns correct sum",
      "steps": [
        "Open Income tab",
        "Enter 3 rows: 500, 1200, 750 in the Amount column",
        "Open Dashboard tab",
        "Read the Total Income cell"
      ],
      "expected": "Total Income shows 2450"
    },
    {
      "id": "edge_01",
      "category": "edge_cases",
      "applies_to": "sheets-notion",
      "description": "Total Income formula returns 0 (not error) when Income tab is empty",
      "steps": [
        "Ensure Income tab has no data rows",
        "Open Dashboard tab",
        "Read the Total Income cell"
      ],
      "expected": "Total Income shows 0 or blank — no #DIV/0! or #REF! error"
    },
    {
      "id": "style_01",
      "category": "style",
      "applies_to": "all",
      "description": "Header background colour matches style-guide palette[0]",
      "steps": [
        "Open Instructions tab",
        "Check the header row background colour"
      ],
      "expected": "Header background is #1A1A2E (style-guide palette[0])"
    },
    {
      "id": "buyer_flow_01",
      "category": "buyer_flow",
      "applies_to": "all",
      "description": "Buyer can find and read the Instructions tab without external help",
      "steps": [
        "Open the product as a new user (no prior knowledge)",
        "Locate the Instructions tab",
        "Read the setup steps"
      ],
      "expected": "Instructions tab is first tab, clearly labelled, contains numbered setup steps"
    },
    {
      "id": "diff_01",
      "category": "differentiation",
      "applies_to": "all",
      "description": "Instructions tab exists and is the first tab (top buyer complaint across competitors)",
      "steps": [
        "Open the product",
        "Check the first tab name",
        "Verify it contains setup instructions"
      ],
      "expected": "First tab is named 'Instructions', contains numbered setup guide"
    },
    {
      "id": "gap_01",
      "category": "gaps_filled",
      "applies_to": "all",
      "description": "Annual summary view exists (deferred gap from POC)",
      "steps": [
        "Navigate to the Dashboard tab (or Annual Summary tab if separate)",
        "Verify an annual summary section or tab exists"
      ],
      "expected": "Annual totals visible — income and expenses summed across all 12 months"
    }
  ]
}
```

---

## Notes

- Skip Category 1 and Category 2 entirely for Canva — set `applies_to: "sheets-notion"` on all logic/edge case tests and the test runner skips them.
- Every item in `differentiation[]` must produce exactly one test in Category 5 — no omissions.
- Every item in `gaps[]` must produce exactly one test in Category 6 — no omissions.
- Test `steps` must be concrete actions, not vague checks ("verify it works" is not a valid step).
- Test `expected` must be a specific, observable outcome — not "it looks correct".

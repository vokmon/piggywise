# build-agent

Orchestrates Stage 04: polish the POC into a shippable product, self-test until clean, produce all product docs, and update `product.json`. Reads the poc-brief from Stage 03. Stage 05 is an independent sign-off — this agent must deliver a clean product before handing off.

---

## Parameters

- `poc_brief` — path to the Stage 03 poc-brief file (e.g. `pipeline/03-poc/output/kids-budget-planner-poc-brief.json`)

---

## Steps

### Step 1 — Load poc-brief

Read `poc_brief`.

Extract and hold in memory:
- `product_type`
- `poc_result.link` — starting point for the build
- `known_issues` — fix these first in Step 2
- `feature_spec` — implement fully in Step 2
- `structure` — actual built structure from the POC (passed to the build skill)
- `differentiation` — every item must exist in the finished product
- `gaps` — fill after all differentiation items are delivered
- `style` — confirmed palette/font/layout
- `competitors[].buyer_complaints` — aggregate across all competitors into a single list (deduplicated)
- `buyer_flow` — step-by-step buyer usage
- `delivery_format`
- `slug`, `keyword`

Confirm `product_type` is recognised (see `skills/study/reverse-engineer.md` routing table for supported types). If unexpected value: stop and ask the human.

Copy the POC into the **Products folder**, named `{keyword}` (no prefix) — this preserves the POC as a fallback if the build goes wrong. See `pipeline/workspace-setup.md` for platform-specific copy and move steps.

All subsequent steps work on this **Products/ copy**, not the original POC. Update `working_link` to the new Products/ link.

### Step 2 — Build full polish

Open the Products/ copy (`working_link`).

Run `skills/build/{product_type}.md` with:
- `working_link` — updated link from Step 1 (Products/ copy)
- `feature_spec` — from poc-brief
- `structure` — actual structure from poc-brief (the built POC structure)
- `style` — from poc-brief
- `differentiation` — from poc-brief
- `gaps` — from poc-brief
- `known_issues` — from poc-brief
- `depth: "full"`
- `slug` — from poc-brief (Google Sheets only — required for file naming)
- `keyword` — from poc-brief (Google Sheets only — required for Drive file naming)

Build order within the skill:
1. Fix all `known_issues` first
2. Polish `feature_spec[]` to full quality
3. Verify every `differentiation[]` item exists (checklist)
4. Fill `gaps[]`

Inline checks are required throughout — see `skills/build/{product_type}.md` for specifics.

### Step 3 — Write formula-spec (Sheets and Notion only)

**Skip this step for Canva** — set `formula_spec_path: null`.

Write `products/{slug}/docs/formula-spec.md` documenting every formula, relation, and rollup in the built product:

```markdown
# Formula Spec — {Product Name}

## {Tab/Database Name}

### {Formula/Property Name}
- **Location:** {cell reference or property name}
- **Calculates:** {plain-language description of what it computes}
- **Inputs:** {which cells/fields it reads from}
- **Output:** {what value it returns}
- **Edge cases:** {what happens when inputs are empty, zero, or negative}

...
```

Cover every non-trivial formula. Trivial formulas (e.g. `=A1+B1` as a one-off) can be grouped under a brief note.

### Step 4 — Write style-guide

Write `products/{slug}/docs/style-guide.json` from poc-brief `style`, updated to reflect any adjustments made during the build:

```json
{
  "product_slug": "{slug}",
  "product_type": "{product_type}",
  "palette": {
    "primary": "#1A1A2E",
    "accent": "#E94560",
    "background": "#F5F5F5",
    "notes": "Primary used for headers and key labels. Accent for highlights and CTA elements. Background for page/tab backgrounds."
  },
  "typography": {
    "heading_font": "Inter",
    "body_font": "Inter",
    "heading_weight": "Bold",
    "body_weight": "Regular",
    "notes": ""
  },
  "layout": {
    "style": "clean minimal",
    "row_height": "28px (data rows), 32px (section headers)",
    "margins": "40px page margins",
    "notes": ""
  }
}
```

### Step 5 — Generate test plan

Run `pipeline/04-build/skills/test-plan.md` with:
- `product_type`
- `formula_spec_path` — `products/{slug}/docs/formula-spec.md` (or null for Canva)
- `style_guide_path` — `products/{slug}/docs/style-guide.json` (written in Step 4)
- `differentiation` — from poc-brief
- `gaps` — from poc-brief
- `buyer_flow` — from poc-brief
- `structure` — from poc-brief

Output: `products/{slug}/docs/test-plan.json`

### Step 6 — Run all tests

**Run every applicable test in `test-plan.json` against the built product. Skip any test whose `applies_to` value doesn't match `product_type` (e.g. skip `sheets-notion` tests for a Canva product).**

For each applicable test:
1. **Copy** — make a fresh test copy of the product, named `[test-{id}] {slug}`. See `pipeline/workspace-setup.md` for platform-specific copy steps.
2. **Test** — follow the test's `steps` exactly on the copy. See `pipeline/workspace-setup.md` test execution table for how to run tests per platform.
3. **Record** — write the result: `pass` or `fail`, with actual outcome observed.
4. **Delete** — move the test copy to trash. Confirm deleted before continuing.

After running all tests:
- If any test fails: fix the failure in the production product, re-run only the failed tests, repeat until all pass.
- Do not proceed to Step 7 until every test in `test-plan.json` shows `pass`.

Update `test-plan.json` with results:
```json
{
  "tests": [
    {
      "id": "logic_01",
      ...
      "result": "pass",
      "actual": "Total Income showed 2450 as expected"
    }
  ],
  "run_summary": {
    "total": 12,
    "passed": 12,
    "failed": 0,
    "run_date": "{ISO date}"
  }
}
```

### Step 7 — Write setup guide

Run `pipeline/04-build/skills/setup-guide.md` with:
- `product_type`
- `product_name` — from keyword or confirmed product title
- `feature_spec` — from poc-brief
- `buyer_flow` — from poc-brief
- `buyer_complaints` — aggregated buyer complaints from Step 1
- `structure` — actual structure from poc-brief
- `working_link`

Output: `products/{slug}/docs/setup-guide.md`

### Step 8 — Delivery prep

Run `pipeline/04-build/skills/delivery-prep.md` with:
- `product_type`
- `delivery_format` — from poc-brief
- `working_link`
- `slug`
- `product_name`

Output: `products/{slug}/delivery/delivery.json` + any download files.

### Step 9 — Final visual pass

Run the visual review for `product_type` — see `pipeline/workspace-setup.md` visual review table.

For Canva: save all page exports to `products/{slug}/screenshots/`.
For Google Sheets: verify the XLSX exists at `products/{slug}/delivery/{slug}.xlsx` before asking the human.

If any issue is found: fix it in the production product and re-check that page. Do not proceed until the product is visually complete.

### Step 10 — Update product.json

Update `products/{slug}/product.json`:

```json
{
  "slug": "{slug}",
  "product_type": "{product_type}",
  "keyword": "{keyword}",
  "pipeline_status": {
    "stage": "04-build",
    "status": "complete",
    "poc_brief": "pipeline/03-poc/output/{slug}-poc-brief.json",
    "test_results": "products/{slug}/docs/test-plan.json",
    "delivery": "products/{slug}/delivery/delivery.json"
  },
  "docs": {
    "formula_spec": "products/{slug}/docs/formula-spec.md",
    "test_plan": "products/{slug}/docs/test-plan.json",
    "style_guide": "products/{slug}/docs/style-guide.json",
    "setup_guide": "products/{slug}/docs/setup-guide.md"
  },
  // Note: set formula_spec to null for Canva (no formulas — Step 3 is skipped)
  "screenshots": "products/{slug}/screenshots/",
  "delivery_link": "{primary_link from delivery.json}"
}
```

---

## Product docs summary

All written to `products/{slug}/docs/`:

| File | Written in step | Purpose |
|------|----------------|---------|
| `formula-spec.md` | Step 3 | Every formula documented (Sheets/Notion only) |
| `style-guide.json` | Step 4 | Confirmed palette/font/layout (used by Stage 06 Marketing) |
| `test-plan.json` | Step 5 + 6 | Tests written + results recorded |
| `setup-guide.md` | Step 7 | Buyer-facing setup instructions |

---

## Cleanup

After Step 10, run Playwright cleanup:

```bash
find .playwright-mcp -delete
```

---

## Notes

- The self-test loop in Step 6 is not optional — Stage 05 is independent verification, not a debugging session. Hand off a clean product.
- Never skip the copy→test→delete pattern in Step 6. Test on a copy, not the production file.
- If Step 6 reveals a systemic issue (not just one failing test): stop, fix the root cause in Step 2, re-run the full test suite.
- `buyer_complaints` is aggregated in Step 1 across all competitors — deduplication is fine (same complaint appearing in multiple competitors = one entry).

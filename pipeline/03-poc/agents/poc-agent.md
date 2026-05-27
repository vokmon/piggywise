# poc-agent

Orchestrates Stage 03: study what works, harvest patterns from multiple templates, build a rough prototype from scratch, and produce `{slug}-poc-brief.json` as the handoff to Stage 04. Internal checkpoint only — not shown to buyers.

Output is saved to `output/{slug}/03-poc/`.

---

## Parameters

Defined here and passed explicitly to every skill — never hardcoded in the skill itself:

- `validate_output` — path to the Stage 02 validate output file (e.g. `output/kids-budget-planner/02-validate/kids-budget-planner-validate-output.json`)
- `max_competitors`: **5** — number of top-ranked competitors to deeply reverse-engineer
- `max_templates`: **5** — number of template candidates to study for pattern harvesting

---

## Working folders

See `pipeline/workspace-setup.md` for folder paths, file naming conventions, platform-specific file operations, and one-time setup instructions.

---

## Steps

### Step 1 — Load validate output

Read `validate_output`.

Check `decision.verdict`. If not `"go"`: stop and ask the human whether to proceed anyway.

Extract:

- `keyword` — `decision.recommended_title_keyword`
- `slug` — derive from `keyword`: lowercase, spaces to hyphens, remove special characters (e.g. `"Simple ADHD Notion Planner"` → `"simple-adhd-notion-planner"`)
- `competitor_urls` — `review_miner.listings_mined[].listing_url` (take top `max_competitors` by order)
- `buyer_complaints` — `review_miner.top_complained`
- `buyer_wishes` — `review_miner.top_praised`
- `unmet_needs` — `review_miner.unmet_needs`
- `pricing` — from `price_check.recommendations`: `{ launch_price, target_price }`

### Step 2 — Confirm product type

Infer `product_type` from the validate output context (keyword, competitor listings, product category). If it cannot be inferred, ask the user directly.

Present to human:

> "Based on the validate output, this looks like a **{product_type}** product (keyword: `{keyword}`). Is this correct, or should I use a different product type?"
> _(Hint: supported types are listed in `skills/study/reverse-engineer.md` routing table.)_

Wait for confirmation.

### Step 3 — Reverse-engineer competitors

Run `skills/study/reverse-engineer.md` with:

- `product_type`
- `competitor_urls` (top `max_competitors` from Step 1)
- `max_competitors`
- `keyword`

The type-specific skill handles source coverage — see `skills/study/reverse-engineer.md` routing table. For Canva and Notion this includes a workspace copy (study → delete); for Google Sheets it is Etsy-only with no workspace copy.

For Canva and Notion: all study copies are placed in the **Study folder** (see `pipeline/workspace-setup.md`), named `[study] {original title}`, and deleted by the skill before returning — the Study folder should be empty when this step completes.

Output populates `competitors[]` in the poc-brief.

### Step 4 — Harvest template patterns

Run `skills/study/template-hunt.md` with:

- `product_type`
- `feature_spec: null` — feature_spec is not yet known; search by keyword
- `max_templates`
- `keyword`

**Note:** feature_spec is null at this stage — synthesis happens in Step 6. Template-hunt studies multiple templates by keyword and extracts the best structural/UX patterns from each. Do NOT copy any single template — the goal is a pattern library to inform a fresh build.

Output populates `template_patterns[]` in the poc-brief.

### Step 5 — Collect visual inspiration

Run `skills/study/design-swipe.md` with:

- `product_type`
- `keyword`
- `style_signals` — preliminary visual observations from Step 3 competitors

Output populates `visual_inspiration` in the poc-brief.

### Step 6 — Synthesise

Using the data from Steps 3–5, synthesise the following. Reviews from Step 3 are the primary driver of what gets built.

**`feature_spec`** — what to build:

- Start from `buyer_wishes` and `unmet_needs` from validate output
- Add features that would directly address `buyer_complaints` from competitors
- Include features consistently present in competitors that buyers praise
- If buyers consistently ask for something no competitor has → include it as a differentiator

**`differentiation`** — specific things we do better than every competitor:

- Derived from the gap between `buyer_complaints` and `buyer_wishes`
- Each item must be a concrete, deliverable thing — not a vague goal
- Stage 04 treats this as a build checklist — if it's in differentiation, it must exist in the finished product

**`gaps`** — features deferred from this POC:

- Features buyers want that are too complex or out of scope for this iteration
- Features that need more data before implementing correctly
- Stage 04 fills these after every `differentiation[]` item is delivered

**`delivery_format`** — based on `product_type` and competitor patterns. See `pipeline/workspace-setup.md` delivery formats table.

**`style`** — confirmed palette/font/layout before building:

- Combine competitor visual styles (from Step 3) + design-swipe inspiration (from Step 5)
- Identify any clear differentiating visual direction (e.g. dark mode when competitors are all light)
- Confirm: `palette` (3 hex codes), `font`, `layout_style`

**`structure` (planned)** — planned tab/page/frame layout based on `feature_spec`. Use the shape from `pipeline/workspace-setup.md` schema shapes table. This is a blueprint for Step 7 — the actual built structure is recorded in Step 9.

### Step 7 — Build rough POC

**For Canva and Notion only** (skip steps 1–2 for Google Sheets — the build skill creates the file):

1. Create a new blank file in the **POC folder**, named `[poc] {keyword}`. See `pipeline/workspace-setup.md` for platform-specific create steps. Always start from a blank file — do not copy any template.

2. Run `skills/build/{product_type}.md` with:
   - `working_link` — the link to the new blank file (Canva/Notion); `null` for Google Sheets
   - `feature_spec` — from Step 6
   - `structure` — planned structure from Step 6
   - `style` — from Step 6
   - `differentiation` — from Step 6
   - `gaps` — from Step 6
   - `known_issues: []` — empty at start of build
   - `depth: "rough"`
   - `slug` — from Step 1 (Google Sheets only — required for file naming)
   - `keyword` — from Step 1 (Google Sheets only — required for Drive file naming)

3. As issues are discovered during the build, add them to `known_issues`.

### Step 8 — Visual check

Run the visual review for `product_type` — see `pipeline/workspace-setup.md` visual review table.

- For Canva: save all page exports to `output/{slug}/03-poc/screenshots/`.
- Review each output. Add any visual issues discovered to `known_issues`.

### Step 9 — Write actual structure and logic_map

Based on what was actually built (not the plan from Step 6):

**`structure`** — the actual tab/page/frame layout. See `pipeline/workspace-setup.md` schema shapes table for the correct shape per product type.

**`logic_map`** — the actual formulas/logic built. See `pipeline/workspace-setup.md` schema shapes table for the correct shape per product type.

### Step 10 — Write buyer_flow

Write the step-by-step flow of how a buyer would use the built POC. Be concrete — reference actual tab/page names built in Step 7.

Example:

```
1. Open the Instructions tab and follow setup steps
2. Enter income entries in the Income tab (date, amount, category)
3. Enter expenses in the Expenses tab
4. View monthly totals on the Dashboard tab
```

### Step 11 — Refine style

Review the visual output from Step 8. If the built result revealed any adjustments to the style (e.g. a palette colour doesn't render well on screen, a font isn't available), update `style` to reflect what was actually used.

### Step 12 — Write poc-brief.json

Compile all fields into `output/{slug}/03-poc/{slug}-poc-brief.json`:

```json
{
  "slug": "{slug}",
  "product_type": "{product_type}",
  "keyword": "{keyword}",
  "feature_spec": [],
  "structure": {},
  "logic_map": {},
  "_schema_notes": {
    "structure": "shape varies by product_type — tabs[] for Sheets; pages/databases[] for Notion; pages/frames[] for Canva",
    "logic_map": "Sheets: key_formulas[]; Notion: formula_properties[] + rollups[]; Canva: omit (no logic)"
  },
  "competitors": [],
  "visual_inspiration": {},
  "differentiation": [],
  "style": {},
  "buyer_flow": [],
  "pricing": {},
  "delivery_format": "",
  "template_patterns": [],
  "gaps": [],
  "known_issues": [],
  "poc_result": {
    "type": "{product_type}",
    "link": "",
    "screenshots": [],
    "notes": ""
  },
  "build_instructions": "Start from the poc_result link. Fix known_issues first. Polish feature_spec[] to full quality (clean formulas, error handling, buyer UX). Verify every differentiation[] item exists — treat as a checklist. Fill gaps[]. Polish style to match confirmed palette."
}
```

### Step 13 — Present to human

Present a summary of the POC:

- Product type and keyword
- Top 3 items in `feature_spec`
- Top 3 items in `differentiation`
- Key `known_issues` (if any)
- Visual outputs from Step 8 (Canva PNG exports; for other types, describe what was reviewed)
- The `poc_result.link` so the human can open it

Ask:

> "POC is ready. **Commit** to proceed to Stage 04 (build), or **abandon** to discard?"

Wait for the human's decision.

### Step 14 — Commit

If the human chooses **commit**:

1. Create `products/{slug}/` directory.
2. Write `products/{slug}/product.json`:
   ```json
   {
     "slug": "{slug}",
     "product_type": "{product_type}",
     "keyword": "{keyword}",
     "pipeline_status": {
       "stage": "03-poc",
       "status": "complete",
       "poc_brief": "output/{slug}/03-poc/{slug}-poc-brief.json"
     }
   }
   ```
3. Create a row in the **POC database** (`PiggyWise › POC`) with:
   - `slug` — `{slug}`
   - `product_type` — `{product_type}`
   - `status` — `committed`
   - `poc_page` — link to the `[poc] {keyword}` page in the POC folder
4. Confirm to human: "Committed. Proceed to Stage 04 with `output/{slug}/03-poc/{slug}-poc-brief.json`."

### Step 15 — Abandon

If the human chooses **abandon**:

1. Delete the POC from the **POC folder**. See `pipeline/workspace-setup.md` for platform-specific delete steps.
2. Delete `output/{slug}/03-poc/{slug}-poc-brief.json` and `output/{slug}/03-poc/screenshots/`.
3. Confirm to human: "Abandoned. All POC artefacts removed."

---

## Cleanup

After all steps complete (commit or abandon), run Playwright cleanup:

```bash
find .playwright-mcp -delete
```

---

## Notes

- Steps 3–5 are study only — no building yet. All copies made in Step 3 are deleted before Step 6.
- The POC is always built from a blank file (Step 7) — never from a copied template. `template_patterns[]` from Step 4 inform what to build, not what to clone.
- `structure` in poc-brief has two forms: the **planned** structure (end of Step 6, used as blueprint) and the **actual** structure (Step 9, recorded from what was built). Step 12 writes the actual structure.
- Do not skip `product_type` confirmation in Step 2 — all downstream skills depend on it.

# build-agent

Orchestrates Stage 03: study competitors, reverse-engineer what works, build the product. Output is the finished product link and `{slug}-brief.json`, handed off to Stage 04 review.

Output saved to `output/{slug}/03-build/`.

---

## Parameters

- `validate_output` — path to the Stage 02 validate output file (e.g. `output/notion-freelancer-crm-template/02-validate/notion-freelancer-crm-template-validate-output.json`)
- `max_competitors`: **5** — competitors to reverse-engineer
- `max_templates`: **5** — templates to study for pattern harvesting

---

## Steps

### Step 1 — Load validate output

Read `validate_output`. If `decision.verdict` is not `"go"`, stop and ask the human whether to proceed anyway.

Extract:
- `keyword` — `decision.recommended_title_keyword`
- `slug` — from keyword: lowercase, spaces to hyphens, no special characters
- `competitor_urls` — `review_miner.listings_mined[].listing_url` (top `max_competitors`)
- `buyer_complaints` — `review_miner.top_complained`
- `buyer_wishes` — `review_miner.top_praised`
- `unmet_needs` — `review_miner.unmet_needs`
- `pricing` — `price_check.recommendations`: `{ launch_price, target_price }`

### Step 2 — Confirm product type

Infer `product_type` from validate output context. If unclear, ask the human.

> "This looks like a **{product_type}** product (keyword: `{keyword}`). Correct?"

Wait for confirmation before continuing.

### Step 3 — Reverse-engineer competitors

Run `pipeline/03-build/skills/study/reverse-engineer.md` with `product_type`, `competitor_urls`, `max_competitors`, `keyword`.

Study copies (Notion/Canva) go in the **Study folder**, named `[study] {title}`, and are deleted before this step returns. Study folder is empty when done.

Output populates `competitors[]` in the brief.

### Step 4 — Harvest template patterns

Run `pipeline/03-build/skills/study/template-hunt.md` with `product_type`, `max_templates`, `keyword`.

Study multiple templates for structural and UX patterns. Do not copy any single template — the goal is a pattern library to inform a build from scratch.

Output populates `template_patterns[]` in the brief.

### Step 5 — Collect visual inspiration

Run `pipeline/03-build/skills/study/design-swipe.md` with `product_type`, `keyword`, and visual observations from Step 3.

Output populates `visual_inspiration` in the brief.

### Step 6 — Synthesise

Using Steps 3–5 data, derive:

- **`feature_spec`** — what to build: buyer wishes + unmet needs + things buyers consistently praise in competitors
- **`differentiation`** — concrete things we do better: gaps between buyer complaints and buyer wishes
- **`style`** — confirmed palette (3 hex), font, layout style — combine competitor styles + design-swipe findings
- **`structure`** — planned tab/page/frame layout based on `feature_spec`
- **`delivery_format`** — from `pipeline/workspace-setup.md` delivery formats table

### Step 7 — Build

Create a new blank file in the **POC folder**, named `[poc] {keyword}` (see `pipeline/workspace-setup.md` for platform-specific steps). Always start from blank — never copy a template.

Run `pipeline/03-build/skills/build/{product_type}.md` with:
- `working_link` — link to the new blank file (Notion/Canva); `null` for Google Sheets
- `feature_spec`, `structure`, `style`, `differentiation` — from Step 6
- `known_issues: []`
- `slug`, `keyword` — for Google Sheets file naming

Record any issues discovered during the build in `known_issues`.

### Step 8 — Write actual structure and logic_map

Document what was actually built (may differ from the plan in Step 6):
- **`structure`** — actual tab/page/frame layout
- **`logic_map`** — actual formulas, relations, rollups (Sheets/Notion only; null for Canva)

### Step 9 — Write brief

Write `output/{slug}/03-build/{slug}-brief.json`:

```json
{
  "slug": "",
  "product_type": "",
  "keyword": "",
  "feature_spec": [],
  "differentiation": [],
  "structure": {},
  "logic_map": {},
  "style": {},
  "delivery_format": "",
  "competitors": [],
  "template_patterns": [],
  "visual_inspiration": {},
  "known_issues": [],
  "pricing": { "launch_price": 0, "target_price": 0 },
  "product_link": ""
}
```

### Step 10 — Present and confirm

Show the human:
- Product type and keyword
- Top 3 `feature_spec` items
- Top 3 `differentiation` items
- `known_issues` (if any)
- `product_link` to open it

> "Product is built. **Commit** to move to review, or **discard** to remove?"

**Commit** → create `products/{slug}/` and write `products/{slug}/product.json`:

```json
{
  "slug": "",
  "product_type": "",
  "keyword": "",
  "pipeline_status": {
    "stage": "03-build",
    "status": "complete",
    "brief": "output/{slug}/03-build/{slug}-brief.json"
  }
}
```

Then create a row in the **POC database** (`PiggyWise › POC`): `slug`, `product_type`, `status: committed`, `poc_page` = product link.

**Discard** → delete the product from the POC folder, delete `output/{slug}/03-build/`, confirm removed.

---

## Cleanup

```bash
find .playwright-mcp -delete
```

---

## Notes

- Build always starts from a blank file — `template_patterns[]` informs what to build, not what to clone.
- Visual check is done by the human after this stage.
- `known_issues` carries forward to Stage 04 review.

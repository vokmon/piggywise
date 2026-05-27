# PiggyWise Pipeline Master Plan

End-to-end system for finding, building, and launching digital products (Google Sheets templates and similar) on Etsy.

**Strategy:** Build products people are already searching for — not invent and hope.

---

## Pipeline Design Rules

These rules apply to every agent and skill across all stages:

- **No hardcoded thresholds.** Every threshold, limit, or cutoff must be derived from pipeline inputs or upstream output data — never a fixed number written into the skill itself.
- **No magic numbers.** If a constant is needed (e.g. `max_reviews_per_listing = 20`), it must be defined and explained in the agent that owns the stage, then passed explicitly to skills as a named parameter.
- **All inputs flow from upstream.** Skills receive their inputs from the agent that calls them. Skills never re-read upstream output files directly.
- **All field references must match the actual output schema.** When a skill or agent references a field from another stage's output (e.g. `etsy_scan.competition_level`), the field name must exactly match what that stage actually writes — verify against the real output file, not assumptions.
- **No currency conversion in skills.** If prices need normalizing, the user handles it. Skills receive prices as-is and work with whatever unit they're given.

---

## How It Works

```
00-discover → 01-research → 02-validate → 03-poc → [human: commit?] → 04-build → 05-qa → 06-marketing → 07-launch → 08-iterate
```

- Stages 00–03: pipeline work, outputs saved to `output/_discover/` (Stage 00) or `output/{slug}/{stage}/` (Stages 01–03) — all gitignored
- Stages 04–07: product work, all assets saved to `products/{slug}/`
- `product.json` inside each product folder tracks pipeline state across stages 04–08
- `/status "product-slug"` prints current stage at any time
- `product_type` is determined at the start of Stage 03 — the agent infers it from validate output and suggests; human confirms or overrides. Can be changed by re-running `/poc "slug"` with a different type.
- `pipeline/workspace-setup.md` — shared reference for all agents: working folder paths (Study/POC/Products per platform), file naming conventions, file operations (copy/create/move/delete per platform), delivery formats per product type, schema shapes per product type, new product type checklist. All agents reference this file instead of repeating per-type steps inline.

---

## Stage Overview

| Stage        | Invoke              | Purpose                                                    | Gate         |
| ------------ | ------------------- | ---------------------------------------------------------- | ------------ |
| 05-marketing | `/marketing "slug"` | Cover image, mockups, video, title, description, tags      | —            |
| 06-launch    | `/launch "slug"`    | Set price, create Etsy listing, publish                    | —            |
| 07-iterate   | `/iterate "slug"`   | Monitor ranking/reviews/conversions, suggest optimizations | Ongoing loop |
| status       | `/status "slug"`    | Show current pipeline state for any product                | —            |

---

## Product State (product.json)

Each product under `products/{slug}/` has a `product.json` tracking pipeline progress:

```json
{
  "slug": "budget-tracker-freelancer",
  "name": "...",
  "pipeline": {
    "current_stage": "05-qa",
    "stages": {
      "04-build": { "status": "completed", "completed_at": "..." },
      "05-qa": { "status": "in-progress", "started_at": "..." },
      "06-marketing": { "status": "pending" },
      "07-launch": { "status": "pending" },
      "08-iterate": { "status": "pending" }
    }
  },
  "product_type": "google-sheets",
  "research_ref": "output/{slug}/01-research/...",
  "validate_ref": "output/{slug}/02-validate/...",
  "poc_ref": "output/{slug}/03-poc/{slug}-poc-brief.json",
  "pricing": {},
  "delivery": {},
  "etsy": {}
}
```

---

## Product Folder Structure

```
products/{slug}/
  product.json              ← pipeline state tracker
  docs/
    formula-spec.md         ← [created: Build] what each formula/logic does, inputs/outputs — Sheets/Notion only
    test-plan.json          ← [created: Build, consumed: QA] test cases with inputs and expected outputs
    style-guide.json        ← [created: Build, consumed: Build + Marketing] palette, fonts, spacing
    setup-guide.md          ← [created: Build, consumed: delivery] buyer instructions for using the product
  screenshots/              ← [created: Build] full visual pass of finished product — fed into Marketing mockups
  qa/
    screenshots/            ← [created: QA] buyer simulation screenshots
    results.json            ← [created: QA] pass/fail per check with screenshot refs — gates marketing
  marketing/                ← [created: Marketing] cover image, mockups, listing.json, videos
  delivery/                 ← [created: Build] final files prepared for buyer download
  iterate-log.json          ← [created/appended: Iterate] performance metrics and optimization history
```

**Build/QA use product-specific docs** — every product has different formulas, test cases, and style, so these must be written per product during Stage 04 and consumed by Stage 05.

**Marketing/Launch/Iterate use generic skills** — same process for every product, fed with product data from upstream. No product-specific instruction docs needed.

## Stage 05 — Marketing (pipeline/06-marketing/)

Create everything needed for the Etsy listing. Cover that makes people click. Generic process — same steps for every product, fed with product-specific data from upstream.

**Stage structure:**

```
pipeline/06-marketing/
  agents/
    marketing-agent.md
  skills/
    cover-brief.md           ← research competitor covers, write visual brief
    mockup-generator.md      ← generate 3–5 preview images from screenshots
```

**Shared skills used:**

- `skills/etsy-listing.md` — Title, description, 13 tags (grounded in validate keyword data)
- `skills/etsy-cover-image.md` — Cover format constraints (2000×1500px, safe zone)
- `skills/canva-design.md` — Create cover using style-guide.json (primary)
- `skills/generate-image.md` — Fallback if Canva output isn't strong
- `skills/generate-video.md` — Demo slideshow video (5–15 sec)
- `skills/record-video.md` — Screen-recorded walkthrough/tutorial video
- `skills/playwright.md` — Research competitor covers

**Inputs from upstream:**

- `products/{slug}/docs/style-guide.json` → palette, fonts for visual consistency
- `products/{slug}/screenshots/` → source material for mockups (from Build)
- `output/{slug}/02-validate/` → best title keyword, buyer language for listing copy
- `poc-brief.json` → `differentiation` and `feature_spec` for listing description

**Agent flow:**

1. Read `product.json`, `style-guide.json`, validate output, poc-brief
2. Run `cover-brief.md` → research competitor covers via Playwright, write visual brief
3. Run `canva-design.md` with style-guide + cover brief → create cover image
4. Run `mockup-generator.md` → generate 3–5 preview images from `products/{slug}/screenshots/`
5. Run `etsy-listing.md` → write title, description, 13 tags using validate keyword + poc-brief differentiation
6. Run `generate-video.md` → create demo slideshow from screenshots
7. Run `record-video.md` → screen-record product walkthrough tutorial
8. Save all assets to `products/{slug}/marketing/`
9. Update `product.json` pipeline status

**Agent:**

- [ ] `agents/marketing-agent.md` — Orchestrates all steps above, saves all assets to `products/{slug}/marketing/`

---

## Stage 06 — Launch (pipeline/07-launch/)

Assemble everything from upstream and publish the Etsy listing. Generic process — same steps for every product.

**Stage structure:**

```
pipeline/07-launch/
  agents/
    launch-agent.md
  skills/
    listing-creator.md       ← assemble + publish listing via Etsy MCP
```

**Shared skills used:** none — pure MCP operations

**Credentials:**

- `ETSY_KEYSTRING` + `ETSY_SECRETSTRING` — Etsy shop management API credentials for creating and publishing the listing via `mcp__etsy__*`

**Inputs from upstream:**

- `products/{slug}/marketing/` → cover image, mockups, videos, listing copy
- `products/{slug}/delivery/` → product files to upload for buyer download
- `product.json` → pricing (from poc-brief), slug, product_type

**Agent flow:**

1. Read `product.json` → slug, pricing, product_type
2. Read `products/{slug}/marketing/` → cover, mockups, videos, title, description, tags
3. Read `products/{slug}/delivery/` → delivery files
4. Run `listing-creator.md`:
   a. Upload delivery files via Etsy MCP
   b. Upload cover + mockup images
   c. Upload videos
   d. Set price from `poc-brief.json` pricing
   e. Create and publish listing via `mcp__etsy__*`
5. Save Etsy listing URL to `product.json`
6. Update `product.json` status to launched

**Agent:**

- [ ] `agents/launch-agent.md` — Orchestrates all steps above, saves listing URL to `product.json`

---

## Stage 07 — Iterate (pipeline/08-iterate/)

Ongoing optimization after launch. Run periodically — not a one-time step. Generic process — same for every product, fed with product-specific Etsy data.

**Stage structure:**

```
pipeline/08-iterate/
  agents/
    iterate-agent.md
  skills/
    performance-check.md     ← scrape Etsy shop: views, favorites, sales, reviews
    suggest-optimizations.md ← compare vs current top performers, recommend changes
```

**Shared skills used:**

- `skills/playwright.md` — search Etsy for current top performers (competitive analysis only)

**Inputs from upstream:**

- `product.json` → Etsy listing ID, slug, keyword
- `output/{slug}/02-validate/` → original keyword for competitive search
- `products/{slug}/iterate-log.json` → previous performance history for trend comparison

**Credentials:**

- `ETSY_KEYSTRING` + `ETSY_SECRETSTRING` — Etsy shop management API credentials. Use for all reads/writes on our own shop: listing stats, sales, reviews, listing updates. Cannot access other shops.

**Agent flow:**

1. Read `product.json` → Etsy listing ID, keyword
2. Run `performance-check.md` → fetch our listing stats via Etsy API (`ETSY_KEYSTRING` + `ETSY_SECRETSTRING`): views, favorites, sales, review score, recent review text
3. Run `suggest-optimizations.md`:
   a. Use Playwright to search Etsy for current top performers on the same keyword (public search)
   b. Compare our title/tags/cover/price against theirs
   c. Mine new reviews from step 2 for complaints and praise
   d. Recommend specific changes: listing (title, tags, cover, price) or product (feature/fix)
4. Append results + recommendations to `products/{slug}/iterate-log.json`
5. Present to human — human decides which changes to action

**Agent:**

- [ ] `agents/iterate-agent.md` — Orchestrates all steps above, appends to `products/{slug}/iterate-log.json`

---

## Infrastructure

- [ ] `agents/status-agent.md` — `/status "slug"` reads `product.json`, prints readable pipeline dashboard
- [ ] All `pipeline/*/output/` folders added to .gitignore (00 through 03)
- [ ] Large files in `products/` added to .gitignore: `products/*/screenshots/`, `products/*/qa/screenshots/`, `products/*/marketing/`, `products/*/delivery/`
- [ ] `products/` folder structure documented in README

---

## Progress

- Stage 05 — Marketing: not started
- Stage 06 — Launch: not started
- Stage 07 — Iterate: not started
- Infrastructure: not started

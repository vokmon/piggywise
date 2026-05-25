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

- Stages 00–03: pipeline work, outputs saved to `pipeline/{stage}/output/` (gitignored)
- Stages 04–08: product work, all assets saved to `products/{slug}/`
- `product.json` inside each product folder tracks pipeline state across stages 04–08
- `/status "product-slug"` prints current stage at any time
- `product_type` is determined at the start of Stage 03 — the agent infers it from validate output and suggests; human confirms or overrides. Can be changed by re-running `/poc "slug"` with a different type.
- `pipeline/workspace-setup.md` — shared reference for all agents: working folder paths (Study/POC/Products per platform), file naming conventions, file operations (copy/create/move/delete per platform), delivery formats per product type, schema shapes per product type, new product type checklist. All agents reference this file instead of repeating per-type steps inline.

---

## Stage Overview

| Stage | Invoke | Purpose | Gate |
|---|---|---|---|
| 00-discover | `/discover` | Broad scan of Etsy digital downloads — surface 10–15 seed candidates | Human: pick 3–5 seeds |
| 01-research | `/research "seed"` | Find opportunity — Etsy demand, Google Trends, gap analysis | 3 auto-gates |
| 02-validate | `/validate "slug"` | Confirm demand, pricing ceiling, buyer sentiment | Human: go / no-go |
| 03-poc | `/poc "slug"` | Study top sellers, build rough prototype | Human: commit / abandon |
| 04-build | `/build "slug"` | Polished product + buyer materials + delivery format | — |
| 05-qa | `/qa "slug"` | Formula checks, edge cases, buyer experience | Must pass before marketing |
| 06-marketing | `/marketing "slug"` | Cover image, mockups, video, title, description, tags | — |
| 07-launch | `/launch "slug"` | Set price, create Etsy listing, publish | — |
| 08-iterate | `/iterate "slug"` | Monitor ranking/reviews/conversions, suggest optimizations | Ongoing loop |
| status | `/status "slug"` | Show current pipeline state for any product | — |

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
      "04-build":     { "status": "completed", "completed_at": "..." },
      "05-qa":        { "status": "in-progress", "started_at": "..." },
      "06-marketing": { "status": "pending" },
      "07-launch":    { "status": "pending" },
      "08-iterate":   { "status": "pending" }
    }
  },
  "product_type": "google-sheets",
  "research_ref": "pipeline/01-research/output/...",
  "validate_ref": "pipeline/02-validate/output/...",
  "poc_ref": "pipeline/03-poc/output/{slug}-poc-brief.json",
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

---

## Shared Skills (skills/)

These are reused across multiple stages.

**General:**
- [x] `skills/playwright.md` — Playwright browser rules: screenshot vs snapshot, block handling, cleanup
- [x] `skills/record-video.md` — Record browser session as `.webm` via `playwright-recorder` MCP server
- [x] `skills/etsy-listing.md` — SEO title, description, 13 tags, listing JSON for Etsy API
- [x] `skills/etsy-cover-image.md` — Cover image specs: 2000×1500px, safe zone, design checklist
- [x] `skills/canva-design.md` — Canva MCP tools for design creation and export
- [x] `skills/generate-image.md` — `echo "..." | codex exec` image generation (fallback)
- [x] `skills/generate-video.md` — ffmpeg slideshow MP4 for Etsy product video
- [x] `skills/pinterest-lookup.md` — Pinterest login + navigation

**Study (skills/study/) — used by Stage 03:**

Study sources per product type (used by both `reverse-engineer` and `template-hunt`):
- **Google Sheets** — Etsy listing page · Google Sheets template gallery · Vertex42 · Smartsheet free templates · Pinterest
- **Notion** — Etsy listing page · notion.so/templates · NotionPages.com · Pinterest
- **Canva** — Etsy listing page · canva.com/templates · Pinterest · Behance · Dribbble

`reverse-engineer` and `template-hunt` share the same sources but have different goals:
- **reverse-engineer**: study multiple products deeply — Etsy listing for sentiment + surface visual; free template galleries for actual structure + logic/formulas
- **template-hunt**: find ONE free template to copy as a starting scaffold to build from

- [x] `skills/study/template-hunt.md` — router: delegates to type-specific skill. Evaluates up to `max_templates` candidates, picks best scaffold candidate. Does NOT copy — records the choice only. Returns `null` if no suitable template.
- [x] `skills/study/template-hunt/notion.md` — Search notion.so/templates + NotionPages.com, evaluate candidates, pick best one
- [x] `skills/study/template-hunt/google-sheets.md` — Search Google Sheets gallery + Vertex42 + Smartsheet, evaluate candidates, pick best one
- [x] `skills/study/template-hunt/canva.md` — Search canva.com/templates + Pinterest + Behance, evaluate candidates, pick best one
- [x] `skills/study/design-swipe.md` — router: delegates to type-specific skill. Collects broader visual inspiration beyond direct competitors.
- [x] `skills/study/design-swipe/notion.md` — Sources: Pinterest (Notion aesthetic boards) + NotionPages.com. Collect: page layouts, database views, icons, cover images, property styling
- [x] `skills/study/design-swipe/google-sheets.md` — Sources: Pinterest (spreadsheet/finance/budget boards) + Vertex42 + Smartsheet. Collect: cell styling, color schemes, chart styles, tab layouts
- [x] `skills/study/design-swipe/canva.md` — Sources: Pinterest + Behance + Dribbble. Collect: design aesthetic, typography, illustration style, frame layout
- [x] `skills/study/reverse-engineer.md` — router: delegates to type-specific skill. Two-source study per competitor: (1) Etsy listing for buyer sentiment; (2) free template from type-specific galleries for actual structure + logic.
- [x] `skills/study/reverse-engineer/notion.md` — Etsy listing → reviews, preview images, feature list; notion.so/templates + NotionPages.com → actual structure, database schema, formulas, views; Pinterest → visual style. Study copies placed in Study folder, deleted before returning.
- [x] `skills/study/reverse-engineer/google-sheets.md` — Etsy listing → reviews, preview images, feature list; Google Sheets gallery + Vertex42 → actual tab structure, formulas, named ranges, charts; Pinterest → visual style. Study copies placed in Study folder, deleted before returning.
- [x] `skills/study/reverse-engineer/canva.md` — Etsy listing → reviews, preview images, feature list; canva.com/templates → actual layout, frames, element structure; Pinterest + Behance → visual style. No logic_map (visual-only product). Study copies placed in Study folder, deleted before returning.

**Build (skills/build/) — used by Stage 03 (rough) and Stage 04 (polished):**
- [x] `skills/build/notion.md` — duplicate + modify Notion template: pages, databases, views, formulas (uses `mcp__notion__*`). Accepts `depth: "rough" | "full"`.
- [x] `skills/build/google-sheets.md` — copy + modify Google Sheets: formulas, formatting, tabs (uses `mcp__claude_ai_Google_Drive__*`). Accepts `depth: "rough" | "full"`.
- [x] `skills/build/canva.md` — build product design in Canva (uses `mcp__canva__*`). Accepts `depth: "rough" | "full"`.

---

## Stage 00 — Discover (pipeline/00-discover/)

No seed needed — runs broad across all Etsy digital downloads. Goal: surface 10–15 candidate seeds ranked by signal strength. You pick 3–5 to run through Stage 01.

**Skills:**
- [x] `skills/etsy-bestsellers.md` — Scrape Etsy's bestselling digital downloads: extract product types, recurring themes, top categories
- [x] `skills/shop-scanner.md` — Study top 5–10 successful shops in the digital downloads / templates niche: what they sell, what their bestsellers are, shop sales volume
- [x] `skills/autocomplete-harvest.md` — Etsy autocomplete for broad terms ("google sheets", "notion template", "spreadsheet", "digital planner", "tracker"): collect all suggestions as raw seed candidates
- [x] `skills/google-signals.md` — Gemini CLI: broad trending categories in digital products / productivity tools space, rising search queries, growing vs declining niches
- [x] `skills/seed-ranker.md` — Synthesize all 4 sources, deduplicate, score each candidate (Etsy demand + Google momentum + competition + format fit), return ranked top 10–15

**Agent:**
- [x] `agents/discover-agent.md` — Orchestrates all 5 skills, saves output to `pipeline/00-discover/output/discover-{date}.json`, prints ranked seed table to conversation

---

## Stage 01 — Research (pipeline/01-research/)

**Skills:**
- [x] `skills/etsy-scan.md` — Playwright scrape: autocomplete, listings, top 3 bestsellers
- [x] `skills/google-trends.md` — Gemini CLI → Playwright → WebSearch fallback chain
- [x] `skills/pinterest-trends.md` — Pinterest early signal (optional, available: true/false)
- [x] `skills/gap-finder.md` — Synthesize signals, score ideas (max 9), ranked shortlist

**Agent:**
- [x] `agents/research-agent.md` — Orchestrates full Stage 1, 3 auto-gates, saves output JSON

---

## Stage 02 — Validate (pipeline/02-validate/)

Deeper Etsy search on the specific product idea. Confirms real buyer demand, price range, and keyword to use in title.

**Skills:**
- [x] `skills/etsy-deep-dive.md` — Targeted search for the specific product angle, confirms gap, finds best title keyword
- [x] `skills/review-miner.md` — Read reviews from closest competitors, extract buyer language, unmet needs, complaints
- [x] `skills/price-check.md` — Map price landscape, find sweet spot, recommend launch and target price

**Agent:**
- [x] `agents/validate-agent.md` — Reads 01-research output, orchestrates all 3 skills, outputs go/no-go with evidence

---

## Stage 03 — POC (pipeline/03-poc/)

Study what works on Etsy, find free templates, collect visual inspiration, then build a rough prototype. Internal checkpoint only — not shown to buyers. Output is `{slug}-poc-brief.json` which feeds Stage 04.

**No stage-specific skills** — all work is done by shared skills. The agent is the only stage-specific file.

**Stage structure:**
```
pipeline/03-poc/
  agents/
    poc-agent.md               ← orchestrates the whole stage
  output/                      ← gitignored
    {slug}-poc-brief.json      ← handoff to Stage 04
    {slug}-screenshots/        ← Playwright visual check screenshots
```

**Working folders** (all agents reference `pipeline/workspace-setup.md` for paths and platform-specific steps):
- **Study folder** — temporary study copies (`[study] {original title}`). Deleted by `reverse-engineer` before returning. Empty when Step 3 completes.
- **POC folder** — rough prototype (`[poc] {keyword}`). Copied from scaffold in Step 7 (or created blank). Survives until commit/abandon decision in Step 13.
- **Products folder** — final polished product (`{keyword}`, no prefix). Created by build-agent in Stage 04.

**Shared skills used:**

Study skills (all follow the pattern: general `.md` routes to `/{type}.md`):
- [x] `skills/study/reverse-engineer.md` → `/{type}.md` — Two-source study per competitor: (1) Etsy listing page → reviews, preview images, description (buyer sentiment + surface visual); (2) free equivalent from type-specific template galleries → actual structure, logic, formulas (deep internals). Feeds `competitors[]` in poc-brief — including `key_features`, `structure`, `logic_notes`, `buyer_complaints`, `buyer_wishes`, `visual_style`, `free_equivalent_urls` per competitor. Does NOT write the top-level `structure` or `logic_map` fields — those document our built POC, not competitors.
- [x] `skills/study/template-hunt.md` → `/{type}.md` — Search type-specific free template galleries (same sources as `reverse-engineer/{type}`), evaluate up to `max_templates` candidates, pick the best one as scaffold candidate (copying happens later in the build step). Do NOT copy yet — just record the choice. If no suitable template found, return `null` and note "build from scratch". Feeds `templates[]`.
- [x] `skills/study/design-swipe.md` → `/{type}.md` — Broader visual inspiration from Pinterest + type-specific design platforms beyond direct competitors. Feeds `visual_inspiration`.

`reverse-engineer` (competitor study: sentiment + internals) + `design-swipe` (broader visual trends) inform the synthesis step. Top-level `structure` and `logic_map` in poc-brief are written from the **actual built POC** in step 9, not from competitor study.

**Copy isolation rule (study phase):** Every template or free product opened for study must be copied into a temporary workspace first. Study the copy, record findings, then delete it. Never study the original. The only copy that survives is the scaffold copied at the start of the build step (step 7) — it becomes the POC being built.

Build skills (same skills used by Stage 04, but rough depth here):
- [x] `skills/build/{type}.md` — Build the rough prototype from the copied template (`depth: "rough"`)

Visual check:
- `skills/playwright.md` — After building, screenshot every tab/page/frame to confirm it renders correctly. Screenshots saved to `pipeline/03-poc/output/{slug}-screenshots/`.

**Agent parameters** (defined in `poc-agent.md`, passed explicitly to skills — never hardcoded in the skill itself):
- `max_competitors`: **3** — number of top-ranked competitors to deeply reverse-engineer (taken from validate output by rank)
- `max_templates`: **3** — number of template candidates to evaluate before picking the best one

**Agent flow:**
1. Read validate output → extract competitor URLs, buyer complaints, pricing, keyword
2. Confirm `product_type` — infer from validate output context (keyword, competitor listings, product category). If cannot infer, ask human directly. Hint: supported types listed in `skills/study/reverse-engineer.md` routing table. Wait for confirmation before proceeding.
3. Run `reverse-engineer/{type}` on top `max_competitors` competitor URLs from validate output → for each: (a) study Etsy listing for reviews, preview images, features; (b) find a free equivalent from type-specific template galleries, copy it to Study folder (`[study] {title}`), study actual structure + logic/formulas, then delete the copy. Populates `competitors[]` in poc-brief. Study folder is empty when step 3 completes.
4. Run `template-hunt/{type}` — search type-specific free template galleries, evaluate up to `max_templates` candidates, pick the best one. Do NOT copy yet — record the choice in `templates[]` as the scaffold candidate. If no suitable template found, record `null` and note "build from scratch".
5. Run `design-swipe/{type}` → broader visual inspiration. Populates `visual_inspiration`.
6. **Synthesise** — reviews are the primary driver of what gets built:
   - **`feature_spec`**: buyer wishes + unmet needs → what to build. If buyers consistently ask for something no competitor has, we build it.
   - **`differentiation`**: buyer complaints + wishes → specific things we do better than every competitor. Each item must be delivered in the final product — Stage 04 treats this as a build checklist. The gap between what buyers hate about competitors and what they ask for.
   - **`gaps`**: features buyers want but deferred from this POC (too complex, out of scope, or needs more data). Stage 04 fills these after delivering every `differentiation[]` item first.
   - **`delivery_format`**: see `pipeline/workspace-setup.md` delivery formats table — based on `product_type` and competitor patterns.
   - **`style`**: confirmed palette/font/layout before building — combine competitor styles + design-swipe inspiration. Build uses this style from the start.
   - **`structure`** (planned): planned tab/page/frame layout based on `feature_spec`. Use schema shape from `pipeline/workspace-setup.md` schema shapes table. Used as blueprint for step 7.
7. Run `skills/build/{type}` (`depth: "rough"`) — if scaffold found in step 4: copy it to **POC folder**, named `[poc] {keyword}` (see `pipeline/workspace-setup.md` for platform-specific copy + move steps); if no scaffold: create a new blank file in **POC folder** (see workspace-setup.md). Then build using confirmed `style` and planned `structure` from step 6. Document `known_issues` as they're discovered.
8. Playwright visual check → screenshots saved to `pipeline/03-poc/output/{slug}-screenshots/`. Add any visual issues to `known_issues`.
9. Write actual `structure` and `logic_map` from what was **actually built** (may differ from the plan in step 6). Use schema shapes from `pipeline/workspace-setup.md`.
10. Write `buyer_flow` — step-by-step of how a buyer would use the built POC.
11. Refine `style` if the built result revealed any adjustments needed.
12. Write `{slug}-poc-brief.json` with all fields populated.
13. Present to human: product type, keyword, top 3 `feature_spec`, top 3 `differentiation`, key `known_issues`, screenshots, `poc_result.link`. Ask: commit / abandon.
14. If **commit** → create `products/{slug}/`, write `product.json` (stage: 03-poc, status: complete), proceed to Stage 04.
15. If **abandon** → delete the built product from **POC folder** (see `pipeline/workspace-setup.md` for platform-specific delete steps), clean up `pipeline/03-poc/output/`, end.

**Agent:**
- [x] `agents/poc-agent.md` — Orchestrates all steps above, saves output to `pipeline/03-poc/output/`

**POC Brief output (`{slug}-poc-brief.json`):**

```json
{
  "slug": "budget-tracker-freelancer",
  "product_type": "google-sheets",
  "keyword": "freelancer budget tracker",

  "feature_spec": ["track income by category", "monthly vs annual toggle", "..."],

  "structure": {
    "tabs": ["Instructions", "Income", "Expenses", "Dashboard"],
    "data_flows": ["Income → Dashboard", "Expenses → Dashboard"],
    "notes": "..."
  },

  "logic_map": {
    "key_formulas": [
      {
        "name": "Total Income",
        "location": "Dashboard!B2",
        "depends_on": "Income!B:B",
        "logic": "SUM of all income entries"
      }
    ],
    "notes": "..."
  },

  "_schema_notes": {
    "structure": "shape varies by product_type — tabs[] for Sheets; pages/databases[] for Notion; pages/frames[] for Canva",
    "logic_map": "Sheets: key_formulas[]; Notion: formula_properties[] + rollups[]; Canva: omit (no logic)"
  },

  "competitors": [
    {
      "url": "...",
      "title": "...",
      "price": "...",
      "key_features": ["..."],
      "structure": ["Instructions", "Income", "Expenses", "Dashboard"],
      "logic_notes": "uses SUMIF for category totals, no named ranges",
      "buyer_complaints": ["no instructions tab", "formulas break on mobile"],
      "buyer_wishes": ["want a dark theme", "want annual summary"],
      "visual_style": { "palette": ["#..."], "font": "...", "style_notes": "..." },
      "free_equivalent_urls": ["https://docs.google.com/spreadsheets/...", "https://vertex42.com/..."]
    }
  ],

  "visual_inspiration": {
    "pinterest_boards": ["https://pinterest.com/..."],
    "etsy_listings": ["https://etsy.com/listing/..."],
    "style_notes": "..."
  },

  "differentiation": [
    "add clear Instructions tab — top complaint across all competitors",
    "mobile-safe formulas — most common review complaint",
    "dark theme — most requested and popular visual direction on Pinterest"
  ],

  "style": {
    "palette": ["#1A1A2E", "#E94560", "#F5F5F5"],
    "font": "Inter",
    "layout_style": "..."
  },

  "buyer_flow": [
    "Open Instructions tab and read setup steps",
    "Enter income entries in Income tab",
    "Enter expenses in Expenses tab",
    "View summary on Dashboard"
  ],

  "pricing": {
    "launch_price": 18,
    "target_price": 25,
    "price_range": { "min": 9, "max": 35 },
    "source": "pipeline/02-validate/output/..."
  },

  "delivery_format": "google-sheets-link + xlsx-download",

  "templates": [
    {
      "url": "...",
      "source": "google-sheets-gallery",
      "title": "...",
      "used_as_scaffold": true,
      "notes": "closest match to planned structure — copied as POC starting point"
    },
    {
      "url": "...",
      "source": "vertex42",
      "title": "...",
      "used_as_scaffold": false,
      "notes": "evaluated but too simple — no chart support"
    }
  ],

  "gaps": [
    "no category breakdown chart",
    "missing annual summary view"
  ],

  "known_issues": [
    "formula in Dashboard!B5 breaks when Income tab is empty"
  ],

  "poc_result": {
    "type": "google-sheets",
    "link": "https://docs.google.com/...",
    "screenshots": ["pipeline/03-poc/output/{slug}-screenshots/tab-1.png", "..."],
    "notes": "..."
  },

  "build_instructions": "Start from the poc_result link. Fix known_issues first. Polish feature_spec[] to full quality (clean formulas, error handling, buyer UX). Verify every differentiation[] item exists — treat as a checklist. Fill gaps[]. Polish style to match confirmed palette."
}
```

---

## Stage 04 — Build (pipeline/04-build/)

Polish the POC into a shippable product. Reads `{slug}-poc-brief.json` from Stage 03. Routes to the correct product-type build skill. Adds instruction tab / setup guide, buyer-facing UI, delivery format. Creates all product-specific docs used by downstream stages. **Self-tests before handing off** — Stage 04 runs its own test-plan and fixes all failures before Stage 05 ever sees the product. Stage 05 is an independent sign-off, not a debugging session.

**Stage structure:**
```
pipeline/04-build/
  agents/
    build-agent.md             ← orchestrates the whole stage
  skills/
    setup-guide.md             ← generate buyer setup guide
    delivery-prep.md           ← prepare final delivery files + set correct sharing/access permissions
    test-plan.md               ← generate test-plan.json from formula-spec + differentiation + gaps
```

**Shared skills used:**

Build skills (same skills as Stage 03, but full polished depth):
- [x] `skills/build/notion.md` — Full Notion build: complete pages, databases, views, formulas, instruction page, buyer UX (`depth: "full"`)
- [x] `skills/build/google-sheets.md` — Full Google Sheets build: clean formulas, consistent styling, instruction tab, named ranges, error handling (`depth: "full"`)
- [x] `skills/build/canva.md` — Full Canva product: polished design, all pages, exportable format (`depth: "full"`)

Visual check:
- `skills/playwright.md` — Final screenshot pass of finished product. Screenshots saved to `products/{slug}/screenshots/` and fed into Stage 06 as mockup source material.

**Build-time checks (inline, during construction):**
Each `skills/build/{type}.md` must verify each major step before moving on — catch issues immediately, not after the whole product is built. This is not a replacement for Stage 05 QA.
- Added a formula or tab → verify 2–3 key formulas via MCP API, fix before continuing
- Built a database or view in Notion → create a test entry, read it back, delete it
- Designed a page in Canva → screenshot to confirm it renders correctly

**What drives the build — poc-brief carries all decisions into Stage 04:**
- `differentiation[]` — the promises we made based on buyer complaints. Build must deliver every item on this list. Treat it as a checklist: if it's in differentiation, it must exist in the finished product.
- `competitors[].buyer_complaints` — known pain points buyers have with existing products. The build should proactively solve these, not just avoid repeating them.
- `feature_spec[]` — already shaped by buyer wishes. Build implements these exactly.
- `gaps[]` — features deferred from POC as too complex or out of scope. Build fills these after every `differentiation[]` item is delivered.

**Product docs created (saved to `products/{slug}/docs/`):**
- `formula-spec.md` — every formula/logic block: what it calculates, input cells/fields, output cells/fields, edge case behaviour (Sheets/Notion only)
- `test-plan.json` — 6 test categories written by `test-plan.md` skill:
  1. **Logic** (Sheets/Notion only): formula correctness, cross-tab data flows, relations, rollups
  2. **Edge cases** (Sheets/Notion only): empty input, zero, negative, max values don't break logic
  3. **Style** (all types): palette, fonts, layout match `style-guide.json`
  4. **Buyer flow** (all types): buyer can follow setup guide and use every tab/page/frame
  5. **Differentiation** (all types): one test per item in `differentiation[]`
  6. **Gaps filled** (all types): one test per filled gap from poc-brief
- `style-guide.json` — finalised palette, fonts, spacing (from poc-brief `style`) — consumed by Stage 06 Marketing
- `setup-guide.md` — buyer instructions written with `buyer_complaints` in mind: anywhere competitors confuse buyers, we explain it clearly and proactively

**Agent flow:**
1. Read `{slug}-poc-brief.json` → confirm `product_type`, load `known_issues`, `feature_spec`, `differentiation`, `gaps`, `style`, `competitors[].buyer_complaints` (aggregated across all competitors), `delivery_format`, `poc_result.link`. Copy the POC into the **Products folder**, named `{keyword}` (no prefix) — see `pipeline/workspace-setup.md` for platform-specific copy + move steps. All subsequent steps work on this Products/ copy. Update `working_link`.
2. Open `working_link` (Products/ copy) and run `skills/build/{type}.md` (`depth: "full"`) — fix `known_issues` first, then polish `feature_spec[]` to full quality, then verify every `differentiation[]` item exists, then fill `gaps[]`, with inline checks after each major step
3. Write `products/{slug}/docs/formula-spec.md` from the built formulas/logic (Sheets/Notion only — skip for Canva, set `formula_spec_path: null`)
4. Write `products/{slug}/docs/style-guide.json` finalised from poc-brief `style`, updated to reflect any adjustments made during the build
5. Run `test-plan.md` with `formula-spec.md` + `style-guide.json` + `differentiation` + `gaps` + `buyer_flow` + `structure` as input → write `products/{slug}/docs/test-plan.json` (6 test categories: logic, edge cases, style, buyer flow, differentiation, gaps filled)
6. **Run all tests from `test-plan.json` against the built product** — for each test: copy the product (`[test-{id}] {slug}`), run test steps on the copy, record result, delete the copy. Fix every failure in the production product, re-run only failed tests, repeat until all pass. Do not proceed to step 7 until clean.
7. Run `setup-guide.md` with `buyer_complaints` + `buyer_flow` + `feature_spec` + `structure` as input → write `products/{slug}/docs/setup-guide.md`
8. Run `delivery-prep.md` → set correct sharing/access permissions, generate download files where required → write `products/{slug}/delivery/delivery.json`
9. Playwright final visual pass → screenshot every tab/page/frame → save to `products/{slug}/screenshots/`. Fix any visual issues found.
10. Update `product.json` pipeline status (stage: 04-build, status: complete)

**Agent:**
- [x] `agents/build-agent.md` — Orchestrates all steps above, self-tests until clean, creates all product docs, updates `product.json`

---

## Stage 05 — QA (pipeline/05-qa/)

Independent verification before marketing spend. Stage 04 already self-tested — Stage 05 is a fresh pass by a different agent with no knowledge of how it was built. QA is product-type aware — checks differ by type. Must pass before Stage 06 can begin.

**Stage structure:**
```
pipeline/05-qa/
  agents/
    qa-agent.md
  skills/
    qa-checklist.md          ← product-type-aware checklist (visual + functional)
    formula-checker.md       ← Google Sheets only
```

**Shared skills used:**
- `skills/playwright.md` — visual check: buyer simulation screenshots

**Inputs from upstream:**
- `product.json` → `product_type`, product link
- `products/{slug}/docs/test-plan.json` → test cases with inputs + expected outputs
- `products/{slug}/docs/formula-spec.md` → formula audit reference (Sheets only)

**Visual check (Playwright) — does it render correctly?**
Simulate the buyer opening the product for the first time. Screenshot each step:
- Google Sheets / Notion: open URL, navigate every tab/page, screenshot
- Canva: open exported file, verify all pages render without corruption, screenshot
- Screenshots saved to `products/{slug}/qa/screenshots/`

**Functional check (MCP APIs) — does the logic produce correct output?**
**Test isolation rule:** Always test on a copy, never the original. Loop: copy → test → record result → delete copy → fix original → repeat until passing.
- Google Sheets (`mcp__claude_ai_Google_Drive__*`): copy file → write test values from `test-plan.json` → read back formula outputs → compare vs expected → delete copy. Edge cases: empty, zero, negative, max.
- Notion (`mcp__notion__*`): duplicate page/database → create test entries → read back rollup/formula properties → verify filter views → delete duplicate.
- Canva (`mcp__canva__*`): copy design → verify placeholder text is editable → export → verify file completes without error and within Etsy size limits → delete copy.

**Agent flow:**
1. Read `product.json` → get `product_type` and product link
2. Read `products/{slug}/docs/test-plan.json` and `formula-spec.md`
3. Playwright visual check → screenshot every tab/page as first-time buyer
4. MCP functional check (copy → test → record → delete) per product type
5. Run `formula-checker.md` (Sheets only) — audit every formula in `formula-spec.md`
6. Run `qa-checklist.md` — 4-area quality rubric (see below)
7. Write `products/{slug}/qa/results.json` with pass/fail per check + screenshot refs
8. If all pass → update `product.json` status, proceed to Stage 06
9. If any fail → list failures, block Stage 06, wait for fix then re-run

**`qa-checklist.md` covers 4 areas (all product types unless noted):**
- **Visual quality**: style consistent across all tabs/pages, no placeholder text remaining, no clashing colours, no broken visual elements
- **Usability**: first impression when opened — is it obvious what to do? Are labels clear? Is navigation intuitive without needing instructions?
- **Instructions tab/page**: does it exist, is it complete, does it cover every step in `buyer_flow`, is it written for the buyer (not the builder)?
- **Compatibility**: mobile viewport renders correctly (Sheets/Notion); export file size within Etsy limits and no corrupted pages (Canva)

**Agent:**
- [ ] `agents/qa-agent.md` — Orchestrates all steps above, gates Stage 06

---

## Stage 06 — Marketing (pipeline/06-marketing/)

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
- `pipeline/02-validate/output/` → best title keyword, buyer language for listing copy
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

## Stage 07 — Launch (pipeline/07-launch/)

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

## Stage 08 — Iterate (pipeline/08-iterate/)

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
- `pipeline/02-validate/output/` → original keyword for competitive search
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

- Stage 00 — Discover: **complete** ✅
- Stage 01 — Research: **complete** ✅
- Stage 02 — Validate: **complete** ✅
- Stage 03 — POC: **complete** ✅
- Stage 04 — Build: **complete** ✅
- Stage 05 — QA: not started
- Stage 06 — Marketing: not started
- Stage 07 — Launch: not started
- Stage 08 — Iterate: not started
- Infrastructure: not started

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
- [ ] `skills/study/template-hunt.md` — general process: find free templates, routes to product-specific skill
- [ ] `skills/study/template-hunt/notion.md` — Notion template sources, how to duplicate
- [ ] `skills/study/template-hunt/google-sheets.md` — Google Sheets template sources, how to copy
- [ ] `skills/study/template-hunt/canva.md` — Canva template sources, how to copy
- [ ] `skills/study/design-swipe.md` — general process: collect visual inspiration, routes to product-specific skill
- [ ] `skills/study/design-swipe/notion.md` — Notion-specific: page layouts, database views, icons, cover images, property styling
- [ ] `skills/study/design-swipe/google-sheets.md` — Sheets-specific: cell styling, color schemes, chart styles, tab layouts
- [ ] `skills/study/design-swipe/canva.md` — Canva-specific: design aesthetic, typography, illustration style, frame layout
- [ ] `skills/study/product-teardown.md` — general process: deep study a competitor (functional + visual), routes to product-specific skill
- [ ] `skills/study/product-teardown/notion.md` — Notion-specific: database properties, views, relations, rollups, page hierarchy, formulas + visual: palette, layout style, icon usage, cover design
- [ ] `skills/study/product-teardown/google-sheets.md` — Sheets-specific: formulas, tab structure, named ranges, charts, conditional formatting + visual: color scheme, font, cell styling, chart design
- [ ] `skills/study/product-teardown/canva.md` — Canva-specific: design elements, layout, frame structure, export format + visual: overall aesthetic, typography, illustration style, colour palette

**Build (skills/build/) — used by Stage 03 (rough) and Stage 04 (polished):**
- [ ] `skills/build/notion.md` — duplicate + modify Notion template: pages, databases, views, formulas (uses `mcp__notion__*`)
- [ ] `skills/build/google-sheets.md` — copy + modify Google Sheets: formulas, formatting, tabs (uses `mcp__claude_ai_Google_Drive__*`)
- [ ] `skills/build/canva.md` — build product design in Canva (uses `mcp__canva__*`)

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

Study what works on Etsy, find free templates, collect visual inspiration, then build a rough prototype. Internal checkpoint only — not shown to buyers. Output is `poc-brief.json` which feeds Stage 04.

**Study skills used (from `skills/study/`):**
All three study skills follow the same pattern: a general skill file describes the overall intent and routes to the product-type-specific file which handles the actual steps.

- [ ] `skills/study/product-teardown.md` → `skills/study/product-teardown/{type}.md` — Study top 3–5 competitors: screenshots, features, formula/logic/database structure, pricing, reviews AND visual style (palette, fonts, layout). Output feeds `competitors`, `feature_spec`, `structure`, `logic_map`, and `visual_inspiration` (competitor styles) in poc-brief.
- [ ] `skills/study/template-hunt.md` → `skills/study/template-hunt/{type}.md` — Find free templates, copy/duplicate one as the starting point. Output feeds `templates` in poc-brief.
- [ ] `skills/study/design-swipe.md` → `skills/study/design-swipe/{type}.md` — Collect broader visual inspiration from Pinterest + Etsy beyond direct competitors. Output adds to `visual_inspiration` in poc-brief.

Together, `product-teardown` (competitor styles) + `design-swipe` (broader trends) populate `visual_inspiration`, which the poc-agent synthesises into the confirmed `style` after the rough build.

**Build skills used (from `skills/build/`):**
- [ ] `skills/build/notion.md` — Duplicate + lightly modify a Notion template: pages, databases, views, basic formulas
- [ ] `skills/build/google-sheets.md` — Copy + lightly modify a Google Sheets template: formulas, formatting, tabs
- [ ] `skills/build/canva.md` — Rough build of product design in Canva

**Visual check (Playwright):**
After building the rough draft, take screenshots of the product to confirm it renders correctly before committing:
- Google Sheets / Notion: navigate to the live URL, screenshot each tab/page
- Canva: screenshot the Canva editor view of each page
- Screenshots saved to `pipeline/03-poc/output/{slug}-screenshots/` and referenced in `poc-brief.json`

**Agent:**
- [ ] `agents/poc-agent.md` — Orchestrates Stage 3: infers `product_type` from validate output and confirms with human, runs study skills, builds rough draft via `skills/build/{type}.md`, runs Playwright visual check, saves `{slug}-poc-brief.json` to `pipeline/03-poc/output/`, creates `products/{slug}/` folder, initializes `product.json`, prompts human for commit/abandon decision

**POC Brief output (`{slug}-poc-brief.json`):**

```json
{
  "slug": "budget-tracker-freelancer",
  "product_type": "google-sheets",

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

  "visual_inspiration": {
    "competitor_styles": [
      { "url": "https://etsy.com/listing/...", "palette": ["#..."], "font": "...", "style_notes": "..." }
    ],
    "pinterest_boards": ["https://pinterest.com/..."],
    "etsy_listings": ["https://etsy.com/listing/..."],
    "style_notes": "..."
  },

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

  "competitors": [
    { "url": "...", "title": "...", "price": "...", "key_features": ["..."] }
  ],

  "templates": [
    { "url": "...", "source": "google-sheets", "notes": "..." }
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

  "build_instructions": "Start from the poc_result link. Fix known_issues first, then fill gaps, then polish style to match confirmed palette."
}
```

---

## Stage 04 — Build (pipeline/04-build/)

Polish the POC into a shippable product. Reads `poc-brief.json` from Stage 03. Routes to the correct product-type build skill. Adds instruction tab / setup guide, buyer-facing UI, delivery format.

**Build-time checks (inline, during construction):**
Each `skills/build/{type}.md` skill must verify each major step before moving to the next — catch issues immediately, not after the whole product is built. This is not a replacement for Stage 05 QA; it prevents Stage 05 from surfacing fundamental build problems. After each major action:
- Added a formula or tab → verify 2–3 key formulas compute correctly via MCP API
- Built a database or view in Notion → create a test entry, read it back, delete it
- Designed a page in Canva → screenshot to confirm it renders correctly
If a check fails, fix it before continuing to the next step.

**Build skills used (from `skills/build/`):**
- [ ] `skills/build/notion.md` — Full Notion build: complete pages, databases, views, formulas, instruction page, buyer UX — with inline checks after each major step
- [ ] `skills/build/google-sheets.md` — Full Google Sheets build: clean formulas, consistent styling, instruction tab, named ranges, error handling — with inline checks after each major step
- [ ] `skills/build/canva.md` — Full Canva product: polished design, all pages, exportable format — with screenshot check after each major step

**Stage-specific skills (`pipeline/04-build/skills/`):**
- [ ] `skills/setup-guide.md` — Generate buyer setup guide → saved to `products/{slug}/docs/setup-guide.md`
- [ ] `skills/delivery-prep.md` — Decide delivery format, prepare final files → saved to `products/{slug}/delivery/`

**Product docs created (saved to `products/{slug}/docs/`):**
- `formula-spec.md` — document every formula/logic block: what it calculates, input cells/fields, output cells/fields, edge case behaviour
- `test-plan.json` — test cases derived from the formula spec: input values, expected outputs, edge cases (empty, zero, negative, max)
- `style-guide.json` — finalised palette, fonts, spacing (refined from `style` in poc-brief)

**Visual check (Playwright) — final pass:**
After the full build is complete, take a screenshot pass of the finished product. Screenshots saved to `products/{slug}/screenshots/` — these feed directly into Stage 06 marketing mockups:
- Google Sheets / Notion: navigate to live URL, screenshot every tab/page in order
- Canva: screenshot editor view of every page, then export and screenshot the exported file

**Agent:**
- [ ] `agents/build-agent.md` — Reads `{slug}-poc-brief.json`, determines product type, runs full build via `skills/build/{type}.md` (with inline checks), runs final Playwright visual pass, saves screenshots to `products/{slug}/screenshots/`, updates `product.json` pipeline status

---

## Stage 05 — QA (pipeline/05-qa/)

Test everything before marketing spend. QA is product-type aware — checks differ by type.

**Skills:**
- [ ] `skills/qa-checklist.md` — Product-type-aware checklist covering both visual and functional checks (see below). Reads `test-plan.json` and `formula-spec.md` from `products/{slug}/docs/` to drive checks. Shared checks: instruction tab/page complete, buyer experience walkthrough, no broken links.
- [ ] `skills/formula-checker.md` — Google Sheets only: reads `formula-spec.md` to audit every documented formula for errors, circular refs, and hardcoded values

**Visual check (Playwright) — does it render correctly?**
Simulate the buyer opening the product for the first time. Screenshot each step:
- Google Sheets: open URL, navigate every tab, screenshot
- Notion: open URL, navigate every page and database view, screenshot
- Canva: open exported file, verify all pages render without corruption, screenshot
- Screenshots saved to `products/{slug}/qa/screenshots/`

**Functional check (MCP APIs) — does the logic produce correct output?**
Use the product's native API to write test inputs and verify outputs — no DOM scraping.

**Test isolation rule:** Always test on a copy, never the original. The loop is: copy → test → record result → delete copy → fix original if needed → repeat. This keeps the product clean and leaves no test data in the workspace.

- Google Sheets (`mcp__claude_ai_Google_Drive__*`): copy the file via Drive API → write known test values to input cells → read back formula output cells → compare expected vs actual → delete copy. Test edge cases: empty, zero, negative, large numbers. Verify named ranges, data validation, cross-tab references.
- Notion (`mcp__notion__*`): duplicate the page/database via Notion MCP → create test entries with known values → read back rollup/formula properties → verify filter views return correct subsets → delete the duplicate.
- Canva (`mcp__canva__*`): copy the design via Canva MCP → verify all placeholder text is editable → export and verify file completes without error and is within Etsy size limits → delete copy. No formula logic to test.

**Agent:**
- [ ] `agents/qa-agent.md` — Reads `product_type` from `product.json`, runs Playwright visual check + MCP functional check for the product type, writes `products/{slug}/qa/results.json` with pass/fail per check and screenshot refs, blocks marketing if any check fails

---

## Stage 06 — Marketing (pipeline/06-marketing/)

Create everything needed for the Etsy listing. Cover that makes people click.

**Skills (pipeline-specific):**
- [ ] `skills/cover-brief.md` — Research competitor covers via Playwright, identify what makes top listings click-worthy, write visual brief for cover image
- [ ] `skills/mockup-generator.md` — Generate 3–5 preview images showing product in use

**Inputs from upstream:**
- `products/{slug}/docs/style-guide.json` — palette, fonts, spacing to keep cover/mockups visually consistent with the product
- `products/{slug}/screenshots/` — Build screenshots used directly as mockup source material

**Shared skills used:**
- `skills/etsy-listing.md` — Title, description, tags (grounded in research keyword data)
- `skills/etsy-cover-image.md` — Cover format constraints
- `skills/canva-design.md` — Generate cover via Canva using style-guide.json (primary)
- `skills/generate-image.md` — Fallback if Canva output isn't strong
- `skills/generate-video.md` — Product demo video (5–15 sec slideshow)
- `skills/record-video.md` — Screen-recorded walkthrough/tutorial video for Etsy listing

**Agent:**
- [ ] `agents/marketing-agent.md` — Orchestrates full marketing suite, saves all assets to `products/{slug}/marketing/`

---

## Stage 07 — Launch (pipeline/07-launch/)

Create and publish the Etsy listing.

**Skills:**
- [ ] `skills/listing-creator.md` — Assemble final listing JSON from marketing assets, set price (from validate data), upload product files, create Etsy listing via Etsy MCP (`mcp__etsy__*`)

**Agent:**
- [ ] `agents/launch-agent.md` — Orchestrates launch, saves Etsy listing URL to `product.json`, marks product as launched

---

## Stage 08 — Iterate (pipeline/08-iterate/)

Ongoing optimization after launch. Run periodically — not a one-time step.

**Skills:**
- [ ] `skills/performance-check.md` — Check listing views, favorites, sales, review score via Playwright on Etsy shop
- [ ] `skills/suggest-optimizations.md` — Compare current title/tags/images against current top performers, recommend specific changes

**Agent:**
- [ ] `agents/iterate-agent.md` — Orchestrates performance check + suggestions, appends to `products/{slug}/iterate-log.json`

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
- Stage 03 — POC: architecture planned, skills not started
- Stage 04 — Build: not started
- Stage 05 — QA: not started
- Stage 06 — Marketing: not started
- Stage 07 — Launch: not started
- Stage 08 — Iterate: not started
- Infrastructure: not started

# PiggyWise Pipeline Master Plan

End-to-end system for finding, building, and launching digital products (Google Sheets templates and similar) on Etsy.

**Strategy:** Build products people are already searching for — not invent and hope.

---

## How It Works

```
00-discover → 01-research → 02-validate → 03-poc → [human: commit?] → 04-build → 05-qa → 06-marketing → 07-launch → 08-iterate
```

- Stages 00–03: pipeline work, outputs saved to `pipeline/{stage}/output/` (gitignored)
- Stages 04–08: product work, all assets saved to `products/{slug}/`
- `product.json` inside each product folder tracks pipeline state across stages 04–08
- `/status "product-slug"` prints current stage at any time

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
  "research_ref": "pipeline/01-research/output/...",
  "validate_ref": "pipeline/02-validate/output/...",
  "pricing": {},
  "delivery": {},
  "etsy": {}
}
```

---

## Shared Skills (skills/)

These are reused across multiple stages.

- [x] `skills/etsy-listing.md` — SEO title, description, 13 tags, listing JSON for Etsy API
- [x] `skills/etsy-cover-image.md` — Cover image specs: 2000×1500px, safe zone, design checklist
- [x] `skills/canva-design.md` — Canva MCP tools for design creation and export
- [x] `skills/generate-image.md` — `echo "..." | codex exec` image generation (fallback)
- [x] `skills/generate-video.md` — ffmpeg slideshow MP4 for Etsy product video

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
- [ ] `skills/etsy-deep-dive.md` — Search for the specific product (not just seed), extract top 10 listings, price range (min/max/sweet spot), review sentiment (what buyers love/complain about)
- [ ] `skills/price-check.md` — Extract pricing from top listings, recommend price based on competition and positioning

**Agent:**
- [ ] `agents/validate-agent.md` — Orchestrates Stage 2, outputs validate JSON, prompts human for go/no-go

---

## Stage 03 — POC (pipeline/03-poc/)

Study what works on Etsy, build a rough prototype. Internal checkpoint only — not shown to buyers.

**Skills:**
- [ ] `skills/seller-study.md` — Playwright: scrape top 3–5 bestselling listings, extract feature clues from listing images/mockups, read reviews for buyer feedback, produce feature spec
- [ ] `skills/spreadsheet-builder.md` — Generate rough XLSX from feature spec using openpyxl, upload to Google Drive via MCP

**Agent:**
- [ ] `agents/poc-agent.md` — Orchestrates Stage 3, creates `products/{slug}/` folder, initializes `product.json`, prompts human for commit/abandon decision

---

## Stage 04 — Build (pipeline/04-build/)

Polish the POC into a shippable product. Add instruction tab, setup guide, buyer-facing UI.

**Skills:**
- [ ] `skills/spreadsheet-polisher.md` — Clean formulas, consistent styling, instruction tab, named ranges, error handling
- [ ] `skills/setup-guide.md` — Generate buyer setup guide (PDF or in-sheet instructions)
- [ ] `skills/delivery-prep.md` — Decide delivery format (XLSX + Google Sheets link + PDF guide), prepare files

**Agent:**
- [ ] `agents/build-agent.md` — Orchestrates Stage 4, updates `product.json` pipeline status

---

## Stage 05 — QA (pipeline/05-qa/)

Test everything before marketing spend.

**Skills:**
- [ ] `skills/qa-checklist.md` — Standard checklist: all formulas work, no broken references, edge cases tested, instruction tab complete, buyer experience walkthrough
- [ ] `skills/formula-checker.md` — Systematic formula audit: check each tab for errors, circular refs, hardcoded values that should be dynamic

**Agent:**
- [ ] `agents/qa-agent.md` — Runs checklist + formula check, writes `products/{slug}/qa/results.json`, blocks marketing if QA fails

---

## Stage 06 — Marketing (pipeline/06-marketing/)

Create everything needed for the Etsy listing. Cover that makes people click.

**Skills (pipeline-specific):**
- [ ] `skills/cover-brief.md` — Research competitor covers via Playwright, identify what makes top listings click-worthy, write visual brief for cover image
- [ ] `skills/mockup-generator.md` — Generate 3–5 preview images showing product in use

**Shared skills used:**
- `skills/etsy-listing.md` — Title, description, tags (grounded in research keyword data)
- `skills/etsy-cover-image.md` — Cover format constraints
- `skills/canva-design.md` — Generate cover via Canva (primary)
- `skills/generate-image.md` — Fallback if Canva output isn't strong
- `skills/generate-video.md` — Product video (5–15 sec slideshow)

**Agent:**
- [ ] `agents/marketing-agent.md` — Orchestrates full marketing suite, saves all assets to `products/{slug}/marketing/`

---

## Stage 07 — Launch (pipeline/07-launch/)

Create and publish the Etsy listing.

**Skills:**
- [ ] `skills/listing-creator.md` — Assemble final listing JSON from marketing assets, set price (from validate data), upload product files, create Etsy listing via Playwright (Etsy API upgrade later)

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
- [ ] `pipeline/02-validate/output/` added to .gitignore
- [ ] `pipeline/03-poc/output/` added to .gitignore
- [ ] `products/` folder structure documented in README

---

## Progress

- Stage 00 — Discover: **complete** ✅
- Stage 01 — Research: **complete** ✅
- Stage 02 — Validate: not started
- Stage 03 — POC: not started
- Stage 04 — Build: not started
- Stage 05 — QA: not started
- Stage 06 — Marketing: not started
- Stage 07 — Launch: not started
- Stage 08 — Iterate: not started
- Infrastructure: not started

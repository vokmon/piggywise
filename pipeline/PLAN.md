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
00-discover → 01-research → 02-validate → 03-build → [human: commit?] → 04-review → 05-marketing → 06-launch → 07-iterate
```

- Stages 00–02: pipeline research, outputs saved to `output/_discover/` (Stage 00) or `output/{slug}/{stage}/` (Stages 01–02) — all gitignored
- Stage 03: build, output saved to `output/{slug}/03-build/` — gitignored; on commit, creates `products/{slug}/`
- Stages 04–07: product work, all assets saved to `products/{slug}/`
- `product.json` inside each product folder tracks pipeline state across stages 04–07
- `/status "product-slug"` prints current stage at any time
- `product_type` is determined at the start of Stage 03 — the agent infers it from validate output and suggests; human confirms or overrides
- `pipeline/workspace-setup.md` — shared reference for all agents: working folder paths, file naming conventions, file operations per platform, delivery formats per product type

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
  "product_type": "notion",
  "keyword": "",
  "pipeline_status": {
    "stage": "03-build",
    "status": "complete",
    "brief": "output/{slug}/03-build/{slug}-brief.json"
  },
  "pricing": {},
  "etsy": {}
}
```

---

## Product Folder Structure

```
products/{slug}/
  product.json              ← pipeline state tracker
  marketing/                ← [created: Marketing] cover, mockups, listing.json, videos
  delivery/                 ← [created: Launch] final files prepared for buyer download
  iterate-log.json          ← [created/appended: Iterate] performance metrics and optimization history
```

---

## Stage 05 — Marketing (pipeline/05-marketing/)

Produces all Etsy marketing assets: cover image, preview images, video, and listing copy. Human provides raw screenshots and video footage; agent composes everything in Canva.

**Stage structure:**

```
pipeline/05-marketing/
  agents/
    marketing-agent.md
  styles/
    laptop-mobile.md         ← style preset: dark premium, laptop + phone frames
```

**Styles system:**

Visual styles are defined as preset files in `pipeline/05-marketing/styles/`. Each preset holds Canva template IDs and layout rules. Selected at invoke via `--style`. New styles = new file, no agent changes needed.

- `laptop-mobile.md` — dark gradient background, laptop + phone on cover, laptop-only previews. **Template IDs TBD** — to be filled in after browsing Canva free templates.

**Skills used:**

- `skills/generate-image.md` — fallback image generation if no suitable free Canva image found

**Inputs:**

- `output/{slug}/02-validate/{file}.json` → keywords, buyer language, tag keywords, competitor insights
- Canva folder `marketing/{slug}/` → raw assets uploaded by human (named: `cover-desktop.*`, `cover-mobile.*`, `dashboard.png`, etc.)

**Outputs (all in `products/{slug}/marketing/`):**

- `cover.png` — laptop + phone side by side, dark background
- `preview-01.png` … `preview-N.png` — one per screenshot provided (laptop frame, flexible count)
- `demo.mp4` — video from footage with feature text overlays
- `{slug}-listing.json` — Etsy title, description, 13 tags, price placeholder

**Canva workspace:**

- `marketing/{slug}/` — human uploads raw assets here
- `marketing/{slug}/output/` — agent saves all built designs here

**Agent flow:**

1. Load validate output → keyword, buyer language, tag keywords
2. Load style preset → template IDs, layout rules
3. Scan `marketing/{slug}/` in Canva → classify assets (cover shots, previews, video)
4. **Confirm plan with human** — list assets found and what will be produced
5. Build cover → copy template, swap in cover-desktop + cover-mobile, update text
6. Build previews → one per screenshot, laptop frame, caption from filename
7. Build video → copy template, place footage, add feature callouts
8. Write listing copy → `{slug}-listing.json`
9. **Pause for human review** in Canva at `marketing/{slug}/output/`
10. On approval → export PNG + MP4 to `products/{slug}/marketing/`
11. Update `product.json` status

**Image sourcing:** search Canva free images first; if nothing suitable → `skills/generate-image.md`, human uploads result to Canva.

**Agent:**

- [x] `agents/marketing-agent.md`
- [ ] `styles/laptop-mobile.md` — template IDs not yet filled in

---

## Stage 06 — Launch (pipeline/06-launch/)

Assemble everything from upstream and publish the Etsy listing. Generic process — same steps for every product.

**Stage structure:**

```
pipeline/06-launch/
  agents/
    launch-agent.md
  skills/
    listing-creator.md       ← assemble + publish listing via Etsy MCP
```

**Credentials:**

- `ETSY_KEYSTRING` + `ETSY_SECRETSTRING` — Etsy shop management API credentials for creating and publishing the listing via `mcp__etsy__*`

**Inputs from upstream:**

- `products/{slug}/marketing/` → cover image, mockups, videos, listing copy
- `products/{slug}/delivery/` → product files to upload for buyer download
- `output/{slug}/03-build/{slug}-brief.json` → pricing
- `product.json` → slug, product_type

**Agent flow:**

1. Read `product.json` → slug, product_type
2. Read `output/{slug}/03-build/{slug}-brief.json` → pricing
3. Read `products/{slug}/marketing/` → cover, mockups, videos, title, description, tags
4. Read `products/{slug}/delivery/` → delivery files
5. Run `listing-creator.md`:
   a. Upload delivery files via Etsy MCP
   b. Upload cover + mockup images
   c. Upload videos
   d. Set price from brief pricing
   e. Create and publish listing via `mcp__etsy__*`
6. Save Etsy listing URL to `product.json`
7. Update `product.json` status to launched

**Agent:**

- [x] `agents/launch-agent.md`
- [x] `skills/listing-creator.md`
- [x] `skills/etsy-connect.md` (root skills/)

---

## Stage 07 — Iterate (pipeline/07-iterate/)

Ongoing optimization after launch. Run periodically — not a one-time step. Generic process — same for every product, fed with product-specific Etsy data.

**Stage structure:**

```
pipeline/07-iterate/
  agents/
    iterate-agent.md
  skills/
    performance-check.md     ← fetch our listing stats via Etsy API
    suggest-optimizations.md ← compare vs current top performers, recommend changes
```

**Shared skills used:**

- `skills/playwright.md` — search Etsy for current top performers (competitive analysis only)

**Credentials:**

- `ETSY_KEYSTRING` + `ETSY_SECRETSTRING` — Etsy shop management API credentials. Use for all reads/writes on our own shop: listing stats, sales, reviews, listing updates. Cannot access other shops.

**Inputs from upstream:**

- `product.json` → Etsy listing ID, slug, keyword
- `output/{slug}/02-validate/` → original keyword for competitive search
- `products/{slug}/iterate-log.json` → previous performance history for trend comparison

**Agent flow:**

1. Read `product.json` → Etsy listing ID, keyword
2. Run `performance-check.md` → fetch our listing stats via Etsy API: views, favorites, sales, review score, recent review text
3. Run `suggest-optimizations.md`:
   a. Use Playwright to search Etsy for current top performers on the same keyword
   b. Compare our title/tags/cover/price against theirs
   c. Mine new reviews from step 2 for complaints and praise
   d. Recommend specific changes: listing (title, tags, cover, price) or product (feature/fix)
4. Append results + recommendations to `products/{slug}/iterate-log.json`
5. Present to human — human decides which changes to action

**Agent:**

- [ ] `agents/iterate-agent.md`

---

## Infrastructure

- [ ] `agents/status-agent.md` — `/status "slug"` reads `product.json`, prints readable pipeline dashboard
- [ ] All `pipeline/*/output/` folders added to .gitignore (00 through 03)
- [ ] Large files in `products/` added to .gitignore: `products/*/marketing/`, `products/*/delivery/`
- [ ] `products/` folder structure documented in README

---

## Progress

- Stage 05 — Marketing: agent written, style file in progress (template IDs TBD)
- Stage 06 — Launch: complete (launch-agent.md, listing-creator.md, shared/etsy-connect.md)
- Stage 07 — Iterate: not started
- Infrastructure: not started

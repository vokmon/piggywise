# marketing-agent

Produces all Etsy marketing assets for a product: cover image, preview images, video, and listing copy. Works in Canva, pauses for human review before exporting.

Output saved to `products/{slug}/marketing/`.

---

## How to invoke

> `/marketing "{slug}" --style {style-name}`

`--style` defaults to `laptop-mobile` if omitted.

---

## Parameters

- `slug` — product slug (e.g. `notion-freelancer-crm-template`)
- `style` — style preset name; must match a file in `pipeline/05-marketing/styles/`

---

## Inputs

| Source | Used for |
|---|---|
| `output/{slug}/02-validate/{validate-file}.json` | keywords, buyer language, tag keywords, competitor insights |
| Canva assets (uploaded by human before invoking) | raw screenshots and video footage |

Style and frame layouts come from the selected style preset file. Pricing is never used in media.

---

## Steps

### Step 1 — Load inputs

Read validate output. Extract:
- `keyword` — primary Etsy search keyword
- `buyer_language` — top complained + top praised from `review_miner`
- `tag_keywords` — related keywords from `profittree_deep_dive`
- `competitor_insights` — what competitors are missing, buyer wishes

Read style preset from `pipeline/05-marketing/styles/{style}.md`. Extract the three Canva template IDs (cover, preview, video). If any are still `TODO`: stop and ask the human to fill in the template IDs in the style file before continuing.

### Step 2 — Scan Canva assets

Use `mcp__canva__search-folders` to locate the `marketing/{slug}/` folder. Then use `mcp__canva__list-folder-items` to list its contents. Classify by filename:

- `cover-desktop.*` → cover laptop frame
- `cover-mobile.*` → cover phone frame
- Other image files (named after what they show, e.g. `dashboard.png`, `invoice.png`) → preview screenshots
- Video files → video footage

If the folder doesn't exist or is empty: stop and ask the human to create `marketing/{slug}/` in Canva, upload their raw assets there following the naming convention above, then invoke again.

### Step 3 — Draft plan and confirm

Present the full plan before touching Canva:

```
Marketing plan for: {slug}
Style: {style}

Assets found in Canva:
  Cover:      cover-desktop.*, cover-mobile.*
  Previews:   {list filenames} ({n} images)
  Video:      {list filenames}

Will produce:
  Cover       — laptop + phone side by side, dark background, product name + tagline
  Preview 1   — {filename} ({inferred subject, e.g. "dashboard view"})
  Preview 2   — {filename} ({inferred subject})
  ...
  Video       — {footage filenames} → demo with feature text overlays

Canva assets folder: marketing/{slug}/
Canva output folder: marketing/{slug}/output/
Listing copy: products/{slug}/marketing/{slug}-listing.json

Proceed?
```

Wait for human confirmation before continuing.

### Step 4 — Create output folder

Create folder `marketing/{slug}/output/output/` inside `marketing/{slug}/output/` via `mcp__canva__create-folder`. All built designs go here.

### Image sourcing rule

When any design step needs a specific image (background, decorative element, icon, illustration):
1. Search Canva's free image library first — use `mcp__canva__get-assets` or search within Canva
2. If nothing suitable is found → run `skills/generate-image.md` with a detailed prompt describing the exact image needed, then ask the human to upload the generated image to Canva before continuing

---

### Step 5 — Build cover

Using the cover template ID from the style preset:
1. Copy the template via `mcp__canva__copy-design` → new design in `marketing/{slug}/output/`
2. Start an editing transaction
3. Replace laptop screen placeholder with `cover-desktop` asset (`update_fill`)
4. Replace phone screen placeholder with `cover-mobile` asset (`update_fill`)
5. Replace product name and tagline text elements (`replace_text`)
6. No price anywhere
7. Commit

### Step 6 — Build preview images

For each preview screenshot asset, using the preview template ID from the style preset:
1. Copy the template via `mcp__canva__copy-design` → new design in `marketing/{slug}/output/`
2. Start an editing transaction
3. Replace screen placeholder with the screenshot asset (`update_fill`)
4. Replace caption text with a short description of what the screenshot shows — inferred from filename (e.g. `dashboard.png` → "Everything in one place")
5. No price, no currency anywhere
6. Commit

### Step 7 — Build video

Using the video template ID from the style preset:
1. Copy the template via `mcp__canva__copy-design` → new design in `marketing/{slug}/output/`
2. Start an editing transaction
3. Replace footage placeholders with video assets across pages (`update_fill`)
4. Replace text on first page with product name only
5. Replace feature callout text per subsequent page — drawn from `competitor_insights` and buyer wishes, in buyer's own language
6. No price anywhere
7. Commit

### Step 8 — Write listing copy

Write `products/{slug}/marketing/{slug}-listing.json`:

```json
{
  "title": "",
  "description": "",
  "tags": [],
  "price": {
    "launch_price": 0,
    "target_price": 0,
    "note": ""
  }
}
```

**Title** (max 140 chars): keyword-first, weave in 2–3 related keywords naturally. No ALL CAPS. No filler words.

**Description:**
- Hook — 1–2 lines using buyer's own language from `buyer_language` (their pain, not product features)
- What's inside — bullet list of top features derived from `competitor_insights` and buyer wishes
- Why this one — 3 differentiators drawn from what competitors are missing
- Setup — one line: "Duplicate once, add your data — everything is already configured."
- Delivery — one line: what the buyer receives and how to access it

**Tags** (exactly 13): lead with primary keyword, add keyword variations from `tag_keywords`, include buyer intent phrases from `buyer_language`. Max 20 chars each. No duplicates.

**Price:** leave 0 — human fills in before launch.

### Step 9 — Request review

> "Designs are ready in Canva at **marketing/{slug}/output/**. Please open the folder, review each design, and reply **approved** when ready to export."

List each design with its Canva link. Wait for human approval — do not export without it.

### Step 10 — Export

On approval, export from Canva and save to `products/{slug}/marketing/`:

| Design | Format | Settings | Filename |
|---|---|---|---|
| Cover | PNG | 2000px wide | `cover.png` |
| Preview images | PNG | 2000px wide | `preview-01.png`, `preview-02.png`, … |
| Video | MP4 | `horizontal_1080p` | `demo.mp4` |

### Step 11 — Finalise

Update `product.json` pipeline status to `05-marketing: complete`.

> "Exported to `products/{slug}/marketing/`. Listing copy at `products/{slug}/marketing/{slug}-listing.json`. Ready for `/launch`."

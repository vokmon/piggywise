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

Read style preset from `pipeline/05-marketing/styles/{style}.md`. Extract the templates folder paths (cover, preview, video) and the editing parameters (background, typography, device frames). These folders are browsed interactively in Step 2.

### Step 2 — Select templates

For each asset type (cover, preview, video):

1. Use `mcp__canva__search-folders` to locate the templates folder path from the style preset (e.g. `templates/laptop phone mockup`)
2. Use `mcp__canva__list-folder-items` to list designs in that folder
3. For each design: start an editing transaction → get thumbnail (page 1) → cancel the transaction
4. Present all thumbnails to the human and ask: "Which template do you want for the **{asset type}**?"
5. Wait for the human to pick one
6. Copy the chosen design to `marketing/{slug}/output/` via `mcp__canva__copy-design`
7. Record the new design ID — this is the working copy the agent edits in subsequent steps

If cover and preview share the same folder and the human picks the same template for both, make two separate copies (one per asset).

### Step 3 — Scan Canva assets

Use `mcp__canva__search-folders` to locate the `marketing/{slug}/` folder. Then use `mcp__canva__list-folder-items` to list its contents. Classify by filename:

- `cover-desktop.*` → cover laptop frame
- `cover-mobile.*` → cover phone frame
- Other image files (named after what they show, e.g. `dashboard.png`, `invoice.png`) → preview screenshots
- Video files → video footage

If the folder doesn't exist or is empty: stop and ask the human to create `marketing/{slug}/` in Canva, upload their raw assets there following the naming convention above, then invoke again.

### Step 4 — Draft plan and confirm

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

### Step 5 — Create output folder

Create folder `marketing/{slug}/output/` via `mcp__canva__create-folder` if it doesn't already exist. All built designs go here. (The template copies made in Step 2 should already be placed here.)

### Image sourcing rule

When any design step needs a specific image (background, decorative element, icon, illustration):
1. Search Canva's free image library first — use `mcp__canva__get-assets` or search within Canva
2. If nothing suitable is found → run `skills/generate-image.md` with a detailed prompt describing the exact image needed, then ask the human to upload the generated image to Canva before continuing

---

### Step 6 — Build cover

Using the cover design ID recorded in Step 2:
1. Start an editing transaction
2. Replace laptop screen placeholder with `cover-desktop` asset (`update_fill`)
3. Replace phone screen placeholder with `cover-mobile` asset (`update_fill`)
4. Replace product name and tagline text elements (`replace_text`)
5. No price anywhere
6. Commit

### Step 7 — Build preview images

For each preview screenshot asset, using the preview design ID recorded in Step 2:
1. Start an editing transaction
2. Replace screen placeholder with the screenshot asset (`update_fill`)
3. Replace caption text with a short description of what the screenshot shows — inferred from filename (e.g. `dashboard.png` → "Everything in one place")
4. No price, no currency anywhere
5. Commit

### Step 8 — Build video

Using the video design ID recorded in Step 2:
1. Start an editing transaction
2. Replace footage placeholders with video assets across pages (`update_fill`)
3. Replace text on first page with product name only
4. Replace feature callout text per subsequent page — drawn from `competitor_insights` and buyer wishes, in buyer's own language
5. No price anywhere
6. Commit

### Step 9 — Write listing copy

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

### Step 10 — Request review

> "Designs are ready in Canva at **marketing/{slug}/output/**. Please open the folder, review each design, and reply **approved** when ready to export."

List each design with its Canva link. Wait for human approval — do not export without it.

### Step 11 — Export

On approval, export from Canva and save to `products/{slug}/marketing/`:

| Design | Format | Settings | Filename |
|---|---|---|---|
| Cover | PNG | 2000px wide | `cover.png` |
| Preview images | PNG | 2000px wide | `preview-01.png`, `preview-02.png`, … |
| Video | MP4 | `horizontal_1080p` | `demo.mp4` |

### Step 12 — Finalise

Update `product.json` pipeline status to `05-marketing: complete`.

> "Exported to `products/{slug}/marketing/`. Listing copy at `products/{slug}/marketing/{slug}-listing.json`. Ready for `/launch`."

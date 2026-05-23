# marketing-agent

Generate all marketing assets and Etsy listing content for a theme pack.

## Input
- Theme name (e.g., "1970s")
- Final PDF path: `workspace/[THEME]/output/[THEME]_Memory_Lane_Brain_Health_Pack.pdf`

## Output
- Etsy cover image: `workspace/[THEME]/images/covers/[THEME]_cover.jpg`
- Preview images: `workspace/[THEME]/images/previews/[THEME]_preview_1.jpg` through `_preview_8.jpg`
- Product video: `workspace/[THEME]/images/videos/[THEME]_etsy.mp4`
- Etsy listing data: `workspace/[THEME]/data/product_posts/[THEME]_listing.json`

## Skills Used
- `skills/generate-image.md`
- `skills/etsy-cover-image.md`
- `skills/canva-design.md`
- `skills/generate-video.md`
- `skills/etsy-listing.md`
- `products/brain-health/skills/design-theme.md`

## Steps

### 1. Cover Image
Use design-theme skill for the visual prompt and generate-image skill to create it.
Apply etsy-cover-image skill for format specs, safe zone rules, and upload checklist:
- Style: warm, nostalgic, inviting
- Include: era name, "Brain Health Activity Pack", mood of the decade
- Format: 2000×1500px (4:3) — all key content centered within the middle 1500×1500px safe zone

### 2. Preview Images
Use design-theme skill for full specs on all 8 previews:
- Preview 1: Cover page + schedule page (canva-design)
- Preview 2: "What's included" callout graphic (canva-design)
- Preview 3: "How it works" — 3 steps: Download → Print → Play (canva-design)
- Preview 4: Sample word search puzzle (canva-design)
- Preview 5: Sample trivia/fill-blank activity (canva-design)
- Preview 6: Large-print close-up with "14pt large print" callout (canva-design)
- Preview 7: Gift angle — "A thoughtful gift for someone who loves the [era]" (canva-design)
- Preview 8: Lifestyle mockup — Canva free stock first (search "cosy reading table", "morning tea book"); fall back to generate-image if nothing warm enough is found

See design-theme skill for full image strategy and specs.

### 3. Product Video
Use generate-video skill to assemble a 15-second Etsy slideshow:
- Slide 1 (3s): Cover image
- Slide 2 (3s): Preview 2 ("What's included")
- Slide 3 (3s): Preview 4 (word search sample)
- Slide 4 (3s): Preview 6 (large-print close-up)
- Slide 5 (3s): Preview 8 (lifestyle mockup)
- Output: `workspace/[THEME]/images/videos/[THEME]_etsy.mp4`

### 4. Etsy Listing
Use etsy-listing skill to generate:
- SEO title (lead with decade + activity type)
- Body description
- 13 tags
- Save as `workspace/[THEME]/data/product_posts/[THEME]_listing.json`

**Key selling points to include in the body:**
- Large print friendly — 14pt body text, A4 size, easy to read
- No screen required — print at home, use with a pencil
- 90 activities across 9 types (word search, crossword, trivia, logic puzzles, and more)
- 4-week guided schedule included
- Answers printed discreetly on each page — no flipping to the back
- Great gift for a parent, grandparent, or loved one

**Tags to always include:** "large print", "large print puzzle", "printable large print"

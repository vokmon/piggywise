# design-theme

Apply era-appropriate visual styling to activity pages, cover images, and marketing assets.
Uses `skills/canva-design.md` and `skills/generate-image.md` as the underlying tools.

## Era Color Palettes

| Theme  | Primary          | Accent 1         | Accent 2         | Accent 3         |
|--------|------------------|------------------|------------------|------------------|
| 1970s  | Warm Orange      | Mustard Yellow   | Avocado Green    | Warm Brown       |
| 1960s  | Teal             | Coral            | Sunshine Yellow  | Cream White      |
| 1950s  | Powder Blue      | Soft Pink        | Cherry Red       | Ivory            |

Use palette colors at **20–30% opacity** for header bands and background tints.
Full-opacity color is used only for borders, icons, and decorative elements.

---

## Activity Page Layout (A4)

### Header Band
- Thin colored band at top (matching era primary color, 25% opacity)
- Running header text inside: `[Pack Name]  |  [Set Name]` (10pt, dark text)

### Border
- Thin colored border around the full page content area (era accent 1, 2–3px)

### Icons / Doodles
- **Maximum 1 decorative element per activity page**
- Place in a corner only (bottom-right preferred, top-left if bottom-right is occupied)
- Size: no larger than 20×20mm
- Style: simple line drawing appropriate to the era (e.g., record player for 1970s, jukebox for 1950s)
- Color: era accent color at 50–70% opacity

### Footer
- Plain white strip at bottom
- Left: `Answers → p.[X]` (10pt)
- Right: `Page [N]` (10pt)

---

## Cover Image

For Etsy format specs, safe zone rules, and upload checklist → see `skills/etsy-cover-image.md`

### Brain-Health Prompt Template
Use `skills/generate-image.md` with a prompt structured as:

```
[Era decade] vintage illustration, warm nostalgic mood, [era primary color palette],
"[Pack Name]" as bold centered text, brain activities theme,
flat design with subtle texture, 2000×1500px landscape,
all key elements (text and main subject) centered in the middle square area,
background fills the full width including the left and right sides,
soft era-appropriate objects in background
(e.g., for 1970s: vinyl records, macramé, lava lamp silhouettes)
```

---

## Etsy Preview Images

All previews: JPG, 2000×2000px minimum. Show actual content — no blank placeholder boxes.
Together they answer every buyer question: *What is it? What's inside? How do I get it? What does it look like? Is it easy to read? Is it a good gift?*

- **Preview 1** — Cover page + 4-week guided schedule side by side. Shows the pack exists and has structure.

- **Preview 2** — "What's included" callout graphic. Clean layout on era-colored background:
  ```
  ✔ 90 activities across 9 types
  ✔ Word search, crossword, trivia, logic puzzles & more
  ✔ 4-week guided schedule
  ✔ Full answer key with context
  ✔ Large print — 14pt A4
  ✔ Print as many times as you like
  ```
  Bold headline at top: "Everything you get:" — era font style, warm color palette.

- **Preview 3** — "How it works" — 3 clear steps with simple icons:
  ```
  1. Download instantly
  2. Print at home (any printer)
  3. Pick up a pencil and play
  ```
  Sub-note: "No special equipment. No screen time." Reassures less tech-savvy buyers and their families.

- **Preview 4** — Sample word search puzzle page (Activity 2.1) showing era colors, border, and warm game intro line.

- **Preview 5** — Sample trivia or fill-in-the-blank page (Activity 1.2 or 1.3) showing the score box and reflection prompt.

- **Preview 6** — Large-print close-up: zoom into 4–5 lines of actual question text at near-full size. Add a bold callout overlay: **"14pt large print — easy on the eyes"**. This is the #1 concern for the target buyer — answer it visually.

- **Preview 7** — Gift angle graphic. Warm background with era color accent:
  ```
  "A thoughtful gift for someone who loves the [era]"

  Perfect for:
  · A parent or grandparent
  · A loved one in a care home
  · Anyone who enjoys a daily brain workout
  ```
  Targets the caregiver and adult child who is the actual Etsy buyer.

- **Preview 8** — Lifestyle mockup: the printed pack open on a wooden table, next to a cup of tea and reading glasses. Warm natural morning light, cosy home atmosphere, no people.
  Use `skills/generate-image.md` — prompt:
  ```
  printed activity book open on a warm wooden table, cup of tea beside it,
  reading glasses nearby, soft natural morning light, cosy home atmosphere,
  no people, [era primary color] colour accent in scene, photorealistic
  ```

### Image Strategy
- **Canva free images first** — faster, consistent quality, more realistic for photos
- **generate-image as fallback** — use only when Canva has nothing era-specific or mood-appropriate enough

| Asset | Tool | Notes |
|-------|------|-------|
| Cover | `generate-image` | Needs era-specific custom illustration — Canva won't have 1970s lava lamp + exact palette |
| Previews 1–7 | `canva-design` | Layout + text + page screenshots — no external photos needed |
| Preview 8 (lifestyle mockup) | `canva-design` free stock first | Search: "cosy reading table", "morning tea book", "reading glasses table". Fall back to `generate-image` only if nothing warm and natural is found |

---

## Design Rules (All Formats)
- Black text on white for all readable content (never colored text on colored background)
- Color is accent only — never behind body text
- Do not use more than 2 palette colors on a single page
- Era imagery should be recognizable but not require knowledge of the era to understand the activity

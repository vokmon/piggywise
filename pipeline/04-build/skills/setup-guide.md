# setup-guide

Write the buyer-facing setup guide for the finished product. Called by build-agent after the product is fully built and verified. Written with `buyer_complaints` in mind — every place competitors confuse buyers, we explain it clearly and proactively.

Output: `products/{slug}/docs/setup-guide.md`

---

## Input

- `product_type` — string identifying the product type
- `product_name` — the product's title (from poc-brief keyword or confirmed name)
- `feature_spec` — array of features to cover in the guide
- `buyer_flow` — step-by-step buyer usage flow from poc-brief
- `buyer_complaints` — aggregated complaints from all competitors (the things buyers struggle with)
- `structure` — actual built structure (tabs/pages/frames) — use exact names from the built product
- `working_link` — link to the finished product

---

## Steps

### 1. Review buyer_complaints for confusion points

Before writing, scan `buyer_complaints` for recurring confusion themes. These become the places in the guide where you proactively explain things, add warnings, or add extra clarity.

Common confusion points to watch for:
- "No instructions" → ensure every step is covered
- "Formulas broke when I deleted a row" → warn buyers not to delete header rows; explain safe data entry
- "Doesn't work on mobile" → note any mobile limitations upfront
- "Too complex / overwhelming" → break setup into numbered steps, keep language simple
- "Couldn't figure out how to customise" → add explicit customisation guidance

### 2. Write the setup guide

Structure the guide as follows:

---

**Header:**
```
# {Product Name} — Setup Guide
```

**What's included:**
- Brief 2–3 sentence description of what the product does and who it's for.
- List what's in the product (tabs/pages/frames with one-line descriptions).

**Getting started:**
Step-by-step numbered list covering `buyer_flow` exactly. Use the actual tab/page/frame names from `structure`. Keep each step to 1–2 sentences. Plain language — write for someone who has never used this type of product before.

**How to use {each major feature}:**
One short section per major item in `feature_spec`. Explain:
- What the feature does
- How to use it (input → output)
- Any important notes or limitations

**Tips and common questions:**
Address the top 3–5 confusion points from `buyer_complaints` directly:
- Frame them as tips or FAQ items, not warnings
- Be specific and actionable

**Customisation:**
- How to change colours / fonts (product-type specific)
- What to change vs what not to touch (e.g. "don't delete formula cells in the Dashboard tab")

**Need help?**
- Brief note directing buyers to the shop's message/help channel

---

### 3. Write product-type specific guidance

_To add a new product type: duplicate the nearest section below and adapt it._

Include the following product-type specific content:

**Google Sheets:**
- "Make a copy" instructions: File → Make a copy → save to your Google Drive
- Warning: do not enter data in the original (view-only) — always work in your copy
- Mobile note: works best on desktop; mobile view is read-only
- Formula safety: which rows/columns contain formulas — do not delete these

**Notion:**
- "Duplicate" instructions: click Duplicate at top right → choose your workspace
- Note: requires a Notion account (free account works)
- Mobile note: Notion app on mobile gives full access
- If using relations: explain how they work briefly ("Tasks linked to Goals will automatically update the progress count")

**Canva:**
- "Use template" instructions: click Use template → opens in your Canva account
- Requires a free Canva account
- How to change colours: select element → Colour picker in toolbar
- How to change fonts: select text → Font picker in toolbar
- Export: File → Download → choose format (PDF recommended for print, PNG for digital)

---

## Output format

Write as clean Markdown. Save to `products/{slug}/docs/setup-guide.md`.

Use:
- `#` for the title
- `##` for main sections
- Numbered lists for step-by-step instructions
- Bullet lists for tips and feature descriptions
- Bold for important warnings or key terms
- No code blocks — this is a buyer-facing document, not technical docs

---

## Notes

- Use exact tab/page/frame names from `structure` — buyers will look for these by name.
- Keep language simple. Assume the buyer is not a spreadsheet/Notion/Canva power user.
- Do not repeat instructions that are already written inside the Instructions tab/page of the product itself — the setup guide is an external reference, not a duplicate.
- Length guide: 400–800 words. Long enough to be useful, short enough to be read.

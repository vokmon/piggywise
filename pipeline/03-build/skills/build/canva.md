# build/canva

Called by Stage 03 build-agent. Builds the product design in Canva from a blank design. Uses Canva MCP for all operations.

---

## Input

- `working_link` — link to the blank Canva design in the POC folder
- `feature_spec` — features/pages to implement
- `structure` — page/frame names and their purpose
- `style` — confirmed palette, font pairing, layout_style
- `differentiation` — items that must exist in the finished product
- `known_issues` — issues to address during build
- `slug`, `keyword`

---

## Steps

### 1. Pages per `structure`

For each page in `structure`: create the page, set the label matching `structure` names, populate content per `feature_spec`.

**Instructions / How to Use page (always present):** Create an instructions page (e.g. "How to Use This Template") covering: how to edit text, how to swap colours, how to replace images, export instructions.

**Editing transaction pattern (required for all content edits):**
1. `mcp__canva__start-editing-transaction`
2. `mcp__canva__perform-editing-operations`
3. `mcp__canva__commit-editing-transaction`

If something goes wrong mid-edit: call `mcp__canva__cancel-editing-transaction` and retry.

**Inline check (required after each page):** Export as PNG via `mcp__canva__export-design` and confirm it renders correctly before continuing.

### 2. Style

Apply palette and fonts across all pages. Check every page uses the same colour roles — flag any one-off colours outside the palette. Consistent heading size/weight and body text size (no more than 2–3 font sizes). Consistent margins (40–60px from page edges) and gap between sections.

### 3. Content

Replace all placeholder text with real content. Replace placeholder images using `mcp__canva__upload-asset-from-url` with a free image URL (Unsplash, Pexels).

### 4. Differentiation checklist

For each item in `differentiation[]`: confirm it exists in the design. Do not close this step until every item is confirmed present.

### 5. Final check

Export every page via `mcp__canva__export-design` (PNG). Verify:
- Consistent palette and typography across all pages
- No placeholder text remaining
- No broken or misaligned elements
- Instructions page covers the final design accurately

Return `working_link` to the calling agent.

---

## Notes

- Page names in Canva must match `structure` — buyers see these in the exported PDF.
- Canva has no formula logic — quality of writing in text frames matters as much as visual design.
- If a Canva MCP operation fails: export the current state and retry once before flagging as an issue.

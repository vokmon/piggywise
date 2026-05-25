# build/canva

Build or polish a Canva product. Called by both Stage 03 (poc-agent — rough prototype) and Stage 04 (build-agent — full polish). The caller's instructions determine the depth. This skill describes all possible build actions; the agent instructs which depth to apply.

Uses Canva MCP for all Canva operations.

---

## Input

- `working_link` — Canva design link to build on (scaffold copy or existing POC)
- `feature_spec` — array of features/pages to implement
- `structure` — planned page/frame names and their purpose
- `style` — confirmed palette, font pairing, layout_style
- `differentiation` — array of items that must exist in the finished product (Stage 04: treat as checklist)
- `gaps` — features to implement after differentiation is complete (Stage 04 only)
- `known_issues` — visual or content issues to fix before building anything new (Stage 04: fix first)
- `depth` — `rough` (Stage 03 POC) or `full` (Stage 04 polish)

---

## Build steps

### 1. Open the working design

Use `mcp__canva__get-design-pages` with `working_link` to read the current page list and confirm the starting state. Use `mcp__canva__export-design` to export pages as PNG for visual review.

### 2. Fix known issues (Stage 04 only)

If `depth` is `full` and `known_issues` is non-empty: fix every issue before adding anything new. Use `mcp__canva__export-design` to export each fixed page as PNG and confirm before continuing.

### 3. Build pages per `structure`

For each page in `structure`:
- Create the page if it doesn't exist.
- Set the page title/label matching `structure` names.
- Build out the content per `feature_spec`.

**Instructions / How to Use page (always present):**
- Always include a clear instructions page (e.g. "How to Use This Template", "Customisation Guide").
- Content: how to edit text, how to swap colours to a custom brand palette, how to replace placeholder photos, any export instructions.
- Style: clean, readable, matching the rest of the design.

**Editing transaction pattern (required for all content edits):**
Wrap every set of edits in a transaction:
1. `mcp__canva__start-editing-transaction` — open the transaction
2. `mcp__canva__perform-editing-operations` — apply edits (text, elements, positioning, style)
3. `mcp__canva__commit-editing-transaction` — persist the changes

If something goes wrong mid-edit: call `mcp__canva__cancel-editing-transaction` and retry.

**Content pages:**
- Apply `style.palette` consistently: primary background colour, accent colour for highlights, text colour.
- Apply `style.font` pairing: use heading font for titles/section headers, body font for all other text.
- Maintain consistent margins, padding, and alignment across all pages.
- Use `perform-editing-operations` (within a transaction) for element positioning — ensure consistent spacing and alignment within the design grid.
- Replace all placeholder text with appropriate sample content matching the product's purpose.
- Replace all placeholder images: use `mcp__canva__upload-asset-from-url` to upload relevant free images (source from Unsplash, Pexels, or similar free image sites). Browsing Canva's built-in stock library is not available via MCP.

**Inline check (required):** After building each page, use `mcp__canva__export-design` to export it as PNG and confirm it renders correctly before continuing.

### 4. Apply style

Apply `style` consistently across all pages:
- **Palette**: every page uses the same colour roles — no one-off colours outside the palette.
- **Typography**: consistent heading size and weight, consistent body text size. No more than 2–3 font sizes across the whole design.
- **Spacing**: consistent margins (suggest 40–60px from page edges), consistent gap between sections.
- **Visual rhythm**: pages should feel like they belong to the same set when viewed as a grid.

### 5. Verify `differentiation` checklist (Stage 04 only)

For each item in `differentiation[]`: confirm it exists in the built design. Mark it verified or note what's missing. Do not close this step until every item is confirmed present.

### 6. Fill `gaps` (Stage 04 only)

Implement each feature in `gaps[]` after all `differentiation[]` items are verified complete.

### 7. Final page review

Export every page via `mcp__canva__export-design` (PNG). Verify:
- Consistent palette and typography across all pages
- No placeholder text remaining
- No broken or misaligned elements
- Instructions page covers the final design
- Design looks polished at presentation size

---

## Depth guidance

| Area | `rough` (Stage 03 POC) | `full` (Stage 04 polish) |
|------|------------------------|--------------------------|
| Content | Placeholder text OK | All placeholder text replaced |
| Photography | Placeholder images OK | Relevant free stock images (Unsplash/Pexels via upload-asset-from-url) |
| Style consistency | Palette applied | Pixel-perfect consistency |
| Typography | Fonts applied | Hierarchy polished, sizes tuned |
| Instructions page | Basic notes | Complete buyer-facing guide |
| Alignment | Approximate | Grid-snapped, alignment-verified |
| Differentiation | Build all items | Verify every item explicitly |
| Gaps | Skip | Fill all after differentiation |

---

## Notes

- Canva MCP handles all design operations. Use `mcp__canva__export-design` for visual checks (PNG export) instead of Playwright.
- Never edit the original scaffold — always work on the copy.
- If a Canva MCP operation fails, export the current design state and retry once before noting in `known_issues`.
- For `rough` depth: placeholder images and approximate alignment are acceptable. Document gaps in `known_issues`.
- Page names in Canva must match `structure` — buyers see these in the exported PDF.
- Canva has no formula logic — all product value is visual and content-based. Quality of writing in text frames matters as much as visual design.

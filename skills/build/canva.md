# build/canva

Called by Stage 03 (poc-agent — `depth: "rough"`) and Stage 04 (build-agent — `depth: "verify"`). `rough`: creates the POC design from scratch. `verify`: checks the POC copy against spec and fixes only what's broken.

Uses Canva MCP for all Canva operations.

---

## Input

- `working_link` — Canva design link to build on (blank design for rough; Products/ copy for verify)
- `feature_spec` — array of features/pages to implement or verify
- `structure` — page/frame names and their purpose
- `style` — confirmed palette, font pairing, layout_style
- `differentiation` — array of items that must exist in the finished product
- `gaps` — deferred items to fill after all other checks pass
- `known_issues` — visual or content issues flagged during POC
- `depth` — `rough` (Stage 03 POC) or `verify` (Stage 04 verify-and-fix)

---

## Steps

### 1. Open the working design

Use `mcp__canva__get-design-pages` with `working_link` to read the current page list and confirm the starting state. Use `mcp__canva__export-design` to export pages as PNG for visual review.

### 2. Fix known issues

For each item in `known_issues`:
- **`rough`**: note them — do not block POC progress.
- **`verify`**: check if it is still present. If yes, fix it before continuing. Export the fixed page as PNG to confirm before moving on.

### 3. Pages per `structure`

For each page in `structure`:
- **`rough`**: create the page if it doesn't exist. Set the page label matching `structure` names. Populate content per `feature_spec`.
- **`verify`**: check the page exists and matches spec (label, content, no placeholder text remaining). Only create or update if something is missing or wrong.

**Instructions / How to Use page (always present):**
- **`rough`**: create an instructions page (e.g. "How to Use This Template", "Customisation Guide") with: how to edit text, how to swap colours, how to replace images, export instructions.
- **`verify`**: check the instructions page exists and covers all the above. Fix or add only what is missing.

**Editing transaction pattern (required for all content edits):**
1. `mcp__canva__start-editing-transaction` — open the transaction
2. `mcp__canva__perform-editing-operations` — apply edits
3. `mcp__canva__commit-editing-transaction` — persist changes

If something goes wrong mid-edit: call `mcp__canva__cancel-editing-transaction` and retry.

**Inline check (required after each page):** Export as PNG via `mcp__canva__export-design` and confirm it renders correctly before continuing.

### 4. Style

- **`rough`**: apply palette and fonts across all pages.
- **`verify`**: export all pages as PNG and check that palette, typography, spacing, and margins are consistent. Fix any page that deviates.

Check: every page uses the same colour roles — flag any one-off colours outside the palette.
Check: consistent heading size/weight and body text size — no more than 2–3 font sizes across the design.
Check: consistent margins (expect 40–60px from page edges) and consistent gap between sections.

### 5. Content

For each page:
- **`rough`**: placeholder text and images are acceptable.
- **`verify`**: check no placeholder text remains. Check all images are relevant (not generic stock placeholders). Fix any remaining placeholders.

To replace placeholder images: use `mcp__canva__upload-asset-from-url` with a free image URL (Unsplash, Pexels). Browsing Canva's built-in stock library is not available via MCP.

### 6. Differentiation checklist

For each item in `differentiation[]`: confirm it exists in the design. Note verified or missing. Do not close this step until every item is confirmed present.

### 7. Fill gaps

For each item in `gaps[]`: implement it after all differentiation items are confirmed. For `verify` depth — only fill gaps not already present.

### 8. Final page review

Export every page via `mcp__canva__export-design` (PNG). Verify:
- Consistent palette and typography across all pages
- No placeholder text remaining
- No broken or misaligned elements
- Instructions page covers the final design accurately
- Design looks polished at presentation size

Return `verify_result` to the calling agent:
- `passed[]` — items confirmed correct without changes
- `fixed[]` — items that had issues and were fixed
- `broken[]` — items that could not be fixed (should be empty)

---

## Depth guidance

| Area | `rough` (Stage 03 POC) | `verify` (Stage 04) |
|------|------------------------|----------------------|
| Pages | Create all pages | Check all pages exist + correct labels |
| Content | Placeholder text OK | No placeholders remaining |
| Photography | Placeholder images OK | Relevant free stock images |
| Style | Palette + fonts applied | Check consistency; fix deviating pages |
| Typography | Fonts applied | Verify hierarchy and sizes are consistent; fix only what deviates |
| Instructions page | Basic notes | Verify complete buyer-facing guide exists; fix if incomplete |
| Alignment | Approximate | Export + visually verify each page |
| Known issues | Note, don't block | Fix before continuing |
| Differentiation | Build all items | Verify every item present |
| Gaps | Skip | Fill after verification passes |

---

## Notes

- Canva MCP handles all design operations. Use `mcp__canva__export-design` for visual checks (PNG) instead of Playwright.
- If a Canva MCP operation fails, export the current design state and retry once before adding to `broken[]`.
- Page names in Canva must match `structure` — buyers see these in the exported PDF.
- Canva has no formula logic — all product value is visual and content-based. Quality of writing in text frames matters as much as visual design.

# build/notion

Called by Stage 03 (poc-agent — `depth: "rough"`) and Stage 04 (build-agent — `depth: "verify"`). `rough`: creates the POC from scratch. `verify`: checks the POC copy against spec and fixes only what's broken.

Uses Notion MCP for all Notion operations.

---

## Input

- `working_link` — Notion page link to build on (blank page for rough; Products/ copy for verify)
- `feature_spec` — array of features to implement or verify
- `structure` — pages/databases and their types
- `style` — confirmed palette, cover style, icon style, layout_style
- `differentiation` — array of items that must exist in the finished product
- `gaps` — deferred items to fill after all other checks pass
- `known_issues` — issues flagged during POC
- `logic_map` — formulas/relations built in the POC (`verify` only; null for `rough`)
- `depth` — `rough` (Stage 03 POC) or `verify` (Stage 04 verify-and-fix)

---

## Steps

### 1. Open the working page

Use `mcp__notion__notion-fetch` with `working_link` to read the current page structure and confirm the starting state. Take a Playwright **screenshot** for visual reference.

### 2. Fix known issues

For each item in `known_issues`:
- **`rough`**: note them — do not block POC progress.
- **`verify`**: check if it is still present. If yes, fix it before continuing. Verify the fix works.

### 3. Pages and databases per `structure`

For each item in `structure`:
- **`rough`**: create the page or database. Set title, icon, and cover per `style`.
- **`verify`**: check it exists and matches spec (name, icon, properties). Only create or update if something is missing or wrong.

**Instructions page (always present):**
- **`rough`**: create an Instructions page (or "Start Here" / "Setup Guide") covering: what the product does, step-by-step setup guide, what each database/view is for, any important notes about formulas, relations, or required manual steps. Use callout blocks (💡 icon) for important notes.
- **`verify`**: check the Instructions page exists and covers all the above. Fix or add only what is missing.

**Database properties:**
- **`rough`**: add all properties per `feature_spec` (name, type, options). For select/multi-select, create options in the correct order (order matters for sort).
- **`verify`**: check all properties exist with the correct name and type. Check select/multi-select options are present and in the correct order. Only add or fix what is missing or wrong.

**Views:**
- **`rough`**: create table view for data entry plus board/gallery/calendar as needed. Apply filter and sort defaults.
- **`verify`**: check all required views exist with correct filters, sorts, and grouping. Fix only what is wrong.

**Relations and rollups:**
- **`rough`**: create relations between databases as specified. Add rollup properties.
- **`verify`**: check each relation exists, points to the correct database, and has the correct backlink setting. Check each rollup targets the correct property and aggregation. Only fix what is wrong.

**Inline check (required after each database):** Create a test entry, verify it appears correctly in all views, delete it.

### 4. Formula properties

For each formula in `logic_map` (verify) or `feature_spec` (rough):
- **`rough`**: implement in Notion formula syntax. Test with 2–3 sample entries, delete test rows.
- **`verify`**: test the existing formula with 2–3 sample entries. If it produces correct output, move on — do not rewrite it. Only fix if it errors or returns wrong values.

**Inline check (required):** Verify 2–3 key formulas before continuing.

### 5. Style

- **`rough`**: set covers, icons, callout blocks, and palette on all pages.
- **`verify`**: check that covers, icons, palette, and layout are consistent across all pages. Fix any page that deviates.

Cover images: check the specified cover style is applied consistently across all top-level pages.
Icons: check the correct icon is set on each page per `style`.
Layout: check callout blocks, dividers, and column blocks are used appropriately.
Linked databases: check that embedded databases use linked views, not duplicates.

### 5a. Embed external tools (when specified in feature_spec)

Notion supports embedding external web apps via embed blocks.

**Reliable embed sources:**

| Tool | Embed URL |
|------|-----------|
| Pomodoro timer | `https://pomofocus.io` |
| Team Pomodoro | `https://cuckoo.team/{room-name}` |
| Google Calendar | Use the embed URL from Google Calendar → Settings → Integrate calendar |

- **`rough`**: add embeds using `mcp__notion__notion-update-page` with `insert_content`.
- **`verify`**: check if the embed block is already present. Only add if missing.

Note in the Setup Guide page that embeds require desktop or browser Notion — the mobile app may show a link instead.

### 6. Differentiation checklist

For each item in `differentiation[]`: confirm it exists in the product. Note verified or missing. Do not close this step until every item is confirmed present.

### 7. Fill gaps

For each item in `gaps[]`: implement it after all differentiation items are confirmed. For `verify` depth — only fill gaps not already present.

### 8. Final page review

Use `mcp__notion__notion-fetch` on each top-level page to verify:
- No broken relations, empty formula outputs, or missing views
- All views show data correctly with sample entries
- Instructions page covers the final structure accurately
- Style is consistent across all pages

Take a Playwright **screenshot** of each major page/view.

Return `verify_result` to the calling agent:
- `passed[]` — items confirmed correct without changes
- `fixed[]` — items that had issues and were fixed
- `broken[]` — items that could not be fixed (should be empty)

---

## Depth guidance

| Area | `rough` (Stage 03 POC) | `verify` (Stage 04) |
|------|------------------------|----------------------|
| Pages / databases | Create if not exists | Check exists + correct; fix only if wrong |
| Properties | Add core properties | Check all properties present and typed correctly |
| Views | 1–2 per database | Check all views exist with correct filters/sorts |
| Formulas | Implement and test | Test existing; only fix if broken or erroring |
| Style | Apply icons + covers | Check consistency; fix deviating pages |
| Known issues | Note, don't block | Fix before continuing |
| Differentiation | Build all items | Verify every item present |
| Gaps | Skip | Fill after verification passes |

---

## Notes

- Notion MCP handles all data operations. Playwright is used for screenshots only.
- Notion formula syntax differs from spreadsheet formulas — test every formula with actual data.
- For `verify` depth: if a relation or formula cannot be fixed after one retry, add it to `broken[]` and continue — do not loop indefinitely.
- Page and database names must match `structure` exactly — buyers see these names.

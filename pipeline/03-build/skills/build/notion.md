# build/notion

Called by Stage 03 build-agent. Builds the product in Notion from a blank page. Uses Notion MCP for all operations.

---

## Input

- `working_link` — link to the blank Notion page in the POC folder
- `feature_spec` — features to implement
- `structure` — pages/databases and their types
- `style` — confirmed palette, cover style, icon style, layout_style
- `differentiation` — items that must exist in the finished product
- `known_issues` — issues to address during build
- `slug`, `keyword`

---

## Steps

### 1. Pages and databases

For each item in `structure`: create the page or database. Set title, icon, and cover per `style`.

**Instructions page (always present):** Create a page named "Instructions" (or "Start Here") covering: what the product does, step-by-step setup guide, what each database/view is for, any important notes about relations or required manual steps. Use callout blocks (💡) for important notes.

**Database properties:** Add all properties per `feature_spec` (name, type, options). For select/multi-select, create options in the correct order.

**Views:** Create a table view for data entry plus board/gallery/calendar as needed per `feature_spec`. Apply filter and sort defaults.

**Relations and rollups:** Create relations between databases as specified. Add rollup properties. Do not use automations — they do not survive template duplication.

**Inline check (required after each database):** Create a test entry, verify it appears correctly in all views, delete it.

### 2. Formula properties

For each formula in `feature_spec`: implement in Notion formula syntax. Test with 2–3 sample entries, delete test rows.

**Inline check (required):** Verify 2–3 key formulas before continuing.

### 3. Style

Set covers, icons, callout blocks, and palette on all pages. Check that style is consistent across all top-level pages.

- Cover images: apply consistently across all top-level pages
- Icons: correct icon set on each page per `style`
- Linked databases: use linked views, not duplicates

### 4. Embed external tools (when specified in feature_spec)

| Tool | Embed URL |
|------|-----------|
| Pomodoro timer | `https://pomofocus.io` |
| Team Pomodoro | `https://cuckoo.team/{room-name}` |
| Google Calendar | Embed URL from Google Calendar → Settings → Integrate calendar |

Add embeds using `mcp__notion__notion-update-page` with `insert_content`. Note in the Instructions page that embeds require desktop or browser Notion — mobile may show a link instead.

### 5. Differentiation checklist

For each item in `differentiation[]`: confirm it exists in the product. Do not close this step until every item is confirmed present.

### 6. Final check

Use `mcp__notion__notion-fetch` on each top-level page to verify:
- No broken relations, empty formula outputs, or missing views
- All views show data correctly with sample entries
- Instructions page covers the final structure accurately
- Style is consistent across all pages

Return `working_link` to the calling agent.

---

## Notes

- Do not use automations — they do not survive template duplication.
- Notion formula syntax differs from spreadsheet formulas — test every formula with actual data.
- Page and database names must match `structure` exactly — buyers see these names.

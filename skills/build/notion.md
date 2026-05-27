# build/notion

Build or polish a Notion product. Called by both Stage 03 (poc-agent — rough prototype) and Stage 04 (build-agent — full polish). The caller's instructions determine the depth. This skill describes all possible build actions; the agent instructs which depth to apply.

Uses Notion MCP for all Notion operations.

---

## Input

- `working_link` — Notion page link to build on (blank page or existing POC)
- `feature_spec` — array of features to implement
- `structure` — planned pages/databases and their types
- `style` — confirmed palette, cover style, icon style, layout_style
- `differentiation` — array of items that must exist in the finished product (Stage 04: treat as checklist)
- `gaps` — features to implement after differentiation is complete (Stage 04 only)
- `known_issues` — issues to fix before building anything new (Stage 04: fix first)
- `logic_map` — actual formulas/relations built in the POC (Stage 04 only; null for Stage 03)
- `confirmed_done` — items from `logic_map` and `structure` verified as correct in the actual product (Stage 04 only; null for Stage 03). Skip reimplementation for these — validate only.
- `depth` — `rough` (Stage 03 POC) or `full` (Stage 04 polish)

---

## Build steps

### 0. Log in to Notion

Run `skills/notion-login.md`. If `logged_in: false`: stop and ask the human to set `NOTION_EMAIL` and `NOTION_PASSWORD` in `.env` before continuing.

### 1. Open the working page

Use `mcp__claude_ai_Notion__notion-fetch` with `working_link` to read the current page structure and confirm the starting state. Take a Playwright **screenshot** for visual reference.

### 2. Fix known issues (Stage 04 only)

If `depth` is `full` and `known_issues` is non-empty: fix every issue before adding anything new. After fixing each one, verify the fix works before continuing.

### 3. Build pages and databases per `structure`

For each item in `structure`:
- Create the page or database if it doesn't exist.
- Set the title, icon, and cover as specified in `style`.

**Instructions page (always present):**
- Always include an Instructions page (or "Start Here" / "Setup Guide").
- Content: what the product does, step-by-step setup guide, what each database/view is for, any important notes about formulas, relations, or required steps.
- Use callout blocks (💡 icon) for important notes.

**Database pages:**
- Add all properties per `feature_spec`: name, type (text, select, multi-select, date, checkbox, number, formula, rollup, relation).
- For select/multi-select: pre-populate with sensible default options.
- Create appropriate views: table view for data entry, board/gallery/calendar as needed per feature.
- Filter and sort views to show useful defaults (e.g. board view grouped by status, calendar view by date property).

**Relations and rollups:**
- Create relations between databases as specified in `structure`. If the relation already exists (check via `mcp__claude_ai_Notion__notion-fetch`), verify it is correct rather than recreating it.
- Add rollup properties to surface aggregated data. Same — check before creating.

**Inline check (required):** After building each database, create a test entry, verify it appears correctly in all views, then delete it.

### 4. Implement formula properties

For each formula property in `logic_map` (Stage 04) or `feature_spec` (Stage 03):
- If the formula is in `confirmed_done`: test it with 2–3 sample entries to confirm it still produces correct output. If it passes, move on — do not rewrite it.
- If the formula is not in `confirmed_done` or has no entry in `logic_map`: write it in plain language first, then implement it in Notion formula syntax. Test with 2–3 sample entries, delete test rows.

**Inline check (required):** Verify 2–3 key formulas after implementation before continuing.

### 5. Apply style

Apply `style` consistently:
- **Cover images**: use the specified cover style (gradient/solid colour/none) consistently across all top-level pages.
- **Icons**: set page icons using the specified icon style (emoji or custom).
- **Palette**: use Notion's page colour settings where applicable. For text emphasis, use the palette's accent colour.
- **Layout**: use callout blocks, dividers, and column blocks to create visual structure. Avoid long unbroken text blocks.
- **Linked databases**: where the same database is embedded on multiple pages, use linked database views (not duplicates).

### 5a. Embed external tools (when specified in feature_spec)

Notion supports embedding external web apps via embed blocks. Use these when the product includes interactive tools not available natively in Notion.

**Reliable embed sources:**

| Tool | Embed URL |
|------|-----------|
| Pomodoro timer | `https://pomofocus.io` |
| Team Pomodoro | `https://cuckoo.team/{room-name}` |
| Google Calendar | Use the embed URL from Google Calendar → Settings → Integrate calendar |

**How to add an embed via Notion MCP:**

Use `mcp__claude_ai_Notion__notion-update-page` with `insert_content` and the following markdown:

```
<embed url="https://pomofocus.io"/>
```

**Embed placement:** Put embeds on the most relevant feature page (e.g. a Pomodoro timer on the Today/Focus page, not the dashboard). Embed height is not controllable via MCP — it renders at Notion's default height.

**Notes:**
- Always note in the Start Here page that embeds require desktop or browser Notion — the mobile app may show a link instead of the live embed.
- Test the embed URL in a browser first to confirm it loads without a login wall.
- If the source requires login: use a styled link button (`[Open timer →](url)`) instead of an embed.

### 6. Verify `differentiation` checklist (Stage 04 only)

For each item in `differentiation[]`: confirm it exists in the built product. Mark it verified or note what's missing. Do not close this step until every item is confirmed present.

### 7. Fill `gaps` (Stage 04 only)

Implement each feature in `gaps[]` after all `differentiation[]` items are verified complete.

### 8. Final page review

Use `mcp__claude_ai_Notion__notion-fetch` on each top-level page to verify:
- No broken relations, empty formula outputs, or missing views
- All views show data correctly with sample entries
- Instructions page covers the final structure
- Style is consistent across all pages

Use Playwright to take a **screenshot** of each major page/view.

---

## Depth guidance

| Area | `rough` (Stage 03 POC) | `full` (Stage 04 polish) |
|------|------------------------|--------------------------|
| Properties | Core properties only | All properties, all types |
| Views | 1–2 per database | Full view set per feature_spec |
| Formulas | Working intent | Correct Notion formula syntax, tested |
| Style | Icons + covers set | Fully consistent, layout polished |
| Instructions page | Basic notes | Complete buyer-facing setup guide |
| Relations/rollups | Core relations | All relations + rollups verified |
| Differentiation | Build all items | Verify every item explicitly |
| Gaps | Skip | Fill all after differentiation |

---

## Notes

- Notion MCP handles all data operations (fetch, create, update, delete). Playwright is used for screenshots only.
- Notion formula syntax differs from spreadsheet formulas — test every formula with actual data before moving on.
- If a relation or rollup can't be made to work on the first attempt, note it in `known_issues` and continue.
- For `rough` depth: placeholder content is acceptable in non-critical pages. Document in `known_issues`.
- Page and database names must match `structure` exactly — buyers see these names.

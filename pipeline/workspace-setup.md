# workspace-setup

One-time setup and platform conventions for the PiggyWise pipeline. Run the setup steps once before starting any pipeline work. All agents reference this file for folder paths and file operations.

---

## Working folders

All working files live in dedicated folders — never mix study copies, POC builds, or final products in the same place.

| Artifact | Google Drive | Notion | Canva |
|---|---|---|---|
| Study copies (temp) | `PiggyWise/Study/` | `PiggyWise › Study` | `PiggyWise` project › `Study` folder |
| POC builds | `PiggyWise/POC/` | `PiggyWise › POC` | `PiggyWise` project › `POC` folder |
| QA copies (temp) | `PiggyWise/QA/` | `PiggyWise › QA` | `PiggyWise` project › `QA` folder |
| Final products | `PiggyWise/Products/` | `PiggyWise › Products` | `PiggyWise` project › `Products` folder |

**File naming:**
- Study copies: `[study] {original title}` — deleted after each study session ends
- POC builds: `[poc] {keyword}` — kept in POC folder permanently after commit
- QA copies: `[qa] {keyword}` — deleted when QA passes
- Test copies: `[test-{id}] {slug}` — deleted immediately after each test run
- Final products: `{keyword}` — no prefix

**Notion databases (tracking across stages):**

| Database | Location | Properties |
|---|---|---|
| POC | `PiggyWise › POC` | `slug` (title), `product_type` (select), `status` (select: `in-progress` / `committed`), `poc_page` (URL) |
| Products | `PiggyWise › Products` | `slug` (title), `product_type` (select), `status` (select: `in-progress` / `complete` / `paused`), `page` (URL) |
| QA | `PiggyWise › QA` | `slug` (title), `product_type` (select), `status` (select: `pending` / `in-progress` / `passed` / `failed`), `product_page` (URL), `qa_page` (URL) |

- POC row created at Stage 03 commit. Abandoned POCs are deleted entirely — no row created.
- Products row created at Stage 04 Step 10.
- QA row created at Stage 05 start; `qa_page` cleared when QA passes; QA copy deleted.

---

## Delivery formats per product type

| product_type | delivery_format |
|---|---|
| `google-sheets` | `google-sheets-link + xlsx-download` |
| `notion` | `notion-template-link` |
| `canva` | `canva-template-link + pdf-export` |

_To add a new product type: add a row above._

---

## Schema shapes per product type

Reference for `structure` and `logic_map` fields in poc-brief.json. Shape varies by product type.

| Field | google-sheets | notion | canva |
|---|---|---|---|
| `structure` | `{ "tabs": [...], "data_flows": [...], "notes": "..." }` | `{ "pages": [...], "databases": [...], "notes": "..." }` | `{ "pages": [...], "notes": "..." }` |
| `logic_map` | `{ "key_formulas": [{ "name", "location", "depends_on", "logic" }], "notes": "..." }` | `{ "formula_properties": [...], "rollups": [...], "notes": "..." }` | omit — set to `null` |

---

## Test execution reference

How to run tests per platform. Agents reference this table instead of repeating per-type steps inline.

| Platform | How to run tests |
|---|---|
| Canva | Use `mcp__canva__export-design` to export pages and inspect visually. |
| Notion | Use Notion MCP to create test entries and read back values. |
| Google Sheets — logic/edge case tests | Drive MCP is read-only. Ask the human to follow the test steps in the Sheet and report the result back. |
| Google Sheets — all other tests | Verify by reading the XLSX at `products/{slug}/delivery/{slug}.xlsx` or the uploaded Sheet via Drive MCP. |

---

## Visual review reference

How to visually review a built product per platform. Agents reference this table instead of repeating per-type steps inline.

| Platform | How to visually review |
|---|---|
| Canva | Export every page via `mcp__canva__export-design` (PNG). Review each export for broken elements, misaligned content, and placeholder text remaining. |
| Notion | Use `mcp__notion__notion-fetch` on each top-level page. Verify content completeness, style settings (covers, icons, palette), and that no placeholder content remains. |
| Google Sheets | Verify the XLSX exists at the expected output path. Ask the human to open the uploaded Google Sheet and confirm all tabs, formulas, and formatting render correctly. |

---

## File operations reference

How to copy, move, and create files per platform. Agents reference this table instead of repeating per-type steps inline.

### Copy an existing file into a folder

| Platform | How to copy |
|---|---|
| Google Sheets | File → Make a copy → choose destination folder in Drive |
| Notion | `...` menu → Duplicate → move to target parent page |
| Canva | Three-dot menu on design → Make a copy → move to target folder |

### Create a new blank file in a folder

| Platform | How to create |
|---|---|
| Google Sheets | Open destination Drive folder → New → Google Sheets |
| Notion | Open destination page → New page |
| Canva | Open destination folder → Create a design → choose dimensions |

### Move a file to a folder

| Platform | How to move |
|---|---|
| Google Sheets | Right-click in Drive → Move to → select folder |
| Notion | `...` menu → Move to → select parent page |
| Canva | Right-click design → Move to folder → select folder |

### Delete / trash a file

| Platform | How to delete |
|---|---|
| Google Sheets | Right-click in Drive → Move to trash |
| Notion | `...` menu → Delete |
| Canva | Right-click design → Move to trash |

---

## One-time platform setup

Create the following before running any pipeline stage for the first time.

### Google Drive

```
PiggyWise/
  Study/
  POC/
  QA/
  Products/
```

### Notion

```
PiggyWise  (top-level page — hub with links to all four sections below)
  ├── Study     (page)
  ├── POC       (page — contains POC database + [poc] pages)
  ├── QA        (page — contains QA database + [qa] pages)
  └── Products  (page — contains Products database + {keyword} pages)
```

The `PiggyWise` top-level page serves as the hub. It should contain visible links (or a simple nav callout) to Study, POC, QA, and Products so you can navigate the workspace from one place.

Database properties — see the **Notion databases** table in the Working folders section above.

### Canva

```
PiggyWise  (project)
  ├── Study    (folder)
  ├── POC      (folder)
  ├── QA       (folder)
  └── Products (folder)
```

---

## Adding a new product type

When adding support for a new product type, update all of the following:

**New files to create:**
- `skills/study/reverse-engineer/{type}.md`
- `skills/study/template-hunt/{type}.md`
- `skills/study/design-swipe/{type}.md`
- `skills/build/{type}.md`

**Existing files to update (add a row or section for the new type):**
- `skills/study/reverse-engineer.md` — add row to routing table
- `skills/study/template-hunt.md` — add row to routing table
- `skills/study/design-swipe.md` — add row to routing table
- `pipeline/04-build/skills/delivery-prep.md` — add per-type steps section
- `pipeline/04-build/skills/setup-guide.md` — add per-type guidance section
- `pipeline/04-build/skills/test-plan.md` — extend `applies_to` values as needed
- `pipeline/workspace-setup.md` — add row to delivery formats table, add column to schema shapes table if structure/logic differs, add `product_type` option to Notion Products database property (this file)

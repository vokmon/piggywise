# workspace-setup

Folder paths, naming conventions, and file operations for the PiggyWise pipeline. All agents reference this file.

---

## Working folders

| Artifact | Google Drive | Notion | Canva |
|---|---|---|---|
| Study copies (temp) | `PiggyWise/Study/` | `PiggyWise › Study` | `PiggyWise` project › `Study` folder |
| POC builds | `PiggyWise/POC/` | `PiggyWise › POC` | `PiggyWise` project › `POC` folder |
| Final products | `PiggyWise/Products/` | `PiggyWise › Products` | `PiggyWise` project › `Products` folder |

**File naming:**
- Study copies: `[study] {original title}` — deleted after each study session
- POC builds: `[poc] {keyword}` — kept in POC folder after commit
- Test copies: `[test-{id}] {slug}` — deleted immediately after each test run
- Final products: `{keyword}` — no prefix

---

## Notion tracking databases

| Database | Location | Properties |
|---|---|---|
| POC | `PiggyWise › POC` | `slug` (title), `product_type` (select), `status` (select: `in-progress` / `committed`), `poc_page` (URL) |
| Products | `PiggyWise › Products` | `slug` (title), `product_type` (select), `status` (select: `in-progress` / `complete` / `paused`), `page` (URL) |

- POC row created at Stage 03 commit. Abandoned POCs: no row created.
- Products row created at Stage 04.

---

## Delivery formats

| product_type | delivery_format |
|---|---|
| `google-sheets` | `google-sheets-link + xlsx-download` |
| `notion` | `notion-template-link` |
| `canva` | `canva-template-link + pdf-export` |

---

## File operations

| Action | Google Sheets | Notion | Canva |
|---|---|---|---|
| Copy | File → Make a copy → choose folder | `...` → Duplicate → move to target page | Three-dot menu → Make a copy → move to folder |
| Move | Right-click in Drive → Move to | `...` → Move to → select parent page | Right-click → Move to folder |
| Delete | Right-click in Drive → Move to trash | `...` → Delete | Right-click → Move to trash |
| New blank | Drive folder → New → Google Sheets | Open page → New page | Open folder → Create a design |

---

## One-time setup

### Google Drive
```
PiggyWise/
  Study/
  POC/
  Products/
```

### Notion
```
PiggyWise  (hub page)
  ├── Study     (page)
  ├── POC       (page — contains POC database)
  └── Products  (page — contains Products database)
```

### Canva
```
PiggyWise  (project)
  ├── Study    (folder)
  ├── POC      (folder)
  └── Products (folder)
```

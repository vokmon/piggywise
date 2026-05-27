# build/google-sheets

Called by Stage 03 (poc-agent — `depth: "rough"`) and Stage 04 (build-agent — `depth: "verify"`). Uses Python (openpyxl) to generate an XLSX file. `rough`: writes the script from scratch. `verify`: checks the POC output against spec and updates only what's broken.

For `rough`: write the generation script from scratch and produce the initial XLSX.
For `verify`: read the existing POC output, check it against spec, and update the script only for what fails.

---

## Input

- `slug` — product slug (used for file naming and output path)
- `keyword` — product keyword (used for Drive file naming)
- `working_link` — existing POC Google Sheets link (`verify` only; null for `rough`)
- `feature_spec` — array of features to implement or verify
- `structure` — planned tab names and data flows
- `style` — confirmed palette, font, layout_style
- `differentiation` — array of items that must exist in the finished product
- `gaps` — deferred items to fill after all other checks pass
- `known_issues` — issues flagged during POC
- `depth` — `rough` (Stage 03 POC) or `verify` (Stage 04 verify-and-fix)

---

## Steps

### 1. Review existing output (`verify` only)

If `depth` is `verify`: use `mcp__claude_ai_Google_Drive__read_file_content` to read the existing POC file at `working_link`. Note the current structure, tab names, and formula locations. This informs what needs fixing vs what can be kept.

Skip for `rough`.

### 2. Write or update the generation script

Script path:
- `rough`: `output/{slug}/03-poc/{slug}-build.py`
- `verify`: `products/{slug}/{slug}-build.py`

**For `rough`**: write the full script from scratch. The spec below describes everything to build.

**For `verify`**: start from the existing POC script at `output/{slug}/03-poc/{slug}-build.py`. Use the spec below only as a reference for what to check — do not rewrite sections that passed review in Step 1. Update only parts that failed or are listed in `known_issues`.

The script uses `openpyxl`. The spec below is the **`rough` build spec**. For `verify`, use it only as a checklist of what should already exist — do not execute these as instructions.

**Worksheets** (`rough`: create; `verify`: check tabs exist in correct order, first tab is `Instructions`)
- Tabs in the order specified by `structure.tabs`
- First tab must always be `Instructions`

**Instructions tab** (`rough`: write content; `verify`: check content is complete and buyer-facing)
- Product name as heading
- What the product does (1–2 sentences)
- Step-by-step setup guide: how to enter data, what each tab does, any formula notes

**Data tabs** (`rough`: create headers + freeze + widths; `verify`: check all present and correct)
- Row 1: headers, bold, background fill using `style.palette[0]`
- Freeze row 1 (`ws.freeze_panes = "A2"`)
- Column widths appropriate to data type

**Dashboard/Summary tab** (`rough`: write cross-tab formulas + charts; `verify`: check formulas exist and reference correct ranges)
- Cross-tab formulas referencing data tabs (e.g. `=SUM(Income!B2:B1000)`)
- Charts where specified in `feature_spec`

**Formulas** (`rough`: write with IFERROR + named ranges; `verify`: check IFERROR present, check named ranges, test outputs)
- Formula strings in Excel/Sheets syntax (e.g. `"=SUM(B2:B1000)"`)
- IFERROR wrapping on all formulas that could break on empty data
- Defined names via `workbook.defined_names` for cross-tab references

**Style** (`rough`: apply palette + fonts + borders; `verify`: check palette, fonts, row heights are consistent)
- Header fill: `PatternFill(fill_type="solid", fgColor=style.palette[0].lstrip("#"))`
- Accent fill: `style.palette[1]`
- Body background: `style.palette[2]`
- Font family: `style.font` for all cells
- Row heights: data rows 24–28pt, section header rows 32pt
- Thin borders on all data ranges
- Hide gridlines on display-only tabs: `ws.sheet_view.showGridLines = False`

**Data validation** (`rough`: add dropdowns + date/number validation; `verify`: check dropdowns exist on correct columns)
- `DataValidation` for dropdown fields (categories, status, type)
- Validate date and numeric fields where appropriate

At the top of the script, create the output directory:

```python
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)
```

Output file path:
- `rough`: `output/{slug}/03-poc/{slug}.xlsx`
- `verify`: `products/{slug}/delivery/{slug}.xlsx`

### 3. Run the script

Ensure `openpyxl` is installed:

```bash
pip install openpyxl
```

Then run:

```bash
python3 {script_path}
```

Confirm the XLSX was created. If the script errors: fix and re-run before continuing.

### 4. Ask human to upload

Present to the human:

> "XLSX generated at `{output_path}`. Please upload it to Google Drive:
> - **`rough`**: upload to `PiggyWise/POC/` folder, rename to `[poc] {keyword}`
> - **`verify`**: upload to `PiggyWise/Products/` folder, rename to `{keyword}`
>
> Once uploaded, share the editable Google Sheets link back."

Wait for the human to share the link. Set `working_link` to the received link.

### 5. Verify via MCP

Use `mcp__claude_ai_Google_Drive__read_file_content` to read the uploaded file. Check:
- All tabs present and in correct order
- Headers match `structure`
- Key formulas appear in expected locations
- Style matches `style` spec (palette, fonts, row heights)

For `verify` depth: compare against the known_issues list — confirm each one is now resolved.

### 6. Differentiation checklist

For each item in `differentiation[]`: confirm it is implemented. Note verified or missing.

### 7. Fill gaps

For any items in `gaps[]` not yet implemented: update the script, re-run it, ask the human to re-upload (replace existing file). Repeat until all gaps are filled.

### 8. Return `working_link` and `verify_result`

Return `working_link` to the calling agent.

For `verify` depth, also return `verify_result`:
- `passed[]` — items confirmed correct without changes
- `fixed[]` — items updated in the script and re-uploaded
- `broken[]` — items that could not be resolved (should be empty)

---

## Depth guidance

| Area | `rough` (Stage 03 POC) | `verify` (Stage 04) |
|------|------------------------|----------------------|
| Script | Write from scratch | Start from POC script; update only broken parts |
| Formulas | Working, simple | Verify IFERROR + named ranges present; fix only what's missing |
| Style | Palette applied, readable | Verify consistency across all tabs; fix only what deviates |
| Instructions tab | Basic notes | Verify complete buyer-facing setup guide exists; fix if incomplete |
| Data validation | Optional | Verify dropdowns + date/number validation present; add only what's missing |
| Known issues | Note, don't block | Fix before re-uploading |
| Differentiation | Build all items | Verify every item present |
| Gaps | Skip | Fill after verification passes |

---

## Notes

- If a fix is needed after upload: update the Python script, re-run, and ask the human to re-upload. Do not try to edit the Google Sheet directly.
- Keep the generation script in the repo — the product can be regenerated if needed.
- Cross-tab references use standard Sheets notation: `SheetName!CellRef` (e.g. `=SUM(Income!B2:B1000)`).
- `openpyxl` `defined_names` are recognised by Google Sheets when the XLSX is opened.

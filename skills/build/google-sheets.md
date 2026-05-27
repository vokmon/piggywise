# build/google-sheets

Build or polish a Google Sheets product by generating an XLSX file via Python (openpyxl). The agent writes a generation script, runs it to produce the file, then asks the human to upload it to Google Drive and share the link back.

Called by both Stage 03 (poc-agent — rough prototype) and Stage 04 (build-agent — full polish).

---

## Input

- `slug` — product slug (used for file naming and output path)
- `keyword` — product keyword (used for Drive file naming)
- `working_link` — optional; existing Google Sheets POC link for Stage 04 reference. Null for Stage 03.
- `feature_spec` — array of features to implement
- `structure` — planned tab names and data flows
- `style` — confirmed palette, font, layout_style
- `differentiation` — array of items that must exist in the finished product (Stage 04: treat as checklist)
- `gaps` — features to implement after differentiation is complete (Stage 04 only)
- `known_issues` — issues to address (Stage 04: must be fixed/improved in the new build)
- `depth` — `rough` (Stage 03 POC) or `full` (Stage 04 polish)

---

## Build steps

### 1. Review reference (Stage 04 only)

If `depth` is `full` and `working_link` is set: use `mcp__claude_ai_Google_Drive__read_file_content` to read the existing POC. Note what was built, what `known_issues` describe, and what needs improvement. This informs the script written in Step 2.

### 2. Write the generation script

Write the Python script to:
- Stage 03: `output/{slug}/03-poc/{slug}-build.py`
- Stage 04: `products/{slug}/{slug}-build.py`

The script uses `openpyxl`. Cover all of the following:

**Worksheets:**
- Create tabs in the order specified by `structure.tabs`
- First tab must always be `Instructions` — buyers see tab names, names must match `structure.tabs` exactly

**Instructions tab:**
- Product name as heading
- What the product does (1–2 sentences)
- Step-by-step setup guide: how to enter data, what each tab does, any formula notes

**Data tabs:**
- Row 1: headers, bold, background fill using `style.palette[0]`
- Freeze row 1 (`ws.freeze_panes = "A2"`)
- Column widths appropriate to data type

**Dashboard/Summary tab:**
- Cross-tab formulas referencing data tabs (e.g. `=SUM(Income!B2:B1000)`)
- Charts where specified in `feature_spec`

**Formulas:**
- Write formula strings in Excel/Sheets syntax (e.g. `"=SUM(B2:B1000)"`)
- Wrap all formulas that could break on empty data with IFERROR (e.g. `"=IFERROR(SUM(B2:B1000),0)"`)
- Use defined names via `workbook.defined_names` for cross-tab references — Google Sheets recognises these when the XLSX is opened

**Style:**
- Header fill: `PatternFill(fill_type="solid", fgColor=style.palette[0].lstrip("#"))`
- Accent fill: `style.palette[1]`
- Body background: `style.palette[2]`
- Font family: `style.font` for all cells
- Row heights: data rows 24–28pt, section header rows 32pt
- Thin borders on all data ranges
- Hide gridlines on display-only tabs: `ws.sheet_view.showGridLines = False`

**Data validation:**
- `DataValidation` for dropdown fields (categories, status, type)
- Validate date and numeric fields where appropriate

At the top of the script, create the output directory:

```python
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)
```

Output file path:
- Stage 03: `output/{slug}/03-poc/{slug}.xlsx`
- Stage 04: `products/{slug}/delivery/{slug}.xlsx`

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
> - **Stage 03**: upload to `PiggyWise/POC/` folder, rename to `[poc] {keyword}`
> - **Stage 04**: upload to `PiggyWise/Products/` folder, rename to `{keyword}`
>
> Once uploaded, share the editable Google Sheets link back."

Wait for the human to share the link. Set `working_link` to the received link.

### 5. Verify via MCP

Use `mcp__claude_ai_Google_Drive__read_file_content` to read the uploaded file. Verify:
- All tabs present and in correct order
- Headers match `structure`
- Key formulas appear in expected locations

### 6. Verify `differentiation` checklist (Stage 04 only)

For each item in `differentiation[]`: confirm it is implemented. Mark verified or note what's missing. Do not close this step until every item is confirmed.

### 7. Fill `gaps` (Stage 04 only)

For any `gaps[]` items not yet implemented: update the script, re-run it, ask the human to re-upload (replace the existing file in Drive). Repeat until all gaps are filled.

### 8. Return `working_link`

Return the confirmed `working_link` to the calling agent. This is used in all subsequent stages.

---

## Depth guidance

| Area | `rough` (Stage 03 POC) | `full` (Stage 04 polish) |
|------|------------------------|--------------------------|
| Formulas | Working but simple | Named ranges, IFERROR, all edge cases |
| Style | Palette applied, readable | Fully consistent, polished |
| Instructions tab | Basic notes | Complete buyer-facing setup guide |
| Data validation | Optional | Required for all input cells |
| Error handling | Minimal | All edge cases handled |
| Differentiation | Build all items | Verify every item explicitly |
| Gaps | Skip | Fill all after differentiation |

---

## Notes

- If a fix is needed after upload: update the Python script, re-run, and ask the human to re-upload. Do not try to edit the Google Sheet directly.
- Keep the generation script in the repo so the product can be regenerated if needed.
- Cross-tab references use standard Sheets notation: `SheetName!CellRef` (e.g. `=SUM(Income!B2:B1000)`).
- `openpyxl` `defined_names` are recognised by Google Sheets when the XLSX is opened — use them for readability.
- The calling agents (poc-agent, build-agent) must pass `slug` and `keyword` in addition to the standard build skill inputs.

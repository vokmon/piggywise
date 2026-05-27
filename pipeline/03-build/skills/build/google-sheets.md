# build/google-sheets

Called by Stage 03 build-agent. Generates the product as an XLSX file using Python (openpyxl), uploads to Google Drive, and returns the editable Sheets link.

---

## Input

- `slug` — product slug (used for file and script naming)
- `keyword` — product keyword (used for Drive file naming)
- `feature_spec` — features to implement
- `structure` — tab names and data flows
- `style` — confirmed palette, font, layout_style
- `differentiation` — items that must exist in the finished product
- `known_issues` — issues to address during build

---

## Steps

### 1. Write the generation script

Script path: `output/{slug}/03-build/{slug}-build.py`

The script uses `openpyxl`. Build the following:

**Worksheets**
- Tabs in the order specified by `structure.tabs`
- First tab must always be `Instructions`

**Instructions tab**
- Product name as heading
- What the product does (1–2 sentences)
- Step-by-step setup guide: how to enter data, what each tab does, any formula notes

**Data tabs**
- Row 1: headers, bold, background fill using `style.palette[0]`
- Freeze row 1 (`ws.freeze_panes = "A2"`)
- Column widths appropriate to data type

**Dashboard/Summary tab**
- Cross-tab formulas referencing data tabs (e.g. `=SUM(Income!B2:B1000)`)
- Charts where specified in `feature_spec`

**Formulas**
- IFERROR wrapping on all formulas that could break on empty data
- Defined names via `workbook.defined_names` for cross-tab references

**Style**
- Header fill: `PatternFill(fill_type="solid", fgColor=style.palette[0].lstrip("#"))`
- Accent fill: `style.palette[1]`
- Body background: `style.palette[2]`
- Font family: `style.font` for all cells
- Row heights: data rows 24–28pt, section header rows 32pt
- Thin borders on all data ranges
- Hide gridlines on display-only tabs: `ws.sheet_view.showGridLines = False`

**Data validation**
- `DataValidation` for dropdown fields (categories, status, type)
- Date and numeric validation where appropriate

Create the output directory at the top of the script:
```python
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)
```

Output file path: `output/{slug}/03-build/{slug}.xlsx`

### 2. Run the script

```bash
pip install openpyxl
python3 output/{slug}/03-build/{slug}-build.py
```

Confirm the XLSX was created. If the script errors: fix and re-run before continuing.

### 3. Ask human to upload

> "XLSX generated at `output/{slug}/03-build/{slug}.xlsx`. Please upload it to `PiggyWise/POC/` in Google Drive, rename to `[poc] {keyword}`, and share the editable Google Sheets link back."

Wait for the human to share the link. Set `working_link` to the received link.

### 4. Verify via MCP

Use `mcp__claude_ai_Google_Drive__read_file_content` to read the uploaded file. Check:
- All tabs present and in correct order
- Headers match `structure`
- Key formulas appear in expected locations
- Style matches `style` spec

### 5. Differentiation checklist

For each item in `differentiation[]`: confirm it is implemented.

### 6. Fill gaps

For any deferred items: update the script, re-run, ask the human to re-upload (replace existing file).

### 7. Return

Return `working_link` to the calling agent.

---

## Notes

- Keep the generation script in the repo — the product can be regenerated if needed.
- To fix anything: update the Python script, re-run, ask human to re-upload. Do not edit the Google Sheet directly.
- Cross-tab references use standard Sheets notation: `SheetName!CellRef` (e.g. `=SUM(Income!B2:B1000)`).
- `openpyxl` `defined_names` are recognised by Google Sheets when the XLSX is opened.

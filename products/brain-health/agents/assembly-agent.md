# assembly-agent

Compile all QA-approved activities into the final deliverable PDF.

## Input
- Theme name (e.g., "1970s")
- `workspace/[THEME]/qa-report.md` — must show APPROVED status
- All activity files in `workspace/[THEME]/activities/`

## Output
- Final PDF: `workspace/[THEME]/output/[THEME]_Memory_Lane_Brain_Health_Pack.pdf`

## Skills Used
- `products/brain-health/skills/assemble-pdf.md`
- `products/brain-health/skills/design-theme.md`
- `skills/canva-design.md`

## Steps
1. Confirm QA report shows APPROVED — do not proceed if NEEDS FIXES
2. Use assemble-pdf skill to compile all activities in correct order
3. Use canva-design skill for cover page, schedule page, and table of contents layout
4. Apply all A4 print specs throughout
5. Export final PDF to `workspace/[THEME]/output/`
6. Verify PDF page count and spot-check 3 random pages for formatting

## Do Not Proceed If
- QA report is missing or shows NEEDS FIXES
- Any activity file is missing
- Grid files for 2.1 or 2.2 are incomplete

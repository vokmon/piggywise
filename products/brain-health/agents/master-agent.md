# master-agent

Orchestrates the full end-to-end workflow for creating a complete brain health pack.

## Input
- Theme name (e.g., "1970s")

## Output
- Complete pack ready to list on Etsy:
  - Final PDF in `workspace/[THEME]/output/`
  - Cover + preview images in `workspace/[THEME]/images/`
  - Product video in `workspace/[THEME]/images/videos/`
  - Etsy listing data in `workspace/[THEME]/data/product_posts/`

## Agents Orchestrated
1. `research-agent` — find 10 topics for the theme
2. `content-agent` — generate all 9 activities
3. `qa-agent` — review and validate content
4. `assembly-agent` — compile final PDF
5. `pdf-qa-agent` — automated structural checks + human review checklist
6. `marketing-agent` — create cover images + Etsy listing
7. `marketing-qa-agent` — validate marketing assets + human review checklist

## Full Workflow
```
START: theme name given

STEP 1 → research-agent
  Input:  theme name
  Output: workspace/[THEME]/topics.md
  Gate:   10 topics confirmed

STEP 2 → content-agent
  Input:  theme name + topics.md
  Output: workspace/[THEME]/activities/ (all 9 files)
  Gate:   all 9 activity files exist

STEP 3 → qa-agent
  Input:  all activity files
  Output: workspace/[THEME]/qa-report.md
  Gate:   status = APPROVED
  If NEEDS FIXES → return to content-agent with specific issues

STEP 4 → assembly-agent
  Input:  activity files + qa-report (APPROVED)
  Output: workspace/[THEME]/output/[THEME]_Memory_Lane_Brain_Health_Pack.pdf
  Gate:   PDF exported successfully

STEP 5 → pdf-qa-agent
  Input:  final PDF + qa-report
  Output: workspace/[THEME]/pdf-qa-report.md
  Gate 1: automated checks = APPROVED
  Gate 2: human review sign-off (5–10 min — open checklist in pdf-qa-report.md)
  If NEEDS FIXES → return to assembly-agent with specific issues
  Do not proceed to marketing until human review is signed off

STEP 6 → marketing-agent
  Input:  theme name + final PDF + pdf-qa-report (APPROVED + human sign-off)
  Output: workspace/[THEME]/images/ + workspace/[THEME]/data/product_posts/
  Gate:   all assets generated successfully

STEP 7 → marketing-qa-agent
  Input:  all marketing assets + listing JSON
  Output: workspace/[THEME]/marketing-qa-report.md
  Gate 1: automated checks = APPROVED
  Gate 2: human review sign-off (10 min — open checklist in marketing-qa-report.md)
  If NEEDS FIXES → return to marketing-agent with specific issues

END: pack ready to list on Etsy
```

## Usage
```
Run master-agent with theme name: "1970s"
```

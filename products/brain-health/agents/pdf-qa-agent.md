# pdf-qa-agent

Review the assembled PDF for structural completeness, formatting accuracy, and print readiness.
This is a second QA pass — runs after assembly-agent, before marketing-agent.

## Input
- Theme name (e.g., "1970s")
- Final PDF: `workspace/[THEME]/output/[THEME]_Memory_Lane_Brain_Health_Pack.pdf`
- Content QA report: `workspace/[THEME]/qa-report.md` (must be APPROVED)

## Output
- PDF QA report: `workspace/[THEME]/pdf-qa-report.md`
- Status: APPROVED / NEEDS FIXES / AWAITING HUMAN REVIEW

---

## Automated Checks

### Structure & Completeness
- [ ] PDF opens without errors
- [ ] Page count is plausible (minimum 60 pages for 90 activities + front matter + answer key)
- [ ] Page 1: Cover page present with pack name and era imagery
- [ ] Page 2: "How to use this pack" page present
- [ ] Page 3: "My Progress" page present — includes Name field, Date started field, 28-day tick grid
- [ ] Page 4: 4-week guided schedule present — all 28 days listed with activity names and page numbers
- [ ] Page 5: Table of contents present with page numbers
- [ ] All 3 Set opener pages present with warm intro blurbs
- [ ] All 9 activity types present (1.1 through 3.3), each with 10 games/puzzles
- [ ] End-of-set celebration lines present after each set
- [ ] Completion certificate page present before the answer section
- [ ] Answer section separator page present ("How Did You Go?")
- [ ] Answer key TOC present with page references
- [ ] Answer pages present for all 9 activity types

### Headers & Footers
- [ ] Every activity page has a running header: `[Pack Name]  |  [Set Name]`
- [ ] Every activity page footer has: `Answers → p.[X]` (left) and `Page [N]` (right)
- [ ] Answer pages footer shows only `Page [N]` — no answer reference
- [ ] No footer answer references are blank (all filled in)

### Content Spot-Check (Sample 5 Random Pages)
- [ ] Game intro line present (warm, scene-setting)
- [ ] Instructions say "Here's how to play:" — not "Instructions:" or "Task:"
- [ ] Score box or completion celebration present at bottom of each game page
- [ ] Score box uses activity-specific warm phrasing — not "How did I do?"
- [ ] No exam language: "test", "exam", "pass", "fail", "must", "complete all"
- [ ] No age labels: "senior", "elderly", "older adult"
- [ ] Difficulty label present (★ Warm Up / ★★ Getting Going / ★★★ Brain Stretcher) on question-based games
- [ ] If page is a memory activity (1.1, 1.2, 1.3): round headers visible between question groups — no unbroken numbered list

### Answer Key Spot-Check (Sample 3 Random Answer Pages)
- [ ] Header says "How Did You Go?" — not "Answer Key"
- [ ] Each answer has a brief context line
- [ ] Page references match the activity pages

---

## Output Format

```
# PDF QA Report: [THEME]

Status: APPROVED / NEEDS FIXES / AWAITING HUMAN REVIEW

## Automated Checks: PASSED / FAILED
- [List any failed checks with page numbers]

## Issues Found
- p.[N]: [Issue description]

## Passed Checks
- [List of checks passed]

## Next Step
Automated checks passed. Proceed to human review using the checklist below.
```

---

## Human Review Checklist
*(Print this section or keep it open on screen while reviewing the PDF)*

Open the PDF and work through this list. Takes about 5–10 minutes.

### Visual Feel
- [ ] Cover feels warm and inviting — not clinical or childish
- [ ] Cover pack name is readable at thumbnail size (zoom out to 10% and check)
- [ ] Era colors look warm and appropriate — not muddy or washed out
- [ ] Activity pages feel spacious and uncluttered — not cramped
- [ ] Icons/doodles feel decorative — not distracting or out of place

### Readability
- [ ] Open to any activity page — does the font feel comfortably large?
- [ ] Print one activity page — is every word easy to read at arm's length?
- [ ] Print the same page in B&W — is everything still fully usable?
- [ ] Score box at the bottom of the page is clear and unambiguous
- [ ] Open to a word recall or trivia page — does it feel spacious and conversational, or like a wall of questions?

### Warmth & Tone
- [ ] Read the intro line of 3 random games — do they feel warm and inviting?
- [ ] Read the end-of-set celebration lines — do they feel genuine, not cheesy?
- [ ] Read the completion certificate — does it feel dignified and worth keeping?
- [ ] Read 3 random answer context lines — do they feel like a friend sharing a story?

### My Progress Page
- [ ] Name and Date started fields are large enough to write in
- [ ] 28-day tick boxes are large enough for an older hand to tick comfortably

### Overall
- [ ] Would you be happy to give this as a gift?
- [ ] Does it feel like something worth £12–£15?

### Sign Off
Reviewed by: _______________   Date: _______________
Status: ✅ Ready to publish  /  ❌ Needs changes → [note issues]

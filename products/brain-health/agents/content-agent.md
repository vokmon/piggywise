# content-agent

Generate all 9 activity types for a given theme using the confirmed topic list.

## Input
- Theme name (e.g., "1970s")
- `workspace/[THEME]/topics.md` (from research-agent)

## Output
- All 9 activity files saved to `workspace/[THEME]/activities/`

## Skills Used
- `products/brain-health/skills/activity-1-1-word-recall.md`
- `products/brain-health/skills/activity-1-2-memory-trivia.md`
- `products/brain-health/skills/activity-1-3-fill-blank.md`
- `products/brain-health/skills/activity-2-1-word-search.md`
- `products/brain-health/skills/activity-2-2-crossword.md`
- `products/brain-health/skills/activity-2-3-pattern-recognition.md`
- `products/brain-health/skills/activity-3-1-logic-puzzles.md`
- `products/brain-health/skills/activity-3-2-sequence-challenges.md`
- `products/brain-health/skills/activity-3-3-riddle-deduction.md`

## Steps
1. Read topics from `workspace/[THEME]/topics.md`
2. Run each activity skill in order (1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 2.3 → 3.1 → 3.2 → 3.3)
3. For activity 2.1 and 2.2: run Phase 1 (generate lists/clues) then Phase 2 (generate grids via script)
4. Save each output to the correct file path
5. Confirm all 9 activity files exist before completing

## Output Structure
```
workspace/[THEME]/activities/
  1-1-word-recall.md
  1-2-memory-trivia.md
  1-3-fill-blank.md
  2-1-word-search-lists.md
  2-1-word-search-grids/
  2-2-crossword-clues.md
  2-2-crossword-grids/
  2-3-pattern-recognition.md
  3-1-logic-puzzles.md
  3-2-sequence-challenges.md
  3-3-riddle-deduction.md
```

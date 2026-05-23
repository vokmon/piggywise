# activity-2-3-sudoku

Generate Sudoku Puzzles for Set 2: Focus & Concentration.

## Input
- Theme name (e.g., "1970s")
- Difficulty mix (default: 3 easy, 4 medium, 3 hard)

## Output
- 10 Sudoku puzzles with solutions
- Saved to: `workspace/[THEME]/activities/2-3-sudoku-grids/`

## Generate Puzzles (Python Script)

```bash
python products/brain-health/scripts/generate_sudoku.py \
  --output workspace/[THEME]/activities/2-3-sudoku-grids/ \
  --count 10 \
  --difficulty easy:3,medium:4,hard:3 \
  --seed 42
```

## Grid Specs (A4 Senior-Friendly)
- Standard 9×9 grid with bold 3×3 box borders
- Cell size: 14mm minimum — large enough to write a digit comfortably
- Given numbers: 18pt bold
- Empty cells: clean and clearly empty — no dots or dashes
- Bold lines between 3×3 boxes; thin lines between individual cells

## Quality Check
- Each puzzle has exactly one solution
- Difficulty mix: 3 easy (38+ givens), 4 medium (28–34 givens), 3 hard (22–26 givens)
- All 10 puzzles generated successfully with no errors

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines.

- **Game name format:** "The [Era] Sudoku — Puzzle [N]" — e.g., "The 1970s Sudoku — Puzzle 3"
- **Intro line:** Warm, no era knowledge needed — e.g., "A classic puzzle to clear your mind and sharpen your focus. No special knowledge needed — just logic and patience."
- **Instructions:** "Here's how to play: Fill every row, column, and bold-bordered box with the numbers 1 to 9. Each number appears exactly once in each. Take your time — there's no rush!"
- **No difficulty label** — sudoku difficulty is inherent in the puzzle itself
- **No score box** — completion celebration instead: "Completed it? Brilliant! ★"
- **No reflection prompt** — puzzle activity, skip it
- **Upside-down solution:** Print the completed 9×9 grid small (reduced size) at the very bottom of the page, rotated 180°, labelled "Solution ↕" in small grey text

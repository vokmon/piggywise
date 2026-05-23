# activity-3-2-crossnumber

Generate Crossnumber Puzzles for Set 3: Logic & Problem Solving.
Like a crossword, but every answer is a number — clues are era-themed facts and figures.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 crossnumber clue sets
- 10 crossnumber grids (generated via script)
- Saved to: `workspace/[THEME]/activities/3-2-crossnumber-clues.md` (clues)
- Saved to: `workspace/[THEME]/activities/3-2-crossnumber-grids/` (grids)

## Phase 1: Generate Clues

Generate era-themed clues whose answers are numbers (years, positions, quantities, durations).
Aim for 18–22 clues per puzzle to allow for ~14–18 to be placed in the grid.

### Good clue types
- **Years:** "Year ABBA won Eurovision" → 1974
- **Chart positions:** "Weeks 'Bohemian Rhapsody' spent in the UK Top 40" → 17
- **Counts:** "Number of members in ABBA" → 4
- **Prices:** "Price of a first-class stamp in 1971 (in pence)" → 3
- **Durations:** "Length in minutes of 'Bohemian Rhapsody'" → 6

### Input format for the script
```
## Game 1: 1970s Music
1974: Year ABBA won Eurovision with Waterloo
17: Weeks Bohemian Rhapsody spent in the UK charts
4: Number of members in ABBA
1975: Year Queen released Bohemian Rhapsody
...
```
Each line: `ANSWER: clue text` where ANSWER is a digit string (e.g., 1974, 17, 4).

## Phase 2: Generate Grids (Python Script)

Reuses the crossword generator — digit sequences are placed exactly like letter sequences:

```bash
python products/brain-health/scripts/generate_crossword.py \
  --input workspace/[THEME]/activities/3-2-crossnumber-clues.md \
  --output workspace/[THEME]/activities/3-2-crossnumber-grids/ \
  --cell-size 11
```

## Grid Specs (A4 Senior-Friendly)
- Grid size: 11×11 maximum
- Cell size: 11mm — large enough for a pencil digit
- Answer cells: white with thick border
- Blocked cells: solid black
- Clue numbers: 8pt

## Quality Check
- All answers are factually accurate for the theme era
- All answers are purely numeric digits (no letters)
- Mix of 1-digit, 2-digit, 3-digit, and 4-digit answers for grid variety
- At least 12 clues placed per puzzle (flag if fewer)

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines.

- **Game name format:** "The [Topic] Number Puzzle" — e.g., "The 1970s Music Number Puzzle"
- **Intro line:** e.g., "Every answer in this puzzle is a number from the 1970s. How many facts do you remember?"
- **Instructions:** "Here's how to play: Fill in the squares using the Across and Down clues. Every answer is a number. Use a pencil — and work across and down to help each other!"
- **No difficulty label** — crossnumbers are self-paced
- **Completion celebration:** "Filled every square? Absolutely brilliant! ★★★" — with "Clues solved: ___ / [N]"
- **No reflection prompt** — puzzle activity, skip it
- **Upside-down solution:** Print the completed grid small and rotated 180° at the very bottom of the page, labelled "Solution ↕" in small grey text

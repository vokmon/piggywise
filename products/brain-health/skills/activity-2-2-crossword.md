# activity-2-2-crossword

Generate Crossword Puzzles for Set 2: Focus & Concentration.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 crossword clue sets (25–30 clues each)
- 10 crossword grids (generated via script)
- Saved to: `workspace/[THEME]/activities/2-2-crossword-clues.md` (clues)
- Saved to: `workspace/[THEME]/activities/2-2-crossword-grids/` (grid files)

## Phase 1: Generate Clues
1. Open `docs/prompt_library.md` and copy the Activity 2.2 prompt template
2. Replace `[THEME]` and `[TOPIC 1–10]`
3. Run the prompt — output is clue lists only (not grids)
4. Save to `workspace/[THEME]/activities/2-2-crossword-clues.md`

## Phase 2: Generate Grids (Python Script)
Run the crossword grid generator script:
```bash
python scripts/generate_crossword.py \
  --input workspace/[THEME]/activities/2-2-crossword-clues.md \
  --output workspace/[THEME]/activities/2-2-crossword-grids/ \
  --cell-size 11
```

## Grid Specs (A4 Senior-Friendly)
- Grid size: 13×13 maximum
- Cell size: 11mm
- Answer cells: white with thick border
- Blocked cells: solid black
- Clue numbers: 8pt

## Quality Check
- All answer words are 3–12 letters
- Clues are clear and unambiguous
- No obscure references
- Mix of across and down clues
- Answer key on separate page

## Tone & Presentation
See `skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "The [Topic] Crossword" — e.g., "The 1970s TV Crossword"
- **Intro line:** e.g., "Every answer in this crossword takes you back to 1970s television. Grab a pencil and see how many you know!"
- **Instructions:** "Here's how to play: Fill in the squares using the Across and Down clues. Use a pencil — no one gets them all first try!"
- **No difficulty label** — crosswords are self-paced
- **Completion celebration instead of score box:** "Filled every square? Absolutely brilliant! ★★★" — with "Clues solved: ___ / [N]"
- **No reflection prompt** — puzzle activity, skip it

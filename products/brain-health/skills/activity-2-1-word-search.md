# activity-2-1-word-search

Generate Word Search Puzzles for Set 2: Focus & Concentration.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 word lists (30 words each)
- 10 word search grids (generated via script)
- Saved to: `workspace/[THEME]/activities/2-1-word-search-lists.md` (word lists)
- Saved to: `workspace/[THEME]/activities/2-1-word-search-grids/` (grid files)

## Phase 1: Generate Word Lists
1. Open `docs/prompt_library.md` and copy the Activity 2.1 prompt template
2. Replace `[THEME]` and `[TOPIC 1–10]`
3. Run the prompt — output is word lists only (not grids)
4. Save to `workspace/[THEME]/activities/2-1-word-search-lists.md`

## Phase 2: Generate Grids (Python Script)
Run the word search grid generator script:
```bash
python scripts/generate_word_search.py \
  --input workspace/[THEME]/activities/2-1-word-search-lists.md \
  --output workspace/[THEME]/activities/2-1-word-search-grids/ \
  --cell-size 12
```

## Grid Specs (A4 Senior-Friendly)
- Grid size: 15×15 maximum
- Cell size: 12mm
- Font: 14pt bold for letters
- Words hidden: horizontal, vertical, diagonal

## Quality Check
- All words are 4–15 letters
- No ambiguous or obscure words
- 30 words fit comfortably in the grid
- Answer key shows word locations

## Tone & Presentation
See `skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "The [Topic] Word Hunt" — e.g., "The 1970s Music Word Hunt"
- **Intro line:** Make it playful — e.g., "Thirty words from the 1970s music scene are hiding in this grid. Can you track them all down?"
- **Instructions:** "Here's how to play: Find all 30 hidden words — they can run across, down, or diagonally. Circle each one as you go. No rush!"
- **Word list:** Print the 30 words below the grid for reference
- **No difficulty label** — word searches are self-paced by nature
- **Completion celebration instead of score box:** "Found all 30? You're a legend! ★★★" at the bottom — with a small line "Words found: ___ / 30"
- **No reflection prompt** — puzzle activity, skip it

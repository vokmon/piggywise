# activity-3-3-riddle-deduction

Generate Riddle & Deduction Challenges for Set 3: Logic & Problem Solving.

## Input
- Theme name (e.g., "1970s")
- 10 category names for the riddles

## Output
- 10 Riddle & Deduction challenges
- Each riddle: mystery setup, 4–6 progressive clues, upside-down answer at page bottom
- Saved to: `workspace/[THEME]/activities/3-3-riddle-deduction.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 3.3 prompt template
2. Replace `[THEME]` and `[CATEGORY 1–10]`
3. Run the prompt in Claude/ChatGPT
4. Save full output to `workspace/[THEME]/activities/3-3-riddle-deduction.md`

## Quality Check
- All clues point to the same specific answer
- Clues progress from vague to specific
- Answer is unambiguous (one correct answer)
- No trick questions — straightforward deduction only
- Mix of difficulty across the 10 riddles

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Who or What Am I? [Topic]" — e.g., "Who or What Am I? 1970s Icons"
- **Intro line:** Build the mystery playfully — e.g., "I've got a few clues for you. Read them one at a time, and see if you can guess what I am before the last one!"
- **Instructions:** "Here's how to play: Read the clues one by one. Write your guess after each clue — or wait until the end. The earlier you guess, the more impressive!"
- **Difficulty label:** Top right of page
- **Score box:** "Riddles I cracked: ___ / 10" — bottom of page
- **Bonus line in score box:** "Guessed it from clue 1 or 2? Give yourself a bonus star! ★"
- **No reflection prompt** — deduction activity, skip it

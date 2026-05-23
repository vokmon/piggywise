# activity-3-2-sequence-challenges

Generate Sequence Challenges for Set 3: Logic & Problem Solving.

## Input
- Theme name (e.g., "1970s")
- 10 sequencing types for the theme

## Output
- 10 Sequence Challenge sets
- Each set: 5–7 sequencing tasks (chronological, ranking, logical)
- Answer key with brief explanation for each
- Saved to: `workspace/[THEME]/activities/3-2-sequence-challenges.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 3.2 prompt template
2. Replace `[THEME]` and `[SEQUENCING TYPE 1–10]`
3. Run the prompt in Claude/ChatGPT
4. Save full output to `workspace/[THEME]/activities/3-2-sequence-challenges.md`

## Quality Check
- Correct order is unambiguous (verifiable fact, not opinion)
- All items are from the theme era
- Mix of sequencing rules: chronological, by popularity, by logic
- Explanations are clear and brief
- No duplicate items across challenge sets

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Put It in Order: [Topic]" — e.g., "Put It in Order: 1970s Number Ones"
- **Intro line:** e.g., "These five songs all reached No. 1 in the 1970s — but can you put them in the right order from earliest to latest?"
- **Instructions:** "Here's how to play: Number the items in the correct order. Give it your best guess — you might remember more than you think!"
- **Difficulty label:** Top right of page
- **Score box:** "Sequences I sorted: ___ / [N]" — bottom of page
- **No reflection prompt** — logic activity, skip it

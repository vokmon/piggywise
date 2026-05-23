# activity-3-1-logic-puzzles

Generate Logic Puzzles for Set 3: Logic & Problem Solving.

## Input
- Theme name (e.g., "1970s")
- 10 scenario names set in the theme context

## Output
- 10 Logic Puzzles
- Each puzzle: scenario setup, 5–8 clues, 2–4 questions, upside-down answers at page bottom
- Saved to: `workspace/[THEME]/activities/3-1-logic-puzzles.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 3.1 prompt template
2. Replace `[THEME]` and `[SCENARIO 1–10]`
3. Run the prompt in Claude/ChatGPT
4. Save full output to `workspace/[THEME]/activities/3-1-logic-puzzles.md`

## Quality Check
- Each puzzle has exactly one correct solution
- Clues are non-contradictory
- Scenarios are interesting and era-appropriate
- Mix of difficulty levels
- Answers are unambiguous with clear explanations

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "The [Scenario] Mystery" — e.g., "The Disco Night Mystery"
- **Intro line:** Set the scene like a story — e.g., "It's a Saturday night in 1976. Five friends each brought a different vinyl record to the party. Can you figure out who brought what?"
- **Instructions:** "Here's how to play: Read the clues carefully, then answer the questions at the end. You can use the grid below to keep track. No rush — think it through!"
- **Difficulty label:** Top right of page
- **Score box:** "Mysteries I solved: ___ / [N]" — bottom of page
- **No reflection prompt** — logic activity, skip it

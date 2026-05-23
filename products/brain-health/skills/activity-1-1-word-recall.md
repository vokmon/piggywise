# activity-1-1-word-recall

Generate Word Recall Games for Set 1: Memory Enhancement.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 complete Word Recall Games
- Each game: 20 multiple-choice questions (4 options, 1 correct answer marked)
- Answer key at end of each game
- Saved to: `workspace/[THEME]/activities/1-1-word-recall.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 1.1 prompt template
2. Replace `[THEME]` with the theme name
3. Replace `[TOPIC 1–10]` with the 10 topics from research
4. Run the prompt in Claude/ChatGPT
5. Save full output to `workspace/[THEME]/activities/1-1-word-recall.md`

## Quality Check
- 20 questions per game × 10 games = 200 questions total
- All questions are factually accurate about the theme
- Mix of easy, medium, hard difficulty
- Each question has exactly one correct answer
- No duplicate questions across games

## Tone & Presentation
See `skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Remember When: [Topic]" — e.g., "Remember When: 1970s Music"
- **Intro line:** Set the scene before question 1 — reference a specific memory or feeling from the era
- **Instructions:** "Here's how to play: Read each question and circle the answer you think is right. Take your time — there's no rush!"
- **Difficulty label:** Top right of page (★ Warm Up / ★★ Getting Going / ★★★ Brain Stretcher)
- **Score box:** "How did I do? ___ / 20" — bottom of page
- **Reflection prompt:** Add after the last question: "Did any of these spark a memory? Jot it down:"

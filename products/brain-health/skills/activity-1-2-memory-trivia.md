# activity-1-2-memory-trivia

Generate Memory Trivia Games for Set 1: Memory Enhancement.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 complete Memory Trivia Games
- Each game: 15 open-ended recall questions (no multiple choice)
- Answer key at end of each game
- Saved to: `workspace/[THEME]/activities/1-2-memory-trivia.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 1.2 prompt template
2. Replace `[THEME]` with the theme name
3. Replace `[TOPIC 1–10]` with the 10 topics from research
4. Run the prompt in Claude/ChatGPT
5. Save full output to `workspace/[THEME]/activities/1-2-memory-trivia.md`

## Quality Check
- 15 questions per game × 10 games = 150 questions total
- All questions require genuine recall (not guessable without knowledge)
- Answers are specific facts, not opinions
- Mix of difficulty levels
- No duplicate questions across games

## Tone & Presentation
See `skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Do You Remember...? [Topic]" — e.g., "Do You Remember...? 1970s TV Shows"
- **Intro line:** Especially important here — open with a warm, nostalgic nudge that primes the memory before questions begin
- **Instructions:** "Here's how to play: Read each question and write your answer in the space below. Don't worry if you can't remember them all — just give it a go!"
- **Difficulty label:** Top right of page
- **Score box:** "How did I do? ___ / 15" — bottom of page
- **Reflection prompt:** This activity benefits most from the reflection prompt — always include the "Jot it down" lines after the last question

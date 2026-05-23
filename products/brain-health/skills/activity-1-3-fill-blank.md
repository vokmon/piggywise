# activity-1-3-fill-blank

Generate Fill-in-the-Blank Challenges for Set 1: Memory Enhancement.

## Input
- Theme name (e.g., "1970s")
- 10 category names (e.g., song lyrics, movie quotes, famous phrases)

## Output
- 10 complete Fill-in-the-Blank games
- Each game: 25 sentences with one or two blanks
- Answer key at end of each game
- Saved to: `workspace/[THEME]/activities/1-3-fill-blank.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 1.3 prompt template
2. Replace `[THEME]` with the theme name
3. Replace `[CATEGORY 1–10]` with category names (song lyrics, movie quotes, slogans, etc.)
4. Run the prompt in Claude/ChatGPT
5. Save full output to `workspace/[THEME]/activities/1-3-fill-blank.md`

## Quality Check
- 25 sentences per game × 10 games = 250 blanks total
- All items are famous or well-known from the theme era
- Blanks are specific words, not entire phrases
- Mix of difficulty (some famous, some moderately known)
- No duplicate sentences across games

## Tone & Presentation
See `skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Finish the Line: [Topic]" — e.g., "Finish the Line: 1970s Song Lyrics"
- **Intro line:** Reference the specific category — e.g., "These song lyrics defined the decade. How many can you finish from memory?"
- **Instructions:** "Here's how to play: Fill in the missing word or words. Say them out loud — sometimes that helps!"
- **Difficulty label:** Top right of page
- **Score box:** "How did I do? ___ / 25" — bottom of page
- **Reflection prompt:** Include after the last sentence — especially good for song lyrics and movie quotes

# activity-1-3-fill-blank

Generate Fill-in-the-Blank Challenges for Set 1: Memory Enhancement.

## Input
- Theme name (e.g., "1970s")
- 10 category names (e.g., song lyrics, movie quotes, famous phrases)

## Output
- 10 complete Fill-in-the-Blank games
- Each game: 25 sentences with one or two blanks, grouped into 5 rounds of 5
- Answer key at end of each game
- Saved to: `workspace/[THEME]/activities/1-3-fill-blank.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 1.3 prompt template
2. Replace `[THEME]` with the theme name
3. Replace `[CATEGORY 1–10]` with category names (song lyrics, movie quotes, slogans, etc.)
4. Run the prompt in Claude/ChatGPT
5. Save full output to `workspace/[THEME]/activities/1-3-fill-blank.md`

## Sentence Format

Each sentence has the blank embedded — the blank IS the answer space. No separate write line needed.

```
She wore an itsy bitsy teeny weeny yellow polka dot __________________.

Can you feel the love __________________ ?

We are family, I got all my __________________ with me.
```

A thin separator (———) sits between sentences. Round headers break the page into sections.
Items are not numbered across the full game — only 1–5 within each round.

### Writing good sentences
- Use only famous, well-known lines — the player should have a fighting chance from memory
- The blank should be a specific word or short phrase, not an entire line
- Leave enough of the sentence intact that it's clearly recognisable
- Keep it singable or speakable — these should feel like completing a memory, not filling a form

## Page Layout

Each game spans 2 pages (rounds 1–3 on page 1, rounds 4–5 on page 2):

**Page 1**
- Game name (top)
- Difficulty label (top right)
- Warm intro paragraph
- Round header: e.g., "— Round 1: [sub-topic] —"
- 5 sentences with embedded blanks, separated by thin rules
- Round 2 header + 5 sentences
- Round 3 header + 5 sentences

**Page 2**
- Round 4 header + 5 sentences
- Round 5 header + 5 sentences
- Reflection prompt after the last sentence
- Score box at the bottom

Round headers give the page visual rhythm — it never reads as a single numbered list.

## Quality Check
- 25 sentences per game × 10 games = 250 sentences total
- All items are famous or well-known from the theme era
- Blanks are specific words or short phrases, not entire lines
- Mix of difficulty — Round 1 easiest, Round 5 hardest
- No duplicate sentences across games

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Finish the Line: [Topic]" — e.g., "Finish the Line: 1970s Song Lyrics"
- **Intro line:** Reference the specific category warmly — e.g., "These song lyrics defined the decade. How many can you finish from memory?"
- **Instructions:** "Here's how to play: Fill in the missing word or words. Say them out loud — sometimes that's all it takes!"
- **Difficulty label:** Top right of page
- **Score box:** "Lines I finished: ___ / 25" — bottom of page 2
- **Reflection prompt:** Always include for this activity — especially powerful for song lyrics and movie quotes: "Did any of these take you right back? Write down the memory:"

# activity-1-2-memory-trivia

Generate Memory Trivia Games for Set 1: Memory Enhancement.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 complete Memory Trivia Games
- Each game: 15 open-ended recall questions, grouped into 3 rounds of 5
- No multiple choice — player writes their own answer
- Answer key at end of each game
- Saved to: `workspace/[THEME]/activities/1-2-memory-trivia.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 1.2 prompt template
2. Replace `[THEME]` with the theme name
3. Replace `[TOPIC 1–10]` with the 10 topics from research
4. Run the prompt in Claude/ChatGPT
5. Save full output to `workspace/[THEME]/activities/1-2-memory-trivia.md`

## Question Format

Each question follows this structure — no numbering within the full game, only within its round:

```
Can you remember [warm, conversational question]?

_____________________________________________

```

A generous write line sits directly below each question. A thin separator (———) between questions.
No answer options, no letters, no checkboxes — just a question and a line to write on.

### Writing good questions
- Phrase as "Can you remember..." / "Do you know..." / "What was the name of..."
- Ask about one specific fact (a name, a show, a song, a place)
- Keep it conversational — a question you'd ask a friend at the dinner table, not in a quiz bowl

## Page Layout

Each game spans 2 pages (Round 1 + 2 on page 1, Round 3 on page 2):

**Page 1**
- Game name (top)
- Difficulty label (top right)
- Warm intro paragraph
- Round header: e.g., "— Round 1: [sub-topic] —"
- 5 questions with write lines, separated by thin rules
- Round header: "— Round 2: [sub-topic] —"
- 5 questions with write lines

**Page 2**
- Round header: "— Round 3: [sub-topic] —"
- 5 questions with write lines
- Reflection prompt after the last question
- Score box at the bottom

Rounds give the page visual rhythm — it never reads as a single numbered list.

## Quality Check
- 15 questions per game × 10 games = 150 questions total
- Questions are warm and conversational, not quizzy or clinical
- Mix of easier and harder questions — Round 1 slightly easier, Round 3 slightly harder
- No duplicate questions across games

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Do You Remember...? [Topic]" — e.g., "Do You Remember...? 1970s TV Shows"
- **Intro line:** Open with a warm nostalgic nudge that primes the memory — reference a feeling or moment from the topic
- **Instructions:** "Here's how to play: Read each question and jot down whatever comes to mind. There's no time limit and no pressure — just enjoy the memories!"
- **Difficulty label:** Top right of page
- **Score box:** "How many came back to me? ___ / 15" — bottom of page 2
- **Reflection prompt:** Always include — this activity benefits most from it: "Did any of these bring back a story? Write it here:"

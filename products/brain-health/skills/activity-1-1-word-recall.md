# activity-1-1-word-recall

Generate Word Recall Games for Set 1: Memory Enhancement.

## Input
- Theme name (e.g., "1970s")
- 10 topic names for the theme

## Output
- 10 complete Word Recall Games
- Each game: 10 open-answer questions, grouped into 2 rounds of 5
- Each question has an optional whisper hint
- Upside-down suggested answers at the bottom of page 2
- Saved to: `workspace/[THEME]/activities/1-1-word-recall.md`

## Steps
1. Open `docs/prompt_library.md` and copy the Activity 1.1 prompt template
2. Replace `[THEME]` with the theme name
3. Replace `[TOPIC 1–10]` with the 10 topics from research
4. Run the prompt in Claude/ChatGPT
5. Save full output to `workspace/[THEME]/activities/1-1-word-recall.md`

## Question Format

Each question follows this exact structure — no numbering, no lettered options:

```
Do you remember [conversational question about the topic]?

Write it here: _________________________________

   Psst... [gentle nudge — not the answer, just a prod in the right direction]

```

A thin separator line (———) sits between questions.
The whisper hint is in smaller italic text, indented. It is clearly a nudge, not a set of options to choose from.

### Writing good questions
- Phrase as "Do you remember..." / "Can you recall..." / "What was the name of..."
- Ask about one specific thing (a name, a title, a place, a phrase)
- Keep it warm and curious — not quizzy or demanding

### Writing good hints
- Sound like a friend whispering a clue, not a test giving you options
- Point toward the answer without giving it away
- One short sentence, lowercase, casual tone
- Examples:
  - *Psst... think about a band named after a chess piece*
  - *Psst... she had a voice like no one else, and a very famous name*
  - *Psst... it started with the letter G and everyone danced to it*

## Page Layout

Each game spans 2 pages (5 questions per page = 1 round per page):

**Page 1**
- Game name (top)
- Difficulty label (top right)
- Warm intro paragraph
- Round header: e.g., "— Round 1: [sub-topic] —"
- 5 questions, each with write-here line + whisper hint, separated by thin rules

**Page 2**
- Round header: e.g., "— Round 2: [sub-topic] —"
- 5 questions
- Reflection prompt after the last question
- Score box at the bottom

This layout gives each question generous breathing room — nothing feels cramped or like a numbered exam list.

## Quality Check
- 10 questions per game × 10 games = 100 questions total
- All questions are factually accurate about the theme
- Mix of easy and harder questions across the 2 rounds (Round 1 slightly easier)
- Every hint is a nudge, not a giveaway and not a set of options
- No duplicate questions across games

## Tone & Presentation
See `products/brain-health/skills/activity-tone.md` for full guidelines. Activity-specific notes:

- **Game name format:** "Remember When: [Topic]" — e.g., "Remember When: 1970s Music"
- **Intro line:** Set the scene warmly — reference a specific feeling or memory from the topic
- **Instructions:** "Here's how to play: Read each question and write down whatever comes to mind. If you're stuck, the little hint below might jog your memory. No rush — just enjoy the trip down memory lane!"
- **Difficulty label:** Top right of page (★ Warm Up / ★★ Getting Going / ★★★ Brain Stretcher)
- **Score box:** "How many came back to me? ___ / 10" — bottom of page 2
- **Reflection prompt:** "Did any of these take you back? Jot down the memory:"

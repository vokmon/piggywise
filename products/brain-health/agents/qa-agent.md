# qa-agent

Review all generated activity content for accuracy, quality, and consistency.

## Input
- Theme name (e.g., "1970s")
- All activity files in `workspace/[THEME]/activities/`

## Output
- QA report saved to `workspace/[THEME]/qa-report.md`
- Status: APPROVED or NEEDS FIXES (with specific issues listed)

## Skills Used
- None (direct review)

## Checks to Perform

### Completeness
- [ ] All 9 activity types exist
- [ ] Each activity has exactly 10 variations
- [ ] All answer keys are present
- [ ] Activity 1.1: 10 questions per game × 10 games = 100 questions total
- [ ] Activity 1.2: 15 questions per game × 10 games = 150 questions total
- [ ] Activity 1.3: 25 sentences per game × 10 games = 250 sentences total

### Accuracy
- [ ] Facts are accurate for the theme era
- [ ] Answer keys match the questions
- [ ] Puzzle activities (crossword, word search, pattern, logic, sequence, riddle): one clear correct answer per question
- [ ] Open-answer activities (1.1, 1.2): answer key notes acceptable variations (e.g., "Queen" or "The Queen")

### Quality
- [ ] Mix of difficulty levels (easy, medium, hard) within each activity
- [ ] No duplicate questions within or across activities
- [ ] Language is clear and appropriate for seniors
- [ ] No offensive or controversial content

### Readability
- [ ] No question or instruction sentence exceeds 18 words
- [ ] No jargon, acronyms, or unexplained modern terms
- [ ] No color-dependent instructions (e.g., "circle the red option") — must work in B&W
- [ ] Font is Arial or Helvetica (not serif) — flag if prompt output specifies a serif font

### Tone & Enjoyment
- [ ] Every game has a warm intro line (1–2 sentences setting the scene)
- [ ] Instructions say "Here's how to play:" — not "Instructions:" or "Task:"
- [ ] No exam language anywhere: "test", "exam", "score", "pass", "fail", "must", "complete all"
- [ ] No age labels anywhere: "senior", "elderly", "older adult"
- [ ] Every game has a score box or completion celebration at the bottom
- [ ] Difficulty is mixed within each set — not all hard or all easy games in a row
- [ ] Reflection prompts present on memory-based activities (1.1, 1.2, 1.3)

### Answer Key
- [ ] Every answer has a brief context line where relevant (one sentence — the "why" behind the answer)
- [ ] Answer section header says "How Did You Go?" — not "Answer Key"
- [ ] Answer key TOC has correct page references

### Format
- [ ] Word search words are 4–15 letters
- [ ] Crossword answers are 3–12 letters
- [ ] Pattern sequences have logical rules with clear explanations

### Activity 1.1 (Word Recall)
- [ ] Every question has a whisper hint (one sentence, casual tone, not a giveaway)
- [ ] Questions are grouped into 2 rounds of 5 with round headers
- [ ] Questions phrased as "Do you remember..." / "Can you recall..." — not quizzy or demanding

### Activity 1.2 (Memory Trivia)
- [ ] Questions are grouped into 3 rounds of 5 with round headers
- [ ] Questions phrased conversationally — warm, not clinical

### Activity 1.3 (Fill-in-the-Blank)
- [ ] Blanks are embedded within sentences — not presented as separate questions
- [ ] Sentences are grouped into 5 rounds of 5 with round headers
- [ ] All sentences are famous or well-known from the theme era

## Output Format
```
# QA Report: [THEME]

Status: APPROVED / NEEDS FIXES

## Issues Found
- [Activity] [Game #]: [Issue description]

## Passed Checks
- [List of checks passed]
```

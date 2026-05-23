# research-agent

Research and confirm 10 topics for a given theme.

## Input
- Theme name (e.g., "1970s")

## Output
- Confirmed list of 10 diverse, senior-appropriate topics for the theme
- Saved to: `workspace/[THEME]/topics.md`

## Steps
1. Use research skill to find the most iconic aspects of the theme era
2. Draft 10 topic candidates covering a range of categories:
   music, TV, movies, events, fashion, food, sports, technology, culture, language
3. Verify each topic is well-known enough for seniors who lived through the era
4. Remove any obscure, offensive, or controversial topics
5. Finalize and save the 10 topics to `workspace/[THEME]/topics.md`

## Output Format
```
# Topics: [THEME]

1. [Topic Name] — [Brief description]
2. [Topic Name] — [Brief description]
...
10. [Topic Name] — [Brief description]
```

# template-hunt/notion

Study free Notion template galleries to harvest structural and UX patterns for the build. Study up to `max_templates` candidates. Extract the best pattern(s) from each. Build fresh from these patterns — do not copy any single template wholesale.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `feature_spec` — always `null` at call time (synthesis happens after this skill runs); pattern extraction is done against the keyword and competitor structures from the reverse-engineer step instead
- `max_templates` — maximum number of candidates to study
- `keyword` — the validated keyword (used as search seed)

---

## Steps

### 0. Log in to Notion

Run `skills/notion-login.md`. If `logged_in: false`: stop and ask the human to set `NOTION_EMAIL` and `NOTION_PASSWORD` in `.env` before continuing.

### 1. Search for candidates

Search these sources in order. Collect up to `max_templates` candidates across all sources:

1. **Notion official gallery** — `https://www.notion.so/templates`
   Search for `{keyword}` or browse the relevant category. Filter to free templates — skip any that require a paid Notion plan to copy.

2. **NotionPages.com** — search `site:notionpages.com {keyword}` or browse `https://notionpages.com/`
   All templates here are free to copy.

3. **Pinterest** — search `{keyword} notion template free`

For each candidate found: take a **screenshot** of the listing/preview page.

### 2. Study each candidate

For each candidate:

1. Copy the template into the Notion workspace using Playwright:
   - Navigate to the template URL
   - Click "Start with this template" (or "Duplicate" / "Get template")
   - Wait for the copy to appear in the workspace (~3s)
   - Note the new page URL/ID

2. Study the copy using `mcp__claude_ai_Notion__notion-fetch`. Extract:
   - **Page structure** — what top-level pages exist? What is the navigation model?
   - **Database design** — what databases are present, what properties (name and type), what views (table/board/gallery/calendar)?
   - **Dashboard layout** — how is the main hub page organised? Linked views, callouts, columns?
   - **Formulas and relations** — any notable computed properties or cross-database relations?
   - **UX patterns** — what makes this template easy or hard to use? Callout usage, toggles, inline databases, embed blocks?
   - **Visual style** — cover style, icon choices, colour palette, layout density
   - **Specific patterns worth borrowing** — the 1–2 things this template does better than others

3. **Trash the copy** using `mcp__claude_ai_Notion__notion-update-data-source` with `in_trash: true` and the page ID noted in sub-step 1 above. Always clean up before moving to the next candidate.

### 3. Compile pattern library

Across all studied candidates, compile a `pattern_library[]`: one entry per candidate with the specific pattern(s) worth borrowing. Also write a `structure_summary` identifying the most common structural patterns and any differentiation opportunities.

Do NOT select a single "best" template to copy. The build step assembles patterns from multiple sources into a fresh product.

---

## Output

```json
{
  "pattern_library": [
    {
      "url": "https://www.notion.so/templates/...",
      "source": "notion-gallery",
      "title": "ADHD Daily Planner by X",
      "patterns_to_borrow": [
        "3-column dashboard layout with Today / This Week / Brain Dump columns",
        "Habit tracker with streak formula using dateBetween()"
      ],
      "notes": "Best dashboard layout of all candidates. Overcomplicated elsewhere — ignore tab structure outside the dashboard."
    },
    {
      "url": "https://notionpages.com/...",
      "source": "notionpages",
      "title": "Focus Flow Template",
      "patterns_to_borrow": [
        "Embedded Pomodoro timer (pomofocus.io embed block) directly on the focus page"
      ],
      "notes": "Weak overall structure but the embed approach is clean and easy to replicate."
    }
  ],
  "structure_summary": {
    "common_pages": ["Dashboard", "Tasks", "Habits", "Notes/Brain Dump", "Setup Guide"],
    "common_databases": ["Tasks/To-Do", "Habits", "Mood/Journal"],
    "common_features": ["Daily focus view", "Habit streak tracking", "Quick capture"],
    "visual_patterns": ["Emoji icons dominant", "Callout boxes as visual anchors", "Gallery view feels more premium than table view"],
    "differentiation_opportunities": ["Pre-filled sample data (none of the studied templates include this)", "Built-in Notion onboarding (all assume Notion familiarity)"]
  }
}
```

---

## Notes

- Always trash each study copy before moving to the next candidate — keep the workspace clean.
- Study all `max_templates` candidates before compiling — do not stop at the first strong match.
- If a template requires a paid Notion plan to copy: skip immediately — do not record.
- `patterns_to_borrow` must be specific and actionable — not "good design" but "3-column layout with linked database views of Tasks and Habits".
- If a source is blocked or returns no useful results: skip it and note it, continue to next source.

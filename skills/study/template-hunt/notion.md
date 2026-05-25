# template-hunt/notion

Search free Notion template galleries to find the best scaffold candidate for the POC. Evaluate up to `max_templates` candidates. Pick the best one. Do NOT duplicate — just record the choice. Duplication happens in poc-agent after synthesis confirms the planned structure.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `feature_spec` — always `null` at call time (synthesis happens after this skill runs); evaluation is done against the keyword and competitor structures from the reverse-engineer step instead
- `max_templates` — maximum number of candidates to evaluate
- `keyword` — the validated keyword (used as search seed)

---

## Steps

### 0. Log in to Notion

Run `skills/notion-login.md`. If `logged_in: false`: stop and ask the human to set `NOTION_EMAIL` and `NOTION_PASSWORD` in `.env` before continuing.

### 1. Search for candidates

Search these sources in order. Collect up to `max_templates` candidates across all sources (stop when you have enough to evaluate):

1. **Notion official gallery** — `https://www.notion.so/templates`
   Search for `{keyword}` or browse the relevant category. Filter to free templates — skip any that require a paid Notion plan to duplicate.

2. **NotionPages.com** — search `site:notionpages.com {keyword}` or browse `https://notionpages.com/`
   All templates here are free to duplicate.

3. **Pinterest** — search `{keyword} notion template free`

For each candidate found: take a **screenshot** of the listing/preview page.

### 2. Evaluate each candidate

For each candidate, assess:
- **Structural fit** — how closely does the page/database structure match the keyword and competitor structures from the reverse-engineer step?
- **Database complexity** — are the databases, properties, and relations at the right level to adapt?
- **Visual starting point** — is it neutral enough to restyle, or too heavily customised?
- **Freely available** — does "Duplicate" work without a paid Notion plan? If it requires a paid plan: skip immediately — do not score or record.

Score each candidate: `strong_fit` / `partial_fit` / `poor_fit`.

### 3. Pick the best candidate

Select the single candidate with the strongest structural fit to the keyword and competitor structures from the reverse-engineer step. If two candidates are equal, prefer the one from an earlier source (Notion gallery > NotionPages > Pinterest).

If no candidate scores at least `partial_fit`: return `null` and note "build from scratch — no suitable scaffold found".

### 4. Record result

Record the chosen candidate (and all evaluated candidates) in the output. Do NOT duplicate the template — just record the URL and decision.

---

## Output

```json
{
  "templates": [
    {
      "url": "https://www.notion.so/templates/...",
      "source": "notion-gallery",
      "title": "Personal Finance Dashboard",
      "fit": "strong_fit",
      "used_as_scaffold": true,
      "notes": "Has Income and Expenses databases with category properties. Dashboard page with rollups. Matches keyword and competitor structure well. Clean design easy to restyle."
    },
    {
      "url": "https://notionpages.com/...",
      "source": "notionpages",
      "title": "Budget Tracker Notion Template",
      "fit": "partial_fit",
      "used_as_scaffold": false,
      "notes": "Single database only — no dashboard. Too simple for keyword and competitor structure."
    }
  ],
  "scaffold_url": "https://www.notion.so/templates/...",
  "scaffold_source": "notion-gallery"
}
```

If no suitable scaffold:

```json
{
  "templates": [
    {
      "url": "https://notionpages.com/...",
      "source": "notionpages",
      "title": "Basic Expense Log",
      "fit": "poor_fit",
      "used_as_scaffold": false,
      "notes": "Just a simple table — no properties, no views, no relations. Does not match keyword or competitor structure."
    }
  ],
  "scaffold_url": null,
  "scaffold_source": null
}
```

---

## Notes

- Do NOT duplicate the scaffold template yet — that happens in poc-agent after synthesis.
- `used_as_scaffold: true` on exactly one entry (or none if `scaffold_url` is null).
- Evaluate all candidates before picking — do not stop at the first `strong_fit`.
- If a template requires a paid Notion plan to duplicate: skip immediately — do not score or record.
- If a source is blocked or returns no useful results: skip it and note it, continue to next source.

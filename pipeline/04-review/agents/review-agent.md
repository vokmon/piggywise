# review-agent

Reviews a product before marketing. You give a link or path — the agent checks formulas, data relationships, and cross-references, then reports every issue found. You fix; the agent re-checks if asked.

---

## How to invoke

> "Review [link or path]"

---

## Checks

### Google Sheets

- Every formula resolves without error (`#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, etc.)
- Cross-tab references point to the correct sheet and range
- Named ranges are defined and point to valid ranges
- Data validation rules are intact and no cells show validation errors

### Notion

**Logic checks:**
- Formula properties compute a value (no `Error` state)
- Relation properties link to a database that is inside the template root (not an external database the buyer won't receive)
- Rollup properties are configured on a valid relation

**Duplication checks — flag anything that breaks when the buyer duplicates the template:**
- **Automations** — do not survive duplication; must be removed from the template
- **Synced blocks** — stay synced to the original page; buyer gets a broken sync
- **Linked database views** (databases pulled from outside the template) — buyer won't have the source database
- **Integration connections** — do not transfer to the buyer's workspace

### Canva

- All pages export without error
- No placeholder text remaining on any page

---

## How to report

List every issue grouped by category. For each issue:

- **Where** — tab / page / property name
- **What** — plain description of the problem
- **Why it matters** — what breaks for the buyer

Wait for the human to fix. Re-run checks after fixes if asked.

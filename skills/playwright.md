# playwright

Shared guidance for all skills that use Playwright to browse the web. Every Playwright-using skill follows these rules.

---

## Screenshot vs Snapshot

| Use            | When                                                                                                                              |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Screenshot** | Search result listings, shop pages, product tiles — these render via JavaScript and often do not appear in the accessibility tree |
| **Snapshot**   | Dropdowns, autocomplete suggestions, filter chips, navigation elements — these are in the DOM and captured reliably by snapshot   |
| **Both**       | When you need structure (snapshot) and visual confirmation (screenshot) — take snapshot first, screenshot if listings are missing |

Default to screenshot when reading page content. Use snapshot only when targeting specific interactive elements.

---

## Handling Blocks and Captchas

- If a page shows a captcha, bot-detection screen, or redirects to an error: note it, do not retry more than once.
- Return `"source": "blocked"` in the skill output.
- The calling agent decides whether to stop or continue with partial data — the skill never stops the pipeline itself.

---

## Cleanup

Playwright saves screenshots, snapshots, and console logs to `.playwright-mcp/`. Individual skills do not clean up — the calling **agent** runs cleanup after all skills complete:

```bash
find .playwright-mcp -delete
```

Run this as the final step in every agent that uses Playwright skills.

If you need to save any intermediate files to disk, save them directly to the calling agent's output folder — never to the project root.

---

## General Rules

- Always include `explicit=1` in Etsy URLs to avoid safe-search filtering affecting results.
- Skip physical products in digital download searches — check title and "Digital download" label.
- Do not retry a blocked URL more than once — move on.

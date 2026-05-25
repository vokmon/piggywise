# template-hunt/canva

Search free Canva template galleries to find the best scaffold candidate for the POC. Evaluate up to `max_templates` candidates. Pick the best one. Do NOT copy — just record the choice. Copying happens in poc-agent after synthesis confirms the planned structure.

Follows `skills/playwright.md` for screenshot/snapshot rules.

## Input

- `feature_spec` — always `null` at call time (synthesis happens after this skill runs); evaluation is done against the keyword and competitor structures from the reverse-engineer step instead
- `max_templates` — maximum number of candidates to evaluate
- `keyword` — the validated keyword (used as search seed)

---

## Steps

### 0. Log in to Canva

Run `skills/canva-login.md`. If `logged_in: false`: stop and ask the human to set `CANVA_EMAIL` and `CANVA_PASSWORD` in `.env` before continuing.

### 1. Search for candidates

Search these sources in order. Collect up to `max_templates` candidates across all sources (stop when you have enough to evaluate):

1. **Canva template gallery** — `https://www.canva.com/templates/`
   Search for `{keyword}` and filter to free templates.

2. **Pinterest** — search `{keyword} canva template free`
   Pinterest results should lead to Canva template pages — only collect candidates that resolve to an actual Canva template URL.

For each candidate found: take a **screenshot** of the listing/preview page.

### 2. Evaluate each candidate

For each candidate, assess:
- **Page/frame fit** — how closely does the page count and structure match the keyword and competitor structures from the reverse-engineer step?
- **Layout adaptability** — is the layout flexible enough to restyle for any palette/font?
- **Element quality** — are the design elements (icons, shapes, typography) of sufficient quality?
- **Freely available** — no Pro lock (free Canva template, not Canva Pro required). If paywalled: skip immediately — do not score or record.

Score each candidate: `strong_fit` / `partial_fit` / `poor_fit`.

### 3. Pick the best candidate

Select the single candidate with the strongest structural fit to the keyword and competitor structures from the reverse-engineer step. If two candidates are equal, prefer the one from Canva template gallery (easier to copy directly).

If no candidate scores at least `partial_fit`: return `null` and note "build from scratch — no suitable scaffold found".

### 4. Record result

Record the chosen candidate (and all evaluated candidates) in the output. Do NOT copy the template — just record the URL and decision.

---

## Output

```json
{
  "templates": [
    {
      "url": "https://www.canva.com/templates/...",
      "source": "canva-gallery",
      "title": "Media Kit Canva Template",
      "fit": "strong_fit",
      "used_as_scaffold": true,
      "notes": "7 pages matching keyword and competitor structure. Clean neutral design — easy to restyle to any palette. Free template, no Pro lock."
    },
    {
      "url": "https://www.canva.com/templates/...",
      "source": "pinterest",
      "title": "Business Proposal Template",
      "fit": "partial_fit",
      "used_as_scaffold": false,
      "notes": "Found via Pinterest. 5 pages — missing key section. Weaker structural fit than first candidate."
    }
  ],
  "scaffold_url": "https://www.canva.com/templates/...",
  "scaffold_source": "canva-gallery"
}
```

If no suitable scaffold:

```json
{
  "templates": [
    {
      "url": "https://www.canva.com/templates/...",
      "source": "canva-gallery",
      "title": "Basic Business Card",
      "fit": "poor_fit",
      "used_as_scaffold": false,
      "notes": "Wrong format entirely — single page, not a multi-page kit. Does not match keyword or competitor structure."
    }
  ],
  "scaffold_url": null,
  "scaffold_source": null
}
```

---

## Notes

- Do NOT copy the scaffold template yet — that happens in poc-agent after synthesis.
- `used_as_scaffold: true` on exactly one entry (or none if `scaffold_url` is null).
- Evaluate all candidates before picking — do not stop at the first `strong_fit`.
- If a source is blocked or returns no useful results: skip it and note it, continue to next source.

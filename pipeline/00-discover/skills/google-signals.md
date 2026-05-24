# google-signals

Use Gemini CLI to identify broad trending categories in the digital products and productivity tools space. This is a lightweight signal check — not the deep per-seed analysis done in Stage 01. Goal: find which broad niches have Google search momentum right now, so the seed-ranker can prioritise candidates that have demand from outside Etsy too.

## Input
- `niche_description` — plain-English description of the target product space

## Steps

### 1. Run Gemini broad trend query

```bash
gemini -p "Using Google Search, what are the most searched and fastest-growing categories right now for: {niche_description}. Tell me: (1) which categories are growing in search interest, (2) which are declining or saturated, (3) any emerging niches showing rising queries. Be specific — name the actual product types, not just broad categories like 'productivity'."
```

**Evaluate the response — does it contain ALL of the following?**
- Named product categories (not just broad labels)
- A direction for each: growing / stable / declining
- At least 2 rising or emerging niches

→ If yes: use the output, skip to Step 3
→ If no (vague or generic): proceed to Step 2

### 2. Fallback — WebSearch

Run three WebSearch queries in sequence:
1. `trending {niche_description} Etsy last 12 months`
2. `growing niches {niche_description}`
3. `best selling {niche_description} trends`

Synthesize results to extract trending categories and directions. Note `"source": "web_search"`.

If WebSearch also returns no useful data: return `{ "source": "unavailable", "raw_seed_candidates": [] }` and stop — the calling agent will continue without Google signals.

### 3. Classify each category

For each niche identified, assign:
- `direction`: `growing` / `stable` / `declining`
- `signal_strength`: `strong` / `moderate` / `weak`
- `notes`: one sentence on why (e.g. "freelance economy driving demand for invoice + income tracking tools")

Set top-level `confidence` based on the quality of data received:
- `high` — Gemini returned specific named categories with clear directions and examples
- `medium` — WebSearch fallback used, or Gemini output was partial
- `low` — results from either source were vague or lacked specific category names

---

## Output

Return a JSON object to the calling agent:

```json
{
  "source": "gemini",
  "confidence": "high",
  "trending_categories": [
    {
      "category": "personal finance trackers",
      "examples": ["budget tracker google sheets", "savings goal tracker", "expense log"],
      "direction": "growing",
      "signal_strength": "strong",
      "notes": "New Year resolutions + cost-of-living awareness driving sustained search growth"
    },
    {
      "category": "freelance business tools",
      "examples": ["invoice template google sheets", "client tracker", "income tracker freelancer"],
      "direction": "growing",
      "signal_strength": "strong",
      "notes": "Creator economy and gig work growth pushing demand for lightweight business admin tools"
    },
    {
      "category": "notion aesthetic templates",
      "examples": ["notion dashboard aesthetic", "notion student planner"],
      "direction": "stable",
      "signal_strength": "moderate",
      "notes": "Steady audience but market maturing — differentiation harder"
    },
    {
      "category": "AI prompt templates",
      "examples": ["chatgpt prompt template", "AI workflow notion"],
      "direction": "growing",
      "signal_strength": "moderate",
      "notes": "Emerging niche, rising fast but high uncertainty on longevity"
    },
    {
      "category": "printable planners PDF",
      "examples": ["daily planner printable", "weekly schedule PDF"],
      "direction": "declining",
      "signal_strength": "weak",
      "notes": "Shifting to digital-first formats; printables losing share to interactive spreadsheets"
    }
  ],
  "raw_seed_candidates": [
    "budget tracker google sheets",
    "freelance invoice template google sheets",
    "income tracker freelancer",
    "notion dashboard aesthetic",
    "AI prompt template google sheets"
  ]
}
```

### `source` values
| Value | Meaning |
|---|---|
| `gemini` | Gemini CLI with Search grounding — highest confidence |
| `web_search` | Synthesized from WebSearch — lower confidence |
| `unavailable` | Both methods failed |

---

## Notes

- This is a broad signal pass only — do not deep-dive any single keyword here. Stage 01 does that.
- If Gemini returns "I don't have real-time data" or generic output: go straight to fallback.
- `declining` categories should still be included in output — `seed-ranker` needs them to deprioritise those seeds.

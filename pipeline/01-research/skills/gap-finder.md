# gap-finder

Synthesize outputs from etsy-scan, google-trends, and pinterest-trends to identify underserved product opportunities. This skill does not browse the web — it reasons over collected data and produces a ranked shortlist of product ideas worth pursuing.

## Input
- `etsy_scan` — full JSON output from etsy-scan skill
- `google_trends` — full JSON output from google-trends skill
- `pinterest_trends` — full JSON output from pinterest-trends skill (may be unavailable)

---

## Steps

### 1. Score each signal

For each data point collected, assign a signal strength:

**Demand signals (from etsy-scan):**
- High total results (> 1000) with multiple bestsellers = proven demand ✅
- Strong autocomplete suggestions (3+ specific variants) = buyers actively searching ✅
- High favorites count on top listings = emotional resonance ✅
- High review counts = repeat purchase category ✅

**Trend signals (from google-trends):**
- `trend_direction: growing` = tailwind ✅
- `emerging` seasonality with rising queries = early mover opportunity ✅
- Clear `best_launch_window` = actionable timing ✅

**Competition signals (from etsy-scan):**
- `competition_level: low` + any demand = gap ✅
- `competition_level: medium` + strong trend = opportunity ✅
- `competition_level: high` + `bestseller_ratio > 0.5` = saturated, needs strong differentiation ⚠️
- `demand_recency_summary: hot` + `competition_level: medium` = active market worth entering ✅
- `demand_recency_summary: declining` = cross-reference `google_trends.trend_direction` — if also declining, that's a strong signal to deprioritise this niche ⚠️

**Pinterest signal (if `pinterest_trends.available: true`):**
- `pinterest_trends.trend_direction: growing` + medium Etsy competition = early opportunity ✅
- `pinterest_trends.related_interests` containing topics not seen in Etsy autocomplete = whitespace idea ✅

### 2. Identify gaps

A gap exists when any of the following is true:
- **Demand–quality gap** — high search volume but top listings look low-quality, generic, or outdated
- **Demand–supply gap** — strong trend signal but low Etsy competition
- **Niche gap** — a specific sub-audience is searching (e.g. "freelancer budget tracker") but no dedicated product exists
- **Format gap** — buyers searching for a format that's underrepresented (e.g. dark mode, mobile-friendly, AI-enhanced)

Look specifically at `rising_queries` and `autocomplete_suggestions` — these often reveal the exact gap (e.g. "budget tracker google sheets with savings goal" = buyers want savings goal feature, most templates don't have it).

### 3. Generate product ideas

For each gap identified, write one product idea. Each idea must:
- Have a clear target buyer (who exactly is this for?)
- Have a specific differentiator (what makes it better than what's already there?)
- Be buildable as a Google Sheets, Notion, or similar digital template
- Be grounded in at least one signal from the collected data

Aim for 3–5 ideas. Rank them by opportunity score (see below).

### 4. Score each idea

Rate each idea across three dimensions (1–3 scale):

| Dimension | 1 | 2 | 3 |
|---|---|---|---|
| **Demand** | Weak signals | Moderate signals | Strong signals |
| **Competition** | High, saturated | Medium, beatable | Low, open |
| **Buildability** | Complex, months of work | Moderate effort | Simple, days to build |

`opportunity_score` = Demand + Competition + Buildability (max 9)

Ideas scoring 7–9 = strong candidates for validation
Ideas scoring 5–6 = worth watching
Ideas scoring < 5 = deprioritise

---

## Output

Return a JSON object to the calling agent (`research-agent`):

```json
{
  "seed_keyword": "budget tracker google sheets",
  "gaps_identified": [
    "No dedicated tracker for freelancers with irregular income",
    "Most templates lack a savings goal progress tracker",
    "No dark mode / aesthetic variant in top results"
  ],
  "product_ideas": [
    {
      "rank": 1,
      "name": "Freelancer Budget Tracker — Google Sheets",
      "target_buyer": "Freelancers and self-employed with variable monthly income",
      "differentiator": "Built around irregular income — tracks per-project earnings, quarterly tax set-aside, and variable expense months. No existing Etsy product does this specifically.",
      "format": "Google Sheets",
      "signal_basis": "Rising query found: 'budget tracker for freelancers google sheets'. Low Etsy competition (< 200 results). Strong Jan + Sep peaks.",
      "scores": {
        "demand": 3,
        "competition": 3,
        "buildability": 2
      },
      "opportunity_score": 8,
      "verdict": "strong candidate"
    },
    {
      "rank": 2,
      "name": "Aesthetic Budget Tracker with Savings Goals — Google Sheets",
      "target_buyer": "Young adults (20s–30s) who want a visually appealing personal finance tool",
      "differentiator": "Dark mode design with pastel accents, savings goal progress bars, and a 'no-shame' spending tracker tone. Aesthetic angle is rising fast on Pinterest.",
      "format": "Google Sheets",
      "signal_basis": "Pinterest trend: growing. Rising query: 'aesthetic budget tracker google sheets'. Medium Etsy competition but top listings are outdated visually.",
      "scores": {
        "demand": 3,
        "competition": 2,
        "buildability": 2
      },
      "opportunity_score": 7,
      "verdict": "strong candidate"
    },
    {
      "rank": 3,
      "name": "Bi-Weekly Paycheck Budget Planner — Google Sheets",
      "target_buyer": "Employees paid every two weeks who struggle with standard monthly budget templates",
      "differentiator": "Aligns all expenses and bill payments to 26 bi-weekly pay periods instead of 12 months.",
      "format": "Google Sheets",
      "signal_basis": "Rising query: 'bi-weekly budget tracker google sheets'. Moderate Etsy competition but no dominant bestseller in this sub-niche.",
      "scores": {
        "demand": 2,
        "competition": 2,
        "buildability": 3
      },
      "opportunity_score": 7,
      "verdict": "strong candidate"
    }
  ],
  "recommended_next": "Freelancer Budget Tracker — strongest signal, lowest competition, clear differentiator"
}
```

---

## Notes

- This skill reasons only — it does not browse or call external tools.
- `seed_keyword` in output is taken from `etsy_scan.keyword` — not a separate input.
- If `pinterest_trends` is unavailable, skip Pinterest-based signals and note it in `signal_basis`.
- `differentiator` must be specific and grounded in data — never generic ("better design", "easier to use"). Always tie it to a gap observed in the collected data.
- The output of this skill feeds directly into `02-validate` — the `recommended_next` field is what the human reviews to decide what to validate first.

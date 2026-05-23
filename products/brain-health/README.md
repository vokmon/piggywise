# Brain Health Activity Packs

> "Relive your favourite decade — and keep your mind sharp doing it"

Structured brain training packs for seniors — nostalgia-themed, cognitively organized, and designed to be used as a 4-week guided program.

---

## Positioning

**Core message:** Brain training through the memories they love

**Three buyer types — one positioning:**

| Buyer | Motivation | How the product speaks to them |
|---|---|---|
| Senior | Enjoyment + feel sharp | "Relive the era I love" |
| Adult child | Meaningful gift | "I know exactly which decade to buy" |
| Caregiver | Structured, ready-to-use | "Organised program, no prep needed" |

The decade theme doubles as a gift signal — adult children don't need to guess which pack to buy. "Mom grew up in the 70s → buy the 1970s pack." Clear, easy, high Etsy conversion.

**Etsy title direction:**
`1970s Brain Training Activity Pack, Memory Games for Seniors, Printable Nostalgia Puzzle Book, Caregiver Gift`

**Avoid:** Positioning as "clinical" or "therapy" — seniors respond better to enjoyment-first messaging. Never lead with age ("for seniors") in the title — lead with the decade instead.

---

## The Gap We're Filling

Most senior activity products on Etsy are random collections — 1,000 word searches, generic trivia, or disconnected puzzles. They have no structure, no purpose per activity, and no guidance on how to use them.

Our difference:
- Activities are organized by **cognitive function**, not just activity type
- Each pack includes a **4-week guided schedule** — like a fitness program for the brain
- All activities are themed around a **specific era** the buyer actually lived through
- Everything is **senior-friendly** — large print, high contrast, clear instructions

---

## Product Structure

### One Pack = 90 Activities + 4-Week Schedule

**3 Cognitive Sets × 3 Activity Types × 10 Variations**

```
SET 1: MEMORY ENHANCEMENT
  1.1 Word Recall Games       (10 × 20 questions)
  1.2 Memory Trivia           (10 × 15 questions)
  1.3 Fill-in-the-Blank       (10 × 25 blanks)

SET 2: FOCUS & CONCENTRATION
  2.1 Word Search Puzzles     (10 × 30 words)
  2.2 Crossword Puzzles       (10 × 25-30 clues)
  2.3 Pattern Recognition     (10 × 5-7 patterns)

SET 3: LOGIC & PROBLEM SOLVING
  3.1 Logic Puzzles           (10 scenarios)
  3.2 Sequence Challenges     (10 × 5-7 sequences)
  3.3 Riddle & Deduction      (10 riddles)
```

### 4-Week Guided Schedule (included in every pack)

```
Week 1 — Memory Focus
  Mon/Wed/Fri → Set 1 activity
  Tue/Thu     → Set 2 activity (warm-up)

Week 2 — Memory Focus (continued)
  Mon/Wed/Fri → Set 1 activity
  Tue/Thu     → Set 3 activity (light logic)

Week 3 — Focus & Logic
  Mon/Wed/Fri → Set 2 activity
  Tue/Thu     → Set 3 activity

Week 4 — Full Mix
  Mon → Set 1 | Tue → Set 2 | Wed → Set 3
  Thu → Set 1 | Fri → Set 2 | Sat → Set 3
```

Rest days are built in. Total solving time per session: 15–30 minutes.

---

## Theme System

Every pack is themed around a specific era — the nostalgia is the hook, the cognitive structure is the value.

| Pack | Theme | Target Buyer |
|---|---|---|
| Pack 1 | 1970s Memory Lane | Born ~1945–1960 |
| Pack 2 | 1960s Memory Lane | Born ~1935–1950 |
| Pack 3 | 1950s Memory Lane | Born ~1925–1940 |
| Bundle | All 3 Decades | Gift buyers, caregivers |

Each new theme uses the **same structure and workflow** — only the content changes. Once Pack 1 is built, subsequent packs take significantly less time.

### 10 Topics Per Theme (1970s example)
1. Music Legends
2. Television Shows
3. Movies & Entertainment
4. Fashion & Style
5. Events & History
6. Food & Dining
7. Technology & Innovation
8. Celebrity Culture
9. Slang & Language
10. Sports & Recreation

---

## Print Specifications (Senior-Friendly)

**Paper size: A4 (210mm × 297mm) — all activities**

Content flows across as many pages as needed. Never squeeze to fit. A 20-question activity may span 3–4 pages — that's fine. Think magazine layout: generous white space, clear sections, easy to navigate.

| Element | Specification |
|---|---|
| Paper size | A4 (210mm × 297mm) |
| Body font | 14pt |
| Headers | 18pt |
| Line spacing | 1.5x |
| Margins | 20mm all sides |
| Questions per page | 4–6 MCQ / 8–10 short answers |
| Word search cell | 12mm per cell |
| Crossword cell | 11mm per cell |
| Answer lines | 8mm tall |
| Color | Black text on white only — no grey backgrounds |
| Instructions | One clear sentence per activity, top of page |

---

## Pricing Strategy

| Product | Price |
|---|---|
| Single themed pack | $14.99 |
| Bundle (3 decades) | $34.99 |

Positioned as a **structured brain training program**, not a generic activity book — justifying the price over competitors selling random puzzle collections at $5–8.

---

## Folder Structure

```
brain-health/
  README.md
  docs/
    prompt_library.md              ← AI prompt templates + production workflow
  data/
    product_posts/                 ← Etsy listing data per theme (English only)
  themes/
    1970s/                         ← generated content per theme
      activities/                  ← raw AI-generated activity files
      output/                      ← final PDFs
    1960s/
    1950s/
  images/
    covers/                        ← Etsy cover images per theme
    previews/                      ← preview images for listings
  skills/                          ← brain-health specific skills
    activity-1-1-word-recall.md
    activity-1-2-memory-trivia.md
    activity-1-3-fill-blank.md
    activity-2-1-word-search.md
    activity-2-2-crossword.md
    activity-2-3-pattern-recognition.md
    activity-3-1-logic-puzzles.md
    activity-3-2-sequence-challenges.md
    activity-3-3-riddle-deduction.md
    assemble-pdf.md
  agents/                          ← brain-health specific agents
    research-agent.md
    content-agent.md
    qa-agent.md
    assembly-agent.md
    marketing-agent.md
    master-agent.md
```

---

## Production Workflow (Per Theme)

1. **Research** — identify 10 topics for the theme
2. **Generate** — run AI prompts for all 9 activity types
3. **Process** — create word search and crossword grids
4. **Design** — layout PDF with senior-friendly formatting + 4-week schedule page
5. **QA** — check accuracy, no duplicates, correct difficulty mix
6. **Package** — export final PDF
7. **List** — create Etsy listing using product post data

See `docs/prompt_library.md` for full AI prompt templates and step-by-step workflow.

---

## Scaling Roadmap

```
Month 1 → Launch 1970s pack, test market
Month 2 → Launch 1960s pack if 1970s gains traction
Month 3 → Launch 1950s pack + bundle all 3
Month 4+ → Explore non-decade themes
            (e.g., "Music Legends", "Hollywood Classics", "Sports Greats")
```

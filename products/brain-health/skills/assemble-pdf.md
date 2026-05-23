# assemble-pdf

Compile all generated activities into a complete A4 PDF ready for delivery.
Includes activity pages, answer key section, running headers, and page references.

## Input
- Theme name (e.g., "1970s")
- Pack name (e.g., "1970s Memory Lane Brain Health Pack")
- All 9 activity files in `workspace/[THEME]/activities/`
- QA approval from qa-agent

## Output
- Final PDF: `workspace/[THEME]/output/[THEME]_Memory_Lane_Brain_Health_Pack.pdf`

---

## Page Structure (Every Page)

**Running header (top of every page):**
```
[Pack Name]  |  [Set Name]
```
Example: `1970s Memory Lane Brain Health Pack  |  Set 1: Memory Enhancement`

**Footer (bottom of every page):**
```
Answers → p.[X]                                    Page [N]
```
- Left: reference to answer key page for this activity
- Right: current page number
- Answer key pages: footer shows only `Page [N]` (no answer reference needed)

---

## PDF Structure

```
Page 1      Cover page — Pack name + era imagery description
Page 2      How to use this pack
Page 3      My Progress page (see below)
Page 4      4-week guided schedule (see below)
Page 5      Table of contents (activities)
Pages 5+    ── ACTIVITY SECTION ──
              [Set opener page] Set 1: Memory Enhancement
                Warm intro blurb (2–3 lines) — what this set trains, encouraging tone
                e.g. "This set is all about memory. Don't worry about getting everything
                right — just enjoy the trip down memory lane."
                Activity 1.1 · Word Recall · Games 1–10
                Activity 1.2 · Memory Trivia · Games 1–10
                Activity 1.3 · Fill-in-the-Blank · Games 1–10
              [End-of-set line] "You've finished Set 1 — time for a well-earned cuppa. ☕"
              [Set opener page] Set 2: Focus & Concentration
                Warm intro blurb — what this set trains
                Activity 2.1 · Word Search · Puzzles 1–10
                Activity 2.2 · Crossword · Puzzles 1–10
                Activity 2.3 · Pattern Recognition · Grids 1–10
              [End-of-set line] "Set 2 done — your focus is sharp! Take a breather before Set 3."
              [Set opener page] Set 3: Logic & Problem Solving
                Warm intro blurb — what this set trains
                Activity 3.1 · Logic Puzzles · 1–10
                Activity 3.2 · Sequence Challenges · 1–10
                Activity 3.3 · Riddle & Deduction · 1–10
              [End-of-pack page] "You've completed the full pack! Every puzzle, every challenge — well done. 🎉"
              [Completion certificate page] (see below)
[Sep. page] ── HOW DID YOU GO? ──
              [Pack Name] — How Did You Go?
[TOC page]  Answer Key Table of Contents
              Set 1: Memory Enhancement
                1.1 Word Recall Games 1–10 ............. p.XX
                1.2 Memory Trivia Games 1–10 ........... p.XX
                1.3 Fill-in-the-Blank Games 1–10 ....... p.XX
              Set 2: Focus & Concentration
                2.1 Word Search Puzzles 1–10 ........... p.XX
                2.2 Crossword Puzzles 1–10 ............. p.XX
                2.3 Pattern Recognition 1–10 ........... p.XX
              Set 3: Logic & Problem Solving
                3.1 Logic Puzzles 1–10 ................. p.XX
                3.2 Sequence Challenges 1–10 ........... p.XX
                3.3 Riddle & Deduction 1–10 ............ p.XX
[Ans. pages] Answer pages — one activity per page or split as needed
              Header on every answer page:
              "[Pack Name] — How Did You Go?"
              "─── p.[activity page] · [Set] · [Activity] · [Game N] ───"
              Each answer followed by a brief context line where helpful
              (see activity-tone.md — Answer Key Tone)
```

---

## Special Pages

### My Progress Page (Page 3)
The first thing the reader fills in — makes the pack feel personal from the start.

```
┌─────────────────────────────────────────────────────┐
│                   My Progress                        │
│                                                      │
│  Name: _______________________________               │
│  Date started: ________________________              │
│                                                      │
│  ── Week 1 ──────────────────────────────────        │
│  Day 1 □  Day 2 □  Day 3 □  Day 4 □  Day 5 □        │
│  Day 6 □  Day 7 □                                    │
│  My stars this week: ★★★★★ (circle yours)           │
│                                                      │
│  ── Week 2 ──────────────────────────────────        │
│  Day 8 □  Day 9 □  Day 10 □  Day 11 □  Day 12 □     │
│  Day 13 □  Day 14 □                                  │
│  My stars this week: ★★★★★                          │
│                                                      │
│  ── Week 3 ──────────────────────────────────        │
│  Day 15 □  Day 16 □  Day 17 □  Day 18 □  Day 19 □   │
│  Day 20 □  Day 21 □                                  │
│  My stars this week: ★★★★★                          │
│                                                      │
│  ── Week 4 ──────────────────────────────────        │
│  Day 22 □  Day 23 □  Day 24 □  Day 25 □  Day 26 □   │
│  Day 27 □  Day 28 □                                  │
│  My stars this week: ★★★★★                          │
│                                                      │
│  Total stars: ___ / 28    Date completed: _______    │
└─────────────────────────────────────────────────────┘
```

- Tick each day's box after completing that day's activity
- Circle stars at the end of each week — relaxed self-rating, no pass/fail
- Name and Date fields make it personal — important for shared/gifted packs

---

### 4-Week Guided Schedule (Page 4)
Each day lists the exact activity so there is zero decision fatigue:

```
Week 1 — Getting Started
  Day 1   Set 1 · Word Recall · Remember When: [Topic 1]           p.X
  Day 2   Set 1 · Memory Trivia · Do You Remember...? [Topic 2]    p.X
  Day 3   Set 1 · Fill in the Line: [Topic 3]                      p.X
  Day 4   Set 2 · The [Topic 4] Word Hunt                          p.X
  Day 5   Set 2 · The [Topic 5] Crossword                          p.X
  Day 6   Set 2 · Spot the Pattern: [Topic 6]                      p.X
  Day 7   ☕ Rest day — or revisit a favourite from the week
...
```

- Every day shows: Set, activity name (warm name format), and page number
- Day 7 of each week is a rest day — low pressure, optional revisit
- Tone: "Getting Started", "Finding Your Groove", "In the Zone", "You're a Champion!"

---

### Completion Certificate (After End-of-Pack Page)
A simple, warm full-page certificate printed at the back of the activity section:

```
        ╔══════════════════════════════════════════╗
        ║                                          ║
        ║         Well Done!                       ║
        ║                                          ║
        ║  This certifies that                     ║
        ║                                          ║
        ║  ____________________________________    ║
        ║                                          ║
        ║  completed the                           ║
        ║  [Pack Name]                             ║
        ║                                          ║
        ║  Date: _______________________________   ║
        ║                                          ║
        ║  "Every puzzle completed is a win."      ║
        ║                                          ║
        ╚══════════════════════════════════════════╝
```

- Styled with era color border (full opacity)
- Era-appropriate small icon in one corner (e.g., record player for 1970s)
- Warm, not childish — dignified celebration
- Many families frame this or stick it on the fridge

---

## Assembly Process (Two-Pass)

### Pass 1 — Assemble Activity Pages
1. Confirm QA report shows APPROVED — do not proceed if NEEDS FIXES
2. Build all activity pages in order with running headers
3. Leave footer answer references blank for now (page numbers not yet known)
4. Note each activity's starting page number in a reference map:
   ```
   Activity 1.1 Game 1 → p.5
   Activity 1.1 Game 2 → p.7
   ...
   ```

### Pass 2 — Build Answer Key + Fill References
1. Build answer key section using the reference map
2. Build answer key TOC with correct page numbers
3. Go back and fill in `Answers → p.[X]` in each activity page footer
4. Assign final page numbers throughout

---

## Print Specs (Applied Throughout)
- Paper: A4 (210mm × 297mm)
- Body font: **14pt Arial or Helvetica** (sans-serif only — serif fonts are harder for aging eyes)
- Headers: 18pt Arial or Helvetica Bold
- Running header: 10pt, top of page
- Footer text: 10pt, bottom of page
- Line spacing: 1.5x
- Margins: 20mm all sides
- 4–6 MCQ questions per page, 8–10 short questions per page
- Word search cell: 12mm
- Crossword cell: 11mm
- **B&W compatible** — era colors are decorative only; no information is conveyed by color alone (a senior printing on a B&W printer must still be able to use every page)

For visual styling (colors, borders, icons, header bands) → see `skills/design-theme.md`

---

## Export
Export as PDF (print quality, 300 DPI) to `workspace/[THEME]/output/`
Filename: `[THEME]_Memory_Lane_Brain_Health_Pack.pdf`

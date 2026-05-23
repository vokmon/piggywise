# assemble-pdf

Compile all generated activities into a complete A4 PDF ready for delivery.
Includes activity pages, running headers, and upside-down answer blocks on each game page.

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
Page [N]
```
- Right-aligned page number only

---

## PDF Structure

```
Page 1      Cover page — Pack name + era imagery description
Page 2      How to use this pack
Page 3      My Progress page (see below)
Page 4      4-week guided schedule (see below)
Page 5      Table of contents (activities)
Pages 6+    ── ACTIVITY SECTION ──
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
                Activity 2.3 · Sudoku · Puzzles 1–10
              [End-of-set line] "Set 2 done — your focus is sharp! Take a breather before Set 3."
              [Set opener page] Set 3: Logic & Problem Solving
                Warm intro blurb — what this set trains
                Activity 3.1 · Logic Puzzles · 1–10
                Activity 3.2 · The Number Puzzle (Crossnumber) · 1–10
                Activity 3.3 · Riddle & Deduction · 1–10
              [End-of-pack page] "You've completed the full pack! Every puzzle, every challenge — well done. 🎉"
              [Completion certificate page] (see below)
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
  Day 3   Set 1 · Finish the Line: [Topic 3]                       p.X
  Day 4   Set 2 · The [Topic 4] Word Hunt                          p.X
  Day 5   Set 2 · The [Topic 5] Crossword                          p.X
  Day 6   Set 2 · The [Era] Sudoku — Puzzle 1                       p.X
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

## Upside-Down Answer Block

Every activity's last page ends with a small upside-down answer block — rotated 180° — printed in a smaller font (9pt) in light grey:

```
Solution ↕          [for puzzle activities: crossword, word search, sudoku, crossnumber, logic, riddle]
Suggested Answers ↕ [for memory activities: word recall, trivia, fill-blank]
```

- Puzzle grids (sudoku, crossword, crossnumber, word search): print the completed grid reduced to ~30% size, rotated 180°
- Text answers (logic puzzles, riddles, word recall, trivia, fill-blank): list answers in compact 2-column format, rotated 180°
- Label in 8pt grey text only — no border, no header box
- Positioned in the bottom 15mm of the page — well below the score box

## Assembly Process

1. Confirm QA report shows APPROVED — do not proceed if NEEDS FIXES
2. Build all activity pages in order with running headers
3. Add upside-down answer block to the bottom of each game's last page
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
- Memory activities (1.1, 1.2): 5 questions per page — 1 round per page, generous write space
- Fill-blank (1.3): ~12 sentences per page — rounds 1–3 on page 1, rounds 4–5 on page 2
- Logic puzzles (3.1): 1 puzzle per page — scenario, clues, and questions together
- All other question-based activities: 8–10 items per page
- Word search cell: 12mm
- Crossword cell: 11mm
- **B&W compatible** — era colors are decorative only; no information is conveyed by color alone (a senior printing on a B&W printer must still be able to use every page)

For visual styling (colors, borders, icons, header bands) → see `skills/design-theme.md`

---

## Export
Export as PDF (print quality, 300 DPI) to `workspace/[THEME]/output/`
Filename: `[THEME]_Memory_Lane_Brain_Health_Pack.pdf`

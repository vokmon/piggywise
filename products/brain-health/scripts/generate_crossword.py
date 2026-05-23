#!/usr/bin/env python3
"""
Crossword grid generator for Brain Health Activity Pack.

Reads clue/answer pairs from a markdown file and generates 13x13 grids.
Uses a greedy intersection-first placement algorithm.

Input format (markdown):
    ## Game 1: 1970s TV Shows
    CORONATION: Long-running soap opera set in Weatherfield
    FAWLTY: Hotel comedy with a short-tempered owner
    MINDER: Crime drama about a car dealer and his minder
    ...

    ## Game 2: 1970s Music
    ABBA: Swedish pop group who won Eurovision in 1974
    ...

    Lines without a colon are treated as answer-only (no clue text).

Usage:
    python scripts/generate_crossword.py \\
      --input workspace/1970s/activities/2-2-crossword-clues.md \\
      --output workspace/1970s/activities/2-2-crossword-grids/ \\
      --cell-size 11
"""

import argparse
import json
import re
import sys
from pathlib import Path

BLOCKED = "#"


# ---------------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[BLOCKED] * size for _ in range(size)]
        self.placements = []   # list of placement dicts

    # ------------------------------------------------------------------
    def _step(self, direction):
        return (0, 1) if direction == "across" else (1, 0)

    def _perp(self, direction):
        return "down" if direction == "across" else "across"

    # ------------------------------------------------------------------
    def can_place(self, word, row, col, direction):
        dr, dc = self._step(direction)
        pr, pc = self._step(self._perp(direction))
        size = self.size

        # Bounds check
        end_r = row + dr * (len(word) - 1)
        end_c = col + dc * (len(word) - 1)
        if not (0 <= row < size and 0 <= col < size):
            return False
        if not (0 <= end_r < size and 0 <= end_c < size):
            return False

        # Cell immediately before the start must be blocked/edge
        br, bc = row - dr, col - dc
        if 0 <= br < size and 0 <= bc < size and self.cells[br][bc] != BLOCKED:
            return False

        # Cell immediately after the end must be blocked/edge
        ar = row + dr * len(word)
        ac = col + dc * len(word)
        if 0 <= ar < size and 0 <= ac < size and self.cells[ar][ac] != BLOCKED:
            return False

        intersections = 0
        for i, letter in enumerate(word):
            r, c = row + i * dr, col + i * dc
            cell = self.cells[r][c]

            if cell == BLOCKED:
                # New cell — check perpendicular neighbours don't form unintended words
                above_r, above_c = r - pr, c - pc
                below_r, below_c = r + pr, c + pc
                if 0 <= above_r < size and 0 <= above_c < size:
                    if self.cells[above_r][above_c] != BLOCKED:
                        return False
                if 0 <= below_r < size and 0 <= below_c < size:
                    if self.cells[below_r][below_c] != BLOCKED:
                        return False
            elif cell == letter:
                intersections += 1
            else:
                return False  # letter conflict

        if not self.placements:
            return True   # first word — no intersection required
        return intersections > 0

    # ------------------------------------------------------------------
    def place(self, word, row, col, direction):
        dr, dc = self._step(direction)
        for i, letter in enumerate(word):
            self.cells[row + i * dr][col + i * dc] = letter
        self.placements.append({
            "word": word,
            "row": row,
            "col": col,
            "direction": direction,
            "number": None,   # filled later by number_cells()
        })

    # ------------------------------------------------------------------
    def find_positions(self, word):
        """Return all valid (row, col, direction, score) for word."""
        results = []
        dr_map = {"across": (0, 1), "down": (1, 0)}

        for placement in self.placements:
            existing = placement["word"]
            existing_dir = placement["direction"]
            perp_dir = self._perp(existing_dir)
            edr, edc = dr_map[existing_dir]
            pdr, pdc = dr_map[perp_dir]

            for ei, el in enumerate(existing):
                for wi, wl in enumerate(word):
                    if el != wl:
                        continue
                    # The intersection cell is at:
                    int_r = placement["row"] + ei * edr
                    int_c = placement["col"] + ei * edc
                    # word[wi] should land at (int_r, int_c)
                    start_r = int_r - wi * pdr
                    start_c = int_c - wi * pdc
                    if self.can_place(word, start_r, start_c, perp_dir):
                        # Score = number of extra intersections this placement gains
                        score = self._count_crossings(word, start_r, start_c, perp_dir)
                        results.append((start_r, start_c, perp_dir, score))

        return results

    def _count_crossings(self, word, row, col, direction):
        dr, dc = self._step(direction)
        count = 0
        for i, letter in enumerate(word):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < self.size and 0 <= c < self.size:
                if self.cells[r][c] == letter:
                    count += 1
        return count

    # ------------------------------------------------------------------
    def number_cells(self):
        """Assign across/down clue numbers to start cells."""
        number = 1
        numbers = {}
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[r][c] == BLOCKED:
                    continue
                needs_num = False
                # Across start: left is blocked/edge, right exists
                if (c == 0 or self.cells[r][c - 1] == BLOCKED) and \
                   (c + 1 < self.size and self.cells[r][c + 1] != BLOCKED):
                    needs_num = True
                # Down start: above is blocked/edge, below exists
                if (r == 0 or self.cells[r - 1][c] == BLOCKED) and \
                   (r + 1 < self.size and self.cells[r + 1][c] != BLOCKED):
                    needs_num = True
                if needs_num:
                    numbers[(r, c)] = number
                    number += 1

        for p in self.placements:
            p["number"] = numbers.get((p["row"], p["col"]))

        return numbers

    # ------------------------------------------------------------------
    def to_display(self, numbers):
        rows = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                cell = self.cells[r][c]
                row.append({
                    "blocked": cell == BLOCKED,
                    "letter":  "" if cell == BLOCKED else cell,
                    "number":  numbers.get((r, c)),
                })
            rows.append(row)
        return rows

    def to_text(self, numbers):
        lines = []
        for r in range(self.size):
            row_str = []
            for c in range(self.size):
                cell = self.cells[r][c]
                if cell == BLOCKED:
                    row_str.append("■■")
                else:
                    n = numbers.get((r, c))
                    row_str.append(str(n).ljust(2) if n else "_ ")
            lines.append(" ".join(row_str))
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate_crossword(entries, size):
    """
    entries: list of {"answer": str, "clue": str}
    Returns (Grid, failed_answers).

    Strategy:
    - Pick a moderate-length word (~55% of grid) as the anchor (first placement).
      A very long first word fills the grid and blocks everything else.
    - Greedy pass: place remaining words by intersection score.
    - Second pass: retry words that failed the first pass.
    - If overall placement rate < 60%, retry with a different anchor word.
    """
    entries = [
        {"answer": e["answer"].upper(), "clue": e.get("clue", "")}
        for e in entries
    ]
    valid   = [e for e in entries if 2 <= len(e["answer"]) <= size]
    invalid = [e["answer"] for e in entries if not (2 <= len(e["answer"]) <= size)]

    if not valid:
        return Grid(size), invalid

    # Try up to 3 anchor words (by closeness to ideal length) and keep best result
    target_len = size * 0.55
    candidates_sorted = sorted(valid, key=lambda e: abs(len(e["answer"]) - target_len))
    best_grid, best_failed = None, list(valid)   # worst case: nothing placed

    for anchor in candidates_sorted[:3]:
        grid, failed = _try_build(valid, anchor, size)
        if len(failed) < len(best_failed):
            best_grid, best_failed = grid, failed
        if len(failed) == 0:
            break  # perfect — stop trying

    return best_grid, invalid + best_failed


def _try_build(entries, anchor, size):
    """Attempt to build a crossword using anchor as the first word."""
    grid = Grid(size)
    remaining = [e for e in entries if e is not anchor]
    remaining.sort(key=lambda e: len(e["answer"]), reverse=True)

    # Place anchor centred horizontally
    word = anchor["answer"]
    row  = size // 2
    col  = max(0, (size - len(word)) // 2)
    if not grid.can_place(word, row, col, "across"):
        return grid, [e["answer"] for e in entries]
    grid.place(word, row, col, "across")

    unplaced = _greedy_pass(grid, remaining)
    # Second pass on leftovers
    still_unplaced = _greedy_pass(grid, unplaced)
    return grid, [e["answer"] for e in still_unplaced]


def _greedy_pass(grid, entries):
    """Try to place each entry; return list of entries that could not be placed."""
    unplaced = []
    for entry in entries:
        word = entry["answer"]
        positions = grid.find_positions(word)
        if not positions:
            unplaced.append(entry)
            continue
        positions.sort(key=lambda x: x[3], reverse=True)
        row, col, direction, _ = positions[0]
        grid.place(word, row, col, direction)
    return unplaced


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

def parse_clue_file(path):
    """
    Parse markdown into ordered list of (game_name, [{"answer", "clue"}]).
    Accepts lines like:
        ANSWER: clue text
        ANSWER   (no clue)
    """
    text = Path(path).read_text(encoding="utf-8")
    games = []
    current_name = None
    current_entries = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if current_name is not None:
                games.append((current_name, current_entries))
            current_name = line[3:].strip()
            current_entries = []
        elif current_name is not None and line and not line.startswith("#"):
            if ":" in line:
                parts = line.split(":", 1)
                answer = re.sub(r"[^A-Za-z]", "", parts[0]).upper()
                clue = parts[1].strip()
            else:
                answer = re.sub(r"[^A-Za-z]", "", line).upper()
                clue = ""
            if 2 <= len(answer) <= 15:
                current_entries.append({"answer": answer, "clue": clue})

    if current_name is not None:
        games.append((current_name, current_entries))

    return games


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate crossword grids.")
    parser.add_argument("--input",     required=True, help="Markdown file with clues")
    parser.add_argument("--output",    required=True, help="Output directory")
    parser.add_argument("--cell-size", type=int, default=11,  help="Cell size in mm (metadata only)")
    parser.add_argument("--grid-size", type=int, default=13,  help="Grid dimension NxN (max 13)")
    parser.add_argument("--max-words", type=int, default=30,  help="Max words per crossword")
    parser.add_argument("--seed",      type=int, default=None, help="Random seed (unused — placement is deterministic)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    games = parse_clue_file(args.input)
    if not games:
        print(f"ERROR: No games found in {args.input}", file=sys.stderr)
        return 1

    print(f"Found {len(games)} game(s) in {args.input}")
    errors = 0

    for i, (name, entries) in enumerate(games, start=1):
        entries = entries[: args.max_words]
        grid, failed = generate_crossword(entries, args.grid_size)
        numbers = grid.number_cells()

        # Attach clue text to placements
        clue_map = {e["answer"].upper(): e["clue"] for e in entries}
        for p in grid.placements:
            p["clue"] = clue_map.get(p["word"], "")

        across = sorted(
            [p for p in grid.placements if p["direction"] == "across"],
            key=lambda p: p["number"] or 999,
        )
        down = sorted(
            [p for p in grid.placements if p["direction"] == "down"],
            key=lambda p: p["number"] or 999,
        )

        game_data = {
            "game_number":  i,
            "game_name":    name,
            "grid_size":    args.grid_size,
            "cell_size_mm": args.cell_size,
            "grid":         grid.to_display(numbers),
            "across":       across,
            "down":         down,
            "failed_words": failed,
        }

        slug = f"game_{i:02d}"
        (output_dir / f"{slug}.json").write_text(
            json.dumps(game_data, indent=2), encoding="utf-8"
        )

        # Human-readable text output
        txt_lines = [f"Game {i}: {name}", "", grid.to_text(numbers), "", "ACROSS"]
        for p in across:
            clue_str = f"  {p['clue']}" if p["clue"] else ""
            txt_lines.append(f"  {p['number']}. {p['word']}{clue_str}")
        txt_lines.append("\nDOWN")
        for p in down:
            clue_str = f"  {p['clue']}" if p["clue"] else ""
            txt_lines.append(f"  {p['number']}. {p['word']}{clue_str}")
        if failed:
            txt_lines.append(f"\nWARNING: Could not place: {', '.join(failed)}")

        (output_dir / f"{slug}_grid.txt").write_text(
            "\n".join(txt_lines), encoding="utf-8"
        )

        placed_count = len(grid.placements)
        total = len(entries)
        if failed:
            errors += 1
            status = f"WARNING — {len(failed)} word(s) not placed: {', '.join(failed)}"
        else:
            status = "OK"
        print(f"  Game {i:02d}: {name} — {placed_count}/{total} words placed  [{status}]")

    print(f"\nDone. Output → {output_dir}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Sudoku puzzle generator for Brain Health Activity Pack.
Generates valid 9x9 puzzles with unique solutions at varying difficulty.

Usage:
    python products/brain-health/scripts/generate_sudoku.py \\
      --output workspace/1970s/activities/2-3-sudoku-grids/ \\
      --count 10 \\
      --difficulty easy:3,medium:4,hard:3 \\
      --seed 42
"""

import argparse
import json
import random
import sys
from pathlib import Path

# Target number of GIVEN (pre-filled) cells per difficulty level.
# More givens = easier puzzle.
GIVENS = {
    "easy":   38,
    "medium": 30,
    "hard":   24,
}


# ---------------------------------------------------------------------------
# Core sudoku logic
# ---------------------------------------------------------------------------

def _valid(grid, row, col, num):
    if num in grid[row]:
        return False
    if any(grid[r][col] == num for r in range(9)):
        return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == num:
                return False
    return True


def _fill(grid, rng):
    """Fill an empty grid with a valid solution using random backtracking."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                nums = list(range(1, 10))
                rng.shuffle(nums)
                for num in nums:
                    if _valid(grid, row, col, num):
                        grid[row][col] = num
                        if _fill(grid, rng):
                            return True
                        grid[row][col] = 0
                return False
    return True


def _count_solutions(grid, limit=2):
    """Count solutions up to `limit` — used to verify uniqueness."""
    count = [0]

    def solve(g):
        if count[0] >= limit:
            return
        for row in range(9):
            for col in range(9):
                if g[row][col] == 0:
                    for num in range(1, 10):
                        if _valid(g, row, col, num):
                            g[row][col] = num
                            solve(g)
                            g[row][col] = 0
                    return
        count[0] += 1

    solve([r[:] for r in grid])
    return count[0]


def _make_puzzle(solution, target_givens, rng):
    """Remove cells from solution while preserving a unique solution."""
    puzzle = [r[:] for r in solution]
    cells = [(r, c) for r in range(9) for c in range(9)]
    rng.shuffle(cells)

    givens = 81
    for row, col in cells:
        if givens <= target_givens:
            break
        saved = puzzle[row][col]
        puzzle[row][col] = 0
        if _count_solutions(puzzle) == 1:
            givens -= 1
        else:
            puzzle[row][col] = saved   # restore — removal breaks uniqueness

    return puzzle


# ---------------------------------------------------------------------------
# Text rendering
# ---------------------------------------------------------------------------

_H_THICK = "╠═══════╬═══════╬═══════╣"
_H_THIN  = "├───────┼───────┼───────┤"
_TOP     = "╔═══════╦═══════╦═══════╗"
_BOT     = "╚═══════╩═══════╩═══════╝"


def _render_grid(grid, empty_char="·"):
    lines = [_TOP]
    for r in range(9):
        if r > 0:
            lines.append(_H_THICK if r % 3 == 0 else _H_THIN)
        row_parts = ["║"]
        for c in range(9):
            if c > 0 and c % 3 == 0:
                row_parts.append("║")
            val = grid[r][c]
            row_parts.append(f" {val if val else empty_char} ")
            if c % 3 == 2 and c < 8:
                pass  # separator already added at start of next group
        row_parts.append("║")
        lines.append("".join(row_parts))
    lines.append(_BOT)
    return "\n".join(lines)


def render_txt(game_number, difficulty, puzzle, solution):
    lines = [
        f"Puzzle {game_number:02d}  [{difficulty}]",
        "",
        _render_grid(puzzle),
        "",
        "─" * 40,
        "Solution (print upside-down at bottom of page):",
        "",
        _render_grid(solution, empty_char=" "),
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Difficulty argument parser
# ---------------------------------------------------------------------------

def parse_difficulty(arg):
    """'easy:3,medium:4,hard:3' → [('easy',3), ('medium',4), ('hard',3)]"""
    result = []
    for part in arg.split(","):
        diff, _, n = part.partition(":")
        result.append((diff.strip().lower(), int(n.strip())))
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate Sudoku puzzles.")
    parser.add_argument("--output",     required=True, help="Output directory")
    parser.add_argument("--count",      type=int, default=10, help="Number of puzzles")
    parser.add_argument("--difficulty", default="easy:3,medium:4,hard:3",
                        help="Difficulty mix e.g. easy:3,medium:4,hard:3")
    parser.add_argument("--seed",       type=int, default=None, help="Random seed")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build ordered difficulty list
    diff_mix = parse_difficulty(args.difficulty)
    order = []
    for diff, count in diff_mix:
        order.extend([diff] * count)
    while len(order) < args.count:
        order.append("medium")
    order = order[:args.count]

    print(f"Generating {args.count} Sudoku puzzle(s) → {output_dir}")
    errors = 0

    for i, difficulty in enumerate(order, start=1):
        target = GIVENS.get(difficulty, 30)

        # Generate filled solution
        solution = [[0] * 9 for _ in range(9)]
        _fill(solution, rng)

        # Carve out puzzle cells
        puzzle = _make_puzzle(solution, target, rng)
        actual_givens = sum(1 for r in range(9) for c in range(9) if puzzle[r][c])

        game_data = {
            "game_number": i,
            "difficulty":  difficulty,
            "givens":      actual_givens,
            "puzzle":      puzzle,
            "solution":    solution,
        }

        slug = f"game_{i:02d}_{difficulty}"
        (output_dir / f"{slug}.json").write_text(json.dumps(game_data, indent=2))
        (output_dir / f"{slug}.txt").write_text(
            render_txt(i, difficulty, puzzle, solution)
        )

        print(f"  Puzzle {i:02d}: {difficulty:<6}  {actual_givens} givens")

    print(f"\nDone. Output → {output_dir}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

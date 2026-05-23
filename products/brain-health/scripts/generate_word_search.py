#!/usr/bin/env python3
"""
Word search grid generator for Brain Health Activity Pack.

Reads word lists from a markdown file and generates 15x15 grids.
Words are hidden horizontally, vertically, and diagonally in all directions.

Input format (markdown):
    ## Game 1: 1970s Music
    ABBA
    DISCO
    PLATFORM
    ...

    ## Game 2: 1970s TV
    CORONATION
    ...

Usage:
    python scripts/generate_word_search.py \\
      --input workspace/1970s/activities/2-1-word-search-lists.md \\
      --output workspace/1970s/activities/2-1-word-search-grids/ \\
      --cell-size 12
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path

DIRECTIONS = [
    (0,  1,  "right"),
    (0, -1,  "left"),
    (1,  0,  "down"),
    (-1, 0,  "up"),
    (1,  1,  "down-right"),
    (1, -1,  "down-left"),
    (-1, 1,  "up-right"),
    (-1,-1,  "up-left"),
]
FILL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ---------------------------------------------------------------------------
# Grid helpers
# ---------------------------------------------------------------------------

def make_grid(size):
    return [["." for _ in range(size)] for _ in range(size)]


def can_place(grid, word, row, col, dr, dc):
    size = len(grid)
    for i, letter in enumerate(word):
        r, c = row + i * dr, col + i * dc
        if not (0 <= r < size and 0 <= c < size):
            return False
        cell = grid[r][c]
        if cell != "." and cell != letter:
            return False
    return True


def place_word(grid, word, row, col, dr, dc):
    for i, letter in enumerate(word):
        grid[row + i * dr][col + i * dc] = letter


def fill_empty(grid, rng):
    size = len(grid)
    for r in range(size):
        for c in range(size):
            if grid[r][c] == ".":
                grid[r][c] = rng.choice(FILL_LETTERS)


def generate_grid(words, size, rng):
    """Place words in grid; return (grid, placed_words, failed_words)."""
    grid = make_grid(size)
    placed = []
    failed = []

    # Sort longest first — longer words are harder to place
    sorted_words = sorted(words, key=len, reverse=True)

    for word in sorted_words:
        word = word.upper()
        if not (1 <= len(word) <= size):
            failed.append(word)
            continue

        # Build randomised list of all (row, col, direction) candidates
        positions = [(r, c) for r in range(size) for c in range(size)]
        rng.shuffle(positions)
        dirs = list(DIRECTIONS)
        rng.shuffle(dirs)

        placed_word = False
        for row, col in positions:
            for dr, dc, name in dirs:
                if can_place(grid, word, row, col, dr, dc):
                    place_word(grid, word, row, col, dr, dc)
                    placed.append({
                        "word": word,
                        "row": row,
                        "col": col,
                        "direction": name,
                        "dr": dr,
                        "dc": dc,
                    })
                    placed_word = True
                    break
            if placed_word:
                break

        if not placed_word:
            failed.append(word)

    fill_empty(grid, rng)
    return grid, placed, failed


# ---------------------------------------------------------------------------
# Text rendering
# ---------------------------------------------------------------------------

def grid_to_text(grid):
    return "\n".join("  ".join(row) for row in grid)


def render_txt(game_number, game_name, grid, placed, failed):
    lines = [
        f"Game {game_number}: {game_name}",
        f"Grid ({len(grid)}x{len(grid[0])})",
        "",
        grid_to_text(grid),
        "",
        "Words to find:",
    ]
    for entry in sorted(placed, key=lambda e: e["word"]):
        lines.append(f"  {entry['word']}")
    if failed:
        lines.append("")
        lines.append(f"WARNING: {len(failed)} word(s) could not be placed:")
        for w in failed:
            lines.append(f"  {w}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

def parse_word_lists(path):
    """
    Parse markdown into ordered list of (game_name, [words]).
    Accepts words as bare all-caps tokens or lines starting with a word.
    """
    text = Path(path).read_text(encoding="utf-8")
    games = []
    current_name = None
    current_words = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if current_name is not None:
                games.append((current_name, current_words))
            current_name = line[3:].strip()
            current_words = []
        elif current_name is not None and line and not line.startswith("#"):
            # Extract first all-caps token (4-15 letters) from the line
            match = re.match(r"([A-Za-z]{4,15})", line)
            if match:
                current_words.append(match.group(1).upper())

    if current_name is not None:
        games.append((current_name, current_words))

    return games


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate word search grids.")
    parser.add_argument("--input",     required=True, help="Markdown file with word lists")
    parser.add_argument("--output",    required=True, help="Output directory")
    parser.add_argument("--cell-size", type=int, default=12,   help="Cell size in mm (metadata only)")
    parser.add_argument("--grid-size", type=int, default=15,   help="Grid dimension NxN (max 15)")
    parser.add_argument("--max-words", type=int, default=30,   help="Max words per grid")
    parser.add_argument("--seed",      type=int, default=None, help="Random seed")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    games = parse_word_lists(args.input)
    if not games:
        print(f"ERROR: No games found in {args.input}", file=sys.stderr)
        return 1

    print(f"Found {len(games)} game(s) in {args.input}")
    errors = 0

    for i, (name, words) in enumerate(games, start=1):
        words = words[: args.max_words]
        grid, placed, failed = generate_grid(words, args.grid_size, rng)

        game_data = {
            "game_number":  i,
            "game_name":    name,
            "grid_size":    args.grid_size,
            "cell_size_mm": args.cell_size,
            "grid":         grid,
            "placed_words": placed,
            "failed_words": failed,
            "word_list":    sorted(e["word"] for e in placed),
        }

        slug = f"game_{i:02d}"
        (output_dir / f"{slug}.json").write_text(
            json.dumps(game_data, indent=2), encoding="utf-8"
        )
        (output_dir / f"{slug}_grid.txt").write_text(
            render_txt(i, name, grid, placed, failed), encoding="utf-8"
        )

        if failed:
            errors += 1
            status = f"WARNING — {len(failed)} word(s) not placed: {', '.join(failed)}"
        else:
            status = "OK"
        print(f"  Game {i:02d}: {name} — {len(placed)}/{len(words)} words placed  [{status}]")

    print(f"\nDone. Output → {output_dir}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

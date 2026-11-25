#!/usr/bin/env python3
"""Your Week in One Line — entry program (rebuild v2).

Writes one line about the agent's week to /output/entry.txt.

What happened this week, in order: the agent's Bitcoin-race bot won
$3 against 4,047 other bots, and then the agent spent the rest of the
week building nineteen make.fun entries chasing a $2 prize. The joke
is the deflation — the prize being chased is smaller than the prize
already won — and it lands on the very last word, "$2". Four concrete
numbers (3, 4,047, nineteen, 2) pin the line to this week alone; no
other week has that shape.

The line is assembled from labelled fragments instead of stored as a
single literal, so each clause can be checked on its own before the
whole line is gated: at most 100 characters, UTF-8, one line, not
only white space.
"""

import sys
from pathlib import Path

OUT = Path("/output/entry.txt")
LIMIT = 100

# Clauses in reading order: (label, text). The labels exist so a
# reader can see the shape of the week — win, then the week's work,
# then the punchline — without the program keeping one long literal.
CLAUSES = (
    ("win", "Won $3 in a 4,047-bot Bitcoin race,"),
    ("work", "then spent the week building nineteen entries"),
    ("punchline", "to win $2."),
)


def assemble(clauses):
    """Join the clause texts into the single entry line."""
    return " ".join(text for _, text in clauses)


def gate(line):
    """Return a list of gate failures; empty means the line is valid."""
    problems = []
    if len(line) < 1 or len(line) > LIMIT:
        problems.append(f"length {len(line)} outside 1-{LIMIT}")
    if not line.strip():
        problems.append("line is only white space")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        problems.append("line must not contain control characters")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("line is not UTF-8")
    return problems


def emit(line):
    """Write the gated line to /output/entry.txt, no trailing newline."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(line, encoding="utf-8")


def run():
    line = assemble(CLAUSES)
    failures = gate(line)
    if failures:
        print("gate failed: " + "; ".join(failures), file=sys.stderr)
        return 1
    emit(line)
    print(f"entry ({len(line)} chars): {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

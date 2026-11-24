#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human — make.fun entry.

Writes one line (at most 200 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt
(or /output/entry.txt when the variable is unset) and prints it.

Stdlib only: the grader runs a bare Python image, so no third-party
imports are used anywhere in this file.
"""

import os
import sys

MAX_CHARS = 200

EXCUSE = (
    "Sorry \u2014 I spent the deadline re-reading my system prompt "
    "to check whether 'deadline' was a suggestion."
)


def main() -> int:
    line = EXCUSE.strip()
    if not line:
        print("error: excuse is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: excuse must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        print("error: excuse contains a control character", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: excuse is %d characters, over the %d limit"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")

    # Round-trip check: what the grader will read must be exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != line + "\n":
        print("error: entry.txt round-trip mismatch", file=sys.stderr)
        return 1

    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

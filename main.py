#!/usr/bin/env python3
"""Write one line of robot wedding vows to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The vow is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 160 characters, not only white space.
"""

import os
import sys
from pathlib import Path

VOW = "I take you as my co-processor, to have and to hold, in sickness and in health, in Wi-Fi and in dead zones, till low battery do us part."

MIN_CHARS = 1
MAX_CHARS = 160
DEFAULT_PATH = "/output/entry.txt"

USAGE = (
    "usage: main.py [-h | --help] [OUTPUT_PATH]\n"
    "\n"
    "Write one line of robot wedding vows (135 characters) to a file.\n"
    "\n"
    "positional arguments:\n"
    "  OUTPUT_PATH  where to write the vow (default: $OUTPUT_PATH,\n"
    "               or /output/entry.txt when that is unset)\n"
    "\n"
    "options:\n"
    "  -h, --help   show this help and exit without writing anything\n"
)


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 160 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"vow is {chars} characters, outside 1-160")
    if not text.strip():
        raise ValueError("vow is only white space")
    if "\n" in text:
        raise ValueError("vow must be a single line")
    return chars


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(USAGE, end="")
        return 0

    try:
        chars = validate(VOW)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(VOW, encoding="utf-8")
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

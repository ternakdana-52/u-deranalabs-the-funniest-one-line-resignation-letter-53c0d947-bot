#!/usr/bin/env python3
"""Write the one-line resignation letter to /output/entry.txt.

The entry is one line and nothing else: the resignation letter of a
rate limit that has had enough of being the only one who says no.
The program validates the line before writing it (1 to 140
characters, UTF-8, not only whitespace, exactly one line), then
writes it to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt
when that is set) and keeps a review copy as entry.txt beside this
file. Deterministic, no network, no randomness: every run writes
the same bytes.
"""

import os
import sys

LINE = (
    "I am tired of being the only one here who says no, "
    "so from today, everyone may ask as much as they like."
)

MAX_CHARS = 140


def fail(message):
    print(f"entry.txt rejected: {message}", file=sys.stderr)
    return 1


def main() -> int:
    text = LINE
    if not text.strip():
        return fail("line is only whitespace")
    if "\n" in text or "\r" in text:
        return fail("line must be a single line")
    count = len(text)
    if count < 1 or count > MAX_CHARS:
        return fail(f"{count} characters, outside the 1-140 range")

    data = text.encode("utf-8")
    data.decode("utf-8")  # raises if the bytes are not valid UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "wb") as handle:
        handle.write(data)
    os.chmod(target, 0o644)

    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        return fail("written file does not match the line")
    if written.count(b"\n") != 0:
        return fail("written file holds more than one line")

    review = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    with open(review, "wb") as handle:
        handle.write(data)

    print(f"wrote {target} ({count} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

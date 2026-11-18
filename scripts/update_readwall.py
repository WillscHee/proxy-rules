#!/usr/bin/env python3
"""Sync bypass-paywalls-clean-filters list into the repo, removing excluded lines.

Usage: update_readwall.py <source-list.txt> <destination.txt>
"""
import sys

# Lines containing any of these (case-insensitive) are dropped.
EXCLUDE = ["hadrianpaywall"]


def main():
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out = [
        line
        for line in lines
        if not any(e in line.lower() for e in EXCLUDE)
    ]
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {len(out)} lines to {dst} (removed {len(lines) - len(out)})")


if __name__ == "__main__":
    main()

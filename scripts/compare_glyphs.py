#!/usr/bin/env python3
"""Compare two Glyphs source files and print glyphs missing from the first one."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from glyphsLib import GSFont


def find_missing_glyphs(first_path: Path, second_path: Path) -> list[str]:
    """Find exported glyphs present in the second font and missing from the first."""
    first_font = GSFont(str(first_path))
    second_font = GSFont(str(second_path))

    first_glyph_names = {glyph.name for glyph in first_font.glyphs}
    missing_glyphs = []
    for glyph in second_font.glyphs:
        if glyph.export and glyph.name not in first_glyph_names:
            missing_glyphs.append(glyph.name)
    return missing_glyphs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print glyphs that exist in the second .glyphs file but not in the first"
    )
    parser.add_argument("first", type=Path, help="First .glyphs file")
    parser.add_argument(
        "second", type=Path, help="Second .glyphs file to compare against"
    )
    args = parser.parse_args()

    first_path: Path = args.first.resolve()
    second_path: Path = args.second.resolve()

    for path in (first_path, second_path):
        if not path.is_file():
            print(f"Error: {path} is not a file", file=sys.stderr)
            sys.exit(1)

    missing_glyphs = find_missing_glyphs(first_path, second_path)
    if len(missing_glyphs) == 0:
        print("No missing glyphs found")
        return

    print("Missing glyphs:")
    for glyph_name in missing_glyphs:
        print(f"  {glyph_name}")


if __name__ == "__main__":
    main()

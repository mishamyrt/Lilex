#!/usr/bin/env python3
"""Rename a font family in built font files by modifying name table entries."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from fontTools import ttLib

FONT_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}


def _rename_name_table(font: ttLib.TTFont, source: str, target: str) -> None:
    for record in font["name"].names:
        value = record.toUnicode()
        if source in value:
            font["name"].setName(
                value.replace(source, target),
                record.nameID,
                record.platformID,
                record.platEncID,
                record.langID,
            )


def rename_font_dir(
    source_dir: Path, target_dir: Path, source: str, target: str
) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True)

    for item in source_dir.rglob("*"):
        rel = item.relative_to(source_dir)
        dest = target_dir / Path(*[part.replace(source, target) for part in rel.parts])

        if item.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue

        if item.suffix not in FONT_EXTENSIONS:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        font = ttLib.TTFont(str(item))
        _rename_name_table(font, source, target)
        font.save(str(dest))
        print(f"  {item.name} → {dest.name}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Rename a font family in built font files"
    )
    parser.add_argument("source_dir", type=Path, help="Directory with built font files")
    parser.add_argument("--source", default="Lilex", help="Source family name")
    parser.add_argument("--target", default="LilexDev", help="Target family name")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: sibling of source_dir named after target)",
    )
    args = parser.parse_args()

    source_dir: Path = args.source_dir.resolve()
    if not source_dir.is_dir():
        print(f"Error: {source_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    target_dir: Path = args.output or source_dir.parent / args.target

    print(f"Renaming {args.source} → {args.target}")
    print(f"  {source_dir} → {target_dir}")
    rename_font_dir(source_dir, target_dir, args.source, args.target)
    print(f"Done. Output: {target_dir}")


if __name__ == "__main__":
    main()

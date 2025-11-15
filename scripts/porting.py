#!/usr/bin/env python3
"""A utility for developing pairings to fonts.
I want Italic to have all the same features as a roman font,
this script will allow to control progress
"""

from __future__ import annotations

import json
from pathlib import Path

from arrrgs import arg, command, global_args, run
from glyphsLib import GSFont

ROMAN_FONT_PATH = "sources/Lilex.glyphs"
ITALIC_FONT_PATH = "sources/Lilex-Italic.glyphs"

GLYPH_GROUPS = [
    ("Ligatures", ".liga"),
    ("Sequences", ".seq"),
    ("Bulgarian forms", ".loclBGR"),
    ("Spacers", ".spacer"),
    ("Miscellaneous", None),
]


global_args(
    arg("--snapshot-dir", "-s", default="__snapshots__", help="Snapshot directory"),
)


@command(
    arg("--markdown", "-m", action="store_true", help="Markdown output"),
    arg("--download-url", "-d", help="Download URL"),
)
def progress(args):
    """Finds missing ligatures"""
    missing_glyphs = _find_missing_glyphs()
    snapshot_path = f"{args.snapshot_dir}/missing_glyphs.json"

    with Path(snapshot_path).open("r", encoding="utf-8") as file:
        stored_glyphs = json.load(file)

    diff = len(stored_glyphs) - len(missing_glyphs)
    progress_value = diff / len(stored_glyphs)
    if not args.markdown:
        for glyph in missing_glyphs:
            print(f"- {glyph}")
        print(f"Glyphs coverage: {(progress_value * 100):.2f}%")
        return

    groups = {
        "Miscellaneous": [],
    }
    for glyph in stored_glyphs:
        for group, suffix in GLYPH_GROUPS:
            if suffix is None:
                groups[group].append(glyph)
                continue
            if suffix in glyph:
                if group not in groups:
                    groups[group] = []
                groups[group].append(glyph)
                break

    print("## Glyphs porting progress")
    print(_progress_badge(progress_value))
    print()

    for group, _ in GLYPH_GROUPS:
        glyphs = groups[group]
        coverage = _group_coverage(glyphs, missing_glyphs)
        coverage_url = _progress_url(coverage)
        counts = f"{int(len(glyphs) * coverage)} of {len(glyphs)}"
        print("<details>")
        print("<summary>")
        print(f'<h3>{group} ({counts})</h3>&nbsp;&nbsp;<img src="{coverage_url}">')
        print("</summary>")
        print()
        for glyph in glyphs:
            if glyph in missing_glyphs:
                print(f"- [ ] {glyph}")
            else:
                print(f"- [x] {glyph}")
        print()
        print("</details>")
        print()

    if args.download_url:
        print(f"**[Download]({args.download_url})** CI build")


@command()
def snapshot(args):
    """Dumps missing glyphs"""
    glyphs = _find_missing_glyphs()
    Path(args.snapshot_dir).mkdir(parents=True, exist_ok=True)
    with Path(f"{args.snapshot_dir}/missing_glyphs.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(glyphs, file)
    print(f"Missing glyphs saved to {args.snapshot_dir}/missing_glyphs.json")


def _group_coverage(glyphs: list[str], missing_glyphs: list[str]) -> list[str]:
    """Finds group coverage. Returns number in range 0-1"""
    missing_in_group = list(filter(lambda glyph: glyph in missing_glyphs, glyphs))
    return 1 - (len(missing_in_group) / len(glyphs))


def _progress_badge(value: float) -> str:
    """Generates progress badge"""
    return f"![]({_progress_url(value)})"


def _progress_url(value: float) -> str:
    """Generates progress URL"""
    return f"https://geps.dev/progress/{int(value * 100):.0f}"


def _find_missing_glyphs() -> list[str]:
    """Finds missing glyphs"""
    target_font = GSFont(ROMAN_FONT_PATH)
    source_font = GSFont(ITALIC_FONT_PATH)
    missing_glyphs = []
    for glyph in target_font.glyphs:
        if glyph.export and glyph.name not in source_font.glyphs:
            missing_glyphs.append(glyph.name)
    return missing_glyphs


if __name__ == "__main__":
    run()

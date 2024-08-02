#!/usr/bin/env python3
"""A utility for developing pairings to fonts.
I want Italic to have all the same features as a roman font,
this script will allow to control progress
"""
import json
from os import makedirs

from arrrgs import arg, command, global_args, run
from glyphsLib import GSFont

ROMAN_FONT_PATH = "sources/Lilex.glyphs"
ITALIC_FONT_PATH = "sources/Lilex-Italic.glyphs"


global_args(
    arg("--snapshot-dir", "-s", default="__snapshots__", help="Snapshot directory"),
)

@command(
    arg("--markdown", "-m", action="store_true", help="Markdown output"),
    arg("--download-url", "-d", help="Download URL"),
    arg("--filter", "-f", help="Filter glyphs by name")
)
def progress(args):
    """Finds missing ligatures"""
    missing_glyphs = find_missing_glyphs()
    snapshot_path = f"{args.snapshot_dir}/missing_glyphs.json"

    with open(snapshot_path, mode="r", encoding="utf-8") as file:
        stored_glyphs = json.load(file)

    if args.filter:
        missing_glyphs = list(filter(lambda glyph: args.filter in glyph, missing_glyphs))
        stored_glyphs = list(filter(lambda glyph: args.filter in glyph, stored_glyphs))

    diff = len(stored_glyphs) - len(missing_glyphs)
    progress_value = (diff / len(stored_glyphs)) * 100
    if not args.markdown:
        for glyph in missing_glyphs:
            print(f"- {glyph}")
        print(f"Glyphs coverage: {progress_value:.2f}%")
        return

    print("### Glyphs porting progress")
    print(f"![](https://geps.dev/progress/{progress_value:.0f})")
    print()

    print("<details>")
    print("<summary>Glyphs status</summary>")
    print()
    for glyph in stored_glyphs:
        if glyph in missing_glyphs:
            print(f"- [ ] {glyph}")
        else:
            print(f"- [x] {glyph}")
    print()
    print("</details>")

    if args.download_url:
        print()
        print(f"**[Download]({args.download_url})** CI build")

@command()
def snapshot(args):
    """Dumps missing glyphs"""
    glyphs = find_missing_glyphs()
    makedirs(args.snapshot_dir, exist_ok=True)
    with open(f"{args.snapshot_dir}/missing_glyphs.json", mode="w", encoding="utf-8") as file:
        json.dump(glyphs, file)
    print(f"Missing glyphs saved to {args.snapshot_dir}/missing_glyphs.json")

def find_missing_glyphs() -> list[str]:
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

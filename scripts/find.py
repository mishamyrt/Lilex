#!/usr/bin/env python3
"""Utility script for feature porting.
Finds glyphs in the .fea file
and checks which of them are present in the source font file.

Usage: find.py ../features/calt/hyphen-arrows.fea missing
"""
from re import sub

from arrrgs import arg, command, run
from builder import GlyphsFont
from glyphsLib import GSFont

FONT_FILE = "Lilex.glyphs"

@command(
    arg("file", help="Input .fea file")
)
def glyphs(args):
    """Finds missing glyphs"""
    font = GSFont(FONT_FILE)
    missing_glyphs = []
    gls = glyphs_from_fea(args.file)
    for glyph in gls:
        if glyph not in font.glyphs:
            missing_glyphs.append(glyph)
    if len(missing_glyphs) > 0:
        print("\n".join(missing_glyphs))

    available = len(gls) - len(missing_glyphs)
    _report_progress("Glyphs coverage", len(gls), available)

@command(
    arg("file", help="Input .glyphs file")
)
def ligatures(args):
    """Finds missing ligatures"""
    other_font = GSFont(args.file)
    lilex = GSFont(FONT_FILE)

    liga_count = 0
    missing_ligatures = []
    for glyph in other_font.glyphs:
        name = glyph.name
        if glyph.export and name.endswith(".liga"):
            liga_count += 1
            if name not in lilex.glyphs:
                missing_ligatures.append(name)
    if len(missing_ligatures) > 0:
        print("\n".join(missing_ligatures))

    available = liga_count - len(missing_ligatures)
    _report_progress("Ligatures coverage", liga_count, available)

@command()
def spacers():
    """Finds missing spacers"""
    font = GlyphsFont(FONT_FILE)
    ligas = font.ligatures()
    unique = []
    for liga in ligas:
        first = liga.split("_")[0]
        if first not in unique:
            unique.append(first)
    missing = []
    for glh in unique:
        spacer = f"{glh}.spacer"
        if spacer not in font.file.glyphs:
            missing.append(spacer)

    available = len(unique) - len(missing)
    for name in missing:
        print(f" - {name}")
    _report_progress("Spacers coverage", len(unique), available)

def _report_progress(title: str, total: int, current: int):
    percent = current / total
    print(f"{title}: {(percent * 100):.1f}% ({current}/{total})")

KEYWORDS = [
    "ignore", "sub", "by"
]

def _is_glyph_name(word: str) -> bool:
    return len(word) > 0 and word[0] != "@" and word not in KEYWORDS

def glyphs_from_fea(path: str) -> list[str]:
    with open(path, mode="r", encoding="utf-8") as file:
        content = file.read()
    # Remove comments
    content = sub(r"\#(.*)", "", content)
    # Remove lookups
    content = sub(r"lookup(.*){", "", content)
    content = sub(r"}(.*);", "", content)
    # Remove symbols
    content = sub(r"[';\[\]]", "", content)
    # Remove newlines and duplicated spaces
    content = content.replace("\n", " ")
    content = sub(" +", " ", content)
    # Filter keywords
    words = content.split(" ")
    glyph_names = filter(_is_glyph_name, words)
    unique_glyphs = list(set(glyph_names))
    return sorted(unique_glyphs)

if __name__ == "__main__":
    run()

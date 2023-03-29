#!/usr/bin/env python3
"""Utility script for feature porting.
Finds glyphs in the .fea file
and checks which of them are present in the source font file.

Usage: find.py ../features/calt/hyphen-arrows.fea missing
"""
from re import sub
from typing import List

from arrrgs import arg, command, global_args, run
from glyphsLib import GSFont

FONT_FILE = "Lilex.glyphs"

global_args(
    arg("--file", "-f", required=True, help="Input .fea file")
)

@command()
def missing(_, gls: List[str]):
    """Finds missing glyphs"""
    font = GSFont(FONT_FILE)
    missing_glyphs = []
    for glyph in gls:
        if glyph not in font.glyphs:
            missing_glyphs.append(glyph)
    print("\n".join(missing_glyphs))

    stock = len(gls) - len(missing_glyphs)
    percent = stock / len(gls)
    print(f"\nGlyphs coverage: {(percent * 100):.1f}% ({stock}/{len(gls)})")



@command()
def glyphs(_, gls: List[str]):
    print("\n".join(gls))

KEYWORDS = [
    "ignore", "sub", "by"
]

def _is_glyph_name(word: str) -> bool:
    return len(word) > 0 and word not in KEYWORDS

def glyphs_from_fea(path: str) -> List[str]:
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

def load_words(args):
    words = glyphs_from_fea(args.file)
    return args, words

if __name__ == "__main__":
    run(prepare=load_words)

#!/usr/bin/env python3
"""A script to normalize the names of glyphs.
Uses names from the Glyphs database and replaces names like "uni04B5"
with human-readable names like "tetsecyrillic"
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from glyphsLib import GSComponent, GSFont, GSGlyph

GIST_ID = "635b753408f9b3abf949eb82b1e40b28"
GLYPHS_DATA_FILE = "glyphs-data.xml"
GLYPHS_DATA_URL = f"https://gist.githubusercontent.com/mishamyrt/{GIST_ID}/raw/{GLYPHS_DATA_FILE}"
GLYPHS_DATA_DIR = "/tmp/glyphs-data"
GLYPHS_DATA_PATH = f"{GLYPHS_DATA_DIR}/{GLYPHS_DATA_FILE}"

Rename = tuple[str, str]

def _get_glyph_names():
    """Get names from the Glyphs database"""
    Path(GLYPHS_DATA_DIR).mkdir(parents=True, exist_ok=True)
    if GLYPHS_DATA_FILE not in Path(GLYPHS_DATA_DIR).iterdir():
        print(f"Downloading data from {GLYPHS_DATA_URL}...")
        response = requests.get(GLYPHS_DATA_URL, timeout=10)
        with Path(GLYPHS_DATA_PATH).open("wb") as file:
            file.write(response.content)
    else:
        print("Using cached data")
    tree = ET.parse(GLYPHS_DATA_PATH)
    root = tree.getroot()
    names = {}
    for elem in root.iter():
        if elem.tag == "glyph" and "unicode" in elem.attrib:
            names[elem.attrib["unicode"]] = elem.attrib["name"]
    return names

def _deep_rename(font: GSFont, renames: list[Rename]) -> None:
    """Renames the glyph"""
    for original, target in renames:
        for glyph in font.glyphs:
            if glyph.name == original:
                glyph.name = target
            for layer in glyph.layers:
                for shape in layer.shapes:
                    if isinstance(shape, GSComponent) and shape.name == original:
                        shape.name = target

def _find_renames(
    font: GSFont,
    known_glyphs: dict[str, str]
) -> tuple[list[Rename], list[GSGlyph]]:
    """Renames uni-prefixed glyphs"""
    renames = []
    unknown = []
    for glyph in font.glyphs:
        if glyph.name is None or glyph.unicode is None:
            continue
        code = glyph.unicode.zfill(4).upper()
        if code not in known_glyphs:
            unknown.append(glyph)
            continue
        original = glyph.name
        target = known_glyphs[code]
        if original != target:
            renames.append((original, target))

    changed_originals = [rename[0] for rename in renames]
    additional_renames = []
    for original, target in renames:
        prefix = original + "."
        for glyph in font.glyphs:
            if glyph.name.startswith(prefix) and glyph.name not in changed_originals:
                child_rename = glyph.name.replace(original, target)
                additional_renames.append((glyph.name, child_rename))
    renames += additional_renames
    return sorted(renames, key=lambda rename: rename[0]), unknown

def normalize_names(input_path: str, output_path: str):
    """Normalize the names of glyphs in the input file"""
    known_glyphs = _get_glyph_names()
    print("Finding wrong names...")
    font = GSFont(input_path)
    renames, unknown = _find_renames(font, known_glyphs)

    if len(unknown) > 0:
        print("Unknown glyphs:")
        for glyph in unknown:
            print(f"  {glyph.name} ({glyph.unicode})")

    if len(renames) == 0:
        print("No renames found")
        return

    print("Renaming...")
    _deep_rename(font, renames)

    for name, new_name in renames:
        print(f"  {name} -> {new_name}")

    font.save(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    normalize_names(sys.argv[1], sys.argv[2])

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

GITHUB_REPO = "schriftgestalt/GlyphsInfo"
GITHUB_REPO_BRANCH = "Glyphs3"
GLYPHS_DATA_FILE_NAME = "GlyphData.xml"
GLYPHS_DATA_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_REPO}"
    f"/refs/heads/{GITHUB_REPO_BRANCH}/{GLYPHS_DATA_FILE_NAME}"
)
GLYPHS_DATA_PATH = Path("/tmp") / GLYPHS_DATA_FILE_NAME

Rename = tuple[str, str]


def _get_glyph_data() -> bytes:
    """Get glyph data from the Glyphs database.
    Downloads and caches the data if it's not already present.
    Returns bytes of the XML file.
    """
    if GLYPHS_DATA_PATH.exists():
        return GLYPHS_DATA_PATH.read_bytes()

    print(f"Downloading {GLYPHS_DATA_FILE_NAME}...")
    response = requests.get(GLYPHS_DATA_URL, timeout=10)
    if response.status_code != 200:
        print(f"Failed to download {GLYPHS_DATA_FILE_NAME} from {GLYPHS_DATA_URL}")
        print("Status code:", response.status_code)
        print("Text:", response.text)
        exit(1)

    content = response.content
    GLYPHS_DATA_PATH.write_bytes(content)
    return content


def _get_glyph_names(glyph_data: bytes) -> dict[str, str]:
    """Get a dictionary of unicode values to names from the Glyphs database."""
    tree = ET.fromstring(glyph_data)
    names = {}
    for elem in tree.iter():
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
    font: GSFont, known_glyphs: dict[str, str]
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
    print("Getting glyph data...")
    glyph_data = _get_glyph_data()
    known_glyphs = _get_glyph_names(glyph_data)

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


def main():
    """Main entrypoint"""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_file> [<output_file>]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    normalize_names(input_path, output_path)


if __name__ == "__main__":
    main()

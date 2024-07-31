#!/usr/bin/env python3
"""A script to normalize the names of glyphs.
Uses names from the Glyphs database and replaces names like "uni04B5"
with human-readable names like "tetsecyrillic"
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

import requests

GIST_ID = "635b753408f9b3abf949eb82b1e40b28"
GLYPHS_DATA_FILE = "glyphs-data.xml"
GLYPHS_DATA_URL = f"https://gist.githubusercontent.com/mishamyrt/{GIST_ID}/raw/{GLYPHS_DATA_FILE}"
GLYPHS_DATA_DIR = "/tmp/glyphs-data"
GLYPHS_DATA_PATH = f"{GLYPHS_DATA_DIR}/{GLYPHS_DATA_FILE}"

def _get_glyph_names():
    """Get names from the Glyphs database"""
    os.makedirs(GLYPHS_DATA_DIR, exist_ok=True)
    if GLYPHS_DATA_FILE not in os.listdir(GLYPHS_DATA_DIR):
        print(f"Downloading data from {GLYPHS_DATA_URL}...")
        response = requests.get(GLYPHS_DATA_URL, timeout=10)
        with open(GLYPHS_DATA_PATH, mode="wb") as file:
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

def _replace_names(
    glyphs_content: str,
    known_glyphs: dict[str, str]
) -> tuple[str, int, list[str]]:
    """Renames uni-prefixed glyphs"""
    content = glyphs_content
    matches = re.findall(r"glyphname = uni(.*);", content, re.MULTILINE)
    codes = list(set(matches))
    changed = 0
    not_found = []
    for full_code in codes:
        code_parts = full_code.split(".")
        if len(code_parts) > 1:
            code = code_parts[0]
        else:
            code = full_code
        if code in known_glyphs:
            content = content.replace(f"uni{code}", known_glyphs[code])
            changed += 1
        else:
            not_found.append(f"uni{full_code}")
    return content, changed, not_found

def normalize_names(input_path: str, output_path: str):
    """Normalize the names of glyphs in the input file"""
    with open(input_path, mode="r", encoding="utf-8") as file:
        content = file.read()

    known_glyphs = _get_glyph_names()
    print("Normalizing names...")
    content, changed, unknown = _replace_names(content, known_glyphs)

    print(f"Changed {changed} names")
    if len(unknown) > 0:
        print("Unknown names:")
        for name in unknown:
            print(f"- {name}")

    with open(output_path, mode="w", encoding="utf-8") as file:
        file.write(content)

    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    normalize_names(sys.argv[1], sys.argv[2])

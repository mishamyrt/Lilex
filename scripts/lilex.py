#!/usr/bin/env python3
"""Lilex helper entrypoint"""
import sys
from argparse import BooleanOptionalAction
from typing import List

from arrrgs import arg, command, global_args, run
from builder import DEFAULT_FORMATS, GlyphsFont
from generator import generate_spacers, render_ligatures
from glyphsLib import GSFeature, GSFont
from utils import print_warn, read_classes, read_features, read_files

FONT_FILE = "Lilex.glyphs"
CLASSES_DIR = "./classes"
FEATURES_DIR = "./features"
OUT_DIR = "./build"

global_args(
    arg("--input", "-i", default=FONT_FILE, help="Input .glyphs file"),
    arg("--features", "-f",
    help="A list of features that will be \"baked\" into the font. Comma separated, no spaces")
)

@command(
    arg("--output", "-o", default=FONT_FILE, help="Output file"),
    arg("--params", "-p", action=BooleanOptionalAction, help="Clear masters custom parameters")
)
def generate(args, font: GlyphsFont):
    """Saves the generated source file with features and classes"""
    if args.params:
        for master in font.file.masters:
            names = []
            for param in master.customParameters:
                names.append(param.name)
            for name in names:
                del master.customParameters[name]
    font.save_to(args.output)
    print("☺️ Font source successfully regenerated")

@command(
    arg("formats", nargs="*", help="Format list", default=DEFAULT_FORMATS),
    arg("--store_temp", "-s", action=BooleanOptionalAction,
        help="Not to delete the temporary folder after build")
)
def build(args, font: GlyphsFont):
    """Builds a binary font file"""
    if font.build(args.formats, OUT_DIR, args.store_temp):
        print("☺️ Font binaries successfully builded")
    else:
        print("💔 Failed to build font binaries")
        sys.exit(1)

def generate_calt(font: GlyphsFont) -> GSFeature:
    glyphs = font.ligatures()
    code = render_ligatures(glyphs) + read_files(f"{FEATURES_DIR}/calt")
    return GSFeature("calt", code)

def move_to_calt(font: GSFont, features: List[str]):
    for fea in features:
        if fea not in font.features:
            print(f"Unknown feature: '{fea}'")
            print(font.features)
            sys.exit(1)
        # Move the code of the feature to the calt,
        # which is executed in most cases
        feature = font.features[fea]
        feature.disabled = True
        font.features["calt"].code += "\n" + feature.code
        # Remove feature from aalt
        aalt = font.features["aalt"]
        aalt.code = aalt.code.replace(f"feature {fea};\n", "")

def create_font(args):
    font = GlyphsFont(args.input)

    cls = read_classes(CLASSES_DIR)
    fea = read_features(FEATURES_DIR)

    calt = generate_calt(font)
    fea.append(calt)
    generate_spacers(font.ligatures(), font.file.glyphs)
    font.set_classes(cls)
    font.set_features(fea)

    if args.features is not None:
        features = args.features.split(",")
        move_to_calt(font.file, features)
        print_warn(f"Forced features: {', '.join(features)}")
    return args, font

if __name__ == "__main__":
    run(prepare=create_font)

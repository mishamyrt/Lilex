#!/usr/bin/env python3
"""Lilex helper entrypoint"""
from arrrgs import arg, command, run, global_args
from builder import SUPPORTED_FORMATS, GlyphsFont
from generator import generate_spacers, render_ligatures
from glyphsLib import GSFeature
from utils import read_classes, read_features, read_files

FONT_FILE = "Lilex.glyphs"
CLASSES_DIR = "./classes"
FEATURES_DIR = "./features"
OUT_DIR = "./build"

global_args(
    arg("--input", "-i", default=FONT_FILE, help="Input .glyphs file")
)

@command(
    arg("--output", "-o", default=FONT_FILE, help="Output file")
)
def generate(args, font: GlyphsFont):
    """Saves the generated source file with features and classes"""
    font.save_to(args.output)
    print("☺️ Font source successfully regenerated")

@command(
    arg("formats", nargs="*", help="Format list", default=SUPPORTED_FORMATS)
)
def build(args, font: GlyphsFont):
    """Builds a binary font file"""
    font.build(args.formats, OUT_DIR)
    print("☺️ Font binaries successfully builded")

def generate_calt(font: GlyphsFont) -> GSFeature:
    glyphs = font.ligatures()
    code = render_ligatures(glyphs) + read_files(f"{FEATURES_DIR}/calt")
    return GSFeature("calt", code)

def prepare(args):
    font = GlyphsFont(args.input)

    cls = read_classes(CLASSES_DIR)
    fea = read_features(FEATURES_DIR)

    print(generate_calt(font))
    fea.append(generate_calt(font))

    generate_spacers(font.ligatures(), font.file.glyphs)

    font.set_classes(cls)
    font.set_features(fea)
    return args, font

if __name__ == "__main__":
    run(prepare=prepare)

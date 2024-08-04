#!/usr/bin/env python3
"""Lilex helper entrypoint"""
import os
import sys
from argparse import BooleanOptionalAction
from typing import TypedDict

import yaml
from arrrgs import arg, command, global_args, run
from glyphsLib import GSFont
from liblilex import (
    FontFormat,
    GlyphsFont,
    OpenTypeFeatures,
    build_family,
    generate_spacers,
    render_ligatures,
)

CLASSES_DIR = "sources/classes"
FEATURES_DIR = "sources/features"
OUT_DIR = "build"

global_args(
    arg("--config", "-c", default="family_config.yaml", help="Font config file")
)

AppConfig = TypedDict("AppConfig", {
    "output": str,
    "fonts": list[GlyphsFont],
})

@command(
    arg("--params", "-p", action=BooleanOptionalAction, help="Clear masters custom parameters"),
    arg("--calt_dump", "-c", action=BooleanOptionalAction,
        help="Save the resulting calt code to file (debugging)"),
    arg("--dry_run", "-d", action=BooleanOptionalAction,
        help="Only run code without actually updating source file (debugging)"),
    arg("--version", "-v", default=None, help="Update version in generated file")
)
def generate(args, config: AppConfig):
    """Saves the generated source file with features and classes"""
    for font in config["fonts"]:
        font.clear_opened_files()
        if args.params:
            for master in font.file.masters:
                names = []
                for param in master.customParameters:
                    names.append(param.name)
                for name in names:
                    del master.customParameters[name]
        if args.version:
            font.set_version(args.version)
        if not args.dry_run:
            font.save()
        if args.calt_dump:
            with open(font.name + "-calt.fea", mode="w", encoding="utf-8") as file:
                file.write(font.file.features["calt"].code)
    print("🟢 Font source successfully regenerated")

@command(
    arg("formats", nargs="*", help="Format list", default=['ttf', 'variable']),
    arg("--store_temp", "-s", action=BooleanOptionalAction,
        help="Not to delete the temporary folder after build")
)
async def build(args, config: AppConfig):
    """Builds a binary font file"""
    if not os.path.exists(config["output"]):
        os.makedirs(config["output"])

    formats = []
    for fmt in args.formats:
        formats.append(FontFormat(fmt))

    print("Building font binaries...")
    fonts = [font.file for font in config["fonts"]]
    await build_family(fonts, config["output"], formats)
    print("🟢 Font binaries successfully built")

# def generate_calt(font: GlyphsFont) -> GSFeature:
#     glyphs = font.ligatures()
#     code = render_ligatures(glyphs) + read_files(f"{FEATURES_DIR}/calt")
#     return GSFeature("calt", code)

def move_to_calt(font: GSFont, features: list[str]):
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

def load_font(args):
    with open(args.config, mode="r", encoding="utf-8") as file:
        config_file = yaml.safe_load(file)
    source_dir = config_file["source"]
    features = OpenTypeFeatures(source_dir)
    config = AppConfig(output=config_file["output"], fonts=[])
    for file in config_file["family"]:
        font_config = config_file["family"][file]
        font = GlyphsFont(os.path.join(source_dir, file))
        skips = []
        if font_config is not None and "skip-features" in font_config:
            skips = font_config["skip-features"]
        feats, cls = features.items(
            ignore_features=skips,
            data={
                "calt": render_ligatures(font.ligatures()),
            }
        )
        generate_spacers(font.ligatures(), font.file.glyphs)
        font.set_classes(cls)
        font.set_features(feats)
        font.set_fea_names()
        config["fonts"].append(font)
    return args, config

if __name__ == "__main__":
    run(prepare=load_font)

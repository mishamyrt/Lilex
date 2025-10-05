#!/usr/bin/env python3
"""Lilex helper entrypoint"""
import asyncio
from argparse import BooleanOptionalAction
from typing import TypedDict

from arrrgs import arg, command, global_args, run
from liblilex import (
    FamilyConfig,
    FontFormat,
    GlyphsFont,
    Workspace,
    build_family,
)

global_args(
    arg(
        "--config", "-c", default="sources/family_config.yaml", help="Font config file"
    ),
    arg(
        "--features",
        "-o",
        default=None,
        help="OpenType features that will be forced to be enabled",
    ),
)

AppConfig = TypedDict(
    "AppConfig",
    {
        "output": str,
        "fonts": list[GlyphsFont],
    },
)


@command(
    arg(
        "--params",
        "-p",
        action=BooleanOptionalAction,
        help="Clear masters custom parameters",
    ),
    arg(
        "--calt_dump",
        "-c",
        action=BooleanOptionalAction,
        help="Save the resulting calt code to file (debugging)",
    ),
    arg(
        "--dry_run",
        "-d",
        action=BooleanOptionalAction,
        help="Only run code without actually updating source file (debugging)",
    ),
    arg("--version", "-v", default=None, help="Update version in generated file"),
)
def generate(args, workspace: Workspace):
    """Saves the generated source file with features and classes"""
    for _, font in workspace.sources():
        font.clear_opened_files()
        font.clear_features()
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
    arg("formats", nargs="*", help="Format list", default=["ttf", "variable"]),
    arg("--output", "-o", default="build", help="Output directory"),
    arg(
        "--store_temp",
        "-s",
        action=BooleanOptionalAction,
        help="Not to delete the temporary folder after build",
    ),
)
async def build(args, workspace: Workspace):
    """Builds a binary font file"""
    fmts = []
    for fmt in args.formats:
        fmts.append(FontFormat(fmt))

    print("Building font binaries...")
    build_tasks = [
        build_family(fonts, args.output, fmts) for fonts in workspace.gs_fonts()
    ]
    await asyncio.gather(*build_tasks)
    print("🟢 Font binaries successfully built")


def load_font(args):
    config = FamilyConfig(args.config)
    workspace = Workspace(config)
    if args.features is not None:
        forced = args.features.split(",")
        forced = map(lambda x: x.strip(), forced)
        forced = filter(lambda x: len(x) > 0, forced)
        args.features = list(forced)
    return args, workspace


if __name__ == "__main__":
    run(prepare=load_font)

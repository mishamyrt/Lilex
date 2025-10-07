#!/usr/bin/env python3
"""Lilex helper entrypoint"""

from argparse import BooleanOptionalAction

import rich
from arrrgs import arg, command, global_args, run
from liblilex import FamilyConfig, FontBuildResult, FontFormat, build_family
from utils.stopwatch import Stopwatch

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
    arg(
        "--profiling",
        action=BooleanOptionalAction,
        help="Enable extra logging for profiling",
    ),
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
def generate(args, workspace):
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
async def build(args, config: FamilyConfig):
    """Builds a binary font file"""
    formats = []
    for fmt in args.formats:
        formats.append(FontFormat(fmt))

    with Stopwatch("Building family fonts", args.profiling):
        build_contexts = await build_family(
            config,
            formats,
            output_dir=args.output,
            cache_path="./.builder_cache",
        )

    rich.print(FontBuildResult(build_contexts, args.output))


def load_font(args):
    with Stopwatch("Loading font config", args.profiling):
        config = FamilyConfig(args.config)
    if args.features is not None:
        forced = args.features.split(",")
        forced = map(lambda x: x.strip(), forced)
        forced = filter(lambda x: len(x) > 0, forced)
        args.features = list(forced)
    return args, config


if __name__ == "__main__":
    run(prepare=load_font)

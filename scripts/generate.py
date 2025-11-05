#!/usr/bin/env python3
"""Lilex helper entrypoint"""
from argparse import BooleanOptionalAction

from arrrgs import arg, command, global_args, run
from lilexgen import LilexGenConfig, regenerate_sources

OUT_DIR = "build"

global_args(
    arg("--config", "-c", default="sources/lilexgen_config.yaml", help="Font config file"),
    arg(
        "--features",
        "-o",
        default=None,
        help="OpenType features that will be forced to be enabled",
    ),
    arg("--version", "-v", default=None, help="Update version in generated file"),
)


@command(
    arg(
        "--params",
        "-p",
        action=BooleanOptionalAction,
        help="Clear masters custom parameters",
    ),
    root=True,
)
def generate(args, config: LilexGenConfig):
    """Saves the generated source file with features and classes"""
    forced_features = None
    if args.features is not None:
        forced = args.features.split(",")
        forced = map(lambda x: x.strip(), forced)
        forced = filter(lambda x: len(x) > 0, forced)
        forced_features = list(forced)
    regenerate_sources(config, forced_features, args.version)
    print("🟢 Font source successfully regenerated")


def load_config(args):
    config = LilexGenConfig(args.config)
    return args, config


if __name__ == "__main__":
    run(prepare=load_config)

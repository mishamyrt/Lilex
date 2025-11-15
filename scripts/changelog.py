#!/usr/bin/env python3
"""Utility script release notes generation.

Usage:
Print release notes for a given version:
    changelog.py notes <version> [--input <path>]
Write the changelog with selected version:
    changelog.py release <version> [--input <path>] [--output <path>]
"""

from __future__ import annotations

import datetime
from pathlib import Path

from arrrgs import arg, command, run

CHANGELOG_PATH = "CHANGELOG.md"
REPO_URL = "https://github.com/mishamyrt/Lilex"


def parse_version_heading(line: str) -> str:
    """Parse well-formed version heading from the changelog.
    "## [2.610] — September 05, 2025" -> "2.610"
    """
    version = line[3:]
    if not version.startswith("["):
        return version
    end = version.find("]")
    if end == -1:
        return version
    return version[1:end]


def _format_version_heading(version: str) -> str:
    """Format a well-formed version heading.
    "2.610" -> "## [2.610] — September 05, 2025"
    """
    timestamp = datetime.date.today().strftime("%B %d, %Y")
    return f"## [{version}] — {timestamp}"


def _format_version_url(version: str) -> str:
    return f"[{version}]: {REPO_URL}/releases/tag/{version}"


def collect_notes(changelog_path: Path) -> dict[str, str]:
    """Collects all version notes from the changelog"""
    with changelog_path.open(encoding="utf-8") as file:
        changelog = file.read()
    lines = changelog.split("\n")
    releases = {}
    version = ""
    notes = ""
    for line in lines:
        if line.startswith("## "):
            if version != "":
                releases[version] = notes.strip("\n ")
                notes = ""
            version = parse_version_heading(line)
            continue
        if version == "":
            continue
        notes += line + "\n"
    return releases


@command(
    arg("version", help="Version number"),
    arg("--input", "-i", default=CHANGELOG_PATH, help="Input file"),
    name="notes",
)
def handle_notes(args):
    """Prints selected version notes to the console"""
    input_path = Path(args.input)
    releases = collect_notes(input_path)
    if args.version not in releases:
        print(f"Version {args.version} not found")
        print("Available versions:")
        for version in releases:
            print(f"- {version}")
        return
    print(releases[args.version])


@command(
    arg("version", help="Version number"),
    arg("--input", "-i", default=CHANGELOG_PATH, help="Input file"),
    arg("--output", "-o", default=CHANGELOG_PATH, help="Output file"),
)
def release(args):
    """Writes the changelog with selected version"""
    input_path = Path(args.input)
    with input_path.open(encoding="utf-8") as file:
        changelog = file.read()
    release_heading = _format_version_heading(args.version)
    changelog = changelog.replace("## Next", release_heading)
    changelog += _format_version_url(args.version) + "\n"

    output_path = Path(args.output)
    with output_path.open(mode="w", encoding="utf-8") as file:
        file.write(changelog)
    print("🟢 Changelog successfully written")


if __name__ == "__main__":
    run()

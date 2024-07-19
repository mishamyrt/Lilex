#!/usr/bin/env python3
"""Utility script release notes generation.

Usage: release_notes.py <version>
"""
import datetime

from arrrgs import arg, command, run

NEXT_VERSION_HEADING = "Next"
CHANGELOG_PATH = "CHANGELOG.md"
REPO_URL = "https://github.com/mishamyrt/Lilex"

def read_changelog() -> str:
    with open(CHANGELOG_PATH, mode="r", encoding="utf-8") as file:
        return file.read()

def parse_version_heading(line: str) -> str:
    version = line[3:]
    if not version.startswith("["):
        return version
    end = version.find("]")
    if end == -1:
        return version
    return version[1:end]

def format_version_heading(version: str) -> str:
    timestamp = datetime.date.today().strftime("%B %d, %Y")
    release_heading = f"## [{version}] — {timestamp}"
    return release_heading

def format_version_url(version: str) -> str:
    return f"[{version}]: {REPO_URL}/releases/tag/{version}"

def collect_notes() -> dict[str, str]:
    lines = read_changelog().split("\n")
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
    name="notes"
)
def print_notes(args):
    """Saves the generated source file with features and classes"""
    releases = collect_notes()
    if args.version not in releases:
        print(f"Version {args.version} not found")
        print("Available versions:")
        for version in releases:
            print(f"- {version}")
        return
    for version, notes in releases.items():
        if version == args.version:
            print(notes)

@command(
    arg("version", help="Version number")
)
def release(args):
    """Regenerates the changelog with the new version"""
    # May 10, 2024
    timestamp = datetime.date.today().strftime("%B %d, %Y")
    release_heading = f"## [{args.version}] — {timestamp}"
    changelog = read_changelog()
    changelog = changelog.replace(f"## {NEXT_VERSION_HEADING}", release_heading)
    changelog += "\n" + format_version_url(args.version) + "\n"
    with open(CHANGELOG_PATH, mode="w", encoding="utf-8") as file:
        file.write(changelog)
    print("🟢 Changelog successfully updated")

if __name__ == "__main__":
    run()

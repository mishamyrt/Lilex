#!/usr/bin/env python3
"""Utility script for feature proofing.
Prints test cases in stdout.

Usage: show.py
"""
from arrrgs import root_command, run

from preview import FEATURES, print_features


@root_command()
def preview():
    """Saves the generated source file with features and classes"""
    print_features(FEATURES)

if __name__ == "__main__":
    run()

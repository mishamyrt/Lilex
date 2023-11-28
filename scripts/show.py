#!/usr/bin/env python3
"""Utility script for feature proofing.
Prints test cases in stdout.

Usage: show.py
"""
from arrrgs import command, run

from preview import FEATURES, print_features


@command(root=True)
def preview():
    """Saves the generated source file with features and classes"""
    print_features(FEATURES)

if __name__ == "__main__":
    run()

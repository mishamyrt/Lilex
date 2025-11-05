#!/usr/bin/env python3
"""Utility script for feature proofing.
Prints test cases in stdout.

Usage: show.py
"""

from preview import FEATURES, print_features

if __name__ == "__main__":
    print_features(FEATURES)

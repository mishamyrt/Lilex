"""CLI utilities"""
from typing import List

from glyphsLib import GSFeature


def print_gs(title: str, items: List[GSFeature]):
    print(f"{title}:")
    for item in items:
        print(f"  - {item.name}")

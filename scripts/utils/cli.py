"""CLI utilities"""
from glyphsLib import GSFeature

ORANGE = "\033[93m"
RESET = "\033[0m"

def print_gs(title: str, items: list[GSFeature]):
    print(f"{title}:")
    for item in items:
        print(f"  - {item.name}")

def print_warn(message: str):
    print(f"{ORANGE}{message}{RESET}")

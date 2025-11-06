"""Feature preview base"""
from __future__ import annotations

from colored import Style


class FeaturePreview:
    """Feature preview baseclass"""

    name: str = ""

    def __init__(self) -> None:
        """Initialized feature"""

    def show(self):
        """Prints feature"""


def print_features(features: list[FeaturePreview]):
    """Prints given feature previews"""
    for fea in features:
        print(f"{Style.BOLD}{fea.name}{Style.reset}")
        fea.show()

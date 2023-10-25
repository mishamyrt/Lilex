"""Feature preview base"""
from typing import List

from colored import Style


class FeaturePreview():
    """Feature preview baseclass"""
    name: str = ""
    def __init__(self) -> None:
        pass

    def show(self):
        pass

def print_features(features: List[FeaturePreview]):
    for fea in features:
        print(f'{Style.BOLD}{fea.name}{Style.reset}')
        fea.show()

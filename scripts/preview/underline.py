"""Powerline preview"""
from typing import Tuple

from colored import attr

from .base import FeaturePreview

class UnderlineFeature(FeaturePreview):
    name = "Underline alignment"

    def show(self):
        print(f'{attr("underlined")}Te{attr("bold")}st{attr("reset")}')

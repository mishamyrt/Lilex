"""Powerline preview"""

from colored import Style

from .base import FeaturePreview


class UnderlineFeature(FeaturePreview):
    name = "Underline alignment"

    def show(self):
        print(f'{Style.underline}Te{Style.bold}st{Style.reset}')

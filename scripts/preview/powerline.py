"""Powerline preview"""
from colored import Style, back, fore

from .base import FeaturePreview

PowerlineEntry = tuple[str, str]

VC_BRANCH_CHAR = "\uE0A0"
LN_CHAR = "\uE0A1"
LOCK_CHAR = "\uE0A2"
RIGHT_BLACK_ARROW_CHAR = "\uE0B0"
RIGHT_ARROW_CHAR = "\uE0B1"
LEFT_BLACK_ARROW_CHAR = "\uE0B2"
LEFT_ARROW_CHAR = "\uE0B3"

class PowerlineFeature(FeaturePreview):
    name = "Powerline"

    def show(self):
        self._print_glyphs()
        self._print_examples()

    def _print_glyphs(self):
        self._print_glyph(VC_BRANCH_CHAR, "Version control branch")
        self._print_glyph(LN_CHAR, "LN (line) symbol")
        self._print_glyph(LOCK_CHAR, "Closed padlock")
        self._print_glyph(RIGHT_BLACK_ARROW_CHAR, "Rightwards black arrowhead")
        self._print_glyph(RIGHT_ARROW_CHAR, "Rightwards arrowhead")
        self._print_glyph(LEFT_BLACK_ARROW_CHAR, "Leftwards black arrowhead")
        self._print_glyph(LEFT_ARROW_CHAR, "Leftwards arrowhead")

    def _print_examples(self):
        self._print_line([
            ("grey_11", "~"),
            ("grey_30", "Git/Lilex"),
            ("grey_46", f'{VC_BRANCH_CHAR} dev'),
        ])


    def _print_line(self, entries: list[PowerlineEntry], right=True):
        line = ""
        if right:
            arrow = RIGHT_ARROW_CHAR
            arrow_black = RIGHT_BLACK_ARROW_CHAR
        else:
            arrow = LEFT_ARROW_CHAR
            arrow_black = LEFT_BLACK_ARROW_CHAR
        for i, entry in enumerate(entries):
            (color, text) = entry
            content = f' {text.replace("/", f" {arrow} ")} '
            template = f'{back(color)}{fore("light_gray")}{content}'
            if i == len(entries) - 1:
                template += f'{Style.reset}'
            else:
                template += f'{back(entries[i+1][0])}'
            template += f'{fore(color)}{arrow_black}'
            line += template
        print(line)

    def _print_glyph(self, glyph: str, name: str, width=30):
        padding = ' ' * (width - len(name))
        print(f'{fore("dark_gray")}{name}{Style.reset}{padding}{glyph}')

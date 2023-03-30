"""Ligatures feature generator module"""
from typing import List

from .const import IGNORE_PREFIXES, IGNORE_TPL, IGNORES, REPLACE_TPL


def _populate_tpl(templates: List[str], prefix: str) -> str:
    """Renders fea statements"""
    result = ""
    for value in templates:
        result += f"  {prefix} {value};\n"
    return result

def _populate_ignore(templates: List[str]) -> str:
    """Renders ignore sub statements"""
    return _populate_tpl(templates, "ignore sub")

def _populate_sub(templates: List[str]) -> str:
    """Renders sub statements"""
    return _populate_tpl(templates, "sub")

class LigatureLookup:
    ignores: List[str] = []
    subs: List[str] = []
    glyphs: tuple
    name: str

    def __init__(self, name: str):
        basename = name.replace(".liga", "")
        self.name = basename
        self.glyphs = tuple(basename.split("_"))

    def add_ignore(self, rule: str):
        self.ignores.append(rule)

    def add_sub(self, rule: str):
        self.subs.append(rule)

    def __str__(self) -> str:
        count = len(self.glyphs)
        template = f"lookup {self.name}" + " { \n"
        if self.glyphs in IGNORES:
            template += _populate_ignore(IGNORES[self.glyphs])
        if self.name not in IGNORE_PREFIXES:
            template += _populate_ignore(IGNORE_TPL[count])
        template += _populate_sub(REPLACE_TPL[count])
        template += "} " + f"{self.name};"
        return self._hydrate(template)

    def _hydrate(self, template: str) -> str:
        result = template
        for i, glyph in enumerate(self.glyphs):
            result = result.replace(str(i + 1), glyph)
        return result

def render_ligatures(items: List[str]) -> str:
    """Renders the list of ligatures in the OpenType feature"""
    result = ""
    for name in items:
        lookup = LigatureLookup(name)
        result += f"{lookup}\n\n"
    return result.rstrip()

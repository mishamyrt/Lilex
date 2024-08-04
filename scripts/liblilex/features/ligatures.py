"""Ligatures feature generator module"""
from __future__ import annotations

from re import sub

from .const import IGNORE_TPL, IGNORES, PRIORITIES, REPLACE_TPL, SKIP_IGNORES


def _populate_tpl(templates: list[str], prefix: str) -> str:
    """Renders fea statements"""
    result = ""
    for value in templates:
        normalized_value = sub(" +", " ", value)
        result += f'  {prefix} {normalized_value};\n'
    return result

def _populate_ignore(templates: list[str]) -> str:
    """Renders ignore sub statements"""
    return _populate_tpl(templates, "ignore sub")

def _populate_sub(templates: list[str]) -> str:
    """Renders sub statements"""
    return _populate_tpl(templates, "sub")

class LigatureLookup:
    ignores: list[str] = []
    subs: list[str] = []
    glyphs: tuple
    name: str

    @property
    def priority(self) -> int:
        if self.glyphs in PRIORITIES:
            return PRIORITIES[self.glyphs]
        return 99

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
        template = f"lookup {self.name}" + " {\n"
        if self.glyphs not in SKIP_IGNORES:
            template += _populate_ignore(IGNORE_TPL[count])
        if self.glyphs in IGNORES:
            template += _populate_ignore(IGNORES[self.glyphs])
        template += _populate_sub(REPLACE_TPL[count])
        template += "} " + f"{self.name};"
        return self._hydrate(template)

    def _hydrate(self, template: str) -> str:
        result = template
        for i, glyph in enumerate(self.glyphs):
            result = result.replace(str(i + 1), glyph)
        return result

def render_ligatures(items: list[str]) -> str:
    """Renders the list of ligatures in the OpenType feature"""
    lookups = []
    for name in items:
        lookups.append(LigatureLookup(name))
    lookups.sort(key=lambda x: (x.priority, -len(x.glyphs), x.name))
    code = ""
    for lookup in lookups:
        code += f"{lookup}\n\n"
    return code.rstrip()

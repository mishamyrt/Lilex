"""Spacer generator"""
from typing import List

from glyphsLib import GSGlyph

def _required_spacers(name: str) -> List[str]:
    return name.split("_")[0:-1]

def generate_spacers(ligatures: List[str], glyphs: List[GSGlyph]) -> List[str]:
    """Finds missing spacers"""
    unique = []
    for liga in ligatures:
        unique.extend(_required_spacers(liga))

    unique = list(set(unique))
    template = glyphs["spacer.tpl"]
    for glh in unique:
        name = f"{glh}.spacer"
        if name not in glyphs:
            spacer = GSGlyph()
            spacer.name = name
            spacer.layers = template.layers
            glyphs.append(spacer)

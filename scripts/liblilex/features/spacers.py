"""Spacer generator"""
from glyphsLib import GSGlyph


def _required_spacers(name: str) -> list[str]:
    return name.split("_")[0:-1]

def generate_spacers(ligatures: list[str], glyphs: list[GSGlyph]) -> list[str]:
    """Finds missing spacers"""
    unique = []
    for liga in ligatures:
        unique.extend(_required_spacers(liga))

    unique = list(set(unique))
    template = glyphs["spacer.tpl"]
    if template is None:
        raise ValueError("Missing 'spacer.tpl' in glyphs font")
    for glh in unique:
        name = f"{glh}.spacer"
        if name not in glyphs:
            spacer = GSGlyph()
            spacer.name = name
            spacer.layers = template.layers
            glyphs.append(spacer)

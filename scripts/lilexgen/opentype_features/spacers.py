"""Spacer generator"""

from glyphsLib import GSFont, GSGlyph


def _required_spacers(name: str) -> list[str]:
    """Returns required spacers for ligature by glyph name"""
    return name.split("_")[0:-1]


def _create_spacer(name: str, template: GSGlyph) -> GSGlyph:
    """Creates a spacer glyph"""
    spacer = GSGlyph()
    spacer.name = name
    spacer.layers = template.layers
    return spacer


def _collect_required_spacers(ligatures: list[str]) -> list[str]:
    """Collects required spacers for ligatures"""
    spacers = map(_required_spacers, ligatures)
    spacers = [item for sublist in spacers for item in sublist]
    return list(set(spacers))


def insert_spacers(ligatures: list[str], font: GSFont) -> list[str]:
    """Finds missing spacers and inserts them into the font"""
    template = font.glyphs["spacer.tpl"]
    if template is None:
        raise ValueError("Missing 'spacer.tpl' in glyphs font")

    spacers = _collect_required_spacers(ligatures)
    inserted = set()

    for spacer_name in spacers:
        glyph_name = f"{spacer_name}.spacer"
        if glyph_name not in font.glyphs:
            spacer = _create_spacer(glyph_name, template)
            font.glyphs.append(spacer)
            inserted.add(glyph_name)

    return list(inserted)

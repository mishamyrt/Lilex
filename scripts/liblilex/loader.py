"""Font loader"""

import os
from copy import deepcopy

from glyphsLib import GSFont

from .config import FamilyConfig, FontDescriptor, FontDescriptorKind
from .opentype_features import OpenTypeFeatures

GSFontGroup = tuple[str, list[GSFont]]


def load_family(config: FamilyConfig) -> list[GSFontGroup]:
    """Loads a family of fonts from a config"""
    loader = FontLoader(config)

    fonts = []
    for group_name, descriptors in config.fonts:
        group_fonts = []
        for descriptor in descriptors:
            font = loader.load(descriptor)
            group_fonts.append(font)
        fonts.append((group_name, group_fonts))
    return fonts


class FontLoader:
    _cache: dict[str, GSFont]
    _dir: str
    _font_map: dict[str, FontDescriptor]
    _features: OpenTypeFeatures

    def __init__(self, config: FamilyConfig):
        """Loads fonts from a config"""
        self._cache = {}
        self._dir = config.dir
        self._font_map = config.font_map
        self._features = OpenTypeFeatures(config.features_dir)

    def load(self, descriptor: FontDescriptor) -> GSFont:
        if descriptor.name in self._cache.values():
            return self._cache[descriptor.name]

        source_path = os.path.join(self._dir, descriptor.name)
        font = GSFont(source_path)
        if descriptor.kind == FontDescriptorKind.SOURCE:
            return font
        elif descriptor.kind == FontDescriptorKind.PATCH:
            target_name = descriptor.config.get("target")
            target_descriptor = self._font_map[target_name]
            target_font = self.load(target_descriptor)
            font = _merge_fonts(target_font, font)
        else:
            raise ValueError(f"Unknown node kind: {descriptor.kind}")

        self._features.inject(font)
        self._cache[descriptor.name] = font
        return font


def _merge_fonts(base: GSFont, patch: GSFont) -> GSFont:
    """Merges two fonts"""
    font = deepcopy(base)
    font.familyName = patch.familyName
    # Merge glyphs
    for glyph in patch.glyphs:
        glyph_idx = _find_glyph_index(font, glyph.name)
        if glyph_idx == -1:
            font.glyphs.append(glyph)
        else:
            font.glyphs[glyph_idx] = glyph
    # Merge custom parameters
    for param in patch.customParameters:
        if param.name in font.customParameters:
            font.customParameters[param.name] = param.value
        else:
            font.customParameters.append(param)
    return font


def _find_glyph_index(font: GSFont, glyph_name: str) -> int:
    """Finds the index of a glyph in a font"""
    for idx, glyph in enumerate(font.glyphs):
        if glyph.name == glyph_name:
            return idx
    return -1

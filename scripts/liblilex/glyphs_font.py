"""Glyphs helper"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Callable

from glyphsLib import (
    GSClass,
    GSFeature,
    GSFont,
    GSGlyph,
)

from .features import NAME_TPL, feature_prefix, name_from_code

GlyphFilter = Callable[[GSGlyph], bool]

class GlyphsFont:
    """Glyphs font file controller"""
    path: str
    _font: GSFont = None
    _name: str

    def __init__(self, path: str, name: str = None):
        self.path = path
        self._font = GSFont(path)
        self.is_ephemeral = False
        if name is None:
            self._name = Path(path).stem
        else:
            self._name = name

    @property
    def file(self) -> GSFont:
        return self._font

    @property
    def name(self) -> str:
        return self._name

    def ligatures(self) -> list[GSGlyph]:
        """Returns a list of ligatures"""
        return self.glyphs(lambda x: x.name.endswith(".liga") and x.export)

    def glyphs(self, filter_fn: GlyphFilter = lambda x: True) -> list[GSGlyph]:
        """Returns a list of glyphs that match filter"""
        return list(filter(filter_fn, self._font.glyphs))

    def patched(self, patch: GlyphsFont) -> GlyphsFont:
        """Returns a new font with the patch applied"""
        font = deepcopy(self)
        for glyph in patch.glyphs():
            glyph_idx = _find_glyph_index(font, glyph.name)
            if glyph_idx == -1:
                font.file.glyphs.append(glyph)
            else:
                font.file.glyphs[glyph_idx] = glyph
        for param in patch.file.customParameters:
            if param.name in font.file.customParameters:
                font.file.customParameters[param.name] = param.value
            else:
                font.file.customParameters.append(param)
        font.file.familyName = patch.file.familyName
        font.path = patch.path

        return font

    def save(self):
        """Saves the file to the same path from which it was opened"""
        self._font.save(self.path)

    def save_to(self, path: str = None) -> None:
        """Saves the file to the specified path"""
        self._font.save(path)

    def set_classes(self, classes: list[GSClass]):
        """Sets the font classes"""
        for cls in classes:
            if cls.name in self._font.classes:
                self._font.classes[cls.name] = cls
            else:
                self._font.classes.append(cls)

    def set_features(self, features: list[GSFeature]):
        """Sets the font features"""
        for fea in features:
            if fea.name in self._font.features:
                self._font.features[fea.name] = fea
            else:
                self._font.features.append(fea)

    def clear_features(self):
        """Clears the font features"""
        self._font.features = []
        self._font.classes = []

    def set_version(self, version: str):
        parts = version.split(".")
        assert len(parts) == 2
        self._font.versionMajor = int(parts[0])
        self._font.versionMinor = int(parts[1])

    def clear_opened_files(self):
        self._font.DisplayStrings = ""

    def set_fea_names(self):
        for fea in self._font.features:
            prefix = feature_prefix(fea.name)
            if prefix in NAME_TPL:
                feature = self._font.features[fea.name]
                name = name_from_code(feature.code)
                if name is not None:
                    feature.code = NAME_TPL[prefix].replace("$NAME", name) + feature.code

def _find_glyph_index(font: GlyphsFont, glyph_name: str) -> int:
    """Finds the index of a glyph in a font"""
    for idx, glyph in enumerate(font.file.glyphs):
        if glyph.name == glyph_name:
            return idx
    return -1

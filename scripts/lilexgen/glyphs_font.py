"""Glyphs helper"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from glyphsLib import (
    GSClass,
    GSFeature,
    GSFont,
    GSGlyph,
)

from .opentype_features import NAME_TPL, feature_prefix, name_from_code

GlyphFilter = Callable[[GSGlyph], bool]

LIGATURE_SUFFIX = ".liga"

class GlyphsFont:
    """Glyphs font file controller"""
    _font: GSFont = None
    _path: str
    _name: str

    def __init__(self, path: str, name: str = None):
        self._font = GSFont(path)
        self._path = path
        if name is None:
            self._name = Path(self._path).stem
        else:
            self._name = name

    @property
    def file(self) -> GSFont:
        return self._font

    @property
    def name(self) -> str:
        return self._name

    def ligatures(self) -> list[str]:
        glyphs = self.glyphs(lambda x: x.name.endswith(LIGATURE_SUFFIX))
        ligatures = []
        for glyph in glyphs:
            if glyph.export:
                ligatures.append(glyph.name)
        return ligatures

    def glyphs(self, _filter: GlyphFilter = lambda x: True) -> list[GSGlyph]:
        """Returns a list of glyphs that match filter"""
        result = []
        for glyph in self._font.glyphs:
            if _filter(glyph):
                result.append(glyph)
        return result

    def save(self):
        """Saves the file to the same path from which it was opened"""
        self._font.save(self._path)

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

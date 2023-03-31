"""Glyphs helper"""
from __future__ import annotations

import sys
from typing import Callable, List

from glyphsLib import (
    GSClass,
    GSFeature,
    GSFont,
    GSGlyph,
    build_masters,
)

from .const import SUPPORTED_FORMATS, UFO_PATH
from .make import make

LIGATURE_SUFFIX = ".liga"
GlyphFilter = Callable[[GSGlyph], bool]

class GlyphsFont:
    """Glyphs font builder"""
    _font: GSFont = None
    _path: str

    def __init__(self, path: str):
        self._font = GSFont(path)
        self._path = path

    @property
    def file(self) -> GSFont:
        return self._font

    def ligatures(self) -> List[str]:
        glyphs = self.glyphs(lambda x: x.name.endswith(LIGATURE_SUFFIX))
        ligatures = []
        for glyph in glyphs:
            if glyph.export:
                ligatures.append(glyph.name)
        return ligatures

    def glyphs(self, _filter: GlyphFilter) -> List[GSGlyph]:
        """Returns a list of glyphs that match filter"""
        result = []
        for glyph in self._font.glyphs:
            if _filter(glyph):
                result.append(glyph)
        return result

    def save(self):
        """Saves the file to the same path from which it was opened"""
        self._font.save(self._path)

    def save_to(self, path: str) -> None:
        """Saves the file to the specified path"""
        self._font.save(path)

    def set_classes(self, classes: List[GSClass]):
        """Sets the font classes"""
        for cls in classes:
            if cls.name in self._font.classes:
                self._font.classes[cls.name] = cls
            else:
                self._font.classes.append(cls)

    def set_features(self, features: List[GSFeature]):
        """Sets the font features"""
        for fea in features:
            if fea.name in self._font.features:
                self._font.features[fea.name] = fea
            else:
                self._font.features.append(fea)

    def build(self, formats: List[str], out_dir: str) -> bool:
        print("Generating master UFOs")
        build_masters(self._path, UFO_PATH, write_skipexportglyphs=True)
        ds_path = f"{UFO_PATH}/{self._font.familyName}.designspace"
        success = True
        for fmt in formats:
            if fmt not in SUPPORTED_FORMATS:
                print(f"Unsupported format '{fmt}'")
                sys.exit(1)
            success = success and make(ds_path, fmt, f"{out_dir}/{fmt}")
        return success

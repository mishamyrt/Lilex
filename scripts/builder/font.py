"""Glyphs helper"""
from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Callable

from glyphsLib import (
    GSClass,
    GSFeature,
    GSFont,
    GSGlyph,
    build_masters,
)

from .const import NAME_TPL, SUPPORTED_FORMATS
from .make import make
from .name import feature_prefix, name_from_code

LIGATURE_SUFFIX = ".liga"
GlyphFilter = Callable[[GSGlyph], bool]

class GlyphsFont:
    """Glyphs font builder"""
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

    def save_to(self, path: str) -> None:
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

    def build(self, formats: list[str], out_dir: str, store_temp=False) -> bool:
        print("Preparing build environment")
        temp_dir, ds_file = self._prepare_build()
        success = True
        for fmt in formats:
            if fmt not in SUPPORTED_FORMATS:
                print(f'Unsupported format "{fmt}"')
                break
            fmt_dir = f'{out_dir}/{fmt}'
            success = success and make(self._name, ds_file, fmt, fmt_dir)
        if store_temp:
            print(f'Build directory: {temp_dir}')
        else:
            rmtree(temp_dir)
        return success

    def _set_fea_names(self):
        for fea in self._font.features:
            prefix = feature_prefix(fea.name)
            if prefix in NAME_TPL:
                feature = self._font.features[fea.name]
                name = name_from_code(feature.code)
                if name is not None:
                    feature.code = NAME_TPL[prefix].replace("$NAME", name) + feature.code

    def _prepare_build(self) -> str:
        self._set_fea_names()
        temp_dir = mkdtemp(prefix="LilexBuild")
        glyphs_file = f'{temp_dir}/{self._font.familyName}.glyphs'
        ufo_dir = f'{temp_dir}/master_ufo'
        ds_file = f"{ufo_dir}/{self._name}.designspace"
        self.save_to(glyphs_file)
        build_masters(
            glyphs_file,
            ufo_dir,
            write_skipexportglyphs=True
        )
        return (temp_dir, ds_file)

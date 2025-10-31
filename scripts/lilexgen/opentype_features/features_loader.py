"""OpenType code loader"""

from __future__ import annotations

import os
import re
from typing import TypeVar

from glyphsLib import GSClass, GSFeature, GSFont

from .const import NAME_TPL
from .ligatures import render_ligature_lookups
from .spacers import insert_spacers

CLASSES_DIR = "_classes"
FEATURE_EXT = ".fea"
CLASS_EXT = ".cls"


class OpenTypeFeatures:
    """Utility class for loading OpenType code files. Can filter features fo sub-font."""

    _path: str
    _features: dict[str, GSFeature]
    _classes: list[GSClass]

    def __init__(self, sources_dir: str, forced: list[str] = None):
        cls_dir = os.path.join(sources_dir, CLASSES_DIR)
        self._path = sources_dir
        self._features = _read_features(sources_dir)
        self._classes = _read_classes(cls_dir)

        if forced is None:
            return

        aalt_fea = self._features["aalt"]
        calt_fea = self._features["calt"]
        if calt_fea is None:
            calt_fea = GSFeature("calt", "")

        for fea in forced:
            if fea in ("calt", "aalt"):
                raise ValueError("calt and aalt features are not allowed to be forced")
            if fea not in self._features:
                raise ValueError(f"Unknown feature: '{fea}'")
            if aalt_fea is not None:
                aalt_fea.code = aalt_fea.code.replace(f"feature {fea};\n", "")

            self._features[fea].disabled = True
            calt_fea.code += "\n" + self._features[fea].code

    def inject(self, font: GSFont):
        ligatures = self._find_ligatures(font)
        calt_code = render_ligature_lookups(ligatures)
        font_features = self._features.copy()
        font_features["calt"] = GSFeature("calt", calt_code)
        if "calt" in self._features:
            font_features["calt"].code += "\n" + self._features["calt"].code
        # Set features
        for fea in font_features.values():
            if fea.name in font.features:
                font.features[fea.name] = fea
            else:
                font.features.append(fea)
        # Set classes
        for cls in self._classes:
            if cls.name in font.classes:
                font.classes[cls.name] = cls
            else:
                font.classes.append(cls)
        insert_spacers(ligatures, font)

    def _find_ligatures(self, font: GSFont) -> list[str]:
        """Finds ligatures glyphs in the font and returns their names"""
        glyphs = filter(lambda x: x.name.endswith(".liga") and x.export, font.glyphs)
        glyph_names = map(lambda x: x.name, glyphs)
        return list(glyph_names)

    def _render_features(
        self, ligatures: list[str], forced: list[str] = None
    ) -> list[GSFeature]:
        """Returns a lists of features for ligatures list"""
        calt_code = render_ligature_lookups(ligatures)
        calt_fea = GSFeature("calt", calt_code)
        fea_map = {
            **self._features,
            "calt": calt_fea,
        }
        for fea_name, feature in self._features.items():
            # Get first segment of the feature path
            if "/" in fea_name:
                fea_name = fea_name.split("/")[0]

            # Add feature to the map
            if fea_name not in fea_map:
                fea_map[fea_name] = feature
            else:
                fea_map[fea_name].code += "\n" + feature.code

            prefix = _feature_prefix(fea_name)
            if prefix in NAME_TPL:
                feature = fea_map[fea_name]
                name = _title_from_code(feature.code)
                if name is not None:
                    feature.code = (
                        NAME_TPL[prefix].replace("$NAME", name) + feature.code
                    )

        if forced is not None:
            aalt_fea = fea_map["aalt"]
            for fea in forced:
                if fea not in fea_map:
                    raise ValueError(f"Unknown feature: '{fea}'")
                fea_map[fea].disabled = True
                calt_fea.code += "\n" + fea_map[fea].code
                aalt_fea.code = aalt_fea.code.replace(f"feature {fea};\n", "")

        return list(fea_map.values())


def _read_features(features_path: str) -> dict[str, GSFeature]:
    """Read all features in the directory.
    Also it will correctly load feature names.
    Nested features will be merged into the feature with root directory name.
    """
    feature_paths = _list_files(features_path)
    features = {}
    for path in feature_paths:
        if CLASSES_DIR in path:
            continue
        name = _name_from_path(path, features_path)
        feature = _read_gs_file(path, GSFeature)
        prefix = _feature_prefix(name)
        if prefix in NAME_TPL:
            title = _title_from_code(feature.code)
            if title is not None:
                feature.code = NAME_TPL[prefix].replace("$NAME", title) + feature.code

        if name in features:
            features[name].code += "\n" + feature.code
        else:
            features[name] = feature
    return features


FEATURE_NAME_RE = re.compile(r"Name:(.*)")
FEATURE_PREFIX_RE = re.compile(r"([a-z]+)")


def _name_from_path(path: str, features_path: str) -> str:
    """Extracts the name from the feature path.
    For nested features, it will return root directory name.
    - `sources/opentype_features/calt.fea` -> `calt`
    - `sources/opentype_features/calt/colon.fea` -> `calt`
    """
    rel_name = os.path.relpath(path, features_path).removesuffix(FEATURE_EXT)
    return rel_name.split("/")[0]


def _title_from_code(content: str) -> str | None:
    """Extracts the name from the feature code"""
    try:
        result = FEATURE_NAME_RE.search(content)
        return result.group(1).strip()
    except AttributeError:
        return None


def _feature_prefix(name: str) -> str | None:
    """Extracts the prefix from the feature name"""
    try:
        result = FEATURE_PREFIX_RE.match(name)
        return result.group(1)
    except AttributeError:
        return None


def _read_classes(dir_path: str) -> list[GSClass]:
    """Read all classes in the directory"""
    classes = []
    for path in _list_files(dir_path):
        cls = _read_gs_file(path, GSClass)
        classes.append(cls)
    return classes


T = TypeVar("T")


def _read_gs_file(path: str, constructor: T) -> T:
    """Read a glyphsLib file"""
    name = os.path.basename(path).split(".")[0]
    with open(path, mode="r", encoding="utf-8") as file:
        return constructor(name, file.read())


def _list_files(dir_path: str) -> list[str]:
    """List matching files in the directory.
    Ignores files starting with a dot and with .disabled suffix.
    Recursively lists files in subdirectories.
    """
    files = []
    for file in os.listdir(dir_path):
        name = os.path.splitext(file)[0]
        if os.path.splitext(file)[0].endswith(".disabled"):
            print(f'WARN: "{os.path.splitext(name)[0]}" is ignored')
            continue
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path) and not file.startswith("."):
            files.append(file_path)
        elif os.path.isdir(file_path):
            files.extend(_list_files(file_path))
    return sorted(files)

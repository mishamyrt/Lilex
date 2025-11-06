"""OpenType code loader"""

from __future__ import annotations

import re
from pathlib import Path

from glyphsLib import GSClass, GSFeature, GSFont

from .const import NAME_TPL
from .ligatures import render_ligature_lookups
from .spacers import insert_spacers

CLASSES_DIR = "_classes"
FEATURE_EXT = ".fea"
CLASS_EXT = ".cls"


class OpenTypeFeatures:
    """Utility class for loading OpenType code files. Can filter features fo sub-font."""

    _path: Path
    _features: dict[str, GSFeature]
    _classes: list[GSClass]

    def __init__(self, sources_dir: str | Path, forced: list[str] = None):
        sources_dir = Path(sources_dir)
        cls_dir = sources_dir / CLASSES_DIR
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
        return [x.name for x in glyphs]

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


def _read_features(features_path: Path) -> dict[str, GSFeature]:
    """Read all features in the directory.
    Also it will correctly load feature names.
    Nested features will be merged into the feature with root directory name.
    """
    feature_paths = _list_files(features_path)
    features = {}
    for path in feature_paths:
        if CLASSES_DIR in path.parts:
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


def _name_from_path(path: Path, features_path: Path) -> str:
    """Extracts the name from the feature path.
    For nested features, it will return root directory name.
    - `sources/opentype_features/calt.fea` -> `calt`
    - `sources/opentype_features/calt/colon.fea` -> `calt`
    """
    rel_path = path.relative_to(features_path)
    rel_name = rel_path.as_posix().removesuffix(FEATURE_EXT)
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


def _read_classes(dir_path: Path) -> list[GSClass]:
    """Read all classes in the directory"""
    classes = []
    for path in _list_files(dir_path):
        cls = _read_gs_file(path, GSClass)
        classes.append(cls)
    return classes


def _read_gs_file[T](path: Path, constructor: T) -> T:
    """Read a glyphsLib file"""
    target = Path(path)
    with target.open("r", encoding="utf-8") as file:
        name = target.stem
        return constructor(name, file.read())


def _list_files(dir_path: Path) -> list[Path]:
    """List matching files in the directory.
    Ignores files starting with a dot and with .disabled suffix.
    Recursively lists files in subdirectories.
    """
    files: list[Path] = []
    target = Path(dir_path)
    for file in target.iterdir():
        name = file.stem
        if file.suffix == ".disabled":
            print(f'WARN: "{name}" is ignored')
            continue
        if file.is_file() and not file.name.startswith("."):
            files.append(file)
        elif file.is_dir():
            files.extend(_list_files(file))
    return sorted(files, key=lambda item: item.as_posix())

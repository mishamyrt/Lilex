"""OpenType code loader"""
from __future__ import annotations

import os
from os import listdir
from os.path import basename, isdir, isfile, join, splitext
from typing import TypeVar

from glyphsLib import GSClass, GSFeature

FEATURES_DIR = "features"
CLASSES_DIR = f"{FEATURES_DIR}/_classes"
FEATURE_EXT = ".fea"
CLASS_EXT = ".cls"

T = TypeVar("T")

def list_files(dir_path: str, ext: str = None) -> list[str]:
    """List all files in the directory"""
    files = []
    for file in listdir(dir_path):
        name = splitext(file)[0]
        if splitext(file)[0].endswith(".disabled"):
            print(f'WARN: "{splitext(name)[0]}" is ignored')
            continue
        file_path = join(dir_path, file)
        if isfile(file_path) and not file.startswith('.'):
            files.append(file_path)
        elif isdir(file_path):
            files.extend(list_files(file_path))
    if ext is not None:
        files = filter(lambda x: x.endswith(ext) == ext, files)
    return sorted(files)

def _read_classes(dir_path: str) -> list[GSClass]:
    classes = []
    for path in list_files(dir_path):
        cls = _read_gs_file(path, GSClass)
        classes.append(cls)
    return classes

def _read_gs_file(path: str, constructor: T) -> T:
    name = basename(path).split('.')[0]
    with open(path, mode="r", encoding="utf-8") as file:
        return constructor(name, file.read())

def _read_features(features_path: str) -> dict[str, GSFeature]:
    feature_paths = list_files(features_path)
    features = {}
    for path in feature_paths:
        if CLASSES_DIR in path:
            continue
        name = path.removeprefix(features_path + "/").removesuffix(FEATURE_EXT)
        features[name] = _read_gs_file(path, GSFeature)
    return features

class OpenTypeFeatures:
    """Utility class for loading OpenType code files. Can filter features fo sub-font."""

    _path: str
    _features: dict[str, GSFeature]
    _classes: list[GSClass]

    def __init__(self, sources_dir: str):
        fea_dir = os.path.join(sources_dir, FEATURES_DIR)
        cls_dir = os.path.join(sources_dir, CLASSES_DIR)
        self._path = sources_dir
        self._features = _read_features(fea_dir)
        self._classes = _read_classes(cls_dir)

    def items(
        self,
        ignore_features: list[str] = None,
        data: dict[str, str] = None
    ) -> tuple[list[GSFeature], list[GSClass]]:
        """Returns a lists of features and classes"""
        feat_map: dict[str, str] = {}
        for name, feature in self._features.items():
            if name in ignore_features:
                continue
            fea_name = name
            if "/" in name:
                fea_name = name.split("/")[0]
            if fea_name not in feat_map:
                if data is not None and fea_name in data:
                    feat_map[fea_name] = data[fea_name]
                else:
                    feat_map[fea_name] = feature.code
            else:
                feat_map[fea_name] += "\n" + feature.code
        feats = []
        for name, code in feat_map.items():
            feats.append(GSFeature(name, code))
        return feats, self._classes

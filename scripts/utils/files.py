"""File utilities"""
from __future__ import annotations

from os import listdir
from os.path import basename, isfile, join
from re import search
from typing import List, TypeVar

from glyphsLib import GSClass, GSFeature

T = TypeVar("T")

def list_files(dir_path: str) -> List[str]:
    files = []
    for file in listdir(dir_path):
        file_path = join(dir_path, file)
        if isfile(file_path) and not file.startswith('.'):
            files.append(file_path)
    return files

def read_classes(dir_path: str) -> List[GSClass]:
    classes = []
    for path in list_files(dir_path):
        cls = _read_gs_file(path, GSClass)
        classes.append(cls)
    return classes

def _extract_name(content: str) -> str | None:
    result = search(r'Name:(.*)', content)
    try:
        return result.group(1).strip()
    except AttributeError:
        return None

def read_features(dir_path: str) -> List[GSFeature]:
    features = []
    for path in list_files(dir_path):
        fea = _read_gs_file(path, GSFeature)
        name = _extract_name(fea.code)
        if name is not None:
            fea.notes = f"Name: {name}"
        features.append(fea)
    return features

def _read_gs_file(path: str, constructor: T) -> T:
    name = basename(path).split('.')[0]
    with open(path, mode="r", encoding="utf-8") as file:
        return constructor(name, file.read())

def read_files(dir_path: str) -> str:
    """Reads all files in the directory and returns a summing string"""
    result = ""
    for path in list_files(dir_path):
        with open(path, mode="r", encoding="utf-8") as file:
            result += file.read() + "\n"
    return result

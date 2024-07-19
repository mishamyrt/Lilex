"""File utilities"""
from __future__ import annotations

from os import listdir
from os.path import basename, isfile, join, splitext
from typing import TypeVar

from glyphsLib import GSClass, GSFeature

T = TypeVar("T")

def list_files(dir_path: str) -> list[str]:
    files = []
    for file in listdir(dir_path):
        name = splitext(file)[0]
        if splitext(file)[0].endswith(".disabled"):
            print(f'WARN: "{splitext(name)[0]}" is ignored')
            continue
        file_path = join(dir_path, file)
        if isfile(file_path) and not file.startswith('.'):
            files.append(file_path)
    return sorted(files)

def read_classes(dir_path: str) -> list[GSClass]:
    classes = []
    for path in list_files(dir_path):
        cls = _read_gs_file(path, GSClass)
        classes.append(cls)
    return classes

def read_features(dir_path: str) -> list[GSFeature]:
    features = []
    for path in list_files(dir_path):
        fea = _read_gs_file(path, GSFeature)
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

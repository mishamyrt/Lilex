"""Lilex font config module"""
import os
from typing import Optional, TypedDict

import yaml

FontConfig = TypedDict(
    "FontConfig",
    {
        "source": Optional[str],
        "patch": Optional[str],
        "target": Optional[str],
    },
)

FontsList = dict[str, list[FontConfig]]

RawConfig = TypedDict(
    "RawConfig",
    {
        "features": str,
        "fonts": FontsList,
    },
)

class FamilyConfig:
    """Font family config"""
    _path: str
    _dir: str
    _raw: RawConfig

    def __init__(self, path: str):
        with open(path, mode="r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        if "features" not in raw:
            raise ValueError("features directory is required")
        if "fonts" not in raw:
            raise ValueError("fonts is required")
        self._raw = raw
        self._path = path
        self._dir = os.path.dirname(path)

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def features_dir(self) -> str:
        return os.path.join(self._dir, self._raw.get("features"))

    @property
    def fonts(self) -> FontsList:
        return self._raw.get("fonts")


__all__ = ["FamilyConfig", "FontsList", "FontConfig"]

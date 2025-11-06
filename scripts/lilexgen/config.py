"""Lilex font config module"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import yaml


class RawLilexGenConfig(TypedDict):
    """Raw Lilex font config"""

    featuresDir: str
    gftoolsConfig: str


class FontDescriptor:
    """Loadable font descriptor."""

    _name: str

    def __init__(
        self,
        name: str,
    ):
        self._name = name

    @property
    def name(self) -> str:
        """Font name"""
        return self._name


class LilexGenConfig:
    """Font family config"""

    _path: Path
    _dir: Path
    _raw: RawLilexGenConfig

    _fonts: list[FontDescriptor]
    _font_map: dict[str, FontDescriptor]

    def __init__(self, path: str | Path):
        path = Path(path)
        with path.open(encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        if "featuresDir" not in raw:
            raise ValueError("featuresDir is required")
        if "gftoolsConfig" not in raw:
            raise ValueError("gftoolsConfig is required")

        self._dir = path.parent

        gftools_config_path = self._dir / raw.get("gftoolsConfig")
        if not gftools_config_path.exists():
            raise ValueError(f"GFTools config file {gftools_config_path} does not exist")
        with gftools_config_path.open(encoding="utf-8") as file:
            gftools_config = yaml.safe_load(file)

        self._raw = raw
        self._path = path

        self._font_map = {}
        for source in gftools_config["sources"]:
            if source in self._font_map:
                raise ValueError(f"Font {source} already exists")
            descriptor = FontDescriptor(source)
            self._font_map[descriptor.name] = descriptor
        self._fonts = list(self._font_map.values())

    @property
    def dir(self) -> Path:
        """Font family directory"""
        return self._dir

    @property
    def features_dir(self) -> Path:
        """Features directory"""
        return self._dir / self._raw.get("featuresDir")

    @property
    def fonts(self) -> list[FontDescriptor]:
        """Font descriptors"""
        return self._fonts

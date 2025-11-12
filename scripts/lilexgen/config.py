"""Lilex font config module"""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import TypedDict

import yaml


class PatchParams(TypedDict):
    """Patch font params"""

    # Basic source font name
    source: str
    # Patch file name
    patch: str


FontSourceParams = PatchParams | None


class RawLilexGenConfig(TypedDict):
    """Raw Lilex font config"""

    featuresDir: str
    # font_name -> output_source_name -> PatchDescriptor | None
    sources: dict[str, dict[str, FontSourceParams]]


class SourceType(Enum):
    """Font source type"""

    SOURCE = "source"
    PATCH = "patch"


class FontDescriptor:
    """Font source descriptor"""

    path: Path
    type: SourceType
    params: FontSourceParams

    def __init__(self, path: Path, source_type: SourceType, params: FontSourceParams):
        self.path = path
        self.type = source_type
        self.params = params

    @property
    def dir(self) -> Path:
        """Directory"""
        return self.path.parent


class LilexGeneratorConfig:
    """Font family config"""

    _path: Path
    _dir: Path
    _raw: RawLilexGenConfig
    _descriptors: dict[str, FontDescriptor]

    def __init__(self, raw_config: RawLilexGenConfig, root_dir: Path):
        """Initializes Lilex generator config"""
        self._raw = raw_config
        self._dir = root_dir
        self._descriptors = {}

        for font, sources in self._raw["sources"].items():
            for file_name, params in sources.items():
                if params is None:
                    source_type = SourceType.SOURCE
                elif "source" in params and "patch" in params:
                    source_type = SourceType.PATCH
                else:
                    raise ValueError(f"Invalid source params: {params}")

                source_path = self._dir / font / file_name
                self._descriptors[file_name] = FontDescriptor(source_path, source_type, params)

    @staticmethod
    def from_file(path: str | Path) -> LilexGeneratorConfig:
        """Loads a config from a file"""
        if isinstance(path, str):
            path = Path(path)
        with path.open(encoding="utf-8") as file:
            raw_config = yaml.safe_load(file)
        return LilexGeneratorConfig(raw_config, path.parent)

    @property
    def dir(self) -> Path:
        """Font family directory"""
        return self._dir

    @property
    def features_dir(self) -> Path:
        """Features directory"""
        return self._dir / self._raw.get("featuresDir")

    @property
    def descriptors(self) -> list[FontDescriptor]:
        """Source descriptors"""
        return list(self._descriptors.values())

    def get_descriptor(self, path: Path) -> FontDescriptor:
        """Gets a source descriptor by path"""
        return self._descriptors[path]

"""Lilex font config module"""

import os
from enum import Enum
from typing import Optional, TypedDict

import yaml


class FontConfig(TypedDict):
    source: Optional[str]
    patch: Optional[str]
    target: Optional[str]


FontsList = dict[str, list[FontConfig]]


class RawConfig(TypedDict):
    features: str
    fonts: FontsList


class FontDescriptorKind(Enum):
    """The kind of node in the dependency tree."""

    SOURCE = "source"
    PATCH = "patch"


class FontDescriptor:
    """Loadable font descriptor."""

    _name: str
    _group_name: str

    _config: FontConfig
    _kind: FontDescriptorKind

    def __init__(
        self,
        group_name: str,
        config: FontConfig,
    ):
        self._group_name = group_name
        self._config = config

        source = config.get("source")
        patch = config.get("patch")
        target = config.get("target")

        if source:
            if patch or target:
                raise ValueError("source must not specify a patch or target")
            self._kind = FontDescriptorKind.SOURCE
            self._name = os.path.basename(source)
        elif patch:
            if source:
                raise ValueError("patch must not specify a source")
            if not target:
                raise ValueError("patch must specify a target")
            self._kind = FontDescriptorKind.PATCH
            self._name = os.path.basename(patch)
        else:
            raise ValueError("source or patch must be specified")

    @property
    def name(self) -> str:
        return self._name

    @property
    def kind(self) -> FontDescriptorKind:
        return self._kind

    @property
    def group(self) -> str:
        return self._group_name

    @property
    def config(self) -> FontConfig:
        return self._config

    def __repr__(self):
        message = f"{self.name}<({self.kind}>"
        return message


FontGroup = tuple[str, list[FontDescriptor]]


class FamilyConfig:
    """Font family config"""

    _path: str
    _dir: str
    _raw: RawConfig

    _fonts: list[FontGroup]
    _font_map: dict[str, FontDescriptor]

    def __init__(self, path: str):
        with open(path, mode="r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        raw = self._assert_config(raw)

        self._raw = raw
        self._path = path
        self._dir = os.path.dirname(path)

        self._font_map = {}
        groups: dict[str, list[FontDescriptor]] = {}

        for group_name, font_configs in raw.get("fonts").items():
            group_descriptors = []
            for font_config in font_configs:
                descriptor = FontDescriptor(group_name, font_config)
                group_descriptors.append(descriptor)
                if descriptor.name in self._font_map:
                    raise ValueError(f"Font {descriptor.name} already exists")
                self._font_map[descriptor.name] = descriptor
            groups[group_name] = group_descriptors

        self._fonts = list(groups.items())

        features_dir = os.path.join(self._dir, self._raw.get("features"))
        if not os.path.exists(features_dir):
            raise ValueError(f"Features directory {features_dir} does not exist")
        self._features_dir = features_dir

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def features_dir(self) -> str:
        return os.path.join(self._dir, self._raw.get("features"))

    @property
    def fonts(self) -> list[FontGroup]:
        return self._fonts

    @property
    def font_map(self) -> dict[str, FontDescriptor]:
        return self._font_map

    def _assert_config(self, raw: dict) -> RawConfig:
        if "features" not in raw:
            raise ValueError("features directory is required")
        if "fonts" not in raw:
            raise ValueError("fonts is required")
        return raw

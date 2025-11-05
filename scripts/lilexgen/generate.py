"""Font loader"""

import os

from glyphsLib import GSFont

from .config import FontDescriptor, LilexGenConfig
from .opentype_features import OpenTypeFeatures


def set_version(font: GSFont, version: str):
    parts = version.split(".")
    assert len(parts) == 2
    font.versionMajor = int(parts[0])
    font.versionMinor = int(parts[1])

def regenerate_sources(
    config: LilexGenConfig,
    forced_features: list[str] = None,
    version: str = None,
):
    """Regenerates the sources for a font family"""
    loader = FontLoader(config, forced_features)
    for descriptor in config.fonts:
        font = loader.load(descriptor)
        output_path = os.path.join(config.dir, descriptor.name)
        if version:
            set_version(font, version)
        font.save(output_path)


class FontLoader:
    _cache: dict[str, GSFont]
    _dir: str
    _features: OpenTypeFeatures

    def __init__(
        self,
        config: LilexGenConfig,
        forced_features: list[str] = None,
    ):
        """Loads fonts from a config"""
        self._cache = {}
        self._dir = config.dir
        self._features = OpenTypeFeatures(config.features_dir, forced_features)

    def load(self, descriptor: FontDescriptor) -> GSFont:
        if descriptor.name in self._cache.values():
            return self._cache[descriptor.name]

        source_path = os.path.join(self._dir, descriptor.name)
        font = GSFont(source_path)
        self._features.inject(font)
        self._cache[descriptor.name] = font
        return font

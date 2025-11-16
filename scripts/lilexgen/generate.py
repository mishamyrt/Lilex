"""Font loader"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from glyphsLib import GSFont

from .config import FontDescriptor, LilexGeneratorConfig, SourceType
from .opentype_features import OpenTypeFeatures


def generate_sources(
    config: LilexGeneratorConfig,
    forced_features: list[str] = None,
    version: str = None,
):
    """Regenerates the sources for a font family"""
    loader = FontLoader(config, forced_features)
    version_major = None
    version_minor = None
    if version:
        (version_major, version_minor) = _parse_version(version)
    for descriptor in config.descriptors:
        font = loader.load(descriptor)
        if version and descriptor.type != SourceType.PATCH_SOURCE:
            font.versionMajor = version_major
            font.versionMinor = version_minor
        font.save(descriptor.path.as_posix())


class FontLoader:
    """Font loader"""

    _cache: dict[Path, GSFont]
    _config: LilexGeneratorConfig
    _features: OpenTypeFeatures

    def __init__(
        self,
        config: LilexGeneratorConfig,
        forced_features: list[str] = None,
    ):
        """Loads fonts from a config"""
        self._cache = {}
        self._features = OpenTypeFeatures(config.features_dir, forced_features)
        self._config = config

    def load(self, descriptor: FontDescriptor) -> GSFont:
        """Loads a font from a descriptor"""
        if descriptor.path in self._cache:
            return self._cache[descriptor.path]

        if descriptor.type == SourceType.SOURCE:
            font = GSFont(descriptor.path.as_posix())
            self._features.inject(font)
        elif descriptor.type == SourceType.PATCH_SOURCE:
            font = GSFont(descriptor.path.as_posix())
        elif descriptor.type == SourceType.PATCH_TARGET:
            source_descriptor = self._config.get_descriptor(descriptor.params["source"])
            source_font = self.load(source_descriptor)
            patch_descriptor = self._config.get_descriptor(descriptor.params["patch"])
            patch_font = GSFont(patch_descriptor.path.as_posix())
            font = _merge_fonts(source_font, patch_font)
        else:
            raise ValueError(f"Invalid source type: {descriptor.type}")

        self._cache[descriptor.path] = font
        return font


def _merge_fonts(base: GSFont, patch: GSFont) -> GSFont:
    """Merges two fonts"""
    font = deepcopy(base)
    font.familyName = patch.familyName
    # Merge glyphs
    for glyph in patch.glyphs:
        if not glyph.export:
            continue
        glyph_idx = _find_glyph_index(font, glyph.name)
        if glyph_idx == -1:
            font.glyphs.append(glyph)
        else:
            font.glyphs[glyph_idx] = glyph
    # Merge custom parameters
    for param in patch.customParameters:
        if param.name in font.customParameters:
            font.customParameters[param.name] = param.value
        else:
            font.customParameters.append(param)
    return font


def _find_glyph_index(font: GSFont, glyph_name: str) -> int:
    """Finds the index of a glyph in a font"""
    for idx, glyph in enumerate(font.glyphs):
        if glyph.name == glyph_name:
            return idx
    return -1


GSFontVersion = tuple[int, int]


def _parse_version(version: str) -> GSFontVersion:
    """Parses a version string into a tuple of major and minor version numbers.
    Example:
    "2.700" -> (2, 700)
    "2.700-beta" -> (2, 700)
    """
    if "-" in version:
        print(
            f"Warning: Version {version} contains a hyphen, using only the first part"
        )
        version = version.split("-")[0]
    parts = version.split(".")
    assert len(parts) == 2
    return (int(parts[0]), int(parts[1]))

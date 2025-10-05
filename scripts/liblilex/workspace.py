"""Workspace loader"""
import os
from enum import Enum
from typing import Optional

from glyphsLib import GSFont

from .config import FamilyConfig, FontConfig, FontsList
from .features import (
    OpenTypeFeatures,
    force_features,
    generate_spacers,
    render_ligatures,
)
from .glyphs_font import GlyphsFont


class FontDescriptorKind(Enum):
    """The kind of node in the dependency tree."""

    SOURCE = "source"
    PATCH = "patch"


class FontDescriptor:
    """Loadable font descriptor. A node in the dependency tree."""

    name: str
    font_name: str
    config: FontConfig
    children: list["FontDescriptor"]
    path: str
    kind: FontDescriptorKind

    def __init__(
        self,
        path: str,
        font_name: str,
        config: FontConfig,
        kind: FontDescriptorKind,
    ):
        self.name = os.path.basename(path)
        self.font_name = font_name
        self.config = config
        self.children = []
        self.path = path
        self.kind = kind

    def __repr__(self):
        message = f"{self.name} ({self.kind})"
        if self.children:
            message += f" -> {', '.join([repr(child) for child in self.children])}"
        return message


FontGroup = tuple[str, list[FontDescriptor]]


class Workspace:
    """A font family"""

    _config: FamilyConfig
    _fonts: list[FontGroup]
    _font_map: dict[str, FontDescriptor]

    _features: OpenTypeFeatures
    _forced_features: Optional[list[str]]

    _font_cache: dict[str, GlyphsFont]

    def __init__(
        self, config: FamilyConfig, forced_features: Optional[list[str]] = None
    ):
        self._config = config
        self._features = OpenTypeFeatures(config.features_dir)
        self._forced_features = forced_features
        self._font_map = _build_dependency_graph(config.fonts, config.dir)

        font_groups = {}
        for descriptor in self._font_map.values():
            if descriptor.font_name not in font_groups:
                font_groups[descriptor.font_name] = []
            font_groups[descriptor.font_name].append(descriptor)
        self._fonts = list(font_groups.items())
        self._font_cache = {}

    def gs_fonts(self) -> list[list[GSFont]]:
        family_fonts = []
        for _, descriptors in self._fonts:
            fonts = []
            for descriptor in descriptors:
                font = self._load(descriptor.name)
                fonts.append(font.file)
            family_fonts.append(fonts)
        return family_fonts

    def sources(self) -> list[tuple[FontDescriptorKind, GlyphsFont]]:
        sources = []
        for _, descriptors in self._fonts:
            for descriptor in descriptors:
                font = GlyphsFont(descriptor.path)
                sources.append((descriptor.kind, font))
        return sources

    def _load(self, name: str) -> GlyphsFont:
        descriptor = self._font_map[name]
        if descriptor.name in self._font_cache:
            return self._font_cache[descriptor.name]
        if descriptor.kind == FontDescriptorKind.SOURCE:
            font = GlyphsFont(descriptor.path)
        elif descriptor.kind == FontDescriptorKind.PATCH:
            patch_font = GlyphsFont(descriptor.path)
            target_font = self._load(descriptor.config.get("target"))
            font = target_font.patched(patch_font)
        else:
            raise ValueError(f"Unknown node kind: {descriptor.kind}")
        _render_features(font, self._features, self._forced_features)
        self._font_cache[descriptor.name] = font
        return font


def _render_features(
    font: GlyphsFont,
    features: OpenTypeFeatures,
    forced: Optional[list[str]] = None,
) -> None:
    """Renders features and spacers"""
    ligatures = [glyph.name for glyph in font.ligatures()]
    feats, cls = features.items(
        data={
            "calt": render_ligatures(ligatures),
        }
    )
    if forced is not None:
        force_features(feats, forced)
    generate_spacers(ligatures, font.file.glyphs)
    font.set_classes(cls)
    font.set_features(feats)
    font.set_fea_names()

def _normalize_path(base_dir: str, relative_path: str) -> str:
    """Returns an absolute, normalized path for a config-provided path."""
    return os.path.normpath(os.path.join(base_dir, relative_path))


def _index_nodes(fonts: FontsList, base_dir: str) -> dict[str, FontDescriptor]:
    """Creates a unique node for every source and patch entry.

    Keyed by absolute normalized file path for stability and cross-family lookups.
    """
    nodes_by_name: dict[str, FontDescriptor] = {}

    for font_name, entries in fonts.items():
        for entry in entries:
            source = entry.get("source")
            patch = entry.get("patch")
            if source:
                if entry.get("patch") or entry.get("target"):
                    raise ValueError(
                        f"Source '{source}' must not specify a 'patch' or 'target'"
                    )
                rel_path = source
                kind = FontDescriptorKind.SOURCE
            elif patch:
                if entry.get("source"):
                    raise ValueError(f"Patch '{patch}' must not specify a 'source'")
                if not entry.get("target"):
                    raise ValueError(f"Patch '{patch}' must specify a 'target'")
                rel_path = patch
                kind = FontDescriptorKind.PATCH
            else:
                raise ValueError(f"Source or patch must be specified for {font_name}")

            abs_path = _normalize_path(base_dir, rel_path)
            name = os.path.basename(abs_path)
            if name not in nodes_by_name:
                node = FontDescriptor(abs_path, font_name, entry, kind)
                nodes_by_name[name] = node

    return nodes_by_name


def _link_dependencies(
    fonts: FontsList, base_dir: str, nodes_by_name: dict[str, FontDescriptor]
) -> None:
    """Connects parent->child edges: target (parent) -> patch (child).

    Supports patch-on-patch by resolving targets to either source or patch nodes.
    """
    for entries in fonts.values():
        for entry in entries:
            if not entry.get("patch"):
                continue
            patch_name = os.path.basename(entry["patch"])
            target_rel = entry.get("target")
            if not target_rel:
                raise ValueError(f"Patch '{entry['patch']}' must specify a 'target'")
            target_abs = _normalize_path(base_dir, target_rel)  # parent
            target_name = os.path.basename(target_abs)

            if target_name not in nodes_by_name:
                raise KeyError(
                    f"Target '{target_name}' for patch '{entry['patch']}' is not present in config"
                )

            parent = nodes_by_name[target_name]
            child = nodes_by_name[patch_name]

            # Avoid duplicate links
            if child not in parent.children:
                parent.children.append(child)


def _build_dependency_graph(
    fonts: FontsList, base_dir: str
) -> dict[str, FontDescriptor]:
    """Parses config and builds a dependency graph for all nodes.

    Returns the loaded config and a mapping of absolute path -> node.
    """
    nodes_by_path = _index_nodes(fonts, base_dir)
    _link_dependencies(fonts, base_dir, nodes_by_path)
    return nodes_by_path

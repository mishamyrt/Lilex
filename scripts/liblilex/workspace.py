"""Workspace loader"""
import os
from collections import deque
from copy import deepcopy
from enum import Enum
from typing import Optional

from .config import FamilyConfig, FontConfig, FontsList
from .features import (
    OpenTypeFeatures,
    force_features,
    generate_spacers,
    render_ligatures,
)
from .glyphs_font import GlyphsFont

# Workspace is a representation of a font family with its source fonts and patches
Workspace = dict[str, list[GlyphsFont]]


def load_workspace(
    config: FamilyConfig, forced_features: Optional[list[str]] = None
) -> Workspace:
    """
    Loads a workspace from a family config and prepares dependency order.
    Reads source fonts, renders patches and insert features.
    """
    fonts = config.fonts
    nodes_by_name = _build_dependency_graph(fonts, config.dir)
    ordered_nodes = _dependency_load_order(nodes_by_name)

    workspace_index: Workspace = {}
    workspace: Workspace = {}
    features = OpenTypeFeatures(config.features_dir)
    for node in ordered_nodes:
        if not workspace.get(node.font_name):
            workspace[node.font_name] = []

        if node.kind == LoadNodeKind.SOURCE:
            font = GlyphsFont(node.path)
        elif node.kind == LoadNodeKind.PATCH:
            target_name = node.config.get("target")
            target_font = workspace_index.get(target_name)
            if not target_font:
                raise ValueError(f"Target font {target_name} not found")

            patch_font = GlyphsFont(node.path)
            font = _apply_patch(target_font, patch_font)
        else:
            raise ValueError(f"Unknown node kind: {node.kind}")

        _render_features(font, features, forced_features)

        workspace_index[node.name] = font
        workspace[node.font_name].append(font)

    return workspace


def _render_features(
    font: GlyphsFont,
    features: OpenTypeFeatures,
    forced: Optional[list[str]] = None,
) -> None:
    """Renders features and spacers"""
    ligatures = font.ligatures()
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


def _find_glyph_index(font: GlyphsFont, glyph_name: str) -> int:
    """Finds the index of a glyph in a font"""
    for idx, glyph in enumerate(font.file.glyphs):
        if glyph.name == glyph_name:
            return idx
    return -1


def _apply_patch(base_font: GlyphsFont, patch_font: GlyphsFont):
    """Returns a new font with the patch applied"""
    font = deepcopy(base_font)
    font.is_ephemeral = True
    for glyph in patch_font.glyphs():
        glyph_idx = _find_glyph_index(font, glyph.name)
        if glyph_idx == -1:
            font.file.glyphs.append(glyph)
        else:
            font.file.glyphs[glyph_idx] = glyph
    for param in patch_font.file.customParameters:
        if param.name in font.file.customParameters:
            font.file.customParameters[param.name] = param.value
        else:
            font.file.customParameters.append(param)
    font.file.familyName = patch_font.file.familyName

    return font


class LoadNodeKind(Enum):
    """The kind of node in the dependency tree."""

    SOURCE = "source"
    PATCH = "patch"


class LoadNode:
    """A node in the dependency tree.

    Attributes
    -----------
    name: Human-friendly name (usually a file basename)
    font_name: Font name from config
    config: Original config entry used to define this node
    children: Nodes that depend on this node (fan-out supported)
    path: Absolute path to the file on disk
    kind: Either "source" or "patch"
    """

    name: str
    font_name: str
    config: FontConfig
    children: list["LoadNode"]
    path: str
    kind: LoadNodeKind

    def __init__(
        self,
        name: str,
        config: FontConfig,
        font_name: str,
        path: str,
        kind: LoadNodeKind,
    ):
        self.name = name
        self.font_name = font_name
        self.config = config
        self.children = []
        self.path = path
        self.kind = kind


def _normalize_path(base_dir: str, relative_path: str) -> str:
    """Returns an absolute, normalized path for a config-provided path."""
    return os.path.normpath(os.path.join(base_dir, relative_path))


def _index_nodes(fonts: FontsList, base_dir: str) -> dict[str, LoadNode]:
    """Creates a unique node for every source and patch entry.

    Keyed by absolute normalized file path for stability and cross-family lookups.
    """
    nodes_by_name: dict[str, LoadNode] = {}

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
                kind = LoadNodeKind.SOURCE
            elif patch:
                if entry.get("source"):
                    raise ValueError(f"Patch '{patch}' must not specify a 'source'")
                if not entry.get("target"):
                    raise ValueError(f"Patch '{patch}' must specify a 'target'")
                rel_path = patch
                kind = LoadNodeKind.PATCH
            else:
                raise ValueError(f"Source or patch must be specified for {font_name}")

            abs_path = _normalize_path(base_dir, rel_path)
            name = os.path.basename(rel_path)
            if name not in nodes_by_name:
                node = LoadNode(
                    name,
                    entry,
                    font_name,
                    abs_path,
                    kind,
                )
                nodes_by_name[name] = node

    return nodes_by_name


def _link_dependencies(
    fonts: FontsList, base_dir: str, nodes_by_name: dict[str, LoadNode]
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


def _build_dependency_graph(fonts: FontsList, base_dir: str) -> dict[str, LoadNode]:
    """Parses config and builds a dependency graph for all nodes.

    Returns the loaded config and a mapping of absolute path -> node.
    """
    nodes_by_path = _index_nodes(fonts, base_dir)
    _link_dependencies(fonts, base_dir, nodes_by_path)
    return nodes_by_path


def _dependency_load_order(nodes_by_path: dict[str, LoadNode]) -> list[LoadNode]:
    """Returns nodes in topological order so that dependencies are loaded first.

    Uses Kahn's algorithm. Cycles are not expected; if encountered, an error is raised.
    """
    in_degree: dict[LoadNode, int] = {}
    for node in nodes_by_path.values():
        in_degree[node] = 0
    for node in nodes_by_path.values():
        for child in node.children:
            in_degree[child] = in_degree.get(child, 0) + 1

    queue: deque[LoadNode] = deque([n for n, deg in in_degree.items() if deg == 0])
    ordered: list[LoadNode] = []

    while queue:
        node = queue.popleft()
        ordered.append(node)
        for child in node.children:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    if len(ordered) != len(nodes_by_path):
        raise RuntimeError("Dependency graph has cycles or unresolved nodes")

    return ordered

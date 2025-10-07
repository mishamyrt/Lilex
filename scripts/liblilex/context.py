import hashlib
import json
import os
from dataclasses import dataclass, field
from io import StringIO
from typing import Any, Optional, TypedDict

from glyphsLib import GSFont
from glyphsLib.writer import Writer

from .external_tools import FontFormat
from .progress import BuildProgressTracker, TrackerTaskKey


class CacheManifest(TypedDict):
    """Manifest for cache entry"""

    hash: str
    size: int
    pipelines: dict[str, list[str]]


class FontCache:
    """Cache entry. Manages font file and its build artifacts."""

    _name: str
    _font: GSFont
    _dir: str
    _artifacts_dir: str
    _manifest: CacheManifest

    def __init__(self, name: str, font: GSFont, cache_root: str):
        self._name = name
        self._font = font
        self._dir = os.path.join(cache_root, name)
        self._artifacts_dir = os.path.join(self._dir, "artifacts")

        content = _dump_font(font)
        content_hash = hashlib.sha256(content).hexdigest()
        size = len(content)

        manifest_path = self.manifest_path
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = json.load(file)
            if manifest["hash"] == content_hash and manifest["size"] == size:
                return
            else:
                os.rmdir(self._dir)

        os.makedirs(self._dir, exist_ok=True)
        os.makedirs(self._artifacts_dir, exist_ok=True)
        with open(self.source_path, "wb") as file:
            file.write(content)
        with open(manifest_path, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "hash": content_hash,
                    "size": size,
                    "pipelines": {},
                },
                file,
            )

    @property
    def name(self) -> str:
        return self._name

    @property
    def font(self) -> GSFont:
        return self._font

    @property
    def source_path(self) -> str:
        return os.path.join(self._dir, f"{self._name}.glyphs")

    @property
    def manifest_path(self) -> str:
        return os.path.join(self._dir, "manifest.json")

    @property
    def manifest(self) -> CacheManifest:
        return self._manifest

    @property
    def steps(self, pipeline: str) -> list[str]:
        return self._manifest["pipelines"][pipeline]

    def add_step(self, pipeline: str, step: str):
        if pipeline not in self._manifest["pipelines"]:
            self._manifest["pipelines"][pipeline] = []
        self._manifest["pipelines"][pipeline].append(step)
        self._dump_manifest()

    def artifact_dir(self, key: str) -> str:
        return os.path.join(self._artifacts_dir, key)

    def list_artifact(self, key: str) -> list[str]:
        artifact_path = self.artifact_dir(key)
        if not os.path.exists(artifact_path):
            return []
        files = os.listdir(artifact_path)
        return [os.path.join(artifact_path, file) for file in files]

    def is_artifact_exists(self, key: str) -> bool:
        return os.path.exists(self.artifact_dir(key))

    def _dump_manifest(self):
        with open(self.manifest_path, "w", encoding="utf-8") as file:
            json.dump(self._manifest, file)


class BuilderCache:
    """Builder cache"""

    _dir: str
    _version: int

    def __init__(self, cache_dir: str):
        self._version = 1
        self._dir = cache_dir

        cache_ver = self._path("cache.ver")

        def create_cache_dir(version: int):
            """Initialize the cache directory"""
            os.makedirs(cache_dir)
            gitignore = os.path.join(cache_dir, ".gitignore")
            with open(gitignore, "w", encoding="utf-8") as file:
                file.write("*")
            with open(cache_ver, "w", encoding="utf-8") as file:
                file.write(str(version))

        if not os.path.exists(cache_dir):
            create_cache_dir(self._version)
        else:
            with open(cache_ver, "r", encoding="utf-8") as file:
                version = file.read()
                if int(version) != self._version:
                    os.rmdir(self._dir)
                    create_cache_dir(self._version)

    def get_manifest(self, key: str) -> CacheManifest:
        manifest_path = self._path(key, "manifest.json")
        if not os.path.exists(manifest_path):
            return None
        with open(manifest_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get(self, key: str, font: GSFont) -> FontCache:
        return FontCache(key, font, self._dir)

    def _path(self, *args: str) -> str:
        return os.path.join(self._dir, *args)


@dataclass(frozen=True)
class BuildContext:
    """Immutable context containing all build state"""

    format: FontFormat
    cache: FontCache
    artifacts: dict[str, Any] = field(default_factory=dict)
    progress_task_key: Optional[TrackerTaskKey] = None
    progress_tracker: Optional["BuildProgressTracker"] = None

    def with_artifacts(self, **kwargs) -> "BuildContext":
        """Create new context with additional artifacts"""
        new_artifacts = {**self.artifacts, **kwargs}
        return BuildContext(
            format=self.format,
            cache=self.cache,
            artifacts=new_artifacts,
            progress_task_key=self.progress_task_key,
            progress_tracker=self.progress_tracker,
        )

    def report_step(self, step_name: str):
        """Reports progress tracker about the current step (without increasing progress)"""
        if self.progress_tracker and self.progress_task_key is not None:
            self.progress_tracker.update_step(
                self.progress_task_key, step_name, advance=0
            )

    def report_complete(self):
        """Reports about the completion of the pipeline"""
        if self.progress_tracker and self.progress_task_key is not None:
            self.progress_tracker.mark_complete(self.progress_task_key)

    def report_failure(self, error: str):
        """Reports about the error"""
        if self.progress_tracker and self.progress_task_key is not None:
            self.progress_tracker.mark_failed(self.progress_task_key, error)


def _dump_font(font: GSFont) -> bytes:
    """Converts GSFont to a .glyphs file content"""
    buffer = StringIO()
    w = Writer(buffer, format_version=3)
    w.write(font)
    return buffer.getvalue().encode("utf-8")

"""Progress tracker for building fonts. rich based."""

from __future__ import annotations

from rich.console import Console
from rich.console import Group as RenderGroup
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text

console = Console()

FONT_NAME_MAX_LENGTH = 16
CLI_FPS = 10

# (group_name, font_name, fmt)
TrackerTaskKey = tuple[str, str, str]


class BuildProgressTracker:
    _live: Live | None
    # group_name -> progress instance
    _groups: dict[str, Progress]
    # (group_name, font_name, fmt) -> task_id
    _tasks: dict[TrackerTaskKey, TaskID]

    def __init__(self):
        self._live = None
        self._groups = {}
        self._tasks = {}

    def add_pipeline(
        self,
        group_name: str,
        font_name: str,
        fmt: str,
        total_steps: int,
    ) -> TrackerTaskKey:
        """Add new pipeline; tasks are grouped by 'group_name'"""
        key = (group_name, font_name, fmt)
        if key in self._tasks:
            return key

        # Validate font name length for fixed-width column
        if len(font_name) > FONT_NAME_MAX_LENGTH:
            raise ValueError(
                f"Font name too long for progress column "
                f"(max {FONT_NAME_MAX_LENGTH}): '{font_name}'"
            )

        progress = self._get_group_progress(group_name)
        task_id = progress.add_task(
            "",
            total=total_steps,
            font_name=font_name,
            format=fmt,
            current_step="starting...",
        )
        self._tasks[key] = task_id
        if self._live is not None:
            self._live.update(self._renderable())

        return key

    def update_step(self, task_key: TrackerTaskKey, step_name: str, advance: int = 1):
        (group_name, _, _) = task_key
        task_id = self._tasks[task_key]
        progress = self._get_group_progress(group_name)
        if progress is None or task_id is None:
            return
        progress.update(task_id, advance=advance, current_step=step_name)

    def mark_complete(self, task_key: TrackerTaskKey):
        (group_name, _, _) = task_key
        task_id = self._tasks[task_key]
        progress = self._get_group_progress(group_name)
        if progress is None:
            return
        progress.update(task_id, current_step="[green]✓ complete")

    def mark_failed(self, task_key: TrackerTaskKey, error: str):
        (group_name, _, _) = task_key
        task_id = self._tasks[task_key]
        progress = self._get_group_progress(group_name)
        if progress is None:
            return
        progress.update(task_id, current_step=f"[red]✗ failed: {error[:40]}")

    def __enter__(self):
        self._live = Live(
            self._renderable(),
            refresh_per_second=CLI_FPS,
            console=console,
            transient=True,
        )
        self._live.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._live is not None:
            self._live.__exit__(exc_type, exc, tb)
            self._live = None

    def _renderable(self):
        if not self._groups:
            return RenderGroup()

        return RenderGroup(
            Text("building fonts...\n"),
            *self._groups.values()
        )

    def _get_group_progress(self, group: str) -> Progress:
        return self._groups.get(group) or self._create_group_progress(group)

    def _create_group_progress(self, group_name: str) -> Progress:
        progress = Progress(
            SpinnerColumn("dots"),
            TextColumn("[cyan]{task.fields[font_name]:<16}"),
            TextColumn("[dim]{task.fields[format]}"),
            BarColumn(bar_width=FONT_NAME_MAX_LENGTH + 4),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("{task.fields[current_step]}"),
            TimeElapsedColumn(),
        )
        self._groups[group_name] = progress
        if self._live is not None:
            self._live.update(self._renderable())
        return progress


class LoadProgress:
    _live: Live | None
    _progress: Progress

    def __init__(self, fonts: list[str]):
        self._live = None
        self._progress = Progress(
            SpinnerColumn("dots"),
            TextColumn("[cyan]{task.fields[source_name]:<16}"),
        )

        for font in fonts:
            self.add_source(font)

    def add_source(self, source_name: str) -> str:
        """Add new source; sources are grouped by 'source_name'"""
        self._progress.add_task(
            "",
            total=None,
            source_name=source_name,
        )

    def __enter__(self):
        panel = RenderGroup(
            Text("loading sources...\n"),
            self._progress,
        )
        self._live = Live(
            panel, refresh_per_second=CLI_FPS, console=console, transient=True
        )
        self._live.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._live is not None:
            self._live.__exit__(exc_type, exc, tb)
            self._live = None

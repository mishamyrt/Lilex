"""Build fonts using the pipeline"""

import asyncio
import os
import re
import shutil

from glyphsLib import GSFont
from glyphsLib.builder.axes import find_base_style

from .config import FamilyConfig
from .context import BuildContext, BuilderCache
from .external_tools import FontFormat
from .loader import load_family
from .progress import (
    BuildProgressTracker,
    LoadProgress,
    TrackerTaskKey,
)
from .steps import (
    BuildStep,
    CompilationStep,
    CopyOutputStep,
    DesignSpaceStep,
    FixVersionStep,
    GenerateStatStep,
    GftoolsFixStep,
    StepResult,
    stat_from_instances,
)


async def build_family(
    config: FamilyConfig, formats: set[FontFormat], output_dir: str, cache_path: str
) -> list[list[BuildContext]]:
    """Build fonts using the pipeline"""

    sources = []
    for _, fonts in config.fonts:
        for font in fonts:
            sources.append(font.name)

    with LoadProgress(sources):
        cache = BuilderCache(cache_path)
        family = load_family(config)

    # Recreate output directory before building
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    tracker = BuildProgressTracker()

    # Pre-register all tasks so they appear simultaneously
    # We need total steps per pipeline to register; compute once
    def compute_steps(reference_font: GSFont) -> tuple[int, int]:
        target_version = float(
            f"{reference_font.versionMajor}.{reference_font.versionMinor}"
        )
        default_steps = [
            DesignSpaceStep(),
            CompilationStep(),
            FixVersionStep(target_version),
            GftoolsFixStep(),
            CopyOutputStep(output_dir),
        ]
        variable_steps = list(default_steps)
        if FontFormat.VARIABLE in formats:
            stat_config = stat_from_instances(reference_font.instances)
            stat_step = GenerateStatStep(stat_config, False)
            variable_steps.insert(-1, stat_step)
        return (len(default_steps), len(variable_steps))

    family_sources = []
    for group_name, fonts in family:
        if not fonts:
            continue
        default_len, variable_len = compute_steps(fonts[0])

        group_sources: list[tuple[str, GSFont, TrackerTaskKey]] = []
        for font in fonts:
            font_name = _font_name(font)
            font_task_keys: dict[FontFormat, TrackerTaskKey] = {}

            for fmt in formats:
                if fmt == FontFormat.VARIABLE:
                    total_steps = variable_len
                else:
                    total_steps = default_len
                task_key = tracker.add_pipeline(
                    group_name,
                    font_name,
                    fmt.value,
                    total_steps,
                )
                font_task_keys[fmt] = task_key
            group_sources.append((font_name, font, font_task_keys))
        family_sources.append(group_sources)

    with tracker:
        tasks = []
        for sources in family_sources:
            tasks.append(build_font(sources, formats, output_dir, cache, tracker))
        contexts = await asyncio.gather(*tasks)

    return contexts


async def build_font(
    sources: list[tuple[str, GSFont, dict[FontFormat, TrackerTaskKey]]],
    formats: set[FontFormat],
    output_dir: str,
    cache: BuilderCache,
    tracker: BuildProgressTracker,
) -> list[BuildContext]:
    """Build fonts using the pipeline"""
    (_, reference_font, _) = sources[0]
    target_version = float(
        f"{reference_font.versionMajor}.{reference_font.versionMinor}"
    )

    # Late init if variable format is requested
    variable_steps = []
    default_steps = [
        DesignSpaceStep(),
        CompilationStep(),
        FixVersionStep(target_version),
        GftoolsFixStep(),
        CopyOutputStep(output_dir),
    ]

    if FontFormat.VARIABLE in formats:
        variable_steps.extend(default_steps)
        stat_config = stat_from_instances(reference_font.instances)
        stat_step = GenerateStatStep(stat_config, False)
        variable_steps.insert(-1, stat_step)

    tasks = []
    for font_name, font, task_keys in sources:
        font_cache = cache.get(font_name, font)

        for fmt in formats:
            if fmt == FontFormat.VARIABLE:
                steps = variable_steps
            else:
                steps = default_steps

            # Create context with tracker
            context = BuildContext(
                fmt,
                font_cache,
                progress_task_key=task_keys[fmt],
                progress_tracker=tracker,
            )

            pipeline = BuildPipeline(steps)
            build_task = pipeline.execute(context)
            tasks.append(build_task)

    return await asyncio.gather(*tasks)


class BuildPipeline:
    """Orchestrates build steps"""

    _steps: list[BuildStep]

    def __init__(self, steps: list[BuildStep]):
        self._steps = steps

    async def execute(self, context: BuildContext) -> BuildContext:
        """Execute all steps in the pipeline"""
        results = []
        current_context = context
        # Pin tracker and task once per pipeline to avoid losing them on context replacements
        pinned_tracker = current_context.progress_tracker
        pinned_task_key = current_context.progress_task_key

        for step in self._steps:
            # Report step starting using pinned tracker to avoid context drift
            if pinned_tracker is not None and pinned_task_key is not None:
                pinned_tracker.update_step(pinned_task_key, step.name, advance=0)

            try:
                step_context, result = await step.execute(current_context)
                current_context = step_context.with_artifacts(**result.artifacts)
            except Exception as e:  # pylint: disable=broad-exception-caught
                result = StepResult(success=False, errors=[str(e)])
            results.append(result)

            if not result.success:
                # Report failure
                error_msg = result.message or (
                    result.errors[0] if result.errors else "Unknown error"
                )
                if pinned_tracker is not None and pinned_task_key is not None:
                    pinned_tracker.mark_failed(pinned_task_key, error_msg)
                break
            else:
                # Advance on success to avoid double-advancing
                if pinned_tracker is not None and pinned_task_key is not None:
                    pinned_tracker.update_step(pinned_task_key, step.name, advance=1)

        # Mark as complete if all steps succeeded
        if all(r.success for r in results):
            if pinned_tracker is not None and pinned_task_key is not None:
                pinned_tracker.mark_complete(pinned_task_key)

        return current_context


def _font_name(font: GSFont) -> str:
    """Returns the font name"""
    base_style = find_base_style(font.masters)
    words = re.split(r"[^a-zA-Z0-9]+", font.familyName.strip())
    base_name = "".join(w.capitalize() for w in words if w)
    if base_style is None or base_style == "":
        return base_name
    return f"{base_name}-{base_style}"

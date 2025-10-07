"""Builds UFO design space from Glyphs files"""

import os

from glyphsLib import build_masters

from ..context import BuildContext
from .base import BuildStep, StepResult


class DesignSpaceStep(BuildStep):
    """Builds UFO design space from Glyphs files"""

    def __init__(self):
        super().__init__("design_space")

    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Build design space files for each font"""
        artifact_key = "ufo"
        ufo_dir = context.cache.artifact_dir(artifact_key)
        ds_file = os.path.join(ufo_dir, f"{context.cache.name}.designspace")
        if context.cache.is_artifact_exists(artifact_key):
            return context, StepResult(
                success=True, artifacts={"design_space": ds_file}
            )

        os.makedirs(ufo_dir, exist_ok=True)
        build_masters(
            context.cache.source_path,
            ufo_dir,
            write_skipexportglyphs=True,
            designspace_path=ds_file,
        )

        new_context = context.with_artifacts(design_space=ds_file)
        return new_context, StepResult(
            success=True, artifacts={"design_space": ds_file}
        )

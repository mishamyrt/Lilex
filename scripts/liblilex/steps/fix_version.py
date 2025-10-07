"""Fixes version in font"""

import os

from fontTools.ttLib import TTFont

from ..context import BuildContext
from .base import BuildStep, StepResult


class FixVersionStep(BuildStep):
    """Fixes version in font.
    This step should be executed after the compilation step to fix
    floating point precision issues."""

    _version: str

    def __init__(self, version: str):
        super().__init__("fix_version")
        self._version = version

    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Fixes version in font"""
        if "compiled_fonts" not in context.artifacts:
            return context, StepResult(
                success=False, errors=["Compiled fonts not found"]
            )

        files = context.artifacts["compiled_fonts"]
        for file_path in files:
            font = TTFont(file_path)
            font["head"].fontRevision = self._version
            os.remove(file_path)
            font.save(file_path)
        return context, StepResult(success=True, artifacts={"compiled_fonts": files})

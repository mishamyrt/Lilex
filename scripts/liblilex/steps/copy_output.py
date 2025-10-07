"""Copies compiled fonts to the output directory"""

import os
import shutil

from ..context import BuildContext
from .base import BuildStep, StepResult


class CopyOutputStep(BuildStep):
    """Copies compiled fonts to the output directory"""

    _output_dir: str

    def __init__(self, output_dir: str):
        super().__init__("copy_output")
        self._output_dir = output_dir

    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Copies compiled fonts to the output directory"""
        artifact_key = context.format.value
        if not context.cache.is_artifact_exists(artifact_key):
            return context, StepResult(
                success=False, errors=["Compiled fonts not found"]
            )

        output_dir = os.path.join(self._output_dir, artifact_key)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        files = context.cache.list_artifact(artifact_key)
        output_files = []
        for file_path in files:
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_dir, file_name)
            shutil.copy(file_path, output_path)
            output_files.append(output_path)

        return context, StepResult(
            success=True, artifacts={"output_files": output_files}
        )

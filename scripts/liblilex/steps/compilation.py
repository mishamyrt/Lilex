"""Compiles font using fontmake"""

from ..context import BuildContext
from ..external_tools import fontmake
from .base import BuildStep, StepResult


class CompilationStep(BuildStep):
    """Compiles font using fontmake"""

    def __init__(self):
        super().__init__("compilation")

    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Compile and post-process fonts"""
        if "design_space" not in context.artifacts:
            return context, StepResult(success=False, errors=["Design space not found"])

        fmt = context.format.value
        if context.cache.is_artifact_exists(fmt):
            return context, StepResult(
                success=True,
                artifacts={"compiled_fonts": context.cache.list_artifact(fmt)},
            )

        design_space = context.artifacts["design_space"]
        out_dir = context.cache.artifact_dir(fmt)
        files = await fontmake(design_space, out_dir, context.format)
        return context, StepResult(success=True, artifacts={"compiled_fonts": files})

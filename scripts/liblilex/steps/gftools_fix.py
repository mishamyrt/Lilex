"""Applies gftools fix to font"""

from ..context import BuildContext
from ..external_tools import gftools_fix
from .base import BuildStep, StepResult


class GftoolsFixStep(BuildStep):
    """Applies gftools fix to font"""

    def __init__(self):
        super().__init__("gftools_fix")

    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Applies gftools fix to font"""
        if "compiled_fonts" not in context.artifacts:
            return context, StepResult(
                success=False, errors=["Compiled fonts not found"]
            )

        files = context.artifacts["compiled_fonts"]
        for file in files:
            await gftools_fix(file)
        return context, StepResult(success=True, artifacts={"compiled_fonts": files})

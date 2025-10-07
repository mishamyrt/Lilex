"""Applies gftools fix to font"""

from typing import TypedDict

from fontTools.ttLib import TTFont
from gftools.stat import gen_stat_tables_from_config
from glyphsLib import GSInstance

from ..context import BuildContext
from ..external_tools import FontFormat
from .base import BuildStep, StepResult


class StatValue(TypedDict):
    name: str
    value: float


class StatAxisConfig(TypedDict):
    tag: str
    name: str
    values: list[StatValue]


class GenerateStatStep(BuildStep):
    """Generates STAT table for variable font"""

    _config: list[StatAxisConfig]
    _has_italic: bool

    def __init__(self, config: list[StatAxisConfig], has_italic: bool):
        super().__init__("generate_stat")
        self._config = config
        self._has_italic = has_italic

    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Generates STAT table for font"""
        if "compiled_fonts" not in context.artifacts:
            return context, StepResult(
                success=False, errors=["Compiled fonts not found"]
            )
        if context.format != FontFormat.VARIABLE:
            return context, StepResult(
                success=False, errors=["Compiled fonts not found"]
            )

        files = context.artifacts["compiled_fonts"]
        fonts = [TTFont(f) for f in files]
        try:
            gen_stat_tables_from_config(
                self._config, fonts, has_italic=self._has_italic
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(e)
            return context, StepResult(success=False, errors=[str(e)])
        return context, StepResult(success=True, artifacts={"compiled_fonts": files})


def stat_from_instances(instances: list[GSInstance]) -> list[StatAxisConfig]:
    """Creates a stat from instances"""
    weight_values = []
    for instance in instances:
        weight_values.append({"name": instance.name, "value": instance.weightValue})
    weight_stat = {
        "tag": "wght",
        "name": "Weight",
        "values": sorted(weight_values, key=lambda x: x["value"]),
    }
    return [weight_stat]

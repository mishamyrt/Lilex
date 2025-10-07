"""Build step base class"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from ..context import BuildContext


@dataclass
class StepResult:
    """Result of a build step execution"""

    success: bool
    message: Optional[str] = None
    artifacts: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class BuildStep(ABC):
    """Single step in the build pipeline"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def execute(self, context: BuildContext) -> tuple[BuildContext, StepResult]:
        """Execute the build step"""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

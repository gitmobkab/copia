from typing import Never
from enum import Enum

from typer import Exit


class ExitCodes(Enum):
    SUCCESS = 0
    VALIDATION_ERROR = 1
    RESSOURCE_ERROR = 2
    FATAL = 3
    UNEXPECTED_ERROR = 4

def exit_app(code: ExitCodes = ExitCodes.SUCCESS) -> Never:
    raise Exit(code.value)
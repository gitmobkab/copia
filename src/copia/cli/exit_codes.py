from enum import IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    VALIDATION_ERROR = 1
    RESOURCE_ERROR = 2
    FATAL = 3
    UNEXPECTED_ERROR = 4
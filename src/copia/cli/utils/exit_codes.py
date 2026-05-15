from enum import IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    VALIDATION_ERROR = 1
    RESOURCE_ERROR = 2
    CONNEXION_TO_DB_FAILED = 3
    FATAL = 4
    UNEXPECTED_ERROR = 5
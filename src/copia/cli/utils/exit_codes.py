from enum import IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    """Returned when nothing wrong happened"""
    UNEXPECTED_ERROR = 1
    """Any unexpected, non-planned error"""    
    BAD_CLI_USAGE = 2
    """Returned when the cli received invalid input, unknown args, options,
    options received value that don't satisfy criteria"""
    BAD_DSL_INPUT = 3
    """Returned when the given dsl input can't be parsed or validated properly"""
    VALIDATION_ERROR = 4
    """Returned when any ressource isn't valid (config file can't be parsed, invalid fetched profile, etc)"""
    RESOURCE_ERROR = 5
    """Returned when any external ressource is missing for use, external library, config file, etc"""
    CONNEXION_TO_DB_REFUSED = 6
    """Returned when the attempt to connect to the db was refused"""
    GENERATION_ERROR = 7
    """Returned when an error occured while generating values"""
    SEEDING_ERROR = 8
    """Returned when the insertion of the generated rows failed"""

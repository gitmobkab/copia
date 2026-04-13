class DuplicateNamedParamException(Exception):
    """Raised by the transformer if a name param repeat"""
    pass

class DuplicateColumnNameError(Exception):
    """Raised by the transformer when a column with a name has already been defined"""
    pass
class UnknownGeneratorException(Exception):
    pass

class TooManyPositionalsException(Exception):
    pass

class UnknownNamedParamException(Exception):
    pass

class TypeMismatchException(Exception):
    pass

class MissingRequiredParamException(Exception):
    pass

class PositionalNamedCollisionException(Exception):
    pass
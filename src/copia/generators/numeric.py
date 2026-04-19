from random import randint, uniform
from .exceptions import GeneratorValueError

def int_range(min: int = 0, max: int = 100) -> int:
    if min > max:
        raise GeneratorValueError("min must be lower or equal to max")
    return randint(min, max)

def float_range(min: float = 0.0, max: float = 100.0) -> float:
    if min > max:
        raise GeneratorValueError("min must be lower or equal to max")
    return uniform(min, max)
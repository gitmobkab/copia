from random import randint, uniform
from .exceptions import GeneratorValueError

def ranged_int(min: int = 0, max: int = 100) -> int:
    """Generate a random integer within a range.
        
    Locale dependent:
        no
 
    Args:
        min: Lower bound (inclusive). Defaults to 0.
        max: Upper bound (inclusive). Defaults to 100.
    """
    if min > max:
        raise GeneratorValueError("min must be lower or equal to max")
    return randint(min, max)

def ranged_float(min: float = 0.0, max: float = 100.0) -> float:
    """Generate a random float within a range.
        
    Locale dependent:
        no
 
    Args:
        min: Lower bound (inclusive). Defaults to 0.0.
        max: Upper bound (inclusive). Defaults to 100.0.
    """
    if min > max:
        raise GeneratorValueError("min must be lower or equal to max")
    return uniform(min, max)
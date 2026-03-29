from ._core import get_faker

def word() -> str:
    return get_faker().word()

def sentence(length: int = 10, vary_length: bool = True) -> str:
    if length <= 0:
        raise ValueError(f"length parameter must be greater than 0, got {length}")
    return get_faker().sentence(length, vary_length)

def paragraph(length: int = 5, vary_length: bool = True) -> str:
    if length <= 0:
        raise ValueError(f"length parameter must be greater than 0, got {length}")
    return get_faker().paragraph(length, vary_length)
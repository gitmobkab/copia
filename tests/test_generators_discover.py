from inspect import signature, Parameter

import pytest

from copia.generators import GENERATORS_REGISTRY, Generator


@pytest.mark.parametrize("generator_name,generator", GENERATORS_REGISTRY.items())
def test_generator_with_default(generator_name, generator):
    if not generator_has_default_args(generator):
        pytest.skip(f"Generator '{generator_name}' does not have default arguments.")
        generator() # whatever this returns, just make sure it doesn't raise an exception

def generator_has_default_args(generator: Generator) -> bool:
    sig = signature(generator)
    for param in sig.parameters.values():
        if param.default is Parameter.empty:
            return False
    return True
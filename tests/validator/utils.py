from typing import Literal

import pytest

from copia.validator.validator import SemanticValidator
from copia.parser.models import GeneratorCall, Params, POSITIONALS, NAMED

def fake_int(min: int, max: int) -> int: ...
def fake_name(locale: str = "en") -> str: ...
def fake_choice(value: Literal["a", "b", "c"]) -> str: ...
def fake_float(min: float, max: float, precision: int = 2) -> float: ...
def fake_no_annotations(a, b): ...
def fake_enum(*args): ...
def fake_racist_picker(*args, racism: bool = True): ...

REGISTRY = {
    "fake_int": fake_int,
    "fake_name": fake_name,
    "fake_choice": fake_choice,
    "fake_float": fake_float,
    "fake_no_annotations": fake_no_annotations,
    "fake_enum": fake_enum,
    "fake_racist_picker": fake_racist_picker
}

VALIDATOR = SemanticValidator(REGISTRY)


def make_call(name: str, positionals: POSITIONALS = [], named: NAMED = {}) -> GeneratorCall:
    return GeneratorCall(
        name=name,
        params=Params(positionals=positionals, named=named)
    )

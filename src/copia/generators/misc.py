from random import choice
from typing import Any

from ._core import get_faker
from .exceptions import GeneratorValueError
from copia.parser.models import TYPES


def uuid() -> str:
    return get_faker().uuid4()


def enum(*args) -> TYPES:
    if not args:
        raise GeneratorValueError("Can't pick without any options")
    return choice(args) # assume parser and validator never allow anything other than TYPES in

def ref(column: str) -> Any:
    """"""
    # filler for validator, help, suggestion, etc
    # the real ref logic is the runners/ module
    raise NotImplementedError("you shouldn't call this generator directly")
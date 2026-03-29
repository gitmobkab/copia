from random import choice

from ._core import get_faker
from copia.parser.models import TYPES


def uuid() -> str:
    return get_faker().uuid4()


def enum(*args) -> TYPES:
    return choice(args) # assume parser and validator never allow anything other than TYPES in

def ref(column: str) -> None:
    """"""
    # filler for validator, help, suggestion, etc
    # the real ref logic is in the TUI
    
    ...
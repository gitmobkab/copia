from random import choice
from typing import Any

from ._core import get_faker
from .exceptions import GeneratorValueError
from copia.parser.models import TYPES


def uuid() -> str:
    """Generate a random UUID v4 as a string."""
    return get_faker().uuid4()


def enum(*args) -> TYPES:
    """Pick a random value from a fixed set of choices.
 
    Args:
        *args: The values to sample from. At least one value required.
    """
    if not args:
        raise GeneratorValueError("Can't pick without any options")
    return choice(args) # assume parser and validator never allow anything other than TYPES in

def ref(column: str) -> Any:
    """Fetch a random existing value from a database column.
 
    Args:
        column: Column reference in 'table.column' format.
 
    Note:
        Only uses values already present in the database.
        An empty column will raise an error at runtime.
    """
    # filler for validator, help, suggestion, etc
    # the real ref logic is the runners/ module
    raise NotImplementedError("you shouldn't call this generator directly")
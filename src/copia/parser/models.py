from dataclasses import dataclass
from typing import TypeAlias

TYPES: TypeAlias = int | float | str | bool
POSITIONALS: TypeAlias = list[TYPES]
NAMED: TypeAlias = dict[str, TYPES]

@dataclass
class Params:
    positionals: POSITIONALS
    named: NAMED
    
@dataclass
class GeneratorCall:
    name: str
    params: Params
        
@dataclass
class Column:
    name: str | None
    generator: GeneratorCall
    
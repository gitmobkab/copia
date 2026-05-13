from dataclasses import dataclass
from typing import TypeAlias

TYPES: TypeAlias = int | float | str | bool
POSITIONALS: TypeAlias = list[TYPES]
NAMED: TypeAlias = dict[str, TYPES]

@dataclass
class Params:
    positionals: POSITIONALS
    named: NAMED
    
    def __positionals_str__(self) -> str:
        printable_positionals = list(map(lambda x: str(x) ,self.positionals))
        return ", ".join(printable_positionals)
    
    def __named_str__(self) -> str:
        printable_pairs: list[str] = []
        for key, value in self.named.items():
            pair = f"{key} = {value}"
            printable_pairs.append(pair)
            
        return ", ".join(printable_pairs)
        
        
    
    def __str__(self) -> str:
        return self.__positionals_str__() + self.__named_str__()
    
    def __repr__(self) -> str:
        return self.__str__()
    
@dataclass
class GeneratorCall:
    name: str
    params: Params
    
    def __str__(self) -> str:
        return f"{self.name}({self.params})"
    
    def __repr__(self) -> str:
        return self.__str__()
        
@dataclass
class Column:
    name: str | None
    unique_constraint: bool
    generator: GeneratorCall

    def __str__(self) -> str:
        name_to_print = self.name or "Anonym"
        unique_str = "unique" if self.unique_constraint else ""
        
        return f"{name_to_print}: {unique_str} {self.generator}"
    
    def __repr__(self) -> str:
        return self.__str__()
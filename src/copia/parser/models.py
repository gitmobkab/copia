from dataclasses import dataclass
from typing import TypeAlias

TYPES: TypeAlias = int | float | str | bool
POSITIONALS: TypeAlias = list[TYPES]
NAMED: TypeAlias = dict[str, TYPES]

@dataclass
class Params:
    positionals: POSITIONALS
    named: NAMED
    
    def _build_str_positional(self) -> str:
        temp_positionals = map(lambda x: str(x), self.positionals)
        return ", ".join(temp_positionals)
    
    def _build_str_named(self) -> str:
        results = []
        for key, value in self.named.items():
            result = f"{key} = {value}"
            results.append(result)
        return ", ".join(results)
    
    def __str__(self) -> str:
        return self._build_str_positional() + self._build_str_named()
    
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
        unique_str = "unique" if self.unique_constraint else ""
        name_str = self.name or "Anonym"
        return f"{name_str}: {unique_str} {self.generator}"
    
    def __repr__(self) -> str:
        return self.__str__()
from dataclasses import dataclass
from inspect import Parameter
from functools import cached_property

@dataclass
class NormalizedSignature:
    normals_args: list[Parameter]
    var_positional: Parameter | None
    keywords_only: dict[str, Parameter]
    
    @cached_property
    def by_name(self) -> dict[str, Parameter]:
        params_dict: dict[str, Parameter] = {}
        for arg in self.normals_args:
            params_dict[arg.name] = arg
        return params_dict | self.keywords_only
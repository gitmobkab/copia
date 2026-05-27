import inspect
import importlib
from pathlib import Path
from typing import get_origin, Callable, Any, Literal, TypeAlias # stupid ref and whatever
from datetime import date
from uuid import UUID

from .exceptions import GeneratorValueError
from ._documentation import generate_generators_markdown
from ._core import GenerationSettings, update_global_faker


ALLOWED_INPUT_TYPES = [int, bool, float, str, Literal]
ALLOWED_RETURN_TYPES = [*ALLOWED_INPUT_TYPES, date, UUID, Any] # use Any sparingly
ALLOWED_INPUT_ORIGINS = [Literal] # aka typing waky types we can't identify without get_origin

GeneratorReturn: TypeAlias = int | bool | float | str | date | UUID | Any
Generator: TypeAlias = Callable[..., GeneratorReturn]

def _build_generators_registery() -> dict[str, Generator]:
    generators : dict[str, Callable] = {}
    generators_path = Path(__file__).parent
    
    for file in generators_path.glob("*.py"):
        if file.stem.startswith("_"):
            continue
        
        module = importlib.import_module(f"copia.generators.{file.stem}")
        
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("_") and func.__module__ == module.__name__:
                if registered_generator := generators.get(name):
                    raise ImportError(f"Found overrinding generator func at {func.__module__}.{name}"
                                        f"\nAlready registered generator identifier at {registered_generator.__module__}.{registered_generator.__name__}")
                _check_func_signature(func)
                generators[name] = func
    
    return generators

# yep no clue of what i'm doing anymore
def _check_func_signature(func: Callable) -> None:
    func_signature = inspect.signature(func)
    func_module = func.__module__
    func_name = func.__name__
    _check_func_parameters_kinds(func_signature, func_module, func_name)
    _check_func_parameters_types(func_signature, func_module, func_name)
    _check_func_return_type(func_signature, func_module, func_name)


def _check_func_parameters_kinds(signature: inspect.Signature, func_module: str, func_name: str) -> None:
    parameters_kinds: list[inspect._ParameterKind] = []
    for parameter in signature.parameters.values():
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            raise ImportError(f"The parameter {parameter.name} in {func_module}.{func_name}, "
                                "is of type VAR_KEYWORD (begins with **)."
                                "\nThis is forbidden by the conventions")
            
        parameters_kinds.append(parameter.kind)
        
    if (inspect.Parameter.POSITIONAL_OR_KEYWORD in parameters_kinds 
        and
        inspect.Parameter.VAR_POSITIONAL in parameters_kinds):
        raise ImportError(
            "The generator at {func_module} identified by {func_name}, "
            "contains a VAR_POSITIONAL (begin with *) and POSITIONAL_OR_KEYWORD arguments at the same time."
            f"\nSignature: def {func_name}{signature}"
        )

def _check_func_parameters_types(signature: inspect.Signature, func_module: str, func_name: str) -> None:
    for parameter in signature.parameters.values():
        try:
            _check_parameter_type(parameter, ALLOWED_INPUT_TYPES, ALLOWED_INPUT_ORIGINS)
        except ImportError as reason:
            raise ImportError(
                "PARAMETERS TYPE CHECK FAILED:\n",
                f"The parameter {parameter.name!r} in {func_module}.{func_name}, ",
                f"{reason}"
            )

def _check_func_return_type(signature: inspect.Signature, func_module: str, func_name: str) -> None:
    try:
        _check_annotation(signature.return_annotation, ALLOWED_RETURN_TYPES, ALLOWED_INPUT_ORIGINS)
    except ImportError as reason:
        raise ImportError(
            "RETURN TYPE CHECK FAILED:\n",
            f"The function located at {func_module}.{func_name}, ",
            f"{reason}"
        )

def _check_parameter_type(parameter: inspect.Parameter, allowed: list, origins: list) -> None:
    if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
        return
    _check_annotation(parameter.annotation, allowed, origins)
    
def _check_annotation(annotation: Any, allowed: list, origins: list) -> None:
    origin = get_origin(annotation)
    if annotation not in allowed and origin not in origins:
        raise ImportError(
            f"uses an unsupported type: {annotation}"
            f"\nALLOWED = {allowed + origins}"
        )
    
GENERATORS_REGISTRY: dict[str, Generator] = _build_generators_registery()
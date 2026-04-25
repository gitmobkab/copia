import inspect
import importlib
from pathlib import Path
from typing import Callable
from .exceptions import GeneratorValueError
from ._documentation import generate_generators_markdown
from ._core import GenerationSettings, update_global_faker

def _build_generators_registery() -> dict[str, Callable]:
    generators : dict[str, Callable] = {}
    generators_path = Path(__file__).parent
    
    for file in generators_path.glob("*.py"):
        if file.stem.startswith("_"):
            continue
        
        module = importlib.import_module(f"copia.generators.{file.stem}")
        
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("_") and func.__module__ == module.__name__:
                if generators.get(name):
                    raise ImportWarning(f"found overrinding generator func at {func.__module__} with identifier {name}")
                _check_func_signature(func)
                generators[name] = func
    
    return generators

def _check_func_signature(func: Callable) -> None:
    signature = inspect.signature(func)
    parameters_kinds = [parameter.kind for parameter in signature.parameters.values()]
    if inspect.Parameter.VAR_KEYWORD in parameters_kinds:
        raise ImportWarning(f"the generator at {func.__module__} identified by {func.__name__} contains a VAR_KEYWORD (**kwargs)")
    if (inspect.Parameter.POSITIONAL_OR_KEYWORD in parameters_kinds 
        and
        inspect.Parameter.VAR_POSITIONAL in parameters_kinds):
        ERR_MSG = f"""
    "the generator at {func.__module__} identified by {func.__name__} contains a var positional (*args) and a POSITIONAL_OR_KEYWORD at the same time.
    This weaken the SemanticValidator"
        """
        raise ImportWarning(ERR_MSG)


GENERATORS_REGISTRY = _build_generators_registery()
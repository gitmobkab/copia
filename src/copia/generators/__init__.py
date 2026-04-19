import inspect
import importlib
from pathlib import Path
from collections.abc import Callable
from .exceptions import GeneratorValueError

def discover() -> dict[str, Callable]:
    generators = {}
    generators_path = Path(__file__).parent
    
    for file in generators_path.glob("*.py"):
        if file.stem.startswith("_"):
            continue
        
        module = importlib.import_module(f"copia.generators.{file.stem}")
        
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("_") and func.__module__ == module.__name__:
                generators[name] = func
    
    return generators

GENERATORS = discover()
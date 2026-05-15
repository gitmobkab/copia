from difflib import get_close_matches

from copia.generators import GENERATORS_REGISTRY


def get_generator_suggestions(generator: str, limit: int = 5) -> list[str]:
    generators_names = list(GENERATORS_REGISTRY.keys())
    return get_suggestions(generator, generators_names, limit)

def get_suggestions(value: str, sources: list[str], limit: int = 5) -> list[str]:
    return get_close_matches(value, sources, limit)

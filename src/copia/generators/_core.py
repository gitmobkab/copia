from faker import Faker
from faker.config import AVAILABLE_LOCALES
from dataclasses import dataclass

_fake = Faker()
"""global faker instance for all generators based on faker"""

@dataclass
class GenerationSettings:
    locale: str = "en_US"
    """the locale to use, this will only influence faker based generators"""
    optimized: bool = False
    """if true, this will disable weighting of the values.
    Effectively increasing performance but losing real-world frequencies.
    """

def update_global_faker(generation_settings: GenerationSettings) -> None:
    """replace the global faker object with a new one

    Args:
        generation_settings (GenerationSettings): the new generation settings

    Raises:
        ValueError: if the locale key of the generation settings isn't supported by faker
    """
    locale = generation_settings.locale
    use_weighting = not generation_settings.optimized
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"{locale!r} is not in fakers availables locals")
    global _fake
    _fake = Faker(locale=locale, use_weighting=use_weighting)

def get_faker() -> Faker:
    """return the global faker object"""
    return _fake

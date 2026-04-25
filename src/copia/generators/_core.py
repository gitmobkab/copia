from faker import Faker
from faker.config import AVAILABLE_LOCALES

_fake = Faker()
"""global faker instance for all generators based on faker"""

def update_global_faker(locale: str = "en_US", use_weighting: bool = True) -> None:
    """replace the global faker object with a new on

    Args:
        locale (str, optional): the locale to use for the next generations. Defaults to "en_US".
        use_weighting (bool, optional): if faker should weight the values to generate.
            this will improve the speed of generation, but the datasets will be completly random.
            See https://faker.readthedocs.io/en/master/#optimizations.
            Defaults to True.

    Raises:
        ValueError: if the locale isn't supported by faker
    """
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"{locale!r} is not in fakers availables locals")
    global _fake
    _fake = Faker(locale=locale, use_weighting=use_weighting)

def get_faker() -> Faker:
    """return the global faker object"""
    return _fake

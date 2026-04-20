from ._core import get_faker
from datetime import date

def past_date() -> date:
    """Generate a random date in the past."""
    return get_faker().past_date()

def future_date() -> date:
    """Generate a random date in the future."""
    return get_faker().future_date()

def date_of_birth() -> date:
    """Generate a random realistic date of birth."""
    return get_faker().date_of_birth()
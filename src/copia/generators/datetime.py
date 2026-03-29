from ._core import get_faker
from datetime import date

def past_date() -> date:
    return get_faker().past_date()

def future_date() -> date:
    return get_faker().future_date()

def date_of_birth() -> date:
    return get_faker().date_of_birth()
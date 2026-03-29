from ._core import get_faker


def address() -> str:
    return get_faker().address()

def city() -> str:
    return get_faker().city()

def country() -> str:
    return get_faker().country()

def zipcode() -> str:
    return get_faker().zipcode()



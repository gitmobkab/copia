from ._core import get_faker


def address() -> str:
    """Generate a realistic street address.
    
    Locale dependent:
        yes
    """
    return get_faker().address()

def city() -> str:
    """Generate a random city name.

    Locale dependent:
        yes    
    """
    return get_faker().city()

def country() -> str:
    """Generate a random country name.
    
    Locale dependent:
        yes

    """
    return get_faker().country()

def zipcode() -> str:
    """Generate a random postal code.
    
    Locale dependent:
        no
    """
    return get_faker().zipcode()



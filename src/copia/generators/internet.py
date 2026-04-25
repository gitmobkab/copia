from typing import Literal

from ._core import get_faker
from .exceptions import GeneratorValueError


def url() -> str:
    """Generate a random URL.
        
    Locale dependent:
        yes
    """
    return get_faker().url()

def ipv4(
       network: bool = False, 
       address_class: Literal["a", "b", "c"] = "c", 
       private: bool = False) -> str:
    """Generate a random IPv4 address.
    
    Locale dependent:
        no
 
    Args:
        network: Return a network address with CIDR notation (e.g. 192.168.0.0/24).
            Defaults to False.
        address_class: IP address class to generate ('a', 'b', or 'c').
            Defaults to 'c'.
        private: Restrict to private address ranges. Defaults to False.
    """
    
    SUPPORTED_ADDRESS_CLASSES = ["a", "b", "c"]
    if address_class not in SUPPORTED_ADDRESS_CLASSES:
        raise GeneratorValueError(f"{address_class} is not a supported ipv4 address class")
    
    fake = get_faker()
    if private:
        real_private = "private"
    else:
        real_private = "public"
    return fake.ipv4(network, address_class, real_private)

def ipv6(network: bool = False ) -> str:
    """Generate a random IPv6 address.
 
    Locale dependent:
        no
        
    Args:
        network: Return a network address with prefix length notation.
            Defaults to False.
    """
    return get_faker().ipv6(network)

def user_agent() -> str:
    """Generate a random browser user agent string.
        
    Locale dependent:
        no
    """
    return get_faker().user_agent()
from typing import Literal

from ._core import get_faker


def url() -> str:
    return get_faker().url()

def ipv4(
       network: bool = False, 
       address_class: Literal["a", "b", "c"] = "c", 
       private: bool = False) -> str:
    
    SUPPORTED_ADDRESS_CLASSES = ["a", "b", "c"]
    if address_class not in SUPPORTED_ADDRESS_CLASSES:
        raise ValueError(f"{address_class} is not a supported ipv4 address class")
    
    fake = get_faker()
    if private == True:
        real_private = "private"
    else:
        real_private = "public"
    return fake.ipv4(network, address_class, real_private)

def ipv6(network: bool = False ) -> str:
    return get_faker().ipv6(network)

def user_agent() -> str:
    return get_faker().user_agent()
from typing import Literal

from ._core import get_faker


def name(gender: Literal["male","female", "nonbinary", "all"] = "all") -> str:
    first_name = firstname(gender)
    last_name = lastname(gender)
    return first_name + " " + last_name

def firstname(gender: Literal["male", "female", "nonbinary" ,"all"] = "all") -> str:
    fake = get_faker()
    match gender:
        case "male":
            return fake.first_name_male()
        case "female":
            return fake.first_name_female()
        case "nonbinary":
            return fake.first_name_nonbinary()
        case "all":
            return fake.first_name()
        case _:
            raise ValueError(f"{gender} is not an available gender")
        

def lastname(gender: Literal["male", "female", "nonbinary" ,"all"] = "all") -> str:
    fake = get_faker()
    match gender:
        case "male":
            return fake.last_name_male()
        case "female":
            return fake.last_name_female()
        case "nonbinary":
            return fake.last_name_nonbinary()
        case "all":
            return fake.last_name()
        case _:
            raise ValueError(f"{gender} is not an available gender")
        
        
def address() -> str:
    return get_faker().address()

def phone() -> str:
    return get_faker().phone_number()

def email(safe : bool = True, domain: str = "") -> str:
    fake = get_faker()
    if domain.strip() == "":
        final_domain = None
    else:
        final_domain = domain
    return fake.email(safe, final_domain)

def username() -> str:
    return get_faker().user_name()

def password(length: int = 12,
             special_chars: bool = True,
             upper_case: bool = False,
             lower_case: bool = False) -> str:
    if length <= 0:
        raise ValueError(f"length parameter must be greater than 0, got {length}")
    fake = get_faker()
    return fake.password(length, special_chars, upper_case, lower_case)

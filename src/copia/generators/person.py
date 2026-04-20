from typing import Literal

from ._core import get_faker
from .exceptions import GeneratorValueError

def name(gender: Literal["male","female", "nonbinary", "all"] = "all") -> str:
    """Generate a full name (first + last).
 
    Args:
        gender: Filter names by gender. Use 'all' for any gender.
            Defaults to 'all'.
    """
    first_name = firstname(gender)
    last_name = lastname(gender)
    return first_name + " " + last_name

def firstname(gender: Literal["male", "female", "nonbinary" ,"all"] = "all") -> str:
    """Generate a random first name.
 
    Args:
        gender: Filter names by gender. Use 'all' for any gender.
            Defaults to 'all'.
    """
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
            raise GeneratorValueError(f"{gender} is not an available gender")
        

def lastname(gender: Literal["male", "female", "nonbinary" ,"all"] = "all") -> str:
    """Generate a random last name.
 
    Args:
        gender: Filter names by gender. Use 'all' for any gender.
            Defaults to 'all'.
    """
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
            raise GeneratorValueError(f"{gender} is not an available gender")

def phone() -> str:
    """Generate a random phone number."""
    return get_faker().phone_number()

def email(safe : bool = True, domain: str = "") -> str:
    """Generate a random email address.
 
    Args:
        safe: If True, uses safe domains (example.com, test.com) that
            cannot receive real emails. Defaults to True.
        domain: Force a specific email domain. Overrides safe if provided.
            Defaults to ''.
    """
    fake = get_faker()
    if domain.strip() == "":
        final_domain = None
    else:
        final_domain = domain
    return fake.email(safe, final_domain)

def username() -> str:
    """Generate a random username."""
    return get_faker().user_name()

def password(length: int = 12,
             special_chars: bool = True,
             upper_case: bool = False,
             lower_case: bool = False) -> str:
    """Generate a random password.
 
    Args:
        length: Number of characters in the password. Defaults to 12.
        special_chars: Include special characters (!@#...). Defaults to True.
        upper_case: Ensure at least one character is in uppercase. Defaults to False.
        lower_case: Ensure at least one character is in lowercase. Defaults to False.
    """
    if length <= 0:
        raise GeneratorValueError(f"length parameter must be greater than 0, got {length}")
    fake = get_faker()
    return fake.password(length, special_chars, upper_case, lower_case)

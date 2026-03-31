"""All the exceptions used by the cli Layer of copia"""

from pydantic import ValidationError


class InvalidConfigError(Exception):
    """Exception raised when the config file is invalid in a way that breaks management"""

class ProfileError(Exception):
    """base class for all profiles errors"""
    
class ProfilesKeyIsNotATableError(ProfileError):
    """Exception raised when the profiles key is found but not a TOML table"""

class ProfileNotFoundError(ProfileError):
    """Exception raised when a profile couldn't be found in the config file"""

class FoundProfileIsNotATableError(ProfileError):
    """Exception raised when a profile is found, but isn't a TOML table"""
    
    def __init__(self, profile_name: str) -> None:
        self.profile_name = profile_name
    
    def __str__(self) -> str:
        return f"'profiles.{self.profile_name}' is not a TOML Table"
    
    def __repr__(self) -> str:
        return self.__str__()    

class ProfileAlreadyExists(ProfileError):
    """Exception raised when trying to add a profile that already exists"""


class InvalidProfileError(ProfileError):
    """
    This exception should be raised when the Profile model fails to validate a potential profile.
    
    it takes the exact pydantic ValidationError exception and build off a list of reasons
    
    it holds a list of reasons, which are just strings explaining what fail in the validation process
    """
    
    def __init__(self, PydanticValidationError: ValidationError) -> None:
        self.reasons : list[_InvalidProfileReason] = []
        
        ValidateError = PydanticValidationError
        for error in ValidateError.errors():
                field = error["loc"][0]
                field = str(field)
                msg = error["msg"].removeprefix("Value error, ")
                current_reason = _InvalidProfileReason(field, msg)
                self.reasons.append(current_reason)
            
    def __str__(self) -> str:
        printable_reasons = map(str, self.reasons)
        return "\n".join(printable_reasons)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __iter__(self):
        for reason in self.reasons:
            yield reason
    
class _InvalidProfileReason:
    """
    the reason of a profile validation failure
    """
    
    def __init__(self, field: str, msg: str) -> None:
        self.field = field
        self.msg = msg
        
    def __str__(self) -> str:
        return f"{self.field} : {self.msg}"
    
    def __repr__(self) -> str:
        return self.__str__()
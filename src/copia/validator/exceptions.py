class ValidationError(Exception):
    ...

class CaughtValidationError(ValidationError):
    
    def __init__(self, column_index: int, validation_err: ValidationError) -> None:
        self.column_index = column_index
        self.validation_err = validation_err
        
    def __str__(self) -> str:
        return f"Error on column {self.column_index}:\n\t{self.validation_err}"
    
class ValidationErrors(ValidationError):
    
    def __init__(self, *errors: ValidationError) -> None:
        self.errors = errors
        
    def __str__(self) -> str:
        seperator = "-"*20
        return f"\n{seperator}\n".join(str(err) for err in self.errors)
    
class UnknownGeneratorException(ValidationError):
    pass

class TooManyPositionalsException(ValidationError):
    pass

class UnknownNamedParamException(ValidationError):
    pass

class TypeMismatchException(ValidationError):
    pass

class MissingRequiredParamException(ValidationError):
    pass

class PositionalNamedCollisionException(ValidationError):
    pass
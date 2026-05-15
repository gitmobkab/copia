from copia.suggestions import get_generator_suggestions

class ValidationError(Exception):
    ...

class CaughtValidationError(ValidationError):
    
    def __init__(self, column_index: int, validation_err: ValidationError) -> None:
        self.column_index = column_index
        self.validation_err = validation_err
        
    def __str__(self) -> str:
        return f"Error on column {self.column_index}:\n{self.validation_err}"
    
class ValidationErrors(ValidationError):
    
    def __init__(self, *errors: ValidationError) -> None:
        self.errors = errors
        
    def __str__(self) -> str:
        seperator = "-"*20
        return f"\n{seperator}\n".join(str(err) for err in self.errors)
    
class UnknownGeneratorException(ValidationError):
    
    def __init__(self, name: str) -> None:
        self.name = name
        """the passed name of the unknwon generator"""
        self._suggestions = get_generator_suggestions(name)
        
    def __str__(self):
        msg = f"Unknown generator: {self.name!r}"
        if self._suggestions:
            msg += "\nDid you mean?:\n"
            msg += "\n".join(f"   - {s}" for s in self._suggestions)
        return msg

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
import inspect



class GeneratorValueError(ValueError):
    """
    Raised by generators when the provided input is wrong
    This is for differenciation from unexpected exceptions
    """
    
    def __init__(self, reason: str, generator_name: str | None = None) -> None:
        if generator_name is None:
            generator_name = inspect.stack()[1].function
        
        self.generator_name = generator_name
        """the name of the generator, if None, it will be deduced from the call stack"""
    
        self.reason = reason
        """the reason that caused the generator value error"""
        
    def __str__(self) -> str:
        return f"{self.generator_name}: {self.reason}"
    
    def __repr__(self) -> str:
        return self.__str__()
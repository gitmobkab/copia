from ._core import get_faker
from .exceptions import GeneratorValueError

def word() -> str:
    """Generate a random word.
        
    Locale dependent:
        yes
    """
    return get_faker().word()

def sentence(length: int = 10, vary_length: bool = True) -> str:
    """Generate a random sentence.
    
    Locale dependent:
        yes

    Args:
        length: Number of words in the sentence. Defaults to 10.
        vary_length: Randomize word count around the target length.
            Defaults to True.
    """
    if length <= 0:
        raise GeneratorValueError(f"length parameter must be greater than 0, got {length}")
    return get_faker().sentence(length, vary_length)

def paragraph(length: int = 5, vary_length: bool = True) -> str:
    """Generate a random paragraph of text.
    
    Locale dependent:
        yes

    Args:
        length: Number of sentences in the paragraph. Defaults to 5.
        vary_length: Randomize sentence count around the target length.
            Defaults to True.
    """
    if length <= 0:
        raise GeneratorValueError(f"length parameter must be greater than 0, got {length}")
    return get_faker().paragraph(length, vary_length)
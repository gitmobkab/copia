from typing import TypeAlias, Callable, Generator

from copia.runners import GeneratedRow


FormatResult: TypeAlias = dict | str

Formatter: TypeAlias = Callable[
    [list[GeneratedRow]],
    
    Generator[FormatResult, None, None]
]
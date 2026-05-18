from typing import Generator
from json import dumps
from copia.runners import GeneratedRow

def format_to_json(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    yield "["
    for index, row in enumerate(rows, 1):
        line = "\t" + dumps(row)
        sep = ", " if index != len(rows) else ""
        yield line + sep
    yield "]"
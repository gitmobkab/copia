from typing import Generator

from copia.runners import GeneratedRow

def format_to_json(rows: list[GeneratedRow]) -> Generator[GeneratedRow, None, None]:
    for row in rows:
        yield row
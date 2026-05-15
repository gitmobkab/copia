from typing import Generator

from copia.runners import GeneratedRow
from .utils import get_dict_values_as_str


def format_to_sql(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    for row in rows:
        printable_row = get_dict_values_as_str(row)
        yield f"({printable_row})"
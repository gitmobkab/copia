from typing import Generator

from copia.runners import GeneratedRow
from .utils import get_dict_values_as_str


def format_to_csv(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    if not rows:
        raise ValueError("rows can't be empty")
    columns_names = rows[0].keys()
    yield ", ".join(columns_names)
    
    for row in rows:
        printable_row = get_dict_values_as_str(row)
        yield printable_row
    
    
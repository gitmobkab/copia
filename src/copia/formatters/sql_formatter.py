from typing import Generator

from copia.runners import GeneratedRow
from .csv_formatter import format_to_csv


def format_to_sql(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    for row in format_to_csv(rows):
        yield f"({row})"
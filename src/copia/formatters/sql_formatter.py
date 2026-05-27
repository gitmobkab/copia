from typing import Generator
from uuid import UUID
from datetime import date

from copia.generators import GeneratorReturn
from copia.runners import GeneratedRow



def format_to_sql(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    if not rows:
        raise ValueError("Rows can't be empty")
    columns_names = ", ".join(rows[0].keys())
    yield f"({columns_names})"
    for row in rows:
        values = map(format_value_for_sql, row.values())
        output = ", ".join(values)
        yield f"({output})"
        
        

def format_value_for_sql(value: GeneratorReturn) -> str:
    match value:
        case bool():
            return "TRUE" if value else "FALSE"
        case int() | float():
            return str(value)
        case UUID():
            return f"'{value}'"
        case date():
            return f"'{value.isoformat()}'"
        case str():
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        case _:
            return f"'{value}'"
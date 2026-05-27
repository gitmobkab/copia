from typing import Generator

from copia.runners import GeneratedRow

def format_to_csv(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    if not rows:
        raise ValueError("rows can't be empty")
    columns_names = rows[0].keys()
    yield ",".join(columns_names)
    
    for row in rows:
        printable_row = get_dict_values_as_str(row)
        yield printable_row
    
def get_dict_values_as_str(dict_input: dict) -> str:
    values = dict_input.values()
    printable_values = map(lambda x: str(x), values)
    return ",".join(printable_values)
from typing import Any, Generator
from json import dumps, JSONEncoder
from uuid import UUID
from datetime import date

from copia.runners import GeneratedRow
from copia.generators import GeneratorReturn

class CopiaEncoder(JSONEncoder):
    def default(self, obj: GeneratorReturn) -> Any:
        match obj:
            case UUID():
                return obj.hex
            case date():
                return obj.isoformat()
            case _:
                return super().default(obj)
            
def format_to_json(rows: list[GeneratedRow]) -> Generator[str, None, None]:
    yield "["
    for index, row in enumerate(rows, 1):
        line = "\t" + dumps(row, cls=CopiaEncoder)
        sep = ", " if index != len(rows) else ""
        yield line + sep
    yield "]"
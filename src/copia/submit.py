from itertools import islice
from typing import Iterable, Any, Generator

from sqlalchemy import Engine, table, column, insert

DEFAULT_BATCH_SIZE = 200

def _batched(iterable: Iterable, batch_size: int = DEFAULT_BATCH_SIZE) -> Generator[list[Any], None, None]:
    iterator = iter(iterable)
    while chunk := list(islice(iterator, batch_size)):
        yield chunk
        
def submit_rows(engine: Engine, rows: list[dict[str, Any]], table_name: str) -> None:
    columns = [column(k) for k in rows[0].keys()]
    target_table = table(table_name, *columns)
    
    with engine.begin() as connection:
        for batch in _batched(rows):
            connection.execute(insert(target_table), batch)

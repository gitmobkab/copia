from abc import ABC, abstractmethod
from typing import Any, Sequence

from .models import ColumnInfo

class BaseAdapter(ABC):

    @abstractmethod
    def ping(self) -> None: ...

    @abstractmethod
    def get_tables(self) -> list[str]: ...

    @abstractmethod
    def get_columns(self, table: str) -> list[ColumnInfo]: 
        self.check_table(table)

    @abstractmethod
    def fetch(self, table: str, columns: Sequence[str]) -> list[tuple[Any, ...]]: 
        self.check_columns_in_table(table, columns)

    @abstractmethod
    def insert(self, table: str, rows: Sequence[dict[str, Any]], batch_size: int = 200) -> None:
        if not rows:
            return
        columns = list(rows[0].keys())
        self.check_columns_in_table(table, columns)
    
    @abstractmethod
    def close(self) -> None: ...    
    
    def check_table(self, table: str) -> None:
        if table not in self.get_tables():
            raise ValueError(f'The table {table!r} does not exist in the current db')
        
    def check_columns_in_table(self, table: str, columns: Sequence[str]) -> None:
        self.check_table(table)
        columns_names = [column.name for column in self.get_columns(table)]
        for column in columns:
            if column not in columns_names:
                raise ValueError(f'The column {column!r} in table {table!r} does not exist')
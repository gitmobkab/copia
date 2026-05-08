from abc import ABC, abstractmethod
from typing import Any, Sequence

from .models import ColumnInfo

class BaseAdapter(ABC):

    @abstractmethod
    def ping(self) -> None: ...

    @abstractmethod
    def get_tables(self) -> list[str]: ...

    @abstractmethod
    def get_columns(self, table: str) -> list[ColumnInfo]: ...

    @abstractmethod
    def fetch(self, table: str, columns: Sequence[str]) -> list[tuple[Any, ...]]: ...

    @abstractmethod
    def insert(self, table: str, rows: Sequence[dict[str, Any]], batch_size: int = 200) -> None: ...
    
    @abstractmethod
    def close(self) -> None: ...    
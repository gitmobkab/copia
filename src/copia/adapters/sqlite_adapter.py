from typing import Any, Sequence, Type, Callable
from itertools import islice
from uuid import UUID
import sqlite3

from .base_adapter import BaseAdapter
from .models import ColumnInfo


class SQLiteAdapter(BaseAdapter):

    COERCERS: dict[Type, Callable[..., Any]] = {
        UUID: str
    }

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        # SQLite disables FK enforcement per-connection by default;
        # turn it on so seeded data behaves like Postgres/MySQL.
        self._connection.execute("PRAGMA foreign_keys = ON")

    def ping(self) -> None:
        self._connection.execute("SELECT 1")

    def get_tables(self) -> list[str]:
        cursor = self._connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in cursor.fetchall()]

    def get_columns(self, table: str) -> list[ColumnInfo]:
        super().get_columns(table)
        columns: list[ColumnInfo] = []
        quoted_table = self._quote_identifier(table)
        cursor = self._connection.execute(f"PRAGMA table_info({quoted_table})")
        for _, name, col_type, notnull, default, pk in cursor.fetchall():
            columns.append(ColumnInfo(
                name=name,
                type=col_type or "",
                is_nullable=not bool(notnull),
                default=default,
                extra="PRIMARY KEY" if pk else None
            ))
        return columns

    def fetch(self, table: str, columns: Sequence[str]) -> list[tuple[Any, ...]]:
        super().fetch(table, columns)
        columns_query = ", ".join(self._quote_identifier(col) for col in columns)
        quoted_table = self._quote_identifier(table)
        cursor = self._connection.execute(f"SELECT {columns_query} FROM {quoted_table}")
        return cursor.fetchall()

    def insert(self, table: str, rows: Sequence[dict[str, Any]], batch_size: int = 200) -> None:
        super().insert(table, rows)
        columns = list(rows[0].keys())
        columns_query = ", ".join(self._quote_identifier(c) for c in columns)
        placeholders = ", ".join(f":{c}" for c in columns)
        quoted_table = self._quote_identifier(table)
        query = f"INSERT INTO {quoted_table} ({columns_query}) VALUES ({placeholders})"

        iterator = iter(rows)
        try:
            while batch := list(islice(iterator, batch_size)):
                coerced_batch = list(map(self._coerce_row, batch))
                self._connection.executemany(query, coerced_batch)
            self._connection.commit()
        except Exception as err:
            self._connection.rollback()
            raise err

    def close(self) -> None:
        self._connection.close()

    def _coerce_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {key: self._coerce(value) for key, value in row.items()}

    def _coerce(self, value: Any) -> Any:
        coercer = self.COERCERS.get(type(value))
        return coercer(value) if coercer else value

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        # Standard SQL identifier escaping: wrap in double quotes,
        # double any embedded double quotes.
        return '"' + identifier.replace('"', '""') + '"'
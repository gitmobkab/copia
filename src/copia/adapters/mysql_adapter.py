from typing import Any, Sequence, Type, Callable
from itertools import islice
from uuid import UUID

import pymysql
from pymysql.cursors import Cursor

from .base_adapter import BaseAdapter
from .models import ColumnInfo


class MySQLAdapter(BaseAdapter):
    
    COERCERS: dict[Type, Callable[..., Any]] = {
        UUID : str
    }
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
        self._connection = pymysql.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                    cursorclass=pymysql.cursors.DictCursor,
                )
    
    def ping(self) -> None:
        self._connection.ping()

    def get_tables(self) -> list[str]:
        with self._connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables : list[str] = []
            for row in cursor.fetchall():
                row_values = list(row.values())
                table_name = row_values[0]
                tables.append(table_name)
            return tables
        
    def get_columns(self, table: str) -> list[ColumnInfo]:
        self.check_table(table)
        columns : list[ColumnInfo] = []
        with self._connection.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            for column in cursor.fetchall():
                column_info = ColumnInfo(
                    name=column['Field'],
                    type=column['Type'],
                    is_nullable=column['Null'] == "YES",
                    default=column['Default'],
                    extra=column['Extra'] or None
                )
                columns.append(column_info)
            return columns

    def fetch(self, table: str, columns: Sequence[str]) -> list[tuple[Any, ...]]:
        self.check_columns_in_table(table, columns)        
        columns_query = ", ".join(columns)
        with self._connection.cursor(Cursor) as cursor:
            cursor.execute(f"SELECT {columns_query} FROM {table}")
            return list(cursor.fetchall())

    def insert(self, table: str, rows: Sequence[dict[str, Any]], batch_size: int = 200) -> None:
        if not rows:
            return
        columns = list(rows[0].keys())
        self.check_columns_in_table(table, columns)
        columns_query = ", ".join(columns)
        placeholders = ", ".join(f"%({c})s" for c in columns)
        query = f"INSERT INTO {table} ({columns_query}) VALUES ({placeholders})"

        iterator = iter(rows)
        with self._connection.cursor() as cursor:
            while batch := list(islice(iterator, batch_size)):
                coerced_batch = list(map(self.coerce_row, batch))
                cursor.executemany(query, coerced_batch)
        self._connection.commit()
        
    def coerce_row(self, row: dict[str, Any]) -> dict[str, Any]:
        coerced_row: dict[str, Any] = {}
        for key, value in row.items():
            coerced_row[key] = self.coerce(value)
        return coerced_row
        
    
    def coerce(self, value: Any) -> Any:
        type_of_value = type(value)
        if coercer := self.COERCERS.get(type_of_value):
            return coercer(value)
        return value
        
    def close(self) -> None:
        self._connection.close()
        
    def check_table(self, table: str) -> None:
        if table not in self.get_tables():
            raise ValueError(f'The table {table!r} does not exist in the current db')
        
    def check_columns_in_table(self, table: str, columns: Sequence[str]) -> None:
        self.check_table(table)
        real_columns_names = [column.name for column in self.get_columns(table)]
        for column in columns:
            if column not in real_columns_names:
                raise ValueError(f'The column {column!r} in table {table!r} does not exist')
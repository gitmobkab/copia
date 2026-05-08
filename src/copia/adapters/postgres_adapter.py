from typing import Any, Sequence
from itertools import islice

import psycopg
from psycopg.sql import SQL, Identifier, Placeholder

from .base_adapter import BaseAdapter
from .models import ColumnInfo


class PostgresAdapter(BaseAdapter):

    def __init__(self, host:str, port: int, database: str, user:str, password: str) -> None:            
        connection_string = f"host={host} port={port} dbname={database} password={password} user={user}"
        self._connection = psycopg.connect(connection_string)

    def ping(self) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT 1")

    def get_tables(self) -> list[str]:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
            )
            return [row[0] for row in cursor.fetchall()]

    def get_columns(self, table: str) -> list[ColumnInfo]:
        columns: list[ColumnInfo] = []
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT column_name, data_type, is_nullable, column_default " 
                "FROM information_schema.columns "
                "WHERE table_name = %s AND table_schema = 'public'",
                (table,)
            )
            for row in cursor.fetchall():
                current_column = ColumnInfo(
                    name=row[0],
                    type=row[1],
                    is_nullable=row[2],
                    default=row[3],
                    extra=None
                )
                columns.append(current_column)
            return columns

    def fetch(self, table: str, columns: Sequence[str]) -> list[tuple[Any, ...]]:
        query = SQL("SELECT {0} FROM {1}")
        columns_query = self.escape_columns(columns)
        composed_query = query.format(
            columns_query,
            Identifier(table)
        )
        with self._connection.cursor() as cursor:
            cursor.execute(composed_query)
            return cursor.fetchall()

    def insert(self, table: str, rows: Sequence[dict[str, Any]], batch_size: int = 200) -> None:
        if not rows:
            return
        columns = list(rows[0].keys())
        query = SQL("INSERT INTO {0} ({1}) VALUES ({2})")
        columns = list(rows[0].keys())
        placeholders = map(Placeholder, columns)
        composed_query = query.format(
            Identifier(table),
            self.escape_columns(columns),
            SQL(", ").join(placeholders)
        )
    
        iterator = iter(rows)
        with self._connection.cursor() as cursor:
            while batch := list(islice(iterator, batch_size)):
                cursor.executemany(composed_query, batch)
        self._connection.commit()
        

    def close(self) -> None:
        self._connection.close()
    
    
    def escape_columns(self, columns: Sequence[str]):
        escaped_columns = map(Identifier, columns)
        columns_query = SQL(", ").join(escaped_columns)
        return columns_query

    
import pytest

from copia.adapters.mysql_adapter import MySQLAdapter

SAMPLE_ROWS = [
    {"id": 1, "email": "alice@test.com", "username": "alice"},
    {"id": 2, "email": "bob@test.com",   "username": "bob"},
    {"id": 3, "email": "carol@test.com", "username": "carol"},
]

def test_ping(mysql_adapter: MySQLAdapter):
    mysql_adapter.ping()

def test_get_tables(mysql_adapter: MySQLAdapter):
    tables = mysql_adapter.get_tables()
    assert "users" in tables

def test_get_columns(mysql_adapter: MySQLAdapter):
    columns = mysql_adapter.get_columns("users")
    names = [c.name for c in columns]
    assert "id" in names
    assert "email" in names
    assert "username" in names

def test_get_columns_unknown_table(mysql_adapter: MySQLAdapter):
    with pytest.raises(ValueError, match="does not exist"):
        mysql_adapter.get_columns("nonexistent")


def test_insert_and_fetch(mysql_adapter: MySQLAdapter):
    mysql_adapter.insert("users", SAMPLE_ROWS)
    result = mysql_adapter.fetch("users", ["id", "email", "username"])
    assert len(result) == 3

def test_fetch_specific_columns(mysql_adapter: MySQLAdapter):
    mysql_adapter.insert("users", SAMPLE_ROWS)
    result = mysql_adapter.fetch("users", ["email"])
    assert all(len(row) == 1 for row in result)

def test_insert_empty_rows_raises(mysql_adapter: MySQLAdapter):
    with pytest.raises(ValueError):
        mysql_adapter.insert("users", [])

def test_insert_batch(mysql_adapter: MySQLAdapter):
    rows = [{"id": i, "email": f"user{i}@test.com", "username": f"user{i}"} for i in range(1, 502)]
    mysql_adapter.insert("users", rows, batch_size=200)
    result = mysql_adapter.fetch("users", ["id"])
    assert len(result) == 501

def test_fetch_unknown_column(mysql_adapter: MySQLAdapter):
    with pytest.raises(ValueError, match="does not exist"):
        mysql_adapter.fetch("users", ["nonexistent"])

def test_fetch_unknown_table(mysql_adapter: MySQLAdapter):
    with pytest.raises(ValueError, match="does not exist"):
        mysql_adapter.fetch("nonexistent", ["id"])
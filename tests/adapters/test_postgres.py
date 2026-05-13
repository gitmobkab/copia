import pytest

from copia.adapters.postgres_adapter import PostgresAdapter

SAMPLE_ROWS = [
    {"id": 1, "email": "alice@test.com", "username": "alice"},
    {"id": 2, "email": "bob@test.com",   "username": "bob"},
    {"id": 3, "email": "carol@test.com", "username": "carol"},
]


def test_ping(pg_adapter : PostgresAdapter):
    pg_adapter.ping()


def test_get_tables(pg_adapter: PostgresAdapter):
    tables = pg_adapter.get_tables()
    assert "users" in tables


def test_get_columns(pg_adapter: PostgresAdapter):
    columns = pg_adapter.get_columns("users")
    names = [c.name for c in columns]
    assert "id" in names
    assert "email" in names
    assert "username" in names


def test_insert_and_fetch(pg_adapter: PostgresAdapter):
    pg_adapter.insert("users", SAMPLE_ROWS)
    result = pg_adapter.fetch("users", ["id", "email", "username"])
    assert len(result) == 3


def test_fetch_specific_columns(pg_adapter: PostgresAdapter):
    pg_adapter.insert("users", SAMPLE_ROWS)
    result = pg_adapter.fetch("users", ["email"])
    assert all(len(row) == 1 for row in result)


def test_insert_empty_rows(pg_adapter: PostgresAdapter):
    pg_adapter.insert("users", [])
    result = pg_adapter.fetch("users", ["id"])
    assert len(result) == 0


def test_insert_batch(pg_adapter: PostgresAdapter):
    rows = [{"id": i, "email": f"user{i}@test.com", "username": f"user{i}"} for i in range(1, 502)]
    pg_adapter.insert("users", rows, batch_size=200)
    result = pg_adapter.fetch("users", ["id"])
    assert len(result) == 501
    
def test_fetch_unknown_column(postgres_adapter: PostgresAdapter):
    with pytest.raises(ValueError, match="does not exist"):
        postgres_adapter.fetch("users", ["nonexistent"])


def test_fetch_unknown_table(postgres_adapter: PostgresAdapter):
    with pytest.raises(ValueError, match="does not exist"):
        postgres_adapter.fetch("nonexistent", ["id"])
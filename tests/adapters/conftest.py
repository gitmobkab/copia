import os
import pytest
from copia.adapters.mysql_adapter import MySQLAdapter
from copia.adapters.postgres_adapter import PostgresAdapter


@pytest.fixture(scope="module")
def mysql_adapter():
    adapter = MySQLAdapter(
        host=os.environ.get("COPIA_TEST_MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("COPIA_TEST_MYSQL_PORT", 3306)),
        database=os.environ.get("COPIA_TEST_MYSQL_DB", "copia_test"),
        user=os.environ.get("COPIA_TEST_MYSQL_USER", "root"),
        password=os.environ.get("COPIA_TEST_MYSQL_PASSWORD", "root"),
    )
    yield adapter
    adapter.close()


@pytest.fixture(scope="module")
def pg_adapter():
    adapter = PostgresAdapter(
        host=os.environ.get("COPIA_TEST_PG_HOST", "127.0.0.1"),
        port=int(os.environ.get("COPIA_TEST_PG_PORT", 5432)),
        database=os.environ.get("COPIA_TEST_PG_DB", "copia_test"),
        user=os.environ.get("COPIA_TEST_PG_USER", "postgres"),
        password=os.environ.get("COPIA_TEST_PG_PASSWORD", "root"),
    )
    yield adapter
    adapter.close()


@pytest.fixture(autouse=True)
def clean_users(mysql_adapter, pg_adapter):
    yield
    mysql_adapter._connection.cursor().execute("DELETE FROM users")
    mysql_adapter._connection.commit()
    pg_adapter._connection.execute("DELETE FROM users")
    pg_adapter._connection.commit()
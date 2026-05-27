import pytest

from copia.runners import generate_rows
from copia.generators import GeneratorValueError

from .utils import make_column


def test_generate_rows_basic():
    columns = [
        make_column("uuid", name="id"),
        make_column("username", name="name"),
    ]
    rows = list(generate_rows(None, columns, 5))
    assert len(rows) == 5
    assert all("id" in row and "name" in row for row in rows)

def test_generate_rows_zero_raises():
    with pytest.raises(ValueError):
        list(generate_rows(None, [], 0))

def test_fetch_without_adapter_raises():
    columns = [make_column("fetch", name="user_id", positionals=["users.id"])]
    with pytest.raises(ValueError):
        list(generate_rows(None, columns, 5))
        
def test_unique_rows():
    columns = [make_column("uuid", name="id", unique=True)]
    rows = list(generate_rows(None, columns, 100))
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)), "Generated IDs are not unique"
    
def test_unique_rows_exhaustion():
    columns = [make_column("enum", name="id", positionals=["a", "b", "c"], unique=True)]
    with pytest.raises(GeneratorValueError):
        list(generate_rows(None, columns, 5)) # Clearly more than 3 unique values available
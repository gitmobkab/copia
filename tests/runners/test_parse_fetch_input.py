from typing import TypedDict

import pytest

from copia.generators import GeneratorValueError
from copia.runners import _parse_fetch_input


class FetchTest(TypedDict):
    input: str
    output: tuple[str, str]
    
valid_formats : list[FetchTest] = [
    {
        "input": "db.table", 
        "output": ("db", "table")
    },
    {
        "input": "db.\t\t table",
        "output": ("db", "\t\t table")
    },
    {
        "input": "db.DROP TABLE users",
        "output": ("db", "DROP TABLE users")
    },
    {
        "input": "youtube. \v\t\t Coffeezilla ",
        "output": ("youtube", " \v\t\t Coffeezilla ")
    }
]

@pytest.mark.parametrize("test", valid_formats)
def test_parse_ref_valid_formats(test: FetchTest):
    assert test["output"] == _parse_fetch_input(test["input"])  

invalid_formats = [
    "db.", 
    "db.\t\t",
    "db. ",
    ".col",
    ". \t",
    "\t.\t",
    ".",
    "db.table.column",
    " \t"
    ""
]

@pytest.mark.parametrize("test", invalid_formats)
def test_parse_ref_invalid_formats(test: str):      
    with pytest.raises(GeneratorValueError):
        _parse_fetch_input(test)
from typing import Any, Generator, TypeAlias
from random import choice
from copia.parser.models import Column, GeneratorCall
from copia.generators import GENERATORS_REGISTRY, GeneratorValueError

from sqlalchemy import Connection, text

REF_COLLECTION : TypeAlias = dict[str, dict[str, list]]


def generate_rows(connection: Connection, columns: list[Column], rows: int) -> Generator[dict[str, Any], Any, None]:
    if rows <= 0:
        raise ValueError("Expected an integer above 0 for the number of rows,"
                         f"got {rows}")
    refs = build_refs(connection, columns)
    for _ in range(rows):
        yield generate_row(columns, refs)

def generate_row(columns: list[Column], refs : REF_COLLECTION) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for index, column in enumerate(columns, start=1):
        result = run_column(column, refs)
        normalized_column_name = column.name or f"Anonym {index}"
        results[normalized_column_name] = result
    return results


def run_column(column: Column, refs: REF_COLLECTION) -> Any:
    generator_name = column.generator.name
    if generator_name == "ref":
        return run_ref(column.generator, refs)
    generator_func = GENERATORS_REGISTRY[generator_name]
    params = column.generator.params
    return generator_func(*params.positionals, **params.named)

def run_ref(ref_call: GeneratorCall, refs: REF_COLLECTION) -> Any:
    table, column = _get_ref_data(ref_call)
    ref_choices = refs[table][column]
    if ref_choices:
        return choice(ref_choices)
    raise GeneratorValueError(f"No values found in db at {table!r}.{column!r}", "ref")
    
def build_refs(connection: Connection, columns: list[Column]) -> REF_COLLECTION:
    refs = _initialize_refs(columns)
    return _populate_refs(connection, refs)

def _initialize_refs(columns: list[Column]) -> REF_COLLECTION:
    refs: REF_COLLECTION = {}
    for column in columns:
        if column.generator.name != "ref":
            continue
        table_name, column_name = _get_ref_data(column.generator)
        if table_name not in refs:
            refs[table_name] = {}
        refs[table_name][column_name] = []
    return refs
        
def _populate_refs(connection: Connection, refs: REF_COLLECTION) -> REF_COLLECTION:
    for table, columns in refs.items():
        columns_str = ", ".join(columns.keys())
        query = f"SELECT {columns_str} FROM {table}"
        try:
            rows = connection.execute(text(query)).fetchall()
        except Exception as err:
            raise GeneratorValueError(str(err), "ref")
        for row in rows:
            for col, val in zip(columns.keys(), row):
                refs[table][col].append(val)
    return refs


def _get_ref_data(ref_call: GeneratorCall) -> tuple[str, str]:
    if ref_call.params.positionals:
        ref_input = ref_call.params.positionals[0]
    else:
        for value in ref_call.params.named.values(): 
            ref_input = value
            continue

    return _parse_ref_input(ref_input) # type: ignore
    # count the invariants with me 🗣️🗣️ 🔥🔥
        
        
def _parse_ref_input(ref_input: str) -> tuple[str, str]:
    content = ref_input.split(".")
    if len(content) != 2 or not all(content):
        raise GeneratorValueError("expected reference to match format 'table.column'", "ref")
    return content[0], content[1]

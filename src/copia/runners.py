from typing import Any, Callable, Generator, TypeAlias
from random import choice

from copia.parser.models import Column, GeneratorCall
from copia.generators import GENERATORS_REGISTRY, GeneratorValueError
from copia.adapters import BaseAdapter

DBDataCollection: TypeAlias = dict[str,
                                 dict[
                                    str, list
                                 ]
                                 ]

GeneratedRow: TypeAlias = dict[str, Any]


def generate_rows(
    adapter: BaseAdapter | None,
    columns: list[Column],
    rows: int,
    on_column_done: Callable[[str, list[Any]], None] | None = None,
) -> Generator[GeneratedRow, None, None]:
    if rows <= 0:
        raise ValueError(f"Expected an integer above 0 for the number of rows, got {rows}")
    refs = {}
 
    columns_names = [column.name for column in columns]
    if adapter:
        refs = build_refs(adapter, columns)
    elif adapter is None and "fetch" in columns_names:
        raise ValueError("Cannot use generator 'fetch' without a database connection")
    columns_data = _generate_columns(columns, rows, refs, on_column_done)
    keys = list(columns_data.keys())
    for values in zip(*columns_data.values()):
        yield dict(zip(keys, values))


def _generate_columns(
    columns: list[Column],
    rows: int,
    refs: DBDataCollection,
    on_column_done: Callable[[str, list[Any]], None] | None = None,
) -> dict[str, list[Any]]:
    result: dict[str, list[Any]] = {}
    for index, column in enumerate(columns, start=1):
        name = column.name or f"Anonym {index}"
        if column.unique_constraint:
            values = _generate_unique_values(column, refs, rows)
        else:
            values = [run_column(column, refs) for _ in range(rows)]
        result[name] = values
        if on_column_done:
            on_column_done(name, values)
    return result

def _generate_unique_values(column: Column, refs: DBDataCollection, rows: int, max_attempts: int = 1000):
    seen = set()
    values = []
    for _ in range(rows):
        for _ in range(max_attempts):
            value = run_column(column, refs)
            if value not in seen:
                seen.add(value)
                values.append(value)
                break
        else:
            column_name = column.name or "<Anonym column>"
            raise GeneratorValueError(
                f"Exhausted unique values for column {column_name!r}",
                column.generator.name
            )
    return values

def run_column(column: Column, refs: DBDataCollection) -> Any:
    generator_name = column.generator.name
    if generator_name == "fetch":
        return run_fetch(column.generator, refs)
    generator_func = GENERATORS_REGISTRY[generator_name]
    params = column.generator.params
    return generator_func(*params.positionals, **params.named)


def run_fetch(ref_call: GeneratorCall, refs: DBDataCollection) -> Any:
    table, column = _get_ref_data(ref_call)
    ref_choices = refs[table][column]
    if ref_choices:
        return choice(ref_choices)
    raise GeneratorValueError(f"No values found in db at {table!r}.{column!r}", "fetch")


def build_refs(adapter: BaseAdapter, columns: list[Column]) -> DBDataCollection:
    refs = _initialize_refs(columns)
    return _populate_refs(adapter, refs)

def _initialize_refs(columns: list[Column]) -> DBDataCollection:
    refs: DBDataCollection = {}
    for column in columns:
        if column.generator.name != "fetch":
            continue
        table_name, column_name = _get_ref_data(column.generator)
        if table_name not in refs:
            refs[table_name] = {}
        refs[table_name][column_name] = []
    return refs
        
def _populate_refs(adapter: BaseAdapter, refs: DBDataCollection) -> DBDataCollection:
    for table, columns in refs.items():
        try:
            rows = adapter.fetch(table, list(columns.keys()))
        except Exception as err:
            raise GeneratorValueError(str(err), "fetch")
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
        raise GeneratorValueError("expected reference to match format 'table.column'", "fetch")
    return content[0], content[1]
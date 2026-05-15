from typing import Literal, TypeAlias
from .types import Formatter

from .csv_formatter import format_to_csv
from .json_formatter import format_to_json
from .sql_formatter import format_to_sql

FormatterId: TypeAlias = Literal['csv','json', 'sql']

REGISTERED_FORMATTERS: dict[FormatterId, Formatter] = {
    'csv': format_to_csv,
    'json': format_to_json,
    'sql': format_to_sql
}

def get_formatter(formatter_id: FormatterId):
    try:
        return REGISTERED_FORMATTERS[formatter_id]
    except KeyError:
        raise ValueError(f'Unknown formatter {formatter_id!r}')
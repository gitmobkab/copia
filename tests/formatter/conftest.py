import pytest
from copia.generators import GENERATORS_REGISTRY

from copia.generators.misc import enum
from copia.runners import GeneratedRow

GENERATOR_DEFAULTS = {
    "fetch": None,
    "enum": lambda: enum("a", "b", "c"),
}

@pytest.fixture()
def test_values(size: int = 20) -> list[GeneratedRow]:
    rows: list[GeneratedRow] = []
    for _ in range(size):
        row = build_row()
        rows.append(row)
    return rows

def build_row() -> GeneratedRow:
    """Build a row with all registered generators

    Returns:
        GeneratedRow: the generated row {generator_name: generated_value, ...}
    """
    row: GeneratedRow = {}
    for name, generator in GENERATORS_REGISTRY.items():
        if name in GENERATOR_DEFAULTS:
            default_generator = GENERATOR_DEFAULTS[name]
            if default_generator is None:
                continue
            result = default_generator()
        else:
            result = generator()
        row[name] = result
    return row

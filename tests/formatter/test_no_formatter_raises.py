import pytest

from copia.formatters import REGISTERED_FORMATTERS
    
@pytest.mark.parametrize("name,formatter", REGISTERED_FORMATTERS.items())
def test_formatter_no_exception(name, formatter, test_values):
    for _ in formatter(test_values):
        pass
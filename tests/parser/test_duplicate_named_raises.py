import pytest

from copia.parser.parser import parse
from copia.parser.exceptions import DuplicateNamedParamException


class TestDuplicateNamedParam:
    def test_duplicate_key_raises(self):
        with pytest.raises(DuplicateNamedParamException):
            parse(":gen(safe=True, safe=False)")

    def test_duplicate_key_non_adjacent_raises(self):
        with pytest.raises(DuplicateNamedParamException):
            parse(':email(domain="gmail.com", safe=True, domain=".com")')
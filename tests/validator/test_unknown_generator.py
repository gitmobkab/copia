from utils import make_call, VALIDATOR
import pytest
from copia.validator.exceptions import UnknownGeneratorException

class TestUnknownGenerator:
    def test_unknown_name_raises(self):
        call = make_call("does_not_exist")
        with pytest.raises(UnknownGeneratorException):
            VALIDATOR.validate(call)

    def test_known_name_does_not_raise(self):
        call = make_call("fake_name")
        VALIDATOR.validate(call)

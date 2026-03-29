from utils import make_call, VALIDATOR

import pytest

from copia.validator.validator import UnknownNamedParamException

class TestUnknownNamedParam:
    def test_unknown_key_raises(self):
        call = make_call("fake_name", named={"typo": "fr"})
        with pytest.raises(UnknownNamedParamException):
            VALIDATOR.validate(call)

    def test_known_key_does_not_raise(self):
        call = make_call("fake_name", named={"locale": "fr"})
        VALIDATOR.validate(call)

    def test_multiple_named_one_unknown_raises(self):
        call = make_call("fake_float", named={"min": 0.0, "max": 1.0, "typo": 2})
        with pytest.raises(UnknownNamedParamException):
            VALIDATOR.validate(call)


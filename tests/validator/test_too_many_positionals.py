from tests.validator.utils import make_call, VALIDATOR

import pytest

from copia.validator.exceptions import TooManyPositionalsException

class TestTooManyPositionals:
    def test_too_many_raises(self):
        # fake_int has 2 params, giving 3
        call = make_call("fake_int", positionals=[0, 45, 99])
        with pytest.raises(TooManyPositionalsException):
            VALIDATOR.validate(call)

    def test_exact_count_does_not_raise(self):
        call = make_call("fake_int", positionals=[0, 45])
        VALIDATOR.validate(call)

    def test_less_than_max_does_not_raise(self):
        # fake_float has 3 params, giving 2 — third has default
        call = make_call("fake_float", positionals=[0.0, 1.0])
        VALIDATOR.validate(call)

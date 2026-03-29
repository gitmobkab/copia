from utils import make_call, VALIDATOR

import pytest

from copia.validator.exceptions import PositionalNamedCollisionException



class TestPositionalNamedCollision:
    def test_first_param_collision_raises(self):
        # fake_int(min, max) — min covered by positional and named
        call = make_call("fake_int", positionals=[0], named={"min": 5, "max": 10})
        with pytest.raises(PositionalNamedCollisionException):
            VALIDATOR.validate(call)

    def test_second_param_collision_raises(self):
        # both covered by positionals, max also in named
        call = make_call("fake_int", positionals=[0, 45], named={"max": 99})
        with pytest.raises(PositionalNamedCollisionException):
            VALIDATOR.validate(call)

    def test_no_collision_does_not_raise(self):
        # fake_float(min, max, precision) — min/max by positional, precision by named
        call = make_call("fake_float", positionals=[0.0, 1.0], named={"precision": 3})
        VALIDATOR.validate(call)

    def test_named_only_no_collision_does_not_raise(self):
        call = make_call("fake_int", named={"min": 0, "max": 45})
        VALIDATOR.validate(call)
    
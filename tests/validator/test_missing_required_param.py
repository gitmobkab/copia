from tests.validator.utils import make_call, VALIDATOR

import pytest

from copia.validator.exceptions import MissingRequiredParamException


class TestMissingRequiredParam:
    def test_no_params_for_required_raises(self):
        # fake_int requires min and max
        call = make_call("fake_int")
        with pytest.raises(MissingRequiredParamException):
            VALIDATOR.validate(call)

    def test_partial_positionals_raises(self):
        # fake_int requires 2, giving 1
        call = make_call("fake_int", positionals=[0])
        with pytest.raises(MissingRequiredParamException):
            VALIDATOR.validate(call)

    def test_optional_not_provided_does_not_raise(self):
        # fake_name has locale with default "en"
        call = make_call("fake_name")
        VALIDATOR.validate(call)

    def test_required_covered_by_named_does_not_raise(self):
        call = make_call("fake_int", named={"min": 0, "max": 45})
        VALIDATOR.validate(call)

    def test_required_covered_by_mix_does_not_raise(self):
        # fake_int(min, max) — min by positional, max by named
        call = make_call("fake_int", positionals=[0], named={"max": 45})
        VALIDATOR.validate(call)

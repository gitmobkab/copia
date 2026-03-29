from utils import make_call, VALIDATOR

import pytest

from copia.validator.exceptions import TypeMismatchException


class TestTypeMismatch:
    def test_wrong_positional_type_raises(self):
        # fake_int expects int, int — giving str, int
        call = make_call("fake_int", positionals=["oops", 45])
        with pytest.raises(TypeMismatchException):
            VALIDATOR.validate(call)

    def test_wrong_named_type_raises(self):
        # fake_name expects locale: str — giving int
        call = make_call("fake_name", named={"locale": 42})
        with pytest.raises(TypeMismatchException):
            VALIDATOR.validate(call)

    def test_correct_positional_types_do_not_raise(self):
        call = make_call("fake_int", positionals=[0, 45])
        VALIDATOR.validate(call)

    def test_correct_named_type_does_not_raise(self):
        call = make_call("fake_float", positionals=[0.0, 1.0], named={"precision": 3})
        VALIDATOR.validate(call)

    def test_literal_valid_value_does_not_raise(self):
        call = make_call("fake_choice", positionals=["a"])
        VALIDATOR.validate(call)

    def test_literal_invalid_value_raises(self):
        call = make_call("fake_choice", positionals=["z"])
        with pytest.raises(TypeMismatchException):
            VALIDATOR.validate(call)

    def test_unannotated_params_do_not_raise(self):
        # fake_no_annotations has no type hints — anything goes
        call = make_call("fake_no_annotations", positionals=["anything", 42])
        VALIDATOR.validate(call)


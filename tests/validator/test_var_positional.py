from tests.validator.utils import make_call, VALIDATOR

import pytest

from copia.validator.exceptions import TypeMismatchException



class TestVarPositional:
    def test_many_positionals_does_not_raise(self):
        call = make_call("fake_enum", positionals=["a", "b", "c", "d"])
        VALIDATOR.validate(call)

    def test_keyword_only_after_var_positional(self):
        call = make_call("fake_racist_picker", positionals=["a", "b"], named={"racism": True})
        VALIDATOR.validate(call)

    def test_wrong_keyword_only_type_raises(self):
        call = make_call("fake_racist_picker", positionals=["a"], named={"racism": "oops"})
        with pytest.raises(TypeMismatchException):
            VALIDATOR.validate(call)
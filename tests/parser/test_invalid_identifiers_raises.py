import pytest
from lark import UnexpectedInput

from copia.parser.parser import parse

class TestInvalidIdentifiers:
    # --- Column names ---

    def test_column_name_starting_with_digit_raises(self):
        with pytest.raises(UnexpectedInput):
            parse("1username:name")

    def test_column_name_with_hyphen_raises(self):
        with pytest.raises(UnexpectedInput):
            parse("user-name:name")

    def test_column_name_with_space_raises(self):
        with pytest.raises(UnexpectedInput):
            parse("user name:name")

    def test_column_name_with_special_char_raises(self):
        with pytest.raises(UnexpectedInput):
            parse("user@name:name")

    # --- Generator names ---

    def test_generator_name_starting_with_digit_raises(self):
        with pytest.raises(UnexpectedInput):
            parse(":1int")

    def test_generator_name_with_hyphen_raises(self):
        with pytest.raises(UnexpectedInput):
            parse(":my-gen")

    def test_generator_name_with_special_char_raises(self):
        with pytest.raises(UnexpectedInput):
            parse(":gen!")

    # --- Named param keys ---

    def test_named_key_starting_with_digit_raises(self):
        with pytest.raises(UnexpectedInput):
            parse(":gen(1key=5)")

    def test_named_key_with_hyphen_raises(self):
        with pytest.raises(UnexpectedInput):
            parse(":gen(my-key=5)")
import pytest
from lark import UnexpectedInput

from copia.parser.parser import parse



class TestInvalidSyntax:
    def test_identifier_start_with_illegal_char_raises(self):
        tests = [
            "1badIdentifier:int()",
            "$illegal_too:rand()",
            "user=name:float()"
        ]
        with pytest.raises(UnexpectedInput):
            parse("1badIdentifier:int()")
            
    
    def test_unquoted_string_raises(self):
        with pytest.raises(UnexpectedInput):
            parse(":gen(hello)")

    def test_named_before_positional_raises(self):
        # grammar enforces positionals first
        with pytest.raises(UnexpectedInput):
            parse(":gen(max=45, 0)")

    def test_missing_colon_raises(self):
        with pytest.raises(UnexpectedInput):
            parse("username")

    def test_empty_input_raises(self):
        with pytest.raises(UnexpectedInput):
            parse("")
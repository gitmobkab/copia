from copia.parser.parser import parse
from copia.parser.models import Column, GeneratorCall, Params

# --- Happy path ---

class TestBasicParsing:
    def test_simple_column_no_params(self):
        result = parse("username:name()")
        assert result == [
            Column("username", 
                   False, 
                   GeneratorCall("name", Params([], {})))
        ]

    def test_anonymous_column(self):
        result = parse(":int()")
        assert result == [
            Column(None, 
                   False, 
                   GeneratorCall("int", Params([], {})))
        ]

    def test_multiple_columns_no_param(self):
        result = parse("age:unique int() username:name()")
        assert result == [
            Column("age",
                   True, 
                   GeneratorCall("int", Params([], {}))),
            
            Column("username",
                   False,
                   GeneratorCall("name", Params([], {}))),
        ]

    def test_empty_parentheses(self):
        result = parse("age: unique int()")
        assert result == [
            Column("age", 
                   True,
                   GeneratorCall("int", Params([], {})))
        ]
from copia.parser.parser import parse
from copia.parser.models import GeneratorCall, Column, Params


class TestNamed:
    def test_single_named_string(self):
        result = parse(':email(domain="gmail.com")')
        assert result == [
            Column(None, GeneratorCall("email", Params([], {"domain": "gmail.com"})))
        ]

    def test_single_named_int(self):
        result = parse(":text(size=500)")
        assert result == [
            Column(None, GeneratorCall("text", Params([], {"size": 500})))
        ]

    def test_named_bool(self):
        result = parse(":gen(safe=true)")
        assert result == [
            Column(None, GeneratorCall("gen", Params([], {"safe": True})))
        ]

    def test_multiple_named(self):
        result = parse(':email(domain="gmail.com", safe=True)')
        assert result == [
            Column(None, GeneratorCall("email", Params([], {"domain": "gmail.com", "safe": True})))
        ]

    def test_whitespace_around_equals(self):
        result = parse(":text( size = 500 )")
        assert result == [
            Column(None, GeneratorCall("text", Params([], {"size": 500})))
        ]


from copia.parser.parser import parse
from copia.parser.models import Column, GeneratorCall, Params


class TestMixed:
    def test_positionals_and_named(self):
        result = parse(":int(0, max=45)")
        assert result == [
            Column(None, GeneratorCall("int", Params([0], {"max": 45})))
        ]

    def test_complex_multi_column(self):
        result = parse(':email(domain="gmail.com") lore:text(size=500)')
        assert result == [
            Column(None, GeneratorCall("email", Params([], {"domain": "gmail.com"}))),
            Column("lore", GeneratorCall("text", Params([], {"size": 500})))
        ]

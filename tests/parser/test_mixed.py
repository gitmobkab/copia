from copia.parser.parser import parse
from copia.parser.models import Column, GeneratorCall, Params


class TestMixed:
    def test_positionals_and_named(self):
        result = parse(":int(0, max=45)")
        assert result == [
            Column(None,
                   False,
                   GeneratorCall("int", Params([0], {"max": 45})))
        ]

    def test_complex_multi_column(self):
        result = parse(':unique email(domain="gmail.com") lore: unique text(size=500)')
        assert result == [
            Column(None, 
                   True,
                   GeneratorCall("email", Params([], {"domain": "gmail.com"}))),
            
            Column("lore",
                   True,
                   GeneratorCall("text", Params([], {"size": 500})))
        ]

from copia.parser.parser import parse
from copia.parser.models import GeneratorCall, Column, Params

class TestPositionals:
    def test_single_int_positional(self):
        result = parse(":int(14)")
        assert result == [
            Column(None, GeneratorCall("int", Params([14], {})))
        ]

    def test_two_int_positionals(self):
        result = parse(":int(0, 45)")
        assert result == [
            Column(None, GeneratorCall("int", Params([0, 45], {})))
        ]

    def test_float_positional(self):
        result = parse(":float(4.5)")
        assert result == [
            Column(None, GeneratorCall("float", Params([4.5], {})))
        ]

    def test_negative_int(self):
        result = parse(":int(-10, 10)")
        assert result == [
            Column(None, GeneratorCall("int", Params([-10, 10], {})))
        ]

    def test_negative_float(self):
        result = parse(":float(-1.5, 1.5)")
        assert result == [
            Column(None, GeneratorCall("float", Params([-1.5, 1.5], {})))
        ]

    def test_bool_positional_true(self):
        result = parse(":gen(True, true)")
        assert result == [
            Column(None, GeneratorCall("gen", Params([True, True], {})))
        ]

    def test_bool_positional_false(self):
        result = parse(":gen(false, False)")
        assert result == [
            Column(None, GeneratorCall("gen", Params([False, False], {})))
        ]

    def test_string_double_quoted(self):
        result = parse(':email(domain="gmail.com")')
        # domain is named here, tested separately — this is a string type check
        result = parse(':gen("hello")')
        assert result == [
            Column(None, GeneratorCall("gen", Params(["hello"], {})))
        ]

    def test_string_single_quoted(self):
        result = parse(":gen('hello')")
        assert result == [
            Column(None, GeneratorCall("gen", Params(["hello"], {})))
        ]

    def test_empty_string(self):
        result = parse(":gen('')")
        assert result == [
            Column(None, GeneratorCall("gen", Params([""], {})))
        ]

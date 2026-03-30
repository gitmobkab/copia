from tests.cli.config.models.utils import make_profile


class TestStr:
    def test_str_format(self):
        p = make_profile(adapter="mysql", host="localhost", port=3306)
        assert str(p) == "(mysql) <localhost:3306>"

    def test_repr_equals_str(self):
        p = make_profile()
        assert repr(p) == str(p)


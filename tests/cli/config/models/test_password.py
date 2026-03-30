from copia.cli.config import Profile

from tests.cli.config.models.utils import make_profile, VALID_PROFILE


class TestPassword:
    def test_valid_password(self):
        assert make_profile(password="s3cr3t!").password == "s3cr3t!"

    def test_empty_password_is_allowed(self):
        assert make_profile(password="").password == ""

    def test_password_defaults_to_empty(self):
        data = {k: v for k, v in VALID_PROFILE.items() if k != "password"}
        assert Profile(**data).password == ""

    def test_password_with_special_chars(self):
        pw = "p@ss/w0rd! #$%^&*()"
        assert make_profile(password=pw).password == pw

    def test_password_with_emoji(self):
        pw = "pass🔑word"
        assert make_profile(password=pw).password == pw

    def test_password_with_spaces(self):
        pw = "PassW0R!D. "
        assert make_profile(password=pw).password == pw

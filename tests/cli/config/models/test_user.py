import pytest
from pydantic import ValidationError

from tests.cli.config.models.utils import make_profile


class TestUser:
    def test_valid_user(self):
        assert make_profile(user="admin").user == "admin"

    def test_empty_user(self):
        with pytest.raises(ValidationError):
            make_profile(user="")

    def test_non_ascii_user(self):
        with pytest.raises(ValidationError):
            make_profile(user="üser")

    def test_emoji_user(self):
        with pytest.raises(ValidationError):
            make_profile(user="user🔑")

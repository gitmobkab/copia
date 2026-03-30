import pytest
from pydantic import ValidationError

from tests.cli.config.models.utils import make_profile


class TestDatabase:
    def test_valid_database(self):
        assert make_profile(database="my_db").database == "my_db"

    def test_empty_database(self):
        with pytest.raises(ValidationError):
            make_profile(database="")

    def test_non_ascii_database(self):
        with pytest.raises(ValidationError):
            make_profile(database="db_café")

    def test_emoji_database(self):
        with pytest.raises(ValidationError):
            make_profile(database="db🎉")

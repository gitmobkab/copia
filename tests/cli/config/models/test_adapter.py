import pytest
from pydantic import ValidationError

from tests.cli.config.models.utils import make_profile



class TestAdapter:
    def test_canonical_adapters(self):
        assert make_profile(adapter="mysql").adapter == "mysql"
        assert make_profile(adapter="postgres").adapter == "postgres"

    def test_invalid_adapter(self):
        with pytest.raises(ValidationError):
            make_profile(adapter="sqlite")

    def test_empty_adapter(self):
        with pytest.raises(ValidationError):
            make_profile(adapter="")

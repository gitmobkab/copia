import pytest
from pydantic import ValidationError

from tests.cli.config.models.utils import make_profile


class TestPort:
    def test_valid_port(self):
        assert make_profile(port=5432).port == 5432

    def test_min_port(self):
        assert make_profile(port=1).port == 1

    def test_max_port(self):
        assert make_profile(port=65535).port == 65535

    def test_port_below_min(self):
        with pytest.raises(ValidationError):
            make_profile(port=0)

    def test_port_above_max(self):
        with pytest.raises(ValidationError):
            make_profile(port=65536)

    def test_port_as_string_rejected(self):
        with pytest.raises(ValidationError):
            make_profile(port="3306")

    def test_port_as_float_rejected(self):
        with pytest.raises(ValidationError):
            make_profile(port=3306.0)

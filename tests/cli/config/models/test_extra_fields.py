import pytest
from pydantic import ValidationError

from tests.cli.config.models.utils import make_profile



class TestExtraFields:
    def test_extra_field_forbidden(self):
        with pytest.raises(ValidationError):
            make_profile(unknown_field="value")
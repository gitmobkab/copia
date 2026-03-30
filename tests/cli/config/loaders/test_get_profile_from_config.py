import pytest

from tests.cli.config.loaders.utils import VALID_PROFILE_DATA

from copia.cli.config.loaders import get_profile_from_config
from copia.cli.config import(
    Profile,
    ProfilesKeyIsNotATableError,
    ProfileNotFoundError,
    FoundProfileIsNotATableError,
    InvalidProfileError
)

class TestGetProfileFromConfig:
    def test_valid_profile(self):
        config = {"profiles": {"dev": VALID_PROFILE_DATA}}
        profile = get_profile_from_config("dev", config)
        assert isinstance(profile, Profile)
        assert profile.adapter == "mysql"

    def test_no_profiles_key_raises_not_found(self):
        with pytest.raises(ProfileNotFoundError):
            get_profile_from_config("dev", {})

    def test_profiles_is_list_raises_not_a_table(self):
        config = {"profiles": [VALID_PROFILE_DATA]}
        with pytest.raises(ProfilesKeyIsNotATableError):
            get_profile_from_config("dev", config)

    def test_profiles_is_string_raises_not_a_table(self):
        config = {"profiles": "not_a_dict"}
        with pytest.raises(ProfilesKeyIsNotATableError):
            get_profile_from_config("dev", config)

    def test_profile_not_found(self):
        config = {"profiles": {"prod": VALID_PROFILE_DATA}}
        with pytest.raises(ProfileNotFoundError):
            get_profile_from_config("dev", config)

    def test_profile_is_string_raises_found_profile_not_a_table(self):
        config = {"profiles": {"dev": "not_a_table"}}
        with pytest.raises(FoundProfileIsNotATableError) as exc_info:
            get_profile_from_config("dev", config)
        assert exc_info.value.profile_name == "dev"

    def test_profile_is_list_raises_found_profile_not_a_table(self):
        config = {"profiles": {"dev": [1, 2, 3]}}
        with pytest.raises(FoundProfileIsNotATableError):
            get_profile_from_config("dev", config)

    def test_invalid_profile_data(self):
        config = {
            "profiles": {
                "dev": {
                    "adapter": "bad",
                    "host": "",
                    "port": 0,
                    "database": "",
                    "user": "",
                }
            }
        }
        with pytest.raises(InvalidProfileError):
            get_profile_from_config("dev", config)

    def test_profile_missing_required_field(self):
        incomplete = {k: v for k, v in VALID_PROFILE_DATA.items() if k != "host"}
        config = {"profiles": {"dev": incomplete}}
        with pytest.raises(InvalidProfileError):
            get_profile_from_config("dev", config)

    def test_extra_field_in_profile_raises(self):
        config = {"profiles": {"dev": {**VALID_PROFILE_DATA, "unknown": "value"}}}
        with pytest.raises(InvalidProfileError):
            get_profile_from_config("dev", config)

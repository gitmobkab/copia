import pytest

from tests.cli.config.loaders.utils import VALID_TOML, RESOLVE_CONGIG_PATH_IMPORT_STRING, write_toml

from copia.cli.config import (
    get_profile,
    Profile,
    ProfileNotFoundError,
    InvalidConfigError
)

class TestGetProfile:
    def test_valid_profile(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", VALID_TOML)
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        profile = get_profile("dev", "local")
        assert isinstance(profile, Profile)

    def test_not_found_raises(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", "[profiles]\n")
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        with pytest.raises(ProfileNotFoundError):
            get_profile("dev", "local")

    def test_invalid_config_raises(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", "not valid ][")
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        with pytest.raises(InvalidConfigError):
            get_profile("dev", "local")

    def test_file_not_found_raises(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            RESOLVE_CONGIG_PATH_IMPORT_STRING,
            lambda _: tmp_path / "missing.toml",
        )
        with pytest.raises(FileNotFoundError):
            get_profile("dev", "local")

    def test_global_scope(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", VALID_TOML)
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        profile = get_profile("dev", "global")
        assert isinstance(profile, Profile)
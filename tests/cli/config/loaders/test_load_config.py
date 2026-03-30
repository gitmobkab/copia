import pytest

from copia.cli.config.loaders import load_config
from copia.cli.config.exceptions import InvalidConfigError

from tests.cli.config.loaders.utils import write_toml, VALID_TOML, RESOLVE_CONGIG_PATH_IMPORT_STRING


class TestLoadConfig:
    def test_valid_config(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", VALID_TOML)
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        result = load_config("local")
        assert "profiles" in result

    def test_file_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            RESOLVE_CONGIG_PATH_IMPORT_STRING,
            lambda _: tmp_path / "missing.toml",
        )
        with pytest.raises(FileNotFoundError):
            load_config("local")

    def test_invalid_toml(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", "not valid ][")
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        with pytest.raises(InvalidConfigError):
            load_config("local")

    def test_permission_error(self, tmp_path, monkeypatch):
        f = write_toml(tmp_path / "config.toml", VALID_TOML)
        f.chmod(0o000)
        monkeypatch.setattr(RESOLVE_CONGIG_PATH_IMPORT_STRING, lambda _: f)
        try:
            with pytest.raises(PermissionError):
                load_config("local")
        finally:
            f.chmod(0o644)
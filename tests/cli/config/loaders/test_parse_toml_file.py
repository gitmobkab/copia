import tomllib
import pytest


from tests.cli.config.loaders.utils import VALID_TOML, write_toml
from copia.cli.config.loaders import parse_toml_file


class TestParseTomlFile:
    def test_valid_toml(self, tmp_path):
        f = write_toml(tmp_path / "config.toml", VALID_TOML)
        result = parse_toml_file(f)
        assert "profiles" in result

    def test_invalid_toml_raises(self, tmp_path):
        f = write_toml(tmp_path / "config.toml", "not valid toml ][")
        with pytest.raises(tomllib.TOMLDecodeError):
            parse_toml_file(f)

    def test_file_not_found_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_toml_file(tmp_path / "missing.toml")

    def test_empty_toml_returns_empty_dict(self, tmp_path):
        f = write_toml(tmp_path / "config.toml", "")
        assert parse_toml_file(f) == {}
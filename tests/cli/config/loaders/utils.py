from pathlib import Path

VALID_PROFILE_DATA = {
    "adapter": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "mydb",
    "user": "admin",
    "password": "secret",
}

VALID_TOML = """\
[profiles.dev]
adapter = "mysql"
host = "localhost"
port = 3306
database = "mydb"
user = "admin"
password = "secret"
"""

RESOLVE_CONGIG_PATH_IMPORT_STRING = "copia.cli.config.loaders.resolve_config_path"

def write_toml(path: Path, content: str) -> Path:
    path.touch()
    path.write_text(content)
    return path
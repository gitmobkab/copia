"""All the CONSTANTS shared by the copia cli"""
from typing import Literal
from pathlib import Path

from typer import get_app_dir


APP_NAME = "copia"
APP_DIR = get_app_dir(APP_NAME)
LOCAL_COPIA_FILE = Path(".copia.toml")
GLOBAL_COPIA_FILE = Path(APP_DIR) / "profiles.toml"
PORT_MIN_VAL = 1
PORT_MAX_VAL = 65535
SUPPORTED_ADAPTERS = Literal['mysql', "postgres"]
CONFIG_SCOPES = Literal["local", "global"]

# -- LINKS AND RESOURCES ---
COPIA_CONFIG_FILE_DOC_LINK = "https://github.com/gitmobkab/copia/docs/config_file.md"
COPIA_CONFIG_FILE_SCHEME = "https://github.com/gitmobkab/copia/configFileScheme.json"
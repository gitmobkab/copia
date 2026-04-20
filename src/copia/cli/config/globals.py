"""All the CONSTANTS shared by the copia config module"""
from typing import Literal
from pathlib import Path

from typer import get_app_dir


APP_NAME = "copia"
APP_DIR = get_app_dir(APP_NAME)
LOCAL_COPIA_FILE = Path(".copia.toml")
GLOBAL_COPIA_FILE = Path(APP_DIR) / "profiles.toml"
PORT_MIN_VAL = 1
PORT_MAX_VAL = 65535
SUPPORTED_ADAPTERS = Literal['mysql']
CONFIG_SCOPES = Literal["local", "global"]


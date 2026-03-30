import pytest

from copia.cli.config.loaders import resolve_config_path
from copia.cli.config import (
    GLOBAL_COPIA_FILE,
    LOCAL_COPIA_FILE
)

class TestResolveConfigPath:
    def test_global_return_valid(self):
        assert resolve_config_path("global") == GLOBAL_COPIA_FILE
    
    def test_local_return_valid(self):
        assert resolve_config_path("local") == LOCAL_COPIA_FILE
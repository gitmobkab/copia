from pathlib import Path

from .globals import CONFIG_SCOPES, GLOBAL_COPIA_FILE, LOCAL_COPIA_FILE

def resolve_config_path(scope: CONFIG_SCOPES) -> Path:
    if scope == "global":
        return GLOBAL_COPIA_FILE
    elif scope == "local":
        return LOCAL_COPIA_FILE
    else:
        raise ValueError(f"Expected either 'global' or 'local' as scope, got '{scope}'")
from pathlib import Path

from .globals import CONFIG_SCOPES, GLOBAL_COPIA_FILE, LOCAL_COPIA_FILE

def resolve_config_path(scope: CONFIG_SCOPES) -> Path:
    if scope == "global":
        return GLOBAL_COPIA_FILE
    elif scope == "local":
        return LOCAL_COPIA_FILE
    else:
        raise ValueError(f"Expected either 'global' or 'local' as scope, got '{scope}'")
    
def is_valid_hostname(host: str) -> bool:
    if len(host) > 253:
        return False
    labels = host.rstrip(".").split(".")
    for label in labels:
        if not label or len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        if not all(char.isalnum() or char == "-" for char in label):
            return False
    return True

def is_ascii_only(value: str) -> bool:
    return value.isascii()
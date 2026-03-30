"""package from read only access of the config files,

    the functions in this module must be called only for accessing profiles relevant information
    
    see writers.py to modify or add a profile to the config file 
"""
from typing import Any
from pathlib import Path
import tomllib


from pydantic import ValidationError

from .globals import  CONFIG_SCOPES, LOCAL_COPIA_FILE, GLOBAL_COPIA_FILE
from .models import Profile
from .exceptions import (
    FoundProfileIsNotATableError,
    ProfilesKeyIsNotATableError,
    ProfileNotFoundError,
    InvalidProfileError,
    InvalidConfigError
)

def parse_toml_file(path: Path) -> dict[str, Any]:
    """parse path as a toml file and return the configuration
    unsafe function, exceptions must be handled by the caller

    Args:
        path (Path): the path of the file to parse.
    
    Raises:
        FileNotFoundError: when the file couldn't be found.
        PermissionError: when permission to read the file had been denied by the os.
        TOMLDecodeError: when the content of the file can't be parsed to valid TOML.
        
    Returns:
    **dict[str, Any]:** the content of the parsed toml file.
    """
    return tomllib.loads(path.read_text())


def resolve_config_path(scope: CONFIG_SCOPES) -> Path:
    if scope == "global":
        return GLOBAL_COPIA_FILE
    elif scope == "local":
        return LOCAL_COPIA_FILE

def load_config(scope: CONFIG_SCOPES) -> dict[str, Any]:
    """load the content of the config file linked to scope

    Args:
        scope (CONFIG_SCOPES): think of it as where to look the config file, either "local" or "global"

    Raises:
        FileNotFoundError: when the file couldn't be found.
        PermissionError: when permission to read the file had been denied by the os.
        InvalidConfigError: when the config can't be parsed into a valid TOML Document.

    Returns:
    **dict[str, Any]:** the parsed content of the config file.
    """

    path = resolve_config_path(scope)
    try:
        return parse_toml_file(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"{scope} config file not found at '{path}'")
    except PermissionError:
        raise PermissionError(f"not enough permissions to read {scope} config file at '{path}'")
    except tomllib.TOMLDecodeError as TOMLErr:
        raise InvalidConfigError(f"{scope} config file is not a valid TOML file: {TOMLErr}")
      

def get_profile_from_config(profile_name: str, config: dict) -> Profile:
    """try to get a valid profile from config

    config must be a dict representation of the config file

    Args:
        profile_name (str): the name by which the profile is identified
        config (dict): the config supposed of holding the profile
        
    Raises:
        FileNotFoundError: when the file couldn't be found.
        PermissionError: when permission to read the file had been denied by the os.
        InvalidConfigError: when the config isn't valid TOML or the value of the "profiles" key is not a dict/TOML Table
        ProfileNotFoundError: when the "profiles.profile_name" key don't exist, this also includes missing "profiles" key
        FoundProfileIsNotATableError: when the "profiles.profile_name" key exist but is not a dict
        InvalidProfileError: when the profile isn't valid

    Returns:
        Profile: a valid Profile object
    """
    profiles = config.get("profiles")
    if profiles is None:
        raise ProfileNotFoundError("no profiles found")
    if not isinstance(profiles, dict):
        raise ProfilesKeyIsNotATableError("The config file 'profiles' key is not a TOML Table.")
    profile_data = profiles.get(profile_name)
    if profile_data is None:
        raise ProfileNotFoundError(f"{profile_name} not found")
    if not isinstance(profile_data, dict):
        raise FoundProfileIsNotATableError(profile_name)

    try:
        return Profile(**profile_data)
    except ValidationError as Err:
        raise InvalidProfileError(Err)


def get_profile(profile_name: str, scope: CONFIG_SCOPES) -> Profile:
    """try to get a valid profile from config based on scope

    Args:
        profile_name (str): the name by which the profile is identified
        scope (CONFIG_SCOPES): think of it as where to look the config file, either "local" or "global"

    Raises:
        FileNotFoundError: when the file couldn't be found.
        PermissionError: when permission to read the file had been denied by the os.
        InvalidConfigError: when the config isn't valid TOML or the value of the "profiles" key is not a dict/TOML Table
        ProfileNotFoundError: when the "profiles.profile_name" key don't exist, this also includes missing "profiles" key
        FoundProfileIsNotATableError: when the "profiles.profile_name" key exist but is not a dict
        InvalidProfileError: when the profile isn't valid
        
    Returns:
        Profile: a valid Profile object
    """
    config = load_config(scope)
    return get_profile_from_config(profile_name, config)



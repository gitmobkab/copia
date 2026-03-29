"""package from read only access of the config files,

    the functions in this module must be called only for accessing profiles relevant information
    
    see writers.py to modify or add a profile to the config file 
"""

from pathlib import Path
import tomllib


from pydantic import ValidationError

from .utils import resolve_config_path
from .globals import  CONFIG_SCOPES
from .models import Profile
from .exceptions import (
    NoProfilesFoundError,
    ProfileNotATableError,
    ProfileNotFoundError,
    InvalidProfileError,
    InvalidConfigError
)


def parse_toml_file(path: Path) -> dict:
    """
    parse *path* as a toml file and return the configuration
    unsafe function, exceptions must be handled by the caller
    """
    return tomllib.loads(path.read_text())



def load_config(scope: CONFIG_SCOPES) -> dict:

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
    """try to fetch a valid profile from config

        config must be a dict representation of the config file
    """
    profiles = config.get("profiles")
    if isinstance(profiles, list):
        raise InvalidConfigError(
            "The config file has  [ [ profiles ] ] instead of [ profiles.X ]. "
            "This silently breaks all profile management. "
        )
    if not isinstance(profiles, dict):
        raise NoProfilesFoundError("no profiles found")
    profile_data = profiles.get(profile_name)
    if profile_data is None:
        raise ProfileNotFoundError(f"{profile_name} not found")
    if not isinstance(profile_data, dict):
        raise ProfileNotATableError(profile_name)

    try:
        return Profile(**profile_data)
    except ValidationError as Err:
        raise InvalidProfileError(Err)
    
def get_profile(profile_name: str, scope: CONFIG_SCOPES) -> Profile:
    config = load_config(scope)
    try:
        return get_profile_from_config(profile_name, config)
    except ProfileNotFoundError as err:
        raise ProfileNotFoundError(f"{err} in the '{scope}' config file")
    

def get_any_profile(profile_name: str) -> Profile:
    """
    Try to fetch *profile* from the local config file,
    and fall back to global on any fail.
    Any exception from local fetching get silently swallowed
    
    All the exceptions raised by this function are always in the global fetch state
    """
    try:
        return get_profile(profile_name, "local")
    except:
        return get_profile(profile_name, "global")
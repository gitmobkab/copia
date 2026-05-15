from typer import Exit

from copia.cli.config import (
    Profile,
    get_profile,
    ConfigScope,
    InvalidConfigError,
    ProfileError
)
from .exit_codes import ExitCodes
from .console_utils import error, print_error, info

RESSOURCES_ERRORS = (
    FileNotFoundError,
    PermissionError,
)

VALIDATION_ERRORS = (
    InvalidConfigError,
    ProfileError
)

def load_profile(profile_name: str, global_flag: bool, local_flag: bool) -> Profile:

    if global_flag and local_flag:
        error("Cannot use (--global | -g) and (--local | -l) flags at the same time")
        raise Exit()

    try:
        if global_flag:
            profile = get_profile(profile_name, "global")
        elif local_flag:
            profile = get_profile(profile_name, "local")
        else:
            profile = get_any_profile(profile_name)
            
        return profile
    except RESSOURCES_ERRORS as ressource_err:
        if ressource_err is FileNotFoundError:
            help_msg = 'try "copia init" to create a config file!'
        else:
            help_msg = 'Try modifying permissions of the file to read-write-execute (rwx)'
        print_error(ressource_err, help_msg)
        raise Exit(ExitCodes.RESOURCE_ERROR)
    except VALIDATION_ERRORS as validation_err:
        print_error(validation_err)
        raise Exit(ExitCodes.VALIDATION_ERROR)
    except Exception as unexpected_err:
        print_error(unexpected_err, 'this is an unexpected error (surely a bug), help us improve copia by reporting it!')
        raise Exit(ExitCodes.UNEXPECTED_ERROR)
    
    
    
    
def get_any_profile(profile_name: str):
    """
    Try to fetch the profile from the local config file,
    and fall back to global on any fail.
    Any exception from local fetching get silently swallowed
    
    All the exceptions raised by this function are always in the global fetch state
    
    Args:
        profile_name (str): the name by which the profile is identified

    Raises:
        FileNotFoundError: when the file couldn't be found.
        PermissionError: when permission to read the file had been denied by the user os.
        InvalidConfigError: when the config isn't valid TOML or the value of the "profiles" key is not a dict/TOML Table
        ProfileNotFoundError: when the "profiles.profile_name" key don't exist, this also includes missing "profiles" key
        FoundProfileIsNotATableError: when the "profiles.profile_name" key exist but is not a dict
        InvalidProfileError: when the profile isn't valid
        
    Returns:
        Profile: a valid Profile object
    """
    try:
        return __load_profile__(profile_name, 'local')
    except Exception as err:
        error(f"{err}")
        info("Falling back to global config...")
        return __load_profile__(profile_name, 'global')
    
def __load_profile__(profile_name: str, scope: ConfigScope) -> Profile:
    info(f"Fetching profiles.{profile_name!r} from {scope!r} config...")
    return get_profile(profile_name, scope)
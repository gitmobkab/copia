from typer import Exit

from copia.adapters import BaseAdapter, get_adapter

from .console_utils import info, success, print_error
from .exit_codes import ExitCodes

from .profile_loader import load_profile

def load_adapter_from_profile(profile_name: str, global_flag: bool, local_flag: bool) -> BaseAdapter:
    profile = load_profile(profile_name, global_flag, local_flag)

    info(f"Found profile: {profile}")
    info("Connecting to db...")
    
    try:
        adapter = get_adapter(profile)
        success("Connection to db successfull") # log first then return
        return adapter
    except ImportError:
        print_error(f"Missing dependencies for adapter {profile.adapter!r}",
                    f'Try "pip install copia-seed\\[{profile.adapter}]"')
        raise Exit(ExitCodes.RESOURCE_ERROR)
    except Exception as connection_err:
        print_error(connection_err)
        raise Exit(ExitCodes.CONNEXION_TO_DB_FAILED)

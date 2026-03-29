import typer

from ..exit import ExitCodes, exit_app
from ..console import echo, print_error
from ..forms import profile_questionary
from ..config import (
    get_profile,
    InvalidProfileError,
    ProfileNotATableError,
    InvalidConfigError,
    ProfileNotFoundError,
    NoProfilesFoundError,
    save_new_profile,
    create_new_config_file,
    CONFIG_SCOPES,
    Profile,
)

add_profile_app = typer.Typer()

UNEXPECTED_ERROR_HELP_MSG = """
Copia encoutered an unexpected error
Help us improving it by reporting it!
"""

@add_profile_app.command("add")
def add(ctx: typer.Context,
                profile_name: str = typer.Argument(help="the name of the profile to add"),
                
                target_global_config: bool = typer.Option(False,
                                                   "-g","--global",
                                                    help="target the global config instead of the local one")
                ):
    """
        add a profile to the local copia config file, identified by PROFILE_NAME

        Note: add will create the config file if found missing
    """
    
    
    config_scope: CONFIG_SCOPES = "local"
    if target_global_config:
        config_scope = "global"
        
    echo(f"Searching for a profile_name named '{profile_name}' in the {config_scope} config file...")
    profile, is_new_config = probe_profile(profile_name, config_scope, ctx)
    
    if profile is not None:
        echo(f"[dim]found profile: {profile_name} - {profile}")
        echo(f"[bold]use 'copia update \"{profile_name}\"' instead")
        exit_code
    try:
        echo("[dim]Starting questionary form...")
        profile = profile_questionary()
        
        if is_new_config:
            echo(f"[blue]Creating brand new {config_scope} config file...")
            create_new_config_file(profile_name, profile, config_scope)
            echo(f"[green]Success, the profile '{profile_name}' has been created as a '{config_scope}' profile")
        else:
            echo(f"[blue]adding '{profile_name}' to '{config_scope}' config file...")
            save_new_profile(profile_name, profile, config_scope)
            echo(f"[green]Success, the profile '{profile_name}' has been created as a '{config_scope}' profile")
    except KeyboardInterrupt:
        echo("[dim]Profile configuration cancelled by user...")
        exit_app(ExitCodes.SUCCESS)
    except Exception as unexpected_error:
        print_error(unexpected_error, ctx, UNEXPECTED_ERROR_HELP_MSG)
        exit_app(ExitCodes.UNEXPECTED_ERROR)


def probe_profile(profile_name: str, scope: CONFIG_SCOPES, ctx: typer.Context) -> tuple[Profile | None, bool]:
    """probe profile will try to fetch a profile with name *profile_name* from the config file defined by *scope* 
    and return it if found valid, otherwise it will return None.
    
    it will exit the typer application on any error except missing resource errors (FileNotFoundError, ProfileNotFoundError, NoProfilesFoundError) and profile validation errors (InvalidProfileError, ProfileNotATableError) which are handled gracefully with a message to the user and a None return value for the profile.

    Args:
        profile_name (str): the name of the profile to probe
        scope (CONFIG_SCOPES): the config scope to probe the profile in, either "local" or "global"
        ctx (typer.Context): the typer context, used for error handling

    Returns:
    tuple[Profile | None, bool]: 
        a tuple containing the probed profile if found and valid, 
        otherwise None,
        and a boolean indicating if the config file is new (only in case of FileNotFoundError)
    """
    PROFILE_VALIDATION_ERRORS = (InvalidProfileError, ProfileNotATableError)
    MISSING_RESOURCE_ERRORS = (FileNotFoundError, ProfileNotFoundError, NoProfilesFoundError)
    FATAL_ERRORS = (InvalidConfigError, PermissionError)
    
    profile: Profile | None = None
    is_new_config: bool = False
    try:        
        profile = get_profile(profile_name, scope)
    except MISSING_RESOURCE_ERRORS as non_fatal_err:
        echo(f"[dim]{non_fatal_err}")
        if isinstance(non_fatal_err, FileNotFoundError):
            echo("[dim blue]Setting context for new config file...")
            is_new_config = True
    except PROFILE_VALIDATION_ERRORS as bad_profile_err:
        echo(f"[dim]found profile: {profile_name}")
        help_msg = f"[bold red]profiles.{profile_name} is invalid\n[white]use 'copia update \"{profile_name}\"' instead to fix it"
        print_error(bad_profile_err, help_msg=help_msg)
        exit_app(ExitCodes.VALIDATION_ERROR)
    except FATAL_ERRORS as fatal_err:
        print_error(fatal_err, ctx, "Manual intervention is required")
        exit_app(ExitCodes.FATAL)
    except Exception as unexpected_error:
        print_error(unexpected_error, ctx, UNEXPECTED_ERROR_HELP_MSG)
        exit_app(ExitCodes.UNEXPECTED_ERROR)

    return profile, is_new_config


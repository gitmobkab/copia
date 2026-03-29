import typer
from ..console import echo, print_error
from tomllib import TOMLDecodeError

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


from ..forms import profile_questionary

add_profile_app = typer.Typer()

UNEXPECTED_ERROR_HELP_MSG = """
Copia encoutered an unexpected error
Help us improving it by reporting it!
"""

BAD_PROFILE_ERRORS = (InvalidProfileError, ProfileNotATableError)
NON_FATAL_ERRORS = (FileNotFoundError, ProfileNotFoundError, NoProfilesFoundError)
FATAL_ERRORS = (InvalidConfigError, TOMLDecodeError, PermissionError)

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
    profile: Profile | None = None
    is_new_config: bool = False
    config_scope: CONFIG_SCOPES = "local"
    if target_global_config:
        config_scope = "global"
    
    echo(f"Searching for a profile_name named '{profile_name}' in the {config_scope} config file...")
    
    # TODO: for you dumbass, it's fucking time to make a shitty exit codes module
    
    try:        
        profile = get_profile(profile_name, config_scope)
    except NON_FATAL_ERRORS as non_fatal_err:
        echo(f"[dim]{non_fatal_err}")
        if non_fatal_err is FileNotFoundError:
            echo("[dim blue]Setting context for new config file...")
            is_new_config = True
    except BAD_PROFILE_ERRORS as bad_profile_err:
        echo(f"[dim]found profile: {profile_name}")
        help_msg = f"[bold red]profiles.{profile_name} is invalid\n[white]use 'copia update \"{profile_name}\"' instead to fix it"
        print_error(bad_profile_err, help_msg=help_msg)
        raise typer.Exit(2)                   
    except FATAL_ERRORS as fatal_err:
        print_error(fatal_err, ctx, "Manual intervention is required")
        raise typer.Exit(2)
    except Exception as unexpected_error:
        print_error(unexpected_error, ctx, UNEXPECTED_ERROR_HELP_MSG)
        raise typer.Exit(2)
    
    
    if profile is not None:
        echo(f"[dim]found profile: {profile_name} - {profile}")
        echo(f"[bold]use 'copia update \"{profile_name}\"' instead")
        raise typer.Exit()
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
        raise typer.Exit()
    except Exception as unexpected_error:
        print_error(unexpected_error, ctx, UNEXPECTED_ERROR_HELP_MSG)
        raise typer.Exit(2)

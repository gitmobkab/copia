import typer

from copia._version import __version__
from .commands import list_app, init_command
from .exit_codes import ExitCodes
from copia.adapters import get_adapter
from ..tui import CopiaApp
from copia.cli.console_utils import print_error, info, success, error, echo
from .config import (
    get_profile,
    LOCAL_COPIA_FILE,
    GLOBAL_COPIA_FILE
)

app = typer.Typer(invoke_without_command=True)

app.add_typer(init_command)
app.add_typer(list_app)

@app.callback()
def main(
    ctx: typer.Context,
    profile_name: str = typer.Option("default",
                                "-p", "--profile",
                                help="The profile to use for the session"),
    version_flag: bool = typer.Option(False, 
                                 "-v", "--version",
                                 help="Display the current version and exit"),
    
    help_flag: bool = typer.Option(False, 
                              "-h", "--help",
                              help="Display this message and exit"),
    
    search_globals_only: bool = typer.Option(False,
                                            "-g", "--global",
                                            help=f"Search only in [green]'{GLOBAL_COPIA_FILE}'"),
    search_locals_only: bool = typer.Option(False,
                                            "-l", "--local",
                                            help=f"Search only in [green]'{LOCAL_COPIA_FILE}'"),
         ):
    
    """An Interactive TUI app for MySQL Database seeding"""
    
    if ctx.invoked_subcommand is not None:
        return
    
    if help_flag:
        echo(ctx.get_help())
        raise typer.Exit()
        
    if version_flag:
        echo(f"[blue]copia {__version__}")
        raise typer.Exit()
    
    profile = None
    try:
        if search_globals_only and search_locals_only:
            error("Cannot use --global | -g and --local | -l at the same time")
            raise typer.Exit()

        if search_globals_only:
            profile = get_profile(profile_name, "global")
        elif search_locals_only:
            profile = get_profile(profile_name, "local")
        else:
            profile = get_any_profile(profile_name)
    except Exception as err:
        print_error(err)
        raise typer.Exit()


    info(f"Found profile: {profile}")
    info("Connecting to db...")
    
    try:
        adapter = get_adapter(profile)
        success("Connection to db successfull")
    except ImportError:
        print_error(f"Missing dependencies for adapter {profile.adapter!r}",
                    f'Try "pip install copia-seed\\[{profile.adapter}]"')
        raise typer.Exit(ExitCodes.RESOURCE_ERROR)
    except Exception as connection_err:
        print_error(connection_err)
        raise typer.Exit(ExitCodes.CONNEXION_TO_DB_FAILED)

    CopiaApp(adapter).run()
    success("Bye.")
        
            
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
        PermissionError: when permission to read the file had been denied by the os.
        InvalidConfigError: when the config isn't valid TOML or the value of the "profiles" key is not a dict/TOML Table
        ProfileNotFoundError: when the "profiles.profile_name" key don't exist, this also includes missing "profiles" key
        FoundProfileIsNotATableError: when the "profiles.profile_name" key exist but is not a dict
        InvalidProfileError: when the profile isn't valid
        
    Returns:
        Profile: a valid Profile object
    """
    try:
        info(f"Fetching profiles.\"{profile_name}\" from local config...")
        return get_profile(profile_name, "local")
    except Exception as err:
        error(f"{err}")
        info("Falling back to global config...")
        info(f"Fetching profiles.\"{profile_name}\" from global config...")
        return get_profile(profile_name, "global")
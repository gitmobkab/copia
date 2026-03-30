import typer
from rich import print as pprint

from copia._version import VERSION
from .commands import list_app

from .exit import exit_app

from .console import print_error, echo
from .config import (
    get_profile,
    LOCAL_COPIA_FILE,
    GLOBAL_COPIA_FILE
)


app = typer.Typer(invoke_without_command=True)

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
    
    """An Interactive TUI app for MySQL and Postegres Database seeding
    
    """
    
    if ctx.invoked_subcommand is not None:
        return
    
    if help_flag:
        echo(ctx.get_help())
        exit_app()
    
    if version_flag:
        echo(f"[blue]copia {VERSION}")
        exit_app()
    
    profile = None
    try:
        if search_globals_only and search_locals_only:
            raise typer.Exit()

        if search_globals_only:
            profile = get_profile(profile_name, "global")
        elif search_locals_only:
            profile = get_profile(profile_name, "local")
        else:
            profile = get_any_profile(profile_name)
    except Exception as err:
        print_error(err, ctx)
        raise typer.Exit()


    print(profile) # connexion logic for later
        
            
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
        echo(f"[blue]Fetching profiles.\"{profile_name}\" from local config...")
        return get_profile(profile_name, "local")
    except Exception as err:
        echo(f"[dim red]Error: {err}")
        echo(f"[dim]Falling back to global config...")
        echo(f"[blue]Fetching profiles.\"{profile_name}\" from global config...")
        return get_profile(profile_name, "global")
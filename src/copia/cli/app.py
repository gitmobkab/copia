import typer
from rich import print as pprint

from .commands import list_app, add_app

from copia._version import VERSION
from .console import print_error
from .config import (
    get_profile,
    get_any_profile,
    LOCAL_COPIA_FILE,
    GLOBAL_COPIA_FILE
)


app = typer.Typer(help="an interactive database TUI seeder",
                  invoke_without_command=True)

app.add_typer(list_app)
app.add_typer(add_app)

@app.callback()
def main(
    ctx: typer.Context,
    profile_name: str = typer.Option("default",
                                "-p", "--profile",
                                help="The profile to use for the session"),
    version: bool = typer.Option(False, 
                                 "-v", "--version",
                                 help="Display the current version and exit"),
    search_globals_only: bool = typer.Option(False,
                                            "-g", "--global",
                                            help=f"Search only in [green]'{GLOBAL_COPIA_FILE}'"),
    search_locals_only: bool = typer.Option(False,
                                            "-l", "--local",
                                            help=f"Search only in [green]'{LOCAL_COPIA_FILE}'"),
         ):
    
    if ctx.invoked_subcommand is not None:
        return
    
    if version:
        print_version()
    
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
        
        
        
def print_version() -> None:
    pprint(f"[blue]copia {VERSION}")


def pretty_error(message):
    pprint(f"[red bold]{message}")
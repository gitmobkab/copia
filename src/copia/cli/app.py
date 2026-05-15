import typer
from typing import get_args
from copia._version import __version__
from .commands import (
    list_command,
    init_command,
    tui_command,
    run_command
)
from .config import Adapter
from .utils import echo


AVAILABLES_ADAPTERS: tuple = get_args(Adapter)

def get_help_msg():
    help_msg = "An Interactive TUI app for Databases seeding"
    help_msg += "\n\nSupported databases:"
    for value in AVAILABLES_ADAPTERS:
        help_msg += f'\n- {value}'
    return help_msg

app = typer.Typer(
    name='copia',
    help=get_help_msg(),
    no_args_is_help=True,
    invoke_without_command=True,
    context_settings={
        'help_option_names': ['--help', '-h']
    }
)

app.add_typer(init_command)
app.add_typer(list_command)
app.add_typer(tui_command)
app.add_typer(run_command)

@app.callback()
def main(
    ctx: typer.Context,

    version_flag: bool = typer.Option(False, 
                                 "-v", "--version",
                                 help="Display the current version and exit"),
    ):    
    if ctx.invoked_subcommand is not None:
        return
            
    if version_flag:
        echo(f"[blue]copia {__version__}")
        raise typer.Exit()
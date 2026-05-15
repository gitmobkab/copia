import typer

from copia._version import __version__
from .commands import (
    list_command,
    init_command,
    playground_command,
    run_command
)
from .utils import echo


app = typer.Typer(
    name='copia',
    invoke_without_command=True,
    context_settings={
        'help_option_names': ['--help', '-h']
    }
)

app.add_typer(init_command)
app.add_typer(list_command)
app.add_typer(playground_command)
app.add_typer(run_command)

@app.callback()
def main(
    ctx: typer.Context,

    version_flag: bool = typer.Option(False, 
                                 "-v", "--version",
                                 help="Display the current version and exit"),
    ):
    
    """An Interactive TUI app for MySQL Database seeding"""
    
    if ctx.invoked_subcommand is not None:
        return
            
    if version_flag:
        echo(f"[blue]copia {__version__}")
        raise typer.Exit()
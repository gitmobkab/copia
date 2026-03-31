from importlib.resources import files


from rich.prompt import Confirm
import typer

from copia.cli.exit_codes import ExitCodes
from copia.cli.console_utils import echo, print_error
from ..config.loaders import (
    resolve_config_path
)

init_command = typer.Typer()

@init_command.command("init")
def main(ctx: typer.Context,
         help_flag: bool = typer.Option(
    False, "-h", "--help", help="Display this message and exit"),
        is_global_config: bool = typer.Option(
    False, "-g", "--global", help="create the config file as a global config"
)):
    """generate a template config file for copia
    
    by default it create a local scoped config file
    """
    
    if help_flag:
        echo(ctx.get_help())
        raise typer.Exit()
    
    if is_global_config:
        config_path = resolve_config_path("global")
    else:
        config_path = resolve_config_path("local")
    

    echo("[blue dim]Loading example config content...")
    example = files("copia").joinpath("example.copia.toml").read_text()

    if config_path.exists():
        echo("[yellow]:warning: Config file already exists!")
        if not Confirm.ask("Overwrite the previous file?"):
            raise typer.Abort()

    try:
        echo(f"Writing example file to '{config_path}'...")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(example)
        echo(f"[green]Done.")
    except (PermissionError) as err:
        print_error(err, help_msg=f"you don't have enough 'permissions' to create the config file")
    except Exception as err:
        echo(f"Something went wrong while writing to '{config_path}'...")
        print_error(err)
        raise typer.Exit(ExitCodes.UNEXPECTED_ERROR)
    

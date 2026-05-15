from typer import Typer, Argument, Option

from copia.tui import CopiaApp
from ..config import GLOBAL_COPIA_FILE, LOCAL_COPIA_FILE
from ..utils.console_utils import success
from ..utils import load_adapter_from_profile

playground_command = Typer()

@playground_command.command('playground')
def main(
    profile_name: str = Argument('default',
                                help="the name of the profile to use for the session"),
    
    search_globals_only: bool = Option(False,
                                            "-g", "--global",
                                            help=f"Search only in [green]'{GLOBAL_COPIA_FILE}'"),
    search_locals_only: bool = Option(False,
                                            "-l", "--local",
                                            help=f"Search only in [green]'{LOCAL_COPIA_FILE}'")
    ):
    """launch the interactive tui
    """

    adapter = load_adapter_from_profile(profile_name, search_globals_only, search_locals_only)

    CopiaApp(adapter).run()
    success("Bye.")
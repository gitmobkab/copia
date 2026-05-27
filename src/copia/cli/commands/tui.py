from typer import Typer, Argument, Option

from copia.tui import CopiaApp
from ..config import GLOBAL_COPIA_FILE, LOCAL_COPIA_FILE
from ..utils.console_utils import success
from ..utils import load_adapter_from_profile

tui_command = Typer()

@tui_command.command('tui')
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
    """Launch the interactive tui. require a valid configuration profile to run. Use --help for more options.
    
    This command starts to the interactive TUI (Text User Interface) of Copia,
    allowing you to generate data and manage your configurations in an interactive way.
    
    You can specify a profile to use for the session, and choose to search for configurations in either the global or local configuration files.
    """

    adapter = load_adapter_from_profile(profile_name, search_globals_only, search_locals_only)

    CopiaApp(adapter).run()
    success("Bye.")
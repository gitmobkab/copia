from typing import Any

from rich import print as rich_print
from rich.console import Console
from rich.panel import Panel
from typer import Context

from ..config.globals import APP_NAME

stderr_console = Console(stderr=True)
stdout_console = Console()


def print_error(error: Exception, ctx: Context | None = None, help_msg: None | str = None) -> None:
    if ctx is not None:
        stderr_console.print(f"[yellow]Usage:[/] {ctx.get_usage()}")
    
    if help_msg is not None:
        stderr_console.print(f"[dim]{help_msg}")
    else:
        stderr_console.print(f"[dim]Try [blue]'{APP_NAME} --help'[/blue] for help.")
    
    error_panel = Panel(str(error), title="Error", border_style="red", title_align="left", highlight=True)
    stderr_console.print(error_panel)
        
        
def echo(*objects: Any, 
         sep: str = " ", 
         end: str = "\n", 
         err: bool = False
         ):
    if err:
        console = stderr_console
    else:
        console = stdout_console
    
    console.print(*objects, sep=sep, end=end)
    
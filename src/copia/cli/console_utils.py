from typing import Any

from rich.console import Console
from rich.panel import Panel

stderr_console = Console(stderr=True)
stdout_console = Console()


COPIA_DOC_LINK = "https://github.com"
SUBTITLE_HELP = f"[dim]See [blue]{COPIA_DOC_LINK}[/blue] for help."

def print_error(error: Exception, help_msg: None | str = None) -> None:
    
    if help_msg is not None:
        stdout_console.print(f"[dim]{help_msg}")
    
    
    error_panel = Panel(str(error),
                        title="Error",
                        title_align="left",
                        subtitle=SUBTITLE_HELP,
                        subtitle_align="left",
                        border_style="red",
                        highlight=True,
                        padding=(1))
    
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
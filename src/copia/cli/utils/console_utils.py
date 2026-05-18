from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

stderr_console = Console(stderr=True)
stdout_console = Console()

COPIA_DOC_LINK = "https://gitmobkab.github.io/copia/"
SUBTITLE_HELP = f"[bold white]See [blue]{COPIA_DOC_LINK}[/blue] for help."

COLORS : dict[str, str] = {
    "info": "#008080",
    "success": "#008000",
    "warn": "#cc5500",
    "error": "#8b0000"
}

def _log(msg: str, level: str, color: str, err: bool = False) -> None:
    console = stderr_console if err else stdout_console
    label = Text(f" {level} ", style=f"bold white on {color}")
    console.print(label, msg)


def info(msg: str) -> None:
    _log(msg, "INFO", COLORS["info"])


def success(msg: str) -> None:
    _log(msg, "OK", COLORS["success"])


def warning(msg: str) -> None:
    _log(msg, "WARN", COLORS["warn"])


def error(msg: str) -> None:
    _log(msg, "ERROR", COLORS["error"], err=True)


def dim(msg: str) -> None:
    stdout_console.print(f"[dim]{msg}")


def print_error(err: object, help_msg: str | None = None) -> None:
    body = str(err)
    if help_msg:
        body = f"[on {COLORS['info']}] HINT [/] {help_msg}\n{body}"
    stderr_console.print(Panel(
        body,
        title="Error",
        title_align="left",
        subtitle=SUBTITLE_HELP,
        subtitle_align="left",
        border_style=COLORS["error"],
        padding=(1),
        highlight=True
    ))


def echo(*objects: Any, sep: str = " ", end: str = "\n", err: bool = False) -> None:
    console = stderr_console if err else stdout_console
    console.print(*objects, sep=sep, end=end)
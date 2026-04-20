from typing import Iterable, Literal, Any, TypeAlias

from rich.console import RenderableType
from textual.containers import Container, HorizontalGroup
from textual.widgets import DataTable, RichLog, Button, ContentSwitcher
from textual.widget import Widget

from copia.parser.models import Column

ROWS : TypeAlias = list[dict[str, Any]]

class ResultsViewer(Container):
    
    DEFAULT_CSS = """
    
    ResultsViewer ContentSwitcher{
        padding: 1;
        height: 1fr;
    }
        
    ResultsViewer DataTable {
        height: 1fr;
    }
    """
    
    
    def compose(self) -> Iterable[Widget]:
        with HorizontalGroup(id="buttons"):
            yield Button("logs", id="logs", variant="primary")
            yield Button("results", id="results", variant="success")
            
        with ContentSwitcher(initial="logs"):
            yield RichLog(id="logs", markup=True, highlight=True)
            yield DataTable(id="results")
        
    def on_mount(self):
        self.border_title = "Results viewer"
        self._rows: ROWS = []
        self._columns: list[str | None] = []
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        content_switcher = self.query_one(ContentSwitcher)
        content_switcher.current = event.button.id
        
    def add_columns(self, columns: list[Column]) -> None:
        self.focus_on("results")
        data_table = self.query_one(DataTable)
        for column in columns:
            column_name = column.name
            if column_name:
                data_table.add_column(column_name)
            else:
                data_table.add_column("Anonym column")
            self._columns.append(column_name)
    
    def get_columns(self) -> list[str | None]:
        return self._columns        
    
    def get_rows(self) -> ROWS:
        return self._rows
            
    def add_row(self, data: dict, index: int) -> None:
        self._rows.append(data)
        self.focus_on("results")
        data_table = self.query_one(DataTable)
        data_table.add_row(*data.values(), label=str(index))
        
    def clear_all(self) -> None:
        self.clear_logs()
        self.clear_results()
        
    def clear_results(self) -> None:
        self._columns.clear()
        self._rows.clear()
        self.focus_on("results")
        self.query_one(DataTable).clear(True)

    def clear_logs(self) -> None:
        self.focus_on("logs")
        self.query_one(RichLog).clear()
    
    def info(self,  content: RenderableType | object) -> None:
        self.echo(f"[blue bold]{content}")
    
    def warn(self, content: RenderableType | object) -> None:
        self.echo(f"[yellow bold]:warning: {content}")
    
    def error(self, content: RenderableType | object) -> None:
        self.echo(f"[red bold]✗ {content}")
    
    def success(self, content: RenderableType | object) -> None:
        self.echo(f"[green bold]✓ {content}")
    
    def echo(self, content: RenderableType | object) -> None:
        self.focus_on("logs")
        self.query_one(RichLog).write(content, animate=True)
        
    def focus_on(self, id: Literal["logs", "results"]) -> None:
        content_switcher = self.query_one(ContentSwitcher)
        content_switcher.current = id
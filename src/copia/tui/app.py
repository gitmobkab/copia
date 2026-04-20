from threading import Event

from sqlalchemy import Engine, Connection, inspect
from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message

from copia.parser import parse
from copia.parser.models import Column
from copia.validator import SemanticValidator
from copia.generators import GENERATORS_REGISTRY, GeneratorValueError
from copia.runners import generate_rows
from copia.submit import submit_rows

from .widgets import CopiaEditor, ActionBar, ResultsViewer
from .screens import HelpScreen
from .utils import build_database_tables_tree
from .theme import COPIA_THEME

class CopiaApp(App):
    
    SCREENS = {"help": HelpScreen}
    BINDINGS = [
        ("?", "push_screen('help')", "show help screen"),
        ("q", "quit", "Close the app")
                ]
    CSS_PATH="style.tcss"
    
    class GenerationCanceled(Message):
        def __init__(self, row: int) -> None:
            super().__init__()
            self.current_row = row
    
    class AllRowsGenerated(Message):
        def __init__(self, rows: int) -> None:
            super().__init__()
            self.rows = rows
            
    class GenerationErrorOccurred(Message):
        def __init__(self, error: object) -> None:
            super().__init__()
            self.error = error
    
    class SubmitSucceeded(Message):
        def __init__(self, rows: int) -> None:
            super().__init__()
            self.rows = rows

    class SubmitFailed(Message):
        def __init__(self, error: object) -> None:
            super().__init__()
            self.error = error
    
    def __init__(self, engine: Engine | None = None):
        self.engine = engine
        self._validator = SemanticValidator(GENERATORS_REGISTRY)
        self._inspector = inspect(engine, False)
        self._connection : Connection | None = None
        self._cancel_requested = Event()
        super().__init__()
        
    def on_mount(self) -> None:
        self.register_theme(COPIA_THEME)
        self.theme = "copia"
        if self.engine:
            self._connection = self.engine.connect()
            self.notify("Connection to database established")
    
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            table = build_database_tables_tree(self.engine, "db-tree")
            yield table
            with VerticalGroup():
                yield CopiaEditor()
                yield ActionBar()
                yield ResultsViewer()
        yield Footer()
                
    @on(Tree.NodeSelected, "#db-tree")
    def update_selected_table(self, event: Tree.NodeSelected) -> None:
            if event.node.data is None:
                print(f"No data available for node with id: {event.node.id}")
                return
            action_bar = self.query_one(ActionBar)
            action_bar.selected_table = event.node.data
            
    @on(ActionBar.RunRequested)
    def run_user_query(self, event: ActionBar.RunRequested) -> None:
        code_editor_content = self.query_one(CopiaEditor).document.text
        results_viewer = self.query_one(ResultsViewer)
        results_viewer.clear_all()
        try:
            parsed_columns = parse(code_editor_content)
            results_viewer.info("parsing your input...")
            results_viewer.success("Looks good")
            for column in parsed_columns:
                self._validator.validate(column.generator)
        except Exception as err:
            results_viewer.error(err)
            return
            
        self.query_one(ActionBar).show_cancel_btn()
        results_viewer.add_columns(parsed_columns)
        self.make_rows(parsed_columns, event.rows)
        
    @on(ActionBar.SubmitRequested)
    def submit_results(self, event: ActionBar.SubmitRequested):
        results_viewer = self.query_one(ResultsViewer)
        results_viewer.clear_logs()
        columns = results_viewer.get_columns()
        rows = results_viewer.get_rows()
        anonym_columns = list(filter(lambda x: x is None, columns))
        if anonym_columns:
            results_viewer.error(f"you have {len(anonym_columns)} anonym columns defined, copia can't map submit until all columns get a name")
            return
        if not rows:
            results_viewer.error("you need to 'run' the query first then submit the result")
            return
        self.query_one(ActionBar).disable_buttons()
        self.commit_rows(rows, event.table)
        
    @work(thread=True)
    def commit_rows(self, rows: list[dict], table_name: str):
        if self.engine is None:
            self.query_one(ResultsViewer).error("There's no engine set, action impossible (if you're using textual_console, consider lauching copia directly)")
            return
        try:
            submit_rows(self.engine, rows, table_name)
            self.post_message(self.SubmitSucceeded(len(rows)))
        except Exception as err:
            self.post_message(self.SubmitFailed(err))
        self.query_one(ActionBar).enable_buttons()
        
    @work(thread=True)
    def make_rows(self, columns: list[Column], rows: int):
        self._cancel_requested.clear()
        results_viewer = self.query_one(ResultsViewer)
        if self._connection is None:
            results_viewer.error("There's no connection, ref can't be used")
            return
        try:
            for index, row in enumerate(generate_rows(self._connection, columns, rows), 1):
                if self._cancel_requested.is_set():
                    self.post_message(self.GenerationCanceled(index))
                    break
                self.call_from_thread(results_viewer.add_row, row, index)
            else:
                self.post_message(self.AllRowsGenerated(rows))
        except GeneratorValueError as err:
            self.post_message(self.GenerationErrorOccurred(err))
            
    def action_quit(self):
        if self.engine:
            self.engine.dispose()
        return super().action_quit()
    
    @on(ActionBar.CancelRequested)
    def stop_rows_stream(self):
        self._cancel_requested.set()
        self.query_one(ActionBar).hide_cancel_btn()
        
    @on(GenerationErrorOccurred)
    def handle_generation_error(self, event: GenerationErrorOccurred):
        self.query_one(ActionBar).hide_cancel_btn()
        self.query_one(ResultsViewer).error(event.error)
        
    @on(AllRowsGenerated)
    def close_row_stream(self, event: AllRowsGenerated):
        self.query_one(ActionBar).hide_cancel_btn()
        results_viewer = self.query_one(ResultsViewer)
        results_viewer.info(f"Succesfully generated {event.rows} rows")
        results_viewer.focus_on("results")
        
    @on(GenerationCanceled)
    def handle_canceled_generation(self, event: GenerationCanceled):
        results_viewer = self.query_one(ResultsViewer)
        results_viewer.info(f"Generation canceled at row {event.current_row}!")
        results_viewer.focus_on("results")
        
    @on(SubmitSucceeded)
    def handle_submit_success(self, event: SubmitSucceeded) -> None:
        self.query_one(ResultsViewer).success(
            f"{event.rows} rows inserted successfully"
        )

    @on(SubmitFailed)
    def handle_submit_failure(self, event: SubmitFailed) -> None:
        self.query_one(ResultsViewer).error(f"Insert failed: {event.error}")
        
from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Input, Label
from textual.containers import HorizontalGroup, Center
from textual.reactive import reactive


class ActionBar(Widget):
    """Control bar between the editor and results panel.

    Displays the currently selected table, a row count input,
    and RUN / SUBMIT buttons.

    Messages:
        ActionBar.RunRequested  — user pressed RUN
        ActionBar.SubmitRequested — user pressed SUBMIT
    """

    DEFAULT_CSS = """
    
    ActionBar{
        align: center middle;
        background: $surface;
        height: 1fr;
    }
    
    ActionBar .hidden{
        display: none;
    }

    ActionBar #table-label{
        width: 1fr;
        color: $text-muted;
        padding: 1 2;
    }

    ActionBar #rows-label{
        padding: 1;
    }

    ActionBar #rows-input{
        width: 20%;
        border: tall $border;
        background: $surface-darken-1;
    }
    
    ActionBar #rows-input.invalid{
        border: tall $error;
    }

    ActionBar #run-btn{
        margin: 0 1;
    }

    ActionBar #submit-btn{
        margin: 0 0;
    }
    
    ActionBar #hint-msg{
        margin-top: 1;
    }
    """

    selected_table: reactive[str | None] = reactive(None)

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------

    class RunRequested(Message):
        """Message sent when the RUN button is pressed"""
        def __init__(self, rows: int) -> None:
            self.rows = rows
            super().__init__()

    class SubmitRequested(Message):
        """Message sent when the SUBMIT button is pressed"""        
        def __init__(self, table: str) -> None:
            self.table = table
            super().__init__()
            
    class CancelRequested(Message):
        """Message sent when the CANCEL button is pressed"""
        def __init__(self) -> None:
            super().__init__()
            
            
    def compose(self) -> ComposeResult:
        with HorizontalGroup():        
            yield Label("No table selected...", id="table-label")
            yield Label("ROWS:", id="rows-label")
            yield Input("1",
                        id="rows-input",
                        restrict=r"[0-9]*",
                        validate_on=["changed"])
            yield Button("RUN", id="run-btn", variant="primary")
            yield Button("SUBMIT", id="submit-btn", variant="success", disabled=True)
            yield Button("CANCEL", id="cancel-btn", variant="error", classes="hidden")
        with Center():
            yield Label("select a table to use 'submit'", id="hint-msg")

    def watch_selected_table(self, table: str | None) -> None:
        label = self.query_one("#table-label", Label)
        hint_label = self.query_one("#hint-msg", Label)
        if table is None:
            label.update("No table selected...")
            label.remove_class("selected")
            self.query_one("#submit-btn", Button).disabled = True
            hint_label.content = "select a table to use 'submit'"
        else:
            label.update(table)
            label.add_class("selected")
            self.query_one("#submit-btn", Button).disabled = False
            hint_label.content = ""

    def show_cancel_btn(self) -> None:
        buttons = self.query(Button)
        for button in buttons:
            if button.id != "cancel-btn":
                button.add_class("hidden")
            else:
                button.remove_class("hidden")
                button.focus()
        
    def hide_cancel_btn(self) -> None:
        buttons = self.query(Button)
        for button in buttons:
            if button.id != "cancel-btn":
                button.remove_class("hidden")
            else:
                button.add_class("hidden")
    
    def disable_buttons(self) -> None:
        self._set_buttons_disabled_state(True)
        
    def enable_buttons(self) -> None:
        self._set_buttons_disabled_state(False)

    def _set_buttons_disabled_state(self, new_state: bool) -> None:
        buttons = self.query(Button)
        for button in buttons:
            if button.id == "cancel-btn":
                continue
            button.disabled = new_state


    def post_run_requested(self) -> None:
        rows = self._get_rows()
        self.post_message(self.RunRequested(rows))


    def post_submit_requested(self) -> None:
        if self.selected_table is None:
            return
        self.post_message(self.SubmitRequested(self.selected_table))

    def _get_rows(self) -> int:
        try:
            raw = self.query_one("#rows-input", Input).value
            rows = int(raw)
            return rows
        except ValueError:
            return 0



    @on(Button.Pressed, "#run-btn")
    def on_run_pressed(self) -> None:
        self.post_run_requested()

    @on(Button.Pressed, "#submit-btn")
    def on_submit_pressed(self) -> None:
        self.post_submit_requested()
        
    @on(Button.Pressed, "#cancel-btn")
    def on_cancel_pressed(self) -> None:
        self.post_message(self.CancelRequested())
        
    def on_input_changed(self, event: Input.Changed):
        hint_label = self.query_one("#hint-msg", Label)
        try:
            converted_value = int(event.input.value)
            if converted_value == 0:
                hint_label.content = "rows must be greater than 0"
                event.input.add_class("invalid")
                self.disable_buttons()
                return
            hint_label.content = ""  
            event.input.remove_class("invalid")
            self.enable_buttons()
        except ValueError:
            hint_label.content = "Please enter a valid integer in the rows input"
            event.input.add_class("invalid")
            self.disable_buttons()
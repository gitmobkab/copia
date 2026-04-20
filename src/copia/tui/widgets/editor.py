from textual.app import App
from textual.widgets import TextArea
from textual import events



class CopiaEditor(TextArea):
    """TextArea for the copia DSL with generator dropdown and auto-close parens.

    Args:
        generators: dict mapping generator name to its callable.
    """
    SPECIAL_CHARS = {
        "left_parenthesis": "()",
        "quotation_mark": '""',
        "apostrophe": "''"
    }

    DEFAULT_CSS = """
    
    Toast {
        padding: 5;
    }
    
    ToastRack {
        align: center middle;
    }
    
    CopiaEditor {
        height: 1fr;
        border: round $border;
    }

    CopiaEditor:focus {
        border: round $accent;
    }
    """

    def on_mount(self) -> None:
        self.border_title = "Copia DSL Editor"

    def on_key(self, event: events.Key) -> None:
        insert_value = self.SPECIAL_CHARS.get(event.key)
        if insert_value:
            event.prevent_default()
            self.insert(insert_value)
            self.move_cursor_relative(columns=-1)
            event.stop()



class EditorApp(App):
    
    def compose(self):
        yield CopiaEditor()
        
    def on_ready(self):
        self.notify("._.")
                
        
        
if __name__ == "__main__":
    EditorApp().run()
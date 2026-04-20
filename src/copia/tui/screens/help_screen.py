from importlib.resources import files
from typing import Iterable

from textual import work
from textual.app import App
from textual.screen import ModalScreen
from textual.widgets import MarkdownViewer, Header, Footer
from textual.containers import Container
from textual.widget import Widget

from copia.generators import GENERATORS_REGISTRY, generate_generators_markdown
from copia.tui.theme import COPIA_THEME


DSL_DOC = files("copia.data").joinpath("dsl.md").read_text(encoding="utf-8")
GENERATORS_DOC = generate_generators_markdown(GENERATORS_REGISTRY)

class HelpScreen(ModalScreen):
    CSS="""
    HelpScreen {
        width: 100%;
        height: 100%;
        layers: base;
    }

    MarkdownViewer {
        width: 100%;
        height: 100%;
    }
    """
    
    
    BINDINGS = [("escape, q", "app.pop_screen", "Close the help screen")]

    def compose(self) -> Iterable[Widget]:
        yield Container()
        yield Footer()
    
    def on_mount(self) -> None:
        self.query_one(Container).loading = True
        self.load_docs()

        
    @work(thread=True)
    def load_docs(self):
        doc = DSL_DOC + "\n\n" + generate_generators_markdown(GENERATORS_REGISTRY)
        self.app.call_from_thread(self._mount_viewer, doc)

    async def _mount_viewer(self, doc: str):
        viewer = MarkdownViewer(doc, show_table_of_contents=True)
        await self.query_one(Container).mount(viewer)
        self.query_one(Container).loading = False
        
    
class BSODApp(App):
    
    SCREENS = {"help": HelpScreen}
    BINDINGS = [("b", "push_screen('help')", "show help screen")]

    def on_mount(self) -> None:
        self.register_theme(COPIA_THEME)
        self.theme = "copia"
        
    def compose(self) -> Iterable[Widget]:
        yield Header()
        yield Footer()
        
        
if __name__ == "__main__":
    app = BSODApp()
    app.run()
from faker.config import AVAILABLE_LOCALES
from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Select, Button, Label, Switch, Footer
from textual.containers import Vertical, Horizontal

from copia.generators._core import GenerationSettings


class GenerationSettingsScreen(ModalScreen[GenerationSettings]):
    
    DEFAULT_CSS = """
        GenerationSettingsScreen {
            align: center middle;
        }

        GenerationSettingsScreen > Vertical {
            width: 60;
            height: auto;
            background: $surface;
            border: round $primary;
            padding: 1 2;
        }

        GenerationSettingsScreen > Vertical > Horizontal {
            height: auto;
            margin-bottom: 1;
        }

        GenerationSettingsScreen Select {
            margin-bottom: 1;
        }

        GenerationSettingsScreen Switch {
            margin-bottom: 1;
        }

        GenerationSettingsScreen #close {
            dock: right;
            min-width: 3;
            height: 1;
            border: none;
            background: transparent;
            color: $error;
        }
                
        GenerationSettingsScreen #buttons {
            align: center middle;
        }
        
        GenerationSettingsScreen #buttons Button {
            margin: 0 3;
        }
    """
    
    BINDINGS = [("escape, q", "dismiss(None)", "Close")]

    def __init__(self, settings: GenerationSettings ,name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.current_settings = settings

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Label("Generation Settings")
                yield Button("X", id="close")
            yield Label("Generation Settings")
            yield Select(
                [(locale, locale) for locale in AVAILABLE_LOCALES],
                value=self.current_settings.locale,
                allow_blank=False,
                prompt="Select locale",
                id="locale-select",
                tooltip="the selected locale will affect the values from some generators"
            )
            yield Label("Fast generation (disables weighting)")
            yield Switch(
                value=self.current_settings.optimized,
                id="optimized",
                tooltip="if checked, generation will be faster but the values will no longer follow real world frequencies")
            with Horizontal(id="buttons"):
                yield Button("Apply", variant="primary", id="apply")
                yield Button("Reset", id="reset")
        yield Footer()

    @on(Button.Pressed, "#apply")
    def apply_settings(self) -> None:
        locale = self.query_one("#locale-select", Select).value
        optimized = self.query_one("#optimized", Switch).value
        new_settings = GenerationSettings(locale, optimized) # type: ignore
        if self.current_settings != new_settings:
            self.dismiss(new_settings)
        else:
            self.close_screen()
        
    @on(Button.Pressed, "#reset")
    def reset_settings(self) -> None:
        self.query_one("#locale-select", Select).value = self.current_settings.locale
        self.query_one("#optimized", Switch).value = self.current_settings.optimized
        
    @on(Button.Pressed, "#close")
    def close_screen(self) -> None:
        self.dismiss(None)
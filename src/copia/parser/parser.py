from lark import Lark
from lark.exceptions import VisitError
from pathlib import Path
from copia.parser.transformer import CopiaTransformer
from copia.parser.models import Column

_parser = Lark(
    (Path(__file__).parent / "grammar.lark").read_text(),
    start="command"
)

def parse(command: str) -> list[Column]:
    """
    parse a string as a generation command and give a list of columns representing the command
    
    """
    try:
        tree = _parser.parse(command)
        return CopiaTransformer().transform(tree)
    except VisitError as err:
        raise err.orig_exc        
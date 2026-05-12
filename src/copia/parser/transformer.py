from lark import Transformer
from .models import Params, GeneratorCall, Column
from .exceptions import DuplicateNamedParamException, DuplicateColumnNameError

class CopiaTransformer(Transformer):
    
    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)
        self.defined_columns: set[str] = set()
            
    def IDENTIFIER(self, token) -> str:
        return str(token)
    
    def INT(self, token) -> int:
        return int(token)
    
    def FLOAT(self, token) -> float:
        return float(token)
    
    def BOOL(self, token) -> bool:
        if token.lower() == "true":
            return True
        else:
            return False
    
    def string(self, items) -> str:
        token = items[0]
        return str(token[1:-1])
    
    def argument(self, items) -> str | int | float | bool:
        token = items[0]
        return token

    def name(self, items) -> tuple:
        return (items[0], items[1])
    
    def positionals(self, items) -> list:
        return list(items)
    
    def named(self, items) -> dict:
        named_args = {}
        for item in items:
            arg_name, arg_val = item
            if arg_name in named_args:
                raise DuplicateNamedParamException(f"{arg_name} is defined twice")
            named_args[arg_name] = arg_val
        return named_args
    
    def params(self, items) -> Params:
        if not items:
            return Params([], {})
        
        if len(items) == 2:
            return Params(items[0], items[1])
        
        item = items[0]
        if isinstance(item, list):
            return Params(item, {})
        else:
            return Params([], item)
        
    def UNIQUE_CONSTRAINT(self, _):
        return True
        
    def generator(self, items) -> GeneratorCall:
        if len(items) == 2:
            return GeneratorCall(
                items[0],
                items[1]
            )
        return GeneratorCall(
            items[0],
            Params(
                [],
                {}
            )
        )
        
    def column(self, items) -> Column:
        construction_args = self._build_column_construction_args(items)
        column_name = construction_args[0]
        if isinstance(column_name, str):
            self._handle_column_name(column_name)
        return Column(*construction_args)
 
    
    def command(self, items) -> list[Column]:
        return list(items)
    
    def _handle_column_name(self, column_name: str) -> None:
        if column_name in self.defined_columns:
            raise DuplicateColumnNameError(f"{column_name} is defined twice")
        else:
            self.defined_columns.add(column_name)
        
    def _build_column_construction_args(self, items: list) -> list:
        if len(items) == 1:
            construction_args = [None, False, items[0]]
        elif len(items) == 2:
            if isinstance(items[0], str):
                construction_args = [items[0], False, items[1]]
            else:
                construction_args = [None, True, items[1]]
        else:
            construction_args = items

        return construction_args
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
        
    def UNIQUE_CONSTRAINT(self, value) -> bool:
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
        construction_values = self._get_construction_values(items)
        column_name = items[0]
        if isinstance(column_name, str):
            self._duplicate_columns_check(column_name)
        return Column(*construction_values)
            
    def _get_construction_values(self, items) -> list:
        items_len = len(items)
        construction_values = []
        if items_len == 1:
            construction_values = [
                None,
                False,
                items[0]
            ]
        elif items_len == 2 and items[0] is True:
            construction_values = [
                None,
                True,
                items[1]
            ]
        elif items_len == 2 and (isinstance(items[0], str) or items[0] is None):
                construction_values = [
                    items[0],
                    False,
                    items[1]
                ]
        else:
            construction_values = [
                *items
            ]
        
        return construction_values
        
    def _duplicate_columns_check(self, column_name: str):
        if column_name in self.defined_columns:
            raise DuplicateColumnNameError(f"{column_name} is defined twice")
        else:
            self.defined_columns.add(column_name)

    def command(self, items) -> list[Column]:
        return list(items)
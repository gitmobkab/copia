from random import randint

from textual.widgets import Tree
from sqlalchemy import Engine, Inspector, inspect


def build_database_tables_tree(engine: Engine | None, id: str | None = None, classes: str | None = None) -> Tree:
    if engine is None:
        return _placeholder_tree_builder(id=id, classes=classes)
    return _real_tree_builder("db", inspect(engine), id=id, classes=classes)
    
        
def _placeholder_tree_builder(id: str | None = None, classes: str | None = None):
    tree = Tree("\\[Placeholder Composer]", id=id, classes=classes)
    tree.root.expand()
    for table_index in range(randint(5, 10)):
        table_data = f"TABLE -- {table_index}"
        current_table = tree.root.add(table_data, table_data)
        for column_index in range(randint(3, 10)):
            current_table.add_leaf(f"COLUMN {column_index}::(TYPE)")
    return tree
        
def _real_tree_builder(name: str, inspector: Inspector, id: str | None = None, classes: str | None = None) -> Tree:
    tree = Tree(name, id=id, classes=classes)
    tree.root.expand()
    for table in inspector.get_table_names():
        current_table_tree = tree.root.add(f"{table} (table)", table)
        columns = inspector.get_columns(table)
        for column in columns:
            current_table_tree.add_leaf(f"{column['name']}::{column['type']}")
    return tree


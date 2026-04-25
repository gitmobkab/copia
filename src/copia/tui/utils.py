from textual.widgets import Tree
from sqlalchemy import Engine, Inspector, inspect


def build_database_tables_tree(engine: Engine , id: str | None = None, classes: str | None = None) -> Tree:
    return _real_tree_builder("db", inspect(engine), id=id, classes=classes)
    
def _real_tree_builder(name: str, inspector: Inspector, id: str | None = None, classes: str | None = None) -> Tree:
    tree = Tree(name, id=id, classes=classes)
    tree.root.expand()
    for table in inspector.get_table_names():
        current_table_tree = tree.root.add(f"{table} (table)", table)
        columns = inspector.get_columns(table)
        for column in columns:
            current_table_tree.add_leaf(f"{column['name']}::{column['type']}")
    return tree


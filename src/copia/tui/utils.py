from textual.widgets import Tree

from copia.adapters import BaseAdapter

def build_database_tables_tree(adapter: BaseAdapter, id: str | None = None, classes: str | None = None) -> Tree:
    tree = Tree("db", id=id, classes=classes)
    tree.root.expand()
    for table in adapter.get_tables():
        current_table_tree = tree.root.add(f"{table} (table)", table)
        columns = adapter.get_columns(table)
        for column in columns:
            current_table_tree.add_leaf(f"{column.name}::{column.type}")
    return tree


from dataclasses import dataclass

@dataclass
class ColumnInfo:
    name: str
    type: str
    is_nullable: bool
    default: str | None
    extra: str | None = None
    
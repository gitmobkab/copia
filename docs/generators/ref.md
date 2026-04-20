# ref

> ref(column: str) -> Any

Fetch a random existing value from a database column.

**Arguments**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `column` | str | — | Column reference in 'table.column' format. |

**Returns** `Any`

> ⚠️ Only uses values already present in the database. An empty column will raise an error at runtime.

# How `ref` Works

`ref` is the only generator that reads from the database rather than generating data. It samples a random value from an existing column.

---

## Usage

```
user_id: ref('users.id')
```

The argument is a string in `table.column` format. `ref` fetches all existing values from that column and returns one at random on each call.

---

## Internals

### Parsing the target

When the DSL is parsed, `ref('users.id')` produces a `GeneratorCall` with a single positional argument — the string `"users.id"`. Before generation, the runner walks all parsed columns, identifies `ref` calls, and extracts the `table.column` string via `_parse_ref_input()`.

The string is split on `.` and must produce exactly two non-empty parts — `table` and `column`. Any other format raises a `GeneratorValueError` immediately.

### Phase 1 — Initialize

Before any generation, the runner scans all parsed columns for `ref` calls and builds an empty `REF_COLLECTION` structure:

```python
REF_COLLECTION = {
    "users": {
        "id": []
    },
    "posts": {
        "id": []
    }
}
```

All tables and columns are identified upfront. Columns belonging to the same table are grouped together — this is what makes the next phase efficient.

### Phase 2 — Populate

With the structure in hand, the runner fetches all columns of a given table in a single query per table. If two `ref` calls target `users.id` and `users.email`, only one query is issued:

```sql
SELECT id, email FROM users
```

This is more efficient than one query per `ref` call. The results are distributed into the corresponding lists in `REF_COLLECTION`.

### Sampling

On each row generation, `ref('users.id')` samples a random value from `REF_COLLECTION["users"]["id"]` using `random.choice()`.

### Empty column behavior

If the target column is empty, `REF_COLLECTION["table"]["column"]` will be an empty list. Sampling from an empty list raises a `GeneratorValueError` with a descriptive message pointing to the empty column.

This is why the `ref` documentation warns: **always populate parent tables before referencing them.**

---

## Limitations

- `ref` can only reference values already in the database at the time of the run. Values generated in the same run are not available to `ref`.
- `ref` requires an active database connection.
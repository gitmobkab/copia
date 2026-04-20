# Copia DSL

Copia is a declarative language — a fusion of SQL `INSERT` semantics and Python function call syntax.
Each line maps a table column to a generator, describing *what* to populate without specifying *how*.

---

## Syntax

```
column_name: generator_name(arguments)
```

A **column name** followed by `:` followed by a **generator call**.

---

## Column name

The column name is optional. If omitted, the column is **anonymous** — its values are
generated but not mapped to any specific column. Anonymous columns are useful for quick
testing without a target table in mind.

```
username: username()
: uuid()
```

Named columns must match the actual column names in your target table.

---

## Generator call

A generator is called by name, with optional arguments in parentheses.
If a generator takes no arguments, the parentheses can be omitted entirely.

```
email: email()
email: email
```

Both forms are equivalent for generators with no required arguments.

---

## Arguments

Generators accept two kinds of arguments: **positional** and **named**.

### Positional

Passed in order, without names.

```
status: enum('active', 'inactive', 'banned')
score: int_range(0, 100)
```

### Named

Passed by name, in any order.

```
email: email(safe=True, domain='example.com')
password: password(length=16, special_chars=False)
```

### Mixed

Positional arguments must always come before named arguments.

```
ip: ipv4(True, address_class='b')
```

### Argument types

| Type    | Example                      |
|---------|------------------------------|
| Integer | `42`, `-7`                   |
| Float   | `3.14`, `-0.5`               |
| String  | `'hello'`, `"world"`         |
| Boolean | `True`, `False`              |

---

## Multiple columns

A Copia file defines one or more columns, one per line.
All columns are generated together for the target table.

```
id:         uuid()
username:   username()
email:      email(safe=True)
password:   password(length=20)
created_at: past_date()
```

---

## The `ref` generator

`ref` samples a random value from an existing column in the database.
It is the only generator that reads from the database rather than generating data.

```
user_id: ref('users.id')
post_id: ref('posts.id')
```

The argument is a string in `'table.column'` format.

> ⚠️ `ref` only reads values already present in the database.
> An empty column will raise an error at runtime.
> Always populate parent tables before referencing them.

---

## The `enum` generator

`enum` picks a random value from a fixed set of choices you define.

```
role:   enum('admin', 'editor', 'viewer')
status: enum('active', 'inactive')
```

At least one value is required.
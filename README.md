# Copia

**Seed your database without the hassle.**

Most frameworks either ship a seeder with questionable decisions, or don't ship one at all. Copia is a TUI-based database seeder with its own declarative language — you describe what data you want, column by column, and Copia generates and inserts it.

```
id:         uuid()
username:   username()
email:      email(safe=True)
role:       enum('admin', 'editor', 'viewer')
created_at: past_date()
```

---

## Features

- **Simple language** — if you know what a function call looks like, you know the Copia DSL
- **Realistic data** — built on [Faker](https://faker.readthedocs.io/), 25+ generators out of the box
- **Relational-aware** — `ref('table.column')` samples from existing rows, so foreign keys just work
- **Interactive TUI** — write, preview, and insert without leaving your terminal
- **Extensible** — add your own generators with a single function

## Installation

```bash
pip install copia
```

Requires Python 3.13+. MySQL and MariaDB are supported.

## Quickstart

```bash
copia init       # generate a config template
copia            # launch the TUI
```

## Documentation

→ [copia.readthedocs.io](https://copia.readthedocs.io)

---

## License

MIT
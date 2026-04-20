<p align="center">
  <img src="docs/assets/logo.svg" width="80" alt="Copia logo">
</p>

<h1 align="center" style="color:#4caf6e;">Copia</h1>

<p align="center">
  <a href="https://github.com/gitmobkab/copia/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/gitmobkab/copia/ci.yml?branch=main&style=for-the-badge&label=CI" alt="CI"></a>
  <a href="https://pypi.org/project/copia-seed/"><img src="https://img.shields.io/pypi/v/copia-seed?style=for-the-badge&color=#4caf6e" alt="PyPI"></a>
  <a href="https://pypi.org/project/copia-seed/"><img src="https://img.shields.io/pypi/pyversions/copia-seed?style=for-the-badge" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/gitmobkab/copia?style=for-the-badge" alt="License"></a>
  <a href="https://gitmobkab.github.io/copia/"><img src="https://img.shields.io/badge/docs-material-4caf6e?style=for-the-badge" alt="Docs"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge" alt="Ruff"></a>
</p>

---

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

## Why Copia

You have this table:

```sql
CREATE TABLE users (
  id           CHAR(36)      NOT NULL PRIMARY KEY,
  username     VARCHAR(50)   NOT NULL UNIQUE,
  email        VARCHAR(255)  NOT NULL UNIQUE,
  password     VARCHAR(255)  NOT NULL,
  role         ENUM('admin', 'editor', 'viewer') NOT NULL,
  created_at   DATE          NOT NULL
);
```

Without copia, seeding it looks like this:

```sql
INSERT INTO users (id, username, email, password, role, created_at)
VALUES
  ('a1b2c3d4-...', 'john_doe',    'john@example.com',  '$2b$12$...', 'admin',  '2023-04-12'),
  ('e5f6g7h8-...', 'jane_smith',  'jane@example.com',  '$2b$12$...', 'editor', '2024-01-05'),
  ('i9j0k1l2-...', 'bob_99',      'bob@example.com',   '$2b$12$...', 'viewer', '2022-11-30'),
  ('m3n4o5p6-...', 'alice_w',     'alice@example.com', '$2b$12$...', 'admin',  '2023-08-19'),
  ('q7r8s9t0-...', 'charlie_k',   'charlie@example.com','$2b$12$...','editor', '2024-03-02');
  -- ... 55 more rows. good luck with that.
```

With copia:

```
id:          uuid()
username:    username()
email:       email(safe=True)
password:    password(length=16)
role:        enum('admin', 'editor', 'viewer')
created_at:  past_date()
```

---

## Features

- **Simple language** — if you know what a function call looks like, you know the Copia DSL
- **Realistic data** — built on [Faker](https://faker.readthedocs.io/), 25+ generators out of the box
- **Relational-aware** — [`ref('table.column')`](https://gitmobkab.github.io/copia/generators/ref) samples from existing rows, so foreign keys just work
- **Interactive TUI** — write, preview, and insert without leaving your terminal
- **Extensible** — add your own generators with a single function

## Installation

```bash
pip install copia-seed
```

Requires Python 3.13+. MySQL and MariaDB are supported.

## Quickstart

```bash
copia init       # generate a config template
copia            # launch the TUI
```

## Documentation

→ [the official copia documentation is available here](https://gitmobkab.github.io/copia/)

---

## License

MIT

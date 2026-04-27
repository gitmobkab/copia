<p align="center">
  <img src="https://raw.githubusercontent.com/gitmobkab/copia/main/docs/assets/logo.svg" width="120" alt="Copia logo">
</p>

<h1 align="center">Copia</h1>

<p align="center">
  <a href="https://github.com/gitmobkab/copia/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/gitmobkab/copia/ci.yml?branch=main&style=for-the-badge&label=CI" alt="CI"></a>
  <a href="https://pypi.org/project/copia-seed/"><img src="https://img.shields.io/pypi/v/copia-seed?style=for-the-badge&color=4caf6e" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/gitmobkab/copia?style=for-the-badge" alt="License"></a>
  <a href="https://gitmobkab.github.io/copia/"><img src="https://img.shields.io/badge/docs-material-4caf6e?style=for-the-badge" alt="Docs"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge" alt="Ruff"></a>
  <a href="https://pypi.org/project/copia-seed/"><img src="https://img.shields.io/pypi/pyversions/copia-seed?style=for-the-badge&" alt="Python"></a>
</p>

---
<p align="center">
  <a href="https://gitmobkab.github.io/copia/">
    <img src="https://raw.githubusercontent.com/gitmobkab/copia/main/docs/assets/tui_layout.png" alt="Copia preview" width="800">
  </a>
</p>

<p align="center"><em>Copia's TUI, showing the editor, preview, and log panels.</em></p>

---
<p align="center">
  <strong>Seed your database without the hassle.</strong>
</p>

Most frameworks either ship a seeder that’s hard to use—or don’t ship one at all.

Copia is a TUI-based database seeder with its own declarative language:
describe your data once, and let Copia generate and insert it for you.

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

→ **[Read the documentation](https://gitmobkab.github.io/copia/)**

---

## License

MIT

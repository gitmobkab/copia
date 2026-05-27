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
  <a href="https://pypi.org/project/copia-seed/"><img src="https://img.shields.io/pypi/pyversions/copia-seed?style=for-the-badge" alt="Python"></a>
</p>

<p align="center"><strong>Seed your database without the hassle.</strong></p>

---

<p align="center">
  <a href="https://gitmobkab.github.io/copia/">
    <img src="https://raw.githubusercontent.com/gitmobkab/copia/main/docs/assets/tui_layout.png" alt="Copia TUI preview" width="800">
  </a>
</p>

<p align="center"><em>Editor, preview, and log panels — all in your terminal.</em></p>

---

Seeding a database with realistic data is tedious. Most frameworks ship a seeder with questionable decisions, or don't ship one at all.

Copia gives you a declarative language and a TUI to describe, preview, and insert data — without boilerplate, without framework dependency.

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

Without Copia:

```sql
INSERT INTO users (id, username, email, password, role, created_at)
VALUES
  ('a1b2c3d4-...', 'john_doe',   'john@example.com',   '$2b$12$...', 'admin',  '2023-04-12'),
  ('e5f6g7h8-...', 'jane_smith', 'jane@example.com',   '$2b$12$...', 'editor', '2024-01-05'),
  ('i9j0k1l2-...', 'bob_99',     'bob@example.com',    '$2b$12$...', 'viewer', '2022-11-30'),
  ('m3n4o5p6-...', 'alice_w',    'alice@example.com',  '$2b$12$...', 'admin',  '2023-08-19'),
  ('q7r8s9t0-...', 'charlie_k',  'charlie@example.com','$2b$12$...', 'editor', '2024-03-02');
  -- ... 55 more rows. good luck with that.
```

With Copia:

```
id:          uuid()
username:    username()
email:       email(safe=True)
password:    password(length=16)
role:        enum('admin', 'editor', 'viewer')
created_at:  past_date()
```

```bash
copia run --table users users.copia --rows 60
```

Done.

## Features

- **Simple language** — if you know what a function call looks like, you know the Copia DSL
- **Realistic data** — built on [Faker](https://faker.readthedocs.io/), 25+ generators out of the box
- **Relational-aware** — `fetch('table.column')` samples from existing rows, so foreign keys just work
- **Interactive TUI** — write, preview, and insert without leaving your terminal
- **Scriptable** — pipe input, dump to JSON/CSV/SQL, skip confirmation prompts

## Installation

```bash
pip install copia-seed
```

Requires Python 3.10+. MySQL and MariaDB included. PostgreSQL available as an optional dependency.

## Quickstart

```bash
copia init      # create a config file
copia tui       # launch the interactive TUI
```

Or run directly from the CLI:

```bash
copia run --dumps json users.copia --skip-config
echo "id:uuid() name:username()" | copia run --dumps json --skip-config
```

## Usage

For detailed usage instructions, see the [CLI documentation](cli.md).

copia's main entry point is the `copia` command, which has several subcommands for different tasks:
- `copia tui` : launch the interactive TUI (requires a valid config profile)
- `copia run` :  parse and run a file content, with options for dumping output, skipping confirmation, and more
- `copia list` : list all available profiles in the config files
- `copia init` : create a new config file with a default profile

## Configuration

Copia config files are TOML files that define what we call "profiles".

Those profiles are just named sets of configuration values, that tell copia how to connect to the database.

a config file can have multiples profiles and usually looks like this:

```toml
[profiles.default]
adapter = "mysql"
host = "localhost"
port = 3306
database = "mydb"
user = "root"

[profiles.staging]
adapter = "postgres"
host = "staging-db.example.com"
port = 5432
database = "stagingdb"
user = "admin"
password = "Y@urRe@lly$trongP@ssw0rd"
```

any command that takes a profile name as an argument or flag will assume the "default" profile if the name is not provided, so in the example above, both `copia tui` and `copia tui staging` will work without issues.

### Scopes

copia supports two scopes for configuration profiles: `global` and `local`.

the global config file is usually located at `{CONFIG_DIR}/copia/profiles.toml` and is meant to store profiles that are shared across all your projects.

while the local config file is located at `.copia.toml` in your project directory and is meant to store profiles that are specific to that project.

In some situations, you might want to limit the search for profiles to a specific config file. 

For example you might have a profile named "staging" in both your global and local config files, but with different connection details, and you want to make sure you're using the one in the global config file.



## Documentation

→ **[For more details on copia see the documentation](https://gitmobkab.github.io/copia/)**

---

MIT License
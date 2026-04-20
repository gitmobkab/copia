# Configuration

Copia is configured via a TOML file. Each entry defines a **profile** — a named set of connection parameters for a database.

---

## Config file locations

Copia looks for config in two places:

| Flag | Path |
|------|------|
| `--local` (default) | `.copia.toml` in the current directory |
| `--global` | System config directory — see below |

**Global config path by OS:**

| OS | Path |
|----|------|
| Linux | `$XDG_CONFIG_HOME/copia/profiles.toml` (usually `~/.config/copia/profiles.toml`) |
| macOS | `~/Library/Application Support/copia/profiles.toml` |
| Windows | `%APPDATA%\copia\profiles.toml` |

Use `copia init` to generate a template in the current directory.

---

## Profile structure

```toml title=".copia.toml"
[profiles.default]
adapter = "mysql"
host = "localhost"
port = 3306
database = "mydb"
user = "root"
# password = ""
```

All fields are required except `password`, which defaults to an empty string.

---

## Fields

### `adapter`

The database adapter to use.

| Value | Database |
|-------|----------|
| `"mysql"` | MySQL / MariaDB |

```toml
adapter = "mysql"
```

### `host`

The database host. Accepts:

- A hostname — `"localhost"`, `"db.example.com"`
- An IPv4 address — `"127.0.0.1"`
- An IPv6 address — `"::1"`

```toml
host = "localhost"
host = "127.0.0.1"
host = "::1"
```

### `port`

The port number. Must be a valid port (1–65535).

```toml
port = 3306
```

### `database`

The name of the target database. Must be non-empty and contain ASCII characters only.

```toml
database = "myapp_dev"
```

### `user`

The database user. Must be non-empty and contain ASCII characters only.

```toml
user = "root"
```

### `password`

The database password. Optional — defaults to `""`.

```toml
password = "secret"
```

---

## Multiple profiles

You can define as many profiles as you need.

```toml
[profiles.default]
adapter = "mysql"
host = "localhost"
port = 3306
database = "myapp_dev"
user = "root"

[profiles.staging]
adapter = "mysql"
host = "staging.db.example.com"
port = 3306
database = "myapp_staging"
user = "admin"
password = "secret"
```

Switch between profiles with the `--profile` flag:

```bash
copia --profile staging
```

---

## TOML edge cases

### Profile names with special characters

Profile names that contain spaces or special characters must be quoted in TOML:

```toml
[profiles."my profile"]
adapter = "mysql"
...
```

Then referenced as:

```bash
copia --profile "my profile"
```

### Extra fields are forbidden

Copia will reject any profile that contains unknown fields:

```toml
[profiles.default]
adapter = "mysql"
host = "localhost"
port = 3306
database = "mydb"
user = "root"
timeout = 30  # ❌ not a valid field, copia will raise an error
```

### ASCII constraint on `database` and `user`

The `database` and `user` fields must contain ASCII characters only.
Non-ASCII characters — including accented letters and Unicode — will be rejected:

```toml
user = "rené"   # ❌ invalid
user = "rene"   # ✓
```
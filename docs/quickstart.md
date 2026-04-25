# Quickstart

## 1. Initialize a config file

```bash
copia init
```

This creates a `.copia.toml` template in the current directory.

```toml title=".copia.toml"
[profiles.default]
adapter = "mysql"
host = "localhost"
port = 3306
database = "mydb"
user = "root"
# password = ""
```

Edit it to match your database. You can define multiple profiles — one per environment or database.

Copia looks for config in two places:

- **Local** — `.copia.toml` in the current directory
- **Global** — {system config directory}/copia/profiles.toml (see below) 

=== "Linux"

    `$XDG_CONFIG_HOME/copia/profiles.toml` (usually `~/.config/copia/profiles.toml`)

=== "macOS"

    `~/Library/Application Support/copia/profiles.toml`

=== "Windows"

    `%APPDATA%\copia\profiles.toml`

---

## 2. Launch Copia

```bash
copia
```

This uses the `default` profile from your config. To use a different profile:

```bash
copia --profile staging
```

To force local or global config lookup:

```bash
copia --local    # only reads .copia.toml
copia --global   # only reads the global config
```

---

## 3. Pick a table

The left panel shows all tables in your database. Select the one you want to seed.

---

## 4. Write your seed

In the editor, describe each column using the Copia DSL — one line per column.

```
id:         uuid()
username:   username()
email:      email(safe=True)
password:   password(length=16)
created_at: past_date()
```

Press `?` at any time to open the help screen — full DSL reference and all available generators.

---

## 5. Run and insert

- Click **Run** to generate a preview of the rows.
- Review the results in the table below the editor.
- Click **Submit** to insert the rows into the database.

---

## Next steps

- [DSL Reference](dsl.md) — full language documentation
- [CLI Reference](cli.md) — all available commands and options
- [Generators](generators/index.md) — all available generators and their parameters
- [Configuration](configuration/index.md) — profiles, adapters, and options
# CLI Reference

Copia is invoked from the command line. All commands share a common set of options for selecting the database profile and config file scope.

---

## `copia`

Launch the interactive TUI.

```bash
copia [OPTIONS]
```

**Options**

| Option | Short | Description |
|--------|-------|-------------|
| `--profile TEXT` | `-p` | Profile to use for the session. Defaults to `default`. |
| `--global` | `-g` | Search only in the global config file. |
| `--local` | `-l` | Search only in `.copia.toml` in the current directory. |
| `--version` | `-v` | Display the current version and exit. |
| `--help` | `-h` | Display this message and exit. |

**Examples**

```bash
# Launch with the default profile
copia

# Launch with a specific profile
copia --profile staging

# Force lookup in the global config only
copia --global --profile "production db"
```

!!! note "Profile fallback"
    When launching the TUI, copia silently falls back to the global config if the local profile is missing or invalid. [Use `copia list`](#copia-list) to inspect the state of both config files before launching.

---

## `copia init`

Generate a template config file.

```bash
copia init [OPTIONS]
```

By default, creates a local `.copia.toml` in the current directory.

**Options**

| Option | Short | Description |
|--------|-------|-------------|
| `--global` | `-g` | Create the config file in the global config directory instead. |
| `--help` | `-h` | Display this message and exit. |

**Examples**

```bash
# Create a local config file
copia init

# Create a global config file
copia init --global
```

---

## `copia list`

List all profiles defined across both global and local config files.

```bash
copia list
```

**Options**

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Display this message and exit. |

**Output**

`copia list` reads both config files and displays all found profiles. It also reports issues it encounters:

- **Warning** — a key under `[profiles]` is not a valid table (e.g. `profiles.key = ""`).
- **Error** — a profile table exists but fails validation (e.g. missing required field, invalid host).

This makes `copia list` useful for debugging your config before launching the TUI.

**Example**

```bash
copia list
```

```
[ LOCAL PROFILES ]
  ✓ default - (mysql) <localhost:3306>
  ✗ profiles.staging
        Reason:
            port : Input should be a valid integer

--- SUMMARY ---
    2 total profiles
    1 valid profiles
    1 invalid profiles
    0 warnings

[ GLOBAL PROFILES ]
  ✓ default - (mysql) <localhost:3306>

--- SUMMARY ---
    1 total profiles
    1 valid profiles
    0 invalid profiles
    0 warnings
```

---

## Shell completion

Copia supports shell completion via Typer.

```bash
# Install completion for your current shell
copia --install-completion

# Print the completion script without installing
copia --show-completion
```

Supported shells: Bash, Zsh, Fish, PowerShell.
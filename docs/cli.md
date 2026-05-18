# CLI Reference

When you install copia-seed, a command will be available on your shell.

The command `copia` documented below.

---

## `copia`

The entrypoint of the cli app.

Doesn't really do anything just print the version 

```bash
copia [OPTIONS] COMMAND [ARGS]...
```

### **Options**

| Long name | Short name | Description |
|--------|-------|-------------|
| `--version` | `-v` | Display the current version and exit. |
| `--install-completion` | | Install completion for the current shell. |
| `--show-completion` | | Show completion for the current shell, to copy it or customize the installation. |
| `--help` | `-h` | Display this message and exit. |


### **Commands**

| Name | Description |
|------|-------------|
| `init` | Generate a template config file for copia. |
| `list` | List all profiles defined in both global and local config files. |
| `tui` | Launch the interactive tui. |
| `run` | Parse and run a file content. |


### Shell completion

Copia supports shell completion via Typer.

```bash
# Install completion for your current shell
copia --install-completion

# Print the completion script without installing
copia --show-completion
```

Supported shells: Bash, Zsh, Fish, PowerShell.
---

## Commands

### `copia init`

Generate a template config file.

#### **Usage:** `copia init [OPTIONS]`

By default, creates a local `.copia.toml` in the current directory.

#### **Options**

| Long name | Short name | Description |
|--------|-------|-------------|
| `--global` | `-g` | Create the config file in the global config directory instead. |
| `--help` | `-h` | Display this message and exit. |

#### **Examples**

```bash
# Create a local config file
copia init

# Create a global config file
copia init --global
```

---

### `copia list`

List all profiles defined across both global and local config files.

#### **Usage:** `copia list [OPTIONS]`

#### **Options**

| Long name | Short name | Description |
|--------|-------|-------------|
| `--help` | `-h` | Display this message and exit. |

#### **Output**

`copia list` reads both config files and displays all found profiles. It also reports issues it encounters:

- **Warning** — a key under `[profiles]` is not a valid table (e.g. `profiles.key = ""`).
- **Error** — a profile table exists but fails validation (e.g. missing required field, invalid host).

This makes `copia list` useful for debugging your config before launching the TUI.

#### **Example**

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

### `copia tui`

Launch the interactive tui.

#### **Usage:** `copia tui [OPTIONS] [PROFILE_NAME]`

#### **Arguments**

| Name         | Type   | Description                                    | Default   |
|--------------|--------|------------------------------------------------|-----------|
| `profile_name` | `string` | the name of the profile to use for the session | `"default"` |


#### **Options**

| Long name | Short name | Description |
|------|-------|-------------|
| `--global` | `-g` | Search only in the global config |
| `--local` | `-l` | Search only in the local config |
| `--help` | `-h` | Show the help menu and exit |

#### **Examples**

```bash
copia tui

copia tui staging

copia tui -g # (1)!

copia tui -g "mark-and-deceive" # (2)!
```

1. look for the profile named "default" **only** in the global config file
2. look for the profile named "mark-and-deceive" **only** in the local config, no fallback to the global config


### `copia run`

Parse and run a file content

#### **Usage:** `copia run [OPTIONS] [FILE]`

#### **Arguments**

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `file` | `string` | the path of the file to parse and run | `"-"` |

!!! tip "Using pipes to run a seed"
    you can also directly pipe the content to parse via a pipe, when passing `"-"` as the file path.
    `echo "uuid:uuid()" | copia run`

#### **Options**

| Long name | Short name | Type | Description | Default |
|-----------|------------|------|-------------|---------|
| `--table` | `-t` | `string` | the name of the table to commit to. mandatory without the --dumps flag. | |
| `--profile` | `-p` | `string` | the name of the profile to use for the run. | `"default"` |
| `--global` | `-g` | | search only in the global config | |
| `--local` | `-l` | | search only in the local config | |
| `--dumps` | `-d` | `("json", "csv", "sql")` | dumps the generated values based on the selected formatter | |
| `--skip-config` | `-s` | | disable config lookup for the run. this will cause an error if the 'fetch' generator is detected. | |
| `--rows` | `-n` | `integer >= 1` | the number of rows for the run. | `10` |
| `--skip-confirm` | `-S` | | Skip the confirmation prompt. directly commit the values to the db. |
| `--help` | `-h` | | Show the help menu and exit.


#### **Examples** 

- How to use the file argument

```bash title="users.copia"
id: uuid()
name: name()
age: int(0, 50)
```

```bash
# launching a run with the file "users.copia"
copia run --table users users.copia

# using piping instead (implicit)
cat users.copia | copia run --table users --skip-confirm

# using piping instead (explicit)
cat users.copia | copia run --table users --skip-confirm - # (1)!
```

1. 
    - since we're using pipes. `--skip-confirm` will tell copia directly to commit.
    This is required or you'll get an error!

    - the `"-"` at the end tell copia to read from the pipes rather than expect a file path.


!!! important "when the `--skip-confirm` flag is useful"
    By default copia will show you a confirmation prompt to ask if you really want to commit the values.
    This behavior is always going to lead to a crash/panic if you use a pipe for the input.
    Adding the flag `--skip-confirm` flag will prevent this. useful when scripting too.

- dumping rather than seeding

```bash
copia run --dumps json --skip-config users.copia # (1)!

copia run --dumps sql users.copia # (2)!

echo "user_id:fetch('users.id')" | copia run --dumps json --skip-config # (3)!
```

1. this will dumps the generated values in a json format and skip the config
2. this will dumps but still perform the config lookup step
3. this won't work because the `fetch generator` require a db connexion to work


**Rules**

1. the `--table` flag is mandatory if the `--dumps` flag is missing
2. the `--skip-config` flag can only be used with the `--dumps` flag

## Exit Codes

Copia uses structured exit codes to make scripting and error handling predictable.

| Code | Name | Description |
|------|------|-------------|
| `0` | `SUCCESS` | Everything went fine. |
| `1` | `UNEXPECTED_ERROR` | An unplanned error occurred. |
| `2` | `BAD_CLI_USAGE` | Invalid arguments, unknown options, or option values that fail validation. |
| `3` | `BAD_DSL_INPUT` | The DSL input could not be parsed or validated. |
| `4` | `VALIDATION_ERROR` | A resource failed validation — malformed config file, invalid profile, etc. |
| `5` | `RESOURCE_ERROR` | A required external resource is missing — config file not found, missing dependency, etc. |
| `6` | `CONNEXION_TO_DB_REFUSED` | The connection attempt to the database was refused. |
| `7` | `GENERATION_ERROR` | An error occurred while generating values. |
| `8` | `SEEDING_ERROR` | The insertion of generated rows into the database failed. |

These codes are stable across versions and safe to use in scripts.
# Installation

Copia requires **Python 3.13 or higher**.

=== "uv"

    ```bash
    uv add copia-seed
    ```

    Or as a standalone tool:

    ```bash
    uv tool install copia-seed
    ```

=== "pip"

    ```bash
    pip install copia-seed
    ```

=== "pipx"

    ```bash
    pipx install copia-seed
    ```

=== "From source"

    we recommend [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to download the repo from source

    ```bash
    git clone https://github.com/gitmobkab/copia
    cd copia
    uv sync --all-groups
    ```

---

## Verify

```bash
copia --version
```

---

## Database support

Copia v1 supports **MySQL and MariaDB** out of the box. PostgreSQL support is planned for a future release.
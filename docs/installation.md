# Installation

Copia requires **Python 3.13 or higher**.

=== "uv"

    ```bash
    uv add copia
    ```

    Or as a standalone tool:

    ```bash
    uv tool install copia
    ```

=== "pip"

    ```bash
    pip install copia
    ```

=== "pipx"

    ```bash
    pipx install copia
    ```

=== "From source"

    ```bash
    git clone https://github.com/gitmobkab/copia
    cd copia
    pip install -e .
    ```

---

## Verify

```bash
copia --version
```

---

## Database support

Copia v1 supports **MySQL and MariaDB** out of the box. PostgreSQL support is planned for a future release.
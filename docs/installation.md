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

Copia come with supports for **MySQL and MariaDB** out of the box. 

To use copia with other dbs, you can install the corresponding adapter optional dependency

for example on pip, the following command `pip install "copia-seed[postgres]"` will install the postgres adapter for copia

### Additional adapters

Those aren't pre-installed adapters.

| Adapter name | Database |
|--------------|----------|
| `postgres` | postgreSQL |
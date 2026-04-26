# Docstring Format

Copia parses generator docstrings to build the in-app help and the documentation site. The format is a subset of Google-style docstrings with one Copia-specific addition.

---

## Structure

```python
def my_generator(param: str = "default") -> str:
    """Short description of what the generator produces.

    Locale dependent:
        yes

    Args:
        param: Description of the parameter. Defaults to 'default'.

    Returns:
        Description of the returned value.

    Note:
        Optional warning or constraint the user should know about.
    """
```

---

## Sections

### Description

The first lines before any section header. Keep it short — one or two sentences. This is the most important part of the docstring, as it gives users a quick understanding of what the generator does.

```python
"""Generate a random job title."""
```

### `Locale dependent`

Indicates whether the output varies based on the active generation locale. Must be `yes` or `no`.

```
Locale dependent:
    yes
```

If omitted, the generator is assumed to be locale-independent.

!!! note title="Not entirely strict"
    To be honest, if the line below Locale dependent is not exactly `yes` it's treated as `no`. But it's best to follow the format strictly to avoid confusion.

### `Args`

Documents each parameter. One line per parameter in the format `name: description.`
if the parameter has a default value, include it in the description for clarity. The type is inferred from the function signature — do not repeat it here.

```
Args:
    length: Number of characters. Defaults to 12.
    special_chars: Include special characters. Defaults to True.
```

### `Returns`

A single line describing the returned value. The type is inferred from the return annotation — do not repeat it here.

```
Returns:
    A randomly generated username string.
```

### `Note`

An optional warning or constraint. Use sparingly — only for things that could cause runtime errors or surprising behavior.

```
Note:
    Only uses values already present in the database.
    An empty column will raise an error at runtime.
```

---

## What gets rendered

The parser extracts these sections and renders them as:

- A signature blockquote
- A description paragraph
- A locale dependent checkbox
- An arguments table
- A returns line
- A warning blockquote for notes
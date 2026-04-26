# Adding a Generator

Generators are plain Python functions registered in the `GENERATORS_REGISTRY`. Adding one requires writing the function, documenting it, and placing it in the right module.

---

## 1. Write the function

A generator is a regular Python function. It must follow these rules:

- It must have a return type annotation
- It must only use types compatible with SQL — `str`, `int`, `float`, `bool`, `date`, `datetime`, `UUID`
- It must not use `**kwargs`
- It may use `*args` (var positional), but not simultaneously with other positional-or-keyword parameters

```python
from copia.generators._core import get_faker

def job() -> str:
    return get_faker().job()
```

Use `get_faker()` to access the global Faker instance. This ensures the generator respects the active locale and generation settings.

---

## 2. Document it

Follow the [docstring format](docstrings.md) to document the generator. Copia uses the docstring to generate the in-app help and the documentation site.

```python
def job() -> str:
    """Generate a random job title.

    Locale dependent:
        yes

    Returns:
        A random job title string.
    """
    return get_faker().job()
```

---

## 3. Register it

Place the function in the appropriate module under `src/copia/generators/` and the rest will be automatically handled by `src/copia/generators/__init__.py`

---

## 4. Verify

1. Run the test with `pytest tests/test_generators_discover.py` to ensure there are no import warnings or errors related to your new generator.

2. Run `copia` and press `?`. to check how your generator docstring looks in the in-app help. If you see any formatting issues, adjust your docstring accordingly.
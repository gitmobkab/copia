# The `generators_registry` System

in the `generators/__init__.py` file 

there's a function called `_build_generators_registry`.
this function is responsible for dynamically building the registry of generators based on a few rules and conventions.

---

## How it works

- when the module is imported, `_build_generators_registry` is called to populate the `GENERATORS_REGISTRY` dictionary.

- it scans the module's global namespace (copia.generators) for all non private modules (those that don't start with `_`).

- for each module, it looks for all non private functions defined in that module. (again, those that don't start with `_`).

- each function is registered in the `GENERATORS_REGISTRY` with its name as the key and the function object as the value.

!!! note "Automatic discovery"
    all this happens automatically when you import the generators module. You don't need to do anything special to register your generator — just define it in a non-private module and it will be picked up.

---

## Constraints

### No overriding

A generator name must be globally unique. If a function with the same name is already registered, `discover()` raises a `ImportWarning`.

```python
Traceback (most recent call last):
    ImportWarning: found overrinding generator func at copia.generators.address with identifier city
```

### No `**kwargs`

Generators must not use `**kwargs`. The DSL only supports positional and named arguments — variadic keyword arguments are not representable in the grammar.

```python
# Invalid
def my_gen(**kwargs) -> str: ...
```

### `*args` and named parameters are mutually exclusive

A generator may use either `*args` (var positional) or POSITIONAL_OR_KEYWORD parameters — but not both simultaneously.

```python
# Valid — only *args
def enum(*args) -> Any: ...

# Valid — only POSITIONAL_OR_KEYWORD params
def email(safe: bool = True, domain: str = "") -> str: ...

# All Valids — *args with only named params
def enum(*args, extra: str) -> str: ...
def yet_another_gen(*args, extra: str = "") -> str: ...

# Invalid — POSITIONAL_OR_KEYWORD params with *args (var positional)
def invalid_gen(extra: str, *args) -> str: ...

# WHY ? Because the Semantic Validator for the DSL cannot currently handle this combination. It would require a more complex parsing logic to determine which arguments are meant for `*args` and which are actual positionals parameters, especially since the user can pass any number of values for `*args`. To keep things simple and unambiguous, we enforce this constraint.
```

!!! note "About union types"
    The current implementation of the docstring parser and the semantic validator does not support union types (e.g., `str | int`) in generator signatures. This will be updated in future updates. and no, even Any is not supported too.

---

## Adding new generators

To add a new generator, simply define a function in any non-private module under `copia.generators` and ensure it follows the constraints outlined above. The function will be automatically registered and available for use in the DSL.

first check if the module you want to add the generator to already exists. If it does, add your function there. If not, create a new module and add your function there.

since the registry is built dynamically, you don't need to do anything else to make your generator available — just define it and it will be picked up when the module is imported.

to ensure your generator is properly documented, follow the docstring format outlined in the [docstrings guide](./docstrings.md). This will help users understand how to use your generator and what it does.

and to finish, simply run pytest tests/test_generators_discover.py to avoid any import warnings or errors related to your new generator. If you see an ImportWarning about overriding a generator, it means you have a naming conflict — either rename your generator or remove the conflicting one. If you see an error about `**kwargs` or invalid parameter combinations, adjust your function signature accordingly.

> just keep in mind, the function signature is a direct interface to users, so keep it simple and intuitive. Avoid complex parameter combinations that could confuse users or make the generator difficult to use in the DSL. The goal is to provide a clear and straightforward way for users to generate data without having to worry about the underlying implementation details.
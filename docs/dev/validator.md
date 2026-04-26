# The Semantic Validator

The semantic validator checks that a parsed DSL call is valid against the registered generator signatures. It runs after parsing and before generation.

---

## What it validates

Given a `GeneratorCall` from the parser, the validator checks:

- The generator name exists in `GENERATORS_REGISTRY`
- The number of positional arguments does not exceed what the signature accepts
- All named arguments exist in the signature
- The types of all arguments match the parameter annotations

If any check fails, the validator raises a typed exception that the TUI catches and displays in the results viewer.

---

## Errors

| Exception | Cause | Can be skipped? |
|-----------|-------|-----------------|
| `UnknownGeneratorError` | The generator name is not in the registry | Never |
| `TooManyPositionalsError` | More positional args than the signature accepts | Only for *args generators |
| `UnknownNamedParamError` | A named argument does not exist in the signature | Never |
| `MissingRequiredParamError` | A required parameter was not provided | Never |
| `TypeMismatchError` | An argument type does not match the annotation | Never |
| `PositionalNamedCollisionError` | A parameter is passed both positionally and by name | Only for *args generators |

---

## Type checking

The validator maps DSL argument types to Python types:

| DSL value | Python type |
|-----------|-------------|
| `42` | `int` |
| `3.14` | `float` |
| `'hello'` | `str` |
| `True` / `False` | `bool` |

`Literal` annotations are checked by value — the argument must be one of the allowed values.

---

## Var positional generators

Generators that use `*args` (like `enum`) bypass the arity check — any number of positional arguments is valid. The type of each argument is still checked against the parameter annotation if present.

---

## When validation runs

Validation runs once when the user clicks **Run**, before any generation starts. If validation fails, no rows are generated and the error is displayed in the logs tab.
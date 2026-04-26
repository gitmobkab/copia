# Developer Guide

This section documents the internals of Copia for contributors and developers who want to extend it.

---

## Contents

- [Adding a generator](generators.md) — how to write and register a new generator
- [Docstring format](docstrings.md) — the docstring convention Copia uses to generate documentation
- [The dynamic generators system](generators_registry.md) — how generators are registered and what constraints apply
- [The semantic validator](validator.md) — how Copia validates DSL calls against generator signatures
- [How `ref` works](ref.md) — the internals of the `ref()` generator
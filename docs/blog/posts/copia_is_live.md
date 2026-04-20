---
date: 2026-04-20
tags:
  - v1
  - release
---

# Copia is finally live!

After way too long, Copia is out.

It's a TUI-based database seeder with its own small declarative language. You describe what you want column by column, it generates realistic data and inserts it. No framework required, no boilerplate.

I won't pretend this was a quick side project — it took longer than I'd like to admit. But I wanted it to actually work before shipping it, and I'm genuinely happy with where it landed.

<!-- more -->

## What's in v1

- MySQL and MariaDB support
- 25+ built-in generators — names, emails, UUIDs, dates, IPs, lorem ipsum, and more
- `ref('table.column')` to sample from existing rows — foreign keys just work
- A full TUI with live preview before inserting
- A help screen with the full DSL reference and generator list, accessible with `?`

## What's next

PostgreSQL support is the obvious next step. Beyond that — more generators, better error messages, and generally making the rough edges less rough.

If you run into anything broken or missing, open an issue.

### btw, Material for MkDocs is fantastic. Highly recommend if you're building docs with MkDocs.
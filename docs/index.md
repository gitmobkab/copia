# Copia

**Seed your database without the hassle.**

Most frameworks either ship a seeder with questionable decisions, or don't ship one at all. Either way, populating a database with realistic data is tedious — and it shouldn't be.

Copia is a TUI-based database seeder with its own declarative language. You describe what data you want, column by column. Copia generates it and inserts it — no boilerplate, no framework dependency.

```
id:         uuid()
username:   username()
email:      email(safe=True)
password:   password(length=20)
role:       enum('admin', 'editor', 'viewer')
created_at: past_date()
```

That's it. That's a table seed.

---

## Why Copia

- **Framework-agnostic.** Works on any relational database, any stack.
- **Simple language.** If you know what a function call looks like, you know the Copia DSL.
- **Realistic data.** Built on [Faker](https://faker.readthedocs.io/) — names, emails, addresses, IPs, dates, and more out of the box.
- **Relational-aware.** The `ref()` generator lets you sample from existing rows, so foreign keys just work.
- **Interactive.** A full TUI lets you write, preview, and insert without leaving your terminal.

---

## Quick example

```
# seed the users table
id:         uuid()
username:   username()
email:      email()
birthdate:  date_of_birth()

# seed the posts table — references existing users
id:      uuid()
user_id: ref('users.id')
body:    paragraph()
date:    past_date()
```

---

## Get started

→ [Installation](installation.md)  
→ [Quickstart](quickstart.md)  
→ [DSL Reference](dsl.md)
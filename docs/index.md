# Copia

**Seed your database without the hassle.**

Most frameworks either ship a seeder with questionable decisions, or don't ship one at all. Either way, populating a database with realistic data is tedious — and it shouldn't be.

Copia is a TUI-based database seeder with its own declarative language. You describe what data you want, column by column. Copia generates it and inserts it — no boilerplate, no framework dependency.

---

## Why Copia

You have this table:

```sql
CREATE TABLE users (
  id           CHAR(36)      NOT NULL PRIMARY KEY,
  username     VARCHAR(50)   NOT NULL UNIQUE,
  email        VARCHAR(255)  NOT NULL UNIQUE,
  password     VARCHAR(255)  NOT NULL,
  role         ENUM('admin', 'editor', 'viewer') NOT NULL,
  created_at   DATE          NOT NULL
);
```

Without copia, seeding it looks like this:

```sql
INSERT INTO users (id, username, email, password, role, created_at)
VALUES
  ('a1b2c3d4-...', 'john_doe',    'john@example.com',  '$2b$12$...', 'admin',  '2023-04-12'),
  ('e5f6g7h8-...', 'jane_smith',  'jane@example.com',  '$2b$12$...', 'editor', '2024-01-05'),
  ('i9j0k1l2-...', 'bob_99',      'bob@example.com',   '$2b$12$...', 'viewer', '2022-11-30'),
  ('m3n4o5p6-...', 'alice_w',     'alice@example.com', '$2b$12$...', 'admin',  '2023-08-19'),
  ('q7r8s9t0-...', 'charlie_k',   'charlie@example.com','$2b$12$...','editor', '2024-03-02');
  -- ... 55 more rows. good luck with that.
```

With copia:

```
id:          uuid()
username:    username()
email:       email(safe=True)
password:    password(length=16)
role:        enum('admin', 'editor', 'viewer')
created_at:  past_date()
```

Run it for as many rows as you need. Thanks to Faker every value is realistic, fetched from a rich dataset, and valid.

- **Framework-agnostic.** Works on any relational database, any stack.
- **Simple language.** If you know what a function call looks like, you know the Copia DSL.
- **Realistic data.** Built on [Faker](https://faker.readthedocs.io/) — names, emails, addresses, IPs, dates, and more out of the box.
- **Relational-aware.** The [`ref()`](generators/ref.md) generator lets you sample from existing rows, so foreign keys just work.
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
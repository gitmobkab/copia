from copia.cli.config import Profile

VALID_PROFILE = {
    "adapter": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "mydb",
    "user": "admin",
    "password": "secret",
}


def make_profile(**overrides) -> Profile:
    return Profile(**{**VALID_PROFILE, **overrides})
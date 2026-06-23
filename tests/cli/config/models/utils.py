from copia.cli.config import ServerBasedProfile

VALID_PROFILE = {
    "adapter": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "mydb",
    "user": "admin",
    "password": "secret",
}


def make_profile(**overrides) -> ServerBasedProfile:
    return ServerBasedProfile(**{**VALID_PROFILE, **overrides})
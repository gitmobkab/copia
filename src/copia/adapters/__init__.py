from .base_adapter import BaseAdapter
from copia.cli.config import Profile


def get_adapter(profile: Profile) -> BaseAdapter: # type: ignore
    profile_info = get_profile_info(profile)
    if profile.adapter == "mysql":
        from .mysql_adapter import MySQLAdapter
        return MySQLAdapter(**profile_info)
    elif profile.adapter == "postgres":
        from .postgres_adapter import PostgresAdapter
        return PostgresAdapter(**profile_info)
    

def get_profile_info(profile: Profile) -> dict:
    return profile.model_dump(exclude={"adapter"})
from .base_adapter import BaseAdapter
from copia.cli.config import BaseProfile


def get_adapter(profile: BaseProfile) -> BaseAdapter: 
    profile_info = get_profile_info(profile)
    if profile.adapter == "mysql":
        from .mysql_adapter import MySQLAdapter
        return MySQLAdapter(**profile_info)
    elif profile.adapter == "postgres":
        from .postgres_adapter import PostgresAdapter
        return PostgresAdapter(**profile_info)
    elif profile.adapter == "sqlite":
        from .sqlite_adapter import SQLiteAdapter
        return SQLiteAdapter(**profile_info)
    raise ValueError(f"unknown adapter, {profile.adapter}")

def get_profile_info(profile: BaseProfile) -> dict:
    return profile.model_dump(exclude={"adapter"})
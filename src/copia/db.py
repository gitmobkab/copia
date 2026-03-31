from sqlalchemy import create_engine, URL, Connection

from copia.cli.config import Profile


def connect_to_db(profile: Profile) -> Connection:
    """connect to a database using the given profile information
    
    multiple errors can be raised while attempting to connect,
    
    the caller is expected to handle them

    Args:
        profile (Profile): the profile to use for the connection

    Returns:
        Connexion: the connextion to the database
    """
    
    connection_url = URL.create(
        drivername=profile.adapter_scheme,
        username=profile.user,
        password=profile.password,
        host=str(profile.host),
        port=profile.port,
        database=profile.database
    )
    
    return create_engine(connection_url).connect()


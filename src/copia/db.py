from sqlalchemy import create_engine, URL, Engine, text

from copia.cli.config import Profile


def create_profile_engine(profile: Profile) -> Engine:
    """create an engine using the given profile informations
    
    Note: the returned engine does not guarantee a successful connection to the database,
    
    use verify_engine_connection to ensure that
    
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
    
    return create_engine(connection_url)

def verify_engine_connection(engine: Engine) -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
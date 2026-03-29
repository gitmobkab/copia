"""package from write only access of the config files,

    the functions in this module must be called only for writing profiles relevant information
    
    the functions ensure to preserve the integrity of the config files, 
    this means keeping comments, positions of keys and so on.
    
    see loaders.py to get load informations about a profile 
"""
from pathlib import Path
import time

from tomlkit import document, table, comment, nl
from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile
from tomlkit.items import Table

from .utils import resolve_config_path
from ..config import (
    CONFIG_SCOPES,
    COPIA_CONFIG_FILE_DOC_LINK,
    COPIA_CONFIG_FILE_SCHEME,
    InvalidConfigError,
    ProfileAlreadyExists,
    NoProfilesFoundError,
    Profile
)

def get_toml_file(path: Path) -> TOMLFile:
    """get a raw TOMLFile from the specified path, this should be used for writing and modyfing data

    Args:
        path (Path): the path to use for the TOMLFile

    Returns:
        TOMLFile: the corresponding TOMLFile
    """
    return TOMLFile(path)

def save_new_profile(new_profile_name: str, profile_data: Profile, scope: CONFIG_SCOPES) -> Path:
    """save a new profile to the config specified by scope.
    
    it creates the file if missing and append the new profile otherwise

    Args:
        new_profile_name (str): the name of the new profile to add
        profile_data (Profile): the new profile data
        scope (CONFIG_SCOPES): the scope of the config file to write to
        
    Returns:
        Path: the path it wrote to
    """
    config_path = resolve_config_path(scope)
    config_file = get_toml_file(config_path)
    config_content = config_file.read()
    new_config = add_new_profile_to_config(new_profile_name, profile_data, config_content)
    save_toml_to_path(new_config, config_path)
    return config_path


def create_new_config_file(profile_name: str,
                           profile_data: Profile,
                           scope: CONFIG_SCOPES,
                           force_overwrite: bool = False) -> Path:
    """create a new config file based on the scope of the config file.
    
    By default it will raise FileExistsError if the config file already exist.
    This can be disabled via force_overwrite

    Args:
        profile_name (str): the name of the profile to include when creating the new config
        profile_data (Profile): the data of the profile
        scope (CONFIG_SCOPES): the scope of the config file
        force_overwrite (bool, optional): either to force an overwrite if the config already exist. Defaults to False.

    Raises:
        FileExistsError: raised when the config already exist and force_overwrite is False

    Returns:
        Path: the path it wrote to
    """
    config_file_header = get_new_file_document_header()
    new_config_file_content = add_new_profile_to_config(profile_name, profile_data, config_file_header)
    path = resolve_config_path(scope)
    if not force_overwrite and path.exists():
        raise FileExistsError(
            f"The file at '{path}' seems to already exist"
            "Creating a new file would cause an overwrite of it's content"
        )
    save_toml_to_path(new_config_file_content, path)
    return path

def add_new_profile_to_config(new_profile_name: str, profile_data: Profile, config: TOMLDocument) -> TOMLDocument:
    """this function adds a new profile to config and return the new config
    
    Args:
        new_profile_name (str): the name of the profile, which is it's id in the 'profiles' table
        profile_data (Profile): the actual data to register in the new profile
        config (TOMLDocument): the config/ TOMLDcument to add the profile

    Raises:
        InvalidConfigError: raised when the profiles key in config is a list
        ProfileAlreadyExist: raised when the given profile name already exist in the config file

    Returns:
        TOMLDocument: The new config/ TOML Document
    """
    config_profiles_table = config.get("profiles")
    
    if isinstance(config_profiles_table, list):
        raise InvalidConfigError(
            "The config file has  [ [ profiles ] ] instead of [ profiles.X ]. "
            "This silently breaks all profile management. "
        )
    
    profile_table = profile_to_toml_table(profile_data)
    if config_profiles_table is None:
        new_profiles_table = table(is_super_table=True)
        config.add("profiles", new_profiles_table)
        config["profiles"][new_profile_name] = profile_table  # type: ignore
    else:
        if not isinstance(config_profiles_table, Table):
            raise InvalidConfigError(
                "The config 'profiles' key is not an actual TOML Table."
                "This might lead to unexpected behaviors."
            )
    
        if config_profiles_table.get(new_profile_name) is not None:
            raise ProfileAlreadyExists(
                f"The profile profiles.{new_profile_name} already exist."
            )
            
        config_profiles_table[new_profile_name] = profile_table
                          
    return config


    
def get_new_file_document_header() -> TOMLDocument:
    """create the TOML Document container header of a new file
    
    it mostly hold comments and links to usefuls ressources

    Returns:
        TOMLDocument: A TOMLDocument representing the header of a new copia config file
    """
    new_file_document = document()
    new_file_document.add(comment(f"if you're using Even Better TOML/ Taplo the config file scheme is available at: {COPIA_CONFIG_FILE_SCHEME}"))
    new_file_document.add(nl())
    new_file_document.add(comment("Avoid using [[profiles]] anywhere in this file."))
    new_file_document.add(comment("It silently swallows all [profiles.X] definitions beneath it,"))
    new_file_document.add(comment("Making all profile management commands behave as if no profiles exist."))
    new_file_document.add(comment("And breaking all attempts to save the file"))
    new_file_document.add(nl())
    new_file_document.add(comment(f"If you're editing this manually, refer to: {COPIA_CONFIG_FILE_DOC_LINK}"))
    new_file_document.add(nl())
    GEN_MESSAGE = time.strftime("GENERATED THE %Y-%m-%d AT %H:%M (%z)")
    new_file_document.add(comment(f"---- {GEN_MESSAGE} ---"))
    
    return new_file_document

def save_toml_to_path(config: TOMLDocument, path: Path ) -> None:
    """take a TOMLDocument and save it to the passed path
    
    it creates the corresponding file, if the path doesn't exist and lead to an actual TOML file

    Args:
        config (TOMLDocument): the config to save
        path (Path): the path to write to
    """
    TOMLFile(path).write(config)    
    
def profile_to_toml_table(profile: Profile) -> Table:
    """turn a Profile into a TOML Table

    Args:
        profile (Profile): The profile to convert

    Returns:
        Table: the converted TOML table
    """
    profile_table = table()
    for key, value in profile.model_dump().items():
        profile_table.add(key, value)
    return profile_table
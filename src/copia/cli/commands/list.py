import typer
from rich import print as pprint
from pydantic import ValidationError

from ..config.loaders import load_config, get_profile_from_config
from ..config.models import Profile
from ..config.exceptions import InvalidProfileError

list_profile_app = typer.Typer()

@list_profile_app.command("list")
def list_profiles():
    """list profiles defined in both global and local config files"""
    local_config = None
    global_config = None
    local_failure_reason = None
    global_failure_reason = None
    
    try:
        local_config = load_config("local")
    except Exception as err:
        local_failure_reason = err
        
    try:
        global_config = load_config("global")
    except Exception as err:
        global_failure_reason = err
        
    pprint("[blue][ LOCAL PROFILES ]")
    if local_config is None:
        pprint(f"\t[dim]{local_failure_reason}")
    else:
        display_config_profiles(local_config)
        
    pprint("\n[blue][ GLOBAL PROFILES ]")
    if global_config is None:
        pprint(f"\t[dim]{global_failure_reason}")
    else:
        display_config_profiles(global_config)

def display_config_profiles(config: dict) -> None:
    """
    display the each profiles in a config with a count summary
    """
    total_profiles = 0
    valid_profiles = 0
    invalid_profiles = 0
    warnings = 0
    
    profiles = config.get("profiles")
    if not isinstance(profiles, dict):
        pprint("\t[dim]No profiles found")
        return
    
    for key, value in profiles.items():
        if not isinstance(value, dict):
            pprint(f"\t[yellow]:WARNING: profiles.{key} is not a table")
            warnings += 1
            continue
        try:    
            profile = get_profile_from_config(key, config)
            pprint(f"\t[green]✓ {key}[/] - {profile}")
            valid_profiles += 1
        except InvalidProfileError as invalid_profile_err:
            invalid_profiles += 1
            pprint(f"\t[red]✗ profiles.{key}")
            pprint(f"\t\t[dim]Reason:")
            for reason in invalid_profile_err:
                pprint(f"\t\t [dim]{reason}")
        except Exception as unexpected_err:
            invalid_profiles += 1
            pprint(f"\t[red]✗ profiles.{key}")
            pprint(f"\t\tAn unexpected error occured: {unexpected_err}")
        total_profiles += 1
    if total_profiles == 0:
        pprint("[dim]\tNo profiles found")
    else:
        valid_color = "[bold green]" if valid_profiles > 0 else "[dim white]"
        invalid_color = "[bold red]" if invalid_profiles > 0 else "[dim white]"
        warning_color = "[bold yellow]" if warnings > 0 else "[dim white]"
        
        pprint("\n[dim] --- SUMMARY ---")
        pprint(f"[bold blue]\t{total_profiles} total profiles")
        pprint(f"{valid_color}\t{valid_profiles} valid profiles")
        pprint(f"{invalid_color}\t{invalid_profiles} invalid profiles")
        pprint(f"{warning_color}\t{warnings} warnings")
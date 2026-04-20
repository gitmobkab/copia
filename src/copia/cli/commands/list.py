import typer
from copia.cli.console_utils import echo

from ..config.loaders import load_config, get_profile_from_config
from ..config.exceptions import InvalidProfileError

list_profile_app = typer.Typer()

@list_profile_app.command("list")
def list_profiles(
    ctx: typer.Context,
    help_flag: bool = 
                typer.Option(False, "-h", "--help", help="Display this message and exit")):
    
    """[blue]list all profiles defined in both global and local config files"""
    local_config = None
    global_config = None
    local_failure_reason = None
    global_failure_reason = None
    
    if help_flag:
        echo(ctx.get_help())
        return
    
    try:
        local_config = load_config("local")
    except Exception as err:
        local_failure_reason = err
        
    try:
        global_config = load_config("global")
    except Exception as err:
        global_failure_reason = err
        
    echo("[blue][ LOCAL PROFILES ]")
    if local_config is None:
        echo(f"\t[dim]{local_failure_reason}")
    else:
        display_config_profiles(local_config)
        
    echo("\n[blue][ GLOBAL PROFILES ]")
    if global_config is None:
        echo(f"\t[dim]{global_failure_reason}")
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
        echo("\t[dim]No profiles found")
        return
    
    for key, value in profiles.items():
        if not isinstance(value, dict):
            echo(f"\t[yellow]:WARNING: profiles.{key} is not a table")
            warnings += 1
            continue
        try:    
            profile = get_profile_from_config(key, config)
            echo(f"\t[green]✓ {key}[/] - {profile}")
            valid_profiles += 1
        except InvalidProfileError as invalid_profile_err:
            invalid_profiles += 1
            echo(f"\t[red]✗ profiles.{key}")
            echo("\t\t[dim]Reason:")
            for reason in invalid_profile_err:
                echo(f"\t\t [dim]{reason}")
        except Exception as unexpected_err:
            invalid_profiles += 1
            echo(f"\t[red]✗ profiles.{key}")
            echo(f"\t\tAn unexpected error occured: {unexpected_err}")
        total_profiles += 1
    if total_profiles == 0:
        echo("[dim]\tNo profiles found")
    else:
        valid_color = "[bold green]" if valid_profiles > 0 else "[dim white]"
        invalid_color = "[bold red]" if invalid_profiles > 0 else "[dim white]"
        warning_color = "[bold yellow]" if warnings > 0 else "[dim white]"
        
        echo("\n[dim] --- SUMMARY ---")
        echo(f"[bold blue]\t{total_profiles} total profiles")
        echo(f"{valid_color}\t{valid_profiles} valid profiles")
        echo(f"{invalid_color}\t{invalid_profiles} invalid profiles")
        echo(f"{warning_color}\t{warnings} warnings")
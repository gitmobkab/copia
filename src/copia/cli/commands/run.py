from itertools import islice

from typer import Typer, Argument, Option, FileText, Exit
from rich.prompt import Confirm
from rich.table import Table

from copia.adapters import BaseAdapter
from copia.formatters import get_formatter, FormatterId
from copia.parser import parse
from copia.parser.models import Column
from copia.runners import generate_rows, GeneratedRow
from copia.validator import SemanticValidator
from copia.generators import GENERATORS_REGISTRY

from copia.cli.config import (
    LOCAL_COPIA_FILE,
    GLOBAL_COPIA_FILE
)

from ..utils import (
    echo,
    info,
    error,
    print_error,
    success,
    load_adapter_from_profile,
    ExitCodes
)

COPIA_DSL_DOC = "https://gitmobkab.github.io/copia/dsl/"
run_command = Typer()

@run_command.command('run')
def main(
    file: FileText = Argument('-',
                              help="the file to parse. use '-' for stdin via pipes."),
    
    table: str | None = Option(None,
                               '--table', '-t',
                               help="the name of the table to commit to. mandatory without the --dumps flag."),
    
    profile_name: str = Option('default',
                               '--profile', '-p',
                               help="The name of the profile to use for the run.",
                               rich_help_panel="Config related options"),
    
    search_global_config_only: bool = Option(False,
                                      '--global', '-g',
                                      help=f"search only in [green]'{GLOBAL_COPIA_FILE}'[/].",
                                      rich_help_panel="Config related options"),
    
    search_local_config_only: bool = Option(False,
                                            '--local', '-l',
                                            help=f"search only in [green]'{LOCAL_COPIA_FILE}'[/].",
                                            rich_help_panel="Config related options"),
    
    dumps: FormatterId | None = Option(None, 
                        '--dumps', '-d',
                        help="dumps the values based on the selected formatter.",
                        ),
    
    skip_config: bool = Option(False,
                               '--skip-config', '-s',
                               help="""disable config lookup for the run.
                               this will cause an error if the [green]'fetch'[/] generator is detected.
                               """,
                               rich_help_panel="Config related options"),
    
    rows: int = Option(10,
                       '--rows', '-n',
                       help="the number of rows for the run.",
                       min=1),
    
    skip_confirm: bool = Option(False,
                              '--skip-confirm', '-S',
                              help="Skip the confirmation prompt. directly commit the values to the db.")
    
        ):
    """Parse and run a file content
    
    Ex: 
        copia run users.copia --table users -S
        echo "uuid:uuid()" | copia run --table users -S
    
    
    Rules:
        the --table flag is mandatory if --dumps is missing
        the --skip-config flag is only usable with --dumps
    
    """
    if not dumps and not table:
        error("the TABLE argument is required when --dumps | -d is missing")
        raise Exit(ExitCodes.BAD_CLI_USAGE)
    if skip_config and not dumps:
        error('--skip-config | -s flag is forbidden without --dumps | -d')
        raise Exit(ExitCodes.BAD_CLI_USAGE)
    
    content = file.read()
    columns = parse_and_validate(content)
    if skip_config:
        adapter = None
    else:
        adapter = load_adapter_from_profile(profile_name, search_global_config_only, search_local_config_only)
    
    try:
        info("Generating values...")
        generated_rows = list(row for row in generate_rows(adapter, columns, rows, column_notifier))
    except Exception as err:
        print_error(err)
        raise Exit(ExitCodes.GENERATION_ERROR)
    
    if not dumps:
        assert adapter is not None
        assert table is not None
        if skip_confirm:
            info("Skipping confirmation prompt")
            seed(table, generated_rows, adapter)
        else:
            ask_and_seed(table, generated_rows, adapter)
    else:
        dump_generated_values(dumps, generated_rows)
    
    success("Bye")
    
    
def column_notifier(column: str, values: list) -> None:
    success(f"Column {column} ready. ({len(values)})")

def dump_generated_values(formatter_id: FormatterId, values: list[GeneratedRow]) -> None:
    formatter = get_formatter(formatter_id)
    for formatted_row in formatter(values):
        echo(formatted_row)

def ask_and_seed(table: str , rows: list[GeneratedRow], adapter: BaseAdapter, preview_limit: int = 20) -> None:
    columns = rows[0].keys()
    table_title = f"{len(rows)} rows generated"
    preview_table = Table(*columns, title=table_title, show_lines=True)
    for row in islice(rows, preview_limit):
        values = [str(value) for value in row.values()]
        preview_table.add_row(*values)
    echo(preview_table)
    if Confirm.ask("Commit to database?", case_sensitive=False):
        seed(table, rows, adapter)
    else:
        info("Commit to db cancelled")

def seed(table: str, rows: list[GeneratedRow], adapter: BaseAdapter):
    try:
        info("Commiting to db...")
        adapter.insert(table, rows)
        success(f"{list(rows)} inserted into databases")
    except Exception as err:
        print_error(err)
        raise Exit(ExitCodes.SEEDING_ERROR)
    finally:
        adapter.close()
    

def parse_and_validate(text: str) -> list[Column]:
    try:
        info("Parsing...")
        columns = parse(text)
        success("File parsed successfully !")
    except Exception as err:
        print_error(err, f"make sure your syntax is correct at '{COPIA_DSL_DOC}'")
        raise Exit(ExitCodes.BAD_DSL_INPUT)
        
    try:
        info("Validating the semantic...")
        generator_calls = [column.generator for column in columns]
        SemanticValidator(GENERATORS_REGISTRY).validate_many(generator_calls)
        success("Validation successfull !")
    except Exception as err:
        print_error(err)
        raise Exit(ExitCodes.BAD_DSL_INPUT)
    
    return columns    
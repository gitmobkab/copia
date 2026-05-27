from copia.cli.utils import ExitCodes

from typer.testing import CliRunner
from copia.cli.app import app

runner = CliRunner()

test_input = "id:uuid() name:username() pass:password() age:ranged_int() :past_date()"

def test_skip_config_and_missing_dumps_flags():
    result = runner.invoke(app, ["run", "--skip-config"], input=test_input)
    assert result.exit_code == ExitCodes.BAD_CLI_USAGE

def test_skip_config_without_dumps():
    result = runner.invoke(app, ["run", "--skip-config", "--table", "users"], input=test_input)
    assert result.exit_code == ExitCodes.BAD_CLI_USAGE

def test_dumps_json_no_exception():
    result = runner.invoke(app, ["run", "--dumps", "json", "--skip-config"], input=test_input)
    assert result.exit_code == ExitCodes.SUCCESS
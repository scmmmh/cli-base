"""Test running an app with no configuration."""
import click
import click.testing


def test_no_config():
    """Test running a command with no configuration."""
    from web_app_cli import setup_cli_app, cli_app

    @click.command()
    def test() -> None:
        pass

    setup_cli_app('test')
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    result = runner.invoke(cli_app, ['test'])

    assert result.exit_code == 0

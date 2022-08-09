"""Test running an app with no configuration."""
import click
import click.testing


def test_no_config():
    """Test running a command with no configuration."""
    from cli_base import setup_cli_app, cli_app

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    setup_cli_app('test')
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 0


def test_missing_config():
    """Test running a command with a missing configuration."""
    from cli_base import setup_cli_app, cli_app

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    setup_cli_app('test', config_schema={'test': {'type': 'string'}}, set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 1

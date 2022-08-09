"""Test running an app's help page."""
import click
import click.testing


def test_help():
    """Test running the help command."""
    from cli_base import create_cli_base

    @click.command(help='Dummy command')
    def test() -> None:
        """A dummy command for testing."""
        pass

    cli_app = create_cli_base('test', 'Test Application')
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli_app, ['--help'])

        assert result.exit_code == 0
        assert 'Test Application' in result.output
        assert 'Dummy command' in result.output

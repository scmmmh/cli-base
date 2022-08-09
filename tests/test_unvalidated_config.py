"""Test running an app with an unvalidated configuration."""
import click
import click.testing


def test_unvalidated_config_yaml():
    """Test running a command with an unvalidated configuration."""
    from cli_base import create_cli_base

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    cli_app = create_cli_base('test', 'Test Application', set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yaml', 'w') as f:
            f.write('test: Loaded')
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 0


def test_unvalidated_config_yml():
    """Test running a command with an unvalidated configuration."""
    from cli_base import create_cli_base

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    cli_app = create_cli_base('test', 'Test Application', set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yml', 'w') as f:
            f.write('test: Loaded')
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 0

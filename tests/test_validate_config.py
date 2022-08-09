"""Test running an app with an unvalidated configuration."""
import click
import click.testing


def test_valid_config():
    """Test running a command with a validated configuration."""
    from cli_base import create_cli_base

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    schema = {
        'test': {
            'type': 'string',
            'allowed': ['Loaded']
        }
    }

    cli_app = create_cli_base('test', 'Test Application', config_schema=schema, set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yaml', 'w') as f:
            f.write('test: Loaded')
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 0


def test_invalid_config():
    """Test running a command with an invalid configuration."""
    from cli_base import create_cli_base

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    schema = {
        'test': {
            'type': 'string',
            'allowed': ['Loaded']
        }
    }

    cli_app = create_cli_base('test', 'Test Application', config_schema=schema, set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yaml', 'w') as f:
            f.write('test: Failed')
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 1

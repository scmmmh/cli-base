"""Test running an app with an unvalidated configuration."""
import click
import click.testing


def test_valid_config_with_logging() -> None:
    """Test running a command with a validated configuration including logging."""
    from generic_cli_base import create_cli_base

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """Set the configuration."""
        pass

    schema = {
        'test': {
            'type': 'string',
            'allowed': ['Loaded']
        },
        'logging': {
            'type': 'dict'
        }
    }

    cli_app = create_cli_base('test', 'Test Application', config_schema=schema, set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yaml', 'w') as f:
            f.write('''test: Loaded
logging:
  version: 1
''')
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 0


def test_unvalidated_config_with_logging() -> None:
    """Test running a command with an unvalidated configuration including logging."""
    from generic_cli_base import create_cli_base

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """Set the configuration."""
        pass

    cli_app = create_cli_base('test', 'Test Application', set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yaml', 'w') as f:
            f.write('''test: Loaded
logging:
  version: 1
''')
        result = runner.invoke(cli_app, ['test'])

        assert result.exit_code == 0

"""Test running an app with an unvalidated configuration."""
import click
import click.testing


def test_valid_config_with_logging():
    """Test running a command with a validated configuration including logging."""
    from web_app_cli import setup_cli_app, cli_app

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
        },
        'logging': {
            'type': 'dict'
        }
    }

    setup_cli_app('test', config_schema=schema, set_config=set_config)
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


def test_unvalidated_config_with_logging():
    """Test running a command with an unvalidated configuration including logging."""
    from web_app_cli import setup_cli_app, cli_app

    @click.command()
    def test() -> None:
        """A dummy command for testing."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    setup_cli_app('test', set_config=set_config)
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

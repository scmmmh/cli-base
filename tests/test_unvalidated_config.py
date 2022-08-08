"""Test running an app with an unvalidated configuration."""
import click
import click.testing


def test_unvalidated_config_yaml():
    """Test running a command with an unvalidated configuration."""
    from web_app_cli import setup_cli_app, cli_app

    @click.command()
    def test() -> None:
        """Test test command."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    setup_cli_app('test', set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yaml', 'w') as f:
            f.write('test: Loaded')
        result = runner.invoke(cli_app, ['test'])
        print(result.output)

        assert result.exit_code == 0


def test_unvalidated_config_yml():
    """Test running a command with an unvalidated configuration."""
    from web_app_cli import setup_cli_app, cli_app

    @click.command()
    def test() -> None:
        """Test test command."""
        pass

    def set_config(config: dict) -> None:
        """A dummy configuration set callback."""
        pass

    setup_cli_app('test', set_config=set_config)
    cli_app.add_command(test)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('config.yml', 'w') as f:
            f.write('test: Loaded')
        result = runner.invoke(cli_app, ['test'])
        print(result.output)

        assert result.exit_code == 0

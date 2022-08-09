# CLI Base - Simple CLI Application Base

The CLI Base is a simple python library that provides the base for creating a commandline (CLI) application.

It uses [Click](https://click.palletsprojects.com) as the underlying library providing the CLI functionality and
[Cerberus](https://docs.python-cerberus.org) to validate an optional configuration file.

If a configuration file should be loaded, then this file **must** be a valid YAML file, **must** be called
`config.yaml` (or `config.yml`) and **must** be placed either in the current directory or at `/etc/{app_name}`.
The loaded configuration is then passed back to the application via a callback.

## Examples

The following three examples show the three basic use patterns: without configuration file, with configuration
file, and with validated configuration file.

### Basic Example

```python
import click

from cli_base import create_cli_base


@click.command()
def test() -> None:
   """A test command."""
   print('This works!')


if __name__ == '__main__':
   cli_app = create_cli_base('test', 'Test Application')
   cli_app.add_command(test)
   cli_app()
```

### Example with Configuration

```python
import click

from cli_base import create_cli_base

config = None


@click.command()
def test() -> None:
   """A test command."""
   print('This works!')
   print(config)


def set_configuration(new_config: dict) -> None:
   """Set the given configuration."""
   global config
   config = new_config


if __name__ == '__main__':
   cli_app = create_cli_base('test', 'Test Application', set_config=set_configuration)
   cli_app.add_command(test)
   cli_app()
```

### Example with validated Configuration

```python
import click

from cli_base import create_cli_base

config = None


@click.command()
def test() -> None:
   """A test command."""
   print('This works!')
   print(config)


def set_configuration(new_config: dict) -> None:
   """Set the given configuration."""
   global config
   config = new_config


CONFIG_SCHEMA = {
   'name': {
      'type': 'string'
   }
}

if __name__ == '__main__':
   cli_app = create_cli_base('test', 'Test Application', config_schema=CONFIG_SCHEMA, set_config=set_configuration)
   cli_app.add_command(test)
   cli_app()
```

## Further Documentation

```{toctree}
---
maxdepth: 2
---
api.rst
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

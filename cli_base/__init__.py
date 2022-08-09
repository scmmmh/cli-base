"""A very simple CLI base.

To use, first configure the CLI application via :func:`~web_app_cli.setup_cli_app` and then call
:func:`~web_app_cli.cli_app`.

The CLI base will automatically load, validate, and set a configuration file. The validation is performed using
`Cerberus <https://docs.python-cerberus.org>`_.
"""
import click
import logging
import logging.config
import os
import yaml

from cerberus import Validator
from collections.abc import Callable
from typing import Union


app_config = {
    'app_name': 'Unknown',
    'config_schema': None,
    'set_config': None,
}


def validate_config(schema: dict, config: dict) -> dict:
    """Validate the configuration.

    :param schema: The validation schema
    :type schema: dict
    :param config: The configuration to validate
    :type config: dict
    :return: The validated and normalised configuration
    :rtype: dict
    """
    validator = Validator(schema)
    if validator.validate(config):
        return validator.normalized(config)
    else:
        error_list = []

        def walk_error_tree(err: Union[dict, list], path: str) -> None:
            if isinstance(err, dict):
                for key, value in err.items():
                    walk_error_tree(value, path + (str(key), ))
            elif isinstance(err, list):
                for sub_err in err:
                    walk_error_tree(sub_err, path)
            else:
                error_list.append(f'{".".join(path)}: {err}')

        walk_error_tree(validator.errors, ())
        error_str = '\n'.join(error_list)
        raise click.ClickException(f'Configuration errors:\n\n{error_str}')


def setup_cli_app(app_name: str, config_schema: dict = None, set_config: Callable[[dict], None] = None) -> None:
    """Set the CLI application settings.

    :param app_name: The name of the application - used to generate config search paths
    :type app_name: str
    :param config_schema: An optional configuration schema to validate the configuration with Cerberus
    :type config_schema: dict
    :param set_config: An optional callback to receive the validated configuration
    :type set_config: callable
    """
    app_config['app_name'] = app_name
    app_config['config_schema'] = config_schema
    app_config['set_config'] = set_config


@click.group()
def cli_app() -> None:
    """Command-line interface."""
    config = None
    if app_config['set_config']:
        if os.path.exists('config.yml'):
            with open('config.yml') as in_f:
                config = yaml.safe_load(in_f)
        elif os.path.exists('config.yaml'):
            with open('config.yaml') as in_f:
                config = yaml.safe_load(in_f)
        elif os.path.exists(f'/etc/{app_config["app_name"]}/config.yml'):
            with open(f'/etc/{app_config["app_name"]}/config.yml') as in_f:
                config = yaml.safe_load(in_f)
        elif os.path.exists(f'/etc/{app_config["app_name"]}/config.yaml'):
            with open(f'/etc/{app_config["app_name"]}/config.yaml') as in_f:
                config = yaml.safe_load(in_f)
        if not config:
            raise click.ClickException(f'No configuration found (./config.y[a]ml, /etc/{app_config["app_name"]}/config.y[a]ml)')  # noqa: E501
        if app_config['config_schema']:
            normalised = validate_config(app_config['config_schema'], config)
            app_config['set_config'](normalised)
            if 'logging' in normalised:
                logging.config.dictConfig(normalised['logging'])
        else:
            app_config['set_config'](config)
            if 'logging' in config:
                logging.config.dictConfig(config['logging'])

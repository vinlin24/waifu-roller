"""
config.py
22 August 2022 07:57:27

Handle configuration setup.
"""

import os
from pathlib import Path
from typing import Any

import rich
import yaml

from waifu.exceptions import (ConfigFileError, ConfigFormatError,
                              get_user_config_path)

# Updated 0.0.3: Remember to update this when a new field is added
CONFIG_FILE_SCHEMA: dict[str, type] = {
    "verbose": bool,
    "revert-window": bool,
    "keep-failsafe": bool,
    "defaults": dict  # subkeys validated in parser.Parser
}


def _set_up_config_file() -> Path:
    """Set up the config.yaml file if it does not exist yet.

    Returns:
        Path: Path to the config.yaml file, regardless if this function
        created it or not.
    """
    config_path = get_user_config_path()
    first_time = not config_path.exists()
    if first_time:
        # Make the project's config directory if doesn't already exist
        try:
            config_path.parent.mkdir()
        except FileExistsError:
            pass

        # 0.0.3: Use an actual YAML file for the template instead of str
        # __file__ trick to get paths relative to module
        template_path = os.path.join(
            os.path.dirname(__file__),
            "config_template.yaml"
        )
        with open(template_path, "rt") as fp:
            template = fp.read()
        with open(config_path, "wt") as fp:
            fp.write(template)

        rich.print(
            "[green]We noticed you didn't have a configuration file set up "
            "yet, so we went ahead and made one for you. You can update your "
            f"preferences at: [/][bold yellow]{config_path}[/]\n"
        )
    return config_path


ConfigDict = dict[str, Any]
"""Represents the content of config.yaml."""


def _validate_config_format(config: ConfigDict) -> None:
    """Raise helpful errors for any format violation in loaded config.

    I recognize that there are existing projects that help validate
    YAML but I would like finer control over the errors. Also, this is
    dependency hell enough.

    Args:
        config (ConfigDict): The configuration loaded from config.yaml.

    Raises:
        ConfigFormatError: If there is any format violation.
    """
    for key, expected_type in CONFIG_FILE_SCHEMA.items():
        # Assert that the expected keys exist
        try:
            loaded_type = type(config[key])
        except KeyError as e:
            raise ConfigFormatError(
                f"Missing option {e.args[0]!r} in configuration file"
            ) from None
        # 0.0.3: Some other unexpected error (maybe user messed with file)
        # For example, the content is not valid YAML
        except Exception as e:
            raise ConfigFileError(
                "An unexpected error occurred in parsing the configuration "
                "file. You can try deleting this file and running the command "
                "again. We'll create a fresh file for you."
            ) from e

        # Assert that the top-level elements are the right type
        # Nested structures like defaults are validated separately
        if loaded_type is not expected_type:
            raise ConfigFormatError(
                f"Option {key!r} should be type {expected_type.__name__}, "
                f"got {loaded_type.__name__} instead"
            )


def load_config() -> ConfigDict:
    """Load configuration options from YAML file.

    Interface function to be called from main process.

    Raises:
        ConfigFormatError: There was a formatting error in the content
        of the configuration file.
        ConfigFileError: There was an issue loading the configuration
        file.

    Returns:
        ConfigDict: The loaded configuration details.
    """
    # Set up config.yaml file in .config directory if doesn't exist yet
    config_path = _set_up_config_file()
    try:
        with open(config_path, "rt") as fp:
            config = yaml.safe_load(fp)
            _validate_config_format(config)
            return config
    # Shouldn't happen but who knows
    except OSError as e:
        rich.print("[bold red]An unexpected OSError occurred:[/]")
        raise ConfigFileError from e

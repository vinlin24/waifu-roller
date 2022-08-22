"""
config.py
22 August 2022 07:57:27

Handle configuration setup.
"""

from pathlib import Path
from typing import Any

import rich
import yaml

from waifu.exceptions import (ConfigFileError, ConfigFormatError,
                              get_user_config_path)

CONFIG_FILE_TEMPLATE = """\
---
# Values to use when command line arguments are omitted
defaults:
  # Name of command (no $ or / prefix)
  mudae-command:
  # Channel to search for
  target-channel:
  # Number of times to send the command
  num-rolls:
"""


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
        # Not using yaml.dump() because that strips comments
        with open(config_path, "wt") as fp:
            fp.write(CONFIG_FILE_TEMPLATE)
        rich.print(
            "[green]We noticed you didn't have a configuration file set up "
            "yet, so we went ahead and did that for you. You can update your "
            f"preferences at [/][bold yellow]{config_path}[/]"
        )
    return config_path


ConfigDict = dict[str, Any]
"""Represents the content of config.yaml."""


def _validate_config_format(config: ConfigDict) -> None:
    """Raise helpful errors for any format violation in loaded config.

    Args:
        config (ConfigDict): The configuration loaded from config.yaml.

    Raises:
        ConfigFormatError: If there is any format violation.
    """
    # Assert that these keys exist
    try:
        config["defaults"]
    except KeyError as e:
        raise ConfigFormatError(
            f"Missing option {e.args[0]!r} in configuration file"
        ) from None


def load_config() -> ConfigDict:
    """Load configuration options from YAML file.

    Interface function to be called from main process.

    Args:
        config_path (str): Path to configuration file.

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
        raise ConfigFileError from e

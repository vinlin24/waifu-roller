"""
exceptions.py
21 August 2022 01:05:57

Defines the custom exceptions for this program.
"""

from pathlib import Path


def get_user_config_path() -> Path:
    """Return the cross-platform path to project's config file.

    Windows example: after first time setup, the config file will be
    located at:

        C:\\Users\\USERNAME\\\0.config\\waifu-roller\\config.yaml

    Returns:
        Path: Path to the user's config file within .config.
    """
    return Path.home() / ".config" / "waifu-roller" / "config.yaml"


def get_config_path_tip() -> str:
    """Return a tip informing the user where their config file is.

    Returns:
        str: The tip as a string to output.
    """
    return ("[TIP] Your configuration file is located at this path: "
            f"{get_user_config_path()}")


class RollerError(Exception):
    """Base class for all custom exceptions in this program."""


class ConfigError(RollerError):
    """Error loading the configuration for the application."""

    def __init__(self, *args: object) -> None:
        """Override to print useful info upon error."""
        args += ("", get_config_path_tip())
        super().__init__(*args)

    def __str__(self) -> str:
        """Override to print useful info upon error."""
        return "\n".join(self.args)


class ConfigFileError(ConfigError):
    """Error loading the configuration file."""
    pass


class ConfigFormatError(ConfigError):
    """Error in parsing the configuration file."""
    pass


class DiscordNotOpenError(RollerError):
    """Error for when the Discord app is not open when it should be."""
    pass


class CommandError(RollerError):
    """Error relating to command input. Meant to be caught."""
    pass

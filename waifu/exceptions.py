"""
exceptions.py
21 August 2022 01:05:57

Defines the custom exceptions for this program.
"""


class RollerError(Exception):
    """Base class for all custom exceptions in this program."""


class ConfigError(RollerError):
    """Error loading the configuration for the application."""
    pass


class ConfigFileError(ConfigError):
    """Error loading the configuration file."""
    pass


class ConfigFormatError(ConfigError):
    """Error in parsing the configuration file."""
    pass


class DiscordNotOpenError(RollerError):
    """Error for when the Discord app is not open when it should be."""
    pass

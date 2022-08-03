# exceptions.py

class ConfigError(Exception):
    """Error loading the configuration for the application."""
    pass


class ConfigFileError(ConfigError):
    """Error loading the configuration file."""
    pass


class ConfigFormatError(ConfigError):
    """Error in parsing the configuration file."""
    pass


class DiscordStartupError(Exception):
    """Error for starting the Discord app."""


class OSNotSupportedError(Exception):
    """Error from running application on unsupported OS."""
    pass


class DiscordNotFoundError(Exception):
    """Error for when the Discord.exe cannot be located."""
    pass

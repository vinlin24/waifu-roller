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


class OSNotSupportedError(Exception):
    """Error from running application on unsupported OS."""
    pass


class DiscordStartupError(Exception):
    """Error for starting the Discord app."""
    pass


class DiscordNotFoundError(DiscordStartupError):
    """Error for when the Discord.exe cannot be located."""
    pass


class DiscordNotOpenError(DiscordStartupError):
    """Error for when the Discord app is not open when it should be."""
    pass

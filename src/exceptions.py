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

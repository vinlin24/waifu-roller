"""
parser.py
22 July 2022 23:45:48

Implements the command line parser for this program.
"""

from argparse import ArgumentParser

from exceptions import ConfigFormatError


def _validate_config(config: dict) -> None:
    """Raise an error if config dict is not formatted properly.

    Args:
        config (dict): Config dict to validate.

    Raises:
        ConfigFormatError: If there is any problem in the format of the
        config dict, including missing keys, incorrect data types, bad
        argument range or characters, etc.
    """
    # Unpack default choices from config
    try:
        command = config["mudae-command"]
        channel = config["target-channel"]
        num_rolls = config["num-rolls"]
    except KeyError as e:
        raise ConfigFormatError(
            f"Missing option {e.args[0]!r} in configuration file"
        ) from None

    # Validate format: command should not be prefixed
    if not isinstance(command, str) or command.startswith(("$", "/")):
        raise ConfigFormatError(
            f"{command!r} is a bad value for option 'mudae-command': "
            f"should be a string and not command-prefixed (e.g. 'wa')"
        )
    # Validate format: channel name shouldn't have spaces in it
    if not isinstance(channel, str) or any(c.isspace() for c in channel):
        raise ConfigFormatError(
            f"{channel!r} is a bad value for option 'target-channel': "
            f"should be a string and not contain any whitespace "
            "(e.g. waifu-spam)"
        )
    # Validate format: num_rolls should be non-negative
    if not isinstance(num_rolls, int) or num_rolls < 0:
        raise ConfigFormatError(
            f"{num_rolls!r} is a bad value for option 'num-rolls': "
            "should be a non-negative integer"
        )


class Parser(ArgumentParser):
    """Command line parser for this program.

    Intended syntax example:
    ```
    roll wa -c digimon-waifus -n 16
    ```
    For rolling with command "$wa" 16 times in the first channel found
    by searching "digimon-waifus".
    """

    def __init__(self, defaults: dict[str, str | int]) -> None:
        """Initialize the parser for this program.

        Args:
            defaults (dict[str, str | int]): Default choices for
            command string, target channel, number of rolls from config
            file.

        Raises:
            ConfigFormatError: If defaults has a formatting error as
            checked by _validate_config.
        """
        super().__init__(description="Roll waifus on Discord")

        _validate_config(defaults)

        self.add_argument("command", nargs="?",
                          default=defaults["mudae-command"])
        self.add_argument("-c", "--channel",
                          default=defaults["target-channel"])
        self.add_argument("-n", "--num", type=int,
                          default=defaults["num-rolls"])
        self.add_argument("-d", "--daily", action="store_true")

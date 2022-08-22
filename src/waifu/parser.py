"""
parser.py
22 July 2022 23:45:48

Implements the command line parser for this program.
"""

from argparse import ArgumentParser
from typing import Any

from waifu.exceptions import ConfigFormatError

DefaultsDict = dict[str, str | int | None]


def _validate_default_command(command: Any) -> None:
    # Validate format: command should not be prefixed
    if not isinstance(command, str) or command.startswith(("$", "/")):
        raise ConfigFormatError(
            f"{command!r} is a bad value for defaults option "
            "'mudae-command': should be a string and not command-prefixed "
            "(e.g. 'wa')"
        )


def _validate_default_channel(channel: Any) -> None:
    # Validate format: channel name shouldn't have spaces in it
    if not isinstance(channel, str) or any(c.isspace() for c in channel):
        raise ConfigFormatError(
            f"{channel!r} is a bad value for defaults option "
            "'target-channel': should be a string and not contain any "
            "whitespace (e.g. waifu-spam)"
        )


def _validate_default_num_rolls(num_rolls: Any) -> None:
    # Validate format: num_rolls should be non-negative
    if not isinstance(num_rolls, int) or num_rolls < 0:
        raise ConfigFormatError(
            f"{num_rolls!r} is a bad value for defaults option 'num-rolls': "
            "should be a non-negative integer"
        )


class Parser(ArgumentParser):
    """Command line parser for this program.

    Intended syntax example:
    ```
    waifu wa -c digimon-waifus -n 16
    ```
    For rolling with command "$wa" 16 times in the first channel found
    by searching "digimon-waifus".
    """

    def __init__(self, defaults: DefaultsDict) -> None:
        """Initialize the parser for this program.

        Args:
            defaults (DefaultsDict): Default choices for
            command string, target channel, number of rolls from config
            file.

        Raises:
            ConfigFormatError: If there is any problem in the format of
            the defaults dict, including missing keys, incorrect data
            types, bad argument range or characters, etc.
        """
        super().__init__(description="Roll waifus on Discord")

        # VALIDATE DEFAULTS
        # Unpack default choices from config
        try:
            command = defaults["mudae-command"]
            channel = defaults["target-channel"]
            num_rolls = defaults["num-rolls"]
        except KeyError as e:
            raise ConfigFormatError(
                f"Missing defaults option {e.args[0]!r} in configuration file"
            ) from None

        # For all of these options, configure the add_argument() kwargs
        # differently for if they are provided or not
        # If they aren't set (left as None), then the parser should
        # treat those options as required.

        command_kwargs = {}
        if command is not None:
            _validate_default_command(command)
            command_kwargs.update({
                "nargs": "?",
                "default": command
            })

        channel_kwargs = {"required": True}
        if channel is not None:
            _validate_default_channel(channel)
            channel_kwargs.update({
                "default": channel,
                "required": False
            })  # type: ignore

        num_rolls_kwargs = {"type": int, "required": True}
        if num_rolls is not None:
            _validate_default_num_rolls(num_rolls)
            num_rolls_kwargs.update({
                "default": num_rolls,
                "required": False
            })  # type: ignore

        self.add_argument("command", **command_kwargs)
        self.add_argument("-c", "--channel", **channel_kwargs)
        self.add_argument("-n", "--num", **num_rolls_kwargs)
        # This one is not configurable
        self.add_argument("-d", "--daily", action="store_true")

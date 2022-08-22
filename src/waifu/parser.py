"""
parser.py
22 July 2022 23:45:48

Implements the command line parser for this program.
"""

from argparse import ArgumentParser, Namespace
from typing import Any, Sequence

from waifu.exceptions import CommandError, ConfigFormatError

DefaultsDict = dict[str, str | int | None]


# These _validate_* helper functions take a second argument is_default to
# distinguish validating an argument as a default value in config.yaml or an
# argument from the command line in action. If they're validating a default
# value, they should raise ConfigFormatError. Otherwise, they should raise
# CommandError.


def _validate_command(command: Any, is_default: bool) -> None:
    # Validate format: command should not be prefixed
    if not isinstance(command, str) or command.startswith(("$", "/")):
        raise ConfigFormatError(
            f"{command!r} is a bad value for defaults option "
            "'mudae-command': should be a string and not command-prefixed "
            "(e.g. 'wa')"
        ) if is_default else CommandError(
            f"{command!r} is a bad value for argument 'command': "
            "should not be command-prefixed (e.g. 'wa')"
        )


def _validate_channel(channel: Any, is_default: bool) -> None:
    # Validate format: channel name shouldn't have spaces in it
    if not isinstance(channel, str) or any(c.isspace() for c in channel):
        raise ConfigFormatError(
            f"{channel!r} is a bad value for defaults option "
            "'target-channel': should be a string and not contain any "
            "whitespace (e.g. 'waifu-spam')"
        ) if is_default else CommandError(
            f"{channel!r} is a bad value for argument 'CHANNEL': "
            "should not contain any whitespace (e.g. 'waifu-spam')"
        )


def _validate_num_rolls(num_rolls: Any, is_default: bool) -> None:
    # Validate format: num_rolls should be non-negative
    if not isinstance(num_rolls, int) or num_rolls < 0:
        raise ConfigFormatError(
            f"{num_rolls!r} is a bad value for defaults option 'num-rolls': "
            "should be a non-negative integer (e.g. 10)"
        ) if is_default else CommandError(
            f"{num_rolls!r} is a bad value for argument 'NUM': "
            "should be a non-negative integer (e.g. 10)"
        )


class Parser(ArgumentParser):
    """Command line parser for this program.

    Intended syntax example:
    ```
    waifu wa -c digimon-waifus -n 16 -d
    ```
    For rolling with command "$wa" 16 times in the first channel found
    by searching "digimon-waifus". The optional -d flag appends the
    daily commands $dk and $daily after the rolling session.
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
        # differently for if they are provided or not.
        # If they aren't set (left as None), then the parser should
        # treat those options as required.
        # Use is_default=True to raise ConfigFormatError for the user to see
        # if bad arg.

        command_kwargs = {}
        if command is not None:
            _validate_command(command, True)
            command_kwargs.update({
                "nargs": "?",
                "default": command
            })

        channel_kwargs = {"required": True}
        if channel is not None:
            _validate_channel(channel, True)
            channel_kwargs.update({
                "default": channel,
                "required": False
            })  # type: ignore

        num_rolls_kwargs = {"type": int, "required": True}
        if num_rolls is not None:
            _validate_num_rolls(num_rolls, True)
            num_rolls_kwargs.update({
                "default": num_rolls,
                "required": False
            })  # type: ignore

        self.add_argument("command", **command_kwargs)
        self.add_argument("-c", "--channel", **channel_kwargs)
        self.add_argument("-n", "--num", **num_rolls_kwargs)
        # This one is not configurable
        self.add_argument("-d", "--daily", action="store_true")

    def parse_args(self, args: Sequence[str] | None = None) -> Namespace:
        """Override function to validate args and print info on error.

        Args:
            args (Sequence[str] | None, optional): Command line
            arguments. Defaults to None.

        Raises:
            SystemExit: Terminates the program if there was an error
            parsing args.

        Returns:
            Namespace: The generated namespace.
        """
        try:
            ns = super().parse_args(args)
        except SystemExit:
            raise  # todo, point to config.yaml location

        # Unpack args to validate
        command: str = ns.command
        channel: str = ns.channel
        num: int = ns.num

        # Validate by raising CommandError if bad arg
        _validate_command(command, False)
        _validate_channel(channel, False)
        _validate_num_rolls(num, False)

        return ns

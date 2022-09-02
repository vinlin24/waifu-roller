"""
parser.py
22 July 2022 23:45:48

Implements the command line parser for this program.
"""

from argparse import ArgumentParser, Namespace
from typing import Any, Sequence

import rich

from .exceptions import CommandError, ConfigFormatError, get_config_path_tip

DefaultsDict = dict[str, str | int | None]
"""Typing for defaults key in config.yaml."""

# Command line argument help descriptions
COMMAND_HELP = ("Name of the Mudae command to use to roll for characters. It "
                "should be unprefixed (no $, /, etc.). "
                "Example: 'wa'")
CHANNEL_HELP = ("Query string to submit to the Discord search bar to locate "
                "the channel to roll in. It should not contain whitespace. "
                "Example: 'waifu-spam'")
NUM_HELP = ("Number of times to roll in this session. Should be nonnegative. "
            "Example: 10")
DAILY_HELP = ("Flag specifying whether the daily Mudae commands, $daily and "
              "$dailykakera, should be run in addition to the rolling this "
              "session.")
VERSION_HELP = ("Show script version and exit.")
CONFIG_HELP = ("Show configuration file path and exit.")

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
    # Changed 0.0.5: removed "no whitespace" constraint
    # Validate format: channel name should be a string
    if not isinstance(channel, str):
        raise ConfigFormatError(
            f"{channel!r} is a bad value for defaults option "
            "'target-channel': should be a string (e.g. 'waifu-spam')"
        ) if is_default else CommandError(
            f"{channel!r} is a bad value for argument 'CHANNEL': "
            "should be a string (e.g. 'waifu-spam')"
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
    waifu roll wa -c digimon-waifus -n 16 -d
    ```
    For rolling with command "$wa" 16 times in the first channel found
    by searching "digimon-waifus". The optional -d flag appends the
    daily commands $dk and $daily after the rolling session.
    """

    def __init__(self, defaults: DefaultsDict, verbose: bool) -> None:
        """Initialize the parser for this program.

        Args:
            defaults (DefaultsDict): Default choices for
            command string, target channel, number of rolls from config
            file.
            verbose (bool): Configuration preference. If True, will
            print config file tip on command error.

        Raises:
            ConfigFormatError: If there is any problem in the format of
            the defaults dict, including missing keys, incorrect data
            types, bad argument range or characters, etc.
        """
        super().__init__(description="Roll waifus on Discord!")
        self._verbose = verbose

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

        command_kwargs = {"help": COMMAND_HELP, "nargs": "?",
                          "default": command}
        if command is not None:
            _validate_command(command, True)
            command_kwargs.update({
                "nargs": "?",
                "default": command
            })  # type: ignore

        channel_kwargs = {"help": CHANNEL_HELP}
        if channel is not None:
            _validate_channel(channel, True)
            channel_kwargs.update({
                "default": channel,
            })  # type: ignore

        num_rolls_kwargs = {"type": int, "help": NUM_HELP}
        if num_rolls is not None:
            _validate_num_rolls(num_rolls, True)
            num_rolls_kwargs.update({
                "default": num_rolls,
            })  # type: ignore

        # Rolling arguments
        self.add_argument("command", **command_kwargs)
        self.add_argument("-c", "--channel", **channel_kwargs)
        self.add_argument("-n", "--num", **num_rolls_kwargs)
        # This one is not configurable
        self.add_argument("-d", "--daily",
                          action="store_true",
                          help=DAILY_HELP)

        # Info arguments
        # I opted out of using action="version" to avoid duplicate tips
        # Instead, they will be extracted from the namespace and invoke
        # callbacks in the main process
        self.add_argument("-v", "--version",
                          action="store_true",
                          help=VERSION_HELP)
        self.add_argument("--config",
                          action="store_true",
                          help=CONFIG_HELP)

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
            if self._verbose:
                rich.print(
                    f"\n[yellow]{get_config_path_tip()}[/]\n"
                    "You can include preferences for the command to use as "
                    "default options. You can also set [blue]verbose[/] to "
                    "[red]false[/] to disable this tip on command error.\n"
                )
            raise  # Give user useful info before quitting

        # Don't even consider rolling arguments if provided info argument
        version_flag: bool = ns.version
        config_flag: bool = ns.config
        if version_flag or config_flag:
            return ns

        # Otherwise unpack rolling args to validate
        command: str | None = ns.command
        channel: str | None = ns.channel
        num: int | None = ns.num

        # Args are None if they are omitted without a default to fall back to
        missing: dict[str, None] = {}
        if command is None:
            missing["command"] = None
        if channel is None:
            missing["-c/--channel CHANNEL"] = None
        if num is None:
            missing["-n/--num NUM"] = None
        # Using a dict for the insertion order since I want 'command' to
        # always appear first
        if missing:
            rich.print(
                "[bold red]The following arguments are missing from your "
                "command and you do not have a default value set in your "
                f"configuration file:[/]\n"
                f"\n\t{', '.join(missing.keys())}\n"
            )
            if self._verbose:
                rich.print(f"[yellow]{get_config_path_tip()}[/]\n")
            raise SystemExit

        # Validate by raising CommandError if bad arg
        _validate_command(command, False)
        _validate_channel(channel, False)
        _validate_num_rolls(num, False)

        return ns

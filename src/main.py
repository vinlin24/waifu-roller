#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import sys
from parser import Parser

import keyboard
import rich
import rich.traceback
import yaml

from abort import register_abort_handlers
from core import navigate_to_channel, open_discord, start_rolling
from exceptions import ConfigFileError, ConfigFormatError

CONFIG_PATH = "config.yaml"  # make configurable later
ConfigDict = dict[str, dict[str, str | int]]  # may change later


def load_yaml(config_path: str) -> ConfigDict:
    """Load configuration options from YAML file.

    Args:
        config_path (str): Path to configuration file.

    Raises:
        ConfigFileError: There was an issue loading the file specified
        by config_path.
        ConfigFormatError: There was a formatting error in the content
        of the configuration file.

    Returns:
        ConfigDict: The loaded configuration details.
    """
    try:
        with open(config_path, "rt") as fp:
            config = yaml.safe_load(fp)
            config["defaults"]
            return config
    except OSError as e:
        raise ConfigFileError(str(e)) from None
    except KeyError as e:
        raise ConfigFormatError(
            f"Missing defaults option {e.args[0]!r} in configuration file"
        ) from None


def main() -> None:
    """Main driver function."""
    # Set up graceful exits
    rich.traceback.install()
    register_abort_handlers()

    # Load config
    config = load_yaml(CONFIG_PATH)

    # Parse command line arguments
    parser = Parser(config["defaults"])
    ns = parser.parse_args(sys.argv[1:])

    # Unpack command line args
    command: str = ns.command
    channel: str = ns.channel
    num: int = ns.num
    daily: bool = ns.daily

    # Echo the chosen options and prompt continuation
    rich.print(
        "[green]"
        f"You have chosen to roll with the Mudae command '${command}' "
        f"{num} times in the channel queried with {channel!r}, and have "
        f"{'' if daily else 'NOT '}opted to run the daily commands as well."
        "[/]"
    )
    rich.print("Hit ENTER to continue, or ^C to quit: ")
    # Use instead of input() as workaround for funky TAB abort behavior
    keyboard.wait("enter")

    # pyautogui sequences
    open_discord()
    navigate_to_channel(channel)
    start_rolling(command, num, daily)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import _thread
import signal
import sys
from argparse import Namespace
from parser import Parser
from types import FrameType
from typing import NoReturn

import keyboard
import rich
import rich.traceback
import yaml

from exceptions import ConfigFileError, ConfigFormatError
from keystrokes import navigate_to_channel, start_rolling, wait_for_ready
from open import open_discord

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


def abort_callback() -> NoReturn:  # type: ignore
    """Attempt to exit the program.

    Raises:
        KeyboardInterrupt: Sends signal SIGINT to main thread.
    """
    rich.print("[bold red]Script interrupted with TAB key[/]")
    # sys.exit() only interrupts keyboard listener thread
    _thread.interrupt_main()


def interrupt_handler(sig: int, frame: FrameType | None) -> NoReturn:
    rich.print("[bold red]Script terminated[/]")
    sys.exit()


def run(ns: Namespace) -> None:
    # Unpack command line args
    command = ns.command
    channel = ns.channel
    num = ns.num
    daily = ns.daily

    # todo: Make this process more intuitive - leave space at the start
    # to give instructions - maybe prompt <ENTER> in either case before
    # moving away from the terminal to Discord
    # Wait for <ENTER> key from user if had to start app
    launched_app = open_discord()
    if launched_app:
        wait_for_ready()

    # Keystroke sequences
    # todo: Make failsafe more graceful
    navigate_to_channel(channel)
    start_rolling(command, num, daily)


def main() -> None:
    """Main driver function."""
    # Set up graceful exits
    signal.signal(signal.SIGINT, interrupt_handler)
    rich.traceback.install()

    # Set up abort handler
    keyboard.add_hotkey("tab", abort_callback)
    rich.print(
        "[bold yellow]Abort the script at any time with the TAB key[/]"
    )

    # Load config
    config = load_yaml(CONFIG_PATH)

    # Parse command line arguments
    parser = Parser(config["defaults"])
    ns = parser.parse_args(sys.argv[1:])

    # Run the main process
    run(ns)


if __name__ == "__main__":
    main()

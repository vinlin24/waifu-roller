#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import sys

import keyboard
import rich
import rich.traceback

from waifu import __version__
from waifu.abort import ABORT_KEY, register_abort_handlers
from waifu.config import load_config
from waifu.core import run_autogui
from waifu.exceptions import get_user_config_path
from waifu.parser import Parser


def version_callback() -> None:
    """Callback for if the -v/--version flag is used."""
    rich.print(f"waifu-roller {__version__}")


def config_callback() -> None:
    """Callback for if the --config flag is used."""
    rich.print(get_user_config_path())


def main() -> None:
    """Main driver function."""
    # Set up graceful exits
    rich.traceback.install(
        # Keep the traceback compact and tidy
        extra_lines=1,
        max_frames=1
    )
    register_abort_handlers()

    # Load and validate config
    config = load_config()

    # Unpack validated config options
    verbose: bool = config["verbose"]
    revert: bool = config["revert-window"]
    defaults: dict = config["defaults"]

    # Parse command line arguments
    parser = Parser(defaults, verbose)
    ns = parser.parse_args(sys.argv[1:])

    # Unpack command line args
    command: str = ns.command
    channel: str = ns.channel
    num: int = ns.num
    daily: bool = ns.daily
    version_flag: bool = ns.version
    config_flag: bool = ns.config

    # If either or both of the info flags are included, use their callbacks
    # instead of the continuing with the script
    if version_flag:
        version_callback()
    if config_flag:
        config_callback()
    if version_flag or config_flag:
        raise SystemExit

    # Display tip now that command is validated
    rich.print(
        "[bold yellow]Note: You can abort the script at any time with the "
        f"{ABORT_KEY.upper()} key[/]"
    )

    # Echo the chosen options and prompt continuation
    rich.print(
        "[green]"
        f"You have chosen to roll with the Mudae command '${command}' "
        f"{num} times in the channel queried with {channel!r}, and have "
        f"opted to {'' if daily else 'NOT '}run the daily commands as well."
        "[/]"
    )
    rich.print("Hit ENTER to continue, or ^C to quit: ")
    # Use instead of input() as workaround for funky abort key behavior
    keyboard.wait("enter")

    # PyAutoGUI sequences
    run_autogui(command, channel, num, daily, verbose, revert)

    # All went well!
    rich.print("[green]Script terminated successfully.[/]")


if __name__ == "__main__":
    main()

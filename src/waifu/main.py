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

from waifu.abort import register_abort_handlers
from waifu.config import load_config
from waifu.core import run_autogui
from waifu.parser import Parser


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
    defaults: dict = config["defaults"]

    # Parse command line arguments
    parser = Parser(defaults, verbose)
    ns = parser.parse_args(sys.argv[1:])

    # Display tip if command is validated
    rich.print(
        "[bold yellow]Note: You can abort the script at any time with the "
        "TAB key[/]"
    )

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
        f"opted to {'' if daily else 'NOT '}run the daily commands as well."
        "[/]"
    )
    rich.print("Hit ENTER to continue, or ^C to quit: ")
    # Use instead of input() as workaround for funky TAB abort behavior
    keyboard.wait("enter")

    # PyAutoGUI sequences
    run_autogui(command, channel, num, daily, verbose)

    # All went well!
    rich.print("[green]Script terminated successfully.[/]")


if __name__ == "__main__":
    main()

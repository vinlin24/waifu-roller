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
from waifu.core import navigate_to_channel, open_discord, start_rolling
from waifu.parser import Parser


def main() -> None:
    """Main driver function."""
    # Set up graceful exits
    rich.traceback.install()
    register_abort_handlers()

    # Load config
    config = load_config()

    # Parse command line arguments
    parser = Parser(config["defaults"])
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
roller.py
22 June 2022 18:45:48

Script using pyautogui for automating rolling waifus on Discord.
Also see: https://pypi.org/project/pynput/

This is a copy and pasted version from when it was a crude, standalone script.
"""

import argparse
import os
import sys
import time

import pyautogui as pag

# open discord window -> click home -> click find or start a conversation
# -> typewrite("digimon-waifus\n", 0.1) -> typewrite(["escape"]) -> start rolling

# finally got the keyboard shortcut lmao:
# open discord window -> Ctrl+T
# -> typewrite("digimon-waifus\n", 0.1) -> typewrite(["escape"]) -> start rolling

# startup
LOAD_WAITING = 5.0  # seconds to wait before continuing if starting app
DISCORD_APP_PATH = "C:/Users/soula/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Discord Inc/Discord"

# cooldowns to not look suspicious
ACTION_COOLDOWN = 0.1  # seconds to wait between actions
TYPING_COOLDOWN = 0.05  # seconds to wait between character input
ROLLING_COOLDOWN = 1.0  # seconds to wait between waifu roll attempts

# observed coords for app components
CLAIM_COORD = (500, 885)

# defaults
DEFAULT_MUDAE_COMMAND = "wa"  # omit $ prefix cuz that messes up shell
DEFAULT_TARGET_CHANNEL = "digimon-waifus"
DEFAULT_NUM_ROLLS = 16


class Parser(argparse.ArgumentParser):
    """Command line parser for this script.

    Intended syntax example:
        python roller.py wa -c digimon-waifus -n 16
    For rolling with command "$wa" 16 times in the first channel found
    by searching "digimon-waifus".
    """

    def __init__(self) -> None:
        super().__init__(description="Roll waifus on Discord")
        self.add_argument("command", nargs="?", default=DEFAULT_MUDAE_COMMAND)
        self.add_argument("-c", "--channel", default=DEFAULT_TARGET_CHANNEL)
        self.add_argument("-n", "--num", type=int, default=DEFAULT_NUM_ROLLS)
        self.add_argument("-d", "--daily", action="store_true")


def open_discord() -> None:
    """Attempt to focus Discord window, starting the app if necessary."""
    win_list = pag.getWindowsWithTitle("Discord")
    # Discord already open
    try:
        discord_win: pag.Window = win_list[0]
        discord_win.maximize()
        discord_win.activate()
        print("successfully maximized and focused Discord app")
    # Discord not open yet
    except IndexError:
        os.startfile(DISCORD_APP_PATH)
        print(f"starting Discord app, waiting {LOAD_WAITING} seconds")
        time.sleep(LOAD_WAITING)


def cooldown() -> None:
    """Sleep for ACTION_COOLDOWN seconds."""
    time.sleep(ACTION_COOLDOWN)


def navigate_to_channel(channel: str) -> None:
    """Navigate to the target channel within Discord to roll in."""
    # bring up global search
    cooldown()
    pag.hotkey("ctrl", "t")

    # type channel name
    cooldown()
    pag.typewrite(channel + "\n", interval=TYPING_COOLDOWN)

    # focus text area
    cooldown()
    # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    pag.hotkey("esc")

    print(f"successfully focused text area in {channel=}")


def start_rolling(command: str, num: int, daily: bool) -> None:
    """Repeatedly enter the roll command into the channel."""
    # move cursor to where the heart emoji shows up
    pag.moveTo(*CLAIM_COORD)

    print(f"starting to roll with {command=}")
    for attempt_num in range(1, num + 1):
        pag.typewrite(f"${command}\n")
        print(f"attempted to roll ({attempt_num}/{num})")
        time.sleep(ROLLING_COOLDOWN)

    if (daily):
        print(f"attempting to run daily commands")
        pag.typewrite(f"$daily\n")
        time.sleep(ROLLING_COOLDOWN)
        pag.typewrite(f"$dk\n")


def main() -> None:
    """Main driver function."""
    # unpack args
    namespace = Parser().parse_args(sys.argv[1:])
    command = namespace.command
    channel = namespace.channel
    num = namespace.num
    daily = namespace.daily

    # automated processes
    open_discord()
    navigate_to_channel(channel)
    start_rolling(command, num, daily)

    print("script terminated successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()

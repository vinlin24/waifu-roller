#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import sys
import time
from argparse import Namespace
from parser import Parser

import pyautogui
import yaml

from exceptions import ConfigFileError, ConfigFormatError
from open import open_discord

CONFIG_PATH = "config.yaml"  # make configurable later

# make configurable later
ACTION_COOLDOWN = 0.1  # seconds to wait between actions
TYPING_COOLDOWN = 0.05  # seconds to wait between character input
ROLLING_COOLDOWN = 1.0  # seconds to wait between waifu roll attempts


def load_yaml(config_path: str) -> dict[str, dict[str, str | int]]:
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


def cooldown() -> None:
    time.sleep(ACTION_COOLDOWN)


def navigate_to_channel(channel: str) -> None:
    """Navigate to the target channel within Discord to roll in."""
    # bring up global search > enter channel name > focus text area
    cooldown()
    pyautogui.hotkey("ctrl", "t")
    cooldown()
    pyautogui.typewrite(channel + "\n", interval=TYPING_COOLDOWN)
    cooldown()
    # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    pyautogui.hotkey("esc")


def run(ns: Namespace) -> None:
    # unpack command line args
    command = ns.command
    channel = ns.channel
    num = ns.num
    daily = ns.daily

    open_discord()
    # navigate_to_channel(channel)


def main() -> None:
    """Main driver function."""
    config = load_yaml(CONFIG_PATH)  # load config
    parser = Parser(config["defaults"])  # load defaults
    ns = parser.parse_args(sys.argv[1:])  # parse args
    run(ns)  # main process


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import sys
from argparse import Namespace
from parser import Parser

import rich.traceback
import yaml

from exceptions import ConfigFileError, ConfigFormatError
from keystrokes import navigate_to_channel, start_rolling
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


def run(ns: Namespace) -> None:
    # unpack command line args
    command = ns.command
    channel = ns.channel
    num = ns.num
    daily = ns.daily

    open_discord()
    navigate_to_channel(channel)
    start_rolling(command, num, daily)


def main() -> None:
    """Main driver function."""
    # Set up global traceback handler for pretty exception printing
    rich.traceback.install()

    # Load config
    config = load_yaml(CONFIG_PATH)

    # Parse command line arguments
    parser = Parser(config["defaults"])
    ns = parser.parse_args(sys.argv[1:])

    # Run the main process
    run(ns)


if __name__ == "__main__":
    main()

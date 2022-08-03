#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import sys
from parser import Parser

import yaml

from exceptions import ConfigFileError, ConfigFormatError

CONFIG_PATH = "config.yaml"  # make configurable later


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
            f"Missing option {e.args[0]!r} in configuration file")


def main() -> None:
    """Main driver function."""
    config = load_yaml(CONFIG_PATH)
    ns = Parser(config["defaults"]).parse_args(sys.argv[1:])
    # run the program


if __name__ == "__main__":
    main()

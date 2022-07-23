"""
parser.py
22 July 2022 23:45:48

Implements the command line parser for this program.
"""

import sys
from argparse import ArgumentParser


class Parser(ArgumentParser):
    """Command line parser for this program.

    Intended syntax example:
        roll wa -c digimon-waifus -n 16
    For rolling with command "$wa" 16 times in the first channel found
    by searching "digimon-waifus".
    """

    def __init__(self, defaults: dict[str, str | int]) -> None:
        """Initialize the parser for this program.

        Args:
            defaults (dict[str, str  |  int]): Default choices for command string, target channel, number of rolls from config file.
        """
        super().__init__(description="Roll waifus on Discord")

        # unpack default choices from config
        command: str = defaults.get("mudae-command")
        channel: str = defaults.get("target-channel")
        num_rolls: int = defaults.get("num-rolls")

        self.add_argument("command", nargs="?", default=command)
        self.add_argument("-c", "--channel", default=channel)
        self.add_argument("-n", "--num", type=int, default=num_rolls)
        self.add_argument("-d", "--daily", action="store_true")

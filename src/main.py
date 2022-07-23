#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
22 July 2022 23:45:08

Entry point and main process.
"""

import sys
from parser import Parser


def main() -> None:
    """Main driver function."""
    ns = Parser().parse_args(sys.argv[1:])
    # run the program


if __name__ == "__main__":
    main()

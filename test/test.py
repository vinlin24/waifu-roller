#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py
22 July 2022 23:55:38

Throwaway test code.
"""

import yaml

with open("config.yaml", "rt") as file:
    config = yaml.safe_load(file)

print(config)

"""config_template.py

Store the content of a default config.yaml file as a string constant.
This is necessary because setuptools does not permit installing data
files to arbitrary locations on a user's machine.
"""

CONFIG_TEMPLATE = """\
---
# Program verbosity setting
verbose: true
# After completion, return to the window that was active at startup
revert-window: false
# Moving your mouse to a corner of the screen terminates script
keep-failsafe: true
# Automatically start rolling, skipping confirmation text
skip-confirmation: false

# Values to use when command line arguments are omitted
defaults:
  # Name of command (no $ or / prefix)
  mudae-command:
  # Channel to search for
  target-channel:
  # Number of times to send the command
  num-rolls:
"""

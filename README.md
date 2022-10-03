<!-- https://github.com/marketplace/actions/dynamic-badges -->
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

# Coder's Waifu Roller

**Command line tool for rolling anime/game characters with the Discord bot [Mudae](https://top.gg/bot/432610292342587392).**

## Description

Suppose you're in the zone coding, but it's a new hour and you can roll for waifus again. Before you'd switch to Discord, find the channel, and brainlessly spam enter `$wa` or something. Now you can start the whole rolling sequence right from the command line:
```
waifu wa -c waifu-spam -n 10 -d
```

:mega: **No asking for user tokens, no Discord self-botting, no automatic claiming or sniping.** This project uses [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) to automate the process of switching to the app, navigating to the channel, and entering commands. This silly script is intended to just free up your hands a little while you watch the rolls go by.

## Installation

### With Python 3.10+

Download the desired wheel file `waifu_roller-x.y.z-py3-none-any.whl` from the [`dist`](dist) folder or the [Releases](https://github.com/vinlin24/waifu-roller/releases) section and install it with pip:
```
pip install path/to/waifu_roller-x.y.z-py3-none-any.whl
```
You can verify that it's installed by running:
```
pip show waifu-roller
```

## Usage

The CLI command is `waifu`:
```
waifu wa -c waifu-spam -n 10 -d
```
This example rolls the Mudae command $wa 10 times in the channel named waifu-spam. The optional -d flag appends the daily commands $dk and $daily after the rolling session.

You can also omit arguments and opt to use the default values set in the [config.yaml](docs/REFERENCE.md#configuration) file. This could be useful if you roll most commonly in a specific channel on a specific server:
```
waifu
```

This program supports [hotkeys](docs/REFERENCE.md#hotkeys) to assist your *competitive waifu snatching*. You can pause and resume rolling with CAPSLOCK to claim a character/kakera/whatnot, or abort altogether with ESC.

As usual, use the help flag for a full list of arguments, or use the config flag to get the full path to your [configuration file](docs/REFERENCE.md#configuration):
```
waifu --help
waifu --config
```

## References and Configuration

See [REFERENCE.md](docs/REFERENCE.md).

## Development

If you would like to contribute, please see [DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Change Log

See [CHANGELOG.md](docs/CHANGELOG.md).

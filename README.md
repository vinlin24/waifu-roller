<!-- https://github.com/marketplace/actions/dynamic-badges -->
![Build Version](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/vinlin24/b4b5eb0dba19ef0cadea7eb95bd0d252/raw/badge.json)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

# Coder's Waifu Roller

## Description

**Command line tool for rolling anime/game characters with the Discord bot [Mudae](https://top.gg/bot/432610292342587392).**

Suppose you're in the zone coding, but it's a new hour and you can roll for waifus again. Before you'd switch to Discord, find the channel, and brainlessly spam enter `$wa` or something. Now you can start the whole rolling sequence right from the command line:
```
waifu -c waifu-spam -n 10
```

> :mega: **No asking for user tokens, no Discord self-botting, no automatic claiming or sniping.** This project uses [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) to automate the process of switching to the app, navigating to the channel, and entering commands. This silly script is intended to just free up your hands a little while you watch the rolls go by.

## Installation

> :warning: At the moment, this application requires you to have Python >=3.10 installed.

Download the desired wheel file `waifu_roller-x.y.z-py3-none-any.whl` from the [`dist`](dist/) folder and install it with pip, preferably in a [virtual environment](https://docs.python.org/3/tutorial/venv.html):
```
python -m pip install path/to/waifu_roller-x.y.z-py3-none-any.whl
```
You can verify that it's installed by running:
```
python -m pip show waifu-roller
```

## Usage

The CLI command is `waifu`:
```
waifu wa -c waifu-spam -n 10 -d
```
This example rolls the Mudae command $wa 10 times in the channel named waifu-spam. The optional -d flag appends the daily commands $dk and $daily after the rolling session.

You can also omit arguments and opt to use the default values set in the [config.yaml](#configuration) file. This could be useful if you roll most commonly in a specific channel on a specific server:
```
waifu
```
As usual, use the help flag for a full list of arguments, or use the config flag to get the full path to your [configuration file](#configuration):
```
waifu --help
waifu --config
```

### Command Reference

| Argument             | Type           | Description                                                                                                                                                                                                                                                                                                        | Example      |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| command              | positional     | Name of the Mudae command to use to roll for characters. It should be unprefixed (no $, /, etc.).                                                                                                                                                                                                                  | 'wa'         |
| -c/--channel CHANNEL | option (1 arg) | Query string to submit to the Discord quick switcher to locate the channel to roll in. It should not contain whitespace. You should try entering this query yourself first with Ctrl+K to make sure it brings up the expected channel. The program has no way of knowing if the correct channel has entered focus. | 'waifu-spam' |
| -n/--num NUM         | option (1 arg) | Number of times to roll in this session. Should be nonnegative. You can troll and put a massive number, but it's not our fault if you get banned for spam.                                                                                                                                                         | 10           |
| -d/--daily           | option (flag)  | Flag specifying whether the daily Mudae commands, $daily and $dailykakera, should be run in addition to the rolling this session.                                                                                                                                                                                  |              |

> :hammer: Developer Todo: Update this reference every time a new command feature is added.

You can also use the following flags to display helpful information instead of rolling:

| Flag         | Description                                          |
| ------------ | ---------------------------------------------------- |
| -h/--help    | Display help message and ignore all other arguments. |
| -v/--version | Display version of installed script.                 |
| --config     | Display path of configuration file.                  |

### Hotkeys

This program uses the [keyboard](https://github.com/boppreh/keyboard) module to implement hotkeys for convenience. At the moment, they aren't configurable and most likely won't be because it wouldn't make much sense to have character or control keys interfere with PyAutoGUI's key-sending.

| Hotkey   | Description                                                                                                                                                                                                                        |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ESC      | Abort script by sending SIGINT to the program. Also handy to use if the [revert-window](#configuration-reference) preference is set, which gives a short window of delay if you choose to stay on Discord to react to a roll, etc. |
| CAPSLOCK | Pause/resume rolling. This is useful if you want to stop to claim a spawned character or kakera drop in the middle of a rolling session.                                                                                           |

## Configuration

> :mega: **Your configuration file is here:
> `~/.config/waifu-roller/config.yaml`**

On first run, the script will try to initialize a configuration file for you at the above path. Default values and helpful comments are provided in the document, but you can refer to the reference below for detailed descriptions.

### Configuration Reference

> :hammer: Developer Todo: Update this schema every time a new configuration feature is added.

| Field                   | Type    | Description                                                                                                                                                                                                  | Default      |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| verbose                 | boolean | Program verbosity level, and include config file path tip on --help and command error.                                                                                                                       | true         |
| revert-window           | boolean | Whether to return to the window from which script was called after rolling is completed. Waits for a short delay first. In case you want to stay on Discord, ESC aborting and TAB pausing still have effect. | false        |
| keep-failsafe           | boolean | Whether to keep PyAutoGUI's fail-safe mechanism, where moving your mouse to a corner of the screen terminates the program.                                                                                   | true         |  |
| defaults                | mapping | Values to use when command line arguments are omitted.                                                                                                                                                       |              |
| defaults.mudae-command  | string  | Default value for the command positional arg.                                                                                                                                                                | null (unset) |
| defaults.target-channel | string  | Default value for the -c/--channel option.                                                                                                                                                                   | null (unset) |
| defaults.num-rolls      | int     | Default value for the -n/--num option.                                                                                                                                                                       | null (unset) |

## Development

As of now, the builds have only been tested on my local PC, which is a Windows 11 64-bit system.

If you want to simulate my virtual environment, you can use the provided [requirements.txt](requirements.txt) after installing the wheel file:
```
python -m pip install -r requirements.txt
```

## Todo

A tentative list of upcoming features (:bulb:) and implementation changes (:wrench:).

- [ ] :bulb: Support binary distributions that don't require the user to have Python installed.
- [ ] :bulb: Make distribution and installation instructions more intuitive.
- [ ] :bulb: Include update script in distribution. Remember to properly handle possibly existing `config.yaml`s.
- [ ] :bulb: Stop exposing `ConfigError`s and `CommandError`s and define more graceful output.
- [ ] :wrench: Figure out a better alternative to the the ENTER listener when prompting confirmation since this leaves an awkward newline at script termination.
- [ ] :wrench: Clean up the `parse_args` process and make better use of `argparse`'s error handling functionality, or migrate to other CLI libraries altogether.
- [ ] :wrench: Enhance [build.ps1](build/build.ps1) to clean up even upon error, such as removing the generated `*.egg-info` directories. Also maybe make it report how long the build takes since they take quite a while lol.
- [ ] :wrench: Maybe use environment variables instead of [meta.json](build/meta.json) to maintain version string since using [update.py](build/update.py) to modify 3 places at once seems like a massive code smell.
- [ ] :wrench: Maybe migrate from [PyYAML](https://pyyaml.org/) to [ruamel.yaml](https://pypi.org/project/ruamel.yaml/).
- [ ] :wrench: Use [rich logging](https://rich.readthedocs.io/en/stable/logging.html) instead of `rich.print` to fix the pervasive `if verbose:` lines.

## Change Log

![0.0.1](https://img.shields.io/badge/version-0.0.1-brightgreen)

- Initial distribution.

![0.0.2](https://img.shields.io/badge/version-0.0.2-brightgreen)

- Make the pause hotkey CAPSLOCK have effect during the [revert-window](#configuration-reference) delay as well (originally only the abort key ESC had effect).
- Add new configuration preference [keep-failsafe](#configuration-reference).

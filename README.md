<!-- https://github.com/marketplace/actions/dynamic-badges -->
![Build Version](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/vinlin24/b4b5eb0dba19ef0cadea7eb95bd0d252/raw/badge.json)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

# Coder's Waifu Roller

## Description

**Command line tool for rolling anime/game characters with the Discord bot [Mudae](https://top.gg/bot/432610292342587392).**

Suppose you're in the zone coding, but it's a new hour and you can roll for waifus again. Before you'd switch to Discord, find the channel, and brainlessly spam enter `$wa` or something. Now you can start the whole rolling sequence right from the command line (that you should always have open anyway :relieved:).
```
$ waifu -c waifu-spam -n 10
```

> :mega: **No asking for user tokens, no Discord self-botting, no automatic claiming or sniping.** This project uses [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) to automate the process of switching to the app, navigating to the channel, and entering commands. This silly script is intended to just free up your hands while you watch the rolls go by.

## Installation

> :warning: At the moment, this application requires you to have Python >=3.10 installed.

Download the desired wheel file `waifu_roller-x.y.z-py3-none-any.whl` from the [`dist`](dist/) folder and install it with pip, preferably in a [virtual environment](https://docs.python.org/3/tutorial/venv.html):
```
(.venv) $ python -m pip install path/to/waifu_roller-x.y.z-py3-none-any.whl
```
You can verify that it's installed by running:
```
(.venv) $ python -m pip show waifu-roller
```

## Usage

The CLI command is `waifu`:
```
$ waifu wa -c waifu-spam -n 10 -d
```
This example rolls the Mudae command $wa 10 times in the channel named waifu-spam. The optional -d flag appends the daily commands $dk and $daily after the rolling session.

You can also omit arguments and opt to use the default values set in the [config.yaml](#configuration) file. This could be useful if you roll most commonly in a specific channel on a specific server.
```
$ waifu
```
As usual, use the help flag for a full list of arguments, or use the config flag to get the full path to your [configuration file](#configuration).
```
$ waifu --help
$ waifu --config
```

### Command Reference

| Argument             | Type           | Description                                                                                                                       | Example      |
| -------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| command              | positional     | Name of the Mudae command to use to roll for characters. It should be unprefixed (no $, /, etc.).                                 | 'wa'         |
| -c/--channel CHANNEL | option (1 arg) | Query string to submit to the Discord search bar to locate the channel to roll in. It should not contain whitespace.              | 'waifu-spam' |
| -n/--num NUM         | option (1 arg) | Number of times to roll in this session. Should be nonnegative.                                                                   | 10           |
| -d/--daily           | option (flag)  | Flag specifying whether the daily Mudae commands, $daily and $dailykakera, should be run in addition to the rolling this session. |              |

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

| Field                   | Type    | Description                                                                                                                                           | Default      |
| ----------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| verbose                 | boolean | Program verbosity level, and include config file path tip on --help and command error.                                                                | true         |
| revert-window           | boolean | Whether to return to the window from which script was called after rolling is completed. Waits for a short delay first. ESC aborting can cancel this. | false        |
| defaults                | mapping | Values to use when command line arguments are omitted.                                                                                                |              |
| defaults.mudae-command  | string  | Default value for the command positional arg.                                                                                                         | null (unset) |
| defaults.target-channel | string  | Default value for the -c/--channel option.                                                                                                            | null (unset) |
| defaults.num-rolls      | int     | Default value for the -n/--num option.                                                                                                                | null (unset) |

## Limitations

As of now, the builds have only been tested on my local PC, which is a Windows 11 64-bit system.

If you want to simulate my virtual environment, you can use the provided [requirements.txt](requirements.txt) after installing the wheel file:
```
(.venv) python -m pip install -r requirements.txt
```

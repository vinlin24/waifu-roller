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
As usual, use the help flag for a full list of arguments:
```
$ waifu --help
```

### Command Reference



| Argument             | Type           | Description                                                                                                                       | Example      |
| -------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| command              | positional     | Name of the Mudae command to use to roll for characters. It should be unprefixed (no $, /, etc.).                                 | 'wa'         |
| -c/--channel CHANNEL | option (1 arg) | Query string to submit to the Discord search bar to locate the channel to roll in. It should not contain whitespace.              | 'waifu-spam' |
| -n/--num NUM         | option (1 arg) | Number of times to roll in this session. Should be nonnegative.                                                                   | 10           |
| -d/--daily           | option (flag)  | Flag specifying whether the daily Mudae commands, $daily and $dailykakera, should be run in addition to the rolling this session. |              |

> :hammer: Todo: Update this reference every time a new command feature is added.

You can also use the following flags to display helpful information instead of rolling:

| Flag         | Description                          |
| ------------ | ------------------------------------ |
| -h/--help    | Display help message.                |
| -v/--version | Display version of installed script. |
| --config     | Display path of configuration file.  |


## Configuration

On first run, the script will try to initialize a configuration file for you at `~/.config/waifu-roller/config.yaml`. You can edit the program preferences here.

### Configuration Reference

> :hammer: Todo: Update this schema every time a new configuration feature is added.

| Field                   | Type    | Description                                                                            | Default      |
| ----------------------- | ------- | -------------------------------------------------------------------------------------- | ------------ |
| verbose                 | boolean | Program verbosity level, and include config file path tip on --help and command error. | true         |
| defaults                | mapping | Values to use when command line arguments are omitted.                                 |              |
| defaults.mudae-command  | string  | Default value for the command positional arg.                                          | null (unset) |
| defaults.target-channel | string  | Default value for the -c/--channel option.                                             | null (unset) |
| defaults.num-rolls      | int     | Default value for the -n/--num option.                                                 | null (unset) |

## Limitations

This project is still incomplete, and as of now, it has only been tested on my local PC, which is a Windows 11 64-bit system.

Missing (but planned) features:
- [ ] Configurable delays in the PyAutoGUI sequences
- [x] Validating command line arguments instead of just the values in the configuration file
- [ ] Option for returning to the last active window after script is complete
- [x] Including instructions on where the configuration file is and how to edit it
- [ ] Binary distributions that do not require Python installed on the user's machine
- [ ] Hotkey to pause and resume the script (to make claiming a character or kakera drop easier) in addition to the existing kill key (`ESC` at the moment)
- [ ] (:unamused: might give up on this one) Option to start the Discord desktop application if it is not already open. I tried implementing this already but it will make cross-platform coding much more challenging (differing Discord.exe locations and startfile protocols) and has an obscure problem I couldn't fix: right after startup, Ctrl+K, then typing in the channel name, sending the ENTER key causes the stupid [Learn more](https://support.discord.com/hc/en-us/articles/115000070311) link on the popup to enter focus and open the webpage

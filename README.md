# Coder's Waifu Roller

## Description

**Command line tool for rolling anime/game characters with the Discord bot [Mudae](https://top.gg/bot/432610292342587392).**

Suppose you're in the zone coding, but it's a new hour and you can roll for waifus again. Before you'd switch to Discord, find the channel, and brainlessly spam enter `$wa` or something. Now you can start the whole rolling sequence right from the command line (that you should always have open anyway :relieved:).
```
$ waifu -c waifu-spam -n 10
```

This project uses [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) to automate the process of switching to the app, navigating to the channel, and entering commands.

> :mega: **No asking for user tokens, no Discord self-botting, no automatic claiming or sniping.** This silly script is intended to just free up your hands while you watch the rolls go by.

## Installation

I'm kind of new to this whole distribution thing, so bear with my most-likely-unintuitive installation instructions. Frankly, setup.py is still magic to me, and despite all its documentation, it cannot be any more confusing to learn and debug.

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
This rolls the Mudae command $wa 10 times in the channel named waifu-spam. The -d flag appends the daily commands $dk and $daily after the rolling session.

You can also omit arguments and opt to use the default values set in the config.yaml file (work-in-progress, see warning [below](#limitations)):
```
$ waifu
```
This could be useful if you roll most commonly in a specific channel on a specific server.

## Limitations

This project is still incomplete, and as of now, it has only been tested on my local PC, which is a Windows 11 64-bit system.

Missing (but planned) features:
- [ ] Configurable delays in the PyAutoGUI sequences
- [ ] Validating command line arguments instead of just the values in the configuration file
- [ ] Option for returning to the last active window after script is complete
- [ ] Including instructions on where the configuration file is and how to edit it
> :warning: Right now it's empty so unless you know to sneak into the `site-packages`, the current distribution flat-out fails with a `ConfigFormatError` on startup lmao.
- [ ] Binary distributions that do not require Python installed on the user's machine
- [ ] Hotkey to pause and resume the script (to make claiming a character or kakera drop easier) in addition to the existing kill key (`TAB` at the moment)
- [ ] (:unamused: might give up on this one) Option to start the Discord desktop application if it is not already open. I tried implementing this already but it will make cross-platform coding much more challenging (differing Discord.exe locations and startfile protocols) and has an obscure problem I couldn't fix: right after startup, Ctrl+K, then typing in the channel name, sending the ENTER key causes the stupid [Learn more](https://support.discord.com/hc/en-us/articles/115000070311) link on the popup to enter focus and open the webpage
